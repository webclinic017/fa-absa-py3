'''-----------------------------------------------------------------------
MODULE
    PS_AllocateTradesSplit

DESCRIPTION
    Date                : 2011-07-15
    Purpose             : Split the allocation trades, created from the PS_AllocateTrades script,
                          into seperate portfolios.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Herman Hoon
    CR Number           : 713436 
    
HISTORY
================================================================================
Date       Change no       Developer          Description
--------------------------------------------------------------------------------
2011-07-15 713436          Herman Hoon        Initial Implementation
2011-07-18 715943          Herman Hoon        Correct portfolio name in log and added premium to split trade
2012-05-28 229824          Nidheesh Sharma    Catered for the CSV file that is read to have a fourth column called Quantity
2012-06-18  C278377        Peter Kutnik       Removed rounding of prices
2012-08-03  C368743        Peter Fabian       Added support for VWAP in csv, changed error message to a more meaningful one
2014-04-30  1937295        Hynek Urban        Allow for mixed (CFD & General) allocation accounts.
2014-06-16  2054154        Ondrej Bahounek    Validate target porfolios (if are physical and existing).
                                              During creating split trade: check if already exists (with Simulated status)
                                              and update it instead of aborting script with error.
                                              If trade can't be voided, create split trades anyway.
2014-08-12  2194554        Ondrej Bahounek    Sort instruments by name.
2015-10-06  3139848        Ondrej Bahounek    XtpTradeType relation completely removed.
2019-06-13  CHG1001882656  Tibor Reiss        Create trade also in allocation portfolio
2019-09-13  CHG1002255241  Tibor Reiss        FAU-308: FA Upgrade (StorageNew doesn't work on clone)
2019-09-16  INC1014719870  Tibor Reiss        Roll back: addinfo should be outside of transaction (in production the
                                              transaction did not work but could not reproduce in dev environment)
ENDDESCRIPTION
-----------------------------------------------------------------------'''

import csv
import os
from logging import DEBUG, INFO

import acm
import FRunScriptGUI

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_addInfo import save as ai_save
from PS_AllocateTrades import (COL_NR_STOCK, COL_NR_BUY_SELL, COL_NR_PRICE, COL_NR_QUANTITY, COL_NR_FIRST_FUND,
                               FUNDS_COL, ALLOCATE_SECTION, XTP_TRADE_TYPE_ALLOCATION, STOCK_LIST,
                               query_get_block_trades)


LOGGER = getLogger(__name__)
FILE_FILTER = "*.csv"
INPUT_FILE = FRunScriptGUI.InputFileSelection(FileFilter=FILE_FILTER)
ZAR_CALENDAR = acm.FCalendar['ZAR Johannesburg']
INCEPTION = acm.Time().DateFromYMD(1970, 1, 1)
TODAY = acm.Time().DateToday()
FIRSTOFYEAR = acm.Time().FirstDayOfYear(TODAY)
FIRSTOFMONTH = acm.Time().FirstDayOfMonth(TODAY)
YESTERDAY = acm.Time().DateAddDelta(TODAY, 0, 0, -1)
TWODAYSAGO = acm.Time().DateAddDelta(TODAY, 0, 0, -2)
PREVBUSDAY = ZAR_CALENDAR.AdjustBankingDays(TODAY, -1)
TWOBUSDAYSAGO = ZAR_CALENDAR.AdjustBankingDays(TODAY, -2)

# Generate date lists to be used as drop downs in the GUI.
startDateList = {'Inception':INCEPTION,
                 'First Of Year':FIRSTOFYEAR,
                 'First Of Month':FIRSTOFMONTH,
                 'PrevBusDay':PREVBUSDAY,
                 'TwoBusinessDaysAgo':TWOBUSDAYSAGO,
                 'TwoDaysAgo':TWODAYSAGO,
                 'Yesterday':YESTERDAY,
                 'Custom Date':TODAY,
                 'Now':TODAY}
startDateKeys = startDateList.keys()
startDateKeys.sort()


class Position(object):
    def __init__(self, trade, instrument_name, portfolio_name, buysell):
        self.trades = []
        self.alloc_trade_oid = trade.Oid()
        self.alloc_instrument = acm.FInstrument[instrument_name]
        self.alloc_buysell = buysell
        self.alloc_portfolio_name = portfolio_name
        self.alloc_quantity = trade.Quantity()
        self.alloc_price = trade.Price()
        self.alloc_quotation = self.alloc_instrument.Quotation().Name()

    def __lt__(self, other):
        return self.alloc_instrument.Name() < other.alloc_instrument.Name()

    def split_trades(self, allocations):
        ''' Split the position into allocation trades.
        '''
        stock_code = self.alloc_instrument.Name()
        key = (stock_code, self.alloc_buysell)
        if key in allocations:
            fund_quantities = allocations[key]
        else:
            msg = ("Failed to get the position {} / {} / {} in the allocation file."
                   .format(self.alloc_portfolio_name, stock_code, self.alloc_buysell))
            LOGGER.error(msg)
            raise RuntimeError(msg)
        if fund_quantities:
            total_quantity = sum(fund_quantities.values())
            if total_quantity != self.alloc_quantity:
                msg = ("Total quantity {} in file does not equal the quantity {} for position {} / {} / {}"
                       .format(total_quantity, self.alloc_quantity,
                               self.alloc_portfolio_name,
                               stock_code, self.alloc_buysell))
                LOGGER.error(msg)
                raise RuntimeError(msg)
            else:
                for portfolio_name in fund_quantities.iterkeys():
                    quantity = fund_quantities[portfolio_name]
                    portfolio = acm.FPhysicalPortfolio[portfolio_name]
                    if quantity and quantity != 0.0:
                        if portfolio:
                            self.__create_both_trades(quantity, portfolio)
                        else:
                            msg = ("Failed to get the portfolio {} specified "
                                   "in the file for position {} / {} / {}"
                                   .format(portfolio_name, self.alloc_portfolio_name, stock_code, self.alloc_buysell))
                            LOGGER.error(msg)
                            raise RuntimeError(msg)
            try:
                trade = acm.FTrade[self.alloc_trade_oid]
                trade.Status('Void')
                trade.Commit()
            except:
                msg = ("Could not void block trade {} / {} / {}."
                       .format(self.alloc_portfolio_name, stock_code, self.alloc_buysell))
                LOGGER.exception(msg)
                raise RuntimeError(msg)
        else:
            msg = ("Empty list for fund quantities {} / {} / {} in the allocation file."
                   .format(self.alloc_portfolio_name, stock_code, self.alloc_buysell))
            LOGGER.error(msg)
            raise RuntimeError(msg)

    def __create_both_trades(self, quantity, portfolio):
        ''' Creates split trade:
              one in client portfolio
              one in alloc portfolio with opposite sign
        '''
        acm.BeginTransaction()
        try:
            trade = acm.FTrade[self.alloc_trade_oid]
            t_clone = self.__create_trade(trade, quantity, portfolio, False)
            t_clone.Commit()
            t_clone2 = self.__create_trade(trade, quantity, portfolio, True)
            t_clone2.Commit()
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            msg = "Failed creating split trade."
            LOGGER.exception(msg)
            raise RuntimeError(msg)
        acm.PollDbEvents()
        acm.BeginTransaction()
        try:
            t_clone.Contract(self.alloc_trade_oid)
            t_clone.ConnectedTrade(t_clone.Oid())
            t_clone.Commit()
            t_clone2.Contract(t_clone.Oid())
            t_clone2.ConnectedTrade(t_clone2.Oid())
            t_clone2.Commit()
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            msg = "Could not update contract/connect trade numbers."
            LOGGER.exception(msg)
            raise RuntimeError(msg)
        acm.PollDbEvents()
        try:
            ai_save(t_clone, "XtpTradeType", XTP_TRADE_TYPE_ALLOCATION)
            ai_save(t_clone2, "XtpTradeType", XTP_TRADE_TYPE_ALLOCATION)
        except:
            msg = "Could not update addinfo XtpTradeType."
            LOGGER.exception(msg)
            raise RuntimeError(msg)
        self.trades.append(t_clone2)

    def __create_trade(self, block_trade, quantity, portfolio, is_client_trade):
        premium = quantity * self.alloc_price
        if self.alloc_quotation == "Per 100 Units":
            premium = premium / 100.0
        t_clone = block_trade.StorageNew()
        if not is_client_trade:
            t_clone.Portfolio(acm.FPhysicalPortfolio[self.alloc_portfolio_name])
            t_clone.Quantity(-1.0 * quantity)
            t_clone.Premium(premium)
        else:
            t_clone.Portfolio(portfolio)
            t_clone.Quantity(quantity)
            t_clone.Premium(-1.0 * premium)
        t_clone.Price(self.alloc_price)
        t_clone.Status('Simulated')
        payments = t_clone.Payments()
        factor = quantity / self.alloc_quantity
        for payment in payments:
            amount = factor * payment.Amount()
            payment.Amount(amount)
        return t_clone


def generate_allocation_positions(query):
    positions = []
    portfolio_grouper = acm.FAttributeGrouper('Trade.Portfolio')
    buy_sell_grouper = acm.Risk.GetGrouperFromName('Trade BuySell')

    calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
    top_node = calc_space.InsertItem(query)
    top_node.ApplyGrouper(acm.FChainedGrouper([portfolio_grouper, buy_sell_grouper]))
    calc_space.Refresh()

    if top_node.NumberOfChildren():
        portfolio_iter = top_node.Iterator().Clone().FirstChild()
        while portfolio_iter:
            portfolio_name = portfolio_iter.Tree().Item().StringKey()
            LOGGER.debug("Processing portfolio {}".format(portfolio_name))
            buysell_iter = portfolio_iter.Clone().FirstChild()
            while buysell_iter:
                buysell = buysell_iter.Tree().Item().StringKey()
                LOGGER.debug("\tBuysell {}".format(buysell))
                instrument_iter = buysell_iter.Clone().FirstChild()
                while instrument_iter:
                    trade_list = instrument_iter.Tree().Item().Trades().AsList()
                    instrument_name = instrument_iter.Tree().Item().StringKey()
                    LOGGER.debug("Instrument {}".format(instrument_name))
                    if len(trade_list) > 1:  # Should actually never happen. Legacy message.
                        LOGGER.error("Position {} / {} / {} contains more than one trade ({}), "
                                     "please run the allocation process before splitting."
                                     .format(portfolio_name, instrument_name, buysell, trade_list))
                    elif len(trade_list) == 0:
                        LOGGER.info("Position {} / {} / {} contains no trades."
                                    .format(portfolio_name, instrument_name, buysell))
                    else:
                        trade = trade_list[0]
                        positions.append(Position(trade, instrument_name, portfolio_name, buysell))
                    instrument_iter = instrument_iter.NextSibling()
                buysell_iter = buysell_iter.NextSibling()
            portfolio_iter = portfolio_iter.NextSibling()
    return positions


def generate_query_for_split_trades(portfolio_list, date, stocks_list=None):
    ''' Generate a query that selects all split trades created on "date".
    '''
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))

    or_node = query.AddOpNode('OR')
    or_node.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'Stock'))
    or_node.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'ETF'))

    query.AddAttrNode('TradeTime', 'GREATER_EQUAL', date)
    query.AddAttrNode('TradeTime', 'LESS_EQUAL', date)

    query.AddAttrNode('AdditionalInfo.XtpTradeType', 'EQUAL', XTP_TRADE_TYPE_ALLOCATION)

    if stocks_list:
        or_node = query.AddOpNode('OR')
        for stock in stocks_list:
            or_node.AddAttrNode('Instrument.Name', 'EQUAL', stock.Name())

    or_node = query.AddOpNode('OR')
    for pf_name in portfolio_list:
        or_node.AddAttrNode('Portfolio.Name', 'EQUAL', pf_name)
    return query


def void_previously_generated_split_trades(allocations, date, alloc_portfolio, stocks_list=None):
    ''' Void all the split trades created on "date". '''
    portfolios = allocations[allocations.keys()[0]].keys()
    portfolios.append(alloc_portfolio.Name())
    candidate_trades = generate_query_for_split_trades(portfolios, date, stocks_list).Select()
    trades = [t for t in candidate_trades if t.Oid() != t.Contract().Oid()
                                             and not t.OptionalKey().startswith("XTP_JSE")]
    acm.BeginTransaction()
    try:
        for t in trades:
            t_clone = t.Clone()
            t_clone.Status("Void")
            t.Apply(t_clone)
            t.Commit()
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        msg = "Could not void previously generated split trades"
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def read_allocations(filepath, date):
    ''' Read the allocations from the file.
    '''
    if not os.path.exists(filepath):
        msg = "ERROR: File: '{}' does not exist".format(filepath)
        display_message("Incorrect Input", msg)
        return None

    allocations = {}
    funds = []
    allocation_flag = False
    row_quantity_check_fail = []
    allocation_file = open(filepath, 'rU')

    try:
        reader = csv.reader(allocation_file)
        for row in reader:
            try:
                column1 = row[COL_NR_STOCK].strip()
                total_quantity = 0.0

                if allocation_flag:
                    if column1 == FUNDS_COL:
                        column_counter = COL_NR_FIRST_FUND
                        count_row = len(row)- column_counter
                        for i in range(count_row):
                            column_counter = COL_NR_FIRST_FUND + i
                            value = row[column_counter].strip()
                            if value != '':
                                funds.append(value)
                    else:
                        count_funds = len(funds)
                        funds_dict = {}
                        for i in range(count_funds):
                            column_counter = COL_NR_FIRST_FUND + i
                            # If quantity cell is blank then use 0.0
                            quantity = 0.0
                            if row[column_counter].strip() != '':
                                quantity = float(row[column_counter].strip())
                            fund = funds[i]
                            funds_dict[fund] = quantity
                            total_quantity = total_quantity + funds_dict[fund]

                        key = row[COL_NR_STOCK].strip(), row[COL_NR_BUY_SELL].strip()
                        allocations[key] = funds_dict

                        # Sanity check to ensure total quantity matches partial quantities in file
                        if total_quantity != float(row[COL_NR_QUANTITY].strip()):
                            row_quantity_check_fail.append(row)

                if column1 == ALLOCATE_SECTION:
                    allocation_flag = True
                elif column1 == '':
                    allocation_flag = False

            except Exception, err:
                msg = 'ERROR: Failed to read quantities for row %s : %s' %(row, err)
                raise RuntimeError(msg)

        # display message if there are rows in the csv whose total quantity doesn't match the partial quantities
        if row_quantity_check_fail:
            row_list = ""
            for r in row_quantity_check_fail:
                for rowColumns in r:
                    row_list = row_list + rowColumns + " "
                row_list = row_list + '\n'
            msg = "ERROR: Total quantity does not match partial quantities for rows: \n%s" % row_list
            raise RuntimeError(msg)

        if not allocations:
            msg = "ERROR: Input file is not correctly formatted. Check its header rows."
            raise RuntimeError(msg)

    except Exception, err:
        msg = 'ERROR: Failed to read input file: %s' % err
        display_message("File Read Error", msg)
        allocations = None
    finally:
        allocation_file.close()
    return allocations


def enable_custom_start_date(field_values):
    '''hook'''
    date_custom = ael_variables.get('dateCustom')
    date_custom.enabled = (field_values.value == 'Custom Date')
    return field_values


ael_variables = AelVariableHandler()
ael_variables.add(
    'date',
    label='Date',
    cls='string',
    collection=startDateKeys,
    default='Now',
    mandatory=True,
    multiple=False,
    alt='Date for witch the file should be selected.',
    hook=enable_custom_start_date,
    )
ael_variables.add(
    'dateCustom',
    label='Date Custom',
    cls='string',
    default=TODAY,
    mandatory=False,
    multiple=False,
    alt='Custom date',
    enabled=False
    )
ael_variables.add(
    'portfolio',
    label='Allocation Portfolio',
    cls='FPhysicalPortfolio',
    mandatory=True,
    alt='Allocation Portfolio for stocks.'
    )
ael_variables.add(
    'stocks',
    label='Stock List',
    cls='FInstrument',
    collection=STOCK_LIST,
    default=None,
    mandatory=False,
    multiple=True,
    alt='Instrument List. If blank, will run for all instruments.'
    )
ael_variables.add(
    'input_file',
    label='File',
    cls=INPUT_FILE,
    default=INPUT_FILE,
    mandatory=True,
    multiple=True,
    alt='Input file.'
    )
ael_variables.add(
    'logging_level',
    label='Logging level',
    cls='int',
    collection=[DEBUG, INFO],
    default=INFO,
    mandatory=False,
    multiple=False
    )
ael_gui_parameters = {'windowCaption':'Prime Broker: 2nd Allocation Script'}


def error_in_portfolios(allocations):
    ''' Validate portfolios: must exist and be physical.
    '''
    portfolios = allocations[allocations.keys()[0]].keys()
    bad_portf = []
    for portf in portfolios:
        p = acm.FPhysicalPortfolio[portf]
        if p is None or p.Compound():
            bad_portf.append(portf)
    return bad_portf


def display_message(title, msg):
    print(msg)
    func = acm.GetFunction('msgBox', 3)
    func(title, msg, 0)


def ael_main(ael_dict):
    LOGGER.setLevel(ael_dict['logging_level'])
    LOGGER.msg_tracker.reset()

    if ael_dict['date'] == 'Custom Date':
        date = ael_dict['dateCustom']
    else:
        date = startDateList[ael_dict['date']]
    alloc_portfolio = ael_dict['portfolio']
    input_file = str(ael_dict['input_file'])
    allocations = read_allocations(input_file, date)
    if not allocations:
        # The next check is needed in case all trades in a stock are voided
        if not ael_dict['stocks']:
            void_previously_generated_split_trades(allocations, date, alloc_portfolio, ael_dict['stocks'])
        return

    err = error_in_portfolios(allocations)
    if err:
        msg = 'ERROR: Target portfolio(s) not valid:\n' + ("\n".join(err))
        display_message("Portfolio Check", msg)
        return

    void_previously_generated_split_trades(allocations, date, alloc_portfolio, ael_dict['stocks'])
    query = query_get_block_trades([alloc_portfolio], date, ael_dict['stocks'])
    positions = generate_allocation_positions(query)
    if positions:
        positions.sort()
        LOGGER.info("\n{}".format('*' * 90))
        LOGGER.info("Processing positions for {}, date {}........\n".format(alloc_portfolio.Name(), date))
        LOGGER.info("{0:{width}}{1:{width}}{2:{width2}}{3:{width2}}{4}"
                    .format('STOCK', 'POSITION', 'PRICE', 'BLOCK TRADE', 'SPLIT TRADES', width=12, width2=15))
        LOGGER.info("{und_s:{width}}{und_l:{width}}{und_s:{width2}}{und_ll:{width2}}{und_ll}"
                    .format(und_s='=======', und_l='==========', und_ll='===========', width=12, width2=15))

        for pos in positions:
            try:
                pos.split_trades(allocations)
                trades = [t.Oid() for t in pos.trades]
                LOGGER.info("{0:{width}}{1:{width}}{2:{width2}}{3:{width2}}{4}"
                            .format(pos.alloc_instrument.Name(), str(pos.alloc_quantity), str(pos.alloc_price),
                                    str(pos.alloc_trade_oid), trades, width=12, width2=15))
            except:
                LOGGER.exception("Error while splitting block trade {0} for "
                                 "position {1} / {2} / {3}: \n"
                                 .format(pos.alloc_trade_oid, pos.alloc_portfolio_name,
                                         pos.alloc_instrument.Name(), pos.alloc_buysell))

        LOGGER.info('\n')
        print('\n', '*'*90)
    else:
        LOGGER.info("WARNING: No allocate positions in portfolio {0},"
                    "make sure the portfolio has been allocated by running PS_AllocateTrades"
                    .format(alloc_portfolio.Name()))

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")

    LOGGER.info("Completed successfully")
