'''----------------------------------------------------------------------------------------------------------------
DESCRIPTION
    Date                : 2013-10-28
    Purpose             : Updates historical spot prices for instruments based on date and market inputs 
    
    History
        2013-10-xx  Christo     created
        2013-11-13  Martin      extended to be able to use "today" and "yesterday" as input
ENDDESCRIPTION
----------------------------------------------------------------------------------------------------------------'''

import acm, FBDPGui, ael

TODAY = acm.Time.DateNow()


#----------------------------------------------------------------------------------------------------------------
#A function to get all the instruments with a price in the from_market in last price table
#----------------------------------------------------------------------------------------------------------------
def Get_Instruments(market, fromDate, from_pricetable):

    #pricetable = 'LastPrice'
    #if market.Type() == 'MtM Market':
    #pricetable = 'Price'
    print (from_pricetable, market.Name(), fromDate)
    query2 = """
        select
        i.insid 'Instrument',
        i.instype,
        i.exp_day,
        i.insaddr
    from
        Instrument i,
        %s lp,
        party p
        
    where
    i.insaddr = lp.insaddr
    and lp.ptynbr = p.ptynbr
    and p.ptyid = '%s'
    and day = '%s'
   
   
    group by 1
    
    """ % (from_pricetable, market.Name(), fromDate)
    print query2
    
    Instruments = acm.FArray()
    ins2 = ael.asql(query2)
    print ins2
    for i in ins2[1][0]:
        if i[0] not in Instruments:
            Instruments.Add(i[0])
    return Instruments

#----------------------------------------------------------------------------------------------------------------
#A function to get the existing price of an instrument given a date
#----------------------------------------------------------------------------------------------------------------
def Get_Existing_Price(instrument, fromDate, curr, market, all_last_prices, all_hist_prices):
    i = acm.FInstrument[instrument]
    
    if fromDate == TODAY:
        all_prices = all_last_prices
    else:
        all_prices = all_hist_prices
    
    for price in all_prices:
        if price.Market() != None:
            if price.Market().Name() == market.Name() and price.Day() == fromDate and price.Currency() == curr:
                return price

#----------------------------------------------------------------------------------------------------------------
#A function to set the new price of an instrument for a given date
#----------------------------------------------------------------------------------------------------------------
def Set_New_Price(instrument, existingPrice, fromDate, newDate, new_price_market, all_last_prices, all_hist_prices):
    price_exists = False
    i = acm.FInstrument[instrument]
    
    if newDate == TODAY:
        all_prices = all_last_prices
    else:
        all_prices = all_hist_prices
    
    for latestPrice in all_prices:
        if latestPrice.Market() != None:            
            if latestPrice.Market().Name() == new_price_market.Name() and existingPrice.Currency() == latestPrice.Currency() :
            
                #only care about the date when it is a historical price.
                if newDate <> TODAY and latestPrice.Day() <> newDate :
                    continue
            
                price_exists = True
                if latestPrice.Settle() != existingPrice.Settle():
                    oldLatestSettlePrice = latestPrice.Settle()
                    latestPrice.Bid(existingPrice.Bid())
                    latestPrice.Ask(existingPrice.Ask())
                    latestPrice.Settle(existingPrice.Settle())
                    latestPrice.Last(existingPrice.Last())
                    latestPrice.Day(newDate)
                    try:
                        latestPrice.Commit()
                        print 'Updated %s %s for %s successfully. Changed from %s to %s.' % (newDate, new_price_market.Name(), i.Name(), oldLatestSettlePrice, latestPrice.Settle())
                    except Exception as e:
                        print 'Could not copy %s SPOT to %s %s for %s: %s' % (fromDate, newDate, new_price_market.Name(), i.Name(), e)
                        
    #create new price if it doesnt exist for the instrument for the newDate
    if not price_exists:
        try:
            
            instrumentPrice = acm.FPrice()
            instrumentPrice.Day(newDate)
            instrumentPrice.Instrument(i)
            instrumentPrice.Market(new_price_market)
            instrumentPrice.Currency(existingPrice.Currency())
            instrumentPrice.Settle(existingPrice.Settle())
            instrumentPrice.Bid(existingPrice.Bid())
            instrumentPrice.Ask(existingPrice.Ask())
            instrumentPrice.Last(existingPrice.Last())
            instrumentPrice.Commit()
            
            print 'Created %s %s for %s.' % (newDate, new_price_market.Name(), i.Name())
        except Exception as e:
            print 'Error in setting instrument %s %s price for instrument %s: %s' % (newDate, new_price_market.Name(), i.Name(), e)
        
def goforit(fromDate, newDate, new_price_market, from_market, from_pricetable):
    
    instrumentList = Get_Instruments(from_market, fromDate, from_pricetable)
    print 'copy prices for %s instruments' %len(instrumentList)
    
    for instrument in instrumentList:
        i = acm.FInstrument[instrument]
        currs = {}
        for p in i.Prices():
            currs[p.Currency()] = 1
            
            
        all_last_prices = i.Prices()
        all_hist_prices = i.HistoricalPrices()
            
        for curr in currs:    
            existingPrice = Get_Existing_Price(instrument, fromDate, curr, from_market, all_last_prices, all_hist_prices)
            if existingPrice:
                Set_New_Price(instrument, existingPrice, fromDate, newDate, new_price_market, all_last_prices, all_hist_prices)
                #print instrument,existingPrice,fromDate,newDate
            else:
                pass
                #print 'Could not find %s SPOT for %s.' % (fromDate,instrument)
    print 'DONE'

def interpret(str):
    if str.upper() == 'TODAY':
        return TODAY
    if str.upper() == 'YESTERDAY':
        return acm.Time.DateAddDelta(TODAY, 0, 0, -1)
    return str

markets = []
for m in acm.FMarketPlace.Select(''):
    markets.append(m.Name())
for m in acm.FMTMMarket.Select(''):
    markets.append(m.Name())
    
# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = FBDPGui.LogVariables(
                ['FromDate', 'From Date', 'string', None, acm.Time.DateAddDelta(TODAY, 0, 0, -1), 1, 0, 'Date of the Price that is used to update the new price', None, 1],
                ['FromMarket', 'From Market', 'string', markets, 'SPOT', 0, 0, 'Name of the source market', None, 1],
                ['FromTable', 'From Table', 'string', ['LastPrice', 'Price'], 'Price', 0, 0, 'Select from Price or Price hist', None, 1],
                
                ['NewDate', 'New Date', 'string', None, TODAY, 1, 0, 'Date of new price that needs to be updated.', None, 1],
                ['NewMarket', 'New Market', 'string', markets, 'SPOT', 0, 0, 'Name of the target market', None, 1])

def ael_main(dictionary):
    fromDate = interpret(dictionary['FromDate'])
    newDate =  interpret(dictionary['NewDate'])
    from_pricetable =  interpret(dictionary['FromTable'])
    
    
    
    new_price_market = acm.FParty[dictionary['NewMarket']]
    from_market = acm.FParty[dictionary['FromMarket']]
    goforit(fromDate, newDate, new_price_market, from_market, from_pricetable)
