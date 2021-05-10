
"""----------------------------------------------------------------------------
MODULE
    FQuoteSettingHooks - Includes hooks that are used when creating quote settings.

    (c) Copyright 2013 by SunGard FRONT ARENA. All rights reserved.
 ---------------------------------------------------------------------------"""

import acm

""" Return trading settings value class.
"""
def actualClass():
    return acm.FOrderBook
    
""" Return trading settings for order book.
"""
def orderBookTradingSettings(invokationInfo):
    return invokationInfo.TradingSettings(invokationInfo.TradingInterface(), actualClass())

""" Return trading settings for the default order book
    of the instrument.
"""
def defaultOrderBookTradingSettings(invokationInfo):
    tradingInterface = acm.Trading.DefaultTradingInterface(invokationInfo.Instrument())
    if tradingInterface:
        return invokationInfo.TradingSettings(tradingInterface, actualClass())
    return None

""" Return trading settings for underlying order book.
"""    
def underlyingTradingSettings(invokationInfo):
    quoteUnderlying = invokationInfo.QuoteUnderlying()
    if quoteUnderlying.Size() == 1:
        tradingInterface = quoteUnderlying.PriceFeed().TradingInterface()
        return invokationInfo.TradingSettings(tradingInterface, actualClass())
    return invokationInfo.TradingSettings(quoteUnderlying, actualClass())
    
