'''

import ael

def regenerate_cflows(depocf,op):

    depo = depocf.legnbr.insaddr
    if len(depo.legs()) >= 1: 
    	cflows = depo.legs()[0].cash_flows()
	float_rates = []
	cfs_updated=[]
	for cf in cflows:
	    ael.poll()
    	    if cf.type in ('Float Rate','Fixed Rate') and cf.start_day >= depocf.pay_day and op =='insert' and cf.cfwnbr not in cfs_updated: 
	    	print cf.nominal_factor, cf.cfwnbr, depocf.fixed_amount, depocf.cfwnbr, 'PRE'
		cfc=cf.clone()
		cfc.nominal_factor = cf.nominal_factor - depocf.fixed_amount
		cfc.commit()
		cfs_updated.append(cf.cfwnbr)
		print cf.nominal_factor, cf.cfwnbr, depocf.fixed_amount, depocf.cfwnbr, 'POST'
	    elif cf.type in ('Float Rate','Fixed Rate') and cf.start_day >= depocf.pay_day and op=='delete' and cf not in cfs_updated: 
		if len(cflows)>1:
		    print 'do I delete anything'
		    cfc=cf.clone()
		    cfc.nominal_factor = cf.nominal_factor + depocf.fixed_amount
		    try: cfc.commit()
    	    	    except: continue
		    cfs_updated.append(cf.cfwnbr)
	    ael.poll()	   
	#float_rates.sort(lambda x,y: x.start_day.to_time()- y.start_day.to_time())


def cashflow_update(o,cfw,arg,op):
    

    if op in ('insert','delete') and cfw.record_type == 'CashFlow' and cfw.type=='Fixed Amount':
    	
	cf = ael.CashFlow[cfw.cfwnbr]

    	if cf.cfwnbr>0:
    	    if cf.legnbr.insaddr.instype in ('Deposit','FRN'):
		if cf.legnbr.insaddr.category_chlnbr != None:
    	    	    if  cf.legnbr.insaddr.category_chlnbr.entry == 'StructuredLoan':
        	    	regenerate_cflows(cf,op)

ael.CashFlow.subscribe(cashflow_update)

'''

print('Please contact Mr Andries Brink x7180.  U are in violation of Ur contract')
