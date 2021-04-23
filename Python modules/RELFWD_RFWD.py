'''
Purpose: Change the AEL RELFWD_RFWD to incorporate additional strikes

Department : Trading

Desk : Fixed Income

Requester : Musundwa, Sifiso

Developer : Anil Parbhoo

CR Number : 319403

Book of Work Reference Number : FI19

'''


import ael, string, re

def currencies():
    currencies = ael.Instrument.select('instype = "Curr"')
    c = [] 
    for curr in currencies:
    	c.append(curr.insid)
    return c
        
def ASQL_call(temp, itype, curr, *rest):
    #same as main section, just added to enable function to be called from and ASQL run overnite.

    if itype == 'Both':
    	ins = []

    	ins_list = ael.Instrument.select('instype = "Cap"')
	for i in ins_list:
            ins.append(i)
	    
	ins_list = []
	ins_list = ael.Instrument.select('instype = "Floor"')
	for i in ins_list:
            ins.append(i)
	    
        ins_list = []
	ins_list = ael.Instrument.select('instype = "Option"')
	for i in ins_list:
            if i.und_instype == 'FRA':
                ins.append(i)
    else:
    	ins = ael.Instrument.select('instype = %s' % itype)

    checkInsList(ins, curr)
    return 'Success'

ael_variables = [('instype', 'Instrument Type', 'string', ['Cap', 'Floor', 'Both'], 'Both'),
    	     	('curr', 'Currency', 'string', currencies(), None)]
           
def ael_main(dict):
    itype = dict["instype"]
    curr = dict["curr"]
                                                      
    if itype == 'Both':
    	ins = []

    	ins_list = ael.Instrument.select('instype = "Cap"')
	for i in ins_list:
	    ins.append(i)
	    
	ins_list = []
	ins_list = ael.Instrument.select('instype = "Floor"')
	for i in ins_list:
	    ins.append(i)
	    
        ins_list = []
	ins_list = ael.Instrument.select('instype = "Option"')
	for i in ins_list:
            if i.und_instype == 'FRA':
                ins.append(i)
    else:
    	ins = ael.Instrument.select('instype = %s' % itype)
    checkInsList(ins, curr)

def parse(insid):
    '''
    returns double following RFWD in insid.
    If RFWD not found, will retun None
    '''
    spreadPattern = r'(.*)(RFWD)([+-][\d.]+)'
    myMatch = re.match(spreadPattern, insid)
    if myMatch:
        return float(myMatch.group(3))
    else:
        return None
        
def checkInsList(insList, curr):
    for i in insList:
        spread = parse(i.insid)
        #if spread:
        #    print i.insid, 'is matched with spread of', spread

        # CAP & FLOORS
        if i.instype in ['Cap', 'Floor'] and i.generic and i.curr.insid == curr and string.rfind(i.insid, 'RELFWD') > -1: 
            for j in i.legs(): 
                oldl = j.clone() 
                oldl.strike = i.used_und_frw_price() 
                #print i.insid,i.used_und_frw_price() 
                oldl.commit()
        elif i.instype in ['Cap', 'Floor'] and i.generic and i.curr.insid == curr and spread: 
            for j in i.legs(): 
                oldl = j.clone() 
                oldl.strike = i.used_und_frw_price() + spread 
                #print i.insid,i.used_und_frw_price() + spread 
                oldl.commit()
       
        # OPTION on a FRA
        elif i.instype == 'Option' and i.generic and i.curr.insid == curr and string.rfind(i.insid, 'RELFWD') > -1: 
            #for j in i.und_insaddr.legs()[0].par_rate(): 
            oldl = i.clone() 
            oldl.strike_price = i.und_insaddr.par_rate()
            oldl.commit() 
        elif i.instype == 'Option' and i.generic and i.curr.insid == curr and spread: 
            #for j in i.und_insaddr.legs(): 
            oldl = i.clone() 
            oldl.strike_price = i.und_insaddr.par_rate() + spread
            oldl.commit()
