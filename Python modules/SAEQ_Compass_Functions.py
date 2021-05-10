import acm
"""-----------------------------------------------------------------------------
PROJECT                 :  Compass feed
PURPOSE                 :  These functions calculate specific values that are
                           required in the Compass Feed
DEPATMENT AND DESK      :  Equities
REQUESTER               :  Cameron Ashton
DEVELOPER               :  Rohan van der Walt
CR NUMBER               :  XXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no  Developer                 Description
--------------------------------------------------------------------------------
2012-02-22  889960     Rohan vd Walt             Initial Implementation
"""

def getBoughtOrSold(trades, endDay, buyOrSell = 'Buy'):
    factor = 1 if buyOrSell == 'Buy' else -1
    total = 0
    for t in trades.AsList():
        if t.TradeTime() >= endDay and factor * t.Quantity() > 0:
            total += t.Quantity()
    return total

def getAvgPrice(trades, endDay, buyOrSell = 'Buy'):
    factor = 1 if buyOrSell == 'Buy' else -1
    total = 0
    val = 0
    for t in trades.AsList():
        if t.TradeTime() >= endDay and factor * t.Quantity() > 0:
            total += t.Quantity()
            val += (t.Quantity()*t.Price())/100
    return val/total if val else 0
