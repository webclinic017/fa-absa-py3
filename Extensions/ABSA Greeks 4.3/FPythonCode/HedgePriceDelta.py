
import acm
import sys

denominatedvalue = acm.GetFunction('denominatedvalue', 4)

def hedgePriceDeltaFilter(hedge, dv):
    if hedge:
        return dv
    return denominatedvalue(0.0, dv.Unit(), dv.Type(), dv.DateTime())
