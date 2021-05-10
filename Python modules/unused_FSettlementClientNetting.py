""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementClientNettingTemplate - Module which includes Netting rules defiend
    by the user/customer.
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Client Netting is called after ordinary netting.
        
RENAME this module to FSettlementClientNetting since this file is only template.

----------------------------------------------------------------------------"""
import ael, FSettlementGeneral2
"""aef-------------------------------------------------------------------------
hook.FSettlementClientNetting::client_netting_1

The **client_netting_1** hook function and the **FSettlementClientNetting** module are a part of the Settlement script package - and support executing client defined netting rules. These rules are always called after standard netting rules. As a result of netting, settlements that match the netting rules (both ordinary and client netting rules) will be summed up in a new settlement. 

In order to create custom netting rules, the customer needs to:

1. Rename the **FSettlementClientNettingTemplate** module to **FSettlementClientNetting**.

2. Add a custom function (client_netting_1 is in place by default).

3. From PRIME (**Admin** menu) open the Netting Rule Definition window and create a netting rule. Update the **Netting Hook** field to points to the hook function, i.e. client_netting_1 (no need to state that a settlement is an input parameter, state just the function name). Note that if you want the rule to be applied for more then one trade use the **Bilateral Netting** checkbox.

4. If you want netting rules to be applied for a certain counterparty then do following: From PRIME (**Admin** menu) open a Party in the Party Definition window. On the **Netting Rule Links** tab, create a link to a netting rule.

Note that the ARENA Task Server real time process that executes **FSettlementAMB** needs to be restarted
every time this file is edited.

@category PRIME.Settlement
@param s:Settlement A settlement entity that is candidate for netting.
@return int If 1 settlement s can be netted, if 0 then not.
@example
def client_netting_1(s):
  # an example of client defined netting rule
  if abs(s.amount)>1000000:
    return 0
  else:
    return 1

----------------------------------------------------------------------------"""
def client_netting_1(s):
    if s.trdnbr.insaddr.legs().members() != [] and s.trdnbr.insaddr.legs()[0].amort_type == 'Annuity' and s.trdnbr.add_info('Funding Instype') == 'FDI':
        return 1
    else:
        return 0
    
def net_based_on_close_trade(s):    
    ''' Returns 1 if settlement should be be netted with the correspondent settlement(s)
        from the corrected trade.
    '''
    ret = 0    
    if s:
        if s.trdnbr:
            ret = FSettlementGeneral2.is_closing(s.trdnbr) or FSettlementGeneral2.is_closed(s.trdnbr)            
                
    return ret


