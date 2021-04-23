import acm

def CalculateOutcomeScore(performance, participation_result, participation_planned):
    return 1000*(float(performance) - 10*(float(participation_planned) - float(participation_result))**2)

def BestOutcomeScore(taker, maker, no_trade, instant_trade):
    
    if taker == max(taker, maker, no_trade, instant_trade):
        return "taker"
    if maker == max(taker, maker, no_trade, instant_trade):
        return "maker"
    if no_trade == max(taker, maker, no_trade, instant_trade):
        return "no trade"
    if instant_trade == max(taker, maker, no_trade, instant_trade):
        return "instant trade"
    return "?"
