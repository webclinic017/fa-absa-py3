import acm
import time
from at import TP_SALES_COVER_CHILD
from FRoutingExtensions import get_fx_rate, trade_system
from FRoutingB2BMethods import SalesDeskPortfolio, SalesDeskAcquirer
'''================================================================================================
================================================================================================'''
def CreateMirrorTrade(original_trade,mirror_portfolio,contactref = 0):
    mirror = original_trade.Clone() 
    mirror.Portfolio( mirror_portfolio )
    mirror.Acquirer( original_trade.Counterparty() )
    mirror.Counterparty( original_trade.Acquirer() )
    mirror.Quantity( -original_trade.Quantity() )
    mirror.Premium( -original_trade.Premium() )
    mirror.MirrorTrade( original_trade )
    mirror.TradeProcess( original_trade.TradeProcess() )
    mirror.ContractTrdnbr( contactref )
    return mirror
'''================================================================================================
================================================================================================'''
def DateString():
    date_string = str(acm.Time.TimeNow())
    time_struct = time.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return str(time_struct[3]) + '-' + str(time_struct[4]) + '-' + str(time_struct[5])
'''================================================================================================
    B2BAcquirerSpt
Example:
    USD/ZAR:AGG|EUR/USD:HDG
Todo:
    Should these methods return the default ?    
================================================================================================'''
def PortfolioSpt(trade,tradeAiProxy,splitCurrencyPair,operationParams = None):
    if tradeAiProxy.B2BPortfolioSpt() == None:
        if operationParams.Portfolio2() == None:  
            return splitCurrencyPair.SpotPortfolio()
        else:
            return operationParams.Portfolio2()
    else:
        try:
            splitCurrencyPairName = splitCurrencyPair.Name()
            for CurrencyPair in tradeAiProxy.B2BPortfolioSpt().split('|'):
                if splitCurrencyPairName == CurrencyPair.split(':')[0]:
                    return acm.FPhysicalPortfolio[CurrencyPair.split(':')[1]]
        except Exception, err:
            print err
'''================================================================================================
    B2BAcquirerFwd
Example:
    USD/ZAR:AGG|EUR/USD:HDG
================================================================================================'''
def PortfolioFwd(trade,tradeAiProxy,splitCurrencyPair,operationParams = None,split = False):
    if tradeAiProxy.B2BPortfolioFwd() == None:
        if operationParams != None:
            if split == False:
                PortfolioFwd =  operationParams.Portfolio4()
            else:
                PortfolioFwd =  operationParams.Portfolio2()
        else:    
            return splitCurrencyPair.ForwardPortfolio()
        if PortfolioFwd == None:
            return splitCurrencyPair.ForwardPortfolio()   
        else:
            return PortfolioFwd
    else:
        try:
            splitCurrencyPairName = splitCurrencyPair.Name()
            for CurrencyPair in tradeAiProxy.B2BPortfolioFwd().split('|'):
                if splitCurrencyPairName == CurrencyPair.split(':')[0]:
                    return acm.FPhysicalPortfolio[CurrencyPair.split(':')[1]]
        except Exception, err:
            print err
'''================================================================================================
================================================================================================'''
def AddInfoOrFxRate( addInfoSpec , currencyPair , valueDate = None): 
    return addInfoSpec if addInfoSpec != None else get_fx_rate(currencyPair, valueDate )  
'''================================================================================================
================================================================================================'''
def AddInfoOrTriangulate( addInfoSpec, currencyPair, currencyPairOne, rateOne, currencyPairTwo,  rateTwo  ):
    return addInfoSpec if addInfoSpec != None else currencyPair.TriangulateRate(currencyPairOne, rateOne, currencyPairTwo, rateTwo)
'''================================================================================================
================================================================================================'''
def GetDrawdownOffsetTrade(instrument, portfolio):
    for trade in instrument.Trades():
        if trade.TradeProcess() == TP_SALES_COVER_CHILD and trade.Portfolio() == portfolio:
            return trade
'''================================================================================================
================================================================================================'''
def PrintTradeDetails(trade):
    print trade.Oid(),\
          trade.Instrument().InsType(),\
          trade.CurrencyPair().Name(),\
          trade.Portfolio().Name(),\
          trade.Acquirer().Name(),\
          trade.Counterparty().Name(),\
          trade.TradeProcessesToString()
'''================================================================================================
Breaks down the tradeProcess representation to tradeProcesses and returns them in a list.
For example: 536879104 becomes [536870912, 8192] which represents [TP_DRAWDOWN_CHILD, 8192]
8192 equals TP_FX_FORWARD in module 'at' but is not imported or used in this module.
================================================================================================'''
def TpBreakdown(tradeProcess):
    result = []
    if tradeProcess == 0:
        result.append(tradeProcess)
        return result
    else:
        bit = 30
        for i in range(bit):
            k = 1 << bit - i - 1
            remainder = tradeProcess % k
            if remainder != tradeProcess: result.append(k)
            if remainder > 0: tradeProcess = remainder
            else: return result
'''================================================================================================
================================================================================================'''
def IsTradeCurrencyPairSpotDateExpired(trade):
    tradeTime =  trade.TradeTime()
    tradeDay = acm.Time.AsDate(tradeTime)
    dateNow = acm.Time.DateNow()
    tradeCPSpotDate = trade.CurrencyPair().SpotDate(tradeDay)
    diff = acm.Time.DateDifference(tradeCPSpotDate, dateNow)
    if  diff < 0:
        return True
    else:
        return False
'''================================================================================================
SpotSplitPair
ForwardSplitCurrency()

why do we even need this ?
================================================================================================'''
def FXStandardTradeAndOperationParametersOverrideHook( trade, tradeParameters, operationParameters ):
    
    #print '***   FXStandardTradeAndOperationParametersOverrideHook'
    salesDesk = SalesDeskPortfolio(trade)
    salesAcquirer = SalesDeskAcquirer(trade)

    if salesDesk is not None:  
        operationParameters.Portfolio4(ConvenienceMethods.GetDefaultPortfolioFromTrade(trade))
        tradePortfolio = operationParameters.Portfolio4()                               #Moved from below
        if tradeParameters.Acquirer(): 
            operationParameters.Acquirer4(tradeParameters.Acquirer())            
        else:
            operationParameters.Acquirer4(operationParameters.Portfolio4().PortfolioOwner())
        tradeParameters.Portfolio(salesDesk)       
        tradeParameters.Acquirer(salesAcquirer)   
    else:
        tradeParameters.Portfolio(ConvenienceMethods.GetDefaultPortfolioFromTrade(trade))
        tradePortfolio = tradeParameters.Portfolio()                                   
        if not tradeParameters.Acquirer():
            tradeParameters.Acquirer(tradeParameters.Portfolio().PortfolioOwner())

    operationParameters.Currency(ConvenienceMethods.GetCoverCurrency(trade))    
    spotCoverPortfolio = trade.CurrencyPair().SpotPortfolio()
    spotCoverPair = trade.CurrencyPair().SpotSplitPair()
 
    if trade.CurrencyPair().IncludesCurrency(acm.FCurrency['USD']) == False:
   
        splitCurrencyPair = trade.CurrencyPair().GetTriangulatingCurrencyPair(spotCoverPair)
        
        splitPortfolio = ConvenienceMethods.GetDefaultPortfolioFromCurrencyPair(splitCurrencyPair, trade)
        operationParameters.Portfolio1(splitPortfolio)                                  
        if not operationParameters.Acquirer1():
            operationParameters.Acquirer1(splitPortfolio.PortfolioOwner())              
  
        if trade.IsFxForward():
            operationParameters.Portfolio2(spotCoverPortfolio)                          
            if not operationParameters.Acquirer2():
                operationParameters.Acquirer2(spotCoverPortfolio.PortfolioOwner())      
            
            if trade.CurrencyPair() != spotCoverPortfolio.CurrencyPair(): 
                spotCoverSplitCurrencyPair = trade.CurrencyPair().GetTriangulatingCurrencyPair(spotCoverPair)
                operationParameters.Portfolio3(spotCoverSplitCurrencyPair.SpotPortfolio())                                   
                if not operationParameters.Acquirer3():
                    operationParameters.Acquirer3(spotCoverSplitCurrencyPair.SpotPortfolio().PortfolioOwner())  

    elif ConvenienceMethods.IsFxForward(trade):                                        

        operationParameters.Portfolio1(spotCoverPortfolio)                              
        if operationParameters.Acquirer2():
            operationParameters.Acquirer1(operationParameters.Acquirer2())                   
        else:
            operationParameters.Acquirer1(spotCoverPortfolio.PortfolioOwner())
        
        if trade.CurrencyPair().IncludesCurrency(acm.FCurrency['USD']) == False:
            spotCoverSplitCurrencyPair = trade.CurrencyPair().GetTriangulatingCurrencyPair(spotCoverPair)
            
            operationParameters.Portfolio2(spotCoverSplitCurrencyPair.SpotPortfolio()) 
            if operationParameters.Acquirer3():
                operationParameters.Acquirer2(operationParameters.Acquirer3())              
            else:
                operationParameters.Acquirer2(spotCoverSplitCurrencyPair.SpotPortfolio().PortfolioOwner())   

'''================================================================================================
Acquirer()
Acquirer(acquirer)
AdditionalInfo()
add_info(field_name)
AllTriangulatingInstrumentPairs()
BusinessDaysBetween(fromDate, toDate)
Cid()
Cid(cid)
ExpiryDate(dateTime, expiryPeriod)
ForwardCalendar()
ForwardCalendar(forwardCalendar)
ForwardCalendarSubstitute()
ForwardCalendarSubstitute(forwardCalendarSubstitute)
ForwardDate(dateTime, period)
ForwardPortfolio()
ForwardPortfolio(portfolio)
ForwardSalesMargin()
ForwardSalesMargin(forwardSalesMargin)
ForwardSplitCurrency()
ForwardSplitCurrency(forwardSplitCurrency)
ForwardSplitPair()
ForwardSplitPair(currPair)
LiquidCrossRate()
LiquidCrossRate(liquidCrossRate)
PointValue()
PointValue(pointValue)
PointValueInverse()
PointValueInverse(pointValueInverse)
PortfolioComparator()
SpotBankingDaysOffset()
SpotBankingDaysOffset(spotBankingDaysOffset)
SpotCalendar()
SpotCalendar(spotCalendar)
SpotCalendarSubstitute()
SpotCalendarSubstitute(spotCalendarSubstitute)
SpotDate(dateTime)
SpotDateInverted(dateTime)
SpotHolidayObservance()
SpotHolidayObservance(spotHolidayObservance)
SpotPortfolio()
SpotPortfolio(portfolio)
SpotSalesMargin()
SpotSalesMargin(spotSalesMargin)
SpotSplitCurrency()
SpotSplitCurrency(spotSplitCurrency)
SpotSplitPair()
SpotSplitPair(currPair)
spot_date([d1])
SweepCurrency()
SweepCurrency(sweepCurrency)
TriangulateRate(instrumentPair1, rate1, instrumentPair2, rate2)
ValidPortfolioChoices(strict)
ValueDayRolloverCutoff()
ValueDayRolloverCutoff(valueDayRolloverCutoff)
ValueDayRolloverTimeZone()
ValueDayRolloverTimeZone(valueDayRolloverTimeZone)

================================================================================================'''
class ConvenienceMethods:

    @staticmethod
    def SpotDate(trade):
        return trade.CurrencyPair().SpotDate(self.Today())

    @staticmethod
    def IsFxForward(trade): #mklimke (done to support ODFs that do not have a trade process function)
    
        instrument = trade.Instrument()
        ins_type = instrument.InsType()

        if ins_type == 'Curr':
            return trade.IsFxForward()

        if ins_type == 'FXOptionDatedFwd':
            if len(instrument.ExerciseEvents()) > 0:
                event = instrument.ExerciseEvents()[0]
                if event.EndDate() > ConvenienceMethods.SpotDate(trade):
                    return True
                else:
                    return False
            else:
                if trade.ValueDay() > ConvenienceMethods.SpotDate(trade):
                    return True
                else:
                    return False

    @staticmethod
    def Today():
        return acm.Time.DateToday()
    
    @staticmethod
    def GetCurrencyCalculation(curr):
        return curr.Calculation()
    
    @classmethod 
    def Rate(self, from_curr, to_curr, date = None):
        
        if type(from_curr) == str:
            from_curr = acm.FCurrency[from_curr]  
        if type(to_curr) == str:
            to_curr = acm.FCurrency[to_curr]
            
        assert(from_curr.IsKindOf(acm.FCurrency))
        assert(to_curr.IsKindOf(acm.FCurrency))

        if from_curr == to_curr:
            return 1.0
        
        if type(date) == str:
            datefunc = acm.GetFunction("date", 1)
            date = datefunc(date)
        else:
            date = from_curr.CurrencyPair(to_curr).SpotDate(self.Today())
        calc_space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        rate = self.GetCurrencyCalculation(from_curr).FXRate(calc_space, to_curr, date)
        return rate.Number()

    @classmethod 
    def SpotDate(self, trade):
        return str(trade.CurrencyPair().SpotDate(self.Today()))
    
   
    @classmethod
    def RateFromCurrencyPair(self, currencyPair, valueDay = None):
        from_currency = currencyPair.Currency1()
        to_currency   = currencyPair.Currency2()        
        return self.Rate(from_currency, to_currency, valueDay)

    @classmethod
    def GetSpotDateFromCurrencyPair(self, currencyPair):
        return currencyPair.SpotDate(self.Today())

    @classmethod
    def GetPriceFromFxSwapFarLeg(self, trade, currencyPair):
        near_leg = trade.ConnectedTrade()
        far_leg = trade
        price = ConvenienceMethods.RateFromCurrencyPair(currencyPair, near_leg.ValueDay())
        far_price = ConvenienceMethods.RateFromCurrencyPair(currencyPair, far_leg.ValueDay())
        return price, far_price        
        
    @classmethod
    def GetPriceAndFarPrice(self, trade, currencyPair):
        if trade.IsFxSwapFarLeg():
            price, far_price = ConvenienceMethods.GetPriceFromFxSwapFarLeg(trade, currencyPair)
        else:
            price = ConvenienceMethods.RateFromCurrencyPair(currencyPair, trade.ValueDay()) 
            far_price = 0
        return price, far_price
   
    @classmethod
    def GetDefaultPortfolioFromTrade(self, trade):
        return self.GetDefaultPortfolioFromCurrencyPair(trade.CurrencyPair(), trade)
   
    @classmethod
    def GetDefaultPortfolioFromCurrencyPair(self, currencyPair, trade):
        if trade.IsFxSpot():
            return currencyPair.SpotPortfolio()
        elif trade.IsFxForward() or trade.IsFxSwapFarLeg():
            return currencyPair.ForwardPortfolio()
        if trade.Instrument().InsType() == 'FXOptionDatedFwd':          #mklimke (needed extending for ODFs)
            if ConvenienceMethods.IsFxForward(trade):
                return currencyPair.ForwardPortfolio()
            else:
                return currencyPair.SpotPortfolio()                     #mklimke (this should never really be true!!!)
        
    @classmethod
    def GetCoverCurrency(self, trade):
        coverCurrency = None
        mappedValuationParameters = acm.GetFunction("mappedValuationParameters", 0)().Parameter()
        accountingCurrency = mappedValuationParameters.AccountingCurrency()
        
        if trade.CurrencyPair().SweepCurrency():
            # Set non-sweep as cover currency
            coverCurrency = trade.CurrencyPair().Currency1()
            if trade.CurrencyPair().Currency1() == trade.CurrencyPair().SweepCurrency():
                coverCurrency = trade.CurrencyPair().Currency2()
        elif trade.CurrencyPair().IncludesCurrency(accountingCurrency):
            coverCurrency = trade.CurrencyPair().Currency1()
            if trade.CurrencyPair().Currency1() == accountingCurrency:
                coverCurrency = trade.CurrencyPair().Currency2()
        else:
            coverCurrency = trade.CurrencyPair().Currency2()
            
        return coverCurrency
        
    @classmethod
    def SetAcquirerAndPortfolioOnNearLeg(self, farLegTrade):
        nearLegTrade = farLegTrade.ConnectedTrade()
        if nearLegTrade:
            nearLegTrade.Portfolio(farLegTrade.Portfolio())
            nearLegTrade.Acquirer(farLegTrade.Acquirer())

    @classmethod  
    def GetOtherSplitCurrencyPair(self, originalCurrencyPair, splitCurrencyPair):
        assert originalCurrencyPair
        return originalCurrencyPair.GetTriangulatingCurrencyPair(splitCurrencyPair)

    @classmethod  
    def GetTriangulatingSpotPrice(self, trade, otherCurrencyPair, otherRate):
        assert trade and otherCurrencyPair and otherRate and trade.CurrencyPair()
        tradeCurrencyPair = trade.CurrencyPair()
        tradeRate = 1/trade.ReferencePrice() if trade.CurrencyPair().Currency1() == trade.Currency() and trade.ReferencePrice() else trade.ReferencePrice()
        triangulatingCurrencyPair = tradeCurrencyPair.GetTriangulatingCurrencyPair(otherCurrencyPair)
        assert triangulatingCurrencyPair
        triangulatingRate = triangulatingCurrencyPair.TriangulateRate(otherCurrencyPair, otherRate, tradeCurrencyPair, tradeRate) if tradeRate else 0
        return triangulatingRate
'''================================================================================================
================================================================================================'''





