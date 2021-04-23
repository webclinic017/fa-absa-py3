"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Lender sweeping to cover short SLL ACS LENDER trades
                           in SBL portfolio from long desks by booking
                           No Collateral trades.
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Danilo Mantoan
DEVELOPER               :  Peter Fabian
CR NUMBER               :  abcdef
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------

"""

from collections import defaultdict
import csv
import os
import math
import traceback
import sys

import acm
import ael
import PS_BrokerFeesRates as Rates
from PS_BrokerFeesRates import get_vat_for_date

from at import eval_ext_attr
from at_calculation_space import CalculationSpace
from SAGEN_IT_Functions import get_Port_Struct_from_Port
from sl_batch import SblSweepBatch
from sl_process_log import ProcessLog
from sl_sweeping import PositionCollection


class TradeReport(object):
    """ Create a report containing a list of trades created by the script.
    """
    def __init__(self, folder, file_name):
        """ Set the report output path and name """
        self.file_name = os.path.join(folder, file_name)
        self.rows = []
        self.fieldnames = ["Trade Number",
                           "Portfolio",
                           "CP Portfolio",
                           "Underlying",
                           "B/S",
                           "SL Rate",
                           "Original Price",
                           "Quantity",
                           "SL_ExternalInternal",
                           "StartDate",
                           "EndDate",
                           "Borrower",
                           "Fund / Lender",
                           "Instrument.OpenEnd",
                           "Trade Type",
                           "Und Type",
                           "Status",
                           "Trader",
                           "ScriptAction", ]

    def add_record(self, record_dict):
        if set(record_dict.keys()) == set(self.fieldnames):
            self.rows.append(record_dict)
        else:
            raise ValueError("Incorrect number of fields for the report")

    def write_report(self):
        with open(self.file_name, "wb") as csv_file:
            self.csv_file = csv_file
            self.dictwriter = csv.DictWriter(csv_file, self.fieldnames)
            self.dictwriter.writerow(dict((fn, fn) for fn in self.fieldnames))
            for row in self.rows:
                self.dictwriter.writerow(row)


class DeferredExceptionReporting(object):
    def __init__(self):
        self.exceptions = []

    def add(self, msg, exc_info):
        self.exceptions.append((msg, exc_info))

    def final_report(self, failed_msg, batch_no):
        if self.exceptions:
            for (msg, exc_info) in self.exceptions:
                acm.LogAll(msg)
                traceback.print_exception(*exc_info)
            raise RuntimeError(failed_msg)
        else:
            print 'Sweeping batch %s completed successfully' % batch_no


class LenderSweeper(object):
    def __init__(self, date, sbl_portfolio, traders_positions, dry_run, batch,
                 log, report):
        # positions used by sweeping -- ACS - SL vs Traders' books
        self.sbl_portfolio = sbl_portfolio
        self.traders_positions = traders_positions
        # Sweeping batch identifier (to be able to void the batch)
        self.sweeping_batch = batch
        self.sweeping_date = date
        self.log = log
        self.dry_run = dry_run
        self.verbose = True

        self.report = report

        self.vat_factor = Rates.VAT_RATE
        self.sbl_margin = 0.1
        self.epsilon = 0.0001

        # Trades from sbl portfolio
        self.sbl_trades = None
        # Buckets containing lent positions from sbl portfolsio
        # will be stored here.
        self.sbl_positions = defaultdict(
            lambda: defaultdict(lambda: defaultdict(Position)))

        # Positions in traders books
        self.traders_books = defaultdict(lambda: defaultdict(Position))
        self.exceptions = DeferredExceptionReporting()

    def _float_equal(self, number_one, number_two):
        """ Determine whether two float numbers differ at most by epsilon. """
        return abs(number_one - number_two) < self.epsilon

    def _trade_in_reserved_prf(self, trd):
        """ Return True if the trade belongs to reserved portfolio,
            otherwise return False.

            Reserved portfolio is a portfolio whose add info SL_ReservedStock
            is set to true, True, Yes, yes, indeed, of course, etc.

            Portfolios cached by self.reserved_books. It does not make
            sense to cache individual trades, but there are many
            trades in the same portfolio. To avoid repeated add info
            lookup, I used the cache.
        """
        if not hasattr(self, "reserved_books"):
            # cache: prf -> reserved prf
            self.reserved_books = {}

        prf = trd.Portfolio()
        if prf in self.reserved_books:
            return self.reserved_books[prf]

        if (prf.AdditionalInfo().SL_ReservedStock()
                and prf.AdditionalInfo().SL_ReservedStock() is True):
            self.reserved_books[prf] = True
            return True
        else:
            self.reserved_books[prf] = False
            return False

    def _trade_in_graveyard(self, trd):
        """ Return True if the trade belongs to portfolio which is
            in Graveyard. Otherwise return False.

            Cached by self.graveyard_books.
        """
        if not hasattr(self, "graveyard_books"):
            # cache: prf -> graveyard prf
            self.graveyard_books = {}

        prf = trd.Portfolio()
        if prf in self.graveyard_books:
            return self.graveyard_books[prf]

        if get_Port_Struct_from_Port(ael.Portfolio[prf.Name()], 'GRAVEYARD'):
            self.graveyard_books[prf] = True
            return True
        else:
            self.graveyard_books[prf] = False
            return False

    def _sl_portfolio_position(self, trd):
        """ Calculate value of SL_Portfolio_Position column for trade trd. """
        simulated_values = {
            'Portfolio Profit Loss End Date': 'Custom Date',
            'Portfolio Profit Loss End Date Custom': self.sweeping_date,
        }

        time_buckets = acm.Time.CreateTimeBuckets(self.sweeping_date, "'0d'",
                                                  None, None, 0, True,
                                                  False, False, False,
                                                  False)

        cs = CalculationSpace.from_source(trd)
        if not cs.values():
            raise RuntimeError("No 'SL Portfolio Position' value for trade %s"
                               % trd.Oid())
        subcs = cs.values()[0]
        for simulate_key, simulate_value in simulated_values.iteritems():
            subcs.simulate_value(simulate_key, simulate_value)

        column_config = acm.Sheet.Column().ConfigurationFromTimeBuckets(time_buckets)
        calculation = subcs.column_value("SL Portfolio Position", column_config)
        SL_port_pos = calculation.Value()
        # Handle ETFs properly. Column returns
        # FRealArray instead of float value.
        try:
            return SL_port_pos[0]
        except TypeError:
            return SL_port_pos

    def _valid_for_sweep(self, trd):
        """ Return True if a trade in ACS - Script Lending is a valid
            candidate for sweeping.
        """
        return _is_fund_lend_ACS(trd) and (self._sl_portfolio_position(trd) < 0)

    def _sweep_fee(self, orig_fee, portf):
        """ Return sweep fee from original fee on a trade.

            Fee is floored at 0. Calculated simply by dividing
            by VAT factor and subtracting margin.
        """
        if portf.add_info("SL_Zero_Fees") == 'Yes':
            return 0
        return max(0, orig_fee / self.vat_factor - self.sbl_margin)

    def _sbl_trades(self):
        """ Return list of all trades defined by _sbl_positions_query. """
        if not self.sbl_trades:
            lend_trades = _sbl_positions_query(self.sbl_portfolio,
                                               self.sweeping_date)
            self.sbl_trades = lend_trades.Select()
            self.log.Information("%s SBL Trades selected"
                                 % len(self.sbl_trades))

        return self.sbl_trades

    def _match_already_swept(self):
        """ Find sweep trades matching by (reversed) fee and ref price
            (in case of manual adjustments/reruns) and modify sbl_positions
            accordingly.

            E.g. There is a 10,000 of ABL lend from ACS - SL paying fee 0.342
            and booked at ref price 15,803.0; now if there are ABL trades
            paying fee 0.2 booked at price 15,803.0 with qty 3,000.0, we
            only need to sweep 7,000.0 of ABL at given price and fee, so
            this function adjusts sbl_positions to reflect this.
        """
        for trd in self._sbl_trades():
            if _is_internal_trd(trd):
                qty = self._sl_portfolio_position(trd)
                if self._float_equal(qty, 0):
                    continue

                # Find actual fee on the internal trade.
                fee = _trd_fee(trd)
                # Fee which should be found on the swept trade.
                # Calculated using reversed algo from SLL ACS LENDER lend
                # trade.
                reversed_fee = (fee + self.sbl_margin) * get_vat_for_date(trd.ValueDay())
                sl_und_ins_name = trd.Instrument().SLUnderlying().Name()
                ref_price = _trd_price(trd)

                # Script is working with floating point numbers,
                # so the hash table can't really be used effectively to check
                # for reversed_fee and price. Therefore, matching trades are
                # found by iterating in smallest possible subset of trades.
                match_found = False
                for trd_fee in self.sbl_positions[sl_und_ins_name]:
                    if self._float_equal(trd_fee, reversed_fee):
                        for ref_price_orig in self.sbl_positions[sl_und_ins_name][trd_fee]:
                            if self._float_equal(ref_price, ref_price_orig):
                                # Fee and price do match, adjust sbl position.
                                self.sbl_positions[sl_und_ins_name][trd_fee][ref_price_orig].change_qty(qty)
                                if self.verbose:
                                    self.log.Information("Match found -- trade %s with qty %s (fee %s, price %s)"
                                                         % (trd.Oid(), qty, ref_price_orig, trd_fee))
                                match_found = True
                                break
                    if match_found:
                        break

                if not match_found:
                    self.log.Warning("Inconsistent fee %s/ref price %s on trade %s"
                                     % (reversed_fee, ref_price, trd.Oid()))

    def _report_sbl_positions(self):
        """ Print information about the found SBL positions to log. """
        if self.verbose:
            self.log.Information("SBL positions")
            for sl_und in sorted(self.sbl_positions.keys()):
                fee_positions = self.sbl_positions[sl_und]
                for fee, price_position in fee_positions.iteritems():
                    for price, position in price_position.iteritems():
                        self.log.Information(
                                             "%s [%s][%s]: %s + %s = %s (%s trades)" %
                                             (sl_und,
                                              fee,
                                              price,
                                              sum(position.trades.values()),
                                              position.qty_adjustment,
                                              position.quantity(),
                                              len(position.trades)))

    def _build_sbl_positions(self):
        """ Create SBL positions buckets.

            Trades are bucketed by SLUnderlying, trade fee
            and ref price.
        """
        # The SLL ACS LENDER lend trades need to be identified first.
        # Only then the script can find matches and report inconsistencies.
        for trd in self._sbl_trades():
            if self._valid_for_sweep(trd):
                qty = self._sl_portfolio_position(trd)
                sl_und_ins_name = trd.Instrument().SLUnderlying().Name()
                fee = _trd_fee(trd)
                ref_price = _trd_price(trd)

                if self.verbose:
                    self.log.Information("Trade %s on und instrument %s with qty %s and fee %s" % (
                        trd.Oid(), trd.Instrument().SLUnderlying().Name(),
                        qty, fee
                        ))

                # Sweeping is done per instrument, ref price and fee amount
                # so the quantities need to be divided by these as well.
                self.sbl_positions[sl_und_ins_name][fee][ref_price].add_trade(trd, qty)

        # Identify matching trades and adjust respective buckets.
        self._match_already_swept()

        # Log what you have found.
        self._report_sbl_positions()

    def _filter_long_positions(self):
        """ Filter only long positions from traders positions
            per desk and instrument and return a dictionary
            of long positions with the same structure.
        """
        long_traders_books = defaultdict(lambda: defaultdict(Position))
        for ins_name, prf_positions in self.traders_books.iteritems():
            for desk_name, position in prf_positions.iteritems():
                if position.quantity() > 0:
                    long_traders_books[ins_name][desk_name] = position
        self.traders_books = long_traders_books
        self.log.Information("Long positions selected")

    def _report_traders_positions(self):
        """ Print information about the found traders'/desks' positions to log.
        """
        if self.verbose:
            self.log.Information("Traders' books")
            sl_unds = sorted(self.traders_books.keys())
            for sl_und in sl_unds:
                prf_positions = self.traders_books[sl_und]
                self.log.Information("%s" % (sl_und))
                for desk_name, position in prf_positions.iteritems():
                    self.log.Information("\t%s: %s (%s trades)"
                                         % (desk_name, position.quantity(),
                                            len(position.trades)))

    def _build_traders_positions(self):
        """ For each security find long desks and save relevant information
            in the traders_books dictionary.

            Using calculation space here saves time and RAM (when compared 
            with iterating over individual trades).
            Fee portfolios for each book are added automatically and included
            in the positions, too. (They must be included to get a correct
            view of the overall positions in each desk).
        """
        portfolio_grouper = acm.FAttributeGrouper('Trade.Portfolio')
        underlying_grouper = acm.FAttributeGrouper('Instrument.SLUnderlying')
        trading_desk_grouper = acm.FAttributeGrouper(
            'Trade.Portfolio.AdditionalInfo.SL_AllocatedDesk')
        calc_space = acm.Calculations().CreateCalculationSpace(
            acm.GetDefaultContext(), 'FPortfolioSheet')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Inception')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', self.sweeping_date)

        top_node = calc_space.InsertItem(self.traders_positions)
        top_node.ApplyGrouper(acm.FChainedGrouper([trading_desk_grouper,
                                                   underlying_grouper,
                                                   portfolio_grouper]))

        calc_space.Refresh()

        position_column = 'SL Portfolio Position'
        time_buckets = acm.Time.CreateTimeBuckets(self.sweeping_date, "'0d'",
                                                  None, None, 0, True, False,
                                                  False, False, False)
        column_config = acm.Sheet.Column().ConfigurationFromTimeBuckets(time_buckets)

        desk_iterator = top_node.Iterator().FirstChild()
        while desk_iterator:
            desk = desk_iterator.Tree().Item().StringKey()
            # Fee portfolio for the desk.
            desk_portfolio = self._get_desk_fee_portfolio(desk)
            if desk_portfolio is not None:
                _validate_prf(desk_portfolio)
                desk_portfolio_node = calc_space.InsertItem(desk_portfolio)
                desk_portfolio_node.ApplyGrouper(acm.FChainedGrouper([underlying_grouper]))
                calc_space.Refresh()
                instrument_iterator = desk_iterator.Clone().FirstChild()
                while instrument_iterator:
                    instrument = acm.FInstrument[instrument_iterator.Tree().Item().StringKey()]
                    # Find instrument in fee portfolio.
                    desk_portfolio_position = desk_portfolio_node.Iterator().Find(instrument)
                    if desk_portfolio_position:
                        read_quantity = calc_space.CreateCalculation(desk_portfolio_position.Tree(), position_column, column_config).Value()
                        quantity = _dearray(read_quantity)
                        if quantity:
                            self.traders_books[instrument.Name()][desk].add_trade(0, quantity)
                    portfolio_iterator = instrument_iterator.Clone().FirstChild()
                    while portfolio_iterator:
                        portfolio = acm.FPhysicalPortfolio[portfolio_iterator.Tree().Item().StringKey()]
                        
                        if portfolio.IsClone():
                            portfolio.RegisterInStorage()

                        if (portfolio.AdditionalInfo().SL_Portfolio_Type() == 'Equity'
                                and portfolio.AdditionalInfo().SL_Sweeping()):
                            read_quantity = calc_space.CreateCalculation(portfolio_iterator.Tree(), position_column, column_config).Value()
                            quantity = _dearray(read_quantity)
                            if portfolio.AdditionalInfo().SL_ReservedStock() != True or quantity < 0:
                                self.traders_books[instrument.Name()][desk].add_trade(0, quantity)
                        portfolio_iterator = portfolio_iterator.NextSibling()
                    instrument_iterator = instrument_iterator.NextSibling()
            else:
                message = 'No Fee portfolio found for trading desk [%(desk)s], please correct this and try again.' \
                    % {'desk': desk}
                self.log.Warning(message)

            desk_iterator = desk_iterator.NextSibling()

        self.log.Information("Positions selected")
        self._report_traders_positions()
        # Only the long positions are relevant (as the sweeping can only
        # sweep from long desks to SBL portfolio).
        self._filter_long_positions()

    def _get_desk_fee_portfolio(self, desk):
        """ Return the fee portfolio for given desk.

            Uses cache for faster lookups.
        """
        if not hasattr(self, "_desk_fee_portfolios"):
            # cache: desk name -> desk's fee portfolio
            self._desk_fee_portfolios = {}

        if len(self._desk_fee_portfolios) == 0:
            query = acm.CreateFASQLQuery('FPhysicalPortfolio', 'AND')
            query.AddAttrNode('AdditionalInfo.SL_Portfolio_Type', 'EQUAL', 'Fee')
            query.AddAttrNode('AdditionalInfo.SL_AllocatedDesk', 'NOT_EQUAL', None)
            query.AddAttrNode('AdditionalInfo.SL_Sweeping', 'EQUAL', True)
            for portfolio in query.Select():
                self._desk_fee_portfolios[portfolio.AdditionalInfo().SL_AllocatedDesk()] = portfolio
        return self._desk_fee_portfolios.get(desk)

    def _float_less_than_equal(self, num_one, num_two):
        """ Perform 'num_one <= num_two', but allows for
            some minor differences and inaccuracies when
            working with float numbers, so that e.g.
            9.0005 <= 9.0004 is True.
        """
        return num_one < num_two or self._float_equal(num_one, num_two)

    def _desk_can_lend(self, desk_name, ins_name, amount):
        """ Return True if desk is at least 'amount' long in security
            'ins_name'.
        """
        available_amount = self.traders_books[ins_name][desk_name].quantity()
        return self._float_less_than_equal(amount,
                                           available_amount)

    def _determine_qties_per_desk(self, ins_name, sbl_position):
        """ Determine the quantity to sweep for sbl position bucket and split
            the quantity among desks which are long in the particular
            instrument.

            Return a dictionary mapping: desk name -> qty to sweep

            Sbl position is a bucket of trades with the same
            sl underlying, fee and ref price.

            Quantity to sweep is smaller of the following numbers:
                - available long quantity in traders' books
                - qty of lend trades in ACS - Script Lending portfolio

            This sweep quantity is then split among desks based on the
            available qty for each desk. First each desk is assigned
            a floor(qty_to_sweep * (qty_avail_in_this_desk/qty_in_all_desks))
            and then we iterate with what is left and try to split
            the remaining qty again. If we could not divide everything
            this way then the leftover is assigned to the desk with
            largest available quantity.
        """
        qty_to_sweep_for = defaultdict(int)
        desk_positions = self.traders_books[ins_name]
        # quantity() method has to be used here (not a direct member access)
        # because the overall quantity is adjusted as the instrument
        # is being swept.
        qty_in_traders_books = sum([pos.quantity()
                                    for pos in desk_positions.values()])
        qty_to_sweep = int(round(min(abs(sbl_position.quantity()),
                                     qty_in_traders_books)))

        if not abs(qty_in_traders_books) > self.epsilon:
            return qty_to_sweep_for

        self.log.Information("Qty in traders books: %s" % qty_in_traders_books)
        for desk_name, traders_position in desk_positions.iteritems():
            self.log.Information("\t%s: %s (of %s trades)"
                                 % (desk_name, traders_position.quantity(),
                                    len(traders_position.trades)))

        left_after_rounding = qty_to_sweep

        # Qty is divided roughly among the desks first, round down (i.e. floor)
        while left_after_rounding != 0:
            for desk_name, traders_position in desk_positions.iteritems():
                addition_for_prf = int(math.floor(
                    left_after_rounding * (traders_position.quantity()
                                           / qty_in_traders_books)))
                # addition_for_prf can only be added if the desk is long enough.
                amount_to_be_swept = (qty_to_sweep_for[desk_name]
                                      + addition_for_prf)
                if self._desk_can_lend(desk_name, ins_name,
                                       amount_to_be_swept):
                    qty_to_sweep_for[desk_name] += addition_for_prf

            # If the qty left for sweeping couldn't be divided among the desks
            # (i.e. the current leftover is the same as would be
            # the next one), the leftover has to be swept one by one,
            # because it might happen that there are e.g. 3 desks, each
            # has a spare qty 1, but neither desk can accept qty of 3.
            next_left_after_rounding = int(round(qty_to_sweep
                                                 - sum(qty_to_sweep_for.values())))
            if self._float_equal(left_after_rounding,
                                 next_left_after_rounding):
                while left_after_rounding != 0:
                    desk_to_use_for_one = None
                    for desk_name in desk_positions.keys():
                        # addition_for_prf can only be added if the desk
                        # is long enough.
                        amount_to_be_swept = (qty_to_sweep_for[desk_name] + 1)
                        if self._desk_can_lend(desk_name, ins_name,
                                               amount_to_be_swept):
                            desk_to_use_for_one = desk_name
                            break

                    if desk_to_use_for_one:
                        qty_to_sweep_for[desk_to_use_for_one] += 1
                        left_after_rounding -= 1
                    else:
                        # This should not happen, as the qty for sweeping is
                        # always at most the qty in traders books, but because
                        # of rounding it sometimes leaves some spare qty.
                        self.log.Warning("There is no desk which could accept this sweeping")
                        break
                # Once the script got here, there is no need to iterate more
                # in the outer while loop, because either everything has been
                # split, or there is no desk to accept the leftover (which is
                # handled above)
                break
            else:
                left_after_rounding = int(round(qty_to_sweep
                                                - sum(qty_to_sweep_for.values())))

        return qty_to_sweep_for

    def _log_trade_creation(self, trdnbr, counterparty_portfolio,
                            acquirer_portfolio, qty, return_fee, ref_price):
        self.log.Information("Book trd |%s| prf: |%s| cp-prf: |%s| qty |%s| fee |%s| @ |%s|"
                             % (trdnbr,
                                acquirer_portfolio.Name(),
                                counterparty_portfolio.Name(),
                                qty,
                                return_fee,
                                ref_price))

        if self.report and not self.dry_run:
            trade = acm.FTrade[trdnbr]
            qty_to_sweep_for_desk = trade.QuantityInUnderlying()
            sl_und = trade.Instrument().SLUnderlying()
            leg = trade.Instrument().Legs()[0]
            report_rec = {"Trade Number": trdnbr,
                          "Portfolio": trade.Portfolio().Name(),
                          "CP Portfolio": trade.CounterPortfolio().Name(),
                          "Underlying": sl_und.Name(),
                          "B/S": "Buy" if qty_to_sweep_for_desk > 0 else "Sell",
                          "SL Rate": _trd_fee(trade),
                          "Original Price": _trd_price(trade),
                          "Quantity": qty_to_sweep_for_desk,
                          "SL_ExternalInternal": trade.Instrument().AdditionalInfo().SL_ExternalInternal(),
                          "StartDate": leg.StartDate(),
                          "EndDate": leg.EndDate(),
                          "Borrower": trade.AdditionalInfo().SL_G1Counterparty1(),
                          "Fund / Lender": trade.AdditionalInfo().SL_G1Counterparty2(),
                          "Instrument.OpenEnd": trade.Instrument().OpenEnd(),
                          "Trade Type": trade.Type(),
                          "Und Type": trade.Instrument().Underlying().InsType(),
                          "Status": trade.Status(),
                          "Trader": trade.Trader().Name(),
                          "ScriptAction": "New Trade",
                          }
            self.report.add_record(report_rec)

    def _sweep(self):
        """ Perform lender sweeping.

            Determine quantities to sweep, book trades and log the bookings.
        """
        for ins_name in sorted(self.sbl_positions.keys()):
            sbl_position_for_ins = self.sbl_positions[ins_name]
            for fee, price_sbl_position in sbl_position_for_ins.iteritems():
                for ref_price, sbl_position in price_sbl_position.iteritems():
                    self.log.Information("Sweeping ins %s fee %s ref price %s"
                                         % (ins_name, fee, ref_price))
                    self.log.Information("Qty in ACS - Script Lending: %s (of %s trades)"
                                         % (sbl_position.quantity(),
                                            len(sbl_position.trades)))

                    if (not abs(sbl_position.quantity()) > self.epsilon
                            or not len(sbl_position.trades)):
                        continue

                    if sbl_position.quantity() > self.epsilon:
                        self.log.Information("Overswept for this bucket, don't sweep more")
                        continue

                    for trd in sbl_position.trades:
                        self.log.Information("\tsbl trade %s fee %s"
                                             % (trd.Oid(), fee))

                    # prepare desk -> qty dict
                    qty_to_sweep_for = self._determine_qties_per_desk(ins_name,
                                                                      sbl_position)
                    self.log.Information("Sweeping qty %s for %s"
                                         % (sum(qty_to_sweep_for.values()),
                                            ins_name))

                    try:
                        # Book trades according to quantities per desk.
                        for desk_name, qty_to_sweep_for_desk in qty_to_sweep_for.iteritems():
                            if abs(qty_to_sweep_for_desk) < self.epsilon:
                                continue
                            
                            acquirer_portfolio = sbl_position.trades.keys()[0].Portfolio()
                            instrument = acm.FInstrument[ins_name]
                            start_date = self.sweeping_date
                            counterparty_portfolio = self._get_desk_fee_portfolio(desk_name)
                            return_fee = self._sweep_fee(fee, counterparty_portfolio)

                            # Open End needs to be set to None so that the
                            # booked Sec Loans are only valid for the period
                            # for which they are booked (1 day).
                            open_end = "None"
                            trdnbr = 0
                            int_external = "No Collateral"
                            book_cfd = False
                            if not self.dry_run:
                                trdnbr = PositionCollection.bookSecurityLoan(self.sweeping_batch.BatchNumber,
                                                                             open_end,
                                                                             acquirer_portfolio,
                                                                             instrument,
                                                                             qty_to_sweep_for_desk,
                                                                             start_date,
                                                                             counterparty_portfolio,
                                                                             int_external,
                                                                             return_fee,
                                                                             ref_price,
                                                                             book_cfd)

                            self._log_trade_creation(trdnbr, counterparty_portfolio,
                                                     acquirer_portfolio,
                                                     qty_to_sweep_for_desk,
                                                     return_fee, ref_price)

                            # Adjust the qty available in desk's portfolios
                            # (so that the script does not sweep more than is
                            # available on the desk and it uses new amounts
                            # for qty weighted distribution.
                            desk_positions = self.traders_books[ins_name]
                            traders_position = desk_positions[desk_name]
                            traders_position.change_qty(-1 * qty_to_sweep_for_desk)
                    except Exception:
                        error_str = "Could not sweep %s for desk %s" % (ins_name,
                                                                        desk_name)
                        self.exceptions.add(error_str, sys.exc_info())

    def sweep(self):
        self.log.Information("Selecting sbl positions")
        self._build_sbl_positions()
        self.log.Information("Selecting traders positions")
        self._build_traders_positions()
        self.log.Information("Sweeping")
        self._sweep()
        self.log.Information("Sweeping done")
        self.exceptions.final_report("Sweeping failed",
                                     self.sweeping_batch.BatchNumber)


def _is_fund_lend_ACS(trd):
    if trd.IsClone():
        trd.RegisterInStorage()
    return trd.AdditionalInfo().SL_G1Counterparty2() == "SLL ACS LENDER"


def _no_fund_lend(trd):
    if trd.IsClone():
        trd.RegisterInStorage()
    return (not trd.AdditionalInfo().SL_G1Counterparty2())


def _trd_fee(trd):
    """ Return fixed rate of first leg of trade's instrument.
        This is often referred to as Fee in SL space (also the field
        on the Sec Loan trade ticket in Front shows this rate labelled
        as Fee).
    """
    return trd.Instrument().Legs()[0].FixedRate()


def _is_internal_trd(trd):
    """ Return True if trade trd is an internal No Collateral trade. """
    return (_no_fund_lend(trd)
            and trd.Counterparty().Type() == 'Intern Dept'
            and trd.Instrument().AdditionalInfo().SL_ExternalInternal() == 'No Collateral')


def _trd_price(trd):
    return trd.RefPrice()


def _sbl_positions_query(portfolio_name, date):
    """ Return query folder containing all current valid trades from specified
        portfolio.

        By valid trade the following is assumed:
        Simulated and Void trades are excluded.
        Only Security Loans (SLs) valid for specified date are included:
            - OpenEnd SLs: start date <= date <= end date
            - None SLs: start date == date
            - Terminated SLs: start date <= date < end date
    """
    # identify lend trades from ACS - Script Lending
    lend_trades = acm.CreateFASQLQuery('FTrade', 'AND')
    lend_trades.AddAttrNode('Status', 'NOT_EQUAL',
                            acm.EnumFromString('TradeStatus', 'Simulated'))
    lend_trades.AddAttrNode('Status', 'NOT_EQUAL',
                            acm.EnumFromString('TradeStatus', 'Void'))
    lend_trades.AddAttrNode('Instrument.InsType', 'EQUAL',
                            acm.EnumFromString('InsType', 'SecurityLoan'))
    lend_trades.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio_name)
    lend_trades.AddAttrNode('Aggregate', 'EQUAL', 0)
    # select only active trades
    orNode = lend_trades.AddOpNode('OR')
    # Open End -> start date <= sweep date <= end date
    open_end_node = orNode.AddOpNode("AND")
    open_end_node.AddAttrNode('Instrument.OpenEnd', 'EQUAL',
                              acm.EnumFromString('OpenEndStatus',
                                                 'Open End'))
    open_end_node.AddAttrNode('Instrument.Legs.StartDate',
                              'LESS_EQUAL', date)
    open_end_node.AddAttrNode('Instrument.Legs.EndDate',
                              'GREATER_EQUAL', date)

    # None -> start date == sweep date
    none_oe_node = orNode.AddOpNode("AND")
    # can't fetch value for None string using EnumFromString function
    none_oe_node.AddAttrNode('Instrument.OpenEnd', 'EQUAL', 0)
    none_oe_node.AddAttrNode('Instrument.Legs.StartDate', 'EQUAL', date)

    # Terminated -> start date <= sweep date < end date
    terminated_node = orNode.AddOpNode("AND")
    terminated_node.AddAttrNode('Instrument.OpenEnd', 'EQUAL',
                                acm.EnumFromString('OpenEndStatus',
                                                   'Terminated'))
    terminated_node.AddAttrNode('Instrument.Legs.StartDate',
                                'LESS_EQUAL', date)
    terminated_node.AddAttrNode('Instrument.Legs.EndDate',
                                'GREATER', date)

    return lend_trades


def _dearray(val_):
    """ Unpack value from the array if val_ is an array, else return val_. """
    try:
        return val_[0]
    except TypeError:
        return val_


def _validate_prf(portfolio):
    """ Raise exception if portfolio's owner is not an internal department. """
    owner = portfolio.PortfolioOwner()
    if owner:
        ownerType = owner.Type()
        if ownerType != 'Intern Dept':
            raise Exception("Portfolio [%(portfolio)s], owned by [%(owner)s] of type [%(ownerType)s], is not valid. It is not owned by an internal department. The portfolio owner must be of type 'Intern Dept'" % \
                {'portfolio': portfolio.Name(), 'owner': owner.Name(), 'ownerType': ownerType})
    else:
        raise Exception("Portfolio [%s] is not valid, since it has no owner." % portfolio.Name())


class Position(object):
    def __init__(self):
        # Qty per trade store.
        self.trades = defaultdict(float)
        # Resulting qty is qty of trades plus qty adjustment.
        self.qty_adjustment = 0
        self.epsilon = 0.0001

    def add_trade(self, trd, qty):
        """ Add a record for trade trd storing qtuantity of qty. """
        if abs(qty) > self.epsilon:
            self.trades[trd] += qty

    def quantity(self):
        """ Return total quantity for this position. """
        return sum(self.trades.values()) + self.qty_adjustment

    def change_qty(self, qty):
        """ Adjust total quantity of the position. """
        self.qty_adjustment += qty

    def trades(self):
        """ Return a list of all trades in this position. """
        return self.trades.keys()

# Variable Name, Display Name, Type, Candidate Values,
# Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [['sbl_portfolio', "SBL Portfolio", "FPhysicalPortfolio", None,
                  None, 1, 0, "", None, 1],
                 ['traders_books', "Traders Positions Filter", "FStoredASQLQuery", None,
                  None, 1, 0, "", None, 1],
                 ['date', 'Date', 'string', None,
                  str(acm.Time.DateToday()), 1, 0, 'Sweeping Date', None, 1],
                 ['dry_run', 'Dry run', 'string', ["Yes", "No"],
                  1, 1, 0, "Don't book trades", None, 1],

                 ['folder', 'Report Folder', 'string', None,
                  "", 0, 0, "Folder where to put trade report", None, 1],
                 ['file_name', 'Report File name', 'string', None,
                  "", 0, 0, "File name of the trade report", None, 1], ]


def ael_main(ael_dict):

    date = ael_dict['date']
    if date.upper() == "TODAY":
        date = acm.Time.DateToday()

    # sbl positions query
    sbl_portfolio = ael_dict['sbl_portfolio'].Name()

    # traders' positions query
    traders_books_trades = ael_dict['traders_books'].Query()

    dry_run = ael_dict['dry_run'] == "Yes"

    batch = None
    if not dry_run:
        batch = SblSweepBatch.CreateBatch(date)

    folder = ael_dict['folder']
    file_name = ael_dict['file_name']
    report = None
    if folder and file_name:
        report = TradeReport(folder, file_name)

    log = ProcessLog('SBL Lending Prop Stock')
    log.Information("Running Lending Prop Stock with the following parameters")
    log.Information("SBL Portfolio: %s" % sbl_portfolio)
    log.Information("Traders positions: %s" % ael_dict['traders_books'].Name())
    log.Information("Sweeping date: %s" % date)
    log.Information("Dry run: %s" % dry_run)
    if not dry_run:
        log.Information("Sweeping Batch no: %s" % batch.BatchNumber)

    sweeper = LenderSweeper(date, sbl_portfolio, traders_books_trades,
                            dry_run, batch, log, report)
    sweeper.sweep()

    report.write_report()
    log.Information("Wrote secondary output to: %s" % report.file_name)
