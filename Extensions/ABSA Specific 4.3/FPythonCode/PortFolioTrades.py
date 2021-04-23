
import ael, string, time

def getTrades(trades, startDate, endDate):
    newTrades = []
    for trade in trades:
        if ael.date_from_time(trade.time) >= startDate  and  ael.date_from_time(trade.time) <= endDate:
            newTrades.append(trade.trdnbr)
    return newTrades
   

def getPremiumforTrades(trades, startDate, endDate):
    filteredTrades = getTrades(trades, startDate, endDate)
    tradePremium = 0
    for trade in filteredTrades :
        tradePremium  = tradePremium  + ael.Trade[trade].premium
    return tradePremium  

def getZARPremiumforTrades(trades, startDate, endDate):
    filteredTrades = getTrades(trades, startDate, endDate)
    tradePremium = 0
    for trade in filteredTrades :
        tradePremium  = tradePremium  + ael.Trade[trade].original_premium() 
    return tradePremium  
