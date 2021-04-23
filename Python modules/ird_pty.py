import ael, string
def ird_pty(filename):
    try:
    	f = open(filename)
    except:
    	print 'File not opened'
    line = f.readline()
    line = f.readline()
    while line != '':
    	list = string.split(line, ',')
	pid = list[0].rstrip()
	pid = pid.lstrip()
	party = ael.Party[pid]
	print '-------------'
	print pid
	print '*************'
	if party:
    	    pty = ael.Party[pid].accounts()
	    print pid, ' ', len(pty)
	    if len(pty) == 1:
	    	ac_clone = pty[0].clone()
	    	ac_clone.accounting = 'IRD'
    	    	ac_clone.commit()
	        
	try:
	    line = f.readline()
	except:
	    print 'End of file'
ird_pty('C:\\CP_Clean\\ird_parties.csv')
