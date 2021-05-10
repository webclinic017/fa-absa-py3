""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/singletons/FSettlementUpdaterSingleton.py"
from FSettlementUpdater import SettlementUpdater

CONST_SettlementUpdater = None

#-------------------------------------------------------------------------
def GetSettlementUpdater():
    global CONST_SettlementUpdater
    if CONST_SettlementUpdater != None:
        return CONST_SettlementUpdater

    CONST_SettlementUpdater = SettlementUpdater()
    return CONST_SettlementUpdater