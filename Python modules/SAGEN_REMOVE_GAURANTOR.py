import ael, string
def trade_guarantor():
    try:
    	f = open('C:\\guarant.csv')
    except:
    	print 'could not open'
    line = f.readline()
    line = f.readline()
    while line:
    	l = []
        line = line.rstrip()
        l = string.split(line, ',')
    	trd = ael.Trade[(int)(l[0])].clone()
        trd.guarantor_ptynbr = 0
        trd.commit()
        line = f.readline()
    f.close()
def party_guarantor():
    try:
    	f = open('C:\\partyguar.csv')
    except:
    	print 'could not open'
    line = f.readline()
    line = f.readline()
    while line:
    	l = []
        line = line.rstrip()
        l = string.split(line, ',')
    	pty = ael.Party[l[0]].clone()
	print pty.ptyid
        pty.guarantor_ptynbr = 0
        pty.commit()
        line = f.readline()
    f.close()
    
party_guarantor()
