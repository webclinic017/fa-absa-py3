"""
Date                  :2015/10/06
Purpose               :Task to copy currency prices from price entry table
Requester             :Market Risk (LUM/Omega Project)
Original Developer    :Zinhle Ndlela & Fancy Dire
CR Number             :Original CR not available
Date           Developer                       Change     Description
2015/10/06     Zinhle Ndlela & Fancy Dire      Create
---------------------------------------------------------------------------------"""

import acm, ael
import FRunScriptGUI
from os.path import join

excluded_currencies = ["TND",
                       "IDR",
                       "MCU",
                       "XRH"]

fx_rates_calculation_space = acm.FStandardCalculationsSpaceCollection()
zar_reference_currency = acm.FCurrency["USD"]
today = acm.Time().DateToday()

currencies = []
fx_rates = []

folder_selection = FRunScriptGUI.DirectorySelection()

ael_variables = [
                ['filepath', 'Path', folder_selection, None, folder_selection, 1, 1, "Path to which text file will be written to."]
                ]

    
def get_Price_Entry_Price(temp, curr1, curr2, date, market, *rest):

    settlePrice = 0
    
    if curr1 == curr2:
        return 1, acm.FCurrency[curr1], 'currency'
    
    currPair = curr1 + '/' + curr2
    #print currPair
    currencyPair = acm.FCurrencyPair[currPair]
    if not currencyPair:
        currPair = curr2 + '/' + curr1
        currencyPair = acm.FCurrencyPair[currPair]

    if not currencyPair:
        curr1 = acm.FCurrency[curr1]
        curr2 = acm.FCurrency[curr2]
        date = ael.date(date)
        prices = get_Price_Entry_History(temp, curr1, curr2, date, market)
        return settlePrice, None, 'noCurrencyPair'
    
    try:
        date = ael.date(date)
    except:
        date = date
    
    currPairCurr1 = currencyPair.Currency1()
    currPairCurr2 = currencyPair.Currency2()
    
    #Retreive rates from Price Table for the date specified.
    prices = get_Price_Entry_History(temp, currPairCurr1, currPairCurr2, date, market)

    if len(prices) == 0:
        #No price exist for the specific date. Retreive last price.
        prices = get_Price_Entry_Last(temp, currPairCurr1, currPairCurr2, market)
    
    if len(prices) > 0:
        settlePrice = prices[0].Bid()
    return settlePrice, currencyPair, 'currencyPair'
    
def get_Price_Entry_Last(temp, curr1, curr2, market, *rest):
    prices = acm.FArray()
    for price in curr1.Prices():
        if price.Market() and price.Market().Name() == market and price.Currency() and price.Currency().Name() == curr2.Name():
            prices.Add(price)
    return prices

def get_Price_Entry_History(temp, curr1, curr2, date, market, *rest):
    print type(date)
    
    priceQuery = acm.CreateFASQLQuery(acm.FPrice, 'AND')
    priceQuery.AddAttrNode('Instrument.Name', 'EQUAL', curr1.Name())
    priceQuery.AddAttrNode('Market.Name', 'EQUAL', market)
    priceQuery.AddAttrNode('Currency.Name', 'EQUAL', curr2.Name())
    priceQuery.AddAttrNode('Day', 'EQUAL', date.to_string())
    prices = priceQuery.Select().SortByProperty('Day', 0)
    
    if len(prices) == 0:
        prices = get_Price_Entry_Last(temp, curr1, curr2, market)
    
    return prices

def ael_main(ael_dict):

    global excluded_currencies
    global today

    for curr in acm.FCurrency.Select(""):
        curr_name = curr.Name()
        #print curr_name
        if curr_name in excluded_currencies:
            continue

        #currencies.append(curr_name)
        price = get_Price_Entry_Price(None, "USD", curr_name, today, 'SPOT')
        if price[1] != None and price[0] != 0 and str(price[0]).lower() != 'nan':
            currencies.append(curr_name)
            #print 'Fancy:',price[1].Name(),str(price[0]),str(price[0])=='nan'
            if price[1].Name().startswith('USD'):
                fx_rates.append(str(price[0]))
            else:
                if price[0] == 0:
                    fx_rates.append('0')
                else:
                    fx_rates.append(str(1/price[0]))
        #rate_in_zar = zar_reference_currency.Calculation().FXRate(fx_rates_calculation_space, curr, today)
        #fx_rates.append(str(rate_in_zar.Number()))

    print len(currencies), len(fx_rates)
    if len(currencies) < 1:
        print "No currencies found!"
        return None

    filepath = str(ael_dict["filepath"])

    filepath = join(filepath, "Currencies_USD.txt")

    with open(filepath, "w") as rates_file:

        for index in range(len(currencies)):

            rates_file.write(currencies[index] + "|" + fx_rates[index] + "\n")

    print "Wrote secondary output to:", filepath
