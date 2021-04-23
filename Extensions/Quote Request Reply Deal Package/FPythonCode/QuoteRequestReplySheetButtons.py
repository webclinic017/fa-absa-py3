
import acm
from DealPackageDevKit import DealPackageUserException
from DealPackageAsDialog import OpenDealPackageDialogWithNoButtons

'''*********************************************************************************
* Row Object from sheet invokation info
*********************************************************************************'''
def GetRowFromInfo(invokationInfo):
    activeSheet = invokationInfo.Parameter("sheet")
    cell = activeSheet.Selection().SelectedCell()
    rowObject = cell.RowObject()
    return rowObject    
    
'''*********************************************************************************
* Assign Broker
*********************************************************************************'''
def ValidateModifyQuoteRequestBroker(task):
    try:
        task.ResultOrThrow()
        return True
    except Exception as e:
        print ('Modify Quote Request Broker Failed')

def AssignToBroker(invokationInfo):
    try:
        trader = acm.User().Name()
        quoteLevelRow = GetRowFromInfo(invokationInfo)
        quoteRequestInfo = quoteLevelRow.QuoteController().RequestForQuote().QuoteRequest()
        
        acm.Trading.ModifyQuoteRequestBroker(quoteRequestInfo, trader).ContinueWith(ValidateModifyQuoteRequestBroker)
        
    except Exception as e:
        errorStr = 'Failed to Assign Broker, ' + str(e)
        raise DealPackageUserException(errorStr)
        
def DisplayAssignToBroker(*args):
    return True
    
'''*********************************************************************************
* Unassign Broker
*********************************************************************************'''
def UnassignBroker(invokationInfo):
    try:
        quoteLevelRow = GetRowFromInfo(invokationInfo)
        quoteRequestInfo = quoteLevelRow.QuoteController().RequestForQuote().QuoteRequest()
        
        acm.Trading.ModifyQuoteRequestBroker(quoteRequestInfo, None).ContinueWith(ValidateModifyQuoteRequestBroker)
        
    except Exception as e:
        errorStr = 'Failed to Unassign Broker, ' + str(e)
        raise DealPackageUserException(errorStr)
        
def DisplayUnassignBroker(*args):
    return True
