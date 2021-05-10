""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/singletons/FSettlementCreatorSingleton.py"
from FSettlementCreator import SettlementCreator

CONST_SettlementCreator = None

#-------------------------------------------------------------------------
def GetSettlementCreator():
    global CONST_SettlementCreator
    if CONST_SettlementCreator != None:
        return CONST_SettlementCreator

    CONST_SettlementCreator = SettlementCreator()
    return CONST_SettlementCreator