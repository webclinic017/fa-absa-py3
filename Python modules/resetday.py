import ael, string
try: infile = open('C:\\devonhelp\\reset_day.csv')
except:
    print 'File not opened'
A = {}
line = infile.readline()
b, c = string.split(line, ',')
A[b] = c.rstrip()
print A
while line:
    line = infile.readline()
    try:	
    	b, c = string.split(line, ',')
    	A[b] = c.rstrip()
    except:
    	print 'wrong size'
for ins in A.keys():
    if ael.Instrument["%s" % (ins)]:	
    	inst = ael.Instrument["%s" % (ins)].clone()
    	#inst = ael.Instrument['ZAR-USD/CCS/JI-LI/001101-101101/#1'].clone()
    	for l in inst.legs():
    	    if (l.curr.insid == 'ZAR'):
#    	    	if (l.type == 'Float'):
      	    	print l.reset_day_offset
		if l.reset_day_offset != 0:
	    	    l.reset_day_offset = 0
		    print l.reset_day_offset	 
    	    	    inst.commit()
 
