import ael, acm

def add_price(p, d):
    pc = acm.FPrice()
    #print p
    pc.Instrument = p.Instrument()
    pc.Market = p.Market()
    pc.Currency = p.Currency()
    pc.Day = ael.date(d)
    pc.Bid = p.Bid()
    pc.Ask = p.Ask()
    pc.Settle = p.Settle()
    pc.Last = p.Last()
    try:
        pc.Commit()
        return ' success '
    except:
        print('did not commit', p.Instrument().Name(), d)
        return ' ERROR '

def add_price_sob(p, d):
    m = acm.FParty['SPOT_SOB']
    pc = acm.FPrice()
    pc.Instrument = p.Instrument()
    pc.Market = m
    pc.Currency = p.Currency()
    pc.Day = ael.date(d)
    pc.Bid = p.Bid()
    pc.Ask = p.Ask()
    pc.Settle = p.Settle()
    pc.Last = p.Last()
    
    try:
        pc.Commit()
        return ' success '
    except:
        #print 'did not commit', p.Instrument().Name(), d
        
        return ' ERROR '

def spot(temp, ins, *rest):
    i = acm.FInstrument[ins.insid]
    #print i.Name()
    p = acm.FParty['SPOT']
    err = '-'
    #d = ael.date('2008-12-05')
    
    s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-06")
    if len(acm.FPrice.Select(s)) == 0:
        s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-05")
        count = 0
        while count < len(acm.FPrice.Select(s)):
            bprc = acm.FPrice.Select(s).At(count)
            err = err + add_price(bprc, "2008-12-06")
            count = count + 1
        
    s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-07")
    if len(acm.FPrice.Select(s)) == 0:
        s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-06")
        count = 0
        while count < len(acm.FPrice.Select(s)):
            bprc = acm.FPrice.Select(s).At(count)
            err = err + add_price(bprc, "2008-12-07")
            count = count + 1
       
    s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-08")
    if len(acm.FPrice.Select(s)) == 0:
        s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-07")
        count = 0
        while count < len(acm.FPrice.Select(s)):
            bprc = acm.FPrice.Select(s).At(count)
            err = err + add_price(bprc, "2008-12-08")
            count = count + 1
      
    s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-09")
    if len(acm.FPrice.Select(s)) == 0:
        s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-08")
        count = 0
        while count < len(acm.FPrice.Select(s)):
            bprc = acm.FPrice.Select(s).At(count)
            err = err + add_price(bprc, "2008-12-09")
            count = count + 1
        
    s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-10")
    if len(acm.FPrice.Select(s)) == 0:
        s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-09")
        count = 0
        while count < len(acm.FPrice.Select(s)):
            bprc = acm.FPrice.Select(s).At(count)
            err = err + add_price(bprc, "2008-12-10")
            count = count + 1
        
    print(i.Name(), err)  
    return err
#i = ael.Instrument['ZAR-USD/C/UI/7.8/081224']

#print testins(1,i)


def sob(temp, ins,*rest):
    i = acm.FInstrument[ins.insid]
    print(i.Name())
    p = acm.FParty['SPOT_SOB']
    spot = acm.FParty['SPOT']
    err = '-'
    s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-06")
    if len(acm.FPrice.Select(s)) == 0:
        s = "instrument = %i and market = %i and day = %s" %(i.Oid(), spot.Oid(), "2008-12-05")
        count = 0
        while count < len(acm.FPrice.Select(s)):
            bprc = acm.FPrice.Select(s).At(count)
            if bprc:
                err = err + add_price_sob(bprc, "2008-12-06")
            else:
                print('no price for 2008-12-05')
            count = count + 1
            
    s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-07")
    if len(acm.FPrice.Select(s)) == 0:
        s = "instrument = %i and market = %i and day = %s" %(i.Oid(), spot.Oid(), "2008-12-06")
        count = 0
        while count < len(acm.FPrice.Select(s)):
            bprc = acm.FPrice.Select(s).At(count)
            if bprc:
                err = err + add_price_sob(bprc, "2008-12-07")
            else:
                print('no price for 2008-12-06')
            count = count + 1
       
    s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-08")
    if len(acm.FPrice.Select(s)) == 0:
        s = "instrument = %i and market = %i and day = %s" %(i.Oid(), spot.Oid(), "2008-12-07")
        count = 0
        while count < len(acm.FPrice.Select(s)):
            bprc = acm.FPrice.Select(s).At(count)
            if bprc:
                err = err + add_price_sob(bprc, "2008-12-08")
            else:
                print('no price for 2008-12-07')
            count = count + 1
            
    s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-09")
    if len(acm.FPrice.Select(s)) == 0:
        s = "instrument = %i and market = %i and day = %s" %(i.Oid(), spot.Oid(), "2008-12-08")
        count = 0
        while count < len(acm.FPrice.Select(s)):
            bprc = acm.FPrice.Select(s).At(count)
            if bprc:
                err = err + add_price_sob(bprc, "2008-12-09")
            else:
                print('no price for 2008-12-08')
            count = count + 1
            
    s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-10")
    #print acm.FPrice.Select(s)
    if len(acm.FPrice.Select(s)) == 0:
        s = "instrument = %i and market = %i and day = %s" %(i.Oid(), spot.Oid(), "2008-12-09")
        count = 0
        while count < len(acm.FPrice.Select(s)):
            bprc = acm.FPrice.Select(s).At(count)
            if bprc:
                err = err + add_price_sob(bprc, "2008-12-10")
            else:
                print('no price for 2008-12-09')
            count = count + 1
    return err
    
def needprice(temp, ins,*rest):
    
    #i = acm.FInstrument['ZAR-USD/C/UI/7.8/081224']
    #i = acm.FInstrument['ZAR']
    i = acm.FInstrument[ins.insid]
    #print i.Name()
    p = acm.FParty['SPOT']
    #d = ael.date('2008-12-05')
    s = "instrument = %i and market = %i and day = %s" %(i.Oid(), p.Oid(), "2008-12-05")
    #s = "instrument = %i and market = %i " %(i.Oid(), p.Oid())
    #for p in acm.FPrice.Select(s):
    #    print p
   
    if len(acm.FPrice.Select(s)) > 0:
        #print 'needs to be updated'
        return 1
    else:
        #print 'no update'
        return 0
        
    
#needprice(1,2)
#sob(1, i = ael.Instrument['ZAR-USD/C/UI/7.8/081224'])
#sob(1, i = ael.Instrument['ZAR/BIL'])
