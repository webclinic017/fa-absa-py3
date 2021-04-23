import ael, time

def duration_comb(temp, insid, *rest):
    
    '''print insid'''
    
    sql = """select distinct
                combund.insaddr,
                cl.weight
                
            from
                trade   t,
                combinationlink cl,
                instrument comb,
                instrument combund
            
            where 
                comb.insaddr = t.insaddr
                and comb.insaddr = cl.owner_insaddr
                and cl.member_insaddr = combund.insaddr
                and comb.insid = '%s'"""%insid
        
    combos = ael.asql(sql)
    all_ins = combos[1][0]
    
    sum = 0
    pv = 0
    
    for c in all_ins:
        ins = ael.Instrument[c[0]]
        w = c[1]
            
        
        for cf in ins.cash_flows().members():
            if cf.pay_day > ael.date_today():
                ttp =round((ael.date_today()).days_between(cf.pay_day))/365
                sum = sum + ttp * cf.present_value()*w
                pv = pv + cf.present_value()*w
            
    try:    
        dur = sum/pv
        return dur
            
    except Exception, e:
        print e   
    
    
    
def copyVolSurfaceToSOB(temp, vol, *rest):
    
    vol_org = ael.Volatility[vol]
    vol_sob = ael.Volatility[vol + '_SOB']
    vol_sob_clone = vol_sob.clone()
    
    t0 = time.time()
    for p in vol_sob_clone.points():
        p.delete()
    
    print vol +'_SOB deleted'
         
    for p in vol_org.points():
        new_pnt = ael.VolPoint.new(vol_sob_clone)
        
        new_pnt.insaddr = p.insaddr
        new_pnt.volatility = p.volatility
        new_pnt.commit()
        #break
    vol_sob_clone.commit()
    print '%.0f' % (time.time() - t0) + ' sec copying ' + vol +'\n'
    
    return 'VolSurface copied to SOB'
    

#Copied from NextCashflow, calculates next CF endday given the legnbr

def NextCF(temp, lnbr, ddate, flag, *rest): 
    l = ael.Leg[lnbr]
    cashf = l.cash_flows()
    list = []
    for c in cashf:
    	tup = (c.end_day, c.cfwnbr, c.fixed_amount)
#	print tup
	list.append(tup)
    	
    list.sort()

    count = 0
    value = '0'
    sdate = ael.date_from_string(ddate)
    
    while count < len(list):
    	pay_day = list[count][0]
	if pay_day > sdate:
#	    print 'Next cashflow pay_day', pay_day
    	    if flag == 0:
		value = (str)(list[count][2])
    	    	return value
	    else:
		value = (str)(list[count][0])
    	        return value		    
	count = count + 1
	
    return value



# returns next CF endday  for a combination instrument

def NextCF_comb(temp, ins, ddate, *rest):
    
    und = []
    
    inst = ael.Instrument[ins]
    sdate = ael.date_from_string(ddate)
    
    for m in inst.combination_links():
        
        und.append(m.member_insaddr)
    
    #legs = []
    cftemp = []
    cfdate = []
    
    
    for i in und:
        for l in i.legs():
            if l.type <> 'Credit Default':
                #legs.append(l.legnbr)
                cftemp.append(NextCF('', l.legnbr, sdate, 1))


    for t in cftemp:
        if t not in cfdate:
            cfdate.append(t)
            
    cfdate.sort()
    
    return cfdate[0]  
    
    
    
#ins = 'CLN107SABMiller/20090620/15/0.9/ACLU020'   

#print NextCF_comb('',ins)

