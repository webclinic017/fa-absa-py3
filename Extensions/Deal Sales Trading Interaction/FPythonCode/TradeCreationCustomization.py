import acm
from TradeCreationTemplate import TradeCreationTemplate
        
'''********************************************************************
* Methods to specify the creation of trades
********************************************************************'''            
def TradeCreation(hookArgument, *args):
    return TradeCreationTemplate(hookArgument)
