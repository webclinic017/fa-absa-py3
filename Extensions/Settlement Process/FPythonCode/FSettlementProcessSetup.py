import acm
import SettlementProcessUtils
import CreateHighRiskStateChart
import CreateMediumRiskStateChart
import CreateLowRiskStateChart

def HasStateChart(name):
    return acm.FStateChart[name] != None



def HasChoiceList(list, name):
    eventChoiceList = acm.FChoiceList.Select("list = '%s'"%list)
    for eventChoiceListItem in eventChoiceList:
        if name == eventChoiceListItem.Name():
            return True
    return False



def AddProcessStatusChoiceList():
    states = ["No Processing Needed", "Awaiting Processing", SettlementProcessUtils.approvedLevel1, SettlementProcessUtils.approvedLevel2,\
        SettlementProcessUtils.approvalComplete, SettlementProcessUtils.rejectedLevel1, SettlementProcessUtils.rejectedLevel2, SettlementProcessUtils.rejectedLevel3, SettlementProcessUtils.error]
    if not HasChoiceList("MASTER", "SettlementProcessStatus"):
        settlementProcessStatus = acm.FChoiceList()
        settlementProcessStatus.Name("SettlementProcessStatus")
        settlementProcessStatus.List("MASTER")
        settlementProcessStatus.Commit()
    
    order = 0
    for state in states:
        if not HasChoiceList("SettlementProcessStatus", state):
            newList = acm.FChoiceList()
            newList.Name(state)
            newList.List("SettlementProcessStatus")        
            newList.SortOrder(order)
            newList.Commit()
        order += 1

def AddUpdateEventsChoiceList():
    if not HasChoiceList("MASTER", "SettlementProcessUpdateEvent"):
        updateEventsChoiceList = acm.FChoiceList()
        updateEventsChoiceList.Name("SettlementProcessUpdateEvent")
        updateEventsChoiceList.List("MASTER")
        updateEventsChoiceList.Commit()
    order = 0
    if not HasChoiceList("SettlementProcessUpdateEvent", SettlementProcessUtils.settlementUpdate):
        newList = acm.FChoiceList()
        newList.Name(SettlementProcessUtils.settlementUpdate)
        newList.List("SettlementProcessUpdateEvent")
        newList.SortOrder(order)
        newList.Commit()

def start(high, medium, low):
    Utils.Log(True, '------------------------------------------------------------')
    pr = 'Creating State Charts' 
    Utils.LogAlways(pr)
    
    if high:
        if not HasStateChart(SettlementProcessUtils.highRiskStateChart):
            Utils.LogAlways("Creating " + SettlementProcessUtils.highRiskStateChart +  " State Chart")
            CreateHighRiskStateChart.Create()
        else:
            Utils.LogAlways("The " + SettlementProcessUtils.highRiskStateChart+ " State Chart already exists")
        SettlementProcessUtils.AddOperation(SettlementProcessUtils.operationHighName)
    if medium:
        if not HasStateChart(SettlementProcessUtils.mediumRiskStateChart):
            Utils.LogAlways("Creating " + SettlementProcessUtils.mediumRiskStateChart +  " State Chart")
            
            CreateMediumRiskStateChart.Create()
        else:
            Utils.LogAlways("The " + SettlementProcessUtils.mediumRiskStateChart+ " State Chart already exists")
        SettlementProcessUtils.AddOperation(SettlementProcessUtils.operationMediumName)
    
    if low:
        if not HasStateChart(SettlementProcessUtils.lowRiskStateChart ):
            Utils.LogAlways("Creating " + SettlementProcessUtils.lowRiskStateChart +  " State Chart")
            
            CreateLowRiskStateChart.Create()
        else:
            Utils.LogAlways("The " + SettlementProcessUtils.lowRiskStateChart+ " State Chart already exists")
        SettlementProcessUtils.AddOperation(SettlementProcessUtils.operationLowName)
    AddProcessStatusChoiceList()
    AddUpdateEventsChoiceList()
    SettlementProcessUtils.AddOperation(SettlementProcessUtils.operationBypass)
    pr = 'FINISHED %s' %  time.asctime(time.localtime())
    Utils.LogAlways(pr)
    Utils.LogAlways('------------------------------------------------------------')

"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
try:
    if __name__ == "__main__":
        import sys, getopt

    import acm, time, ael
    import FOperationsUtils as Utils

    ael_variables = [('create_high_risk_state_chart', "Create " +SettlementProcessUtils.highRiskStateChart + " State Chart",
                       'bool', [False, True], True),
                    ('create_medium_risk_state_chart', "Create " +SettlementProcessUtils.mediumRiskStateChart + " State Chart",
                       'bool', [False, True], True),
                    ('create_low_risk_state_chart', "Create " +SettlementProcessUtils.lowRiskStateChart + " State Chart",
                       'bool', [False, True], True)]

    def ael_main(dict):
        start(dict["create_high_risk_state_chart"], dict["create_medium_risk_state_chart"], dict["create_low_risk_state_chart"])

except Exception as e:
    if globals().has_key('ael_variables'):
        del globals()['ael_variables']
    if globals().has_key('ael_main'):
        del globals()['ael_main']
    Utils.LogAlways('Could not run FSettlementProcessSetup due to ')
    Utils.LogAlways(str(e))
