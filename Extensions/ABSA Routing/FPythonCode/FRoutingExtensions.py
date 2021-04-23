import time
import acm
#import inspect
from at_time import acm_date
import FRoutingCommon
from at import TP_SWAP_FAR_LEG, TP_SWAP_NEAR_LEG, TP_FX_SPOT, TP_FX_FORWARD
SPACE = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
FXBASECURRENCY = acm.UsedValuationParameters().FxBaseCurrency()
'''================================================================================================
how do you expose something in a class?
================================================================================================'''
class DB:
    DEBUG       = 1 
    LOG         = 2
    WARNING     = 3
    NOTICE      = 4
    TIME        = 5
    EXCEPTION   = 6
    NOTHING     = 7
DEBUG_LEVEL = DB.NOTHING
'''================================================================================================
================================================================================================'''
class Debug(object):

    def __init__(self,level = DEBUG_LEVEL,decsription=''):
        self.__description = decsription
        self.__level = level

    def report(self):
        if self.__level in [DB.DEBUG, DB.LOG, DB.TIME]:
            print ('{0},{1}'.format(self.__funtion.__name__, self.__total_time)), self.__level

    def __call__(self, original_func):
        #@functools.wraps(func)
        self.__funtion = original_func
        def wrappee( *args, **kwargs):
            self.start()
            if DEBUG_LEVEL == DB.EXCEPTION:
                try:
                    self.__return_value = self.__funtion(*args, **kwargs)
                except  Excption, err:
                    print err
                    pass
            else:
                self.__return_value = self.__funtion(*args, **kwargs)        
            self.stop()
            self.report()
            return self.__return_value 
        return wrappee
        
    def start(self):
        self.__start_time = time.time()

    def stop(self): 
        self.__stop_time = time.time()
        self.__total_time = (self.__stop_time - self.__start_time) * 1000
       
'''================================================================================================
================================================================================================'''
def cls(trade):

    if trade.Counterparty() == None or trade.Counterparty().Cls() == 'None': return 0
    CurrencyPair = trade.CurrencyPair()
    Currency1    = CurrencyPair.Currency1()
    Curr1Decomp  = Currency1.Decompositions()
    
    if len(Curr1Decomp) == 0: #use lambda
        return 0
    else:
        Curr1Decomp = Curr1Decomp[0]
 
    if Curr1Decomp.Cls() == False and trade.TradeTime(): return 0
    Currency2   = CurrencyPair.Currency2()
    Curr2Decomp = Currency2.Decompositions()

    if len(Curr2Decomp) == 0:
        return 0
    else:
        Curr2Decomp = Curr2Decomp[0] 

    time_struct = time.strptime(str(trade.TradeTime()), "%Y-%m-%d %H:%M:%S")
    time_struct = str(time_struct[3])+str(time_struct[3])
    time_struct = int(time_struct)
    if time_struct > Curr1Decomp.ClsExternalCutOff() or time_struct > Curr2Decomp.ClsExternalCutOff(): return 0
    return 1    
'''================================================================================================
================================================================================================'''
def create_addinfo(obj,spec,value,commit=True):
    spec = acm.FAdditionalInfoSpec[spec]      
    addInfo = acm.FAdditionalInfo.Select01('recaddr = '+ str(obj.Oid()) + ' and addInf = ' + str(spec.Oid()), '')
    if addInfo == None:
        addInfo=acm.FAdditionalInfo() 
        addInfo.AddInf(spec)
        addInfo.Recaddr(obj)
    addInfo.FieldValue(value)
    if commit: addInfo.Commit()      
'''================================================================================================
================================================================================================'''
def ForwardPair(trade): return trade.CurrencyPair().ForwardSplitPair() if trade.CurrencyPair().ForwardSplitPair() != None else trade.CurrencyPair()
def is_inverse(trade): return trade.CurrencyPair().Currency1() == trade.Currency()
def USDEquivalent(trade): return trade.BaseCostDirty()
def RoutingLongDated(trade): return trade.CurrencyPair().AdditionalInfo().RoutingLongDated()
def RoutingShortDated(trade): return trade.CurrencyPair().AdditionalInfo().RoutingShortDated()
def SSA(trade): return trade.CurrencyPair().AdditionalInfo().SSA()
def RoutingUser(trader): return trader.AdditionalInfo().RoutingUser()
def TradeQuantity(trade): return trade.Quantity() if trade.Instrument().InsType() != 'FXOptionDatedFwd' else trade.ODFQuantity()
def TradePrice(trade): return trade.Price() if trade.Instrument().InsType() != 'FXOptionDatedFwd' else trade.Instrument().InitialExerciseEventStrike() 
def InitialExerciseEventStrike(instrument): return instrument.ExerciseEvents()[0].Strike()
def InitialExerciseEventValueDate(trade): return trade.Instrument().ExerciseEvents()[0].EndDate() if trade.ODFQuantity() < 0 else trade.Instrument().ExerciseEvents()[0].StartDate()
def InitialExerciseEventStartDate(instrument): return instrument.ExerciseEvents()[0].StartDate()
def InitialExerciseEventEndDate(instrument): return instrument.ExerciseEvents()[0].EndDate()
'''================================================================================================
================================================================================================'''
@Debug()
def get_fx_rate(trade, currencyPair,valueDate = None,inverse = False):
    
    if valueDate == None: valueDate = currencyPair.SpotDate(acm.Time.DateNow())
    
    FRoutingCommon.rates[currencyPair]['trade'].ValueDay(valueDate)
    FRoutingCommon.rates[currencyPair]['trade'].AcquireDay(valueDate)
    FRoutingCommon.rates[currencyPair]['trade'].SimulateRecursive()
    FRoutingCommon.rates[currencyPair]['calc_space'].Refresh()
    
    rate = FRoutingCommon.rates[currencyPair]['calculation'].Value().Number()

    if trade.TradeSystem() == 'SML':
        rate_adj = rate * FRoutingCommon.rates[currencyPair]['variance'] / 100
        complement_curr = currencyPair.GetComplementingCurrency(acm.FCurrency['USD']).Name()

        if complement_curr is not None:
            if currencyPair.Currency1().Name() == complement_curr:
                rate_adj = -1 * rate_adj
            if trade.Currency().Name() == complement_curr and trade.Premium() < 0:
                rate_adj = -1 * rate_adj
            if trade.Instrument().Name() == complement_curr and trade.Quantity() < 0:
                rate_adj = -1 * rate_adj
             
        rate = rate + rate_adj
    
    if inverse:
        rate = (1/rate)
        
    assert rate not in (float('nan'), float('inf')), 'Invalid FX Rate for %s' % currencyPair.Name()    
    return round(rate, 6)

'''================================================================================================
================================================================================================'''
def AddTenorDaystoSpot(CurrencyPair):

    Spot = CurrencyPair.SpotDate(acm.Time.DateNow())
    SpotHolidayObservance = CurrencyPair.SpotHolidayObservance()
    RoutingTenor = CurrencyPair.AdditionalInfo().RoutingTenorDays() - CurrencyPair.SpotBankingDaysOffset()
    Calendar1 = CurrencyPair.Currency1().Calendar()
    Calendar2 = CurrencyPair.Currency2().Calendar()
    BaseCalendar = FXBASECURRENCY.Calendar()
    Count = 0        

    if SpotHolidayObservance == 'Split Via Base':
        while Count < RoutingTenor:
            Spot = acm.Time().DateAddDelta(Spot, 0, 0, 1)
            if (Calendar1.IsNonBankingDay(None, None, Spot) == False and Calendar2.IsNonBankingDay(None, None, Spot) == False and BaseCalendar.IsNonBankingDay(None, None, Spot) == False):
                Count = Count + 1  
                
    elif SpotHolidayObservance == 'Spot Days In Both': 
        while Count < RoutingTenor:
            Spot = acm.Time().DateAddDelta(Spot, 0, 0, 1)
            if (Calendar1.IsNonBankingDay(None, None, Spot) == False and Calendar2.IsNonBankingDay(None, None, Spot) == False):
                Count = Count + 1  
                
    elif SpotHolidayObservance == 'Spot Days In Non-Base':
        if CurrencyPair.Currency1() == FXBASECURRENCY:
            while Count < RoutingTenor:
                Spot = acm.Time().DateAddDelta(Spot, 0, 0, 1)
                if Calendar2.IsNonBankingDay(None, None, Spot) == False: 
                    Count = Count + 1  
        
        elif CurrencyPair.Currency2() == FXBASECURRENCY:
            while Count < RoutingTenor:
                Spot = acm.Time().DateAddDelta(Spot, 0, 0, 1)
                if Calendar1.IsNonBankingDay(None, None, Spot) == False:
                    Count = Count + 1  
        else:
            while Count < RoutingTenor:
                Spot = acm.Time().DateAddDelta(Spot, 0, 0, 1)
                if (Calendar1.IsNonBankingDay(None, None, Spot) == False and Calendar2.IsNonBankingDay(None, None, Spot) == False):
                    Count = Count + 1  
    return Spot
'''================================================================================================
================================================================================================'''
@Debug()
def IsSpotOrLess(trade): 
    TradePair = trade.CurrencyPair()
    VD = trade.ValueDay()
    TradeTD = AddTenorDaystoSpot(TradePair)
    if TradePair.IncludesCurrency('USD'):
        return True if VD <= TradeTD else False
    else:
        SplitPair = TradePair.SpotSplitPair()
        SplitTD = AddTenorDaystoSpot(SplitPair)
        SalesTD = AddTenorDaystoSpot(TradePair.GetTriangulatingCurrencyPair(SplitPair))
        return True if (VD <= TradeTD and VD <= SplitTD and VD <= SalesTD) else False
'''================================================================================================
================================================================================================'''
@Debug()
def SplitCurrencyPair(trade):
    tradeCurrencyPair = trade.CurrencyPair()
    SpotSplitPair = tradeCurrencyPair.SpotSplitPair()
    if SpotSplitPair != None: return SpotSplitPair.GetTriangulatingCurrencyPair(tradeCurrencyPair).Name()
'''================================================================================================
================================================================================================'''
@Debug()
def SplitPairSSA(trade):
    splitpair= None
    tradeCurrencyPair = trade.CurrencyPair()
    SpotSplitPair = tradeCurrencyPair.SpotSplitPair()
    if SpotSplitPair != None: splitpair = SpotSplitPair.GetTriangulatingCurrencyPair(tradeCurrencyPair)
    if splitpair != None: return splitpair.AdditionalInfo().SSA()
'''================================================================================================
================================================================================================'''
@Debug()
def SplitCurrencyPairRoutingLongDated(trade):
    tradeCurrencyPair = trade.CurrencyPair()
    SpotSplitPair = tradeCurrencyPair.SpotSplitPair()
    if SpotSplitPair == None: return 'NoSplit'    
    triangulatedSplitCurrencyPair  = SpotSplitPair.GetTriangulatingCurrencyPair(tradeCurrencyPair)
    if triangulatedSplitCurrencyPair == None: return 'NoSplit'
    return triangulatedSplitCurrencyPair.AdditionalInfo().RoutingLongDated()
'''================================================================================================
================================================================================================'''
@Debug()
def SplitCurrencyPairRoutingSpot(trade):
    tradeCurrencyPair = trade.CurrencyPair()
    SpotSplitPair = tradeCurrencyPair.SpotSplitPair()
    if SpotSplitPair == None: return 'NoSplit'
    triangulatedSplitCurrencyPair  = SpotSplitPair.GetTriangulatingCurrencyPair(tradeCurrencyPair)
    if triangulatedSplitCurrencyPair == None: return 'NoSplit'
    return triangulatedSplitCurrencyPair.AdditionalInfo().RoutingShortDated()    
'''================================================================================================
================================================================================================'''
def ODFQuantity(trade):
    if trade.Instrument().InsType() == 'FXOptionDatedFwd':
        return -1 * trade.Quantity() if trade.Instrument().IsCallOption() == False else trade.Quantity()
    else:   
        return trade.Quantity() 
'''================================================================================================
================================================================================================'''
def ExtendReference(trade):
    BE = trade.BusinessEvents('End Day Extension')
    if len(BE) > 0:
        for tradeLink in BE[0].TradeLinks():
            if tradeLink.Trade() != trade:
                return tradeLink.Trade()
'''================================================================================================
================================================================================================'''
def trade_system(trade):
    if trade.Counterparty().Name() == 'MIDAS DUAL KEY':
        return 'MIDAS CFR'
    instrument  = trade.Instrument()
    if trade.GroupTrdnbr()!= None:
        trade = trade.GroupTrdnbr()
    elif (not trade.OptionalKey()) and trade_system(trade.GetMirrorTrade()) == 'OWM':
        trade = trade.GetMirrorTrade()         
    key = trade.OptionalKey() if instrument.InsType() in ['Curr', 'FXOptionDatedFwd'] else instrument.ExternalId1()
    if len(key.split('|')) > 1: return key.split('|')[1]
'''================================================================================================
================================================================================================'''
def reuters_feed(trade):
    instrument  = trade.Instrument()
    if trade.GroupTrdnbr()!= None: trade = trade.GroupTrdnbr()
    key = trade.OptionalKey() if instrument.InsType() in ['Curr', 'FXOptionDatedFwd'] else instrument.ExternalId1()
    if len(key.split('#')) > 1: return key.split('#')[0]
'''================================================================================================
================================================================================================'''
def midas_dealno(trade):
    instrument = trade.Instrument()
    if trade.IsFxSwapFarLeg(): trade = trade.FxSwapNearLeg()
    if trade.GroupTrdnbr()!= None: trade = trade.GroupTrdnbr()
    return str(trade.YourRef()).split('|')[0]  
'''================================================================================================
================================================================================================'''
def IsSalesMargin(trade):
    try:
        list = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', 'FRoutingParameters').Value()['NoSalesMargin'].Split(',')
        return False if trade_system(trade) in list else True
    except Exception, e:
        print 'Failed to find NoSalesMargin parameter in FRoutingParameters'
        return True
'''================================================================================================
================================================================================================'''
def SuppressPips(trade):
    try:
        list = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', 'FRoutingParameters').Value()['SuppressPips'].Split(',')
        return True if trade_system(trade) in list else False
    except Exception, e:
        print 'Failed to find SuppressPips parameter in FRoutingParameters'
        return False  
'''================================================================================================
================================================================================================'''
def IsAfricanInterbank(party):
    if party.RiskCountry() != None and party.BusinessStatus() != None:
        businessStatus = party.RiskCountry().Name()
        if party.BusinessStatus().Name() == 'Interbank' and ('Africa' in businessStatus and businessStatus != 'Africa/South Africa'):
            return True
    return False
'''================================================================================================
================================================================================================'''

