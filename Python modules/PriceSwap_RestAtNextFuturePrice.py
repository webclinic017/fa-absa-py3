'''
Date                    : 2014-07-29
Purpose                 : Scipt that commits the nearest futures price of a price swap floating price commodity
                          to a new commodity for fixing purposes
Departmentand desk      : Credit Risk Trading
Rquester                : Mofokeng, Victor: ABSA (JHB)
Developer               : Anil Parbhoo
Code Review             : Andreas Bayer
CR Number               : CHNG0002158077

'''

import acm

def benchmarks_futures_of_mapped_price_curve(ins):
    bm_list = []
    string_for_context = "context = %s" %'ACMB Global'
    global_context = acm.FContextLink.Select(string_for_context)
    for m in global_context:
        if m.Type() == 'Price Curve':
            if m.MappingType() == 'Instrument':
                if (m.Instrument().Name() == ins.Name()) and (m.Currency().Name()== ins.Currency().Name()):
                    yc = acm.FYieldCurve[m.Name()]
                    print 'mapped Price Swap YC for', ins.Name(), 'is = ', yc.Name()
                    bms = yc.Benchmarks()
                    for bm in bms:
                        if bm.Instrument().InsType() == 'Future/Forward' and bm.Instrument().ExpiryDateOnly() >= acm.Time().DateToday():
                            bm_list.append(bm.Instrument())
    return bm_list

def get_spot_price(ins):
    for p in ins.Prices():
        if (p.Market().Name() == 'SPOT') and (p.Currency().Name()== ins.Currency().Name()):
            return p.Settle()


comm_ins = acm.FCommodity.Select('')

#[variable name, Display Name, Type, Candidate values, Default, mandatory, Multiple, Description , Input Hook, enabled]
ael_variables = [['comm_ins_RaNF', 'Commodity Ins to Reset at Next Future', acm.FCommodity, comm_ins, None, 1, 1]]#, 'Commodity Ins to Reset price Swaps at Next Future price', None, 1]]

def ael_main(dict):
    
    comms_for_reset = dict['comm_ins_RaNF']
    #print 'number of comms_for_reset = ', len(comms_for_reset)
    commit_count = 0
    for new_comm in comms_for_reset:
        dates = []
        org_comm = acm.FCommodity[new_comm.ExternalId1()]
        
        print 'new comm = ', new_comm.Name(), 'org comm name = ', org_comm.Name()

        comm_future_ins = benchmarks_futures_of_mapped_price_curve(org_comm)
        
        for f in comm_future_ins:
            
            if f.ExpiryDateOnly()>= acm.Time().DateToday():
                
                dates.append(f.ExpiryDateOnly())
        
       
        next_futures_date = min(dates)
        print 'next/nearest futures date', next_futures_date
        
        for f in comm_future_ins:
            if f.ExpiryDateOnly() == next_futures_date:
                SpotPrice = get_spot_price(f)
                print 'nearest future is ', f.Name(), 'that has expiry date =  ', f.ExpiryDateOnly(), 'and a market price of = ', SpotPrice
        
        
        todays_spot_prices = [p for p in new_comm.Prices() if p.Market().Name() == 'SPOT' and  p.Day() == acm.Time().DateToday()]
        #acm.Log('There already exists %s SPOT prices for today for %s' % (len(todays_spot_prices),new_comm.Name()))
        price = None
        if todays_spot_prices:
            price = todays_spot_prices[0]
        else:
            price = acm.FPrice()
            price.Market('SPOT')
            price.Day(acm.Time().DateToday())
            
        price.Instrument(new_comm)    
        price.Ask(SpotPrice)
        price.Bid(SpotPrice)
        price.Last(SpotPrice)
        price.Settle(SpotPrice)
        price.Currency(new_comm.Currency().Name())
        
        try:
            price.Commit()
        except:
            acm.Log('Price did not commit for' + new_comm.Name())
        else:
            commit_count += 1
            
   
        print '==============='
        
    if commit_count == len(comms_for_reset):
        acm.Log('completed successfully' )
