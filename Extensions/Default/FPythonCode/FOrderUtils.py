""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FOrderUtils.py"
"""--------------------------------------------------------------------------
MODULE
    FOrderUtils

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Module with utility functions for creating, sending and modifying orders.
-----------------------------------------------------------------------------"""

import acm
from FAssetManagementUtils import GetLogger
from FPromise import PromiseInterface, AsynchronousCall

LOGGER = GetLogger('FOrderUtils')

#----------------------------------------------------------------------------
#                        Order Creation Utils
#----------------------------------------------------------------------------

def LookupTradingInterface(instrument, market, currency=None):
    orderBookLookup = acm.FOrderBookLookupInfo()
    orderBookLookup.Instrument(instrument)
    orderBookLookup.Currency(currency or instrument.Currency())
    return acm.Trading.CreateOrderBookLookupTradingInterface(orderBookLookup, market)

def ExistingTradingInterface(instrument, market, currency=None):
    tradingInterfaces = acm.Trading.TradingInterfaces(instrument)
    for ti in tradingInterfaces:
        if ti.MarketPlace() == market and ti.Currency() == currency:
            return ti
    return None

def CreateSalesOrder(instrument, currency=None, internalMarket=None):
    tradingInterface = LookupTradingInterface(instrument, internalMarket or GetPrimaryMarket(), currency)
    return TradingSession().NewSalesOrder(tradingInterface)

def CreateMoveOrder(salesOrder, market):
    tradingInterface= ExistingTradingInterface(salesOrder.Instrument(), market, salesOrder.TradingInterface().Currency())
    return salesOrder.NewMoveOrder(tradingInterface, False)

def CreateExecutionOrder(salesOrder):
    return TradingSession().CreateExecutionOrder(salesOrder, True)

def CreateOrderProgram(orderProgramName, market):
    if not market.IsConnected():
        raise OrderCreatorError('Not connected to market {0}. The order program can\'t be created.'.format(market.Name()))
    orderProgram = TradingSession().CreateOrderProgram(market)
    orderProgram.Name(orderProgramName)
    orderProgram.UserId(acm.User().Name())
    return orderProgram

def CreateOrderProcessTypeInfo(orderProcessType, valueDate, processSubTypeName=None):
    orderProcessTypeInfo = acm.FOrderProcessTypeInfo(orderProcessType)
    orderProcessTypeInfo.ValueDate(valueDate)
    if processSubTypeName:
        processSubTypes = acm.Trading.GetProcessSubTypes()
        processSubType = processSubTypes.GetChoice(processSubTypeName)
        orderProcessTypeInfo.ProcessSubType(processSubType)
    return orderProcessTypeInfo

#----------------------------------------------------------------------------
#                  Promise Interfaces for handling orders
#----------------------------------------------------------------------------

class EnsureOrderBookStatus(PromiseInterface):
    """ Ensures that the defined orderbook status is set to True for all orders before
        calling a function. Expects a keyword argument 'orders' that contains a list of orders """
    STATUS = None

    def Init(self, *args, **kwargs):
        self._orders = kwargs['orders']
        self._statuses = {order.TradingInterface().Status() for order in self._orders}

    def Subscriptions(self):
        return self._orders

    def Fulfilled(self, *args, **kwargs):
        return all(getattr(status, self.STATUS)() for status in self._statuses)

    def ErrorMessage(self,*args, **kwargs):
        #orderBooks = {ob.Name() for ob in self._statuses if not getattr(status, self.STATUS)()}
        #return '{0} not allowed in order book(s): {1}'.format(self.STATUS, list(orderBooks))
        return 'Error'

class EnsureOrdersCanBeSent(EnsureOrderBookStatus):
    STATUS = 'EnterOrder'

class EnsureOrdersCanBeModified(EnsureOrderBookStatus):
    STATUS = 'ModifyOrder'

class EnsureOrderInSalesState(PromiseInterface):
    """ Ensures that the defined sales state is equal to the orders sales state before calling
        a function. Expects a keyword argument 'order' that contains a list of orders """
    SALES_STATE = None

    def Init(self, *args, **kwargs):
        self._order = kwargs['order']

    def Subscriptions(self):
        return [self._order]

    def Fulfilled(self, *args, **kwargs):
        return self._order.SalesState() == self.SALES_STATE

    def ErrorMessage(self, *args, **kwargs):
        return 'Sales state {0} different from {1}'.format(self._order.SalesState(), self.SALES_STATE)

class EnsureOrderStateIsCancelled(EnsureOrderInSalesState):
    SALES_STATE = 'Cancelled'

class EnsureOrdersInClient(PromiseInterface):
    """ Ensures that all orders are loaded into the client before calling a function.
        Expects two keyword arguments: 'orderIds' that contains a list of the ids of all orders that
        should be in the client, and 'orderQueryFolder' that should be populated with those ids. """

    def Init(self, *args, **kwargs):
        self._orderIds = kwargs['orderIds']
        self._orderQueryFolder = kwargs['orderQuery']

    def Subscriptions(self):
        return [self._orderQueryFolder]
    
    def ErrorMessage(self, *args, **kwargs):
        idsInQueryResult = [order.OrderId() for order in self._orderQueryFolder]
        ids = [oid not in idsInQueryResult for oid in self._orderIds]
        return 'Following orders could not be found {0}'.format(ids)
    
    def Fulfilled(self, *args, **kwargs):
        idsInQueryResult = [order.OrderId() for order in self._orderQueryFolder]
        return all(oid in idsInQueryResult for oid in self._orderIds)


#----------------------------------------------------------------------------
#                        Order Sending Utils
#----------------------------------------------------------------------------

class OrderSenderListener(object):
    
    def __init__(self, order):
        self._order = order
    
    def OnSuccess(self, order):
        LOGGER.debug('{0} ({1}) successfully sent'.format(order, order.OrderId()))

    def OnError(self, errorMessage):
        self.HandleError(self, errorMessage)
        
    @AsynchronousCall
    def HandleError(self, errorMessage):
        LOGGER.error(errorMessage)

class OrderProgramSenderListener(OrderSenderListener):
    
    def OnSuccess(self, order):
        LOGGER.info('{0} ({1}) successfully sent'.format(order.Name(), order.Id()))

class MultiOrderSenderListener(OrderSenderListener):
    
    def __init__(self, orders):
        self._orders = orders
        self._successful = []
        self._failed = []
    
    def CheckIfDone(self):
        if len(self._successful) + len(self._failed) == len(self._orders):
            if self._failed:
                self.HandleError(self, '\n'.join(self._failed))
            else:
                self.HandleSuccess()
    
    def OnSuccess(self, order):
        LOGGER.debug('{0} ({1}) successfully sent'.format(order, order.OrderId()))
        self._successful.append(order)
        self.CheckIfDone()

    def OnError(self, errorMessage):
        self._failed.append(str(errorMessage))
        self.CheckIfDone()
    
    def HandleSuccess(self):
        LOGGER.debug('All orders successfully sent')

class OrderSender(object):
    """ Handles the asynchronous sending of orders. Allows you to pass in a listener that implements 
        the methods OnSuccess(order) and OnError(orderMessage). The default listener simply prints whether 
        it was successfull or not. """
    
    def __init__(self, handler, listener=None):
        self._handler = handler
        self._listener = listener or OrderSenderListener(handler)
    
    def SendAsync(self):
        if not any(handler.IsOrderActive() for handler in self._Handlers()):
            self._SendAsync(orders=self._Handlers())
        else:
            self._ModifyAsync(orders=self._Handlers())
      
    def SendOrder(self):
        self._SendOrders()

    def HandleOrderResult(self, task):
        try:
            order = task.ResultOrThrow()
            self._listener.OnSuccess(order)
        except StandardError as e:
            self._listener.OnError(e)
    
    def _SendOrders(self):
        for handler in self._Handlers():
            acm.Trading.SendOrder(handler).ContinueWith(self.HandleOrderResult)
                
    def _Handlers(self):
        return [self._handler]
    
    def _OnSendRejected(self, *args, **kwargs):
        error = OrderSenderError(kwargs['errorMessage'])
        self._listener.OnError(error)

    def _SendAsync(self, *args, **kwargs):
        self._SendOrders()
    
    def _ModifyAsync(self, *args, **kwargs):
        self._SendOrders()
    
class MultiOrderSender(OrderSender):
    """ This class takes a list of orders and sends all of them, The default listener
        will be called when all orders have been sent to ensure that all were successfull. """

    def __init__(self, handlers, listener=None):
        self._handlers = handlers
        self._listener = listener or MultiOrderSenderListener(handlers)

    def _Handlers(self):
        return self._handlers

class OrderProgramSender(OrderSender):
    
    def SendAsync(self):
        self._SendAsync(orders=self._Handlers())    
    
    def _SendOrders(self):
        self._MonitorCommandCompletion(self._handler.SendOrderProgram())

    def _Handlers(self):
        return self._handler.GetOrders()
        
    def _MonitorCommandCompletion(self, command):
        if self._listener and command:
            if not command.IsComplete():
                command.AddDependent(self)
            else:
                self.ServerUpdate(command)
    
    def ServerUpdate(self, sender, aspect=None, param=None):
        if sender.IsKindOf(acm.FOrderCommandCompletion):
            if sender.IsComplete():
                if sender.Result() == 'Success':
                    self._listener.OnSuccess(self._handler)
                elif sender.Result() == 'Error':
                    errorMessage = ' : '.join([str(e) for e in [sender.Exception(), sender.Errors()] if e])
                    self._listener.OnError(errorMessage)
                sender.RemoveDependent(self)

#----------------------------------------------------------------------------
#                  Various Order utils
#----------------------------------------------------------------------------

def GetPrimaryMarket():
    market = acm.Trading.GetPrimaryInternalMarket(False)
    assert market, 'No primary Internal Market found'
    return market

def Connect(market):
    mktService = acm.FMarketService(market)
    if not market.IsConnected():
        if not mktService.Connect(5000):
            raise StandardError('Failed to connect to market "{0}"'.format(market.Name()))

class OrderCreatorError(StandardError):
    pass

class OrderSenderError(StandardError):
    pass

def TradingSession():
    return acm.Trading.DefaultTradingSession()

def AsOrderHandler(order):
    return TradingSession().AttachOrder(order)

def NumericOrderEnums(enum, values):
    enumType = acm.FEnumeration[enum]
    return [enumType.Enumeration(value) for value in values]

def AllChildOrders(order):
    orders = list()
    for childOrder in order.OwnOrders():
        orders.append(childOrder)
        orders.extend(AllChildOrders(childOrder))
    return orders

def GetOrderQuery(orderIds, roleIntegers=None):
    query = acm.CreateFASQLQuery('FOwnOrder', 'OR')
    for oid in orderIds:
        query.AddAttrNode('OrderId', 'EQUAL', oid)
    orderFilter = acm.FOwnOrderFilter()
    orderFilter.Query(query)
    orderFilter.OrderRoles(roleIntegers or list(range(15)))
    orderFilter.Traders([user.Name() for user in acm.FUser.Select('')])
    return acm.Trading.GetOrders(orderFilter)

def GetSalesOrderQuery(orderIds):
    return GetOrderQuery(orderIds, roleIntegers=[2,6])

def SetSalesState(order, state):
    if state == 'Accepted': acm.Trading.SetAccepted(order)
    elif state == 'Pending': acm.Trading.SetPendingExecution(order)
    elif state == 'Indication': acm.Trading.SetIndicative(order)
    elif state == 'Inactive': acm.Trading.SetInactive(order)
    elif state == 'Notified': acm.Trading.SetInExecutionNotified(order)
    elif state == 'In Exec (phone)': acm.Trading.SetInExecutionByPhone(order)
    elif state == 'Hold': acm.Trading.SetHoldExecution(order)

#----------------------------------------------------------------------------
#                  Manual Filling of orders
#----------------------------------------------------------------------------

def CreateEqualizeInfo(orderHandler, extendedData, account):
    equalizeInfo = acm.FEqualizeInfo()
    equalizeInfo.Account(account)
    equalizeInfo.ExtendedData(extendedData)
    equalizeInfo.BuyOrSellType(orderHandler.BuyOrSellType())
    equalizeInfo.BuyOrSell('Buy' if orderHandler.BuyOrSell() == 'Sell' else 'Sell')
    return equalizeInfo
    
def CreateMatchOrderSide(orderHandler, extendedData):
    matchOrderSide = orderHandler.CreateMatchOrderSide() 
    matchOrderSide.ExtendedData(extendedData)
    return matchOrderSide
    
def CreateOrderExtendedData(*args, **kwargs):
    extendedData = acm.FOrderExtendedData()
    for k, v in kwargs.iteritems():
        setattr(extendedData, k, v)
    return extendedData

def CreateMatchOrderHandler(orderHandler, quantity, price, counterparty=None, account='Manual Fill', agreementDatetime = None):
    matchOrderHandler = acm.FMatchOrderHandler(orderHandler.TradingInterface())
    matchOrderHandler.Quantity(quantity)
    matchOrderHandler.Price(price)
    matchOrderHandler.AgreementDateTime(agreementDatetime)
    
    extendedData = CreateOrderExtendedData(Preferred_Counterparty_Broker=counterparty) 
    matchOrderSide = CreateMatchOrderSide(orderHandler, extendedData)
    equalizeInfo = CreateEqualizeInfo(orderHandler, extendedData, account)
 
    if orderHandler.BuyOrSell() == 'Sell':
        matchOrderHandler.BidSide(equalizeInfo)
        matchOrderHandler.AskSide(matchOrderSide)
    else:
        matchOrderHandler.AskSide(equalizeInfo)
        matchOrderHandler.BidSide(matchOrderSide)
    
    return matchOrderHandler

