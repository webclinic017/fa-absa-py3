import ael


def Change_Ins(temp, from_Ins, to_Ins, *rest):
    ins1 = ael.Instrument[from_Ins]
    ins2 = ael.Instrument[to_Ins]
    trades = ins1.trades()
    for t in trades:
        print t.status
        if t.status != 'Void':
            t_clone = t.clone()
            #print t_clone.trdnbr, t_clone.insaddr.insid
            t_clone.insaddr = ins2.insaddr
            try:
                t_clone.commit()
            except:
                print 'Could not commit: ', t.trdnbr
            print 'Changed Instrument of Trade ', t_clone.trdnbr, ' to ', t_clone.insaddr.insid 
            print
            ael.poll()
	
	
    print
    print
    insid = ''
    old_ins = ins1.trades()
    if len(old_ins) == 0:
    	insid = ins1.insid
    	ins1.delete()
    	print insid, ' deleted'
    else:
    	print insid, 'could not be deleted'
	
    
    return 'Success'
	
	
#main#
#f = 70198
#t = 70181
#print Change_Ins('temp', f, t)
    
    
    
