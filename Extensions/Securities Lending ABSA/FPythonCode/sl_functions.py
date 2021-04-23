"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Functions that get used in ADFL extension attributes and python scripts in the securities lending project
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Paul Jacot-Guillarmod
CR NUMBER               :  562530

History:

Date        CR Number    Who                      What

2010-04-14  282030       Paul Jacot-Guillarmod    Updated monthly_interest to look at the additional_info
                                                  on a cashflow to correctly include 
                                                  Interest Repayments
2010-07-01  371587       Francois Truter          Added SLPartialReturn functions
2010-08-23  409966       Francois Truter          Added SLPrice, SLUnderlying and ValidUnderlyingTypesWithETF
2010-11-16  494829       Paul Jacot-Guillarmod    Added additional functions to be used for CFD security loans
2011-02-01  562530       Francois Truter          Update FCashflow.PayDate in SplitCashflow
2011-01-12  581108       Rohan vd Walt            Nominal factor calculation for Sec Loans on Bonds
2011-11-01  816158       Rohan vd Walt            Lender Split and Min Fee calculations
2012-01-09  XXXXXX       Rohan vd Walt            Remove old L B F entries from Trade Entry Choicelist
2012-05-24  206714       Anil Parbhoo             convert g1 time stamp to local time
2012-11-08  582907       Hynek Urban              Add the logic for minimum lender fee rate selection.
2019-09-25  FAU-378      Libor Svoboda            Update nominal factor calculations.
2020-01-09  CHG0073639   Libor Svoboda            Update sec loan regenerate logic.
2020-01-21  PCGDEV-165   Qaqamba Ntshobane        Added more functions for SBL onto FA project reporting.
-----------------------------------------------------------------------------"""

import ael
import acm
import time
from math import isnan
import at_calculation_space as acs
from FBDPCommon import is_acm_object, acm_to_ael
from at_calculation_space import CalculationSpace


FINDER_CHLIST = 'GlobalOneFinders'

VALID_SBL_STATUS = (
    'FO Confirmed',
    'BO Confirmed',
    'BO-BO Confirmed',
)
CALENDAR = acm.FCalendar['ZAR Johannesburg']
CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()


def get_finder_names():
    choice_list = acm.FChoiceList.Select01(
        'name="%s" and list="MASTER"' % FINDER_CHLIST,
        'Choice list %s does not exist.' % FINDER_CHLIST)
    return [item.Name() for item in choice_list.Choices()]


def get_addinfo(entity, ai_name):
    # Return the value of an additional info field for a given entity
    
    if is_acm_object(entity):
        entity = acm_to_ael(entity)
    
    val = None
    for ai in entity.additional_infos():
        if ai.addinf_specnbr.field_name == ai_name:
            val = ai.value
            break
    return val
    
def set_additional_info(entity, ai_name, ai_value):
    ''' Sets an additional info field for a given entity.
    '''
    
    if is_acm_object(entity):
        entity = acm_to_ael(entity)
    ent_clone = entity.clone()
    
    # Clone the additional info entity if it exists, otherwise create a new additional info
    for ai in entity.additional_infos():
        if ai.addinf_specnbr.field_name == ai_name:
            new_ai = ai.clone()
            break
    else:
        new_ai = ael.AdditionalInfo.new(ent_clone)
        new_ai.addinf_specnbr = ael.AdditionalInfoSpec[ai_name]
    
    new_ai.value = str(ai_value)
    try:
        new_ai.commit()
        ent_clone.commit()
    except:
        print 'Error: Could not update additional info value %s' %(ai_name)

def copy_additional_infos(original_entity, new_entity, exception_list = None):
    ''' Copy all additional infos from original_entity to new_entity
        excluding those additional infos in exception_list.
    '''    
    if exception_list is None:
        exception_list = []
        
    if is_acm_object(original_entity):
        original_entity = acm_to_ael(original_entity)
    
    if is_acm_object(new_entity):
        new_entity = acm_to_ael(new_entity)
    
    for addinfo in original_entity.additional_infos():
        addinfo_name = addinfo.addinf_specnbr.field_name
        addinfo_value = addinfo.value
        if addinfo_value and addinfo_value <> 'None' and addinfo_name not in exception_list:
            set_additional_info(new_entity, addinfo_name, addinfo_value)
            
            
def remove_additional_infos( new_entity, exception_list = None):
    ''' Copy all additional infos from original_entity to new_entity
        excluding those additional infos in exception_list.
    '''    
    if exception_list is None:
        exception_list = []
        
    
    if is_acm_object(new_entity):
        new_entity = acm_to_ael(new_entity)
        
    print 'Exception List ', exception_list    
    
    for addinfo in new_entity.additional_infos():
        addinfo_name = addinfo.addinf_specnbr.field_name
        addinfo_value = addinfo.value
        
        if  addinfo_name  in exception_list:
            set_additional_info(new_entity, addinfo_name, None)   
        new_entity.commit()         

def underlying_quantity(tq, i):
    ''' Calculate the quantity of the underlying instrument, given the trade quantity tq.
    '''
    
    return i.RefValue() * tq

def trade_quantity(uq, i):
    ''' Calculate the trade quantity, given the quantity of the underlying instrument uq.
    '''
    
    return uq / i.RefValue()
  
def counterparty_limit(p):
    ''' Retrieve a counterparties credit limit against the Securities Lending Desk, the credit limit is set as the 1d limit.
    '''
    department = acm.FParty['SECURITY LENDINGS DESK']
 
    if p.GroupLimit() and p.Parent():
        party = p.Parent()
    else:
        party = p
        
    credit = acm.FCreditLimit.Select('department = "%s" and party = "%s"' %(department.Name(), party.Name()))
    
    # If credit limit has been set then return the credit limit else return 0
    return credit and credit.At(0).Limit0() or 0

def monthly_interest(t, first_day_of_month, calculation_date):
    ''' Calculates the interest from the first day of a month corresponding to a given calculation date. 
    '''
    
    i = t.Instrument()
    l = i.Legs().At(0)
    total_interest = 0
    
    for cf in l.CashFlows():
        if first_day_of_month <= cf.PayDate() <= calculation_date:
            if cf.CashFlowType() in ('Fixed Amount'):
                settle_type = get_addinfo(cf, 'Settle_Type')
                if settle_type in ('Interest Repayment'): 
                    total_interest += cf.FixedAmount()  
            elif cf.CashFlowType() in ('Interest Reinvestment'):
                total_interest += cf.FixedAmount()  
    return total_interest


def trade_end_date(t):
    ''' Return the end date of a fixed term security loan and return big date (9999/12/31) for a 
        stock or open ended security loan.
    '''
    if t.Instrument().InsType() == 'SecurityLoan' and not t.Instrument().IsOpenEnd():
        return t.Instrument().Legs().At(0).EndDate()
    else:
        return acm.Time().BigDate()

def accumulated_dividend_value(t, port_start_date, port_end_date):
    ''' Sums the value of the dividends for a trade between the portfolio start and end date.
    '''
    
    if t.Instrument().InsType() == 'SecurityLoan':
        i = t.Instrument().Underlying()
        trd_quant = underlying_quantity(t.Quantity(), t.Instrument())
    else:
        i = t.Instrument()
        trd_quant = t.Quantity()
    
    trade_start = t.AcquireDay()
    trade_end = trade_end_date(t)
    
    div_value_sum = 0
    
    # Only sum dividends if the life of the trade intersects the portfolio start and end dates
    if trade_start <= port_end_date and trade_end >= port_start_date:
        
        for div in i.Dividends():
        
            # Check that the record day of the dividend falls within the life of the trade and
            # between the portfolio start and end dates. (intersection of two time intervals)
            if max(port_start_date, trade_start) <= div.RecordDay() <= min(port_end_date, trade_end):
            
                div_value_sum += trd_quant * div.Amount()
                
    return div_value_sum
    
def collateralLevel(t):
    ''' Returns the margin factor associated with an instrument '''
    
    if t.Instrument().InsType() in ('Bill'):
        ins_type = t.AdditionalInfo().MM_Instype()
    else:
        ins_type = t.Instrument().InsType()
    
    if ins_type not in ('SecurityLoan'):
        if ins_type in ('Bond', 'NCD', 'NCC', 'FRN'):
            return 1.10
        # Call and Fixed cash
        elif ins_type in ('Deposit'):
            return 1.05
        elif ins_type in ('Stock'):
            return 1.15
        else:
            return 1

def slInstype(t):
    i = t.Instrument()
    if i.InsType() in ('Bill'):
        return t.AdditionalInfo().MM_Instype()
    elif i.InsType() in ('Deposit'):
        if i.OpenEnd() == 'Open End':
            return 'Call Cash'
        else:
            return 'Fixed Cash'
    else:
        return i.InsType()
        
def is_single_collateral(trade_list):
    ''' Checks to see whether the list of trades contains instruments at a single collateral level
        Security Loans will not be considered '''
    
    margin_factors = set([])
    
    if trade_list:
        for t in [trd for trd in trade_list.AsList() if trd.Status() not in ('Simulated', 'Void')]:
            if t.Instrument().InsType() not in ('SecurityLoan'):
                margin_factors.add(collateralLevel(t))
        
            # As soon as the set contains more than one element we know collateral is mixed.
            if len(margin_factors) > 1:
                return 0
                
    # If we haven't returned a value yet then collateral is single
    return 1


def margin_factor(trade_list):
    ''' Return the collateral level associated with the instruments in a list of trades 
    '''
    
    for t in [trd for trd in trade_list.AsList() if trd.Status() not in ('Simulated', 'Void')]:
        if t.Instrument().InsType() not in ('SecurityLoan'):
            return collateralLevel(t)
    return 1

def getSLPartialReturned(trade):
    return trade.Text1() in ['FULL_RETURN', 'PARTIAL_RETURN']
    
def getSLPartialReturnIsPartOfChain(trade):
    return trade.Oid() != trade.ContractTrdnbr() or trade.Oid() != trade.ConnectedTrdnbr()
    
def getSLPartialReturnFirstTrade(trade):
    if trade.SLPartialReturnIsPartOfChain() and trade.Instrument().InsType() == 'SecurityLoan':
        return trade.Contract()
    else:
        return trade.ConnectedTrdnbr()

def getSLPartialReturnPrevTrade(trade):
    if trade.SLPartialReturnIsPartOfChain() and trade != trade.SLPartialReturnFirstTrade():
        if trade.TrxTrade():
            print "Using trans ref as previous trade."
            return trade.TrxTrade()
        else:
            print "Missing Trans ref on return, using contract ref as previous trade."
            return trade.Contract()
    else:
        return None
        
def getSLPartialReturnNextTrade(trade):
    if trade.SLPartialReturned():
        return trade.ConnectedTrade()
    else:
        return None

def getSLPartialReturnAmountReturned(trade):
    prevTrade = getSLPartialReturnPrevTrade(trade)
    if prevTrade:
        if trade.Instrument().InsType() == 'SecurityLoan':
            return abs(int(round(trade.AddInfoValue("SL_ReturnedQty"))))
        else:
            return abs(int(trade.FaceValue()))

def setSLPartialReturnNextTrade(trade, nextTrade, partOfTransaction = False):
    if not nextTrade:
        nextTrade = trade.SLPartialReturnNextTrade()
        if not nextTrade:
            return
        if not partOfTransaction and nextTrade.SLPartialReturned():
            raise Exception('Cannot clear SLPartialReturnNextTrade on trade %(trade)i. The next trade %(nextTrade)i has been partially returned.' % {'trade': trade.Oid(), 'nextTrade': nextTrade.Oid()})
        tradeConnected = trade
        connected = nextTrade
        contract = nextTrade
        trx = nextTrade
    else:
        tradeConnected = nextTrade
        connected = nextTrade.ConnectedTrade()
        contract = trade.Contract()
        trx = trade
        
    if not partOfTransaction: acm.BeginTransaction()
    try:
        trade.ConnectedTrade(tradeConnected)
        nextTrade.ConnectedTrade(connected)
        nextTrade.Contract(contract)
        nextTrade.TrxTrade(trx)
        if not partOfTransaction: acm.CommitTransaction()
    except Exception, ex:
        if not partOfTransaction: acm.AbortTransaction()
        raise ex
        
def getSLPartialReturnLastTrade(trade, buffer=None):
    if trade.SLPartialReturnIsPartOfChain():
        if not trade.SLPartialReturned():
            return trade
        elif buffer and trade.Oid() in buffer:
            return trade
        else:
            if not buffer:
                buffer = set()
            buffer.add(trade.Oid())
            return getSLPartialReturnLastTrade(trade.SLPartialReturnNextTrade(), buffer)
    else:
        return None

def getValidUnderlyingTypesWithETF(instrument):
    list = instrument.ValidUnderlyingTypes()
    etf = 'ETF'
    if not etf in list:
        list.Add(etf)
    return list


def insTheoPrice(instrument, backDate=None):
    cs = CalculationSpace.from_source(instrument)

    if backDate:
        cs.simulate_value('Valuation Date', backDate)

    for ins in cs:
        return cs[ins].column_value('Price Theor').Value().Number()


def getSLPrice(instrument):
    zero = lambda x: 0
    market_settings = {
        'ETF': {'market':'SPOT', 'fallback': insTheoPrice},
        'Bond': {'market': 'SPOT_BESA', 'fallback': zero},
        'IndexLinkedBond': {'market': 'SPOT_BESA', 'fallback': zero},
    }

    if instrument.InsType() in market_settings.keys():
        if instrument.MtmFromFeed():
            market = market_settings[instrument.InsType()]['market']
            spotMarket = acm.FMarketPlace[market]
    
            for price in instrument.Prices():
                if price.Market() == spotMarket:
                    p = price.Settle()
                    if abs(p) < 0.000001:
                        continue
                    return p
    
            calendar = acm.FCalendar['ZAR Johannesburg']
            hist_limit = calendar.AdjustBankingDays(acm.Time.DateToday(), -2)
            for price in instrument.HistoricalPrices().SortByProperty('Day', False):
                if price.Day() < hist_limit:
                    break
                if price.Market() == spotMarket:
                    p = price.Settle()
                    if abs(p) < 0.000001:
                        continue
                    return p

        return market_settings[instrument.InsType()]['fallback'](instrument)
    else:
        calc = instrument.Calculation()
        theor_val_calc = calc.TheoreticalPrice(CALC_SPACE)
        if theor_val_calc.Value():
            value = theor_val_calc.Value().Number()
            if _is_float_(value) and isnan(value):
                return 0.0
            return value
        else:
            return 0.0


def getHistoricSLPrice(instrument, date):
    zero = lambda x: 0
    market_settings = {
        'ETF': {'market':'SPOT', 'fallback': insTheoPrice},
        'Bond': {'market': 'SPOT_BESA', 'fallback': zero},
        'IndexLinkedBond': {'market': 'SPOT_BESA', 'fallback': zero},
    }

    if date == acm.Time.DateToday():
        return getSLPrice(instrument)

    if instrument.InsType() in market_settings.keys():
        if instrument.MtmFromFeed():
            market = market_settings[instrument.InsType()]['market']
            spotMarket = acm.FMarketPlace[market]
    
            calendar = acm.FCalendar['ZAR Johannesburg']
            hist_limit = calendar.AdjustBankingDays(date, -2)
            for price in instrument.HistoricalPrices().SortByProperty('Day', False):
                if price.Day() > date:
                    continue
                if price.Day() < hist_limit:
                    break
                if price.Market() == spotMarket:
                    p = price.Settle()
                    if abs(p) < 0.000001:
                        continue
                    return p

        return market_settings[instrument.InsType()]['fallback'](instrument, date)
    else:
        return instrument.used_price()


def getSLUnderlying(instrument):
    type = instrument.InsType()
    underlying = None
    if type == 'ETF':
        underlying = instrument
    else:
        underlying = instrument.UnderlyingOrSelf()
    
    return underlying
    
def getQuantityInUnderlying(trade):
    instrument = trade.Instrument()
    instrumentType = instrument.InsType()
    if instrumentType != 'SecurityLoan':
        raise NotImplementedError('Not implemented for instrument type [%s].' % instrumentType)
    
    return underlying_quantity(trade.Quantity(), instrument)
    
def _getBorrowersAndLenders():
    _return = []
    query = acm.CreateFASQLQuery('FParty', 'OR')
    query.AddAttrNode('Name', 'RE_LIKE_NOCASE', 'SLL .*') 
    query.AddAttrNode('Name', 'RE_LIKE_NOCASE', 'SLB .*') 
    for cpty in query.Select():
        _return.append(cpty.Name())
    return _return
    
def _getChoices(name):
    choiceList = acm.FChoiceList.Select01("name = '%s'" % name, "More than one Choice List with name '%s'" % name)
    if not choiceList:
        raise Exception("Could not load Choice List named '%s'" % name)
    
    choices = []
    for choice in choiceList.Choices():
        choices.append(choice)
    return choices

def getG1CounterpartyList(trade):
    _return = []
    #funds = _getChoices('GlobalOneFunds')
    #borrowers = _getChoices('GlobalOneBorrowers')
    #lenders = _getChoices('GlobalOneLenders')
    counterparties = _getBorrowersAndLenders()
    for choice in counterparties: 
        _return.append(choice)
    _return.sort(key = str)
    return _return

def _getGlobalOneTimeStampSpec():
    name = 'SBL_G1SentTime'
    spec = acm.FTimeSeriesSpec[name]
    if not spec:
        raise Exception('Could not load FTimeSeriesSpec %s' % name)
    return spec
    
def _getGlobalOneTimeSeries(trade):
    return acm.FTimeSeries.Select('recaddr=%i and timeSeriesSpec=%i' %(trade.Oid(), _getGlobalOneTimeStampSpec().Oid()))

def getGlobalOneTimeSeriesCount(trade):
    return len(_getGlobalOneTimeSeries(trade))

def setGlobalOneTimeStamp(trade, timeStamp):
    count = getGlobalOneTimeSeriesCount(trade)
    if count >= 2:
        print 'WARNING: Trades cannot have more than 5 timestamps: Trade %i already has %i.' % (trade.Oid(), count)
    
    timeSeries = acm.FTimeSeries()
    timeSeries.TimeSeriesSpec(_getGlobalOneTimeStampSpec())
    timeSeries.Day(acm.Time().DateToday())
    timeSeries.RunNo(count)
    # Front Upgrade 2013.3 -- Value() amended to TimeValue(), method name changed
    timeSeries.TimeValue(timeStamp)
    timeSeries.Recaddr(trade.Oid())
    try:
        timeSeries.Commit()
    except Exception, ex:
        raise Exception('Could not stamp trade %i: %s' % (trade.Oid(), ex))


def getGlobalOneTimeStamp(trade):
    timeSeries = _getGlobalOneTimeSeries(trade)
    if timeSeries:
        # Front Upgrade 2013.3 -- Value() amended to TimeValue(), method name changed
        return timeSeries.Last().TimeValue()
    else:
        return None
    
def globalOneTimeStampExists(trade):
    return True if _getGlobalOneTimeSeries(trade) else False
    
def convert_g1_timeStamp_to_LocalTime(trade):

    if globalOneTimeStampExists(trade):
    
        mt = time.localtime(getGlobalOneTimeStamp(trade))
  
        year = mt[0]       
        month = mt[1]        
        day = mt[2]        
        hour = mt[3]        
        minute = mt[4]        
        second = mt[5]        
        ms = 0
        
        at = acm.Time().LocalTimeAsUTCDays(year, month, day, hour, minute, second, ms)

        return at
        
    else:
        return None
 

    

def getDaysToOneYearExpiry(trade):
    instrument = trade.Instrument()
    instrumentType = instrument.InsType()
    if instrumentType != 'SecurityLoan':
        raise NotImplementedError('Not implemented for instrument type [%s].' % instrumentType)
    
    namespaceTime = acm.Time()
    today = namespaceTime.DateToday()
    oneYear = namespaceTime.DateAddDelta(trade.AcquireDay(), 1, 0, 0)
    return namespaceTime.DateDifference(oneYear, today)


def GetMtMDate(date):
    return CALENDAR.AdjustBankingDays(date, -1)


def DateGenerator(start_date, end_date):
    ''' Generate a stream of dates from start_date to end_date inclusive.
    '''
    next_date = start_date
    while next_date <= end_date:
        yield next_date
        next_date = acm.Time().DateAddDelta(next_date, 0, 0, 1)
    
def InternationalCFDInterest(instrument, start_date, end_date):
    trade = instrument.Trades().At(0)
    leg = instrument.Legs().At(0)
    ins_start_date = instrument.StartDate()
    ins_end_date = leg.EndDate()
    
    # Make sure the security loan is valid between the start and end date
    if ins_end_date > start_date and ins_start_date < end_date:
        interest = 0.0
        rate = leg.FixedRate() / 100.0
        underlying_quant = underlying_quantity(trade.Quantity(), instrument)
        underlying_instrument = instrument.Underlying()
        curr = underlying_instrument.Currency()
        calendar = acm.FCalendar['ZAR Johannesburg']
        
        # Interest calculation start and end date (inclusive)
        if start_date > ins_start_date:
            interest_start_date = start_date
        else:
            interest_start_date = acm.Time().DateAddDelta(ins_start_date, 0, 0, 1)
        
        interest_end_date = min(end_date, ins_end_date)
        
        for date in DateGenerator(interest_start_date, interest_end_date):
            mtm_date = calendar.AdjustBankingDays(date, -1)
            mtm_price = underlying_instrument.MtMPrice(mtm_date, curr, 0)
            mtm_value = mtm_price * underlying_quant / 100.0
            daily_interest =  -1 * mtm_value * rate / 365.0
            interest += daily_interest
        return interest
    else:
        return 0.0

def YTM_To_Price(ins, date, YTM, toDirty, isSettlementDate = True):
    '''
    For a given trade/settlement date, return the clean or dirty price for the given YTM for settlement
    '''
    try:
    
        denominatedvalue = acm.GetFunction('denominatedvalue', 4)
        price = denominatedvalue(YTM, acm.FCurrency['ZAR'], None, date)
        leg = ins.Legs().At(0)
        # Front Upgrade 2013.3 -- leg info & quote to rounded clean unit value changed for 2013.3
        sli = leg.StaticLegInformation(ins, date, None)
        legInf = leg.LegInformation(date)
        
        """
        Upgrade 2016.5 (H)
        
        Old code:
        
        if isSettlementDate:
            result = ins.QuoteToRoundedCleanUnitValueOverrideUnitDate(price, date, date, toDirty, [legInf], [sli], ins.Quotation(), 1.0, 0.0)
        else:
            result = ins.QuoteToRoundedCleanUnitValue(price, date, toDirty, [legInf], [sli], ins.Quotation(), 1.0, 0.0)
        """
        
        if isSettlementDate:
            result = ins.QuoteToUnitValueBase(price, date, date, toDirty, [legInf], [sli], ins.Quotation(), 1.0, 0.0)
        else:
            result = ins.QuoteToUnitValueBase(price, date, date, toDirty, [legInf], [sli], ins.Quotation(), 1.0, 0.0)
        
        
        
        return result.Number() * 100
        
    except Exception, e:
        print "EXCEPTION: Couldn't convert YTM to Price - ", e
        return 0
    
def GetBesaYield(instrument, date):
    ''' Return the SPOT_BESA settle price (stored as a yield) for a given date.
    '''
    market = acm.FParty['SPOT_BESA']
    priceList = acm.FPrice.Select("instrument = %i and market = %i and day = %s" %(instrument.Oid(), market.Oid(), str(date)))
    if priceList:
        price = priceList.At(0)
        return price.Settle()
    else:
        # None is returned so that NaN value is displayed in trading manager so missing prices will be detected.
        return None

def GetBesaDirtyPrice(trade, date):
    ''' Return the BESA dirty price for a given date.
    '''
    instrument = trade.Instrument()
    besaYield = GetBesaYield(instrument, date)
    return YTM_To_Price(instrument, date, besaYield, True, False)


def security_price(instrument, date):
    underlying = instrument.Underlying()
    curr = underlying.Currency()
    mtm_date = GetMtMDate(date)
    if underlying.InsType() in ('Bond', 'IndexLinkedBond'):
        if curr == acm.FCurrency['ZAR']:
            bond_mtm_price = underlying.UsedPrice(mtm_date, curr.Name(), 'SPOT_BESA')
            price_date = CALENDAR.AdjustBankingDays(mtm_date, underlying.SpotBankingDaysOffset())
        else:
            bond_mtm_price = underlying.UsedPrice(mtm_date, curr.Name(), 'internal')
            price_date = mtm_date
        if not bond_mtm_price:
            return 0.0
        all_in_price = underlying.Calculation().PriceToUnitValue(CALC_SPACE, 
                                                                 bond_mtm_price, 
                                                                 underlying.Quotation(), 
                                                                 price_date, 
                                                                 False)
        return all_in_price.Number()
    if underlying.InsType() == 'ETF':
        return underlying.UsedPrice(mtm_date, curr.Name(), 'SPOT')
    if underlying.InsType() == 'FRN':
        return underlying.UsedPrice(mtm_date, curr.Name(), 'SPOT_BESA')
    return underlying.MtMPrice(mtm_date, curr, 0)


def get_initial_price(instrument):
    underlying = instrument.Underlying()
    if underlying.InsType() in ('Bond', 'IndexLinkedBond'):
        return instrument.ContractSize() / instrument.RefValue()
    return instrument.RefPrice()


def CalculateNominalFactor(instrument, date):
    ''' Calculate the nominal factor that would adjust the nominal on a cashflow
        to be equal to the underlying amount multiplied by yesterdays mtm price 
        (where yesterday is calculated according to GetMtMDate)
    '''
    mtm_price = security_price(instrument, date)
    initial_price = get_initial_price(instrument)
    nominal_factor = mtm_price / initial_price
    return nominal_factor if nominal_factor else 1.0


def SLGenerateCashflows(instrument, start_date='', update_leg=False):
    ''' Regenerate cashflows on a security loan, in the case of a CFD the 
        nominal factor is adjusted to scale the nominal.
    '''
    ael_ins = ael.Instrument[instrument.Oid()]
    if not ael_ins:
        raise RuntimeError('Instrument "%s" not found (insaddr: %s).' 
                           % (instrument.Name(), instrument.Oid()))
    sl_cfd = instrument.AdditionalInfo().SL_CFD()
    ael_ins_clone = ael_ins.clone()
    for leg in ael_ins_clone.legs():
        regenerate = False
        fee_rate = leg.fixed_rate
        leg_start = leg.start_day
        regenerate_date = ael.date(start_date) if start_date else leg_start
        if update_leg and leg.pay_day_method != 'None':
            leg.pay_day_method = 'None'
            regenerate = True
        if update_leg and sl_cfd and leg.rolling_period != '1d':
            leg.rolling_period = '1d'
            regenerate = True
        if update_leg and not sl_cfd and leg.rolling_period != '1m':
            leg.rolling_period = '1m'
            regenerate = True
        if (not sl_cfd 
                and leg.rolling_base_day != leg.rolling_base_day.first_day_of_month()):
            base_day = leg_start.first_day_of_month().add_months(1)
            leg.rolling_base_day = base_day
            regenerate = True
        if regenerate or regenerate_date == leg_start:
            leg.regenerate()
            regenerate_date = leg_start
        for cf in leg.cash_flows():
            cf.rate = fee_rate
            if sl_cfd and cf.start_day >= regenerate_date:
                cf_start = acm.Time.DateFromYMD(*cf.start_day.to_ymd())
                nf = CalculateNominalFactor(instrument, cf_start)
                cf.nominal_factor = nf
    ael_ins_clone.commit()
    acm.PollDbEvents()


def SLExtendOpenEnd(self):
    ''' Extend the open end on a security loan to today.
    '''
    instrument = self
    openEnd = instrument.OpenEnd()
    if openEnd != 'Open End':
        raise Exception('Only open ended loans can be extended. Open end status: %s' % openEnd)
    today = acm.Time().DateToday()
    leg = instrument.Legs().At(0)
    
    # Database needs to be polled to detect the updated end date after extension
    while leg.EndDate() <= today:
        instrument.ExtendOpenEnd()
        acm.PollDbEvents()

def SLMenuGenerateCashflows(extensionInvokationInfo):
    ''' Called from the Special Menu on a security loan to regenerate all cashflows on the loan.
    '''
    instrument = extensionInvokationInfo.ExtensionObject().OriginalInstrument()
    instrument.SLGenerateCashflows()
    
def SLMenuExtendOpenEnd(extensionInvokationInfo):
    ''' Called from the Special Menu on a security loan to extend the open end 
        of a loan up until today and then regenerate all the cashflows.
    '''
    instrument = extensionInvokationInfo.ExtensionObject().OriginalInstrument()
    instrument.SLExtendOpenEnd()
    instrument.SLGenerateCashflows()

def SplitCashflow(cashflow, split_date):
    ''' Split the cashflow into single cashflows up until split_date and 
        update the remainder of the cashflow to start at the day after
        split_date.
    ''' 
    assert split_date >= cashflow.StartDate()
    assert acm.Time().DateDifference(cashflow.EndDate(), cashflow.StartDate()) > 1
    
    split_start_date = cashflow.StartDate()
    split_end_date = min(split_date, acm.Time().DateAddDelta(cashflow.EndDate(), 0, 0, -2))
    
    acm.BeginTransaction()
    try:
        instrument = cashflow.Leg().Instrument()
        calendar = cashflow.Leg().PayCalendar()
        for date in DateGenerator(split_start_date, split_end_date):
            end_date = acm.Time().DateAddDelta(date, 0, 0, 1)
            if calendar and calendar.IsNonBankingDay(None, None, end_date):
                pay_date = calendar.AdjustBankingDays(end_date, 1)
            else:
                pay_date = end_date
            single_cashflow = cashflow.Clone()
            single_cashflow.StartDate(date)
            single_cashflow.EndDate(end_date)
            single_cashflow.PayDate(pay_date)
            single_cashflow.NominalFactor(CalculateNominalFactor(instrument, date))
            single_cashflow.Commit()
        
        cashflow.StartDate(end_date)
        cashflow.NominalFactor(CalculateNominalFactor(instrument, end_date))
        cashflow.Commit()
        acm.CommitTransaction()
    except Exception, ex:
        acm.AbortTransaction()
        raise Exception('Cashflow was not split: ' + str(ex))
    
def ExtendTerminatedLoan(instrument):
    ''' When a security loan is terminated for a future date a cashflow is generated
        from today to that future date.  This procedure splits the cashflow into
        single cashflows up until today and updates the rest of cashflow to start 
        tomorrow.
    '''
    leg = instrument.Legs().At(0)
    future_cashflow = None
    
    for cashflow in leg.CashFlows():
        if acm.Time().DateDifference(cashflow.EndDate(), cashflow.StartDate()) > 1:
            future_cashflow = cashflow
    
    today = acm.Time().DateToday()
    if future_cashflow and future_cashflow.StartDate() <= today:
        SplitCashflow(future_cashflow, today)


def get_min_fee_field(trade):
    """
    Return Party's AddInfo field name containing the correct min fee rate.

    Field name rather then field value is returned to enable callings and
    optimizations in different contexts (see e.g. the AEL Module
    FValidation_SecLending).

    """
    if trade.Instrument().UnderlyingType() == 'Bond':
        return 'SL_LenderMinFee_Bd'
    return 'SL_LenderMinFee_Eq'


def _get_lender_min_fee(cpty, trade):
    return getattr(cpty.AdditionalInfo(), get_min_fee_field(trade))()


def calculateLenderCalculatedFee(trade):
    try:
        cpty = acm.FParty[trade.AdditionalInfo().SL_G1Counterparty2()]
    except:
        return 0        
    if cpty:
        mf = _get_lender_min_fee(cpty, trade)
        if not mf:
            mf = 0
        sf = cpty.AdditionalInfo().SL_LenderSplitFee()
        if not sf:
            sf = 0
        fixedrate = trade.Instrument().PayLeg().FixedRate()
        value = max(mf, (sf/100)*fixedrate)
        if value:
            return value
        else:
            return 0
    else:
        return 0

def calculateLenderSplitFee(trade):
    try:
        cpty = acm.FParty[trade.AdditionalInfo().SL_G1Counterparty2()]
    except:
        return 0
    if cpty:
        sf = cpty.AdditionalInfo().SL_LenderSplitFee()
        if sf:
            return str(sf) + " %"
        else:
            return "None"
    else:
        return "None"
    
def calculateLenderMinFee(trade):
    try:
        cpty = acm.FParty[trade.AdditionalInfo().SL_G1Counterparty2()]
    except:
        return 0
    if cpty:
        mf = _get_lender_min_fee(cpty, trade)
        if mf:
            return str(mf)
        else:
            return 0
    else:
        return 0

def calculateSblFlag(buy, sell, children):
    if buy and sell:
        if round(buy, 10) >= round(sell, 10):
            return 0
        else:
            return -1
    else:
        for child in children:
            if child and child < 0.0:
                return 1
    return None

def sl_borrower(trade):
    cp_code = trade.AdditionalInfo().SL_G1Counterparty1()
    if not cp_code:
        return None
    return acm.FParty[cp_code]

def sl_lender(trade):
    cp_code = trade.AdditionalInfo().SL_G1Counterparty2()
    if not cp_code:
        return None
    return acm.FParty[cp_code]

def sl_party_converter(counterparty_string):
    return acm.FParty[counterparty_string]

def sl_true_counterparty(trade):
    counterparty_string = acs.calculate_value('FTradeSheet', trade, 'True Counterparty')
    return acm.FParty[counterparty_string]

def sl_is_sl_party(counterparty_string):
    return counterparty_string.split(" ")[0].startswith("SL")

def getDaysToNinetyDayExpiry(trade):
    if acs.calculate_value('FTradeSheet', trade, 'Less than 90d to 1Y Expiry'):
        return acs.calculate_value('FTradeSheet', trade, 'Less than 90d to 1Y Expiry')
    return acs.calculate_value('FTradeSheet', trade, 'Recall Adjusted Days To 1Y Expiry')

def date_formatter(format_pattern):

    date_formatter = acm.FDateFormatter('date_formatter')
    date_formatter.FormatDefinition(format_pattern)

    return date_formatter


def _is_float_(value):
    try:
        float(value)
        return True
    except Exception as error:
        return False
