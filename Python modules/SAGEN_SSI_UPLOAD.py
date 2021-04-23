import ael, string
def create_acc(infile):
    try:
    	f = open(infile)
    except:
    	print 'Infile could not be opened'
    list = ['ATS', 'BEF', 'DEM', 'ESP', 'FIM', 'FRF', 'IEP', 'ITL', 'NLG', 'PTE', 'XEU']
    line = f.readline()
    line = f.readline()
    while line:
    	l = [] 
	line = line.rstrip()
	l = string.split(line, ',')
	pty = ael.Party[l[4]].clone()
	if l[1] not in list:
	    acc = ael.Account.new(pty)
	    acc.name = l[0] + l[1]
	    acc.correspondent_bank_ptynbr = ael.Party[l[2]]
	    if l[3] != '':
	    	acc.correspondent_bank2_ptynbr = ael.Party[l[3]]
	    acc.curr = ael.Instrument[l[1]]
	    acc.network_alias_type = ael.InstrAliasType['SWIFT']
	    pty.commit()
	line = f.readline()
    
def create_SSI(infile):
    try:
    	f = open(infile)
    except:
    	print 'Infile could not be opened'
    line = f.readline()
    line = f.readline()
    while line:
    	l = [] 
	line = line.rstrip()
	l = string.split(line, ',')
	ssi = ael.SettleInstruction.new()
	ssi.curr.insid = l[1]
	ssi.money_cp_accnbr = ael.Account['toets2']
	
	
def create_typ_None_pty(infile):
    try:
    	f = open(infile)
    except:
    	print 'Infile could not be opened'
    line = f.readline()
    line = f.readline()
    while line:
    	l = [] 
	line = line.rstrip()
	l = string.split(line, ',')
	print l[0]
	InsAlType = ael.InstrAliasType['Delete']
	cp = ael.Party[l[0]]
	if not cp:
	    pty = ael.Party.new()
	    pty.type = 'None'
	    pty.ptyid = l[0]
	    pty.fullname = l[0]
	    InsAlType = ael.InstrAliasType['Delete']
	    al = ael.PartyAlias.new(pty)
	    al.type = InsAlType
	    al.alias = 'No'
	    pty.commit()
	    print pty.ptyid
	    ael.poll()
	else:
	    found = 0
	    cpc = cp.clone()
	    for a in cpc.aliases():
	    	if a.type == InsAlType:
		    a.alias = 'No'
		    cpc.commit()
		    ael.poll()
		    found = 1 
	    if found == 0:
	    	al = ael.PartyAlias.new(cpc)
	    	al.type = InsAlType
	    	al.alias = 'No'
		cpc.commit()
    	line = f.readline()
def create_Nonepty_Corr(infile):
    try:
    	f = open(infile)
    except:
    	print 'Infile could not be opened'
    line = f.readline()
    line = f.readline()
    while line:
    	l = [] 
	line = line.rstrip()
	l = string.split(line, ',')
	pty = ael.Party[l[0]].clone()
	pty.correspondent_bank = 1
	pty.commit()
	print l[0]
	line = f.readline()

def populate_acc_freetext(infile):
    try:
    	f = open(infile)
    except:
    	print 'Infile could not be opened'
    list = ['ATS', 'BEF', 'DEM', 'ESP', 'ECU', 'FIM', 'FRF', 'IEP', 'ITL', 'NLG', 'PTE', 'XEU']
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
		    	acc.accounting = 'TT-FX-Default'
	    	    	acc.commit()
	line = f.readline()
    	
	
	
	
	
	
#create_Nonepty_Corr('C:\\SSIBICAll.csv')	
#create_acc('C:\\AccountDetailAcq.csv')
#create_typ_None_pty('C:\\SSIBICAll.csv')
populate_acc_freetext('C:\\AccountDetail.csv')
