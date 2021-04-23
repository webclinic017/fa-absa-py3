import ael

flag = 0
instr1 = ael.Instrument.select('product_chlnbr = 1242')
for i in instr1:
    i_clone = i.clone()
    if (i_clone.otc != 0 or i_clone.instype == 'Option'):
	i_clone.paytype = 'Future'
	flag = 1
	
    if flag == 1:
    	print(i.insid, i.otc, i_clone.product_chlnbr, i.paytype)
    	print()			    
    	i_clone.commit()
    else:
    	print('No change to: ', i.insid, i.instype)
    	
    ael.poll()
    flag = 0
        

instr2 = ael.Instrument.select('product_chlnbr = 1243')
for i in instr2:
    i_clone = i.clone()
    if (i_clone.otc != 0 or i_clone.instype == 'Option'):
	i_clone.paytype = 'Future'
	flag = 1
	
    if flag == 1:
    	print(i.insid, i.otc, i_clone.product_chlnbr, i.paytype)
    	print()			    
    	i_clone.commit()
    else:
    	print('No change to: ', i.insid, i.instype)
    	
    ael.poll()
    flag = 0


instr3 = ael.Instrument.select('product_chlnbr = 1244')
for i in instr3:
    i_clone = i.clone()
    if (i_clone.otc != 0 or i_clone.instype == 'Option'):
	i_clone.paytype = 'Future'
	flag = 1
	
    if flag == 1:
        print(i.insid, i.otc, i_clone.product_chlnbr, i.paytype)
    	print()			    
    	i_clone.commit()
    else:
    	print('No change to: ', i.insid, i.instype)

    ael.poll()
    flag = 0


instr4 = ael.Instrument.select('product_chlnbr = 1245')
for i in instr4:
    i_clone = i.clone()
    if (i_clone.otc != 0 or i_clone.instype == 'Option'):
	i_clone.paytype = 'Future'
	flag = 1
	
    if flag == 1:
    	print(i.insid, i.otc, i_clone.product_chlnbr, i.paytype)
	print()			    
    	i_clone.commit()
    else:
    	print('No change to: ', i.insid, i.instype)
	
    ael.poll()
    flag = 0
	
    
