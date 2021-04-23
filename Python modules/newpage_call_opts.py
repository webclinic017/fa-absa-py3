import ael
def UpdateListedPage(ins,mun,maks,*rest):
    chl = ael.ChoiceList[979]
    print 'ins: ', ins
    print 'min: ', mun
    print 'max: ', maks
    min = int(mun)
    max = int(maks)
    print min 
    fut = ins
    if fut:
    	name = "und_insaddr.insid = %s" %ins.insid
	print name
    	opt = ael.Instrument.select(name)    
	liststrike = [t.strike_price for t in opt]
	#print liststrike
	listins = []
    	while (min <= max):
    	    print min
    	    newopt = ael.Instrument.new("Option")   
	    newopt.und_insaddr = fut
	    newopt.strike_price = min * 1
	    newopt.curr = ael.Instrument['ZAR'].curr
	    newopt.exp_day = fut.exp_day
	    newopt.call_option = 1
	    newopt.exercise_type = 'American'
	    newopt.contr_size = 10
	    newopt.product_chlnbr = chl
	    newopt.otc = 0
	    newopt.quote_type = 'Per Contract'
	    newopt.spot_banking_days_offset = 0
	    newopt.pay_day_offset = 0
	    newopt.insid = newopt.suggest_id()
	    stri = newopt.insid
	    st = stri.rstrip('/#1')
	    print st
	    listins.append(st)
	    if (ael.Instrument['%s' % st]):
	    	print 'Exists'
	    else:
	    	print 'Create'
		newopt.commit()
	    min = min + 50
    
    return 'Sucess'


'''
	ln = ael.ListNode.select()
    	for i in ln:
    	    if i.id == 'Listed Options' and i.father_nodnbr.id == 'Safex Options':
	    	val = i.leafs()
		break
	nodecl = i.clone()
	leaflist = [i.insaddr.insid for i in val]
	leaflist.sort()
	for v in listins:
    	    if v in leaflist:
    	    	print v
	    else:
	    	print 'New Leaf'
		if ael.Instrument[v]:
		    newLeaf = ael.ListLeaf.new(nodecl)
	    	    newLeaf.insaddr = ael.Instrument[v]
	    	    newLeaf.commit()
		    print 'Added to Page'
	    	else: 
		    print 'The Instument: %s does not exist' % v 
		print ael.Instrument[v] 
	nodecl.commit()
    else:
    	print "##############"
	print "error"	
	print "##############"

'''	
	

