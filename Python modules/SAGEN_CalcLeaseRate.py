import ael
def getleaserate(s,toCurve,depoCurve,inspre,*rest):
    q = """select i.insid
    	    from
	    	instrument i
	    where
	    	i.insid like '%s'""" %(inspre)
    gofo = {}
    for i in ael.dbsql(q)[0]:
    	ins = ael.Instrument[i[0]]
	print ins.insid
	price = ins.used_price()
	per = convtoM(ins.legs()[0].end_period)
	gofo[per] = price
#    print gofo	
#    print '-----------------------------------------'	
    depo = {}
    depoyc = ael.YieldCurve[depoCurve] 	
    for dycp in depoyc.benchmarks():
    	ins = dycp.instrument
	print ins.insid
	price = ins.used_price()
	per = convtoM(ins.legs()[0].end_period)
	depo[per] = price
#    print depo
#    print '-----------------------------------------'
    lyc = ael.YieldCurve[toCurve]
    for lycp in lyc.benchmarks():
    	ins = lycp.instrument
	per = ins.legs()[0].end_period
#    	print 'GOFO: ', gofo[per]
	gof = gofo[per]
#	if per in depo.keys():
#	    print 'DEPO: ', depo[per]
#	    rate = depo[per]  
#	else:
    	dtoday = ins.spot_date(ael.date_today())
	date = ins.maturity_date()
	print date
	rate = depoyc.yc_rate(ael.date_today(), date, 'Simple', 'Act/360') * 100
#	    print 'ChangedDepo', rate
    	print 'GofoRate: ', gof, ' Depo: ', rate 
#	print ins.exp_period.rstrip('d')
	days = dtoday.days_between(date)
	print ins.insid, ' DAYS: ', days
    	leaserate = ((((1.0 + (rate/100.0) * (days/360.0))/(1.0 + (gof/100.0) * (days/360.0))) - 1.0) * 36000.0/days) 
	print 'LeaseRate: ', leaserate
    	prcs = ins.prices()
    	for p in prcs:
            if p.ptynbr.ptyid == 'SPOT':
                prclone = p.clone()
                prclone.ptynbr = p.ptynbr
                prclone.day = ael.date_today()
                prclone.insaddr = ins
                prclone.curr = p.curr
                prclone.settle = leaserate
                prclone.bid = leaserate
                prclone.ask = leaserate
                print prclone.insaddr.insid
                prclone.commit()
    clyc = lyc.clone()
    clyc.calculate()
    clyc.commit()
    return 'done'
        
def convtoM(period):
    if period.find('d') >= 0:
        days = period.rstrip('d')
	m = (int)(round((int)(days) / 30.00))
	period = str(m) + 'm'
    if period.find('y') >= 0:
        years = period.rstrip('y')
	m = (int)(years) * 12
	period = str(m) + 'm'	
    return period
#getleaserate(1,'XAU-DEPO','USD-DEPO','GOFO/%')
