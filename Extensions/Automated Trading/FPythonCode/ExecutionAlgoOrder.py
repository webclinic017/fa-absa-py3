
import acm
import random
import datetime


def RoundQuantity(quantity):
    if quantity < 100:
            return round(quantity, 0)
    elif quantity < 1000:
            return round(quantity / 10, 0) * 10
    elif quantity < 10000:
            return round(quantity / 100, 0) * 100
    
    return round(quantity / 1000, 0) * 1000

                
def GetNewOrderPrice(self, event, order):
    Print2Trace(self, 'GetNewOrderPrice')
    tp = self.TargetPrice()
    op= order.Price().Number()   
    rf = self.BaseTradingInterface().GetDefaultValueEx("AlgoPriceSlackReactionFactor", self.Context())
    
    if acm.Math.AlmostZero(rf, 1e-4):
        return tp
       
    else:
        # jump ahead based on slack and reaction factor
        trig = self.Trigger().StringKey()        
        np = 0
        
     
        if trig == 'Join':
            ej = self.DistEJ()
            if ej > 0.0:
                np = tp + ((tp - op)/ej) * self.DistJM() * rf
                if self.BaseOrder().IsBuy() and (np > self.TargetPriceMatch()):
                    np = self.TargetPrice() + self.DistJM() - 0.001
                elif (not self.BaseOrder().IsBuy()) and (np < self.TargetPriceJoin()):
                    np = self.TargetPrice() - self.DistJM() + 0.001
            else:
                # price flickered, ignore update
                return op
        elif trig == 'Enter':
            np = tp + (tp - op) * rf
            if self.BaseOrder().IsBuy() and (np > self.TargetPriceJoin()):
                np = self.TargetPrice() + self.DistEJ() - 0.001
            elif (not self.BaseOrder().IsBuy()) and (np < self.TargetPriceJoin()):
                np = self.TargetPrice() - self.DistEJ() + 0.001
        else:
            return tp
            
        if self.BaseOrder().IsBuy():
            if (self.LimSlicePriceUsed() > 0.0) and (np > self.LimSlicePriceUsed()):
                np = self.LimSlicePriceUsed()
            elif (self.LimSlicePriceUsed() == 0.0) and (np > self.LimMaxPriceDiffAllowed()):
                np = self.LimMaxPriceDiffAllowed()
        else:
            if (self.LimSlicePriceUsed() > 0.0) and (np < self.LimSlicePriceUsed()):
                np = self.LimSlicePriceUsed()
            elif (self.LimSlicePriceUsed() == 0.0) and (np < self.LimMaxPriceDiffAllowed()):
                np = self.LimMaxPriceDiffAllowed()
        
        price = self.PriceFeed().RoundTickUpDown(not self.BaseOrder().IsBuy(), np)

        if self.PriceFeed().IsValidPrice(price) and self.OrderActive() and (not self.CurrentOrder().UpdateInProgress()):
            return price

        else:
            print ('error: invalid price')
    return tp



def Print2Trace(self, message):
    if self.IsTraceEnabled() and self.Log():
        self.Log().AddStringRecord(message)
    else:
        pass
    
def ActiveQty(self):
    if self.CurrentOrderActive():
        activeQty = self.CurrentOrder().MovedQuantity()
    return 0.0
    
