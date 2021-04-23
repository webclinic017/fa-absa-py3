import ael

def change_val(temp, trd, *rest):
    t = ael.Trade[trd]
    curr = t.curr.insid
    SABaseM = ael.ChoiceList[1114].seqnbr
    SAEnergy = ael.ChoiceList[1204].seqnbr
    i = ael.Instrument[t.insaddr.insaddr]
    oldVal = i.product_chlnbr.entry
    if oldVal == 'SA_BaseMetals':
    	return 'Unchanged'
    elif curr in ('BRT_CRD_OIL', 'DIESEL', 'GAS_OIL', 'JET_FUEL'):
    	newVal = SAEnergy
    else:
    	newVal = SABaseM
	
    ins_clone = i.clone()
    ins_clone.product_chlnbr = newVal
    print(i.product_chlnbr.entry, ins_clone.product_chlnbr.entry)
    
    try:
    	ins_clone.commit()   
	print('Trade ', trd, ' changed from Valgroup ', i.product_chlnbr.entry, ' to ', ins_clone.product_chlnbr.entry)
	return 'Success'
    except:
    	print('Unable to commit trade ', trd)
	return 'Fail' 
    
    
    
#main
#print change_val(1, 471469)

