import acm

def Trade(trade):
    t = trade
    if trade.IsFxSwapFarLeg():
        t = trade.FxSwapNearLeg()
    return t
    
def SalesDeskPortfolio(trade):
    try:
        return Trade(trade).AdditionalInfo().SalesDeskPortfolio()
    except:
        return None
        
def SalesDeskAcquirer(trade):
    try:
        return Trade(trade).AdditionalInfo().SalesDeskAcquirer()
    except:
        return None

def SalesSpotPrice(trade):
    try:
        return Trade(trade).AdditionalInfo().SalesSpotPrice()
    except:
        return None

def SalesNearPrice(trade):
    try:
        return Trade(trade).AdditionalInfo().SalesNearPrice()
    except:
        return None

def SalesFarPrice(trade):
    try:        
        return Trade(trade).AdditionalInfo().SalesFarPrice()
    except:
        return None

def SplitSpotPrice(trade):
    try:
        return Trade(trade).AdditionalInfo().SplitSpotPrice()
    except:
        return None

def SplitNearPrice(trade):
    try:
        return Trade(trade).AdditionalInfo().SplitNearPrice()
    except:
        return None

def SplitFarPrice(trade):
    try:
        return Trade(trade).AdditionalInfo().SplitFarPrice()
    except:
        return None
