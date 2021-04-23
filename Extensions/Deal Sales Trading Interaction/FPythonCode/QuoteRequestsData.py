
import acm
import math

from DealPackageDevKit import ReturnDomainDecorator
from DealPackageUtil import SalesTradingInteraction, UnDecorate, SalesTradingInfo
from RFQUtils import Direction, MethodDirection, Misc, PriceAndMarginConversions, QuoteRequest
from RFQUtils import Amount, RFQCalcAPI, Time, Status, CustomerPriceTypes, TradingInterface
from TradeCreationUtil import TradeCreationUtil, TradeCreation
from RFQHistoryProvider import QrQueryHandler
from SalesTradingCustomizations import RFQTimerDefaultSettings
from RFQHistoryUtil import FromRequest, QuoteRequestHistoryHelper

NO_ALL_IN_PRICE = 'NO ALL IN PRICE'
MAIN_TRADING_COMPONENT_NAME = SalesTradingInteraction.MAIN_TRADING_COMPONENT_NAME

class TradingQuoteRequestData(object):
    def __init__(self, tradeOrDealPackage):
        self._tradeOrDealPackage = tradeOrDealPackage
        self._quoteRequestInfo = None
        self._nominalFactorCalculationCb = None
        self._traderPrices = {Direction.ask : 0.0, Direction.bid : 0.0}
        self._counterEnabled = {Direction.ask : False, Direction.bid : False}
        self._counterPrices = {Direction.ask : 0.0, Direction.bid : 0.0}
        self._traderQuantities = {Direction.ask : 0.0, Direction.bid : 0.0}
        self._counterQuantities = {Direction.ask : 0.0, Direction.bid : 0.0}
        self._toTrader = None

    def QuoteRequestInfo(self, val = MethodDirection.asGetMethod, silent=False):
        if MethodDirection.AsGetMethod(val):
            return self._quoteRequestInfo
        else:
            self._Unsubscribe(self._quoteRequestInfo)
            self._quoteRequestInfo = val
            self._Subscribe(val)
            if not silent:
                acm.AsynchronousCall(self._observerCb, [val])

    def InitAllVariables(self, result):
        self.__InitTraderPrice(result)
        self.__InitCounterEnabled(result)
        
    def __InitTraderPrice(self, result):
        request = self.QuoteRequestInfo()
        if request:
            name = QuoteRequest.GetQuoteRequestName(request)
            prices = QuoteRequestHistoryHelper.LastTraderPrice(result, name)
            if prices:
                if not Direction.IsAsk(self.__Direction()):
                    self.TraderPrice(Direction.bid, prices[Direction.bid])
                if not Direction.IsBid(self.__Direction()):
                    self.TraderPrice(Direction.ask, prices[Direction.ask])

    def __InitCounterEnabled(self, result):
        if self._quoteRequestInfo:
            direction = self.__Direction()
            isCountered = self.SideIsCountered(direction)
            if not Direction.IsAsk(direction):
                self.CounterEnabled(Direction.bid, isCountered)
            if not Direction.IsBid(direction):
                self.CounterEnabled(Direction.ask, isCountered)
    
    def __Direction(self):
        return self._quoteRequestInfo.BidOrAsk()
    
    def TradingInterface(self):
        return TradingInterface.Get(self.Instrument())

    def Instrument(self):
        return self.Trade().Instrument()
    
    def Trade(self):
        if self.DealPackage():
            trade = Misc.GetTradeFromDealPackage(self._tradeOrDealPackage)
        else:
            trade = self._tradeOrDealPackage
        return trade
    
    def DealPackage(self):
        dp = None
        if hasattr(self._tradeOrDealPackage, 'GetAttributeMetaData'):
            dp = self._tradeOrDealPackage
        return dp

    def ObjectToQuote(self, quoteOnlyInstrumentPart):
        return TradeCreationUtil.ObjectToQuote(self.DealPackage(), self.Trade(), quoteOnlyInstrumentPart)

    def RegisterCbs(self, observerCb, customerPriceTypeAsFirmOrStreamCb, rfqCalcAPICb, qrQueryHandlerCb):
        self._observerCb = observerCb
        self._customerPriceTypeAsFirmOrStreamCb = customerPriceTypeAsFirmOrStreamCb
        self._rfqCalcAPICb = rfqCalcAPICb
        self.QueryHandler = qrQueryHandlerCb

    def IsActive(self):
        finalStates = [Status.cancelled, Status.passed, Status.accepted, Status.noAnswer, Status.expired]
        return self.QuoteRequestStatus() not in finalStates
    
    def IsDead(self):
        return self.QuoteRequestStatus() in [Status.rejected, Status.noAnswer, Status.cancelled]

    def CanBeAccepted(self, direction):
        canBeAccepted = False
        quoteRequestInfo = self.QuoteRequestInfo()
        if quoteRequestInfo:
            canBeAccepted = quoteRequestInfo.CanBeAccepted(direction)
        return canBeAccepted
    
    def QuoteRequestStatus(self):
        return self._FromCalcAPI().GetStatus(self.QuoteRequestInfo())

    def CustomerPriceTypeAsFirmOrStream(self):
        return self._customerPriceTypeAsFirmOrStreamCb()

    def CustomerPriceTypeAsStream(self):
        return self.CustomerPriceTypeAsFirmOrStream() == CustomerPriceTypes.firmStream

    def _FromCalcAPI(self):
        return self._rfqCalcAPICb()

    def TimeLeft(self):
        timeLeft = -1
        if self.QuoteRequestInfo():
            timeLeft = self.QuoteRequestInfo().TimeoutCountdown() if self.QuoteRequestInfo() else -1
        return timeLeft if timeLeft is not None else -1 # .TimeoutCountdown() will return None if quote request does not exist on IM (e.g. after trader reject)

    def TraderPriceIsFirmStream(self):
        answer = self.QuoteRequestInfo().Answer()
        traderPriceIsFirmStream = answer and answer.Stream()
        return traderPriceIsFirmStream

    def TraderPrice(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._traderPrices[direction]
        else:
            self._traderPrices[direction] = val

    def TraderQuantity(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            self.UpdateTraderQuantity(direction)
            return self._traderQuantities[direction]

    def TraderNominal(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.QuantityToNominal(self.TraderQuantity(direction))

    def CounterEnabled(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._counterEnabled[direction]
        else:
            self._counterEnabled[direction] = val
            if val == True:
                self.CounterNominal(direction, self.TraderNominal(direction))
                self.CounterPrice(direction, self.TraderPrice(direction))
    
    def SideIsCountered(self, direction, val = MethodDirection.asGetMethod):
        isCountered = False
        request = self.QuoteRequestInfo()
        if request and request.State() and request.BidOrAsk() in [direction, Direction.twoWay]:
            isCountered = str(request.State().GetDisplayName('FQuotePrice')) == Status.countered
        return isCountered

    def CounterPrice(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._counterPrices[direction]
        else:
            self._counterPrices[direction] = val

    def CounterQuantity(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._counterQuantities[direction]
        else:
            self._counterQuantities[direction] = val

    def CounterNominal(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.QuantityToNominal(self.CounterQuantity(direction))
        else:
            self.CounterQuantity(direction, self.NominalToQuantity(val))

    def ToTrader(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            self.UpdateToTrader()
            return self._toTrader
        else:
            self._toTrader = val

    def UpdatePrice(self, direction):
        price = self._FromCalcAPI().GetPrice(self.QuoteRequestInfo(), direction)
        if price is not None and not math.isnan(price):
            self._traderPrices[direction] = price

    def UpdateTraderQuantity(self, direction):
        if self.QuoteRequestInfo():
            quantity = self._FromCalcAPI().GetQuantity(self.QuoteRequestInfo(), direction)
            price = self._FromCalcAPI().GetPrice(self.QuoteRequestInfo(), direction)
            if price is not None and quantity != 0.0:
                self._traderQuantities[direction] = quantity
        else:
            self._traderQuantities[direction] = 0.0

    def UpdateToTrader(self):
        request = self.QuoteRequestInfo() 
        if request:
            self._toTrader = acm.FUser[request.ToBrokerId()] if request.ToBrokerId() else None

    def ResetCountered(self, direction):
        self.SideIsCountered(direction, False)
        self.CounterEnabled(direction, False)

    def _Subscribe(self, obj):
        try:
            obj.AddDependent(self)
        except:
            pass

    def _Unsubscribe(self, obj):
        try:
            obj.RemoveDependent(self)
        except:
            pass

    def EndSubscription(self):
        self._Unsubscribe(self.QuoteRequestInfo())

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        try:
            acm.AsynchronousCall(self._observerCb, [self.QuoteRequestInfo()])
        except Exception as e:
            print(('ServerUpdate failed', e))

    '''********************************************************************
    * Quantity-Nominal Conversions
    ********************************************************************'''
    def NominalFactorCalculationCb(self, val):
        self._nominalFactorCalculationCb = val

    def InstrumentNominal(self):
        instrumentNominal = 0
        try:
            nominalFactorCalculation = self._nominalFactorCalculationCb() if self._nominalFactorCalculationCb else None
            nominalFactor = nominalFactorCalculation.Value() if nominalFactorCalculation else 0
            instrumentNominal = nominalFactor * self.Instrument().ContractSize()
        except: 
            pass
        return instrumentNominal

    def NominalToQuantity(self, nominal):
        return Amount.NominalToQuantity(nominal, self.InstrumentNominal())
    
    def QuantityToNominal(self, quantity):
        return Amount.QuantityToNominal(quantity, self.InstrumentNominal())
    
    def NomInQuotToQuantity(self, nomInQuot):
        return Amount.NomInQuotToQuantity(nomInQuot, self.InstrumentNominal(), self.Instrument().Quotation())
    
    def QuantityToNomInQuot(self, quantity):
        return Amount.QuantityToNomInQuot(quantity, self.InstrumentNominal(), self.Instrument().Quotation())

  
class TradingQuoteRequestsData(object):
    def __init__(self, tradeCb, dealPackageCb):
        self._tradeCb = tradeCb
        self._dealPackageCb = dealPackageCb
        self._components = acm.FDictionary()
        self._invertDirections = acm.FDictionary()
        self._quantityFactors = acm.FDictionary()
        self._currentStatus = ''

    def MainTrade(self):
        return self._tradeCb()

    def MainInstrument(self):
        return self.MainTrade().Instrument()

    def DealPackage(self):
        return self._dealPackageCb()
    
    def STISettings(self):
        stiSettings = None
        if self.DealPackage():
            stiSettings = self.DealPackage().GetAttribute('salesTradingInteraction')
        return stiSettings
    
    def CallSettingsHook(self, hookName, *args):
        returnVal = None
        stiSettings = self.STISettings()
        if stiSettings:
            hook = getattr(stiSettings, hookName)
            returnVal = hook(*args)
        return returnVal
        
    def InitAllVariables(self, result):
        for componentName in self.Components().Keys():
            qrData = self.QRDataAt(componentName)
            qrData.InitAllVariables(result)

    def PrimaryTradingQuoteRequestInfo(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            qrInfo = self.QuoteRequestInfoAt(MAIN_TRADING_COMPONENT_NAME)
            return qrInfo
    
    def LoadMissingTradingQuoteRequestInfos(self, qrInfos):
        names = self.Components().Keys()
        for qrInfo in qrInfos:
            name = QuoteRequest.GetQuoteRequestName(qrInfo)
            if name in names:
                if not self.QuoteRequestInfoAt(name):
                    self.QuoteRequestInfoAt(name, qrInfo, True)
            else:
                raise Exception('Quote request name mismatch, "' + name + '"')

    def RegisterCbs(self, observerCb, customerPriceTypeAsFirmOrStreamCb, rfqCalcAPICb, qrQueryHandlerCb):
        for componentName in self.Components().Keys():
            qrData = self.QRDataAt(componentName)
            qrData.RegisterCbs(observerCb, customerPriceTypeAsFirmOrStreamCb, rfqCalcAPICb, qrQueryHandlerCb)

    def InitComponents(self):
        componentsInfo = self.CallSettingsHook('QuoteRequestComponents', self.MainTrade(), self.DealPackage())
        if componentsInfo is None:
            componentsInfo = SalesTradingInteraction.DefaultComponent(self.MainTrade(), self.DealPackage())
        self.CreateComponents(componentsInfo)
            
    def Components(self):
        return self._components

    def CreateComponents(self, componentsInfo):
        for componentName in componentsInfo.Keys():
            tradeOrDealPackage = componentsInfo.At(componentName)
            self.Components().AtPut(componentName, TradingQuoteRequestData(tradeOrDealPackage))
    
    def NumberOfComponents(self):
        return self.Components().Size() if self.Components() else 0

    def QRDataAt(self, componentName):
        qrData = None
        component = self.Components().At(componentName)
        if component:
            qrData = component
        return qrData

    def QuoteRequestInfoAt(self, componentName, val = MethodDirection.asGetMethod, silent=False):
        qrInfo = None
        qrData = self.QRDataAt(componentName)
        if qrData:
            qrInfo = qrData.QuoteRequestInfo(val, silent)
        return qrInfo 

    def TradeAt(self, componentName):
        trade = None
        qrData = self.QRDataAt(componentName)
        if qrData:
            trade = qrData.Trade()
        return trade 

    def InstrumentAt(self, componentName):
        ins = None
        qrData = self.QRDataAt(componentName)
        if qrData:
            ins = qrData.Instrument()
        return ins 
    
    def ObjectToQuoteAt(self, componentName, quoteOnlyInstrumentPart):
        objectToQuote = None
        qrData = self.QRDataAt(componentName)
        if qrData:
            objectToQuote = qrData.ObjectToQuote(quoteOnlyInstrumentPart)
        return objectToQuote

    def TradingInterfaceAt(self, componentName):
        tradingInterface = None
        qrData = self.QRDataAt(componentName)
        if qrData:
            tradingInterface = qrData.TradingInterface()
        return tradingInterface 

    def DirectionAt(self, componentName, mainDirection):
        direction = mainDirection
        component = self.Components().At(componentName)
        if component:
            direction = Direction.Opposite(mainDirection) if self.QuantityFactorAt(componentName) < 0.0 else mainDirection
        return direction

    def RequestedQuantityAt(self, componentName, requestedQuantity):
        quantity = 0.0
        component = self.Components().At(componentName)
        if component:
            quantity = abs(self.QuantityFactorAt(componentName)) * requestedQuantity
        return quantity
    
    def QuantityFactorAt(self, componentName):
        quantityFactor = self.CallSettingsHook('QuantityFactor', self.DealPackage(), componentName)
        if quantityFactor is None:
            quantityFactor = 1.0
        return quantityFactor

    def TraderPriceAt(self, componentName, mainDirection, val = MethodDirection.asGetMethod):
        price = 0.0
        qrData = self.QRDataAt(componentName)
        if qrData:
            price = qrData.TraderPrice(self.DirectionAt(componentName, mainDirection))
        return price

    def TraderQuantityAt(self, componentName, mainDirection, val = MethodDirection.asGetMethod):
        quantity = 0.0
        qrData = self.QRDataAt(componentName)
        if qrData:   
            quantity = qrData.TraderQuantity(self.DirectionAt(componentName, mainDirection))
        return quantity

    def TraderNominalAt(self, componentName, mainDirection, val = MethodDirection.asGetMethod):
        nominal = 0.0
        qrData = self.QRDataAt(componentName)
        if qrData: 
            nominal = qrData.TraderNominal(self.DirectionAt(componentName, mainDirection))
        return nominal

    def CounterPriceAt(self, componentName, mainDirection, val = MethodDirection.asGetMethod):
        price = 0.0
        qrData = self.QRDataAt(componentName)
        if qrData: 
            price = qrData.CounterPrice(self.DirectionAt(componentName, mainDirection), val)
        return price

    def CounterQuantityAt(self, componentName, mainDirection, val = MethodDirection.asGetMethod):
        quantity = 0.0
        qrData = self.QRDataAt(componentName)
        if qrData: 
            quantity = qrData.CounterQuantity(self.DirectionAt(componentName, mainDirection), val)
        return quantity

    def CounterNominalAt(self, componentName, mainDirection, val = MethodDirection.asGetMethod):
        nominal = 0.0
        qrData = self.QRDataAt(componentName)
        if qrData: 
            nominal = qrData.CounterNominal(self.DirectionAt(componentName, mainDirection), val)
        return nominal

    def SideIsCounteredAt(self, componentName, mainDirection, val = MethodDirection.asGetMethod):
        isCountered = False
        qrData = self.QRDataAt(componentName)
        if qrData: 
            isCountered = qrData.SideIsCountered(self.DirectionAt(componentName, mainDirection), val)
        return isCountered

    def CounterEnabledAt(self, componentName, mainDirection, val = MethodDirection.asGetMethod):
        enabled = False
        qrData = self.QRDataAt(componentName)
        if qrData: 
            enabled = qrData.CounterEnabled(self.DirectionAt(componentName, mainDirection), val)
        return enabled

    def ToTraderAt(self, componentName, val = MethodDirection.asGetMethod):
        toTrader = None
        qrData = self.QRDataAt(componentName)
        if qrData: 
            toTrader = qrData.ToTrader(val)
        return toTrader

    def StatusAt(self, componentName):
        status = ''
        qrData = self.QRDataAt(componentName)
        if qrData: 
            status = qrData.QuoteRequestStatus()
        return status
    
    def AttributeAt(self, attrName, componentName, mainDirection, val = MethodDirection.asGetMethod):
        methodName = attrName + 'At'
        method = getattr(self, methodName)
        return method(componentName, mainDirection, val)

    def TimeLeft(self):
        timeLeft = -1
        for componentName in self.Components().Keys():
            qrData = self.QRDataAt(componentName)
            componentTimeLeft = qrData.TimeLeft()
            if componentTimeLeft != -1:
                if timeLeft == -1 or componentTimeLeft < timeLeft:
                    timeLeft = componentTimeLeft
        return timeLeft

    def UpdatePrices(self, mainDirection):
        for componentName in self.Components().Keys():
            qrData = self.QRDataAt(componentName)
            qrData.UpdatePrice(self.DirectionAt(componentName, mainDirection))
    
    def AttributeDict(self, attrName, mainDirection):
        attributeDict = acm.FDictionary()
        for componentName in self.Components().Keys():
            attributeDict.AtPut(componentName, self.AttributeAt(attrName, componentName, mainDirection))
        return attributeDict
    
    def AggregatedDoubleAttribute(self, attrName, mainDirection):
        attr = 0.0
        if self.Components().Size():
            attr = self.CallSettingsHook(attrName, self.DealPackage(), self.AttributeDict(attrName, mainDirection))
            if attr is None:
                attr = self.AttributeAt(attrName, MAIN_TRADING_COMPONENT_NAME, mainDirection)
        return attr

    def AggregatedTraderPrice(self, mainDirection):
        return self.AggregatedDoubleAttribute('TraderPrice', mainDirection)

    def AggregatedTraderQuantity(self, mainDirection):
        return self.AggregatedDoubleAttribute('TraderQuantity', mainDirection)

    def AggregatedTraderNominal(self, mainDirection):
        return self.AggregatedDoubleAttribute('TraderNominal', mainDirection)

    def AggregatedCounterPrice(self, mainDirection, val = MethodDirection.asGetMethod):
        return self.CounterPriceAt(MAIN_TRADING_COMPONENT_NAME, mainDirection, val)

    def AggregatedCounterQuantity(self, mainDirection, val = MethodDirection.asGetMethod):
        return self.CounterQuantityAt(MAIN_TRADING_COMPONENT_NAME, mainDirection, val)

    def AggregatedCounterNominal(self, mainDirection, val = MethodDirection.asGetMethod):
        return self.CounterNominalAt(MAIN_TRADING_COMPONENT_NAME, mainDirection, val)

    def AggregatedSideIsCountered(self, mainDirection, val = MethodDirection.asGetMethod):
        return self.SideIsCounteredAt(MAIN_TRADING_COMPONENT_NAME, mainDirection, val)

    def AggregatedCounterEnabled(self, mainDirection, val = MethodDirection.asGetMethod):
        return self.CounterEnabledAt(MAIN_TRADING_COMPONENT_NAME, mainDirection, val)

    def AggregatedToTrader(self, val = MethodDirection.asGetMethod):
        return self.ToTraderAt(MAIN_TRADING_COMPONENT_NAME, val)

    def AggregatedStatus(self):
        if self.Components().Size():
            allEqual = True
            status = -1
            for componentName in self.Components().Keys():
                if status != -1:
                    if self.StatusAt(componentName) != status:
                        allEqual = False
                        break
                status = self.StatusAt(componentName)
            if allEqual:
                self._currentStatus = status
        return self._currentStatus

    def ResetCountered(self, mainDirection):
        for componentName in self.Components().Keys():
            qrData = self.QRDataAt(componentName)
            qrData.ResetCountered(self.DirectionAt(componentName, mainDirection))

    def IsActive(self):
        active = False
        for componentName in self.Components().Keys():
            qrData = self.QRDataAt(componentName)
            if qrData:
                active |= qrData.IsActive()
                if active:
                    break
        return active
    
    def HasDeadRequests(self):
        hasDead = False
        for componentName in self.Components().Keys():
            qrData = self.QRDataAt(componentName)
            hasDead |= qrData.IsDead()
            if hasDead:
                break
        return hasDead

    def CanBeAccepted(self, mainDirection):
        canBeAccepted = True
        for componentName in self.Components().Keys():
            qrData = self.QRDataAt(componentName)
            canBeAccepted &= qrData.CanBeAccepted(self.DirectionAt(componentName, mainDirection))
        return canBeAccepted

    def AllowFirmStreamToCustomer(self):
        allowFirmStream = False
        for componentName in self.Components().Keys():
            qrData = self.QRDataAt(componentName)
            allowFirmStream |= qrData.TraderPriceIsFirmStream()
            if allowFirmStream:
                break
        return allowFirmStream

    def EndSubscriptions(self):
        for componentName in self.Components().Keys():
            qrData = self.QRDataAt(componentName)
            qrData.EndSubscription()

class QuoteRequestsData(object):
    def __init__(self, tradeCb, dealPackageCb, observerCb, customerPriceTypeAsFirmOrStreamCb):
        self._tradeCb = tradeCb
        self._dealPackageCb = dealPackageCb
        self._observerCb = observerCb
        self._customerPriceTypeAsFirmOrStreamCb = customerPriceTypeAsFirmOrStreamCb
        self.Reset()
    
    def Reset(self):
        self._orderHandler = None
        self._customerQuoteRequestInfo = None
        self._nominalFactorCalculationCb = None
        self._allInPrices = {Direction.ask : NO_ALL_IN_PRICE, Direction.bid : NO_ALL_IN_PRICE}
        self._counterAllInPrices = {Direction.ask : 0.0, Direction.bid : 0.0}
        self._lockAllInPrice = {Direction.ask : False, Direction.bid : False}
        self._priceLimit = acm.GetFunction('marketPrice', 0)()
        self._marketPlace = None
        self._client = None
        self._direction = Direction.twoWay
        self._investmentDecider = None
        self._requestedQuantity = 0.0
        self._minimumQuantity = 0.0
        self._comment = ''
        self._marginAmounts = {Direction.ask : 0.0, Direction.bid : 0.0}
        self._counterMarginAmounts = {Direction.ask : 0.0, Direction.bid : 0.0}
        self._salesPortfolio = None
        self._replyTimeoutType = None
        self._replyExpiry = None
        self._replyTime = None
        self._negotiationTimeoutType = None
        self._negotiationExpiry = None
        self._negotiationTime = None
        self._wireTime = None

        self._rfqCalcAPI = RFQCalcAPI()
        self._tradingQRData = TradingQuoteRequestsData(self._tradeCb, self._dealPackageCb)
        self._qrQueryHandler = QrQueryHandler()

    def Trade(self):
        return self._tradeCb()

    def Instrument(self):
        return self.Trade().Instrument()
    
    def DealPackage(self):
        return self._dealPackageCb()
        
    def TradingInterface(self):
        return TradingInterface.Get(self.Instrument())

    def QrQueryHandler(self):
        return self._qrQueryHandler

    def TradingQuoteRequestsData(self):
        return self._tradingQRData
    
    def IsMultiRFQ(self):
        return len(self.TradingQuoteRequestsData().Components()) > 1
    
    def IsRFQOnDealPackage(self):
        return self.DealPackage() != None and not self.DealPackage().IsDeal()
    
    def OrderHandler(self, val = MethodDirection.asGetMethod, silent=False):
        if MethodDirection.AsGetMethod(val):
            return self._orderHandler
        else:
            self._Unsubscribe(self._orderHandler)
            self._orderHandler = val
            self._Subscribe(val)
            if not silent:
                acm.AsynchronousCall(self._observerCb, [val])

    def CustomerQuoteRequestInfo(self, val = MethodDirection.asGetMethod, silent=False):
        if MethodDirection.AsGetMethod(val):
            return self._customerQuoteRequestInfo
        else:
            self._Unsubscribe(self._customerQuoteRequestInfo)
            self._customerQuoteRequestInfo = val
            self._Subscribe(val)
            if not silent:
                acm.AsynchronousCall(self._observerCb, [val])
    
    def PrimaryTradingQuoteRequestInfo(self, val = MethodDirection.asGetMethod):
        if self.OrderHandler():
            return self.OrderHandler().QuoteRequest()
        else:
            return self.TradingQuoteRequestsData().PrimaryTradingQuoteRequestInfo(val)

    def LoadMissingCustomerQuoteRequestInfo(self, qrInfo):
        if not self.CustomerQuoteRequestInfo():
            self.CustomerQuoteRequestInfo(qrInfo, True)
    
    def LoadMissingTradingQuoteRequestInfos(self, qrInfos):
        return self.TradingQuoteRequestsData().LoadMissingTradingQuoteRequestInfos(qrInfos)
    
    def InitAllVariables(self, result):
        self.TradingQuoteRequestsData().InitAllVariables(result)
        self.__InitAllInPrices(result)
        self.__InitMarginAmounts()

    def __InitAllInPrices(self, result):
        prices = QuoteRequestHistoryHelper.LastProposedPrice(result)
        if prices:
            bidPrice = prices[Direction.bid]
            askPrice = prices[Direction.ask]
            
            if not Direction.IsAsk(self.Direction()):
                if self.SideIsCountered(self.Direction()):
                    self.CounterAllInPrice(self.Direction(), bidPrice)
                self._allInPrices[Direction.bid] = bidPrice
            if not Direction.IsBid(self.Direction()):
                if self.SideIsCountered(self.Direction()):
                    self.CounterAllInPrice(self.Direction(), askPrice)
                self._allInPrices[Direction.ask] = askPrice
                
    def __InitMarginAmounts(self):
            if not Direction.IsAsk(self.Direction()):
                if self.SideIsCountered(self.Direction()):
                    self._counterMarginAmounts[Direction.bid] = PriceAndMarginConversions.MarginAmount(self.CounterPrice(self.Direction()), self.CounterAllInPrice(self.Direction()), self.Trade(), self.DealPackage(), self.TradingInterface(), False)
                self._marginAmounts[Direction.bid] = PriceAndMarginConversions.MarginAmount(self.TraderPrice(self.Direction()), self.AllInPrice(self.Direction()), self.Trade(), self.DealPackage(), self.TradingInterface(), False)
            if not Direction.IsBid(self.Direction()):
                if self.SideIsCountered(self.Direction()):
                    self._counterMarginAmounts[Direction.ask] = PriceAndMarginConversions.MarginAmount(self.CounterPrice(self.Direction()), self.CounterAllInPrice(self.Direction()), self.Trade(), self.DealPackage(), self.TradingInterface(), True)
                self._marginAmounts[Direction.ask] = PriceAndMarginConversions.MarginAmount(self.TraderPrice(self.Direction()), self.AllInPrice(self.Direction()), self.Trade(), self.DealPackage(), self.TradingInterface(), True)

    def InitQuoteRequests(self):
        self.TradingQuoteRequestsData().InitComponents()

    def RegisterCbsOnTradingQuoteRequests(self):
        self.TradingQuoteRequestsData().RegisterCbs(self._observerCb, self._customerPriceTypeAsFirmOrStreamCb, self._FromCalcAPI, self.QrQueryHandler)
    
    def _FromCalcAPI(self):
        return self._rfqCalcAPI
    
    def CustomerPriceTypeAsFirmOrStream(self):
        return self._customerPriceTypeAsFirmOrStreamCb()

    def CustomerPriceTypeAsFirm(self):
        return self.CustomerPriceTypeAsFirmOrStream() == CustomerPriceTypes.firm

    def CustomerPriceTypeAsStream(self):
        return self.CustomerPriceTypeAsFirmOrStream() == CustomerPriceTypes.firmStream
    
    def AllowFirmStreamToCustomer(self):
        return self.TradingQuoteRequestsData().AllowFirmStreamToCustomer()

    def CustomerPriceIsFirm(self):
        return self.CustomerQuoteRequestStatus() == Status.firm

    def QuoteRequestCanBeAccepted(self, direction):
        return self.TradingQuoteRequestsData().CanBeAccepted(direction)
    
    def RequestForQuoteIsActive(self):
        finalStates = [Status.cancelled, Status.passed, Status.accepted, Status.noAnswer, Status.expired]
        return self.CustomerQuoteRequestStatus() not in finalStates or self.TradingQuoteRequestsData().IsActive()
    
    def UpdateOrWithdrawRequired(self):
        hasDeadRequests = self.TradingQuoteRequestsData().HasDeadRequests()
        customerStatus = self.CustomerQuoteRequestStatus()
        return hasDeadRequests and customerStatus in [Status.pending, Status.subject, Status.subjAccept, Status.stream]

    def _UpdateClient(self):
        client = ''
        if self.OrderHandler():
            client = self.OrderHandler().Client()
        elif self.CustomerQuoteRequestInfo():
            client = self.CustomerQuoteRequestInfo().Client()
        if client:
            self._client = acm.FParty[client]
        
    def _UpdateDirection(self):
        request = self.CustomerQuoteRequestInfo() 
        if request:
            self._direction = request.BidOrAsk()
    
    def _UpdateInvestmentDecider(self):
        request = self.CustomerQuoteRequestInfo() 
        if request and request.InvestmentDecisionMaker():
            investmentDeciderStringKey = request.InvestmentDecisionMaker()
            investmentDecider = Misc.GetInvestmentDeciderObject(self.Client(), investmentDeciderStringKey)
            self._investmentDecider = investmentDecider
    
    def _UpdateSalesPortfolio(self):
        salesPortfolio = ''
        if self.OrderHandler():
            salesPortfolio = self.OrderHandler().Account()
        elif self.CustomerQuoteRequestInfo():
            salesPortfolio = self.CustomerQuoteRequestInfo().Account()
        if salesPortfolio:
            self._salesPortfolio = acm.FPhysicalPortfolio[salesPortfolio]
        
    def _UpdateRequestedQuantity(self):
        request = self.CustomerQuoteRequestInfo() 
        if request:
            self._requestedQuantity = request.Quantity()

    def _PreserveAllInPrice(self, direction):
        return (self.CustomerPriceTypeAsFirm() and self.PriceProposedToClient()) or self.LockAllInPrice(direction)
    
    def _AllInPriceSetByUser(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._allInPrices[direction] != NO_ALL_IN_PRICE
        else:
            if val:
                self._allInPrices[direction] = self.AllInPrice(direction)
            else:
                self._allInPrices[direction] = NO_ALL_IN_PRICE
    
    def _UpdatePrices(self, direction):
        if self.Direction() in [direction, Direction.twoWay]:
            oldPrice = self.TradingQuoteRequestsData().AggregatedTraderPrice(direction)
            self.TradingQuoteRequestsData().UpdatePrices(direction)
            price = self.TradingQuoteRequestsData().AggregatedTraderPrice(direction)
            if self._AllInPriceSetByUser(direction):
                if price is not None and not math.isnan(price):
                    if not self._PreserveAllInPrice(direction):
                        oldAllInPrice = self.AllInPrice(direction)
                        self.AllInPrice(direction, price + oldAllInPrice - oldPrice)
    
    def AllInPricesSetByUser(self, val):
        self._AllInPriceSetByUser(Direction.bid, val)
        self._AllInPriceSetByUser(Direction.ask, val)
            
    def ResetCountered(self, direction):
        self.TradingQuoteRequestsData().ResetCountered(direction)

    @ReturnDomainDecorator('FMarketPlace')
    def MarketPlace(self, val = MethodDirection.asGetMethod, *args):
        if MethodDirection.AsGetMethod(val):
            return self._marketPlace
        else:
            self._marketPlace = val

    @ReturnDomainDecorator('FParty')
    def Client(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            self._UpdateClient()
            return self._client
        else:
            self._client = val
    
    def ClientName(self):
        name = ''
        if self.Client():
            name = self.Client().Name() if hasattr(self.Client(), 'Name') else self.Client()
        return name

    @ReturnDomainDecorator('string')
    def Direction(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            self._UpdateDirection()
            return self._direction
        else:
            self._direction = val

    @ReturnDomainDecorator('FPhysicalPortfolio')
    def SalesPortfolio(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            self._UpdateSalesPortfolio()
            return self._salesPortfolio
        else:
            self._salesPortfolio = val
    
    @ReturnDomainDecorator('FContact')
    def InvestmentDecider(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            self._UpdateInvestmentDecider()
            return self._investmentDecider
        else:
            self._investmentDecider = val

    @ReturnDomainDecorator('FUser')
    def ToTrader(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.TradingQuoteRequestsData().AggregatedToTrader()
        else:
            self.TradingQuoteRequestsData().AggregatedToTrader(val)

    @ReturnDomainDecorator('double')
    def RequestedNominal(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            self._UpdateRequestedQuantity()
            return self.QuantityToNominal(self.RequestedQuantity())
        else:
            self.RequestedQuantity(self.NominalToQuantity(val))
    
    @ReturnDomainDecorator('double')
    def RequestedNomInQuot(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            self._UpdateRequestedQuantity()
            return self.QuantityToNomInQuot(self.RequestedQuantity())
        else:
            self.RequestedQuantity(self.NomInQuotToQuantity(val))

    @ReturnDomainDecorator('double')
    def RequestedQuantity(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            self._UpdateRequestedQuantity()
            return self._requestedQuantity
        else:
            self._requestedQuantity = val
    
    @ReturnDomainDecorator('double')
    def MinimumNominal(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.QuantityToNominal(self.MinimumQuantity())
        else:
            self.MinimumQuantity(self.NominalToQuantity(val))
    
    @ReturnDomainDecorator('double')
    def MinimumNomInQuot(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.QuantityToNomInQuot(self.MinimumQuantity())
        else:
            self.MinimumQuantity(self.NomInQuotToQuantity(val))

    @ReturnDomainDecorator('double')
    def MinimumQuantity(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._minimumQuantity
        else:
            self._minimumQuantity = val
    
    @ReturnDomainDecorator('double')
    def TraderNominal(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.TradingQuoteRequestsData().AggregatedTraderNominal(direction)
    
    @ReturnDomainDecorator('double')
    def TraderQuantity(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.TradingQuoteRequestsData().AggregatedTraderQuantity(direction)
    
    @ReturnDomainDecorator('double')
    def CounterNominal(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.TradingQuoteRequestsData().AggregatedCounterNominal(direction)
        else:
            self.TradingQuoteRequestsData().AggregatedCounterNominal(direction, val)
    
    @ReturnDomainDecorator('double')
    def CounterQuantity(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.TradingQuoteRequestsData().AggregatedCounterQuantity(direction)
        else:
            self.TradingQuoteRequestsData().AggregatedCounterQuantity(direction, val)
    
    @ReturnDomainDecorator('string')    
    def Comment(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._comment
        else:
            self._comment = val

    def ClearComment(self):
        self._comment = ''

    @ReturnDomainDecorator('string')  
    def ReplyTimeoutType(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._replyTimeoutType
        else:
            self._replyTimeoutType = val
            if self._replyTimeoutType == RFQTimerDefaultSettings.gtc:
                self.NegotiationTimeoutType(RFQTimerDefaultSettings.gtc)
            elif self._replyTimeoutType == RFQTimerDefaultSettings.gtd:
                self.ReplyExpiry(RFQTimerDefaultSettings.defaultReplyExpiry)
            else:
                self.ReplyTime(RFQTimerDefaultSettings.defaultReplyTime)
    
    @ReturnDomainDecorator('datetime')  
    def ReplyExpiry(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._replyExpiry
        else:
            self._replyExpiry = val
    
    @ReturnDomainDecorator('double')
    def ReplyTime(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._replyTime
        else:
            self._replyTime = val
            if self.NegotiationTimeoutType() == RFQTimerDefaultSettings.timeSpan and self._replyTime > self.NegotiationTime():
                self.NegotiationTime(self._replyTime)
    
    @ReturnDomainDecorator('string')  
    def NegotiationTimeoutType(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._negotiationTimeoutType
        else:
            self._negotiationTimeoutType = val
            if self._negotiationTimeoutType == RFQTimerDefaultSettings.gtd:
                self.ReplyExpiry(Time.MinExpiry(RFQTimerDefaultSettings.defaultReplyExpiry, self.NegotiationExpiry()))
            elif self._negotiationTimeoutType == RFQTimerDefaultSettings.timeSpan:
                self.NegotiationTime(RFQTimerDefaultSettings.defaultNegotiationTime)
    
    @ReturnDomainDecorator('datetime')  
    def NegotiationExpiry(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._negotiationExpiry
        else:
            self._negotiationExpiry = val
    
    @ReturnDomainDecorator('double')
    def NegotiationTime(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._negotiationTime
        else:
            self._negotiationTime = val
            if self.ReplyTimeoutType() == RFQTimerDefaultSettings.timeSpan and \
               self.NegotiationTimeoutType() != RFQTimerDefaultSettings.gtc and \
               self._negotiationTime < self.ReplyTime():
                self.ReplyTime(self._negotiationTime)
                
    @ReturnDomainDecorator('double')
    def WireTime(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._wireTime
        else:
            self._wireTime = val
        
    @ReturnDomainDecorator('double')
    def PriceLimit(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._priceLimit
        else:
            self._priceLimit = val

    @ReturnDomainDecorator('double')
    def TraderPrice(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            self._UpdatePrices(direction)
            return self.TradingQuoteRequestsData().AggregatedTraderPrice(direction)
    
    @ReturnDomainDecorator('double')
    def AllInPrice(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            if self._AllInPriceSetByUser(direction):
                allInPrice = self._allInPrices[direction]
            else:
                allInPrice = self._FromCalcAPI().GetPrice(self.CustomerQuoteRequestInfo(), direction)
                if allInPrice is None or math.isnan(allInPrice):
                    self.TradingQuoteRequestsData().UpdatePrices(direction) # One may argue that this call should be put in the AggregatedTraderPrice-method,
                                                                            # but then it would not be possible to obtain the "oldPrice" in the _UpdatePrices-method on this class
                    allInPrice = self.TradingQuoteRequestsData().AggregatedTraderPrice(direction)
            return allInPrice
        else:
            self._allInPrices[direction] = val
        

    @ReturnDomainDecorator('double')   
    def MarginAmount(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._marginAmounts[direction]
        else:
            self._marginAmounts[direction] = val
    
    @ReturnDomainDecorator('bool')
    def LockAllInPrice(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._lockAllInPrice[direction]
        else:
            self._lockAllInPrice[direction] = val
    
    @ReturnDomainDecorator('bool')
    def CounterEnabled(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.TradingQuoteRequestsData().AggregatedCounterEnabled(direction)
        else:
            self.TradingQuoteRequestsData().AggregatedCounterEnabled(direction, val)
            if val == True:
                self.CounterAllInPrice(direction, self.AllInPrice(direction))
    
    @ReturnDomainDecorator('bool')
    def SideIsCountered(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.TradingQuoteRequestsData().AggregatedSideIsCountered(direction)
        else:
            self.TradingQuoteRequestsData().AggregatedSideIsCountered(direction, val)
    
    @ReturnDomainDecorator('double')
    def CounterPrice(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self.TradingQuoteRequestsData().AggregatedCounterPrice(direction)
        else:
            oldPrice = self.TradingQuoteRequestsData().AggregatedCounterPrice(direction)
            self.TradingQuoteRequestsData().AggregatedCounterPrice(direction, val)
            oldAllInPrice = self.CounterAllInPrice(direction)
            self.CounterAllInPrice(direction, val + oldAllInPrice - oldPrice)
    
    @ReturnDomainDecorator('double')
    def CounterAllInPrice(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._counterAllInPrices[direction]
        else:
            self._counterAllInPrices[direction] = val
            
    @ReturnDomainDecorator('double')
    def CounterMarginAmount(self, direction, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._counterMarginAmounts[direction]
        else:
            self._counterMarginAmounts[direction] = val
    
    def PriceProposedToClient(self):
        priceIsProposed = False
        result = self.QrQueryHandler().QueryResultDict()
        if result:
            prices = QuoteRequestHistoryHelper.LastProposedPrice(result)
            if prices:
                proposedBidPrice = prices[Direction.bid]
                proposedAskPrice = prices[Direction.ask]
                
                allInBid = self.CounterAllInPrice(Direction.bid) if self.SideIsCountered(Direction.bid) else self.AllInPrice(Direction.bid)
                allInAsk = self.CounterAllInPrice(Direction.ask) if self.SideIsCountered(Direction.ask) else self.AllInPrice(Direction.ask)
                
                bidProposed = abs(proposedBidPrice - allInBid) < 1e-12
                askProposed = abs(proposedAskPrice - allInAsk) < 1e-12
                    
                if self.Direction() == Direction.twoWay:
                    priceIsProposed = bidProposed and askProposed
                else:
                    priceIsProposed = bidProposed if self.Direction() == Direction.bid else askProposed
        return priceIsProposed
    
    def QuantityProposedToClient(self):
        quantityIsProposed = False
        result = self.QrQueryHandler().QueryResultDict()
        if result:
            quantities = QuoteRequestHistoryHelper.LastProposedQuantity(result)
            if quantities:
                proposedBidQuantity = quantities[Direction.bid]
                proposedAskQuantity = quantities[Direction.ask]
                
                traderBidQuantity = self.CounterQuantity(Direction.bid) if self.SideIsCountered(Direction.bid) else self.TraderQuantity(Direction.bid)
                traderAskQuantity = self.CounterQuantity(Direction.ask) if self.SideIsCountered(Direction.ask) else self.TraderQuantity(Direction.ask)
                
                bidProposed = abs(proposedBidQuantity - traderBidQuantity) < 1e-12
                askProposed = abs(proposedAskQuantity - traderAskQuantity) < 1e-12
                
                if self.Direction() == Direction.twoWay:
                    quantityIsProposed = bidProposed and askProposed
                else:
                    quantityIsProposed = bidProposed if self.Direction() == Direction.bid else askProposed
        return quantityIsProposed
    
    @ReturnDomainDecorator('bool')
    def ProposedToClient(self):
        return self.PriceProposedToClient() and self.QuantityProposedToClient()
    
    @ReturnDomainDecorator('bool')
    def IsPriceEqualOrBetterThanProposed(self):
        priceIsBetter = False
        result = self.QrQueryHandler().QueryResultDict()
        if result:
            prices = QuoteRequestHistoryHelper.LastProposedPrice(result)
            if prices:
                proposedBidPrice = prices[Direction.bid]
                proposedAskPrice = prices[Direction.ask]
                
                allInBid = self.CounterAllInPrice(Direction.bid) if self.SideIsCountered(Direction.bid) else self.AllInPrice(Direction.bid)
                allInAsk = self.CounterAllInPrice(Direction.ask) if self.SideIsCountered(Direction.ask) else self.AllInPrice(Direction.ask)
                
                bidDiff = proposedBidPrice - allInBid
                askDiff = proposedAskPrice - allInAsk
                
                if PriceAndMarginConversions.ShouldSubtractSpread(tradingInterface=None, instrument=self.Instrument(), directionIsAsk=False):
                    bidIsBetter = bidDiff < 1e-12
                else:
                    bidIsBetter = bidDiff > -1e-12
                    
                if PriceAndMarginConversions.ShouldSubtractSpread(tradingInterface=None, instrument=self.Instrument(), directionIsAsk=True):
                    askIsBetter = askDiff < 1e-12
                else:
                    askIsBetter = askDiff > -1e-12
                    
                if self.Direction() == Direction.twoWay:
                    priceIsBetter = bidIsBetter and askIsBetter
                else:
                    priceIsBetter = bidIsBetter if self.Direction() == Direction.bid else askIsBetter
        return priceIsBetter

    @ReturnDomainDecorator('bool')
    def CanBeConfirmed(self):
        return self.IsPriceEqualOrBetterThanProposed() and self.QuantityProposedToClient() and self.CustomerQuoteRequestStatus() in [Status.countered, Status.subjAccept]

    @ReturnDomainDecorator('string') 
    def QuoteRequestStatus(self, role='Trading'):
        if role == 'Trading':
            return self.TradingQuoteRequestStatus()
        else:
            return self.CustomerQuoteRequestStatus()

    @ReturnDomainDecorator('string') 
    def TradingQuoteRequestStatus(self):
        if self.OrderHandler():
            return self._FromCalcAPI().GetStatus(self.OrderHandler().QuoteRequest()) if self.OrderHandler().QuoteRequest() else ''
        else:
            return self.TradingQuoteRequestsData().AggregatedStatus()
    
    @ReturnDomainDecorator('string') 
    def CustomerQuoteRequestStatus(self):
        status = ''
        if self.CustomerQuoteRequestInfo():
            status = self._FromCalcAPI().GetStatus(self.CustomerQuoteRequestInfo())
        return status
    
    @ReturnDomainDecorator('string')
    def TimeLeftFormatted(self, *args):
        return Time.SecondsSpanFormat(self.TimeLeft())
    
    @ReturnDomainDecorator('string')
    def CustomerTimeLeftFormatted(self, *args):
        return Time.SecondsSpanFormat(self.CustomerTimeLeft())

    def TimeLeft(self, *args):
        return self.TradingQuoteRequestsData().TimeLeft()
    
    def CustomerTimeLeft(self, *args):
        return self.CustomerQuoteRequestInfo().TimeoutCountdown() if self.CustomerQuoteRequestInfo() else -1

    def _Subscribe(self, obj):
        try:
            obj.AddDependent(self)
        except:
            pass

    def _Unsubscribe(self, obj):
        try:
            obj.RemoveDependent(self)
        except:
            pass
            
    def EndSubscriptions(self):
        self._Unsubscribe(self._customerQuoteRequestInfo)
        self.TradingQuoteRequestsData().EndSubscriptions()

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        try:
            imObject = None
            if sender == self.OrderHandler():
                imObject = self.OrderHandler()
            elif sender == self.CustomerQuoteRequestInfo():
                imObject = self.CustomerQuoteRequestInfo()
            if imObject:
                acm.AsynchronousCall(self._observerCb, [imObject])
        except Exception as e:
            print(('ServerUpdate failed', e))

    '''********************************************************************
    * Quantity-Nominal Conversions
    ********************************************************************'''
    def NominalFactorCalculationCb(self, val):
        self._nominalFactorCalculationCb = val

    def InstrumentNominal(self):
        instrumentNominal = 0
        try:
            nominalFactorCalculation = self._nominalFactorCalculationCb() if self._nominalFactorCalculationCb else None
            nominalFactor = nominalFactorCalculation.Value() if nominalFactorCalculation else 0
            instrumentNominal = nominalFactor * self.Instrument().ContractSize()
        except: 
            pass
        return instrumentNominal
        
    def NominalToQuantity(self, nominal):
        return Amount.NominalToQuantity(nominal, self.InstrumentNominal())
    
    def QuantityToNominal(self, quantity):
        return Amount.QuantityToNominal(quantity, self.InstrumentNominal())
    
    def NomInQuotToQuantity(self, nomInQuot):
        return Amount.NomInQuotToQuantity(nomInQuot, self.InstrumentNominal(), self.Instrument().Quotation())
    
    def QuantityToNomInQuot(self, quantity):
        return Amount.QuantityToNomInQuot(quantity, self.InstrumentNominal(), self.Instrument().Quotation())

