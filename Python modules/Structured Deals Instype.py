import ael

ins = ael.Instrument.select('instype = "Deposit"')

#StructureLoans
ch = ael.ChoiceList[1261]

SDcount = 0
SLcount = 0
ANcount = 0
count = 0

for i in ins:
    if i.category_chlnbr == ch:
    	print(i.insid)
	trds = i.trades()
	for t in trds:
	    ads = t.additional_infos()
	    for a in ads:
	    	if a.addinf_specnbr.field_name == 'Funding Instype':
		    a_clone = a.clone()

		    if a.value == 'CD':
		    	a_clone.value = 'SD'
		    	SDcount = SDcount + 1			
		    elif a.value == 'CL':
		    	a_clone.value = 'SL'
		    	SLcount = SLcount + 1			
		    else:
		    	if a.value =='FDI':
		    	    a_clone.value = 'Annuity'
    	    	    	    ANcount = ANcount + 1
			    
		    try:
		    	a_clone.commit()
			count = count + 1
	    	    	print('Funding Instype: ', a.value, a_clone.value)
    	    	    	print()
		    except:
		    	print('Could not commit addinfo for ', i.insid)
			print()


print() 
print('SD           	: ', SDcount)
print('SL           	: ', SLcount)
print('Annuity      	: ', ANcount)
print('TOTAL commited	: ', count)
	
