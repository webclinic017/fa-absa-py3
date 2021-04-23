""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FSalesActivityUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSalesActivityUtils

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A collection of utility functions used by Sales Activity.
-------------------------------------------------------------------------------------------------------"""

import math
import datetime
import acm
import FSheetUtils

def double(number):
    value = acm.GetFunction('double', 1)(number)
    if math.isnan(value):
        return 0
    return value
    
def FXRateIsValid(ins):
    try:
        curr1 = ins.Currency()
        curr2 = ins.Underlying().Currency()
        pairName = '/'.join((curr1.Name(), curr2.Name()))
        return bool(acm.FCurrencyPair.Select01('name=%s' % pairName, None))
    except AttributeError:
        return False

def FXRateLabel(ins):
    try:
        curr1 = ins.Currency()
        curr2 = ins.Underlying().Currency()
        return '/'.join((curr1.Name(), curr2.Name()))
    except Exception:
        return ''

def FXRateValue(ins, fxRate):
    if FXRateIsValid(ins):
        try:
            return 1/fxRate
        except Exception:
            return 0.0
    return fxRate
    
def GetFXRateFormatted(salesActivity):
    return FXRateValue(
        salesActivity.Instrument(),
        salesActivity.FXRate()
        )
                
def SetFXRateFormatted(salesActivity, fxRate):
    fxRateValue = FXRateValue(salesActivity.Instrument(), fxRate)
    salesActivity.FXRate(fxRateValue)
    
def GetEvaluator(obj, attr):
    ctx = acm.GetDefaultContext()
    tag = acm.GetGlobalEBTag()
    return acm.GetCalculatedValueFromString(
        obj, ctx, attr, tag)

def GetCalculatedValue(obj, attr):
    try:
        return GetEvaluator(obj, attr).Value()
    except RuntimeError:
        return 0
        
def GetMarketMakingValue(orderBook, columnId):
    try:
        ctx = acm.GetDefaultContext()
        quoteCtx = acm.MarketMaking.CreateQuoteContext(ctx)
        quoteData = quoteCtx.Insert(acm.FQuoteController(orderBook))
        value = quoteData.GetDataSource(columnId, 0).Get()
        quoteCtx.Clear()
        return value
    except RuntimeError:
        return 0
        
def ProposedBidPrice(ins):
    try:
        orderbook = FSheetUtils.OrderBook(ins)
        if orderbook is None:
            return double(GetCalculatedValue(ins, 'pricingPriceFeed'
                ).BestBidPrice().Get())
        return GetMarketMakingValue(orderbook, 'Proposed Bid Price Raw')
    except AttributeError:
        return 0
    
def ProposedAskPrice(ins):
    try:
        orderbook = FSheetUtils.OrderBook(ins)
        if orderbook is None:
            return double(GetCalculatedValue(ins, 'pricingPriceFeed'
                ).BestAskPrice().Get())
        return GetMarketMakingValue(orderbook, 'Proposed Bid Price Raw')
    except AttributeError:
        return 0
        
def IsValidNumber(number):
    try:
        if number.IsKindOf(acm.FDenominatedValue):
            number = double(number)
    except AttributeError:
        pass
    return (type(number) in (int, float, long) and
        not math.isnan(number) and
        not math.isinf(number))
        
def IndexedDiary(diary):
    def IsValidKey(d):
        try:
            datetime.datetime.strptime(d, 
                '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False

    d = {}
    key = None
    try:
        for line in diary.Text().splitlines():
            if line: 
                _key = line[:19]
                if IsValidKey(_key):
                    key = _key
                    d[key] = []
                elif key in d:
                    d[key].append(line)
    except AttributeError:
        pass

    return d
            
def LastDiaryEntry(diary):
    try:
        d = IndexedDiary(diary)
        return ' '.join(d[sorted(d.keys())[-1]])
    except IndexError:
        pass
