import acm

FOX = ('EUR_USD', 'USD_HUF', 'USD_MXN', 'USD_GHS', 'USD_PLN', 'USD_ILS', 
'USD_CZK', 'USD_JPY', 'USD_HKD', 'USD_INR', 'USD_KES', 'USD_MUR', 
'USD_MWK', 'USD_NAD', 'USD_NGN', 'USD_SAR', 'USD_SEK', 'USD_SGD', 
'USD_SZL', 'USD_TRY', 'USD_TZS', 'USD_UGX', 'USD_CHF', 'USD_CNY',
'USD_CAD', 'USD_DKK', 'USD_NOK', 'USD_AOA', 'GBP_USD', 'USD_KWD',
'USD_PKR', 'USD_QAR', 'USD_THB', 'USD_SCR', 'USD_MYR', 'USD_LSL',
'USD_EGP', 'USD_AED', 'AUD_USD', 'USD_ZWD', 'USD_XOF', 'USD_CNH',
'USD_XAF', 'USD_RUB', 'USD_BRL', 'USD_MZN', 'USD_ZMW', 'USD_RON',
'USD_BHD', 'NZD_USD', 'USD_MAD', 'BWP_USD', 'USD_ZAR')

ins = []

PLDs = acm.FPriceLinkDefinition.Select('')
for PLD in PLDs:
    if PLD.PriceDistributor().Name() == 'FOX_PRICING':
        if PLD.Instrument().InsType() == 'Curr' and PLD.Market().Name()=='SPOT_RT':
            if PLD.Instrument().Name()+'_'+PLD.Currency().Name() in FOX:
                ins.append((PLD.Instrument().Name(), PLD.Currency().Name()))



for i in ins:
    todays_SPOT_RT_prices = [p for p in acm.FCurrency[i[0]].Prices() if p.Market().Name() == 'SPOT_RT' and p.Currency().Name() == i[1]]
    if todays_SPOT_RT_prices:
                price = todays_SPOT_RT_prices[0]
    else:
                price = acm.FPrice()
                price.Market('SPOT_RT')
                price.Day(acm.Time().DateToday())
    

    price.Instrument(i[0])    
    price.Ask(3.0)
    price.Bid(1.0)
    price.Last(2.0)
    price.Settle(2.0)
    price.Currency(i[1])
    
    try:
        price.Commit()
        print('unit value did commit for    ', i)
    except:
        print('Price did not commit for   ', i) 

    
    

            
            

