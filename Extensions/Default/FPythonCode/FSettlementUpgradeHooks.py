""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeHooks.py"
import acm
import FSettlementUpgradeModuleAdmin as ModuleAdministrator
import FSettlementUpgradeVarHandler as VariableHandler
try:
    import FSettlementUpgradeParameters as UpgradeParams
except ImportError:    
    acm.Log("Error, The FSettlementUpgradeParameters file do not excist.")
    import FSettlementUpgradeParametersTemplate as UpgradeParams
import FOperationsUtils as Utils
from FSettlementEnums import RelationType
    
def GetModuleHeaderAsText():
    resString = '''import FOperationsUtils as Utils
    
'''
    return resString

def GetmostRecentlyPositionDay():
    query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    query.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', 'Coupon'))
    query.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', 'Dividend'))
    query.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', 'Redemption'))
    
    Today = acm.GetFunction('dateToday', 0)
    dayZero = '1980-01-01'
    diff = acm.FDateTime()
    for i in query.Select():
        if i.Trade() == None and i.RelationType() != RelationType.COUPON_NET and \
           i.RelationType() != RelationType.REDEMPTION_NET and i.RelationType() != RelationType.DIVIDEND_NET:
            if i.ValueDay() > dayZero:
                if i.ValueDay() < UpgradeParams.upgradeDate:
                    dayZero = i.ValueDay()
                    
    return dayZero

def GetDaysBackAsText(variableHandler):
    resString = \
'''\
def GetDaysBack(settlement):
    if settlement.Type() == 'Dividend' or settlement.Type() == 'Coupon' or settlement.Type() == 'Redemption':
        if settlement.ValueDay() <= \'%s\':
            return 0; #This is for preventing the scripts to update settlements generated before the upgrade to the new scripts. If the date is equal 1980-01-01 no dividend, coupon or redemption where found and this if statement can be removed.
    return %s

''' % (GetmostRecentlyPositionDay(), variableHandler.GetVariable('days_back'))
    return resString

    
    
def GetCurrDaysForIndex(variableHandler, currencyKey):
    daysValue = (variableHandler.GetVariable('days_curr'))[currencyKey]
    resString = \
'''settlement.Currency().Name() == '%s':
        daysForward = %s
''' % (currencyKey, daysValue)
    return resString


def GetDaysforwardAsText(variableHandler):
    firstIfStatement = 1
    resString = \
'''\
def GetDaysForward(settlement):
    daysForward = 10
'''
    for key in sorted(variableHandler.GetVariable('days_curr')):
        if firstIfStatement:
            resString += "    if "
        else:
            resString += "    elif "           
        resString += GetCurrDaysForIndex(variableHandler, key)
        firstIfStatement = 0

    resString += "    return daysForward"
    return resString


def CreateHooks():
    variableHandler = VariableHandler.VariableHandler()
    moduleAdmin = ModuleAdministrator.GetModuleAdministrator()
    hooksModule = moduleAdmin.GetModule(ModuleAdministrator.ModuleIndex.HOOKS)
    settlementHooksCode = GetModuleHeaderAsText() + GetDaysBackAsText(variableHandler) + GetDaysforwardAsText(variableHandler)
    hooksModule.Text(settlementHooksCode)
    moduleAdmin.SaveModule(ModuleAdministrator.ModuleIndex.HOOKS)
    
