import ael

trades = ael.Portfolio['ABL_Member'].trades()
out = open('C:\\backupout_agries.txt', 'w')

for t in trades:
    ins = t.insaddr.insid
    insadd = t.insaddr.insaddr
        
    White = ins.find('WMAZ')
    Yellow = ins.find('YMAZ')
    Wheat = ins.find('WHEAT')
    Weat = ins.find('WEAT')
    Sunflw = ins.find('SUNS')
    
    i = ael.Instrument[insadd]
    out.write('%s,%d,%d,%s\n' %(i.insid, i.otc, (i.product_chlnbr).seqnbr, i.paytype))
    i_clone = i.clone()
    flag = 0
    if White != -1:
    	if (i_clone.instype == 'Future/Forward' or i_clone.instype == 'Option'):
	    if ((i_clone.product_chlnbr.seqnbr) != 1238) or (i_clone.otc != 0) or (i_clone.paytype != 'Future'):
	    	i_clone.product_chlnbr = 1238
		i_clone.otc = 0
		i_clone.paytype = 'Future'
		flag = 1
    else: 
    	if Yellow != -1:
    	    if (i_clone.instype == 'Future/Forward' or i_clone.instype == 'Option') or (i_clone.paytype != 'Future'):
	    	if i_clone.product_chlnbr.seqnbr != 1239 or i_clone.otc != 0:
	    	    i_clone.product_chlnbr = 1239
		    #print i.insaddr
		    i_clone.otc = 0
    	    	    i_clone.paytype = 'Future'
	    	    flag = 1
	else: 
    	    if (Wheat != -1 or Weat != -1):
	    	if (i_clone.instype == 'Future/Forward' or i_clone.instype == 'Option') or (i_clone.paytype != 'Future'):
	    	    if i_clone.product_chlnbr.seqnbr != 1240 or i_clone.otc != 0:		    
		    	i_clone.product_chlnbr = 1240
		    	i_clone.otc = 0
    	    	    	i_clone.paytype = 'Future'
			flag = 1
	    else: 
	    	if Sunflw != -1:
		    if (i_clone.instype == 'Future/Forward' or i_clone.instype == 'Option') or (i_clone.paytype != 'Future'):
	    	    	if i_clone.product_chlnbr.seqnbr != 1241 or i_clone.otc != 0:    	    	    	
			    i_clone.product_chlnbr = 1241
			    i_clone.otc = 0
    	    	    	    i_clone.paytype = 'Future'
			    flag = 1

			
    if flag == 1:
    	print i.insid, i.otc, i_clone.product_chlnbr, i.paytype
    	print			    
    	i_clone.commit()
    else:
    	print 'No change to: ', i.insid, i.instype
    ael.poll()
out.close()    
   	    	
    
    #print t.trdnbr, ins, ins.find('WMAZ')
    #print t.trdnbr
