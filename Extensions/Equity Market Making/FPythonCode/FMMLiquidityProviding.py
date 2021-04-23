"""----------------------------------------------------------------------------
MODULE
    FMMLiquidityProviding - Market Making specific.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.
 ---------------------------------------------------------------------------"""
import acm
import ael
import math

""" Minimum Quantity
Amounts listed in EUR will be converted into number of stocks by dividing the EUR amount
through the stock price and then rounding up to the next multiple of roundLot. However, only
2,000 stocks must be quoted. A stock price of EUR 210.50 for a liquidity class 2
instrument, for example, is converted to a minimum quote size of 100 stocks. 
The minimum quote size is reviewed on a weekly basis.

"""
def minimumQuantity(liquidityClass, price, quantityOrAmount, quantityType, roundLot):   
    if quantityType == 1 or quantityType == 'Amount':
        return MaxQuoteValueQuantity(quantityOrAmount, price, roundLot)
    
    else:       
        mqs = 1
        if liquidityClass == 0:
            return quantityOrAmount
        if liquidityClass == 1:
            mqs = 20000
        if liquidityClass == 2:
            mqs = 15000
        if liquidityClass == 3:
            mqs = 10000
        if liquidityClass == 4:
            mqs = 5000
        if liquidityClass == 5:
            mqs = 1

        reducedSize = HighPriceEquity(mqs, price)
        if reducedSize < 100:
            return reducedSize

        return LiquidityClassMinimumQuantity(mqs, price) 

"""
MaxQuoteValueQuantity

"""
def MaxQuoteValueQuantity(amount, price, roundLot): 
    if amount == 0:
        return 0
	
    else:
        if price == 0:
            return 0
        rawVolume = amount / price        
        return FixRoundLotUp(rawVolume, roundLot)
        

"""HighPriceEquity
To reduce the risk for high-priced equities, a lower minimum quote size applies for equities traded in
Xetra with Round Lot 1. Here, the following minimum quote sizes apply:

- 50 stocks, if the transaction value of 100 stocks exceeds five times the amount of the MQS
- 10 stocks, if the transaction value of 100 stocks exceeds ten times the amount of the MQS
- 2 stocks, if the transaction value of 100 stocks exceeds fifty times the amount of the MQS

For example, if a stock is worth 630 Euro in a liquidity class 3 instrument, the minimum
quote size is converted to 50 shares.

"""
def HighPriceEquity(mqs, price):
    if 100*price / 50 > mqs:
        return 2  
    if 100*price / 10 > mqs:
        return 10  
    if 100*price / 5 > mqs:
        return 50
    else:
        return 100  

""" Minimum Quantity

"""
def LiquidityClassMinimumQuantity(mqs, price):
    if price != 0.0:
        qty = mqs / price 
        return FixRoundLotUp(qty)
    else:
        return 100

def FixRoundLotUp(quantity, roundLot):
    if quantity > 0:
        return math.ceil((quantity) / roundLot) * roundLot
    else:
        return 0
