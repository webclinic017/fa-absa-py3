""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/singletons/FSettlementTradeAmendmentFilterHandlerSingleton.py"
from FSettlementTradeFilter import TradeAmendmentFilterHandler

CONST_TradeAmendmentFilterHandler = None

#-------------------------------------------------------------------------
def GetTradeAmendmentFilterHandler():
    global CONST_TradeAmendmentFilterHandler
    if CONST_TradeAmendmentFilterHandler != None:
        return CONST_TradeAmendmentFilterHandler
    CONST_TradeAmendmentFilterHandler = TradeAmendmentFilterHandler()
    return CONST_TradeAmendmentFilterHandler