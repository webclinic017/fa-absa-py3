""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FCounterpartyExposureUtils.py"

"""------------------------------------------------------------------------------------------------
MODULE
    FCounterpartyExposureUtils

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Utils for the column Portfolio Inventory Position + Counterparty Exposure Limit  

------------------------------------------------------------------------------------------------"""

import acm
import math

def GetExposureThresholdFromCounterparty(object):
    cptyName = str(object)
    # This function is intended to retrieve the Exposure Threshold Limit for a counterparty.
    # The customer can override this function to retrieve the correspondand limit from the appropriate source.
    # By default the exposure limit is set to a big number: 1 000 000 000 000 in the FX Base Currency set in the system.
    return 5000000000000


csc = acm.Calculations().CreateStandardCalculationsSpaceCollection()
prices = {}

def GetExposureFromCounterparty(tradesCpty, simuTrades, currency):
    result = 0
    trades = []
    trades.extend(tradesCpty)
    trades.extend(simuTrades)
    for trade in trades:
        if not trade.Instrument().Underlying() in prices:
            marketPrice = SecurityMarketPrice(trade, currency, csc)
            prices[trade.Instrument().Underlying()] = marketPrice
        if not math.isnan(prices[trade.Instrument().Underlying()]):
            exposure = trade.Quantity()*prices[trade.Instrument().Underlying()]
            result +=  exposure.Number()            
    return result


def SecurityMarketPrice(trade, currency, csc):
    instrument = trade.Instrument()
    today = acm.Time().DateNow()
    curr = currency
    price = instrument.Underlying().Calculation().MarketPrice(csc, today, 0, curr)
    return price.Value()


import FParameterSettings
_SETTINGS_ALLOC = FParameterSettings.ParameterSettingsCreator.FromRootParameter('SecLendAllocationSettings')

def GetAvailabilityPortfolio():
    return acm.FPhysicalPortfolio[_SETTINGS_ALLOC.AvailabilityPortfolio()]



