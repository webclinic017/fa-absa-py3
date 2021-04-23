
import acm
from DealPackageDevKit import DealPackageUserException
from DealPackageUtil import SalesTradingInfo, SalesTradingInteraction
from RFQUtils import Direction, MethodDirection, ExceptionAccumulator, TradingInterface, Status, Time, Validation

from SalesTradingCustomizations import OrderBookCreation

class IMInterfaceBase(object):
    def __init__(self, qrData, onSendOrderCompleteCb, onRequestQuoteCompleteCb, hooksCb):
        self._qrData = qrData
        self._onSendOrderCompleteCb = onSendOrderCompleteCb
        self._onRequestQuoteCompleteCb = onRequestQuoteCompleteCb
        self._hooksCb = hooksCb
        self._exceptionAccumulator = ExceptionAccumulator()
        
    def _QRData(self):
        return self._qrData

    def _TradingQRData(self):
        return self._qrData.TradingQuoteRequestsData()
    
    def _Instrument(self):
        return self._QRData().Instrument()
    
    def _TradingInterface(self):
        return TradingInterface.Get(self._Instrument())
                
    def _MarketPlace(self):
        tradingInterface = self._TradingInterface()
        return tradingInterface.MarketPlace() if tradingInterface else acm.FMarketPlace[OrderBookCreation.DefaultMarket(self._Instrument())]
    
    def _Hooks(self):
        return self._hooksCb()
    
    def _SetCustomDict(self, customDict):
        self._customDict = customDict
    
    def _CustomDict(self):
        return self._customDict
    
    def _GetAccountName(self):
        return self._QRData().SalesPortfolio().Name() if self._QRData().SalesPortfolio() else ''
    
    def _GetTraderName(self):
        return self._QRData().ToTrader().Name() if self._QRData().ToTrader() else ''
    
    def _OnRequestQuoteComplete(self):
        self._onRequestQuoteCompleteCb(self._QRData().CustomerQuoteRequestInfo())
    
    def _OnSendOrderComplete(self):
        self._onSendOrderCompleteCb(self._QRData().OrderHandler())

    def _QuoteRequestCounterparties(self):
        return self._Hooks()['QuoteRequestCounterparties']()[0]

    def _OnAcceptQuote(self, order, quoteRequestInfo):
        return self._Hooks()['OnAcceptQuote'](order, quoteRequestInfo)

    def _OnSendQuoteRequestAnswerToClient(self, quoteRequestInfo, quoteRequestAnswer):
        return self._Hooks()['OnSendQuoteRequestAnswerToClient'](quoteRequestInfo, quoteRequestAnswer)

    def _OnCreateQuoteRequest(self, quoteRequest, role, customDict):
        onCreateQuoteRequestCb = self._Hooks().get('OnCreateQuoteRequest')
        return onCreateQuoteRequestCb and onCreateQuoteRequestCb(quoteRequest, role, customDict)
    
    def _OnCreateOrder(self, orderHandler, customDict):
        onCreateOrderCb = self._Hooks().get('OnCreateOrder')
        return onCreateOrderCb and onCreateOrderCb(quoteRequest, customDict)
        
    def _CustomerRequestName(self):
        return self._Hooks()['SuggestCustomerRequestName'](self._QRData().Client())

    def _ExceptionAccumulator(self):
        return self._exceptionAccumulator
    
    def _SetSalesTradingInfoExtendedData(self, imObject, componentName, numberOfComponents=None):
        SalesTradingInfo.SetSalesTradingExtendedData(imObject, componentName, self._CustomDict(), numberOfComponents)

    '''********************************************************************
    * Create New Orderbook Asynch
    ********************************************************************'''    
    def _CreateOrderBookAsynch(self, instrument):
        try:
            createInfo = TradingInterface.CreateOrderBookCreateInfo(instrument)
        except Exception as e:
            self._ExceptionAccumulator().AddException('CreateOrderBookCreateInfo failed: ' + str(e))
        else:
            return createInfo.Create()
    
    def _SubscribeAsynch(self, task):
        try:
            tradingInterface = task.ResultOrThrow()
        except Exception as e:
            self._ExceptionAccumulator().AddException('Failed to create trading interface: ' + str(e))
        else:
            return tradingInterface.Subscribe('RealTime', self) 
    
    '''********************************************************************
    * Send Order
    ********************************************************************'''       
    def SetActionsOnAutoQuoteRequest(self, orderHandler):
        actions = acm.FActionOnAutoQuoteRequest()
        actions.KillOrderOnDelete(True)
        actions.KillOrderOnNonMatchingQuote(True)
        orderHandler.ActionOnAutoQuoteRequest(actions)
        
    def _CreateOrder(self, customerRequest):
        tradingSession = acm.Trading().DefaultTradingSession()
        orderHandler = tradingSession.NewOrder(self._TradingInterface())
        
        orderHandler.AutoQuoteRequest(True)
        orderHandler.CustomerRequest(customerRequest)
        orderHandler.BuyOrSell('Buy' if self._QRData().Direction() == Direction.ask else 'Sell')
        orderHandler.Price(self._QRData().PriceLimit())
        orderHandler.Quantity(self._QRData().RequestedQuantity())
        orderHandler.QuantityCondition('Min Quantity')
        orderHandler.MinimumQuantity(self._QRData().MinimumQuantity())
        orderHandler.Client(self._QRData().Client())
        orderHandler.Account(self._GetAccountName())
        orderHandler.ValidityCondition('Good till Cancelled')
        orderHandler.UserId(self._GetTraderName())
        self.SetActionsOnAutoQuoteRequest(orderHandler)
        self._SetSalesTradingInfoExtendedData(orderHandler, SalesTradingInteraction.SALES_NAME, 0)
        self._OnCreateOrder(orderHandler, self._CustomDict())
        return orderHandler
    
    def _ValidateSendOrderAsynch(self, task):
        try:
            orderHandler = task.ResultOrThrow()
        except Exception as e:
            errorStr = 'Failed to send order: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)
        else:
            self._QRData().OrderHandler(orderHandler)
            self._OnSendOrderComplete()        
    
    def _SendOrderAsynch(self, task):
        try:
            task.ResultOrThrow()
        except Exception as e:
            self._ExceptionAccumulator().AddException('Failed to subscribe to trading interface: ' + str(e))
        else:
            self._DoSendOrder() 
    
    def _EnterOrderAsynch(self, task):
        try:
            customerRequest = task.ResultOrThrow()
        except Exception as e:
            errorStr = 'Failed to enter Customer Request: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)
        else:
            orderHandler = self._CreateOrder(customerRequest)
            return acm.Trading().SendOrder(orderHandler)
    
    def _DoSendOrder(self):
        marketId = self._MarketPlace().Name()
        customerRequest = acm.Trading().CreateCustomerRequest(marketId, self._QRData().ClientName(), self._CustomerRequestName(), '')
        if self._QRData().InvestmentDecider():
            customerRequest.InvestmentDecisionMaker(self._QRData().InvestmentDecider())
        acm.Trading().SendCustomerRequest(customerRequest).ContinueWith(self._EnterOrderAsynch).ContinueWith(self._ValidateSendOrderAsynch)
    
    def _CreateNewOrderBookAndSendOrderAsynch(self):
        self._CreateOrderBookAsynch(self._Instrument()).ContinueWith(self._SubscribeAsynch).ContinueWith(self._SendOrderAsynch)
    
    def _ValidateCancelOrder(self, task):  
        try:
            task.ResultOrThrow()
        except Exception as e:
            errorStr = 'Failed to Cancel Order: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)
    
    def _CancelOrder(self):
        acm.Trading().CancelOrder(self._QRData().OrderHandler()).ContinueWith(self._ValidateCancelOrder)
    
    '''********************************************************************
    * Request Quote
    ********************************************************************'''
    def _SetSalesTradingInfoExtendedData(self, quoteRequest, componentName, numberOfComponents=None):
        SalesTradingInfo.SetSalesTradingExtendedData(quoteRequest, componentName, self._CustomDict(), numberOfComponents)
    
    def _CreateTradingQuoteRequestFromTarget(self, quotetarget, componentName):
        quoteRequest = quotetarget.CreateRequest()
        quoteRequest.TradingInterface(self._TradingQRData().TradingInterfaceAt(componentName))
        quoteRequest.BidOrAsk(self._TradingQRData().DirectionAt(componentName, self._QRData().Direction()))
        quoteRequest.Quantity(self._TradingQRData().RequestedQuantityAt(componentName, self._QRData().RequestedQuantity()))
        quoteRequest.Message(self._QRData().Comment())
        self._SetSalesTradingInfoExtendedData(quoteRequest, componentName)
        self._OnCreateQuoteRequest(quoteRequest, componentName, self._CustomDict())
        return quoteRequest

    def _CreateCustomerQuoteRequestFromTarget(self, quotetarget):
        quoteRequest = quotetarget.CreateRequest()
        quoteRequest.TradingInterface(self._TradingInterface())
        quoteRequest.BidOrAsk(self._QRData().Direction())
        quoteRequest.Client(self._QRData().Client())
        quoteRequest.Quantity(self._QRData().RequestedQuantity())   
        quoteRequest.Message(self._QRData().Comment())
        quoteRequest.ExpirationTimeSpan(self._QRData().ReplyTime())
        quoteRequest.NegotiationTimeSpan(self._QRData().NegotiationTime())
        quoteRequest.Account(self._GetAccountName())
        self._SetSalesTradingInfoExtendedData(quoteRequest, SalesTradingInteraction.SALES_NAME, self._TradingQRData().NumberOfComponents())
        self._OnCreateQuoteRequest(quoteRequest, SalesTradingInteraction.SALES_NAME, self._CustomDict())
        return quoteRequest
    
    def _ValidateEnterTradingQuoteRequestAsynch(self, componentName):
        def _Lambda(task):
            try:
                quoteRequestInfo = task.ResultOrThrow()
            except Exception as e:
                errorStr = 'Failed to enter Trading Quote Request: ' + str(e)
                self._ExceptionAccumulator().AddException(errorStr)
                return False
            else:
                self._TradingQRData().QuoteRequestInfoAt(componentName, quoteRequestInfo)
                self._QRData().ClearComment()
                return True
        return _Lambda

    def _EnterTradingQuoteRequest(self, componentName):
        toTrader = self._GetTraderName()
        counterparty = self._QuoteRequestCounterparties()
        target = acm.FLinkedQuoteRequestQuoteTarget(self._QRData().CustomerQuoteRequestInfo())
        quoteRequest = self._CreateTradingQuoteRequestFromTarget(target, componentName)
        return acm.Trading().SendQuoteRequest(quoteRequest, target, counterparty, toTrader, 'Trading')

    def _EnterTradingQuoteRequestAsynch(self, componentName):
        def _Lambda(task):
            try:
                tradingInterface = task.ResultOrThrow()
            except Exception as e:
                self._ExceptionAccumulator().AddException('Failed to subscribe to trading interface: ' + str(e))
            else:
                return self._EnterTradingQuoteRequest(componentName)
        return _Lambda 

    def _CreateNewOrderBookAndEnterTradingQuoteRequest(self, componentName):
        ins = self._TradingQRData().InstrumentAt(componentName)
        return self._CreateOrderBookAsynch(ins).ContinueWith(self._SubscribeAsynch).ContinueWith(self._EnterTradingQuoteRequestAsynch(componentName)).ContinueWith(self._ValidateEnterTradingQuoteRequestAsynch(componentName))
        
    def _EnterTradingQuoteRequestsAsynch(self, task):
        try:
            customerQuoteRequestInfo = task.ResultOrThrow()
        except Exception as e:
            errorStr = 'Failed to enter Customer Quote Request: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)
        else:
            self._QRData().CustomerQuoteRequestInfo(customerQuoteRequestInfo)
            components = self._TradingQRData().Components()
            for componentName in components.Keys():
                if not self._TradingQRData().TradingInterfaceAt(componentName):
                    self._CreateNewOrderBookAndEnterTradingQuoteRequest(componentName)
                else:
                    self._EnterTradingQuoteRequest(componentName).ContinueWith(self._ValidateEnterTradingQuoteRequestAsynch(componentName))
            self._OnRequestQuoteComplete()
        
    def _EnterCustomerQuoteRequestAsynch(self, task):
        try:
            customerRequest = task.ResultOrThrow()
        except Exception as e:
            errorStr = 'Failed to enter Customer Request: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)
        else:
            quotetarget = acm.FCustomerRequestQuoteTarget(customerRequest)
            quoteRequest = self._CreateCustomerQuoteRequestFromTarget(quotetarget)
            counterparty = self._QuoteRequestCounterparties()
            return acm.Trading().SendQuoteRequest(quoteRequest, quotetarget, counterparty, None, 'Sales')

    def _DoRequestQuote(self):
        marketId = self._MarketPlace().Name()
        customerRequest = acm.Trading().CreateCustomerRequest(marketId, self._QRData().ClientName(), self._CustomerRequestName(), '')
        if self._QRData().InvestmentDecider():
            customerRequest.InvestmentDecisionMaker(self._QRData().InvestmentDecider())
        acm.Trading().SendCustomerRequest(customerRequest).ContinueWith(self._EnterCustomerQuoteRequestAsynch).ContinueWith(self._EnterTradingQuoteRequestsAsynch)

    def _RequestQuoteAsynch(self, task):
        try:
            task.ResultOrThrow()
        except Exception as e:
            self._ExceptionAccumulator().AddException('Failed to subscribe to trading interface: ' + str(e))
        else:
            self._DoRequestQuote() 
            
    def _CreateNewOrderBookAndRequestQuoteAsynch(self):
        self._CreateOrderBookAsynch(self._Instrument()).ContinueWith(self._SubscribeAsynch).ContinueWith(self._RequestQuoteAsynch)

    '''********************************************************************
    * Send quote request answer
    ********************************************************************'''
    def _SendQuoteRequestAnswer(self, bidPrice, bidQuantity, askPrice, askQuantity, wireTime):
        quoteRequestInfo = self._QRData().CustomerQuoteRequestInfo()
        stream = self._QRData().CustomerPriceTypeAsStream() and self._QRData().AllowFirmStreamToCustomer()
        direction = 'Both' if self._QRData().Direction() == Direction.twoWay else self._QRData().Direction()
        quoteRequestAnswer = acm.Trading().CreateQuoteRequestAnswer(quoteRequestInfo, direction, bidPrice, bidQuantity, askPrice, askQuantity)
        wireTime = Time.DateTimeToMilliseconds(wireTime)
        quoteRequestAnswer.WireTime(wireTime)
        quoteRequestAnswer.Stream(stream)
        quoteRequestAnswer.Account(self._GetAccountName())
        self._OnSendQuoteRequestAnswerToClient(quoteRequestInfo, quoteRequestAnswer)
        acm.Trading().SendQuoteRequestAnswer(quoteRequestInfo, quoteRequestAnswer).ContinueWith(self._SendQuoteRequestAnswerAsynch)
        
    def _SendQuoteRequestAnswerAsynch(self, task):
        try:
            task.ResultOrThrow()
            return True
        except Exception as e:
            errorStr = 'Failed to Send Quote Request Answer: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)
    
    '''********************************************************************
    * Accept/Counter Quote Request
    ********************************************************************'''
    def _BuyOrSellFromDirection(self, direction):
        return 'Sell' if direction == 'Bid' else 'Buy'
    
    def _SendOrderResultAsynch(self, task):
        try:
            task.ResultOrThrow()
            return True
        except Exception as e:
            errorStr = 'Failed to Send Order: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)

    def _CreateAndSendOrder(self, quoteRequestInfo, buyOrSell, price, quantity, account):
        session = acm.Trading().DefaultTradingSession()
        order = session.CreateQuoteRequestOrder(quoteRequestInfo, False)
        order.BuyOrSell(buyOrSell)
        order.Price(price)
        order.Quantity(quantity)
        order.Account(account)
        self._OnAcceptQuote(order, quoteRequestInfo)
        return acm.Trading().SendOrder(order)
    
    def _SendAnswerIfNecessary(self, task):
        try:
            task.ResultOrThrow()
        except Exception as e:
            errorStr = 'Failed to Send Order: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)
        if self._QRData().QuoteRequestStatus('Sales') in [Status.subject, Status.subjAccept]:
            quantity = self._QRData().CustomerQuoteRequestInfo().Quantity()
            allInPrice = self._QRData().AllInPrice(direction)
            self._SendQuoteRequestAnswer(allInPrice, quantity, allInPrice, quantity, -1)
    
    def _AcceptQuoteRequest(self, quoteRequestInfo, direction, quantity, price):
        buyOrSell = self._BuyOrSellFromDirection(direction)
        account = self._GetAccountName()
        return self._CreateAndSendOrder(quoteRequestInfo, buyOrSell, price, quantity, account)

    def _AcceptCustomerQuoteRequest(self, direction):
        allInPrice = self._QRData().AllInPrice(direction)
        quantity = self._QRData().TraderQuantity(direction)
        self._AcceptQuoteRequest(self._QRData().CustomerQuoteRequestInfo(), direction, quantity, allInPrice).ContinueWith(self._SendAnswerIfNecessary)

    def _AcceptTradingQuoteRequests(self, mainDirection):
        components = self._TradingQRData().Components()
        for componentName in components.Keys():
            quoteRequestInfo = self._TradingQRData().QuoteRequestInfoAt(componentName)
            direction = self._TradingQRData().DirectionAt(componentName, mainDirection)
            traderPrice = self._TradingQRData().TraderPriceAt(componentName, mainDirection)
            quantity = self._TradingQRData().TraderQuantityAt(componentName, mainDirection)
            self._AcceptQuoteRequest(quoteRequestInfo, direction, quantity, traderPrice).ContinueWith(self._SendOrderResultAsynch)

    def _CounterOrder(self, quoteRequestInfo, direction, newPrice, newQuantity):
        buyOrSell = self._BuyOrSellFromDirection(direction)
        price = newPrice
        quantity = newQuantity
        account = self._GetAccountName()
        self._CreateAndSendOrder(quoteRequestInfo, buyOrSell, price, quantity, account).ContinueWith(self._SendOrderResultAsynch)
        
    '''********************************************************************
    * Reject Quote
    ********************************************************************'''
    def _DeleteCustomerQuoteRequestAsynch(self, task):
        try:
            task.ResultOrThrow()
            return True
        except Exception as e:
            errorStr = 'Failed to Delete Trading Quote Request: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)
    
    def _RejectQuote(self):
        acm.Trading().DeleteQuoteRequest(self._QRData().CustomerQuoteRequestInfo()).ContinueWith(self._DeleteCustomerQuoteRequestAsynch)

    '''********************************************************************
    * Send message
    ********************************************************************'''
    def _DoTradingQuoteRequestSendMsg(self, task):
        try:
            task.ResultOrThrow()
            return True
        except Exception as e:
            errorStr = 'Failed to Trading Send Message: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)

    def _DoTradingQuoteRequestsSendMsg(self, task):
        try:
            task.ResultOrThrow()
            text = self._QRData().Comment()
            components = self._TradingQRData().Components()
            for componentName in components.Keys():
                tradingQuoteRequest = self._TradingQRData().QuoteRequestInfoAt(componentName)
                acm.Trading().ModifyQuoteRequest(tradingQuoteRequest, text).ContinueWith(self._DoTradingQuoteRequestSendMsg)
            self._QRData().ClearComment()
        except Exception as e:
            errorStr = 'Failed to Customer Send Message: ' + str(e)
        self._ExceptionAccumulator().AddException(errorStr)

    def _DoQuoteRequestSendMsg(self):
        text = self._QRData().Comment()
        customerQuoteRequest = self._QRData().CustomerQuoteRequestInfo()
        if customerQuoteRequest:
            acm.Trading().ModifyQuoteRequest(customerQuoteRequest, text).ContinueWith(self._DoTradingQuoteRequestsSendMsg)
    
    '''********************************************************************
    * Update Quote Request
    ********************************************************************'''
    def _ValidateUpdateQuoteRequest(self, task):
        try:
            task.ResultOrThrow()
            self._QRData().ClearComment()
            return True
        except Exception as e:
            errorStr = 'Failed to Update Quote Request: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)

    def _DoUpdateTradingQuoteRequest(self, componentName):
        text = self._QRData().Comment()
        return acm.Trading().RequestNewQuote(self._TradingQRData().QuoteRequestInfoAt(componentName), text).ContinueWith(self._ValidateUpdateQuoteRequest)

    def _DoUpdateTradingQuotes(self):
        components = self._TradingQRData().Components()
        for componentName in components.Keys():
            if self._TradingQRData().StatusAt(componentName) in [Status.noAnswer, Status.rejected]:
                try:
                    self._EnterTradingQuoteRequest(componentName).ContinueWith(self._ValidateEnterTradingQuoteRequestAsynch(componentName))
                except Exception as e:
                    errorStr = 'Failed to Enter Trading Quote Request for component ' + componentName + ': ' + str(e)
                    self._ExceptionAccumulator().AddException(errorStr)
            else:
                self._DoUpdateTradingQuoteRequest(componentName).ContinueWith(self._ValidateUpdateQuoteRequest)

    def _DoUpdateCustomerQuote(self):
        text = self._QRData().Comment()
        acm.Trading().RequestNewQuote(self._QRData().CustomerQuoteRequestInfo(), text).ContinueWith(self._ValidateUpdateQuoteRequest)
    
    def _DoUpdateQuoteRequests(self):
        self._DoUpdateTradingQuotes()
 
'''********************************************************************
* Public interface
********************************************************************'''
class IMInterface(IMInterfaceBase):    
    def SetCustomDict(self, customDict):
        self._SetCustomDict(customDict)
    
    def TradingInterface(self):
        return self._TradingInterface()
    
    def AccumulatedExceptionStr(self):
        return self._ExceptionAccumulator().AccumulatedExceptionStr()
    
    def VerifyIsConnected(self):
        Validation.IsConnected(self._MarketPlace())
    
    def SendOrder(self):
        try:
            if self._TradingInterface():
                self._DoSendOrder()
            else:
                self._CreateNewOrderBookAndSendOrderAsynch()
        except Exception as e:
            errorStr = 'Failed to Send Order: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)
        
    def RequestQuote(self):
        try:
            if self._TradingInterface():
                self._DoRequestQuote()
            else:
                self._CreateNewOrderBookAndRequestQuoteAsynch()
        except Exception as e:
            errorStr = 'Failed to Request Quote: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)

    def UpdateQuoteRequest(self):
        self._DoUpdateQuoteRequests()
        
    def UpdateCustomerQuote(self):
        self._DoUpdateCustomerQuote()

    def QuoteRequestSendMsg(self):
        self._DoQuoteRequestSendMsg()

    def Withdraw(self):
        if self._QRData().OrderHandler():
            self._CancelOrder()
        else:
            self._RejectQuote()

    def SendQuoteRequestAnswer(self, bidPrice, bidQuantity, askPrice, askQuantity, wireTime):
        self._SendQuoteRequestAnswer(bidPrice, bidQuantity, askPrice, askQuantity, wireTime)
    
    def AcceptQuote(self, direction):
        try:
            if self._QRData().CanBeConfirmed():
                bidPrice = self._QRData().AllInPrice(Direction.bid)
                bidQuantity = self._QRData().TraderQuantity(Direction.bid)
                askPrice = self._QRData().AllInPrice(Direction.ask)
                askQuantity = self._QRData().TraderQuantity(Direction.ask)
                wireTime = self._QRData().TimeLeft()
                self.SendQuoteRequestAnswer(bidPrice, bidQuantity, askPrice, askQuantity, wireTime)
            else:
                self._AcceptCustomerQuoteRequest(direction)
            
            if self._QRData().TradingQuoteRequestStatus() != Status.accepting:  
                self._AcceptTradingQuoteRequests(direction)
        except Exception as e:
            errorStr = 'Failed to Accept Quote: ' + str(e)
            self._ExceptionAccumulator().AddException(errorStr)

    def CounterOrder(self, direction, newPrice, newQuantity, allInPrice):
        self._CounterOrder(self._QRData().CustomerQuoteRequestInfo(), direction, allInPrice, newQuantity)
        self._CounterOrder(self._QRData().PrimaryTradingQuoteRequestInfo(), direction, newPrice, newQuantity)
