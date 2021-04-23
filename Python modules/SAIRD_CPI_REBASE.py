import ael

def update_prices(factor):
    cpi = ael.Instrument['SACPI']
    hist_prcs = cpi.historical_prices()
    prcs = cpi.prices()    
    print 'UPDATING SACPI HISTORICAL PRICES...................'    
    for p in hist_prcs:
        pc = p.clone()
        pc.ask = pc.ask/factor*100.0
        pc.bid = pc.bid/factor*100.0
        pc.last = pc.last/factor*100.0
        pc.settle = pc.settle/factor*100.0
        try:
            pc.commit()
        except:
            print 'Price not commited on SACPI for date: ', p.day 
    print 'UPDATING SACPI CURRENT PRICES...................'          
    for p in prcs:
        pc = p.clone()
        pc.ask = pc.ask/factor*100.0
        pc.bid = pc.bid/factor*100.0
        pc.last = pc.last/factor*100.0
        pc.settle = pc.settle/factor*100.0
        try:
            pc.commit()
        except:
            print 'Price not commited on SACPI for date: ', p.day
            

def update_initial_price(factor):
    bonds = ael.Instrument.select('instype = "IndexLinkedBond"') # single leg
    swaps = ael.Instrument.select('instype = "IndexLinkedSwap"') # fixed leg with CPI nominal scaling
    print 'UPDATING INDEX LINKED SWAPS INITIAL PRICE...................'    
    for i in swaps:
        for l in i.legs():
            if l.nominal_scaling == 'CPI':
                lc = l.clone()
                lc.initial_index_value = lc.initial_index_value / factor*100.0
                try:
                    lc.commit()
                    #print 'Instrument ', i.insid, ' has been updated'
                except:
                    print 'Instrument ', i.insid, ' has not been updated'
    print 'UPDATING INDEX LINKED BONDS INITIAL PRICE...................'                 
    for i in bonds:
        l = i.legs()[0]
        if l.nominal_scaling == 'CPI':
            lc = l.clone()
            lc.initial_index_value = lc.initial_index_value / factor*100.0
            try:
                lc.commit()
                #print 'Instrument ', i.insid, ' has been updated'
            except:
                print 'Instrument ', i.insid, ' has not been updated'

def update_resets(factor, date):
    bonds = ael.Instrument.select('instype = "IndexLinkedBond"') # single leg
    swaps = ael.Instrument.select('instype = "IndexLinkedSwap"') # fixed leg with CPI nominal scaling
    fdc = ael.Instrument.select('instype = "FreeDefCF"')
    print 'UPDATING INDEX LINKED SWAPS RESETS...................' 
    for i in swaps:
        for l in i.legs():
            if l.nominal_scaling == 'CPI':
                for r in l.resets():
                    if  r.value != 0:
                        #print 'ILS',r.type, l.type, r.day, r.value
                        rc = r.clone()
                        rc.value = rc.value / factor*100.0
                        try:
                            rc.commit()
                        except:
                            print 'Reset not updated for ', i.insid
    print 'UPDATING INDEX LINKED BONDS RESETS...................'             
    for i in bonds:
        l = i.legs()[0]
        if l.nominal_scaling == 'CPI':
            for r in l.resets():
                if r.value != 0:
                    #print 'ILB',r.type, l.type
                    rc = r.clone()
                    rc.value = rc.value / factor*100.0
                    try:
                        rc.commit()
                    except:
                        print 'Reset not updated for ', i.insid
    print 'UPDATING FREEDEFCF RESETS...................'                    
    for i in fdc:
        for l in i.legs():
            for r in l.resets():
                if r.type in ('Return', 'Nominal Scaling') and r.value != 0:
                    
                    #print 'FREEDEFCF',i.insid, r.value, r.type
                    rc = r.clone()
                    rc.value = rc.value / factor*100.0
                    try:
                        rc.commit()
                    except:
                        print 'Reset not updated for ', i.insid
                
#update_initial_price(0.95)


#swaps = ael.Instrument.select('instype = "IndexLinkedSwap"')
#l = swaps[0].legs()[1]
#print l.resets()
#update_resets(1, ael.date_today())


#i= ael.Instrument ['ILN_20111020_3.02']
#l = i.legs()
#print l[0].resets()
ael_variables=[
                ['date', 'Date', 'string', [ael.date_today(), ael.date_today().add_banking_day(ael.Instrument['ZAR'], -1)], ael.date_today(), 0, 0],
                ['factor', 'Factor: ', 'string']            ]

def ael_main(dict):
    date = ael.date(dict["date"])
    factor= float(dict["factor"])
    update_prices(factor)
    update_initial_price(factor)
    update_resets(factor, date)
    print 'COMPLETED...'
