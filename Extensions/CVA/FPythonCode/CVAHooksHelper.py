
import acm
USER_MODULE_EXISTS = False
try:
    import CVAHooks
    USER_MODULE_EXISTS = True
except:
    pass
import CVAHooksTemplate

def CreditDeskCounterParty():
    if USER_MODULE_EXISTS and hasattr(CVAHooks, 'CreditDeskCounterParty'):
        return CVAHooks.CreditDeskCounterParty()
    else:
        return CVAHooksTemplate.CreditDeskCounterParty()

def IsCVACandidate(trade):
    if USER_MODULE_EXISTS and hasattr(CVAHooks, 'IsCVACandidate'):
        return CVAHooks.IsCVACandidate(trade)
    else:
        return CVAHooksTemplate.IsCVACandidate(trade)

def ConfirmedTradeStatus():
    if USER_MODULE_EXISTS and hasattr(CVAHooks, 'ConfirmedTradeStatus'):
        return CVAHooks.ConfirmedTradeStatus()
    else:
        return CVAHooksTemplate.ConfirmedTradeStatus()

def CreditBalanceIncludedTrades(creditBalanceInstrument):
    if USER_MODULE_EXISTS and hasattr(CVAHooks, 'CreditBalanceIncludedTrades'):
        return CVAHooks.CreditBalanceIncludedTrades(creditBalanceInstrument)
    else:
        return CVAHooksTemplate.CreditBalanceIncludedTrades(creditBalanceInstrument)
