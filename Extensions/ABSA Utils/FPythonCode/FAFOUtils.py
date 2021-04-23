import acm, os, csv, ael
from at_logging import getLogger
from IR_Delta_Calculation import get_calculation_space
from FTradeCreator import DecoratedTradeCreator
from at_time import acm_datetime

LOGGER = getLogger(__name__)
spaceCollection = acm.Calculations().CreateStandardCalculationsSpaceCollection()


def get_calendars(leg):
    calendars = []
    if leg.ResetCalendar() <> None:
        calendars.append(leg.ResetCalendar().Name())
    elif leg.Reset2Calendar() <> None:
        calendars.append(leg.Reset2Calendar().Name())
    elif leg.Reset3Calendar() <> None:
        calendars.append(leg.Reset3Calendar().Name())
    elif leg.Reset4Calendar() <> None:
        calendars.append(leg.Reset4Calendar().Name())
    elif leg.Reset5Calendar() <> None: 
        calendars.append(leg.Reset5Calendar().Name())
    return calendars
    

def create_resets(cf, cals):
    days = acm.Time.DateDifference(cf.EndDate(), cf.StartDate())
    day_method = cf.Leg().ResetDayMethod()
    reset_type = cf.Leg().ResetType() 
    if len(cals) == 0:
        cals.append(cf.Leg().Currency().Calendar().Name())
    date = cf.StartDate()
    stop_date = acm.Time.DateAdjustPeriod(cf.EndDate(), '1d', cals, 'Following')
    if days >= 1:
        while days != 0 and date != stop_date:
            print 'date is', ':', date
            rs = acm.FReset()
            rs.CashFlow(cf)
            rs.Day(date)
            rs.ResetType('Unweighted')
            rs.Leg(cf.Leg())
            rs.Commit()
            days -= 1
            date = acm.Time.DateAdjustPeriod(date, '1d', cals, 'Following')
            

def custom_resets(trade, leg_dates):
    for leg in trade.Instrument().Legs():
        if leg:
            cals = get_calendars(leg)
            for cf in leg.CashFlows():
                if leg.PayLeg() == True:
                    cf_start_date = leg_dates['Pay start']
                    cf_end_date = leg_dates['Pay end']
                    cf_pay_date = leg_dates['Pay pay date']
                else:
                    cf_start_date = leg_dates['Rec start']
                    cf_end_date = leg_dates['Rec end']
                    cf_pay_date = leg_dates['Rec pay date']
                LOGGER.info(cf_start_date, cf_start_date)
                if cf_start_date <> None: 
                    cf.StartDate(cf_start_date)
                if cf_end_date <> None:
                    cf.EndDate(cf_end_date)
                if cf_pay_date <> None:
                    cf.PayDate(cf_pay_date)
                if leg.LegType() == 'Float':
                    cf.Resets().Clear()
                    create_resets(cf, cals)
                cf.Commit()
            LOGGER.info('Done with creating custom resets for trade: {}'.format(trade.Name()))


def create_trade_filter(TFname):
    tradeFilter = ael.TradeFilter.new()
    tradeFilter.fltid = TFname
    tradeFilter.set_query([('', '', 'Trade Number', 'equal to', '-999', '')])
    tradeFilter.commit()
    LOGGER.info('Trade filter {} created....'.format(tradeFilter.fltid))
    return tradeFilter
    
    
def upload_trades(trade_list, tf_name):
    tf = ael.TradeFilter[tf_name]
    q = []
    k = 0
    if tf:
        tf_object = tf.clone()
    else:
        tf_object = create_trade_filter(tf_name)
    for trdnbr in trade_list:
        k = k + 1
        if k == 1:
            q.append(('', '', 'Trade number', 'equal to', trdnbr, ''))
        else:
            q.append(('Or', '', 'Trade number', 'equal to', trdnbr, ''))
    tf_object.set_query(q)
    tf_object.commit()


def get_parSpread(trade):
    sheet_type = "FTradeSheet"
    column_id = "Par Spread"
    calc_space = get_calculation_space(sheet_type)
    node = calc_space.InsertItem(trade)
    return round(calc_space.CreateCalculation(node, column_id).Value() * 100, 4)


class CreateFXTrade:

    def __init__(self, portfolio, amount, acquirer, curr_pair, trd_price, counterparty, counterparty_prf, days_to_valueday, status, trader, tradeprocess):
        self.portfolio = portfolio
        self.nominal = amount
        self.acquirer = acquirer
        self.currencyPair = curr_pair
        self.instrument = curr_pair.Currency1().Name()
        self.currency = curr_pair.Currency2().Name()
        self.counterparty = counterparty
        self.cp_prf = counterparty_prf
        self.days = days_to_valueday
        self.price = trd_price
        self.trd_status = status
        self.trader = trader.Name()
        self.tradeprocess = tradeprocess
    
    def is_cross(self):
        if 'USD' not in self.currencyPair.Name():
            return True
        else:
            return False

    def value_date(self):
        usd_cal = acm.FCurrency['USD'].Calendar()
        today = usd_cal.ModifyDate(self.currencyPair.Currency1().Calendar(), self.currencyPair.Currency2().Calendar(), acm.Time.DateToday(), 3)
        if self.days== 0:
            return today
        else:
            adjusted_date = self.currencyPair.Currency1().Calendar().AdjustBankingDays(today, self.days)
            if self.is_cross():
                return usd_cal.ModifyDate(self.currencyPair.Currency1().Calendar(), self.currencyPair.Currency2().Calendar(), adjusted_date, 3)
            else:
                return usd_cal.ModifyDate(self.currencyPair.Currency2().Calendar(), None, adjusted_date, 3)
                
    def format_trade_dict(self):
        formatted_dict = dict()
        formatted_dict['Instrument'] = self.instrument
        formatted_dict['Currency'] = self.currency
        formatted_dict['Nominal'] = float(self.nominal)
        formatted_dict['ReferencePrice'] = float(self.price)
        formatted_dict['Price'] = float(self.price)
        formatted_dict['Type'] = 'Normal'
        formatted_dict['DiscountingType'] = 'CCYBasis'
        formatted_dict['Premium'] = float(self.nominal*self.price)
        formatted_dict['Portfolio'] = self.portfolio 
        formatted_dict['Counterparty'] = str(self.counterparty)
        if acm.FParty[str(self.counterparty)].Type() == 'Intern Dept':
            formatted_dict['MirrorPortfolio'] = self.cp_prf
        formatted_dict['Acquirer'] = str(self.acquirer)
        formatted_dict['ValueDay'] = self.value_date()
        formatted_dict['Status'] = self.trd_status
        formatted_dict['Trader'] = self.trader
        formatted_dict['TradeProcess'] = self.tradeprocess
        return formatted_dict

    def _process_record(self):
        try:
            formatted_dict = self.format_trade_dict()
            creator = DecoratedTradeCreator(formatted_dict)
            trade = creator.CreateTrade()
            trade.Commit()
            LOGGER.info("Successfully booked FX Cash trade {}".format(trade.Oid()))
	    return trade
        except Exception as exc:
            msg = 'Failed to save trade: {}'.format(exc)
            LOGGER.exception(msg)
            
            
def wipe_payments(trade):
    payments = list(trade.Payments())
    for payment in payments:
        payment.Delete()
        
        
def get_FX_rate(curr_pair, market):
    instrument_currency = curr_pair.Currency1()
    qouted_currency = curr_pair.Currency2()
    price_date = acm.Time.DateToday()
    marketPlace = acm.FParty[market]
    return instrument_currency.Calculation().MarketPrice(spaceCollection, price_date, 1, qouted_currency, 1, marketPlace, 1).Number()
    
    
def get_currPair_price(curr_pair, market):
    if  curr_pair.SpotSplitPair() == None:
        base_currency = curr_pair.Currency1().Name()
        qouted_currency = curr_pair.Currency2().Name()
        price = get_FX_rate(curr_pair, market)
        return price
    else:
        split_currpair =  curr_pair.SpotSplitPair()
        split_price = get_FX_rate(split_currpair, market)
        if curr_pair.SweepCurrency().Name() in curr_pair.SpotSplitPair().Name():
            curr_pair2 = acm.FCurrencyPair[curr_pair.Currency1().Name()+'/'+'USD']
            if curr_pair2 == None:
                curr_pair2 = acm.FCurrencyPair['USD'+'/'+curr_pair.Currency1().Name()]
                dummy_curr_pair = acm.FCurrencyPair['USD'+'/'+curr_pair.Currency1().Name()]
                price2 = get_FX_rate(dummy_curr_pair, market)
            else:
                dummy_curr_pair = acm.FCurrencyPair[curr_pair.Currency1().Name()+'/'+'USD']
                price2 = get_FX_rate(dummy_curr_pair, market)
        else:
            curr_pair2 = acm.FCurrencyPair[curr_pair.Currency2().Name()+'/'+'USD']
            if curr_pair2 == None:
                curr_pair2 = acm.FCurrencyPair['USD'+'/'+curr_pair.Currency2().Name()]
                if curr_pair2:
                    dummy_curr_pair = acm.FCurrencyPair['USD'+'/'+curr_pair.Currency2().Name()]
                    price2 = get_FX_rate('USD', curr_pair.Currency2().Name(), market)
            else:
                dummy_curr_pair = acm.FCurrencyPair[curr_pair.Currency2().Name()+'/'+'USD']
                price2 = get_FX_rate(curr_pair.Currency2().Name(), 'USD', market)
        price = curr_pair.TriangulateRate(split_currpair, split_price, curr_pair2, price2)
        return price


def check_counterparty_name(cpty_name):
    cpty_obj = acm.FParty[cpty_name]
    if cpty_obj <> None:
        return True
    else:
        return False


def verify_qty_premium(block_trade, allocated_trades):
    trade_qty = block_trade.Nominal()
    trade_premium = block_trade.Premium()
    qty_counter = 0
    premium_counter = 0
    for trd in allocated_trades:
        qty_counter += trd.Nominal()
        premium_counter += trd.Premium()
    if qty_counter == trade_qty and premium_counter == premium_counter:
        return True
    else:
        return False

def WriteCSVFile(outputFileLocation, file_name, resultsList, HeaderList):
    """
    Create a file to store all results
    """
    #Checking if user has acess to the file path exist
    if os.path.exists(outputFileLocation):
        LOGGER.info("File path exists")
        file = outputFileLocation+"/"+file_name
        with open(file,  'wb') as reconBreaksFile:
            reconWriter = csv.writer(reconBreaksFile,  quoting=csv.QUOTE_ALL)
            reconWriter.writerow(HeaderList)
            for itemInList in resultsList:
                reconWriter.writerow(itemInList)
        LOGGER.info("File created succesfully")
    else:
        LOGGER.error("File path: {} does not exist.".format(outputFileLocation))

def get_calendarname(ins_obj):
    try:
        for leg in ins_obj.Legs():
            return leg.ResetCalendar().Name()
        LOGGER.info("Succesfully retirved the calendar linked to the instrument {}".format(ins_obj.Name()))
    except Exception as e:
        LOGGER.error("Failed while trying to retrieve the calander linked to the following instrument {}".format(ins_obj.Name()))
        LOGGER.info(e)

def get_period(ins_obj):
        if ins_obj.ExpiryPeriod_unit() == "Days":
            return str(ins_obj.ExpiryPeriod_count())+"d"
        elif ins_obj.ExpiryPeriod_unit() == "Weeks":
            return str(ins_obj.ExpiryPeriod_count())+"w"
        elif ins_obj.ExpiryPeriod_unit() == "Months":
            return str(ins_obj.ExpiryPeriod_count())+"m"
        else:
            return str(ins_obj.ExpiryPeriod_count())+"y"
            

def get_price(ins_name, mkt_name):
    ins_obj = acm.FInstrument[ins_name]
    for prc in ins_obj.Prices():
        if prc.Market().Name() == mkt_name and prc.Day() == acm.Time.DateToday():
            return prc.Last()


def get_calendar_banking_date(date, calendar_type):
    try:
        calendar = acm.FCalendar[calendar_type]
        date = acm_datetime(date)

        return calendar.ModifyDate(None, None, date)
    except Exception as error:
        LOGGER.info(error)

