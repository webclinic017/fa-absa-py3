""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/singletons/FSettlementModificationInspectorSingleton.py"
from FSettlementModificationInspector import SettlementModificationInspector

CONST_ModInspector = None

#-------------------------------------------------------------------------
def GetModInspector():
    global CONST_ModInspector
    if CONST_ModInspector != None:
        return CONST_ModInspector
    CONST_ModInspector = SettlementModificationInspector()
    return CONST_ModInspector