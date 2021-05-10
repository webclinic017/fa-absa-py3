""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_fva/./etc/FVAHooksTemplate.py"
'''---------------------------------------------------------------------
FVAHooksTemplate module contains functions called by the AA Integration. 
It should never be edited. All functions in FVAHooksTemplate can be 
overridden in a FVAHooks module. To do so, create a module called FVAHooks 
(or rename the FVAHooksTemplate to FVAHooks) and copy the function 
declaration of the function you want to override into it. 
---------------------------------------------------------------------'''

import acm

def CreditDeskCounterParty():
    return 'FVA Credit sales desk'

def IsFVACandidate(trade):
    """Filter to enable Request FVA"""
    hasCreditBalance = trade.CreditBalance() != None
    isStatusSimulated = trade.Status() == 'Simulated'
    return hasCreditBalance and isStatusSimulated
    
def ConfirmedTradeStatus():
    """Trade status to use after FVA is confirmed"""
    return 'FO Confirmed'

def CreditBalanceIncludedTrades():
    ''' This method creates a filter (FASQLQuery) that specifies if a trade should be included in 
        the Credit Balance portfolio. The filter is merged with the filter defined by the mapping in the 
        extension value 'creditBalanceToTrade'.
        
        It is also possible to use a stored insert items query
        Example:
            1. Create a shared Insert Items query that excludes trades where Status = Simulated named "GlobalFVAFilter"
            2. Use this stored query in the hook
            
               def CreditBalanceIncludedTrades(): 
                   filter = acm.FStoredASQLQuery["GlobalFVAFilter"]
                   return filter.Query()
    '''
    enum = acm.FEnumeration["enum(TradeStatus)"].Enumeration("Simulated")
    return acm.Filter.SimpleAndQuery("FTrade", "Status", "GREATER", enum)
