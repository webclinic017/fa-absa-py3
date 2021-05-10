"""----------------------------------------------------------------------------
Date            Change Number   Developer       Description
2018-05-11      CHG1000406751   Willie vd Bank  Initial implementation
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
    '''
    if (settlement.Type() == "Security Nominal" and
            settlement.Trade() and
            settlement.Trade().Acquirer().Name() in ("AFRICA DESK") and 
            settlement.Trade().Instrument().InsType() in ("Bond", "Bill")):
        trade = settlement.Trade()
        if len(trade.Instrument().Isin()) != 12:
            return "Manual Match:Warning - Incorrect or missing Isin!"
        elif settlement.Currency().Name() == 'GHS':
            payments = trade.Payments()
            if len(payments) > 1:
                return "Manual Match:Warning - Trade has more than 1 additional payment!"
    return "Authorised"
