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
	print l
	
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

def create_instrument(Ins):
    i_new = ael.Instrument.new('FreeDefCF') 
    i_new.insid = 'CPF'
#    i_new.date_from = ael.date('13-Jul-99') 
#    i_new.date_to = ael.date('01-Jul-09')
    
    i_new.legs()[0].type ='Fixed'
    i_new.legs()[0].payleg = 0
    i_new.legs()[0].daycount_method =	'Act/365'
    i_new.legs()[0].start_day =	ael.date('13/07/1999')
    i_new.legs()[0].end_day	=ael.date('01/07/2009')
    i_new.legs()[0].rolling_period =	'1M'

    i_new.legs()[0].rolling_base_day=	ael.date('01/07/2009')
#    i_new.legs()[0].pay_day_offset.unit	='Days'
    
    i_new.legs()[0].pay_day_method	='Following'
    i_new.legs()[0].fixed_rate	= 17.08

    i_new.legs()[0].amort_period = '1m'

    i_new.legs()[0].amort_type	='Annuity'
    i_new.legs()[0].amort_start_day =	ael.date('13/07/1999')
    #i_new.legs()[0].amort_start_period.unit	='Days'
    i_new.legs()[0].amort_end_day	= ael.date('01/07/2009')
#    i_new.legs()[0].amort_end_period.unit	='Days'
    i_new.legs()[0].annuity_rate	 = 17.08
    i_new.legs()[0].amort_daycount_method = 'Act/365'
    i_new.legs()[0].amort_generation ='Target End'
    i_new.commit()
    print i_new.legs()[0].pp()
def populate_Contract_Info(infile):
    try:
    	f = open(infile)
    except:
    	print 'Infile could not be opened'
    list = ['ATS', 'BEF', 'DEM', 'ESP', 'ECU', 'FIM', 'FRF', 'IEP', 'ITL', 'NLG', 'PTE', 'XEU']
  #  line = f.readline()
    line = f.readline()
    while line:
    	l = [] 
	line = line.rstrip()
	l = string.split(line, ',')
	print l
	line = f.readline()
    	
	
	
#print ael.Instrument['4051770113_0'].legs()[0].pp()
print create_instrument('Test')
	
#populate_Contract_Info('C:\\CPF\\Contract Info.csv')
