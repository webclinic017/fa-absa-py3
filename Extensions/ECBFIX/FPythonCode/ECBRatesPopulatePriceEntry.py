from __future__ import print_function
""" 
    Script for downloading ECBFIX FX rates. 
    This module contains code for retrieving current or creating
    new prices as well as populating them.
                                                                  """
import acm

def GetPriceEntry(ins, curr, mkt, overwrite):
    if not ins or not curr or not mkt:
        return None
    for price in ins.Prices(): #Latest prices
         if price.Currency() == curr and price.Market() == mkt:
            if overwrite: #User can choose to not overwrite existing prices
                return price
            return None
    
    return NewPrice(ins, curr, mkt)

def GetPriceEntryHist(ins, curr, mkt, day, overwrite):
    if not ins or not curr or not mkt or not day:
        return None
    qry = acm.CreateFASQLQuery('FPrice', 'AND')
    qry.AddAttrNode('Instrument.Name', 'EQUAL', ins.Name())
    qry.AddAttrNode('Currency.Name', 'EQUAL', curr.Name())
    qry.AddAttrNode('Market.Name', 'EQUAL', mkt.Name())
    qry.AddAttrNode('Day', 'EQUAL', str(day))

    if qry.Select().Size() > 0:
        if overwrite:
            return qry.Select()[0]
        return None
    return NewPrice(ins, curr, mkt)

def NewPrice(ins, curr, mkt):
    price = acm.FPrice()
    price.Instrument(ins)
    price.Currency(curr)
    price.Market(mkt)
    return price

def GetMarket(mktName,fullName=None):
    if acm.FMarketPlace[mktName]:#Market exists
        return acm.FMarketPlace[mktName] 
    #Create new market
    mkt = acm.FMarketPlace()
    mkt.Name(mktName)
    if fullName:
        mkt.FullName(fullName)
    mkt.NotTrading(True)
    mkt.Commit()
    return mkt

def GetCurrencyIns(currName, createIfNotExist):
    if acm.FCurrency[currName]:
        return acm.FCurrency[currName]
    if not createIfNotExist:
        return None
    #CREATE CURRENCY INSTRUMENT: Currently a clone of the EUR instrument
    ins = acm.FCurrency['EUR'].Clone()
    ins.Name(currName)
    try:
        ins.Commit()
        return ins
    except Exception as e:
        print ('Unsuccessful creation of currency ', currName, '. Error message: ', e)
    return None

def PopulatePriceEntry(day, fxRatesDict, addNewCurrencies = False, addHistRates = False, overwrite = False):
    ins = GetCurrencyIns('EUR', False)
    if not ins or not acm.Time.IsValidDateTime(day):
        return None
    
    market = GetMarket('ECBFIX')
    if addHistRates:
        PopulateHistoricalPriceEntry(day, ins, fxRatesDict, market, addNewCurrencies, overwrite)
    else:
        PopulateLatestPriceEntry(day, ins, fxRatesDict, market, addNewCurrencies, overwrite)

def PopulateLatestPriceEntry(day, ins, fxRatesDict, mkt, addNewCurrencies, overwrite):
    for fxrate in fxRatesDict:
        curr = GetCurrencyIns(fxrate[0], addNewCurrencies)
        if not curr:
            continue

        entry = GetPriceEntry(ins, curr, mkt, overwrite)
        if not entry:
            continue

        #Set to today's date first and then update to not add to hist. prices (if not today's date)
        if day != acm.Time.DateNow():
            entry.Day(acm.Time.DateNow())
            entry.Commit()

        entry.Settle(fxrate[1])
        entry.Last(fxrate[1])
        entry.Day(day)
        try:
            entry.Commit()
        except Exception as e:
            print ('Exception occurred when saving price. ', e)

def PopulateHistoricalPriceEntry(day, ins, fxRatesDict, mkt, addNewCurrencies, overwrite):
    for fxrate in fxRatesDict:
        curr = GetCurrencyIns(fxrate[0], addNewCurrencies)
        if not curr:
            continue
        if day == acm.Time.DateNow():
            entry = GetPriceEntry(ins, curr, mkt, overwrite)
        else:
            entry = GetPriceEntryHist(ins, curr, mkt, day, overwrite)
        if not entry:
            continue

        entry.Settle(fxrate[1])
        entry.Last(fxrate[1])
        entry.Day(day)
        try:
            entry.Commit()
        except Exception as e:
            print ('Exception occurred when saving price. ', e)
