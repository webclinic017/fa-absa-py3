import acm

def get_theo_price(ins):
    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    ins_calcs = ins.Calculation()
    return ins_calcs.TheoreticalPrice(cs).Number()

#indexes = acm.FCommodityIndex.Select('')
markets = acm.FMarketPlace.Select('')

#[variable name, Display Name, Type, Candidate values, Default, mandatory, Multiple, Description , Input Hook, enabled]
ael_variables = [['indexes', 'Instrument priced theoretically', acm.FInstrument, None, None, 1, 1], ['markets', 'Markets', acm.FMarketPlace, markets, None, 1, 1]]#, 'Commodity Ins to Reset price Swaps at Next Future price', None, 1]]

def ael_main(dict):
    theo_indexes = dict['indexes']
    markets = dict['markets']
    commit_count = 0
    for market in markets:
        for ci in theo_indexes:
            SpotPrice = get_theo_price(ci)
            if SpotPrice:
                todays_spot_prices = [p for p in ci.Prices() if p.Market().Name() == market.Name()]# and  p.Day() == acm.Time().DateToday()]
                price = None
                if todays_spot_prices:
                    price = todays_spot_prices[0]
                else:
                    price = acm.FPrice()
                    price.Market(market.Name())
                    price.Day(acm.Time().DateToday())
                    
                price.Instrument(ci)    
                price.Ask(SpotPrice)
                price.Bid(SpotPrice)
                price.Last(SpotPrice)
                price.Settle(SpotPrice)
                price.Currency(ci.Currency().Name())
                
                try:
                    price.Commit()
                except Exception, e:
                    acm.Log('Price did not commit for %s | %s' % (ci.Name(), e))
                else:
                    commit_count += 1
            if commit_count == len(theo_indexes):
                acm.Log('Completed Successfully' )
        
