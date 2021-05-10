""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementClientSTPTemplate.py"
"""----------------------------------------------------------------------------
MODULE
    FSettlementClientSTPTemplate - Module which includes STP rules defiend
    by the customer.


DESCRIPTION
    Client STP processing is done after ordinary STP. After making changes
    to this file, the settlement ATS needs to be restarted for the changes
    to take affect.

RENAME 
    This module to FSettlementClientSTP since this file is only template.

----------------------------------------------------------------------------"""

def ClientSTP(settlement):
    '''
    The ClientSTP function is documented in FCA 2104 and FCA 2105. In short
    this hook can be used to put a settlement record to status Manual Match
    for manual authorisation. This hook is called upon if the core validation
    (STP) does not find any Exceptions, i.e. it would have been set to 
    Authorised by core STP. It is also possible to write to the diary in
    this hook with the return value.
    
    Input - The FSettlement (acm object) that can be set to Manual Match
            (or Authorised).
    Output - A string. The return value of the string should be either
             "Manual Match" or "Authorised" followed by optional ":" 
             concatenated with string the should be put in the diary.
    Example - 
        if (settlement.Trade() and
            settlement.Trade().Instrument().InsType() == "Bond"):
            return "Manual Match: Settlements from bond trades needs manual authorisation"
        else:
            return "Authorised"
    '''
    
    return "Authorised"
    
    