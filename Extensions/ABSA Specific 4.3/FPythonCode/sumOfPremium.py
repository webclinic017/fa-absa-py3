import acm
import sys

def sumOfTradesUnSettledPremium(tradesInPosition, endDate, multiplier, accumulated):
    sum = 0
    for t in tradesInPosition.AsArray():
        if t.Status() != "Simulated":
           if t.ValueDay() > endDate:
                if accumulated:
                    if t.Premium() * multiplier > 0:
                        sum = sum + t.Premium()
                else:
                    #if acm.Time.AsDate(t.TradeTime()) == endDate:
                    if t.Premium() * multiplier > 0:
                        sum = sum + t.Premium()
                    if multiplier == 0:
                        sum = sum + t.Premium()
        
        
    return sum
