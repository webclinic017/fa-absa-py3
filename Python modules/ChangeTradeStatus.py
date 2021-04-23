import ael

def VoidTrades(t,*rest):
    if t.status != 'Void':
    	newTrd = t.clone()
    	newTrd.status = 'Void'
    	ins = ael.Instrument.read('insaddr=%d'%t.insaddr.insaddr)
    	ins.free_text
    	newIns = ins.clone()
    	newTrd.text1 = 'Trds before 31Mar03 Voided'
	newTrd.commit()
	newIns.commit()
    return 'Done'
    
def ChangeTradeStatus(t,status,*rest):
#    if t.status == 'FO Confirmed':
    trd = t.clone()
    trd.status = status
    try:
        print('Was:', t.status, 'Now: ', trd.status)
	trd.commit()
    except:
	print("")
    print(trd.status)
    if t.status == status:
        return 'Status Successfully Changed'
    else:
        return 'Change Unsuccessful'

#    else:
#    	return 'Not Updated'
