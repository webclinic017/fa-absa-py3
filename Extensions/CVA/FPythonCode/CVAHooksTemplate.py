
'''---------------------------------------------------------------------
CVAHooksTemplate module contains functions called by the AA Integration. 
It should never be edited. All functions in CVAHooksTemplate can be 
overridden in a CVAHooks module. To do so, create a module called CVAHooks 
(or rename the CVAHooksTemplate to CVAHooks) and copy the function 
declaration of the function you want to override into it. 
---------------------------------------------------------------------'''

import acm

def CreditDeskCounterParty():
    return 'Credit sales desk'

def IsCVACandidate(trade):
    """Filter to enable Request CVA"""
    hasCreditBalance = trade.CreditBalance() != None
    isStatusSimulated = trade.Status() == 'Simulated'
    return hasCreditBalance and isStatusSimulated
    
def ConfirmedTradeStatus():
    """Trade status to use after CVA is confirmed"""
    return 'FO Confirmed'

def CreditBalanceIncludedTrades(creditBalanceInstrument):
    ''' This method creates a filter (FASQLQuery) that specifies if a trade should be included in 
        the Credit Balance portfolio. The filter is merged with the filter defined by the mapping in the 
        extension value 'creditBalanceToTrade'.
        
        It is also possible to use a stored insert items query
        Example:
            1. Create a shared Insert Items query that excludes trades where Status = Simulated named "GlobalCVAFilter"
            2. Use this stored query in the hook
            
               def CreditBalanceIncludedTrades(): 
                   filter = acm.FStoredASQLQuery["GlobalCVAFilter"]
                   return filter.Query()
    '''
    enum = acm.FEnumeration["enum(TradeStatus)"].Enumeration("Simulated")
    return acm.Filter.SimpleAndQuery("FTrade", "Status", "GREATER", enum)
