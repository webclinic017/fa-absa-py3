import ael, string



def create_acc(infile):

    count = 0
    fail_list = []
    
    try:
    	f = open(infile)
    except:
    	print 'Infile could not be opened'
	

    line = f.readline()
    line = f.readline()
    while line:
    	l = [] 
#	print line
    	line = line.rstrip()
	l = string.split(line, ',')

	try:
	    pty = ael.Party[l[0]].clone()
	except:
	    return 'Error'
  
    	acc = ael.Account.new(pty)
	acc.name = l[9]
	acc.curr = ael.Instrument[l[4]]
	acc.accounting = l[13]
    	
    	acc.network_alias_type = ael.InstrAliasType['SWIFT']
	
	acc.correspondent_bank_ptynbr = ael.Party[l[1]]
    	acc.account = l[3]

	try:
	    acc.commit()
#	    print 'Account committed'
	    count = count + 1
	    result = 'Success'
	except:
#	    print 'Unable to commit Account'
	    fail_list.append(l[0])
	    result = 'Failed'
	    
#        pty.commit()

	line = f.readline()

    f.close()
    
    print 'Accs committed : ', count
    print 'Failed CounterParty Accounts', fail_list
      	
    return result

    
def create_SSI(infile):

    count = 0
    fail_list = []

    try:
    	f = open(infile)
    except:
    	print 'Infile could not be opened'
    line = f.readline()
    line = f.readline()

    while line:
    	l = [] 
#	print line
	l = string.split(line, ',')
    	
	ssi_funding = ael.SettleInstruction.new()
	ssi_mm = ael.SettleInstruction.new()	

	ssi_funding.counterparty_ptynbr = ael.Party[l[0]]
	ssi_mm.counterparty_ptynbr = ael.Party[l[0]]	

	ssi_funding.curr = ael.Instrument[l[4]]
	ssi_mm.curr = ael.Instrument[l[4]]	

	ssi_funding.effective_from = ael.date_from_string('01/01/01')
	ssi_mm.effective_from = ael.date_from_string('01/01/01')
#	ssi_funding.effective_to = ael.date_from_string('01/01/00')
#	ssi_mm.effective_to = ael.date_from_string('01/01/00')

    	ssi_funding.settleid = l[7]  
	ssi_mm.settleid = l[8]  	    
	ssi_funding.acquirer_ptynbr = ael.Party['Funding Desk']
	ssi_mm.acquirer_ptynbr = ael.Party['Money Market Desk']	    
	
	try:
    	    accs = ael.Party[l[0]].accounts()
	    for i in ael.Party[l[0]].accounts():
	    	#print i.name
	    	if i.name == l[9]:
	    	    ssi_funding.money_cp_accnbr = i
	    	    ssi_mm.money_cp_accnbr = i
		else:
		    print 'Cannot find account for ', l[0]
	    
	except:
	    print 'Error on ', l[0]
	    
#	print ssi_funding.pp()
#	print ssi_mm.pp()

    	try:
	    ssi_funding.commit()
    	    ssi_mm.commit()
	    count = count + 1
	    result = 'Success'
	except:
	    fail_list.append(l[0])
	    result = 'Failed'

	line = f.readline()
	
    f.close()
    
    print 'SSIs committed : ', count
    print 'Failed CounterParty SSIs : ', fail_list
        
    return result
	



def populate_acc_freetext(infile):
    try:
    	f = open(infile)
	print 'file opened'
    except:
    	print 'Infile could not be opened'

    line = f.readline()
    line = f.readline()
    while line:
    	l = [] 
	line = line.rstrip()
	l = string.split(line, ',')
	pty = ael.Party[l[4]]
	print pty.ptyid
	if l[1] not in list:
	    for a in pty.accounts():
	    	if a.curr:
	    	    if (a.curr.insid == l[1]) and (a.name == (l[0] + l[1])): 
		    	acc = a.clone()
		    	acc.accounting = 'Money Market'
	    	    	acc.commit()
	line = f.readline()
    	
	
	
	
### main ###
create_acc('C:\\MM_SSI\Upload_SSI_Fri.csv')
ael.poll()
create_SSI('C:\\MM_SSI\Upload_SSI_Fri.csv')
#populate_acc_freetext('C:\\AccountDetail.csv')
