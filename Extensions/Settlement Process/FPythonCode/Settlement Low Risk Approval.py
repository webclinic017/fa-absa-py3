
import acm
import SettlementProcessUtils


def HasUserRights():
    return SettlementProcessUtils.HasUserRights(SettlementProcessUtils.operationLowName)

def condition_entry_state_approval_complete(context):
    return HasUserRights()
    
def condition_entry_state_ready(context):
    if SettlementProcessUtils.IsUpdateEvent(context):
        return True
    return HasUserRights()

def condition_entry_state_rejected_level_1(context):
    return HasUserRights()

def condition_exit_state_rejected_level_1(context):
    if SettlementProcessUtils.IsUpdateEvent(context):
        return True
    return SettlementProcessUtils.CanLeaveRejectedState(context) and HasUserRights()
