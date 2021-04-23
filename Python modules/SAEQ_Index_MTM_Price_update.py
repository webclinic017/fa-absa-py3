'''
Purpose: Changed acm.FIndex to acm.FEquityIndex as part of the 2010.2 upgrade.
Developer: Willie van der Bank
20/08/2011
'''

import ael, acm

def getMarketPrice(ins):
    context = acm.GetDefaultContext()
    sheet_type = 'FDealSheet'
    column_id = 'Instrument Market Price'
    calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)
    calc = calc_space.CalculateValue(ins, column_id)
    return calc.Value().Number()

def update_prices():
    for ins in [i for i in acm.FEquityIndex.Select('') if not i.MtmFromFeed()]:
        price_list = acm.FList()
        price_list.AddAll(ins.Prices().AsList())
        price_list.AddAll(ins.HistoricalPrices().AsList())
        for p in price_list: 
            if p.Day() == acm.Time().DateToday() and p.Market().Name() == 'internal' and p.Settle() == 0.0:
                p_clone = p.Clone()
                p_clone.Settle(getMarketPrice(ins))
                p.Apply(p_clone)
                try:
                    p.Commit()
                    break
                except:
                    ael.log('Could not commit price for ' + ins.Name())
        print(ins.Name())
    print('Success')
                                
update_prices()
