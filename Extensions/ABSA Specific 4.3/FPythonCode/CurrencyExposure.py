"""-----------------------------------------------------------------------------
PURPOSE                 :  Calculates currency exposure
DEPATMENT AND DESK      :  Front Office, FX Spot
REQUESTER               :  Denzil Pieterse
DEVELOPER               :  Francois Truter
CR NUMBER               :  XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-05-11 XXXXXX    Francois Truter           Initial Implementation
--------------------------------------------------------------------------------"""

import acm
import FBDPCommon 

ZAR = acm.FCurrency['ZAR']
    
def GetZarExposureCurrency(currencyPair):
    exposureCurrency = None
    if currencyPair.Currency1() == ZAR and currencyPair.Currency2() != ZAR:
        exposureCurrency = currencyPair.Currency2()
    elif currencyPair.Currency1() != ZAR and currencyPair.Currency2() == ZAR:
        exposureCurrency = currencyPair.Currency1()
    
    return exposureCurrency
    
def GetZarCurrencyExposure(trades, currency, exposureDate):
    today = acm.Time().DateNow()
    exposure = {acm.Time().DateNow(): 0}
        
    for trade in trades.AsArray():
        if trade.Instrument().IsExpiredAt(exposureDate):
            continue
        if trade.CurrencyPair():
            exposureCurrency = GetZarExposureCurrency(trade.CurrencyPair())
            if exposureCurrency and exposureCurrency == currency:
                exposureDate = today if trade.ValueDay() < today else trade.ValueDay()
                if not exposureDate in exposure:
                    exposure[exposureDate] = 0
                exposure[exposureDate] += trade.Nominal()
        
        for payment in trade.Payments():
            if payment.Currency() == currency:
                exposureDate = today if payment.PayDay() < today else payment.PayDay()
                if not exposureDate in exposure:
                    exposure[exposureDate] = 0
                exposure[exposureDate] += payment.Amount()
    
    results = acm.FArray()
    for exposureDate in exposure:
        results.Add(acm.DenominatedValue(exposure[exposureDate], currency.Name(), exposureDate))
    
    return results
