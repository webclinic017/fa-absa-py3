import ael

'''
Purpose:        Copies todays price to SPOT_MID
Developer:      Manan Ghosh
Date:           August 2013

History:
When:   CR Number:      Who:                    Requester:
2013-09-30              Martin Spoerri          Amended for Africa instance
--------------------------------------------------------------------------
'''

def PriceCopy(i):
 
    today = ael.date_today()
    spotmid = {}
    spot = {}

    midflag = {}
    
    for p in i.prices():
        if p.ptynbr != None and p.day <= i.maturity_date:
            
            if p.ptynbr.ptyid == 'SPOT_MID':
                spotmid[p.curr.insid] = p
                    
            if p.ptynbr.ptyid == 'SPOT':
                if p.day == ael.date_today():
                    spot[p.curr.insid] = p
         
    for curr in spot:
        
        mid_clone = None        
        if curr in spotmid and spotmid[curr]:
            if spot[curr]:  
                mid_clone = spotmid[curr].clone()
                settle = (spot[curr].settle and spot[curr].settle != 0.0) and spot[curr].settle or spot[curr].last
                ask = (spot[curr].ask and spot[curr].ask != 0.0) and spot[curr].ask or settle
                bid = (spot[curr].bid and spot[curr].bid != 0.0) and spot[curr].bid or settle
                mid = (ask + bid)/ 2
                mid_clone.bid = mid
                mid_clone.ask = mid
                mid_clone.settle = mid
                mid_clone.last = mid
                mid_clone.day = ael.date_today()  
            else:
                print 'No SPOT prices  for Instrument [%s] in currency %s' % (i.insid, curr)
                
        else:
            if spot[curr]:
                mid_clone = spot[curr].new()
                mid_clone.ptynbr = ael.Party['SPOT_MID'] 
                settle = (spot[curr].settle and spot[curr].settle != 0.0) and spot[curr].settle or spot[curr].last
                ask = (spot[curr].ask and spot[curr].ask != 0.0) and spot[curr].ask or settle
                bid = (spot[curr].bid and spot[curr].bid != 0.0) and spot[curr].bid or settle
                mid = (ask + bid)/ 2
                mid_clone.bid = mid
                mid_clone.ask = mid
                mid_clone.settle = mid
                mid_clone.last = mid            
                mid_clone.day = ael.date_today()
            else:
                print 'No SPOT prices  for Instrument [%s] in currency %s' % (i.insid, curr)
            
        try:
            if mid_clone != None:
                mid_clone.commit()
                
                print 'MID Price created/updated for Instrument[%s]' %(i.insid)
        except:
            print 'Not able to copy SPOT price to MID price for Instrument [%s] in currency %s' % (i.insid, curr)
            
    
    return True
    
  
ael_variables = []

def ael_main(args):

    print 'Copy Mid Price rerun...'
    '''
    sql = """select 
        i.insaddr,
        p.data[3]
    
        from
            PriceDefinition p,
            Instrument i
        where
            p.insaddr = i.insaddr 
        """

    print 'Found', len(ael.asql(sql,1)[1][0]), 'Prices'
    for (ins,data) in ael.asql(sql,1)[1][0]:
        #if data != '':
        PriceCopy(ins)
    '''
     
    import acm
    TODAY = acm.Time().DateToday()
    prices_all = acm.FPrice.Select('market = "SPOT"')
    prices = [p for p in prices_all if p.Day() == TODAY]
    
    #print len(prices)
    
    for p in prices:
        try:
            ins = p.Instrument()
            if ins != None:
                ins = ael.Instrument[ins.Oid()]
                PriceCopy(ins)
            else:
                print 'Price cannot be copied for price entry oid [%i] ...' % (p.Oid())

        except Exception, e:
            print 'ERROR copying price', e
            print '-----', p
    
            
    print 'Copy Mid Prices completed - Successful... '
    
     
                
                    
