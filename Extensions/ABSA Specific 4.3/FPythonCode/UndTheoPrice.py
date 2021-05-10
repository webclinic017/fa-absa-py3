

import acm

def missingUnderlying(trade):
    
    message = "The instrument of trade {0} doesn't have an underlying."
    return ValueError(message.format(trade.Oid()))


def getUndTheoPrice(trade):
    if trade.Instrument().Underlying():
        und_ins = trade.Instrument().Underlying()

        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        und_ins_calcs = und_ins.Calculation()
        
        return und_ins_calcs.TheoreticalPrice(cs)
    else:
        raise missingUnderlying(trade)
    
