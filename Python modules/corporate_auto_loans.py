"""
Description
===========
Date                          :  2018-07-03
Purpose                       :  Automation of loans booking for Corporate
Department and Desk           :  Finance and Trade
Requester                     :  Hilliard Nyman
Developer                     :  Ondrej Bahounek

Details:
========
The automation of the booking of loans for corporate.
Information is sent from Supplier Finance system to the trader, who then books it into FA.
An internal booking leg is then performed and submitted for trader's confirmation.

Example:
========
See workbook: SF_loans_auto [BAHOUNEO]

testing set:
Trade 1: 70,057,939  -> ins:ZAR/161012-170103/8.488753
Trade 2: 70,058,131  -> ins:ZAR/161012-170103/7.676/#1
Trade 3: 70,058,132  -> ins:ZAR/161012-170103/7.676/#1

Trade1:
70,057,939
portfolio: 'Supplier Finance ZAR'
acquirer: 'TWC SF'
cparty: <<CLIENT>>
quantity: q

Trade2:
contract: Trade1
instrument: 'ZAR/161012-170103/7.676/#1'
70,058,131
portfolio: 'Int Term Fund Econ Alloc'
acquirer: 'Funding Desk'
cparty: 'TWC SF'
Funding Instrype: 'CL'
quantity: q
valueDay(start date): '2016-10-12'
end date: '2017-01-03'

Trade3:
70,058,132
portfolio: 'Supplier Finance ZAR'
acquirer: 'TWC SF'
cparty: 'Funding Desk'
Funding Instrype: 'CD'
quantity: -q


CSV <-> FA MAPPING
==================
The CSV file                    FA                 
- Certified Value               - Capital amount  
- Loan Amount                   - Loan amount     
- Effective Date                - Settlement date 
- Maturity Date                 - Maturity date   
- Days                          - Tenor (days)    
- Loan Rate                     - Trade loan rate 
- Acquirer                      - Acquirer        
- Buyer                         - Counterparty    
- Currency                      - Currency        
- Portfolio                     - Portfolio       
- Funding Instype               - Funding Instype 

"""

import os
import string
import csv
from collections import OrderedDict

import acm
from at_feed_processing import SimpleCSVFeedProcessor, notify_log
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_email import EmailHelper


LOGGER = getLogger()

FILE_PREFIX = "SFTradeLoans_${DATE}"
TRADE_STATUS = "Simulated"
CALENDAR = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()
YESTERDAY = acm.Time().DateAddDelta(TODAY, 0, 0, -1)
PREVBUSDAY = CALENDAR.AdjustBankingDays(TODAY, -1)
DATE_LIST = {
             'PrevBusDay':PREVBUSDAY,
             'Yesterday':YESTERDAY,
             'Custom Date':TODAY,
             'Today':TODAY,
             }
DATE_KEYS = DATE_LIST.keys()
DATE_KEYS.sort()

ZAR_JIBAR_3M = acm.FRateIndex['ZAR-JIBAR-3M']
SPACE = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
PRICE_MARKETS_ORDERS = ('SPOT', 'internal')


class MissingFileException(Exception):
    pass


def used_price(ins, for_date, curr=None, price_find_type=None, market=None):
    """
    USD/ZAR rate = # used_price('USD', '2018-05-14', 'ZAR')
    
    market:
        you should use SPOT for any historical date and None for date today
    """
    dict = acm.FDictionary()
    if for_date:
        dict['priceDate'] = for_date
    if curr:
        dict['currency'] = curr
    if price_find_type and price_find_type != 'None':
        if price_find_type == 'Ask' or price_find_type == 'Bid':
            dict['typeOfPrice'] = 'Average'+price_find_type+'Price'
        else:
            dict['typeOfPrice'] = price_find_type+'Price'
    if market:
        dict['marketPlace'] = market
        dict['useSpecificMarketPlace'] = True
    return ins.Calculation().MarketPriceParams(SPACE, dict).Value().Number()


def get_price(ins, for_date, curr=None):
    if for_date == TODAY:
        price = used_price(ins, for_date, curr)
        if price == price:
            return price
    
    for market in PRICE_MARKETS_ORDERS:
        price = used_price(ins, for_date, curr, market=market)
        if price == price:
            return price
    return float('nan')


def display_msg(title, msg):
    func = acm.GetFunction('msgBox', 3)
    func(title, msg, 0)
    

def strip_datetime(date_time_detailed):
    """
    '2016-12-14 11:22:33.789' -> '2016-12-14 11:22:33'
    """
    return date_time_detailed.split(".")[0]


def confirm_trades(eii):
    trade = eii.ExtensionObject().OriginalTrade()
    trades = acm.FTrade.Select("contract=%d and status='Simulated'" %trade.Oid())
    if len(trades) != 3:
        raise RuntimeError("Trade '%d' is not an external auto loan trade." % trade.Oid())
    LOGGER.info("FO Confirming trades: %s" % trades)
    acm.BeginTransaction()
    try:
        for trd in trades:
            raise RuntimeError("myerror")
            trd.Status("FO Confirmed")
            trd.Commit()
        LOGGER.info("Done")
        acm.CommitTransaction()
    except Exception as exc:
        acm.AbortTransaction()
        LOGGER.error("ERROR: %s" % str(exc))
        raise
    display_msg("Corp Loans FO Confirmation",
                "Corporate trades have been FO Confirmed.\nCheck logs for details.")


def get_bussiness_day(the_date, calendar):
    if calendar.CalendarInformation().IsNonBankingDay(the_date):
        return calendar.AdjustBankingDays(the_date, 1)
    return the_date


def linear_interpolation(dx, date1, date2, fd1, fd2):

    if not date1 < dx <= date2:
        raise RuntimeError("Invalid dates.")
    
    diff_d12 = acm.Time.DateDifference(date2, date1)
    diff_d1n = acm.Time.DateDifference(dx, date1)
    diff_fd = fd2 - fd1
    
    interp = diff_fd / diff_d12 * diff_d1n + fd1
    return interp


# start-date: 2016-11-18, end-date: 2017-01-30, rate date: 2016-11-18
def interpolate(start_date, end_date, rate_day, calendar):
    
    day_21d = get_bussiness_day(acm.Time.DateAddDelta(rate_day, 0, 0, 21), calendar)
    #day_21d = acm.Time.DateAddDelta(rate_day, 0, 0, 21)
    period_date = rate_day
    periods = (1, 3, 6, 9, 12)
    rates_for_dates = {}
    p_date = get_bussiness_day(start_date, calendar)
    rates_for_dates[p_date] = acm.FRateIndex['ZAR-ABSA-TOP20-CALL'].UsedPrice(rate_day, 'ZAR', 'SPOT')
    rates_for_dates[day_21d] = acm.FRateIndex['ZAR-JIBAR-1M'].UsedPrice(rate_day, 'ZAR', 'SPOT')
    for period in periods:
        p_date = acm.Time.DateAddDelta(start_date, 0, period, 0)
        p_date = get_bussiness_day(p_date, calendar)
        p_index = acm.FRateIndex['ZAR-JIBAR-%dM' % period]
        #period_date = acm.Time.DateAddDelta(rate_day, 0, period, 0)
        #period_date = get_bussiness_day(period_date, calendar)
        rates_for_dates[p_date] = p_index.UsedPrice(period_date, 'ZAR', 'SPOT')
    
    dates = sorted(rates_for_dates.keys())
    for dx1 in range(len(dates) - 1):
        dx2 = dx1 + 1
        date1 = dates[dx1]
        date2 = dates[dx2]
        
        #print "date1, end_date, date2", date1, end_date, date2
        if date1 < end_date <= date2:
            rate1 = rates_for_dates[date1]
            rate2 = rates_for_dates[date2]
            interp = linear_interpolation(end_date, date1, date2, rate1, rate2)
            #print "interp", end_date, date1, date2, rate1, rate2
            return interp
    
    raise RuntimeError("Can't find bounding dates required for interpolation. Date: %s"
                       % end_date)


class DepoCreator(object):

    INT_TRD_PORTFOLIO = acm.FPhysicalPortfolio[6574]  # "Int Term Fund Econ Alloc"
    INT_TRD_ACQUIRER = acm.FParty[2247]  # "Funding Desk"
    INT_TRD_CPARTY = acm.FParty[42673]  # "TWC SF"

    CONTRACT_SIZE = 1000000
    SPREAD = 0.35
    ID_PREFIX = "TradeLoansID_"

    def __init__(self, sf_id, acquirer, counterparty, end_cash,
        quantity, settle_date, maturity_date, tenor_days, rate,
        currency, portf, fund_instype, created_datetime, pm_acmfacility, pm_facility):

        self.sf_id = sf_id  # unique ID in external system
        self.acm_acquirer = self._get_acm_obj('FInternalDepartment', acquirer)
        self.acm_counterparty = self._get_acm_obj('FParty', counterparty)
        self.end_cash = float(end_cash)
        self.quantity = float(quantity) / self.CONTRACT_SIZE
        self.settle_date = settle_date
        self.maturity_date = maturity_date
        self.tenor_days = int(tenor_days)
        self.rate = float(rate)
        self.acm_currency = self._get_acm_obj('FCurrency', currency)
        self.acm_portf = self._get_acm_obj('FPhysicalPortfolio', portf)
        self.fund_instype = fund_instype
        self.created_datetime = created_datetime
        self.pm_acmfacility = pm_acmfacility
        self.pm_facility = pm_facility
        
    def _get_acm_obj(self, acm_cls, obj_name):
        cls = acm.GetClass(acm_cls)
        obj = cls[obj_name]
        if not obj:
            raise RuntimeError("Nonexisting %s: %s" % (acm_cls, obj_name))
        return obj
        
    def _format_date(self, the_date):
        """Convert FA date to YYYYmmdd.
        Example: '2016-10-14' -> '20161014'
        """
        conv_name = the_date.replace("-", "").replace("/", "")
        if len(conv_name) != 8:
            raise ValueError("Incorrect input date: %s" % the_date)
        return conv_name

    def _get_date_from_datetime(self, date_time):
        """
        Strip date from date and time combination.
        
        '2016-12-14 11:22:44' -> '2016-12-14'
        """
        parts = date_time.split(" ")
        if len(parts[0]) != 10:
            raise RuntimeError("Incorrect datetime format '%s'" % date_time)
        return parts[0]

    def _create_external_depo(self):
        cal = self.acm_currency.Calendar()
        day_count_method = self.acm_currency.Legs()[0].DayCountMethod()
        
        ins = acm.FDeposit()
        ins.Currency(self.acm_currency)
        ins.ContractSize(self.CONTRACT_SIZE)
        ins.DateFrom('')
        ins.Otc(True)
        ins.OpenEnd('None')
        ins.PayOffsetMethod('Business Days')
        ins.PriceFindingChlItem(
            acm.FChoiceList.Select('list="PriceFindingGroup" and name="Close"')[0])
        ins.SpotBankingDaysOffset(0)
        ins.ShortDividendFactor(1)
        ins.ValuationGrpChlItem(
            acm.FChoiceList.Select('list="ValGroup" and name="AC_GLOBAL_Funded"')[0])
        ins.QuoteType('Clean')
        ins.Quotation('Clean')
        ins.ExpiryDate(self.maturity_date)
        ins.ExpiryPeriod('3m')
        ins.StrikeCurrency('ZAR')
        ins.MinimumPiece(0)
        ins.RoundingSpecification('Rounding_FX_2Dec')

        # Receive Leg
        leg = ins.CreateLeg(False)
        leg.AmortDaycountMethod(day_count_method)
        leg.AmortPeriodUnit('Days')
        leg.AmortStartPeriodCount(1)
        leg.AmortEndPeriodCount(self.tenor_days)
        leg.AmortEndPeriodUnit('Days')
        leg.AmortStartDay(self.settle_date)
        leg.AmortEndDay(self.maturity_date)
        leg.EndPeriodUnit('Days')
        leg.EndPeriodCount(self.tenor_days)
        leg.StartPeriodCount(1)
        leg.PayCalendar(cal)
        leg.ResetCalendar(cal)
        leg.Currency(self.acm_currency)
        leg.Decimals(11)
        leg.FloatRateFactor(0)
        leg.FixedRate(self.rate)
        leg.NominalFactor(1)
        leg.FixedCoupon(False)
        leg.PayLeg(False)
        leg.DayCountMethod(day_count_method)
        leg.NominalAtEnd(True)
        leg.Rounding('Normal')
        leg.RollingPeriod("0d")
        leg.ResetDayOffset(0)
        leg.ResetType("None")
        leg.ResetPeriod("1d")
        leg.ResetDayMethod("Following")
        leg.RollingPeriodBase(self.maturity_date)
        leg.PayDayMethod("Mod. Following")
        leg.Reinvest(False)
        leg.PriceInterpretationType('As Reference')
        leg.RollingConv('Preserve EOM')

        leg.StartDate(self.settle_date)
        leg.EndDate(self.maturity_date)
        leg.LegType('Fixed')
        leg.StrikeType("Absolute")
        
        ins.RegisterInStorage()
        leg.Instrument(ins)
        ins.Name(ins.SuggestName())
        ins.Commit()

        LOGGER.info("External loan: %s" % ins.Name())

        return ins


    def _get_cashflow(self, instr, cf_type):
        existing_cf = [cf for cf in instr.Legs()[0].CashFlows()
            if cf.CashFlowType() == cf_type]

        if not existing_cf:
            return instr.Legs()[0].CreateCashFlow()
        else:
            if len(existing_cf) > 1:
                LOGGER.warning("More cashflows of type '%s' found (%d). Updating first one (oid: %d)..."
                    % (cf_type, len(existing_cf), existing_cf[0].Oid()))
            return existing_cf[0]

    def _create_ext_cashflows(self, instr):

        #LOGGER.info("Creating cashflows...")

        # 1) Fixed Amount cashflow
        cf_type = 'Fixed Amount'
        new_cf1 = self._get_cashflow(instr, cf_type)
        new_cf1.PayDate(self.maturity_date)
        new_cf1.CashFlowType(cf_type)
        new_cf1.FixedAmount(1)
        new_cf1.NominalFactor(1)
        new_cf1.Commit()
        #LOGGER.info("Cashflow of type '%s' created." % cf_type)

        # 2) Fixed Rate cashflow
        cf_type = 'Fixed Rate'
        new_cf2 = self._get_cashflow(instr, cf_type)
        new_cf2.StartDate(self.settle_date)
        new_cf2.PayDate(self.maturity_date)
        new_cf2.EndDate(self.maturity_date)
        new_cf2.CashFlowType(cf_type)
        new_cf2.FixedAmount(0)
        new_cf2.FixedRate(self.rate)
        new_cf2.NominalFactor(1)
        new_cf2.Commit()
        #LOGGER.info("Cashflow of type '%s' created." % cf_type)


    def _book_external_trade(self, instr):
        """Client facing trade"""

        LOGGER.info("Booking external trade...")

        trade = acm.FTrade()
        trade.Instrument(instr)
        trade.Portfolio(self.acm_portf)
        trade.Currency(self.acm_currency)
        trade.Quantity(self.quantity)
        trade.Counterparty(self.acm_counterparty)
        trade.Acquirer(self.acm_acquirer)
        trade.ValueDay(self.settle_date)
        trade.AcquireDay(self.settle_date)
        trade.TradeTime(acm.Time.TimeNow())
        trade.Status(TRADE_STATUS)
        trade.Trader(acm.User())
        trade.EndCash(self.end_cash)
        trade.Price(100)
        trade.Premium(-1 * trade.Quantity() * instr.ContractSize())
        trade.Text1(self.ID_PREFIX + self.sf_id)
        trade.Type('Normal')

        trade.RegisterInStorage()
        trade.AddInfoValue('Funding Instype', self.fund_instype)
        trade.AddInfoValue('PM_FacilityCPY', self.acm_counterparty)
        trade.AddInfoValue('PM_ACMFacilityID', self.pm_acmfacility)
        trade.AddInfoValue('PM_FacilityID', self.pm_facility)
        trade.Commit()
        #LOGGER.info("External trade booked: %d" % trade.Oid())
        return trade
        
    def _calculate_rate_interp(self):
        # TODO: confirm whether datetoday or settle date should be used
        #tenor_date = acm.Time.DateAddDelta(acm.Time.DateToday(), 0, 0, self.tenor_days)
        created_date = self._get_date_from_datetime(self.created_datetime)
        tenor_date = get_bussiness_day(acm.Time.DateAddDelta(created_date, 0, 0, self.tenor_days), self.acm_currency.Calendar())
        rate_date = get_bussiness_day(created_date, self.acm_currency.Calendar())
        LOGGER.info("Interpolating (start-date: %s, end-date: %s, rate date: %s)"
                    %(created_date, tenor_date, rate_date))
        interp = interpolate(created_date, tenor_date, rate_date, self.acm_currency.Calendar())
        rounded = round(interp, 3)
        LOGGER.info("Interpolated value for %s: %f , rounded: %f" 
                    %(tenor_date, interp, rounded))
        res = rounded + self.SPREAD
        LOGGER.info("Adding spread %f: %f" %(self.SPREAD, res))
        return res
    
    def _calculate_rate(self):
        rate = get_price(ZAR_JIBAR_3M, self.settle_date)
        if rate != rate:
            raise RuntimeError("Nonexisting price for '%s' for '%s'" 
                               %(ZAR_JIBAR_3M.Name(), self.settle_date))
        return rate + 0.35

    def _book_internal_depo(self, external_depo):
        LOGGER.info("Creating internal depo...")
        rate = self._calculate_rate()
        depo = acm.FDeposit()
        depo.Apply(external_depo)
        leg = depo.Legs()[0]
        leg.FixedRate(rate)

        cf = [cf for cf in leg.CashFlows() if cf.CashFlowType() == 'Fixed Rate'][0]
        cf.FixedRate(rate)

        depo.RegisterInStorage()
        depo.Name(depo.SuggestName())
        depo.Commit()

        LOGGER.info("Internal depo: %s" % depo.Name())

        return depo

    def _book_internal_trades(self, external_trade):
        """Treasury trade and its mirror Funding trade"""

        depo = self._book_internal_depo(external_trade.Instrument())
        depo_rate = depo.Legs()[0].FixedRate()

        LOGGER.info("Booking internal trade...")
        trade1 = acm.FTrade()
        trade1.Apply(external_trade)

        trade1.Instrument(depo)
        trade1.ConnectedTrade(external_trade)
        trade1.Price(100)

        trade1.Portfolio(self.INT_TRD_PORTFOLIO)
        trade1.Acquirer(self.INT_TRD_ACQUIRER)
        trade1.Counterparty(self.INT_TRD_CPARTY)
        
        trade1.TradeTime(self.created_datetime)
        
        # end cash = nominal * (1 + rate * period/365 / 100)
        end_cash = trade1.Nominal() * (1 + depo_rate * self.tenor_days / 365 / 100)
        trade1.EndCash(end_cash)

        trade1.RegisterInStorage()
        trade1.AddInfoValue('Funding Instype', "CL")
        trade1.AddInfoValue('PM_ACMFacilityID', None)
        trade1.AddInfoValue('PM_FacilityCPY', external_trade.add_info('PM_FacilityCPY'))
        trade1.AddInfoValue('PM_FacilityID', external_trade.add_info('PM_FacilityID'))
        
        trade1.MirrorPortfolio(external_trade.Portfolio())
        trade1.Commit()
        
        mirror = trade1.GetMirrorTrade()
        mirror.AddInfoValue('Funding Instype', "CD")
        mirror.Commit()
        
        return trade1

    def book(self):
        LOGGER.info("Booking started.")

        acm.BeginTransaction()
        try:
            depo = self._create_external_depo()
            self._create_ext_cashflows(depo)
            trade1 = self._book_external_trade(depo)
            self._book_internal_trades(trade1)
            LOGGER.info("Committing...")
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            LOGGER.exception("Error during booking.")
            raise

        LOGGER.info("External trade: %d", trade1.Oid())
        return trade1


class LoanReader(SimpleCSVFeedProcessor):

    col_id = "ID"
    col_cap_amount = "Certified Value"
    col_loan_amount = "Loan Amount"
    col_settle_date = "Effective Date"
    col_maturity_date = "Maturity Date"
    col_tenor = "Days"
    col_loan_rate = "Loan Rate"    
    col_acquirer = "Acquirer"
    col_counterparty = "Counterparty"
    col_currency = "Currency"
    col_portf = "Portfolio"
    col_fund_instype = "Funding Instype"
    col_created = "Created"
    col_pm_acmfacility = "PM_ACMFacilityID"
    col_pm_facility = "PM_FacilityID"
    
    col_ref = "Ref"
    
    PROCESSED_SUFF = "_processed"
    
    _required_columns = [
        col_id, col_acquirer, col_counterparty, col_cap_amount, 
        col_loan_amount, col_settle_date, col_maturity_date, col_tenor,
        col_loan_rate, col_currency, col_portf, col_fund_instype,
        col_created]


    def __init__(self, file_path, email_addrss=None):
        super(LoanReader, self).__init__(file_path)
        self.headers = self._read_headers()
        self.records = []
        self.addrss = email_addrss

    def _process_record(self, record, dry_run):
        (_index, record_data) = record

        try:
            sf_id = record_data[self.col_id]
            acq = record_data[self.col_acquirer]
            cparty = record_data[self.col_counterparty]
            cap_amt = record_data[self.col_cap_amount]
            loan_amt = record_data[self.col_loan_amount]
            settle_date = record_data[self.col_settle_date]
            maturity_date = record_data[self.col_maturity_date]
            tenor = record_data[self.col_tenor]
            rate = record_data[self.col_loan_rate]
            curr = record_data[self.col_currency]
            portf = record_data[self.col_portf]
            fund_instype = record_data[self.col_fund_instype]
            created_datetime = strip_datetime(record_data[self.col_created])
            pm_acmfacility= record_data[self.col_pm_acmfacility]
            pm_facility = record_data[self.col_pm_facility]
            
            creator = DepoCreator(sf_id, acq, cparty, cap_amt,
                        loan_amt, settle_date, maturity_date, 
                        tenor, rate, curr, portf, fund_instype,
                        created_datetime, pm_acmfacility, pm_facility)

            extern_trd = creator.book()
            
            self._append_record(record_data, extern_trd)

        except Exception as exc:
            msg = 'Row #%d: Failed to read data from file: %s' % (_index, str(exc))
            LOGGER.exception(msg)
            raise self.RecordProcessingException(msg)

    def _append_record(self, record_data, extern_trd):
        record_data[self.col_ref] = extern_trd.Oid()
        record_data["Bank Account"] = extern_trd.PortfolioId() + " Account"
        self.records.append(record_data)
        
    def _read_headers(self):
        """List of all headers with the same ordering as in file."""
        with open(self._file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            headers = reader.next()
        return headers
        
    def _finish(self):
        if LOGGER.msg_tracker.errors_counter:
            LOGGER.warning("Errors occurred, no output will be written.")
            return
            
        output_filename = os.path.basename(self._file_path).replace('.csv', self.PROCESSED_SUFF + '.csv')
        out_path = os.path.join(os.path.dirname(self._file_path), output_filename)
        
        LOGGER.info("Writing output: %s", out_path)
        with open(out_path, 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, self.headers)
            writer.writer.writerow(self.headers)
            for row in self.records:
                writer.writerow(row)
                
        if self.addrss is not None and len(self.addrss) > 0:
            LOGGER.info("Sending email.")
            subj = "Auto Loans for %s" % os.path.basename(self._file_path)
            html_body = self._construct_body(self.records, self._file_path, out_path)
            send_email(subj, self.addrss, html_body)
        
    def _to_html(self, records):
        
        # mapping: records_dict_key -> email column name
        header_mapping = OrderedDict([(self.col_ref, "FA trdnbr"),
                                      (self.col_id, "Source " + self.col_id),
                                     ])
                                      
        res_text = '<table width="200" border="1">'
        res_text += "<tr>" + "".join(map("<td><b>{0}</b></td>".format, header_mapping.values())) + "</tr>"
        for row in records:
            vals = map(row.get, header_mapping.keys())
            line = "<tr>" + "".join(map("<td>{0}</td>".format, vals)) + "</tr>"
            res_text += line
        return res_text + "</table>"
    
    def _construct_body(self, records, input, output):
        msg = "Hello MM Team, <br /><br />"
        msg += "These Loan Trades were just booked.<br /><br />"
        msg += "Amount of trades: <b>%d</b><br /><br />" % len(records)
                       
        msg += self._to_html(records)    
        
        msg += "<br /><br />"
        msg += "Please check and confirm them.<br /><br />"
        msg += "Input file: <b>%s</b><br />" % input
        msg += "Output file: <b>%s</b><br />" % output
        msg += "<br /><br />"
        msg += "Best regards,<br />{0}".format(
                "CIB Africa TS Dev - Prime and Equities")
        msg += "<br /><br /><br /><small>This is an automated message from '%s'</small>" % __name__
        return msg


def enable_custom_start_date(selected_variable):
    cust = ael_variables.get("custom_date")
    cust.enabled = (selected_variable.value == 'Custom Date')


ael_variables = AelVariableHandler()
ael_variables.add(
    "date",
    label="Date",
    cls="string",
    default="Today",
    collection=DATE_KEYS,
    hook=enable_custom_start_date,
    mandatory=True,
    alt=("A date for which files will be taken."))
ael_variables.add(
    "custom_date",
    label="Custom Date",
    cls="string",
    default=TODAY,
    enabled=False,
    alt=("Format: '2016-11-07'."))
ael_variables.add(
    "dir_input",
    label="Input Directory",
    default=r"c:\DEV\Perforce\FA\features\ABITFA-4501 - Automation of loans booking for Corporate .br\Input",
    alt=("A Directory template with all input files. "
         "It can contain the variable DATE (\"$DATE\") "
         "which will be replaced by the today's date (format YYYY-MM-DD)"))
ael_variables.add(
    "file_name",
    label="Filename prefix",
    default=FILE_PREFIX,
    alt=("A prefix path template to the input file. "
         "It can contain the variable DATE (\"$DATE\") "
         "which will be replaced by the today's date (format DD-MM-YYYY). "
         "There must be just one file with this prefix in the directory."))
ael_variables.add(
    "email_recipients",
    label="Email Recipients",
    default="Ondrej.Bahounek@barclays.com",
    multiple=True,
    mandatory=False,
    alt=("Email recipients. Use comma seperated email addresses "
         "if you want to send report to multiple users. "
         "Leave blank if no email needs to be sent."))


def send_email(subj, addresses, body):
    environment = acm.FDhDatabase['ADM'].InstanceName()
    email_helper = EmailHelper(
        body,
        subj,
        addresses
        )
    if str(acm.Class()) == "FACMServer":
        email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email_helper.host = EmailHelper.get_acm_host()
    try:
        email_helper.send()
    except:
        LOGGER.exception("Error while sending e-mail.")


def get_date(ael_dict):
    # date in string
    if ael_dict['date'] == 'Custom Date':
        the_date = ael_dict['custom_date']
    else:
        the_date = DATE_LIST[ael_dict['date']]
    return the_date


def get_file_paths(the_date, inpt_dir, file_name):
    """
    Get full path for given date.
    
    Filename can be a template where a date is replaced for ${DATE}.
    If Filename doesn't have a '.csv' suffix,
    search for a file in the input dir with same prefix.
    """
    file_date = the_date.replace("-", "")
    fname_template = string.Template(file_name)
    dir_template = string.Template(inpt_dir)
    file_name = fname_template.substitute(DATE=file_date)
    all_file_names = [file_name]
    dir_name = dir_template.substitute(DATE=the_date)
    if not file_name.endswith(".csv"):
        all_files = [f for f in os.listdir(dir_name) if f.endswith(".csv")
                     and f.startswith(file_name)]
        to_process = set(f for f in all_files if LoanReader.PROCESSED_SUFF not in f)
        processed_files = [f for f in all_files if LoanReader.PROCESSED_SUFF in f]
        for fn in processed_files:
            f_raw = fn.replace(LoanReader.PROCESSED_SUFF, "")
            if f_raw in to_process:
                LOGGER.info("Skipping file '%s'", f_raw)
                to_process.remove(f_raw)
        
        if len(to_process) == 0:
            LOGGER.info("No file to process with name '%s'", file_name)

        all_file_names = to_process
    
    full_path_list = []
    for fname in all_file_names:
        full_path = os.path.join(dir_name, fname)
        if not os.path.exists(full_path):
            raise RuntimeError("Nonexisting file path: '%s'" % full_path)
        full_path_list.append(full_path)
    
    return full_path_list


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    the_date = get_date(ael_dict)
    addrss = list(ael_dict['email_recipients'])
    file_path_list = get_file_paths(the_date, ael_dict['dir_input'], ael_dict['file_name'])
    LOGGER.info("Input name: '%s'", ael_dict['file_name'])
    LOGGER.info("Amount of files to process: %d", len(file_path_list))
    for file_path in file_path_list:
        proc = LoanReader(file_path, addrss)
        proc.add_error_notifier(notify_log)
        proc.process(False)
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
    if LOGGER.msg_tracker.warnings_counter:
        LOGGER.warning("Completed with some warnings.")
    else:
        LOGGER.info("Completed successfully.")
