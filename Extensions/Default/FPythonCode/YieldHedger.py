import acm
import AutomaticHedger

def OnPrepare(self):
    AutomaticHedger.OnPrepare(self)

def CalculateSignedHedgeQuantity(self):
    trade = self.CurrentTrade()
    
    # The yield delta hedge ratio is calculated by extension values
    hedgeRatio = self.HedgeDelta()
    
    hedgeOrderBook = self.HedgeOrderBook()
    signedTradeQuantity = 0
    
    if trade.BuySell() == "Buy":
        signedTradeQuantity = abs(trade.Quantity())
    elif trade.BuySell() == "Sell":
        signedTradeQuantity = - abs(trade.Quantity())
    else:
        self.HedgeOrder = None
        self.SmartOrder = None
        raise Exception
    
    numberOfTradedContracts = signedTradeQuantity / trade.Instrument().ContractSize()
    signedHedgeQuantity = hedgeRatio * numberOfTradedContracts
    
    return signedHedgeQuantity
