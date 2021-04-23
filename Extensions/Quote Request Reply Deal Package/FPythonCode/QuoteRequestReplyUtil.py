import acm
from DealPackageUtil import SalesTradingInfo, SalesTradingInteraction, UnDecorate

'''*****************************************************************************************
* Timer formatter utilities
*****************************************************************************************'''
class TimeFormatting(object):
    secondsSpanFormatter = acm.FDateTimeSpanFormatter('SecondsSpan')

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
        hourOrMinutePeriod = TimeFormatting.ParsePeriod(inputStr)
        if hourOrMinutePeriod:
            if hourOrMinutePeriod[1] == 'h':
                seconds = hourOrMinutePeriod[0] * 3600
            elif hourOrMinutePeriod[1] == 'm':
                seconds = hourOrMinutePeriod[0] * 60
        return seconds

    @staticmethod        
    def ParseTimeSpan(inputStr):
        if inputStr and isinstance(inputStr, str):
            if TimeFormatting.ParsePeriod(inputStr):
                inputStr = str( TimeFormatting.PeriodToSeconds(inputStr) )
            else:
                splitStr = inputStr.split(':')
                if len(splitStr) == 2:
                    inputStr = str( float(splitStr[0])*60+float(splitStr[1]) )
                elif len(splitStr) == 3:
                    inputStr = str( float(splitStr[0])*3600 + float(splitStr[1])*60+float(splitStr[2]) )
        return inputStr
        
    @staticmethod
    def SecondsSpanFormat(time):
        return TimeFormatting.secondsSpanFormatter.Format(time)

'''*****************************************************************************************
* Order book utilities
*****************************************************************************************'''
class TradingInterface(object):
    @staticmethod
    def TickValue(value, increment, tickCB, instrument, tradingInterface, *args):
        def Sign(increment):
            return 1 if increment else -1
        def Value(value):
            return 0 if (value is None) else value
        return Value(value) + (Sign(increment) * tickCB(instrument, tradingInterface, value, *args))


'''*****************************************************************************************
* Get/Set Method Util
*****************************************************************************************'''
class MethodDirection(object):
    asGetMethod = '*NotUsed*'

    @staticmethod
    def AsGetMethod(val):
        return MethodDirection.asGetMethod == val

'''********************************************************************
* Quantity/Nominal
********************************************************************'''  
class Amount(object):
    @staticmethod
    def UseQuantity(instrument, dealPackage):
        return SalesTradingInteraction.UseQuantity(instrument, dealPackage)

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

'''*****************************************************************************************
* Return the tick size for Price and Nominal Fields when using the spinn button,
*   Please note that the orderBook will not be available when called from a not yet saved Instrument
*****************************************************************************************'''
class TickSizeSettings(object):
    @staticmethod
    def PriceTickSize(instrument, orderBook, currentValue):
        minimumTick = 0.01
        tick = minimumTick
        if orderBook:
            tick = orderBook.TickSizeList().TickSizeAt(currentValue)
        return minimumTick if tick < minimumTick else tick
    
    @staticmethod
    def NominalTickSize(instrument, tradingInterface, currentValue):
        roundLot = 1
        if tradingInterface:
            roundLot = tradingInterface.RoundLot()
        contractSize = instrument.ContractSize()
        return roundLot * contractSize

'''********************************************************************
* Misc
********************************************************************''' 
class Misc(object):
    @staticmethod
    def IdentifyObjectTypeFromQuoteController(quoteController):
        identifier = None
        try:
            quoteRequest = quoteController.QuoteRequestReply().QuoteRequest()
            salesTradingInfo = SalesTradingInfo(quoteRequest)
            objectToQuote = salesTradingInfo.ObjectToQuote()
            if objectToQuote:
                if objectToQuote.IsKindOf('FPackageBase'):
                    identifier = objectToQuote.DefinitionName()
                else:
                    identifier = acm.DealCapturing().CustomInstrumentDefinition(objectToQuote)
        except:
            pass
        return identifier
    
    @staticmethod
    def FindTrade(content, gui):
        trade = None
        if content:
            if hasattr(content, 'IsKindOf'):
                if hasattr(content, 'Trade'):
                    trade = content.Trade().Originator()
                if not trade or trade.StorageId() < 0:
                    if hasattr(content, 'Instrument'):
                        trade = acm.DealCapturing().CreateNewTrade(content.Originator())
                    elif hasattr(content, 'TradingInterface'):
                        trade = acm.DealCapturing().CreateNewTrade(content.TradingInterface().Instrument())
                if trade.StorageId() > 0:
                    trade = trade.StorageImage()
                trade = acm.FBusinessLogicDecorator.WrapObject(trade, gui)
        return trade
    
    @staticmethod
    def FindDealPackage(content, gui):
        dealPackage = None
        insOrTrade = None
        if isinstance(content, str):
            dealPackage = Misc.CreatePackageFromDefinitionName(content, gui)
        elif hasattr(content, 'IsKindOf'):
            insOrTrade = content if content.IsKindOf(acm.FInstrument) or content.IsKindOf(acm.FTrade) else None
            if content.IsKindOf(acm.FDealPackage):
                dealPackage = acm.FBusinessLogicDecorator.WrapObject(content, gui).Edit()
            elif content.IsKindOf(acm.FInstrumentPackage):
                dealPackage = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(content, gui)
            if not dealPackage and insOrTrade:
                if acm.DealPackage.SalesTradingInteractionSetting(UnDecorate(insOrTrade), 'tradingCustomPane'):
                    dealPackage = acm.Deal.WrapAsDecorator(insOrTrade, gui, "")
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
    def FindDealPackageFromImObject(imObject, gui):
        salesTradingInfo = SalesTradingInfo(imObject)
        objectToQuote = salesTradingInfo.ObjectToQuote()
        dealPackage = Misc.FindDealPackage(objectToQuote, gui)
        if objectToQuote.IsKindOf('FInstrumentPackage') or objectToQuote.IsKindOf('FInstrument'):
            amountInfo = acm.DealPackage.SalesTradingInteractionSetting(dealPackage, 'amountInfo')
            if amountInfo:
                dealPackage.SetAttribute(amountInfo['amountAttr'], imObject.Quantity())
        return dealPackage
    
    @staticmethod
    def FindDealPackageFromQuoteController(quoteController, gui):
        quoteRequest = quoteController.QuoteRequestReply().QuoteRequest()
        dealPackage = Misc.FindDealPackageFromImObject(quoteRequest, gui)
        return dealPackage
    
    @staticmethod
    def FindTradeFromQuoteController(quoteController, gui):
        quoteRequest = quoteController.QuoteRequestReply().QuoteRequest()
        trade = Misc.FindTradeFromImObject(quoteRequest, gui)
        return trade
    
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
    def DealPackageCustomPanes(dp, getCustomPanesFromExtValueCb):
        pane = None  
        delegatedDealPackageCustomPane = dp.GetAttribute('salesTradingInteraction').At('tradingCustomPane')
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

'''*****************************************************************************************
* Clipboard
*****************************************************************************************'''
def ToClipboard(text):
    import FClipboardUtilities
    FClipboardUtilities.SetClipboardText(text)
