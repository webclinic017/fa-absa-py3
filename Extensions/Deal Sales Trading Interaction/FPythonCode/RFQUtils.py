import acm

from SalesTradingCustomizations import IsYieldQuoted, OrderBookCreation, ButtonLabels
from SalesTradingCustomizations import PriceAndMarginConversions as ConversionCustomizations

from DealPackageDevKit import DealPackageUserException
from DealPackageUtil import FormatException, UnDecorate, SalesTradingInfo, SalesTradingInteraction
from DealPackageUtil import SetNew as UtilSetNew
from DealPackageUtil import InstrumentSetNew_Filter as UtilInstrumentSetNew_Filter

'''********************************************************************
* Get/Set Method helpers
********************************************************************'''        
class MethodDirection(object):
    asGetMethod = '*NotUsed*'

    @staticmethod
    def AsGetMethod(val):
        return MethodDirection.asGetMethod == val
        
'''********************************************************************
* Direction
********************************************************************'''        
class Direction(object):
    bid = 'Bid'
    ask = 'Ask'
    twoWay = ''

    @staticmethod
    def IsAsk(direction):
        return direction == Direction.ask

    @staticmethod
    def IsBid(direction):
        return direction == Direction.bid

    @staticmethod
    def IsTwoWay(direction):
        return direction == Direction.twoWay

    @staticmethod
    def Opposite(direction):
        opposite = Direction.twoWay
        if Direction.IsAsk(direction):
            opposite = Direction.bid
        elif Direction.IsBid(direction):
            opposite = Direction.ask
        return opposite

    @staticmethod
    def FromQuantity(quantity, instrument):
        if quantity > 0.0:
            direction = Direction.bid if instrument.IsSwap() and instrument.SwapType() != 'Float/Float' and instrument.RecLeg().IsFixedLeg() else Direction.ask
        else:
            direction = Direction.ask if instrument.IsSwap() and instrument.SwapType() != 'Float/Float' and instrument.RecLeg().IsFixedLeg() else Direction.bid
        return direction
    
    @staticmethod
    def FromQuoteRequestInfo(quoteRequestInfo, direction=None):
        return 'Bid' if quoteRequestInfo.BidOrAsk() == 'Bid' else 'Ask'
    
    @staticmethod
    def Color(direction, instrument):
        buy = Colors.colors['Buy']
        sell = Colors.colors['Sell']
        twoWay = Colors.colors['2Way']
        color = twoWay
        if Direction.IsAsk(direction):
            color = buy
        elif Direction.IsBid(direction):
            color = sell
        return color

    @staticmethod    
    def Label(direction, instrument):
        return ButtonLabels.FullLabel(direction, instrument)

'''********************************************************************
* Status
********************************************************************'''     
def StatusDisplayName(status):
    return acm.GetDefaultContext().GetExtension('FStringResource', acm.FQuotePrice, status).Value()
    
class Status(object):
    pending = StatusDisplayName('Request Quote')
    firm = StatusDisplayName('Quote Firm')
    stream = StatusDisplayName('Quote Firm Stream')
    proposed = 'Proposed'
    subject = StatusDisplayName('Quote Subject')
    subjAccept = StatusDisplayName('Request Quote Subject Accepted')
    countered = StatusDisplayName('Request Quote Countered')
    delayed = StatusDisplayName('Request Quote Delayed')
    accepting = StatusDisplayName('Pending Deal')
    accepted = StatusDisplayName('Quote Accepted')
    expired = StatusDisplayName('Quote Expired')
    passed = StatusDisplayName('Quote Rejected')
    cancelled = StatusDisplayName('Request Cancelled')
    noAnswer = StatusDisplayName('Request Expired')
    rejected = StatusDisplayName('Request Rejected')

    @staticmethod
    def PingPongChoices():
        return [Status.pending, Status.firm, Status.stream, Status.subject, Status.subjAccept, 
            Status.countered, Status.delayed, Status.accepting, Status.accepted, Status.expired, 
            Status.passed, Status.cancelled, Status.noAnswer, Status.rejected]

    @staticmethod
    def Default(role):
        if role == 'Trading':
            return [Status.countered, Status.pending, Status.subjAccept, Status.subject]
        elif role == 'Sales':
            return [Status.expired, Status.firm, Status.noAnswer, Status.rejected, Status.stream]
        return []

'''********************************************************************
* Colors
********************************************************************'''    
def CreateColor(name):
    color = acm.GetDefaultContext().GetExtension('FColor', acm.FColor, name)
    return color.Value()    
    
class Colors(object):
    colors =    {'Buy' : CreateColor('BuyColor'), 
                 'Sell': CreateColor('SellColor'), 
                 '2Way': CreateColor('TwoWayColor'),
                 'Buy_Inactive' : CreateColor('BuyColor_Inactive'), 
                 'Sell_Inactive': CreateColor('SellColor_Inactive'), 
                 '2Way_Inactive': CreateColor('TwoWayColor_Inactive'),
                 'Bkg' : CreateColor('Background')}  
    
    @staticmethod
    def Color(colorName):
        return Colors.colors[colorName]

'''********************************************************************
* Time 
********************************************************************'''   
class Time(object):
    secondsSpanFormatter = acm.FDateTimeSpanFormatter('SecondsSpan')
    onlyIfTodayFormatter = acm.FDateTimeFormatter('TimeOnlyIfToday')

    @staticmethod
    def TimeLeft(timeOrExpiry):
        time = timeOrExpiry
        if isinstance(timeOrExpiry, basestring):
            time = (acm.Time.DateTimeToTime(timeOrExpiry) - acm.Time.DateTimeToTime(acm.Time.TimeNow())) / (24.0 * 3600.0)
        return time
    
    @staticmethod
    def ExpiryDateTime(timeLeftOrExpiry):
        expiry = timeLeftOrExpiry
        if not isinstance(timeLeftOrExpiry, basestring):
            expiry = acm.Time.DateTimeFromTime(int(timeLeftOrExpiry * 24.0 * 3600.0) + acm.Time.DateTimeToTime(acm.Time.TimeNow()))
        return expiry

    @staticmethod
    def ParsePeriod(inputStr):
        def IsInt(s):
            try: 
                int(s)
                return True
            except ValueError:
                return False
        
        isValid = False
        countStr = inputStr[0:-1]
        if IsInt(countStr):
            if inputStr[-1] == 'h' or inputStr[-1] == 'm':
                unit = inputStr[-1]
                count = int(countStr)
                isValid = True
        if isValid:
            return count, unit
        else:
            return False

    @staticmethod
    def PeriodToSeconds(inputStr):
        seconds = ''
        hourOrMinutePeriod = Time.ParsePeriod(inputStr)
        if hourOrMinutePeriod:
            if hourOrMinutePeriod[1] == 'h':
                seconds = hourOrMinutePeriod[0] * 3600
            elif hourOrMinutePeriod[1] == 'm':
                seconds = hourOrMinutePeriod[0] * 60
        return seconds

    @staticmethod
    def PeriodToDateTime(period):
        dateTime = ''
        if Time.ParsePeriod(period):
            time = int(acm.Time.DateTimeToTime(acm.Time.TimeNow()) + Time.PeriodToSeconds(period))
            dateTime = acm.Time.DateTimeFromTime(time)
        else:
            today = acm.Time().TodayAt(23, 59, 59, 0, False)
            dateTime = acm.Time().DateTimeAdjustPeriod(today, period, None, 0)
        return dateTime

    @staticmethod
    def ParseTimeSpan(inputStr):
        if inputStr and isinstance(inputStr, basestring):
            if Time.ParsePeriod(inputStr):
                inputStr = str( Time.PeriodToSeconds(inputStr) )
            else:
                splitStr = inputStr.split(':')
                if len(splitStr) == 2:
                    inputStr = str( float(splitStr[0])*60+float(splitStr[1]) )
                elif len(splitStr) == 3:
                    inputStr = str( float(splitStr[0])*3600 + float(splitStr[1])*60+float(splitStr[2]) )
        return inputStr

    @staticmethod
    def MaxExpiry(timeOrExpiry1, timeOrExpiry2):
        time1 = Time.TimeLeft(timeOrExpiry1)
        time2 = Time.TimeLeft(timeOrExpiry2)
        return acm.Time.DateTimeFromTime(max(time1, time2))

    @staticmethod
    def MinExpiry(timeOrExpiry1, timeOrExpiry2):
        time1 = Time.TimeLeft(timeOrExpiry1)
        time2 = Time.TimeLeft(timeOrExpiry2)
        return acm.Time.DateTimeFromTime(min(time1, time2))

    @staticmethod
    def Compare(timeOrExpiry1, timeOrExpiry2):
        time1 = Time.TimeLeft(timeOrExpiry1)
        time2 = Time.TimeLeft(timeOrExpiry2)
        return time1 > time2
    
    @staticmethod
    def SecondsSpanFormat(time):
        return Time.secondsSpanFormatter.Format(time)
    
    @staticmethod
    def OnlyIfTodayFormat(time):
        return Time.onlyIfTodayFormatter.Format(time)
    
    @staticmethod
    def OnlyIfTodayParse(inputStr):
        return Time.onlyIfTodayFormatter.Parse(inputStr)
    
    @staticmethod
    def DateTimeToMilliseconds(fraction):
        if fraction:
            ms = fraction * 86400000
        else:
            ms = -1
        return ms
    
'''********************************************************************
* History direction from Quote Price Status
********************************************************************'''        
class HistoryDirectionMap(object):
    auto = [Status.noAnswer, Status.expired, Status.accepted]
    traderUpdates = [Status.rejected, Status.firm, Status.subject]
    salesUpdates = [Status.pending, Status.cancelled, Status.passed, Status.subjAccept, Status.countered]

    @staticmethod
    def Initiator(status, previousStatus):
        initiator = ''
        if status == Status.accepting:
            initiator = 'Sales' if previousStatus == Status.firm or previousStatus == Status.proposed else 'Trader'
        elif status in HistoryDirectionMap.auto:
            initiator = 'Auto'
        elif status in HistoryDirectionMap.traderUpdates:
            initiator = 'Trader'
        elif status in HistoryDirectionMap.salesUpdates:
            initiator = 'Sales'
        else:
            print ('Status update, status: ' + str(status) + ' unhandled')
        return initiator

'''********************************************************************
* Price, AllInPrice, Margin triangulation
********************************************************************'''        
class PriceAndMarginConversions(object):
    @staticmethod
    def ShouldSubtractSpread(tradingInterface, instrument, directionIsAsk):
        isYieldQuoted = IsYieldQuoted(tradingInterface, instrument)
        return bool(isYieldQuoted) == bool(directionIsAsk)
        
    @staticmethod
    def AllInPrice(spread, price, directionIsAsk, tradingInterface, instrument):
        sign = spread/abs(spread) if spread != 0 else 1
        priceDiff = ConversionCustomizations.PriceDifferenceFromMargin(abs(spread), tradingInterface, instrument)
        priceDiff *= sign
        allInPrice = price + (-1 if PriceAndMarginConversions.ShouldSubtractSpread(tradingInterface, instrument, directionIsAsk) else 1) * priceDiff
        return allInPrice

    @staticmethod
    def Price(spread, allInPrice, directionIsAsk, tradingInterface, instrument):
        sign = spread/abs(spread) if spread != 0 else 1
        priceDiff = ConversionCustomizations.PriceDifferenceFromMargin(abs(spread), tradingInterface, instrument)
        priceDiff *= sign
        traderPrice = allInPrice + (1 if PriceAndMarginConversions.ShouldSubtractSpread(tradingInterface, instrument, directionIsAsk) else -1) * priceDiff
        return traderPrice
     
    @staticmethod
    def Spread(price, allInPrice, directionIsAsk, tradingInterface, instrument):
        sign = 1 if (allInPrice-price > 0) else -1
        spread = ConversionCustomizations.MarginFromPriceDifference(abs(allInPrice-price), tradingInterface, instrument) 
        spread *= sign * (-1 if PriceAndMarginConversions.ShouldSubtractSpread(tradingInterface, instrument, directionIsAsk) else 1)
        return spread  

    @staticmethod
    def MarginAmount(price, allInPrice, trade, dealPackage, tradingInterface, directionIsAsk, *args):
        marginAmount = 0
        instrument=trade.Instrument()
        if dealPackage and not dealPackage.IsDeal():
            for trd in dealPackage.Trades():
                marginAmount += PriceAndMarginConversions.CalculatePVDifference(trd, instrument, allInPrice, price, tradingInterface)
        else:
            marginAmount = PriceAndMarginConversions.CalculatePVDifference(trade, instrument, allInPrice, price, tradingInterface)
        if directionIsAsk:
            return -marginAmount
        else:
            return marginAmount

    @staticmethod
    def CalculatePVDifference(trade, instrument, allInPrice, price, tradingInterface):
        calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet' )        
        if OrderBookCreation.IsPriceBased(instrument):
            return PriceAndMarginConversions.TradePriceScenario(calcSpace, trade, instrument, allInPrice, price)
        elif PriceAndMarginConversions.PriceAsFixedRate(instrument, tradingInterface):
            return PriceAndMarginConversions.FixedRateScenario(calcSpace, trade, instrument, allInPrice, price)
        elif PriceAndMarginConversions.PriceAsSpread(instrument, tradingInterface):
            return PriceAndMarginConversions.FloatSpreadScenario(calcSpace, trade, instrument, allInPrice, price)
        else:
            raise DealPackageUserException("Cannot handle non-price based instrument '%s'" % instrument.Name()) 
     
    @staticmethod
    def FixedRateScenario(calcSpace, trade, instrument, allInPrice, price):
        fixedRateCalc = calcSpace.CreateCalculation(trade, 'Fixed Rate')
        calcSpace.SimulateValue(trade, 'Fixed Rate', price)
        calc = calcSpace.CreateCalculation(trade, 'Portfolio Total Profit and Loss')
        pvClean=calc.Value().Number()
        calcSpace.SimulateValue(trade, 'Fixed Rate', allInPrice)
        pvMargin = calcSpace.CreateCalculation(trade, 'Portfolio Total Profit and Loss').Value().Number()
        calcSpace.RemoveSimulation(trade, 'Fixed Rate')
        if PriceAndMarginConversions.OppositeMarginAmount(instrument):
            return pvClean-pvMargin
        else:
            return pvMargin-pvClean

    @staticmethod
    def FloatSpreadScenario(calcSpace, trade, instrument, allInPrice, price):
        floatSpreadCalc = calcSpace.CreateCalculation(trade, 'Float Spread')
        calcSpace.SimulateValue(trade, 'Float Spread', price)
        calc = calcSpace.CreateCalculation(trade, 'Portfolio Total Profit and Loss')
        pvClean=calc.Value().Number()
        calcSpace.SimulateValue(trade, 'Float Spread', allInPrice)
        pvMargin = calcSpace.CreateCalculation(trade, 'Portfolio Total Profit and Loss').Value().Number()
        calcSpace.RemoveSimulation(trade, 'Float Spread')
        if PriceAndMarginConversions.OppositeMarginAmount(instrument):
            return pvClean-pvMargin
        else:
            return pvMargin-pvClean
            
    @staticmethod
    def TradePriceScenario(calcSpace, trade, instrument, allInPrice, price):
        priceCalc = calcSpace.CreateCalculation(trade, 'Price Edit')
        calcSpace.SimulateValue(trade, 'Price Edit', price)
        if instrument.ReportDate(0) in ['Instrument Spot', 'Grouping Spot']:
            columnName = 'Portfolio Total Profit and Loss'
        else:
            columnName = 'Portfolio Book Total Profit and Loss'
        calc = calcSpace.CreateCalculation(trade, columnName)
        pvClean=calc.Value().Number()
        calcSpace.SimulateValue(trade, 'Price Edit', allInPrice)
        pvMargin = calcSpace.CreateCalculation(trade, columnName).Value().Number()
        calcSpace.RemoveSimulation(trade, 'Price Edit')
        return pvMargin-pvClean
        
    @staticmethod
    def OppositeMarginAmount(instrument):
        return (instrument.IsSwap() and instrument.SwapType() != 'Float/Float' and instrument.RecLeg().IsFixedLeg()) or instrument.IsRepoInstrument() or instrument.InsType() == 'Deposit'
            
    @staticmethod
    def PriceAsFixedRate(instrument, tradingInterface):
        return PriceAndMarginConversions.QuotationIsCoupon(instrument, tradingInterface) or PriceAndMarginConversions.IsFixedLegSecLoanOrRepo(instrument)
    
    @staticmethod    
    def PriceAsSpread(instrument, tradingInterface):
        return PriceAndMarginConversions.QuotationIsSpreadBps(instrument, tradingInterface) or PriceAndMarginConversions.IsFloatLegSecLoanOrRepo(instrument)
        
    @staticmethod
    def QuotationIsSpreadBps(instrument, tradingInterface=None):
        quotation = OrderBookCreation.Quotation(instrument, tradingInterface)
        return quotation.Name() == 'Spread bps'
        
    @staticmethod
    def QuotationIsCoupon(instrument, tradingInterface=None):
        quotation = OrderBookCreation.Quotation(instrument, tradingInterface)
        return quotation.Name() == 'Coupon'
    
    @staticmethod    
    def IsFloatLegSecLoanOrRepo(instrument):
        return instrument.InsType() in ['SecurityLoan', 'Repo/Reverse', 'BasketRepo/Reverse', 'BasketSecurityLoan'] and instrument.FirstFloatLeg()
        
    @staticmethod    
    def IsFixedLegSecLoanOrRepo(instrument):
        return instrument.InsType() in ['SecurityLoan', 'Repo/Reverse', 'BasketRepo/Reverse', 'BasketSecurityLoan'] and instrument.FirstFixedLeg()

    @staticmethod
    def Margin(marginAmount, trade, dealPackage, *args):
        totalNominal = 0
        if dealPackage:
            for trd in dealPackage.Trades():
                totalNominal += trd.Nominal()
        else:
            totalNominal += trade.Nominal()
        priceDiff = marginAmount / totalNominal if totalNominal != 0 else 0
        margin = ConversionCustomizations.MarginFromPriceDifference(priceDiff, None, trade.Instrument())
        if trade.Instrument().IsSpreadInBasisPoints():
            margin *= 100
        return margin

'''********************************************************************
* Validation
********************************************************************'''        
class Validation(object):
    @staticmethod
    def CounterPrice(traderPrice, counterPrice, isAskSide, isYieldQuoted):
        priceValid = False 
        if isAskSide:
            if isYieldQuoted:
                priceValid = counterPrice > traderPrice
            else:
                priceValid = counterPrice < traderPrice
        else:
            if isYieldQuoted:
                priceValid = counterPrice < traderPrice
            else:
                priceValid = counterPrice > traderPrice
        return priceValid
    
    @staticmethod
    def Nominal(nominal, instrument, amountLabel='Nominal'):
        if nominal <= 1e-12:
            raise DealPackageUserException(amountLabel + ' must be greater than zero')
        trade = acm.DealCapturing.CreateNewTrade(instrument)
        trade.Nominal = nominal
        trade = acm.FBusinessLogicDecorator.WrapObject(trade, instrument.GUI())
        trade.CheckNominal()
    
    @staticmethod
    def MinimumAmount(minAmount, amount, amountLabel):
        if minAmount > amount:
            raise DealPackageUserException('Minimum ' + amountLabel + ' cannot be greater than total ' + amountLabel)
        if minAmount < -1e-12:
            raise DealPackageUserException('Minimum ' + amountLabel + ' must be at least zero')
    
    @staticmethod
    def Instrument(instrument):
        if instrument.Originator().StorageId() < 0:
            raise DealPackageUserException('Instrument is not Persisted')
            
    @staticmethod
    def InstrumentIsExpired(instrument):
        if instrument.IsExpired():
            raise DealPackageUserException('Instrument is Expired')
    
    @staticmethod
    def ValidateModifyQuoteRequestBroker(task):
        try:
            task.ResultOrThrow()
            return True
        except Exception as e:
            print ('Modify Quote Request Broker Failed')
    
    @staticmethod
    def IsMarket(marketName):
        market = acm.FMarketPlace[marketName]
        if not market:
            raise DealPackageUserException('Customization Module contains errors (not a valid Market): ' + marketName)
        return market 
    
    @staticmethod
    def IsConnected(marketPlace):
        if marketPlace and not marketPlace.IsConnected():
            errorStr = 'Market %s not available' % marketPlace.Name()
            raise DealPackageUserException(errorStr)

'''********************************************************************
* Quantity/Nominal
********************************************************************'''  
class Amount(object):
    @staticmethod
    def UseQuantity(instrument, dealPackage):
        return SalesTradingInteraction.UseQuantity(instrument, dealPackage)

    @staticmethod
    def TopAmountLabel(nomInQuot, dealPackage):
        formattedLabel = acm.Get('formats/InstrumentDefinitionQuantity').Format(nomInQuot)
        if nomInQuot and dealPackage:
            amountInfo = dealPackage.GetAttribute('salesTradingInteraction').At('amountInfo')
            if amountInfo:
                amountLabelAttr = amountInfo.At('amountLabelAttr') if hasattr(amountInfo, 'At') else amountInfo.get('amountLabelAttr')
                if amountLabelAttr:
                    formattedLabel = dealPackage.GetAttribute(amountLabelAttr)
                    formatter = dealPackage.GetAttributeMetaData(amountLabelAttr, 'formatter')()
                    if formatter:
                        formattedLabel = formatter.Format(formattedLabel)
        return formattedLabel
    
    @staticmethod
    def QuantityLabel(label, dealPackage):
        if dealPackage and not dealPackage.IsDeal():
            amountInfo = dealPackage.GetAttribute('salesTradingInteraction').At('amountInfo')
            if amountInfo:
                name = amountInfo.At('name') if hasattr(amountInfo, 'At') else amountInfo.get('name')
                if name:
                    label = name
        return label
    
    @staticmethod
    def QuotationLabel(instrument, dealPackage):
        label = ''
        if dealPackage and not dealPackage.IsDeal():
            amountInfo = dealPackage.GetAttribute('salesTradingInteraction').At('amountInfo')
            if amountInfo:
                quotationLabelAttr = amountInfo.At('quotationLabelAttr') if hasattr(amountInfo, 'At') else amountInfo.get('quotationLabelAttr')
                if quotationLabelAttr:
                    quotation = dealPackage.GetAttribute(quotationLabelAttr)
                    if hasattr(quotation, 'IsKindOf') and quotation.IsKindOf(acm.FQuotation):
                        label = quotation.Name()
                    else:
                        label = quotation
        if not label:
            tradingInterface = TradingInterface.Get(instrument)
            quotation = tradingInterface.PriceFeed().Quotation() if tradingInterface else None
            if not quotation:
                quotation = OrderBookCreation.Quotation(instrument, tradingInterface)
            label = quotation.Name()
        return label

    @staticmethod 
    def NominalToQuantity(nominal, insNominal):
        if insNominal:
            quantity = nominal / insNominal
        else:
            quantity = 0.0
        return quantity

    @staticmethod 
    def QuantityToNominal(quantity, insNominal):
        insNominal = insNominal if insNominal else 0.0
        return insNominal * quantity

    @staticmethod
    def QuoteMetricFactor(quotation):
        quoteMetricFactor = 1.0
        if quotation:
            quoteMetricFactor = quotation.QuotationFactor() if quotation.MetricSpaceType() == 'None' else quotation.MetricSpaceFactor()
        return quoteMetricFactor
    
    @staticmethod
    def NomInQuotToQuantity(nomInQuot, insNominal, quotation):
        quoteMetricFactor = Amount.QuoteMetricFactor(quotation)
        return Amount.NominalToQuantity(nomInQuot / quoteMetricFactor, insNominal)

    @staticmethod
    def QuantityToNomInQuot(quantity, insNominal, quotation):
        quoteMetricFactor = Amount.QuoteMetricFactor(quotation)
        return Amount.QuantityToNominal(quantity, insNominal) * quoteMetricFactor

    @staticmethod
    def NomInQuotRelevant(instrument, dealPackage):
        if dealPackage and not dealPackage.IsDeal():
            nomInQuotRelevant = False
        else:
            nomInQuotRelevant = instrument.IsCommodityDerivative() or instrument.InsType() in ['Commodity', 'Average Future/Forward', 'Combination']
        return nomInQuotRelevant
    
    @staticmethod
    def IsCustomAmount(dealPackage):
        isCustom = False
        if dealPackage and not dealPackage.IsDeal():
            amountInfo = dealPackage.GetAttribute('salesTradingInteraction').At('amountInfo')
            if amountInfo:
                dpAmount = dealPackage.GetAttribute(amountInfo['amountAttr'])
                if not dpAmount:
                    isCustom = True
        return isCustom


'''********************************************************************
* Trading Interface
********************************************************************''' 
class TradingInterface(object):    
    @staticmethod
    def Get(instrument):
        tradingInterface = None
        interfaces = acm.Trading().TradingInterfaces(instrument.Originator())
        marketPlace = acm.FMarketPlace[OrderBookCreation.DefaultMarket(instrument)]
        marketSegmentId = OrderBookCreation.MarketSegmentId(instrument)
        for interface in interfaces:
            if interface.IsAvailable():
                if interface.MarketPlace() == marketPlace:
                    tradingInterface = interface
                    if interface.OrderBookList() and interface.OrderBookList().Id() == marketSegmentId:
                        #Any interface on the market place is ok - but the defaultMarketSegmentId is prioritized
                        break
        if tradingInterface:
            tradingInterface.Subscribe('RealTime')
        return tradingInterface

    @staticmethod
    def TickValue(value, increment, tickCB, instrument, tradingInterface, *args):
        def Sign(increment):
            return 1 if increment else -1
        def Value(value):
            return 0 if (value is None) else value
        return Value(value) + (Sign(increment) * tickCB(instrument, tradingInterface, value, *args))
    
    @staticmethod
    def CreateOrderBookCreateInfo(instrument):
        marketPlace = OrderBookCreation.DefaultMarket(instrument)
        marketSegmentId = OrderBookCreation.MarketSegmentId(instrument)
        tickSizeId = OrderBookCreation.TickSizeId(instrument)
        quotation = OrderBookCreation.Quotation(instrument, None)
        createInfo = acm.Trading.CreateOrderBookCreateInfo(instrument, marketPlace)
        if quotation != instrument.Quotation():
            createInfo.AdmQuotation(quotation)
        createInfo.InsType('Stock')
        createInfo.MarketInstrumentId(instrument.Name())
        createInfo.ListId(marketSegmentId)
        createInfo.TickSizeList(tickSizeId)
        createInfo.RoundLot(1)
        createInfo.ShortName(instrument.Name())
        createInfo.LongName(instrument.Name() )
        return createInfo

'''********************************************************************
* Exception Accumulator
********************************************************************'''        
class ExceptionAccumulator(object):
    def __init__(self):
        self._exceptionStr = ''
    def __NewLine(self):
        if len(self._exceptionStr):
            self._exceptionStr = self._exceptionStr + '\n'
    def __AppendException(self, exceptionStr):
        self._exceptionStr = self._exceptionStr + exceptionStr
    def __ResetAccumulator(self):
        self._exceptionStr = ''    
    def AddException(self, exceptionStr):
        self.__NewLine()
        self.__AppendException(FormatException(exceptionStr))
    def AccumulatedExceptionStr(self):
        exceptionStr = self._exceptionStr
        self.__ResetAccumulator()
        return exceptionStr

'''********************************************************************
* RFQCalcAPI
********************************************************************'''      
class RFQCalcAPI(object):
    def __init__(self):
        self._calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), acm.FQuoteRequestPriceSheet)

    def __FormatTime(self, time):
        return Time.secondsSpanFormatter.Format(time)

    def __GetCalcValue(self, obj, columnId, formatter = None, default = None):
        val = default
        if obj:
            val = self._calcSpace.CalculateValue(obj, columnId)
        return formatter(val) if formatter else val
    
    def __GetColumnId(self, baseId, quoteRequestInfo, direction):
        direction = Direction.FromQuoteRequestInfo(quoteRequestInfo) if quoteRequestInfo and not direction else str(direction)
        return baseId + ' ' + direction

    def GetTimeLeft(self, quoteRequestInfo, direction = None):
        columnId = self.__GetColumnId('Quote Timeout', quoteRequestInfo, direction)
        return self.__GetCalcValue(quoteRequestInfo, columnId, self.__FormatTime, '')

    def GetStatus(self, quoteRequestInfo, direction = None):
        columnId = self.__GetColumnId('Quote Status', quoteRequestInfo, direction)
        return self.__GetCalcValue(quoteRequestInfo, columnId, None, '')

    def GetPrice(self, quoteRequestInfo, direction = None):
        columnId = self.__GetColumnId('Quote Price', quoteRequestInfo, direction)
        return self.__GetCalcValue(quoteRequestInfo, columnId)

    def GetQuantity(self, quoteRequestInfo, direction = None):
        columnId = self.__GetColumnId('Quote Quantity', quoteRequestInfo, direction)
        return self.__GetCalcValue(quoteRequestInfo, columnId)


'''********************************************************************
* Open
********************************************************************'''      
class Open(object):
    @staticmethod
    def OpenButtonVisible(dp, ins, requestSent=True, creatingNewInsOrIp=False):
        visible = False
        if requestSent or not creatingNewInsOrIp:
            isOnDp = dp and not dp.IsDeal()
            visible = dp and dp.InstrumentPackage().Originator().StorageId() > 0 or \
                   not isOnDp and ins and ins.Originator().StorageId() > 0
        return visible
               
    @staticmethod
    def ObjectsToOpen(dp, trade, taggedTrades, creatingNew, isSales):
        instrument = trade.Instrument().Originator() if trade and trade.Instrument().Originator().StorageId() > 0 else None
        trade = trade.Originator() if trade and trade.Originator().StorageId() > 0 and not creatingNew else None
        ip = dp.InstrumentPackage().Originator() if dp and dp.InstrumentPackage().Originator().StorageId() > 0 else None
        dp = dp.Originator() if dp and dp.Originator().StorageId() > 0 and not creatingNew else None
        if taggedTrades:
            if ip:
                dp = taggedTrades.First().DealPackage()
            else:
                trade = taggedTrades.First() if taggedTrades.Size() == 1 else taggedTrades
        
        if not (dp or ip):
            customPane = 'salesCustomPane' if isSales else 'tradingCustomPane'
            tradeOrIns = trade if trade else instrument
            if tradeOrIns:
                if acm.DealPackage.SalesTradingInteractionSetting(tradeOrIns, customPane):
                    dp = acm.Deal.WrapAsDecorator(tradeOrIns, None, "")
                    ip = dp.InstrumentPackage()
                    
        dpOrTrades = UnDecorate(dp) if dp else UnDecorate(trade)
        ipOrIns = UnDecorate(ip) if ip else UnDecorate(instrument)
        return dpOrTrades, ipOrIns
                        
    @staticmethod
    def FindTaggedTrades(addInfoName, addInfoValue):
        trades = acm.FArray()
        if addInfoValue:
            spec = acm.FAdditionalInfoSpec[addInfoName]
            addinfs = acm.FAdditionalInfo.Select('addInf = %s and fieldValue = %s' % (spec.Oid(), addInfoValue))
            trades.AddAll([acm.FTrade[addinf.Recaddr()] for addinf in addinfs])
        return trades
    
    @staticmethod
    def LaunchApp(content, startAppCb, dialogCb):
        if content.IsKindOf(acm.FArray):
            if dialogCb:
                dialogCb(content)
        else:        
            if startAppCb:
                package = content if content.IsKindOf(acm.FDealPackage) or content.IsKindOf(acm.FInstrumentPackage) else None
                insOrTrade = content if content.IsKindOf(acm.FInstrument) or content.IsKindOf(acm.FTrade) else None        
                if package:
                    startAppCb('Deal Package', package)
                elif insOrTrade:        
                    startAppCb('Instrument Definition', insOrTrade)
            
    @staticmethod
    def OpenEntity(dp, trade, creatingNew, addInfoName, addInfoValue, startAppCb, dialogCb, isSales=True):
        toReturn = None
        taggedTrades = Open.FindTaggedTrades(addInfoName, addInfoValue)
        dpOrTrades, ipOrIns = Open.ObjectsToOpen(dp, trade, taggedTrades, creatingNew, isSales)
        if dpOrTrades:
            Open.LaunchApp(dpOrTrades, startAppCb, dialogCb)
            toReturn = dpOrTrades
        elif ipOrIns:
            Open.LaunchApp(ipOrIns, startAppCb, dialogCb)
            toReturn = ipOrIns
        return toReturn
                

'''********************************************************************
* QuoteRequest
********************************************************************'''  
class QuoteRequest(object):
    @staticmethod
    def GetQuoteRequestName(qr):
        salesTradingInfo = SalesTradingInfo(qr)
        return salesTradingInfo.Name()
        
    @staticmethod
    def FindQuoteRequestsFromFromList(requests, role):
        try:
            def sortCB(obj, *args):
                return obj.Role() == role
        
            quoteRequests = requests.Filter(sortCB)
            return quoteRequests
        except Exception as e:
            print ('FindQuoteRequestFromFromList failed', e)
    
    @staticmethod
    def GetCustomerQuoteRequestFromQuoteRequest(quoteRequest):
        customerQuoteRequest = quoteRequest
        if quoteRequest and quoteRequest.Role() == 'Trading':
            customerRequest = quoteRequest.CustomerRequest()
            requests = acm.Trading().FindRelatedQuoteRequests(customerRequest)
            salesRequests = QuoteRequest.FindQuoteRequestsFromFromList(requests, 'Sales')
            customerQuoteRequest = salesRequests.First() if salesRequests.Size() else None
        return customerQuoteRequest
    
    @staticmethod
    def QueryQuoteRequests(customerRequest, onQueryCompleteCb):
        marketPlace = customerRequest.MarketPlace()
        customerRequestId = customerRequest.Id()
        filter = acm.FQuoteRequestFilter()
        filter.Latest(True)
        query = acm.Trading().CreateQuoteRequestQuery(marketPlace, filter)
        query.CustomerRequestId(customerRequestId)
        query.Send().ContinueWith(onQueryCompleteCb)

TEMPLATES = [str(cid.Value().Caption()) for cid in acm.GetDefaultContext().GetAllExtensions('FCustomInstrumentDefinition') if str(cid.Value().InstantiatedAs()) == "Template"]
DEALS = acm.DealPackageDefinition().GetAllDisplayNames('Deal')

'''********************************************************************
* Misc
********************************************************************''' 
class Misc(object):
    @staticmethod
    def FindInvestmentDeciderChoices(client):
        investmentDeciderDict = acm.FOrderedDictionary()
        investmentDeciderDict.AtPut('', None)
        if client:
            investmentDeciders = client.Contacts()                   
            for investmentDecider in investmentDeciders:
                item = ''
                item += investmentDecider.Name()
                investmentDeciderDict.AtPut(item, investmentDecider)
        return investmentDeciderDict

    @staticmethod
    def GetInvestmentDeciderObject(client, investmentDeciderStringKey):
        investmentDecider = None
        if client:
            for contact in client.Contacts():
                if contact.StringKey() == investmentDeciderStringKey:
                    investmentDecider = contact
                    break
        return investmentDecider

    @staticmethod
    def GetTradeFromDealPackage(dp):    
        trade = None
        if dp:
            trade = dp.LeadTrade()
            if not trade:
                trade = dp.Trades().First()
            if not trade:
                raise DealPackageException('Cannot perform action on an empty Deal Package')
        return trade
    
    @staticmethod
    def CreateNewInstrumentFromGeneric(instrument):
        try:
            if instrument.Generic():
                instrument = acm.DealCapturing().CreateNewInstrumentFromGenericInstrument(instrument)
                instrument.InitializeUniqueIdentifiers()
        except Exception as e:
            print ('Create Instrument from generic Instrument failed: ', e)
        return instrument

    @staticmethod
    def CreatePackageFromDefinitionName(definitionName, gui):
        dealPackage = None
        if definitionName in DEALS or definitionName in TEMPLATES:
            dealPackage = acm.Deal().NewAsDecorator(definitionName, gui)
        else:
            dealPackage = acm.DealPackage().NewAsDecorator(definitionName, gui)
        return dealPackage
    
    @staticmethod
    def FindDealPackageFromImObject(imObject, gui, isSales=True, wrapDeal=True):
        salesTradingInfo = SalesTradingInfo(imObject)
        objectToQuote = salesTradingInfo.ObjectToQuote()
        dealPackage = Misc.FindDealPackage(objectToQuote, gui, isSales, wrapDeal)
        if objectToQuote.IsKindOf('FInstrumentPackage') or objectToQuote.IsKindOf('FInstrument'):
            amountInfo = acm.DealPackage.SalesTradingInteractionSetting(dealPackage, 'amountInfo')
            if amountInfo:
                dealPackage.SetAttribute(amountInfo['amountAttr'], imObject.Quantity())
        return dealPackage
    
    @staticmethod
    def FindTradeFromImObject(imObject, gui):
        salesTradingInfo = SalesTradingInfo(imObject)
        insOrTrade = salesTradingInfo.ObjectToQuote()
        trade = Misc.FindTrade(insOrTrade, gui)
        if insOrTrade.IsKindOf('FInstrument'):
            trade.Quantity(imObject.Quantity())
        return trade
    
    @staticmethod
    def FindOrderHandler(content):
        orderHandler = content if hasattr(content, 'IsKindOf') and content.IsKindOf(acm.FOrderHandler) else None
        tradingInterface = None
        salesOrder = content if content and hasattr(content, 'IsKindOf') and content.IsKindOf(acm.FSalesOrder) else None
        if salesOrder:
            tradingSession = acm.Trading().DefaultTradingSession()
            orderHandler = tradingSession.AttachOrder(salesOrder)
        if orderHandler:
            tradingInterface = orderHandler.TradingInterface()
        return orderHandler, tradingInterface
    
    @staticmethod
    def FindCustomerQuoteRequest(content):
        customerQuoteRequest = None
        quoteRequest = content if content and hasattr(content, 'IsKindOf') and content.IsKindOf(acm.FQuoteRequestInfo) else None
        if quoteRequest:
            customerQuoteRequest = QuoteRequest.GetCustomerQuoteRequestFromQuoteRequest(quoteRequest)
        return customerQuoteRequest
    
    @staticmethod
    def FindDealPackage(content, gui, isSales=True, wrapDeal=True):
        dealPackage = None
        insOrTrade = None
        if isinstance(content, basestring):
            dealPackage = Misc.CreatePackageFromDefinitionName(content, gui)
        elif hasattr(content, 'IsKindOf'):
            insOrTrade = content if content.IsKindOf(acm.FInstrument) or content.IsKindOf(acm.FTrade) else None
            if content.IsKindOf(acm.FDealPackage):
                dealPackage = acm.FBusinessLogicDecorator.WrapObject(content, gui).Edit()
            elif content.IsKindOf(acm.FInstrumentPackage):
                dealPackage = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(content, gui)
            if not dealPackage and insOrTrade:
                if insOrTrade.IsKindOf(acm.FInstrument):
                    insOrTrade = Misc.CreateNewInstrumentFromGeneric(insOrTrade)
                elif insOrTrade.IsKindOf(acm.FTrade):
                    dealPackage = insOrTrade.DealPackage()
                    if dealPackage:
                        dealPackage = acm.FBusinessLogicDecorator.WrapObject(dealPackage, gui).Edit()
                if not dealPackage and wrapDeal and acm.DealPackage.SalesTradingInteractionSetting(UnDecorate(insOrTrade), 'salesCustomPane' if isSales else 'tradingCustomPane'):
                    dealPackage = acm.Deal.WrapAsDecorator(insOrTrade, gui, "")
        return dealPackage
    
    @staticmethod
    def FindTrade(content, gui):
        trade = None
        if content:
            if hasattr(content, 'IsKindOf'):
                if hasattr(content, 'Trade'):
                    trade = content.Trade().Originator()
                if not trade or trade.StorageId() < 0:
                    if hasattr(content, 'Instrument'):
                        ins = Misc.CreateNewInstrumentFromGeneric(content.Instrument())
                        trade = acm.DealCapturing().CreateNewTrade(ins.Originator())
                    elif hasattr(content, 'TradingInterface'):
                        trade = acm.DealCapturing().CreateNewTrade(content.TradingInterface().Instrument())
                if trade.StorageId() > 0:
                    trade = trade.StorageImage()
                trade = acm.FBusinessLogicDecorator.WrapObject(trade, gui)
        return trade
    
    @staticmethod
    def FindRowObjectFromInfo(invokationInfo):
        activeSheet = invokationInfo.Parameter("sheet")
        cell = activeSheet.Selection().SelectedCell()
        rowObject = cell.RowObject()
        return rowObject
    
    @staticmethod
    def SetNew(obj):
        def _RecursiveGetChildPackage(pkg, outputChildren):
            if pkg.IsKindOf(acm.FDealPackage):
                children = pkg.ChildDealPackages()
            else:
                children = pkg.ChildInstrumentPackages()
            outputChildren.extend(children)
            for child in children:
                _RecursiveGetChildPackage(child, outputChildren)

        def AllChildPackages(pkg):
            # For backwards compatibility
            children = []
            if pkg.IsKindOf(acm.FInstrumentPackage):
                if False and hasattr(pkg, 'AllChildInstrumentPackages'):
                    children = pkg.AllChildInstrumentPackages()
                else:
                    _RecursiveGetChildPackage(pkg, children)
            elif pkg.IsKindOf(acm.FDealPackage):
                if False and hasattr(pkg, 'AllChildDealPackages'):
                    children = pkg.AllChildDealPackages()
                else:
                    _RecursiveGetChildPackage(pkg, children)
            return children
        
        if hasattr(obj, 'IsKindOf') and obj.IsKindOf(acm.FDealPackage):
            if obj.StorageId() > 0:
                dp = obj.Copy()
            else:
                dp = obj
            
            toSetNew = []
            # Child Packages
            toSetNew.extend(AllChildPackages(dp.DealPackage().InstrumentPackage()))
            toSetNew.extend(AllChildPackages(dp))
            # Instruments & Trades
            toSetNew.extend(dp.Instruments().Filter( UtilInstrumentSetNew_Filter ))
            toSetNew.extend(dp.Trades())
            # Deal Package & Instrument Package
            toSetNew.extend([dp, dp.InstrumentPackage()])
            
            UtilSetNew(toSetNew)
            obj = dp
        return obj
    
    @staticmethod
    def DealPackageCustomPanes(dp, getCustomPanesFromExtValueCb, attrName):
        pane = None  
        delegatedDealPackageCustomPane = dp.GetAttribute('salesTradingInteraction').At(attrName)
        if delegatedDealPackageCustomPane and len(delegatedDealPackageCustomPane):
            try:
                pane = getCustomPanesFromExtValueCb(delegatedDealPackageCustomPane)
            except Exception as e:
                pass
        if not pane:
            if dp.IsDeal():
                pane = dp.GetAttribute('customPanes')[0]['Instrument']
        pane = pane or [{'PANE':'vbox(;fill;);'}]
        return [{'PANE':pane}]

'''********************************************************************
* Customer Price Types
********************************************************************'''  
class CustomerPriceTypes(object):
    firmStream = 1
    firm = 2

