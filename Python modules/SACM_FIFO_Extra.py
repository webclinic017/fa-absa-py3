import ael


def close_all_positions():

    trds = ael.Portfolio['JOB1'].trades()
    for t in trds:
    	if t.insaddr.instype in ('PromisLoan', 'Option', 'CD', 'Bill') and t.status not in ('Void', 'Simulated'):
	    pop_FIFO(t, 0.0)



def unfifo_all_positions():

    trds = ael.Portfolio['JOB1'].trades()
    for t in trds:
    	if t.status not in ('Void', 'Simulated') and t.insaddr.instype not in ('PromisLoan', 'Option', 'CD', 'Bill'):
    	    pop_FIFO(t, t.nominal_amount())

    

def pop_FIFO(t, value):
    
    if abs(t.nominal_amount()) <= 0.000001: value = 0.0
    saved = 0
    value_str = str(value)
    for addinfo in t.additional_infos():
    	if addinfo.addinf_specnbr.field_name == 'FIFO_POS':
#	    if t.trdnbr in (268210,268225,268164):print addinfo.value, value, t.trdnbr,addinfo.value, value_str
    	    if not addinfo.value and value_str:
	    	if t.trdnbr in (268210, 268225, 268164):print addinfo.value, value, t.trdnbr
		ai=ael.AdditionalInfoSpec['FIFO_POS']    
		addinfoclone = addinfo.clone()
    	    	t_c = ael.Trade[t.trdnbr].clone()
		addinfoclone.value= value
	    	addinfoclone.commit()
		saved = 1 
	    elif  addinfo.value and value_str and addinfo.value != value_str:
		ai=ael.AdditionalInfoSpec['FIFO_POS']    
		addinfoclone = addinfo.clone()
    	    	t_c = ael.Trade[t.trdnbr].clone()
		addinfoclone.value= value_str
	    	addinfoclone.commit()
		saved = 1 
	    else: 
	    	saved = 1
	    
    if saved == 0:
    	t_c = ael.Trade[t.trdnbr].clone()
	x=ael.AdditionalInfo.new(t_c)
	x.recaddr = t.trdnbr
	value_str= str(value)
    	x.value= value_str
	ai=ael.AdditionalInfoSpec['FIFO_POS']
	x.addinf_specnbr=ai.specnbr
	x.commit()
    	saved = 1

unfifo_all_positions()
#close_all_positions()
