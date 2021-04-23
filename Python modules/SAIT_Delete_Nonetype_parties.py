import ael
try:
    f = open('C:\\nonepty_error_new.csv', 'w')
    ope = 1
except:
    print 'outfile could not be opened'
if ope:
    ptys = ael.Party.select()
    count = 0
    for p in ptys:
    	if ((not p.correspondent_bank) and (p.type == 'None')):
    	    print p.ptyid, ' ', p.type, ' ', p.add_info('Cpty_Delete')
	    count = count + 1
	    pt = p.clone()
	    cont = pt.contacts() 
    	    for cp in cont:
    	    	c = cp.clone()
    	    	rule = ael.ContactRule.select('contact_seqnbr = %d' %(cp.seqnbr))
    	    	print rule
    	    	for b in rule:
    	    	    print 'rules'
    	    	    b.delete()
    	    	print 'contacts'
    	    	c.delete()
	    print pt.accounts()
	    for a in pt.accounts():
	       	a.delete()
		print 'Could not delete the account'
	    pt.commit()
	    try:
	    	p.delete()
	    except:
	    	ael.log(p.ptyid)
	    	f.write((str)(p.ptynbr)+','+ p.ptyid + '\n') 
	
    print count
f.close()
