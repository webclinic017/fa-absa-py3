
#Date:                   2010-03-19

#Purpose:                Scale price for safex variance swaps so that when they are discounted the result is the correct original price

#Department and Desk:    FO Equities

#Requester:              Andrey Chechin

#Developer:              Zaakirah kajee

#CR Number:              259002







import acm, ael

today = acm.Time().DateToday()
safex_vswaps = acm.FVarianceSwap.Select("otc = 0")
from zak_funcs import write_file
prod = '//services/frontnt/BackOffice/Atlas-End-Of-Day/' +  ael.date_today().to_string('%Y-%m-%d') + '/'

data = [['INSTRUMENT', 'OLD PRICE', 'NEW PRICE', 'DISCOUNT FACTOR']]
for vswap in safex_vswaps:

    if vswap.ExpiryDateOnly() >= today:
        spot = vswap.Currency().Calendar().AdjustBankingDays(today, vswap.SpotBankingDaysOffset())
        expspot = vswap.Currency().Calendar().AdjustBankingDays(vswap.ExpiryDate(), vswap.SpotBankingDaysOffset())
        zarswap = acm.FYieldCurve['ZAR-SWAP']
        df=  zarswap.IrCurveInformation().Rate(today, expspot, 'Discount', 'None', 'Discount', None, 0)
        for p in vswap.HistoricalPrices():
            if p.Day() == today:
                op = p.Settle()
                p.Settle(p.Settle()/df)
                try:
                    
                    p.Commit()
                    data.append([vswap.Name(), op, p.Settle(), df])
                except:
                    data.append([vswap.Name(), 'ERROR', 'ERROR', 'ERROR'])
                    acm.Log('ERROR: VAR SWAP PRICE NOT COMMITED FOR '+ vswap.Name())
if len(data) > 1:
    write_file(prod + 'SAEQ_VARSWAP_SAFEX_DAILYPRICE.csv', data)
    #write_file('f://varswaps.csv', data)
