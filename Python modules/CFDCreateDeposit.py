print 'CFDCreateDeposit re-loaded.'
import ael


def findShortestRateIndex(curr):
    res = []
    for r in ael.Instrument.select('instype="RateIndex"'):
    	if r.curr == curr:
   	    
	    res.append((int(r.exp_period[:-1]), r))
	    
    res.sort()
       	    
    return res[0][1]   


def createCFDDeposit(t):
    
    
    i = ael.Instrument.new('Deposit')
    instrid = str(t.insaddr.insid) + '/' + t.prfnbr.prfid
    
    if ael.Instrument[instrid]:
    	return 'Nothing created'
	
    i.insid = instrid

    i.generic = 0
    i.notional = 0

    i.curr = t.insaddr.curr
    i.quote_type = 'Pct of Nominal'

    i.otc = 1
    i.mtm_from_feed = 0
    i.spot_banking_days_offset = 0
    chl = ael.ChoiceList.read('list="ValGroup" and entry="CFD"')
    i.product_chlnbr = chl   

    i.contr_size = 1

    i.open_end = 1
    
    ai = ael.AdditionalInfo.new(i)
    ais  = ael.AdditionalInfoSpec['CFD Future Ref']
    ai.addinf_specnbr = ais.specnbr
    ai.value = t.insaddr.insid
    
    ai = ael.AdditionalInfo.new(i)
    ais  = ael.AdditionalInfoSpec['CFD Portfolio Ref']
    ai.addinf_specnbr = ais.specnbr
    ai.value = t.prfnbr.prfid   
    
    
    leg = i.legs()[0]
    leg.start_day =  t.value_day
    leg.end_day =  t.value_day.add_delta(0, 6, 0)
    leg.fixed_rate = 0    
    
    fl = findShortestRateIndex(i.curr)
		
    leg.float_rate = fl
    
    leg.type = 'Call Float'
    leg.payleg = 0
    leg.daycount_method = 'Act/ActISMA'
    leg.curr = t.insaddr.curr
    leg.nominal_factor = 1

    leg.rolling_period = '1D'
    
    leg.rolling_base_day =  t.value_day
    
    leg.pay_calnbr = t.insaddr.curr.legs()[0].pay_calnbr
    leg.reset_calnbr = t.insaddr.curr.legs()[0].pay_calnbr
    
    leg.reset_type = 'Single'
    leg.reset_period = '1D'
    leg.reset_day_offset = 0
    
    for c in leg.cash_flows():
    	c.delete()

    i.commit()

    
    tn = ael.Trade.new(i)
    tn.quantity = 1
    tn.prfnbr = t.prfnbr
    tn.status = t.status
    tn.price = 0
    tn.premium = 0
    tn.curr = t.curr
    tn.time = t.time
    tn.value_day = t.value_day
    tn.acquire_day = t.acquire_day
    tn.counterparty_ptynbr = t.counterparty_ptynbr
    tn.acquirer_ptynbr = t.acquirer_ptynbr
    tn.trader_usrnbr = t.trader_usrnbr
    
    tn.commit()
    
    return instrid

#createCFDDeposit(ael.Trade[44309])


def trade_update(o, t, arg, op): 
    global statuslist
    #print o,t,arg,op


    if op in ['insert', 'update']:
    	ins = t.insaddr
    	pf = t.prfnbr

    	if ins.instype == 'Future/Forward':
	    chl = ael.ChoiceList.read('list="ValGroup" and entry="CFD"')
	    if ins.product_chlnbr == chl:
    	    	
		found = 0
		
		for d in ael.Instrument.select('instype="Deposit"'):
		    if d.add_info('CFD Future Ref') and d.add_info('CFD Portfolio Ref'):

	    		if d.add_info('CFD Future Ref')== ins.insid and d.add_info('CFD Portfolio Ref') == pf.prfid:
    	    		    ael.log('Deposit exists for:'+ins.insid + pf.prfid)
			    found = 1
			    break

		if not found:
    	    	    try:
	    	    	res = createCFDDeposit(t)
		    	if res != 'Nothing created':
			    ael.log('Deposit created for:'+ins.insid + pf.prfid)
			else:
			    ael.log('Deposit exists for:'+ins.insid + pf.prfid)   
		    except:
		    	ael.log('Not possible to create deposit for:'+ins.insid + pf.prfid)
		    
	    
	               
def start(): 
    #ael.Trade.subscribe(trade_update)
    """Start subscription on trades.""" 
    global statuslist
    
    ael.Trade.subscribe(trade_update)

def status():
    return statuslist


start()

'''
rounding                 Normal
decimals                 5
start_day                2003-12-11
start_period.unit        Weeks
start_period.count       -1
end_day                  2004-03-11
end_period.unit          Months
end_period.count         3
rolling_period.unit      Days
rolling_period.count     1
rolling_base_day         2003-12-11
pay_day_offset.unit      Days
pay_day_offset.count     0
pay_day_method           Mod. Following
pay_calnbr               500407
reset_calnbr             500407
pay2_calnbr              0
pay3_calnbr              0
extended_final_cf        No
reset_type               Weighted
reset_period.unit        Months
reset_period.count       3
reset_day_offset         -2
reset_day_method         Following
reset_calnbr             500407
reset2_calnbr            0
reset3_calnbr            0
fixed_rate               0
fixed_coupon             No
exclude_first_period     No
spread                   100
strike                   0
nominal_at_end           Yes
nominal_at_start         No
reset_in_arrear          No
long_stub                No
amort_period.unit        Days
amort_period.count       0
float_rate_factor        1
float_rate_offset        0
amort_type               None
amort_start_day          2003-12-11
amort_start_period.unit  Days
amort_start_period.count 0
amort_end_day            2004-03-15
amort_end_period.unit    Months
amort_end_period.count   1
amort_end_nominal_factor 0
annuity_rate             0
amort_daycount_method    Act/360

'''

