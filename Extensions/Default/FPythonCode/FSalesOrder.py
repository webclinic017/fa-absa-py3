
import acm

#------------------------------------------------------
def FormatSalesStateString(order, stateStr):

    if order.IsOrderExpired():
        stateStr = stateStr +  "EXP - "
        
    stateStr = stateStr + str(order.SalesState())
    
    modifyReq = order.ModifyOrderRequest()
    if modifyReq:
        if modifyReq.IsRejected():
            stateStr = stateStr +  " (R)"
            
    return stateStr
            
#------------------------------------------------------
def SalesStateFixOrders(order):
    
    fixReqState = order.FixRequestState()
    
    if fixReqState == "Order Rejected":
        return "Order Rejected"
        
    elif fixReqState == "Request: New Order":
    
        if order.IsOrderExpired():
            return "New Order Expired"
        else: 
            return "New Order"
    
    elif fixReqState == "Order Accepted" or fixReqState == "Request: Modify Order" or fixReqState == "Request: Cancel Order":
        
        stateStr = ""
        fixReq = order.FixRequest()
        
        if fixReq.IsPendingDontKnow():
            stateStr = "(DK) - "
            
        if fixReqState == "Request: Modify Order":
            stateStr = stateStr + "(M) - "   
            
        elif fixReqState == "Request: Cancel Order":
            stateStr = stateStr + "(C) - " 
            
        elif fixReq.IsRejected(): # HasRejectedLastRequest
            stateStr = stateStr + "(R) - "
            
        return FormatSalesStateString(order, stateStr)
        
    else:
        if order.SalesState() == "Req Cancel":
            return "Cancelled (Req Can)"
        else:
            return "Cancelled"
    
#------------------------------------------------------
def SalesStateOtherOrders(order):

    stateStr = ""
    
    if order.IsBulkOrder():
        stateStr = "BULK: "
        
    elif order.IsExecutionSalesOrder():
        stateStr = "ESO: "
        
    elif order.IsAllocationSalesOrder():
        stateStr = "ALLOC: "
    
    return FormatSalesStateString(order, stateStr)


#------------------------------------------------------    
def SalesStateString(order):

    if order.IsSalesOrder():

        if order.IsManagedFIXRequest():
            return SalesStateFixOrders(order)
            
        else:
            return SalesStateOtherOrders(order)
    else:
        return ""
