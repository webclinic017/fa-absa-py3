""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/singletons/FSettlementRecallHandlerSingleton.py"
from FSettlementRecallHandler import SettlementRecallHandler

CONST_SettlementRecallHandler = None

#-------------------------------------------------------------------------
def GetSettlementRecallHandler():
    global CONST_SettlementRecallHandler
    if CONST_SettlementRecallHandler != None:
        return CONST_SettlementRecallHandler
    CONST_SettlementRecallHandler = SettlementRecallHandler()
    return CONST_SettlementRecallHandler