import acm

def OnPrepare(self):
    if None != self.HedgeLegCombination():
        self.HedgeLegOrderBook = acm.Trading.CreateBasketTrading(self.HedgeLegCombination())

    #Call QuoteAndHedge OnPrepare
    method = self.Class().Superclass().GetMethod('OnPrepare', 0)(self)
