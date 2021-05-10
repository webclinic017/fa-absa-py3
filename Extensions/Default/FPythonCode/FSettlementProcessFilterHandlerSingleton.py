""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/singletons/FSettlementProcessFilterHandlerSingleton.py"
from FSettlementTradeFilter import SettlementProcessFilterHandler

CONST_SettlementProcessFilterHandler = None

#-------------------------------------------------------------------------
def GetSettlementProcessFilterHandler():
    global CONST_SettlementProcessFilterHandler
    if CONST_SettlementProcessFilterHandler != None:
        return CONST_SettlementProcessFilterHandler
    CONST_SettlementProcessFilterHandler = SettlementProcessFilterHandler()
    return CONST_SettlementProcessFilterHandler
