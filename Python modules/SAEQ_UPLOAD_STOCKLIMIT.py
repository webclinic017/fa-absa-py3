import ael, string
try:
    f = open('C:\\Liquidity_limits_stocks_2005.csv')
except:
    print 'File not opened'
line = (f.readline()).strip()
line = (f.readline()).strip()
count = 0

while line != '':
    print
    print line
    l = []
    l = string.split(line, ',')
    ins = ael.Instrument[l[1]]
    if ins != None:
    	addinfs = ins.additional_infos()
	flag = 'false'
	for a in addinfs:
#	    print a.addinf_specnbr.field_name
	    if a.addinf_specnbr.field_name == 'Stock_Limit':
	    	flag = 'true'

		if a.value == l[2]:
		    print 'Stock Limit is the same'
		else:
		    addinf_clone = a.clone()
		    addinf_clone.value = l[2]
		    try:
		    	addinf_clone.commit()
    	    	    	print 'Value updated for Stock Limit'
		    except:
		    	print 'Error updating add_info'
		    
		
	if flag == 'false':
	    ins_clone = ins.clone()
	    x = ael.AdditionalInfo.new(ins_clone)
	    x.value = l[2]
	    ai = ael.AdditionalInfoSpec['Stock_Limit']
	    x.addinf_specnbr = ai.specnbr
	    try:
	    	x.commit()
    	    	print 'Stock Limit added'
	    except:
	    	print 'Error adding add_info'

#           print x.pp()

    else:
    	print 'None'
	count = count + 1
    
    line = (f.readline()).strip()

	    
f.close()
print 'done'
print 'Instruments not uploaded ', count
