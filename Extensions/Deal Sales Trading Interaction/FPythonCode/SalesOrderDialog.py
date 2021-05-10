import acm
import SalesDialogUtils
from DealPackageDevKit import DealPackageException
from DealPackageAsDialog import OpenDealPackageDialogWithNoButtons
from DealPackageUtil import SalesTradingInfo
from RFQUtils import Misc

def StartSalesOrderDialog(shell, content, reOpening=True, initialAttrs=None, wrapDeal=True):
    try:        
        #label = SalesDialogUtils.GetQuoteRequestDialogLabel(dealPackage)
        label = 'Sales Order'
        SalesDialogUtils.StartSalesDialog(shell, content, reOpening, 'SalesOrder', label, initialAttrs, wrapDeal)
    except Exception as e:
        errorStr = 'Failed to Start Sales Order Dialog, ' + str(e)
        raise DealPackageException(errorStr)

def RowObjectIsOfValidType(rowObject):
    return rowObject.IsKindOf(acm.FSalesOrder) or rowObject.IsKindOf(acm.FPriceLevelRow) or rowObject.IsKindOf(acm.FPriceLevelRow) or rowObject.IsKindOf(acm.FTradeRow) or rowObject.IsKindOf(acm.FTrade) or rowObject.IsKindOf(acm.FInstrument)
    
def ButtonCreate(eii):
    try:
        cell = eii.Parameter("Cell")
        rowObject = cell.RowObject()
        return RowObjectIsOfValidType(rowObject)
        
    except Exception as e:
        errorStr = 'Failed to create Button to open Sales Order dialog, ' + str(e)
        print (errorStr) 
        
def ButtonAction(invokationInfo):
    try:
        shell = invokationInfo.Parameter('shell')
        rowObject = Misc.FindRowObjectFromInfo(invokationInfo)
        if rowObject.IsKindOf('FSalesOrder'):
            StartSalesOrderDialog(shell, rowObject)
        else:
            ins = rowObject.Instrument()
            StartSalesOrderDialog(shell, ins)
    except Exception as e:
        errorStr = 'Failed to open Sales Order dialog, ' + str(e)
        print (errorStr) 

