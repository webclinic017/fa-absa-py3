
import acm
import SettlementProcessUtils

def CanLeaveRejectedState(context):
    return SettlementProcessUtils.CanLeaveRejectedState(context)

def HasUserRights():
    return SettlementProcessUtils.HasUserRights(SettlementProcessUtils.operationHighName)

def condition_entry_state_ready(context):
    if SettlementProcessUtils.IsUpdateEvent(context):
        return True
    return HasUserRights()

def condition_entry_state_approved_level_1(context):
    return HasUserRights()
    

def condition_exit_state_approved_level_1(context):
    if SettlementProcessUtils.IsUpdateEvent(context):
        return True
    if SettlementProcessUtils.IsSuperUser():
        return True
    if HasUserRights():
        if SettlementProcessUtils.CanLeaveApprovedState(context):
            return True
    return False

def condition_entry_state_approved_level_1(context):
    return HasUserRights()

def condition_exit_state_approved_level_2(context):
    if SettlementProcessUtils.IsUpdateEvent(context):
        return True
    if SettlementProcessUtils.IsSuperUser():
        return True
    if HasUserRights():
        if SettlementProcessUtils.CanLeaveApprovedState(context):
            return True
    return False

def condition_entry_state_approval_complete(context):
    return HasUserRights()

def condition_entry_state_rejected_level_1(context):
    return HasUserRights()

def condition_exit_state_rejected_level_1(context):
    if SettlementProcessUtils.IsUpdateEvent(context):
        return True
    return CanLeaveRejectedState(context) and HasUserRights()

def condition_entry_state_rejected_level_2(context):
    return HasUserRights()

def condition_exit_state_rejected_level_2(context):
    if SettlementProcessUtils.IsUpdateEvent(context):
        return True
    return CanLeaveRejectedState(context) and HasUserRights()

def condition_entry_state_rejected_level_3(context):
    return HasUserRights()

def condition_exit_state_rejected_level_3(context):
    if SettlementProcessUtils.IsUpdateEvent(context):
        return True
    return CanLeaveRejectedState(context) and HasUserRights()
