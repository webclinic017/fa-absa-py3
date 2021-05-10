""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FTrade2SalesActivityCustomFunctions.py"
"""--------------------------------------------------------------------------
MODULE
    FTrade2SalesActivityCustomFunctions

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

import acm


def HasCBTradeInDealPackage(trade):
    hasCBTrade = False
    if trade.DealPackage() != None:
        for dptrade in trade.DealPackage().Trades():
            if dptrade.Instrument().IsKindOf(acm.FConvertible):
                hasCBTrade = True
    return hasCBTrade

def GetCBPriceFromDealPackage(trade):
    cbPrice = 0.0
    if trade.DealPackage() != None:
        for dptrade in trade.DealPackage().Trades():
            if dptrade.Instrument().IsKindOf(acm.FConvertible):
                cbPrice = acm.DenominatedValue(
                    dptrade.Price(), 
                    dptrade.Currency(), 
                    'Price', 
                    acm.Time.DateValueDay()
                    )
    return cbPrice

def GetStockPriceFromDealPackage(trade):
    stockPrice = 0.0
    if trade.DealPackage() != None:
        for dptrade in trade.DealPackage().Trades():
            if dptrade.Instrument().IsKindOf(acm.FStock):
                stockPrice = acm.DenominatedValue(
                    dptrade.Price(), 
                    dptrade.Currency(), 
                    'Price', 
                    acm.Time.DateValueDay()
                    )
    return stockPrice

def IsASCOTTrade(trade):
    hasCBTrade = HasCBTradeInDealPackage(trade)
    isCBOptionTrade = trade.Instrument().IsKindOf(acm.FOption) and trade.Instrument().Underlying().IsKindOf(acm.FConvertible)
    return isCBOptionTrade and not hasCBTrade