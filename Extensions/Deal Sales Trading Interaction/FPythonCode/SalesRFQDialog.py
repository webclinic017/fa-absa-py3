import acm
import SalesDialogUtils
from DealPackageDevKit import DealPackageException
from DealPackageUtil import SalesTradingInfo
from SalesTradingCustomizations import ButtonLabels
from RFQUtils import QuoteRequest, Misc
    
def StartSalesRFQDialog(shell, content, reOpening=True, initialAttrs=None, wrapDeal=True):
    try:        
        #label = SalesDialogUtils.GetQuoteRequestDialogLabel(dealPackage)
        label = 'RFQ'
        SalesDialogUtils.StartSalesDialog(shell, content, reOpening, 'QuoteRequest', label, initialAttrs, wrapDeal)
    except Exception as e:
        errorStr = 'Failed to Start Sales RFQ Dialog, ' + str(e)
        raise DealPackageException(errorStr)

def StartSalesRFQDialogFromQuoteRequest(shell, quoteRequest):
    customerQuoteRequest = Misc.FindCustomerQuoteRequest(quoteRequest)
    if customerQuoteRequest:
        StartSalesRFQDialog(shell, customerQuoteRequest)
    else: 
        QuoteRequest.QueryQuoteRequests(quoteRequest.CustomerRequest(), QuoteRequestQueryResultCompleted(shell))            

def QuoteRequestQueryResultCompleted(shell):
    def partial_wrapper(task):
        try:
            result = task.ResultOrThrow()
            requests = QuoteRequest.FindQuoteRequestsFromFromList(result, 'Sales')
            customerQuoteRequest = requests.First() if requests else None
            if customerQuoteRequest:
                StartSalesRFQDialog(shell, customerQuoteRequest)
            else:
                raise DealPackageException('Could not find Sales Quote Request')
        except Exception as e:
            print(str(e))
    return partial_wrapper

def GetQuoteRequestDialogLabel(quoteRequestPackage):
    return 'Quote Request - %s' % quoteRequestPackage.GetAttribute('rfq_topPanel_instrumentType')

'''****************************************************************************
* Buttons in Sheet
****************************************************************************'''    
def ButtonClick(invokationInfo, direction):
    try:
        shell = invokationInfo.Parameter('shell')
        instrument = Misc.FindRowObjectFromInfo(invokationInfo)

        StartSalesRFQDialog(shell, instrument, True, {'rfq_request_direction' : direction})
    except Exception as e:
        print(str(e))
        
def RowObjectIsOfValidType(rowObject):
    return rowObject.IsKindOf(acm.FPriceLevelRow) or rowObject.IsKindOf(acm.FPriceLevelRow) or rowObject.IsKindOf(acm.FTradeRow) or rowObject.IsKindOf(acm.FTrade) or rowObject.IsKindOf(acm.FInstrument)

def DisplayButton(invokationInfo):
    try:
        cell = invokationInfo.Parameter("Cell")
        rowObject = cell.RowObject()
        return RowObjectIsOfValidType(rowObject)
        
    except Exception as e:
        errorStr = 'Failed to create Button to open RFQ dialog, ' + str(e)
        print(errorStr) 
    
def EnterBuy(invokationInfo):
    ButtonClick(invokationInfo, 'Ask')

def EnterSell(invokationInfo):
    ButtonClick(invokationInfo, 'Bid')

def Enter2Way(invokationInfo):
    ButtonClick(invokationInfo, '')
    
def TwoWayQuoteRequestLabel(object):
    try:
        ins=object.Instrument()
    except:
        return 'Fail'
    return ButtonLabels.ButtonLabels(ins)[1].title()
    
def BuyQuoteRequestLabel(object):
    try:
        ins=object.Instrument()
    except:
        return 'Fail'
    return ButtonLabels.ButtonLabels(ins)[2].title()

def SellQuoteRequestLabel(object):
    try:
        ins=object.Instrument()
    except:
        return 'Fail'
    return ButtonLabels.ButtonLabels(ins)[0].title()
