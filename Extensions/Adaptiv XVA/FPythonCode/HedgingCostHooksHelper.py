""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/HedgingCostHooksHelper.py"
import acm
USER_MODULE_EXISTS = False
try:
    import HedgingCostHooks
    USER_MODULE_EXISTS = True
except:
    pass
import HedgingCostHooksTemplate

def CreditDeskCounterParty():
    if USER_MODULE_EXISTS and hasattr(HedgingCostHooks, 'CreditDeskCounterParty'):
        return HedgingCostHooks.CreditDeskCounterParty()
    else:
        return HedgingCostHooksTemplate.CreditDeskCounterParty()

def IsHedgingCostCandidate(trade):
    if USER_MODULE_EXISTS and hasattr(CVAHooks, 'IsHedgingCostCandidate'):
        return HedgingCostHooks.IsHedgingCostCandidate(trade)
    else:
        return HedgingCostHooksTemplate.IsHedgingCostCandidate(trade)

def ConfirmedTradeStatus():
    if USER_MODULE_EXISTS and hasattr(HedgingCostHooks, 'ConfirmedTradeStatus'):
        return HedgingCostHooks.ConfirmedTradeStatus()
    else:
        return HedgingCostHooksTemplate.ConfirmedTradeStatus()

def CreditBalanceIncludedTrades():
    if USER_MODULE_EXISTS and hasattr(HedgingCostHooks, 'CreditBalanceIncludedTrades'):
        return HedgingCostHooks.CreditBalanceIncludedTrades()
    else:
        return HedgingCostHooksTemplate.CreditBalanceIncludedTrades()
        
def SuggestedHedgingCost(trade):
    if USER_MODULE_EXISTS and hasattr(HedgingCostHooks, 'GetSuggestedHedgingCost'):
        return HedgingCostHooks.GetSuggestedHedgingCost(trade)
    else:
        return HedgingCostHooksTemplate.GetSuggestedHedgingCost(trade)
