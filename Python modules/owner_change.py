import string, ael
try: infile = open('C:\\devoncheck\\instr.csv')
except:
    print 'File not opened'
A = []
number = ael.User['ABGW070'].usrnbr
#print number
line = infile.readline()
while line:
    line = (line.rstrip())*1
    A.append(line) 
    line = infile.readline()
for ins in A:
    if ael.Instrument[ins]:
    	instr = ael.Instrument[ins]
    	instrcl = instr.clone()
    	instrcl.owner_usrnbr = number
    	instrcl.commit()
#    	for trd in instr.trades():
#    	    trad = trd.clone()
#	    trad.owner_usrnbr = number
#	    #print trad.owner_usrnbr.userid 	
#    	    trad.commit()
