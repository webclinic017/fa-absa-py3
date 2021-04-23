'''
Purpose:                Uploads YIELDX prices from external file for Currency Future/Forwards and trurn the Mtm From Feed on.
Department and Desk:    Middle Office
Requester:              Khunal Ramesar
Developer:              Heinrich Cronje
CR Number:              C581033

History:
When:       CR Number:      Who:                    Requester:              What:
            C732121         Heinrich Cronje         Jan Kotze               Added CHF Currency to be divided.
2012-07-06  C318884         Nidheesh Sharma                                 Added a condition to the if statement to prevent the rates and prices from changing for MTM instruments.
2013-08-22  C1270650        Peter Fabian            JP Potgieter            Added support for inverted quotation (Rand/CCY) instruments
2014-03-04  CHNG0001779667  Peter Basista           JP Potgieter            Fixed and cleaned-up the code of getRate function.
'''

import acm
import ael
import SAGEN_IT_Functions as Utils

def openFile(filename):
    try:
        file = open(filename, 'r')
        return file
    except Exception, e:
        print e
        return None

def closeFile(file):
    try:
        file.close()
    except Exception, e:
        print e
        
def loadData(file):
    line = file.readline()
    line = file.readline()
    dict = {}
    while line <> '':
        l = line.split(',')
        key = l[1].replace('"', '') + l[2].replace('"', '')
        dict[key] = float(l[5])
            
        line = file.readline()
        
    return dict

def selectInstruments(date):
    instrumentQuery = acm.CreateFASQLQuery(acm.FInstrument, 'AND')
    instrumentQuery.AddAttrNode('InsType', 'EQUAL', Utils.GetEnum('InsType', 'Future/Forward'))
    instrumentQuery.AddAttrNode('UnderlyingType', 'EQUAL', Utils.GetEnum('InsType', 'Curr'))
    instrumentQuery.AddAttrNode('ExpiryDate', 'GREATER_EQUAL', acm.Time().AsDate(date))
    ins = instrumentQuery.Select()

    return ins

def getRate(acm_instrument, exchange_rates):
    """
    Look up and return an estimated exchange rate
    between the instrument's currency
    and the currency of its underlying instrument.
    The returned exchange rate should be valid for the instrument's
    expiry date adjusted using the spot days offset
    of the underlying instrument.
    The available exchange rate estimations against USD
    should be present in the provided dictionary exchange_rates.
    """
    expiry_date = acm.Time().AsDate(acm_instrument.ExpiryDate())
    expiry_date_adjusted = acm_instrument.Currency().Calendar().\
        AdjustBankingDays(expiry_date,
        acm_instrument.Underlying().SpotBankingDaysOffset())
    currency = acm_instrument.Currency().Name()
    underlying_currency = acm_instrument.Underlying().Currency().Name()
    try:
        # exchange rate for the instrument's currency.
        currency_rate = exchange_rates[expiry_date_adjusted + currency]
    except KeyError as e:
        print ("Warning: Can not look up an exchange rate "
            "for currency '{0}' and date '{1}'.\n"
            "Error message: {2}").format(currency,
            expiry_date_adjusted, e)
        # If the lookup fails, we want the returned rate to be zero.
        return 0
    try:
        # Exchange rate for the underlying instrument's currency.
        underlying_currency_rate = exchange_rates[
            expiry_date_adjusted + underlying_currency]
    except KeyError as e:
        print ("Warning: Can not look up an exchange rate "
            "for currency '{0}' and date '{1}'.\n"
            "Error message: {2}").format(underlying_currency,
            expiry_date_adjusted, e)
        # If the lookup fails, we want the returned rate to be zero.
        return 0
    # The convention is that the following four currencies
    # have higher priority than the USD.
    high_priority_currencies = ('EUR', 'GBP', 'AUD', 'NZD')
    # All the remaining currencies have lower priority.
    # In order to be able to calculate the resulting exchange rate,
    # we need consistency in the exchange rates against USD.
    # So, we need to make sure that all of them are based on USD.
    # In other words, we will make USD the currency with the highest priority.
    if currency in high_priority_currencies:
        currency_rate = 1 / currency_rate
    if underlying_currency in high_priority_currencies:
        underlying_currency_rate = 1 / underlying_currency_rate
    # We get the final exchange rate by comparing (dividing)
    # the two obtained, USD-based exchange rates.
    # It is important to note that typically, we are interested
    # in the exchange rate based on the underlying instrument's currency.
    # But if the inverted quotation type is used, then we are looking for
    # an exhange rate based on the main instrument's currency.
    if acm_instrument.Quotation().QuotationType() == "Per Unit Inverse":
        rate = underlying_currency_rate / currency_rate 
    else:
        rate = currency_rate / underlying_currency_rate
    return rate

def amendPrice(price, newRate, date):
    price.Last(newRate)
    price.Settle(newRate)
    price.Ask(newRate)
    price.Bid(newRate)
    price.Day(date)
    try:
        price.Commit()
        print "%s: %s price committed" % (price.Instrument().Name(), newRate)
    except Exception, e:
        print e

def createPrice(ins, newRate, date):
    priceNew = acm.FPrice()
    priceNew.Last(newRate)
    priceNew.Settle(newRate)
    priceNew.Ask(newRate)
    priceNew.Bid(newRate)
    priceNew.Day(date)
    priceNew.Instrument(ins)
    priceNew.Market(acm.FParty['SPOT'])
    priceNew.Currency(ins.Currency())
    try:
        priceNew.Commit()
        print "%s: %s price created" % (ins.Name(), newRate)
    except Exception, e:
        print e

def changePrice(ins, newRate, date):
    price = None
    prices = ins.Prices()
    if prices:
        for p in prices:
            if p.Market().Name() == 'SPOT':
                price = p
                
        if price:
            amendPrice(price, newRate, date)
        else:
            createPrice(ins, newRate, date)
    else:
        createPrice(ins, newRate, date)

def turnMtmOn(ins):
    if not ins.MtmFromFeed():
        ins.MtmFromFeed(1)
        try:
            ins.Commit()
            print 'MTM From Feed turned on : ' + ins.Name()
        except Exception, e:
            print e

ael_variables = [('date', 'Date', 'string', None, str(ael.date_today()), 1),
                 ('path', 'File Path', 'string', None, 'Y:\Jhb\FAReports\AtlasEndOfDay\LIVEXPF\\', 1),
                 ('name', 'File Name', 'string', None, 'pfmidmlp_eod.txt', 1)]
                 
def ael_main(dict):
    date = dict['date']
    filename = dict['path'] + date + '/' + dict['name']
    file = openFile(filename)
    if file:
        data = loadData(file)
        closeFile(file)
        
        ins = selectInstruments(date)
        for i in ins:
            if 'YIELDX' in i.Name() and i.Name()[-4:] != '/MTM':
                newRate = getRate(i, data)
                changePrice(i, newRate, date)
                turnMtmOn(i)
