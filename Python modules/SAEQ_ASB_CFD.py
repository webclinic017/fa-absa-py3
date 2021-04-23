import ael, acm
global ports 
ports = []
def get_portfolios(port):
        
        for l in port.children():
            if l.member_prfnbr.compound == 1:
                get_portfolios(l.member_prfnbr)
            else:
                if l.member_prfnbr.prfid not in ('EQ_Forward_Structure', 'Futuregrowth_AM'):
                    ports.append(l.member_prfnbr.prfid)
                
        
        
def Create_CFD(i,prfol,date,*rest):
    
    if prfol == -1:
        get_portfolios(ael.Portfolio['9806'])
        prfol = ports 
        
    port = ael.Portfolio['ASB CFD']
    
    if CheckCFD(i.insid, port, date) == 'PASS':
        try:
            dt = ael.date(date)
        except:
            dt = date
        
        trds = i.trades()
        bsum = 0
        bprice = 0
        ssum = 0
        sprice = 0
        
        for t in trds:
            
            if t.insaddr == i and ael.date_from_time(t.time) <= dt and t.status not in ['Simulated', 'Terminated', 'Void']:
                if t.prfnbr.prfid in prfol:
                    if t.quantity > 0:
                        
                        bsum = bsum + t.quantity
                        bprice = bprice + (t.quantity * t.price)
                    else:
                        ssum = ssum + t.quantity
                        sprice = sprice + (t.quantity * t.price)
                    
    
        if bsum > 0:    
            bvwap = bprice/bsum
            print i.insid, ' BUY', 'price', bvwap, 'quantity', bsum
            trdn1 = Book_CFD(1, i.insid, port, bsum, i.mtm_price(dt), dt)
            #trdn1 = Book_CFD(1,i.insid,port,bsum,bvwap,dt)
           
        if ssum < 0:
            svwap = sprice/ssum
            #trdn1 = Book_CFD(1,i.insid,port,ssum,svwap,dt)
            print i.insid, ' SELL', 'price', svwap, 'quantity', ssum
            #trdn1 = Book_CFD(1,i.insid,port,ssum,svwap,dt)
            trdn1 = Book_CFD(1, i.insid, port, ssum, i.mtm_price(dt), dt)
        ael.poll()
        return 'SUCCESS'
    else:
        return 'FAIL'

def Book_CFD(temp, insid, port, qty, vwap, cfddate,  *rest):

    i = ael.Instrument[insid + '/CFD']
    if i == None:
        s = 'Please note that the CFD instrument does not exist for: '+ insid + '. Please create instrument.'
        q = 'ASB CFD CREATION - ' + insid
        ael.log(s)
        ael.sendmail('zaakirah.bagdadi@absacapital.com', q, s)
        ael.sendmail('andrew.nobbs@absacapital.com', q, s)
        return 0
    t_new = ael.Trade.new(i)
	    
    t_new.price = vwap
    
    t_new.quantity = qty * -1        
    t_new.status = 'FO Confirmed'
    t_new.prfnbr = port
    t_new.acquirer_ptynbr = ael.Party['EQ Derivatives Desk']
    
    ais = port.additional_infos()
    for ai in ais:
        if ai.addinf_specnbr.field_name == 'CFD Counterparty':
            t_new.counterparty_ptynbr = ael.Party[ai.value]  
    
    
    t_new.time = cfddate.to_time()
    t_new.value_day = cfddate
    t_new.acquire_day = cfddate

    t_new.curr = i.curr
    user = ael.userid()
    t_new.trader_usrnbr = ael.User[user]
    
    try:
    	t_new.commit()
    	
    except:
    	s =  'Error committing trade on instrument: ' + insid
    	ael.log(s)
	return 0
    return 1

def CheckCFD(insid, port, ddate, *rest):
    ins = ael.Instrument[insid + '/CFD']
    if ins == None:
        
        return 'PASS'
        
    trds = ins.trades()
    ddt = ael.date(ddate)
    for t in trds:
    	if ael.date_from_time(t.time) == ddt:
            if t.prfnbr.prfid == port.prfid and t.status not in ('Simulated', 'Terminated', 'Void'):
               msg = 'CFDs have already been committed on this instrument: '+ t.insaddr.insid +  ' for ' + (str)(ddate)
               ael.log(msg)
               return 'FAIL'
    
    return 'PASS'
