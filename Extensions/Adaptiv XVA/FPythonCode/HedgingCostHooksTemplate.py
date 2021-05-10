""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/HedgingCostHooksTemplate.py"
'''---------------------------------------------------------------------
All functions in HedgingCostHooksTemplate can be 
overridden in a HedgingCostHooks module. To do so, create a module called HedgingCostHooks 
(or rename the HedgingCostHooksTemplate to HedgingCostHooks) and copy the function 
declaration of the function you want to override into it. 
---------------------------------------------------------------------'''

import acm
context = acm.GetDefaultContext()

def CreditDeskCounterParty():
    return 'HedgingCost Credit sales desk'

def IsHedgingCostCandidate(trade):
    """Filter to enable Request HedgingCost"""
    hasCreditBalance = trade.CreditBalance() != None
    isStatusSimulated = trade.Status() == 'Simulated'
    return hasCreditBalance and isStatusSimulated
    
def ConfirmedTradeStatus():
    """Trade status to use after HedgingCost is confirmed"""
    return 'FO Confirmed'

def CreditBalanceIncludedTrades():
    ''' This method creates a filter (FASQLQuery) that specifies if a trade should be included in 
        the Credit Balance portfolio. The filter is merged with the filter defined by the mapping in the 
        extension value 'creditBalanceToTrade'.
        
        It is also possible to use a stored insert items query
        Example:
            1. Create a shared Insert Items query that excludes trades where Status = Simulated named "GlobalHedgingCostFilter"
            2. Use this stored query in the hook
            
               def CreditBalanceIncludedTrades(): 
                   filter = acm.FStoredASQLQuery["GlobalHedgingCostFilter"]
                   return filter.Query()
    '''
    enum = acm.FEnumeration["enum(TradeStatus)"].Enumeration("Simulated")
    return acm.Filter.SimpleAndQuery("FTrade", "Status", "GREATER", enum)

def GetSuggestedHedgingCost(trade):
    calculationSpaceTradeSheet = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')
    denomValue = calculationSpaceTradeSheet.CalculateValue(trade, 'Incremental CVA')
    return denomValue
