""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/HedgingCostUtils.py"
import acm
 
context = acm.GetDefaultContext()
    
class HedgingCostAttributeMapper:
    def __init__(self):
        #self.m_calculationSpaceTradeSheet = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')
        pass
    
    def GetHedgingCost( self, trade ):
        return 0.0
        #return self.m_calculationSpaceTradeSheet.CalculateValue(trade, 'Incremental HedgingCost')

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
    
def IsHedgingCostDesk():
    return IsOperationSpecificationAllowed('Hedging Cost Desk')
    
def DocumentType(instrument):
    documentType = instrument.AdditionalInfo().HedgingCostDocument()
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
class HedgingCostStateChartConstants:
    CHART_NAME               = 'HedgingCostWorkflow'
    class STATES:
        START                        = 'Ready'
        PENDING_HEDGINGCOST          = 'Pending HedgingCost'
        PENDING_CONFIRMATION         = 'Pending Confirmation'
        END                          = 'Confirmed'
    
    class EVENTS:
        HEDGINGCOST_REQUESTED        = 'HedgingCost Requested'
        HEDGINGCOST_ASSIGNED         = 'HedgingCost Assigned'
        HEDGINGCOST_RE_REQUEST       = 'HedgingCost Re-Requested'
        TRADE_CONFIRMED              = 'Trade Confirmed'

    class PAYMENT_KEYS:
        PAYMENT_TYPE              = 'Hedging Cost Transfer'
        PAYMENT_CURRENCY          = 'HedgingCost Payment Currency'
        PAYMENT_ORIGINAL_VALUE    = 'HedgingCost Original Value'
        PAYMENT_ORIGINAL_CURRENCY = 'HedgingCost Original Currency'
        FX_RATE                   = 'HedgingCost FX Rate'
        #CALCULATION_TYPE          = 'CVA Calculation Type'
