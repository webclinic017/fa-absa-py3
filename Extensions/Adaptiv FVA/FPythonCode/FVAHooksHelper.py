""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_fva/./etc/FVAHooksHelper.py"
import acm
USER_MODULE_EXISTS = False
try:
    import FVAHooks
    USER_MODULE_EXISTS = True
except:
    pass
import FVAHooksTemplate

def CreditDeskCounterParty():
    if USER_MODULE_EXISTS and hasattr(FVAHooks, 'CreditDeskCounterParty'):
        return FVAHooks.CreditDeskCounterParty()
    else:
        return FVAHooksTemplate.CreditDeskCounterParty()

def IsFVACandidate(trade):
    if USER_MODULE_EXISTS and hasattr(CVAHooks, 'IsFVACandidate'):
        return FVAHooks.IsFVACandidate(trade)
    else:
        return FVAHooksTemplate.IsFVACandidate(trade)

def ConfirmedTradeStatus():
    if USER_MODULE_EXISTS and hasattr(FVAHooks, 'ConfirmedTradeStatus'):
        return FVAHooks.ConfirmedTradeStatus()
    else:
        return FVAHooksTemplate.ConfirmedTradeStatus()

def CreditBalanceIncludedTrades():
    if USER_MODULE_EXISTS and hasattr(FVAHooks, 'CreditBalanceIncludedTrades'):
        return FVAHooks.CreditBalanceIncludedTrades()
    else:
        return FVAHooksTemplate.CreditBalanceIncludedTrades()
