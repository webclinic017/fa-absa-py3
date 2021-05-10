
import SAIT_Portfolios

def getRootPortfolio(trade):
    if trade.Portfolio():
        rootPrf = SAIT_Portfolios.get_root(None, trade.Portfolio().Name(), 0)
        if rootPrf:
            return rootPrf
        return 'None'
    return 'None'
