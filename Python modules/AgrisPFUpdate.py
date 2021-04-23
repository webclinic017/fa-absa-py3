import ael, string

'''

This AEL has been written for ABSA to reassign all trades 
from their various Agris portfolios to a single Agris portfolio. 

The source file is Agris Client Portfolio mapping.xls

This file (in csv format) needs to be passed to the function or saved 
as a csv file on the C:\ drive for this AEL.


'''

def update_agris(file):


    if not file: file = 'c:\agris.csv'
    f = open(file)
    line = f.readline()
    ael.log('Started loading from %s.' % file)

    good_trade_list=[]
    bad_trade_list=[]


    while line:
    	
	oldpf, newpf = string.split(line, ',')

    	print oldpf, newpf[:12]
	newpf = newpf[:12]
	
    	oldpfolio = ael.Portfolio.read("prfid = '%s'" %oldpf)
	newpfolio = ael.Portfolio.read("prfid = '%s'" %newpf)
	
    	print oldpfolio, newpfolio, 'line37'
	if oldpfolio and newpfolio:
	    print oldpfolio.prfid
    	    trades = oldpfolio.trades()

    	    # create two lists, one for successfully modified trades, one for less successfully
    	    # modified trades. 


    	    # go through the list of trades that need to be modified
	    for t in trades:

		try:
		    tc = t.clone()
		    tc.prfnbr = newpfolio
		    tc.commit()
		    good_trade_list.append(t.trdnbr)
		except:
    		    bad_trade_list.append(t.trdnbr)
    	    
    	else:
	    print 'No portfolio %s or %s'  %(oldpf, newpf)
	
	line=f.readline()
    print good_trade_list
    print bad_trade_list
        # send a mail notifying the recipient of the reults	
    ael.sendmail('panos.prodromou@front.com', 'Updated Eq prop trades', 'The following trades have had their pfolio updated'  \
    '\n' + str(good_trade_list) + '\n' + 'The following trades should have had their pfolio updated, but failed \n' + str(bad_trade_list))


update_agris('c:\\agris.csv')
