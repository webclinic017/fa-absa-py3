import ael, string


def currencies():
    currencies = ael.Instrument.select('instype = "Curr"')
    c = [] 
    for curr in currencies:
    	c.append(curr.insid)
    return c
    


def ASQL_call(temp, itype, curr, *rest):
    #same as main section, just added to enable function to be called from and ASQL run overnite.

    if itype == 'Cap':
    	ins = []

    	ins_list = ael.Instrument.select('instype = "Cap"')
	for i in ins_list:
	    ins.append(i)
	    	
    else:
    	ins = ael.Instrument.select('instype = %s' % itype)
	
    for i in ins:

    	if i.instype == 'Cap' and i.generic and i.curr.insid == curr and  string.rfind(i.insid, 'OPT') > -1: 
            for j in i.legs(): 
    	        oldl = j.clone() 
                oldl.strike = i.used_und_frw_price() 
#                print i.insid,i.used_und_frw_price() 
    	        oldl.commit()

		
    return 'Success'	    








ael_variables = [('instype', 'Instrument Type', 'string', ['Cap'], 'Cap'),
    	     	('curr', 'Currency', 'string', currencies(), None)]


def ael_main(dict):
    itype = dict["instype"]
    curr = dict["curr"]
                                                      
    if itype == 'Cap':
    	ins = []

    	ins_list = ael.Instrument.select('instype = "Cap"')
	for i in ins_list:
	    ins.append(i)
	    
	
    for i in ins:

    	if i.instype == 'Cap' and i.generic and i.curr.insid == curr and  string.rfind(i.insid, 'OPT') > -1: 
            for j in i.legs(): 
    	        oldl = j.clone() 
                oldl.strike = i.used_und_frw_price() 
                print i.insid, i.used_und_frw_price() 
    	        oldl.commit()
