import acm

def GetOrdersFromSalesOrderId(salesOrderId):
    orderFilter = acm.FOwnOrderFilter()
    query = acm.CreateFASQLQuery('FOwnOrder', 'AND')
    query.AddAttrNode('OrderId', 'EQUAL', salesOrderId)        
    orderFilter.Query(query)
    orderFilter.OrderRoles([1])
    return acm.Trading().GetOrders(orderFilter)

def OrderHandlerFromSalesOrderId(salesOrderId):
    orderHandler = None
    try:
        orders = GetOrdersFromSalesOrderId(salesOrderId)
        orderHandler = orders.AsArray().First()
    except:
        pass
    return orderHandler

def OpenSalesOrderHistoryViewer(orderHandler, shell):
    if orderHandler:
        acm.Trading().UX().OrderHistoryDialog(shell, orderHandler)
    
def OpenSalesOrderHistoryViewerFromTrade(trade, shell):
    salesOrderId = GetSalesOrderId(trade)
    orderHandler = OrderHandlerFromSalesOrderId(salesOrderId)
    OpenSalesOrderHistoryViewer(orderHandler, shell)
    
def GetSalesOrderId(trade):
    addInfos = trade.AdditionalInfo()
    return hasattr(addInfos, "SalesOrderId") and addInfos.SalesOrderId()   
