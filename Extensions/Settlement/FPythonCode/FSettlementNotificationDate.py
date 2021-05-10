""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementNotificationDate.py"
from FSettlementHookAdministrator import SettlementHooks, GetHookAdministrator

def GetNotificationDay(settlement):
    '''This hook function is called from the core PRIME when button is pressed '''
    hookAdmin = GetHookAdministrator()
    return hookAdmin.HA_CallHook(SettlementHooks.GET_NOTIFICATION_DATE, settlement)

