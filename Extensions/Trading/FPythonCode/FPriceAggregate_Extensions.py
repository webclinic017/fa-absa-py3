
import acm

def OrderBookInterface(self):
    if self.IsKindOf('FPriceLevelRow'):
        return self.TradingInterface()
    else:
        return None
        
