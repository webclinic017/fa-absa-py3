import acm
 
context = acm.GetDefaultContext()
    
class CVAAttributeMapper:
    def __init__(self):
        self.m_calculationSpaceTradeSheet = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')
    
    def GetIncrementalCVA( self, trade ):
        return self.m_calculationSpaceTradeSheet.CalculateValue(trade, 'Incremental CVA')

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
    
def IsCVADesk():
    return IsOperationSpecificationAllowed('CVA Desk')
    
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
class CVAStateChartConstants:
    CHART_NAME               = 'CVA Workflow'
    class STATES:
        START                = 'Ready'
        PENDING_CVA          = 'Pending CVA'
        PENDING_CONFIRMATION = 'Pending Confirmation'
        END                  = 'Confirmed'
    
    class EVENTS:
        CVA_REQUESTED        = 'CVA Requested'
        CVA_ASSIGNED         = 'CVA Assigned'
        CVA_RE_REQUEST       = 'CVA Re-Requested'
        TRADE_CONFIRMED      = 'Trade Confirmed'

    class PAYMENT_KEYS:
        PAYMENT_TYPE              = 'CVA Transfer'
        PAYMENT_CURRENCY          = 'CVA Payment Currency'
        PAYMENT_ORIGINAL_VALUE    = 'CVA Original Value'
        PAYMENT_ORIGINAL_CURRENCY = 'CVA Original Currency'
        FX_RATE                   = 'CVA FX Rate'
        CALCULATION_TYPE          = 'CVA Calculation Type'
