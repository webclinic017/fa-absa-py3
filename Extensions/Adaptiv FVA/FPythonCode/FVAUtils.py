""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_fva/./etc/FVAUtils.py"
import acm
 
context = acm.GetDefaultContext()
    
class FVAAttributeMapper:
    def __init__(self):
        self.m_calculationSpaceTradeSheet = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')
    
    def GetIncrementalFVA( self, trade ):
        return self.m_calculationSpaceTradeSheet.CalculateValue(trade, 'Incremental FVA')

def IsOperationSpecificationAllowed(specName):
    """
    If the Operation specification does not exist, Prime defaults to allow the operation. This is not what we want, hence the FComponent.Select(...)
    """
    result = False
    where = "name='%s' and type='Operation'" % specName
    if bool(acm.FComponent.Select(where)):
        u = acm.User()
        componentType = acm.GetDomain("enum(ComponentType)")
        result = u.IsAllowed(specName, componentType.Enumeration('Operation'))
    
    return result
    
def IsSwapDesk():
    return IsOperationSpecificationAllowed('Trading Desk')
    
def IsFVADesk():
    return IsOperationSpecificationAllowed('FVA Desk')
    
def DocumentType(instrument):
    documentType = instrument.AdditionalInfo().FVADocument()
    if documentType:
        correct_list = 'Standard Document'
        correct_entry = acm.FChoiceList.Select('name="%s" and list="%s"' %(documentType, correct_list))
        return correct_entry[0]
    return documentType
    
def strTrdList(trades):

    strTrdList = ','.join([str(t.Oid()) for t in trades]) 
    return strTrdList

def convertStrToTrdList(strTrdList):
    if not strTrdList:
        return []

    trdLst = strTrdList.split(',')
    trades = []
    for id in trdLst:
        trd = acm.FTrade[id]
        if trd:
            trades.append(trd)

    return trades

# Constants
class FVAStateChartConstants:
    CHART_NAME               = 'FVAWorkflow'
    class STATES:
        START                = 'Ready'
        PENDING_FVA          = 'Pending FVA'
        PENDING_CONFIRMATION = 'Pending Confirmation'
        END                  = 'Confirmed'
    
    class EVENTS:
        FVA_REQUESTED        = 'FVA Requested'
        FVA_ASSIGNED         = 'FVA Assigned'
        FVA_RE_REQUEST       = 'FVA Re-Requested'
        TRADE_CONFIRMED      = 'Trade Confirmed'

    class PAYMENT_KEYS:
        PAYMENT_TYPE              = 'FVA Transfer'
        PAYMENT_CURRENCY          = 'FVA Payment Currency'
        PAYMENT_ORIGINAL_VALUE    = 'FVA Original Value'
        PAYMENT_ORIGINAL_CURRENCY = 'FVA Original Currency'
        FX_RATE                   = 'FVA FX Rate'
        #CALCULATION_TYPE          = 'CVA Calculation Type'
