import acm
import FOperationsUtils as Utils

operationHighName = "Approve High Risk Settlements"
operationMediumName = "Approve Medium Risk Settlements"
operationLowName = "Approve Low Risk Settlements"
operationBypass = "Bypass Settlement Process"

highRiskStateChart = "Settlement High Risk Approval"
mediumRiskStateChart = "Settlement Medium Risk Approval"
lowRiskStateChart = "Settlement Low Risk Approval"



approvedLevel1 = "Approved Level 1"
approvedLevel2 ="Approved Level 2"
approvalComplete ="Approval Complete"
rejectedLevel1 ="Rejected Level 1"
rejectedLevel2 = "Rejected Level 2"
rejectedLevel3 = "Rejected Level 3"
error = "Error"

approvePaymentsLevel1 = "Approve - Level 1" 
approvePaymentsLevel2 = "Approve - Level 2"
approvePaymentsLevel3 = "Approve - Level 3"

rejectPaymentsLevel1 = "Reject - Level 1"
rejectPaymentsLevel2 = "Reject - Level 2"
rejectPaymentsLevel3 = "Reject - Level 3"

approveRejectedLevel1 = "Approve Rejected - Level 1"
approveRejectedLevel2 = "Approve Rejected - Level 2"
approveRejectedLevel3 = "Approve Rejected - Level 3"
 
sendForReProcessing =  "Send For Re-Processing"

settlementUpdate = "Settlement Update"

import acm
def HasBeenUpdaterByUserAfterReadyState(approvalProcess):
    if approvalProcess:
        for step in approvalProcess.Steps():
            if step.UpdateUser() == acm.User() and ("Rejected" not in step.State().Name()):
                return True
    return False



def CanLeaveApprovedState(context):
    if UserHasOperationPermission(acm.User(), operationBypass):
        return True
    return not HasBeenUpdaterByUserAfterReadyState(context.Subject().Originator().GetSettlementProcess())


def CanLeaveRejectedState(context):
    if UserHasOperationPermission(acm.User(), operationBypass):
        return True

    return context.Subject().Originator().GetSettlementProcess().CurrentStep().UpdateUser() == acm.User()

def HasUserRights(operationName):
    if UserHasOperationPermission(acm.User(), operationBypass):
        return True

    if UserHasOperationPermission(acm.User(), operationName):
        return True
    return False



def IsSuperUser():
    return UserHasOperationPermission(acm.User(), operationBypass)

def GetOperationComponentType():
    componentTypes = acm.FEnumeration['enum(ComponentType)']
    return componentTypes.Enumeration('Operation')

def UserHasOperationPermission(user, operation):
    if OperationExists(operation):
        return user.IsAllowed(operation, GetOperationComponentType())
    return False

def OperationExists(operation):
    compType = 'Operation'
    queryString = 'name=\'%s\' and type=\'%s\'' % (operation, compType)
    op = acm.FComponent.Select01(queryString, '')
    if op == None:
        return False
    return True

def AddOperation(operationName):
    if not OperationExists(operationName):
        componentTypes = acm.FEnumeration['enum(ComponentType)']
        operation = componentTypes.Enumeration('Operation')
        component = acm.FComponent()
        component.Name(operationName)
        component.Type(operation)
        component.Commit()

        Utils.LogAlways('Operation added: \'%s\'' % (operationName))
    else:
        Utils.LogAlways('Operation already exists: \'%s\'' % (operationName))


settlementProcessStatusDictionary = dict()
def FindProcessStatus(sortOrder):
    if sortOrder in settlementProcessStatusDictionary:
        return settlementProcessStatusDictionary[sortOrder]
    choiceList = acm.FChoiceList.Select("list = 'SettlementProcessStatus'")
    for item in choiceList:
        if item.SortOrder() == sortOrder:
            settlementProcessStatusDictionary[sortOrder] = item
            return item

def ProcessStatus(settlement):
    if settlement.ProcessStatusChlItem():
        return settlement.ProcessStatusChlItem()
    elif settlement.StateChart():
        return FindProcessStatus(1)
    return FindProcessStatus(0)

def IsUpdateEvent(context):
    isSettlementUpdate = False
    event = context.Event()
    if event and event.Name() == settlementUpdate:
        isSettlementUpdate = True
    return isSettlementUpdate

def HideProcessStatus(settlement):
    hideProcessStatus = False
    if settlement.Parent() or len(settlement.SplitChildren()):
        hideProcessStatus = True
    return hideProcessStatus
