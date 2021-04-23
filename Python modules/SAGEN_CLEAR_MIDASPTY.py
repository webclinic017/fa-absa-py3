import ael, string
def clean_cp(infile):
    try:    
    	f = open(infile)
    except:
    	print 'File could not be opened'
    try:
    	out = open('C:\\erroralias.txt', 'w')
    except:
    	print 'Outfile could not be opened'
    line = f.readline()
    line = f.readline()
    while line:
    	l = []
	line = line.rstrip('\n')
	l = string.split(line, ',')
	mparty = ael.Party[(int)((l[0]))].clone()
	print mparty.ptyid
	alias = mparty.aliases()
	for a in alias:
	    if a.type:
	    	print a.type.alias_type_name, a.alias
	    	if a.type.alias_type_name == 'MIDAS':
	    	    val = (int)(a.alias)
	    	    if val != (int)(l[3]):
	    	    	out.write(mparty.ptyid + ',' + a.alias + '\n')
		    	a.delete()
		    	mparty.commit()
		    	ael.poll()
	    	else:
	    	    print 'Correct Alias'
	
	line = f.readline()
    f.close()
    out.close()
    
def create_new(infile):
    try:    
    	f = open(infile)
    except:
    	print 'File could not be opened'
    try:
    	out = open('C:\error.txt', 'w')
    except:
    	print 'Outfile could not be opened'
    line = f.readline()
    line = f.readline()
    InsAlType = ael.InstrAliasType['MIDAS']
    print InsAlType
    while line:
    	l = []
	line = line.rstrip('\n')
	l = string.split(line, ',')
	mparty = ael.Party[(int)((l[0]))].clone()
	if l[6] == '1':
	    #print mparty
	    if len(l[7]) <= 39:
	    	if not ael.Party[l[7]]:
	    	    newp = ael.Party.new()
	    	    newp.type = 'Counterparty'
	    	    newp.ptyid = l[7]
	    	    newp.fullname = l[7]
	       	    print 'new party'
		    newp.commit()
		    print l[7]
		    al = ael.PartyAlias.new(newp)
		    al.alias = l[3]
		    print l[3]
		    al.type = InsAlType
		    al.commit()
		    print al.pp()
		else:
		    out.write(l[7]+ ',' + l[3] + '\n')
	    else:
	    	out.write(l[7]+ ',' + l[3] + '\n')
		
	line = f.readline()
    out.close()
    f.close()

def delete_alias(infile):
    try:    
    	f = open(infile)
    except:
    	print 'File could not be opened'
    try:
    	out = open('C:\error.txt', 'w')
    except:
    	print 'Outfile could not be opened'
    line = f.readline()
    line = f.readline()
    InsAlType = ael.InstrAliasType['MIDAS']
    while line:
    	l = []
	line = line.rstrip('\n')
	l = string.split(line, ',')
	mparty = ael.Party[(int)((l[0]))].clone()
	print mparty.ptyid
	if l[6] == '1':
    	    for a in mparty.aliases():
	    	if a.type == InsAlType:
		    print 'Alias', a.alias, InsAlType.alias_type_name, 'L3-', l[3]
	    	    val = (int)(a.alias)
	    	    if val == (int)(l[3]):
		    	out.write(mparty.ptyid + a.alias + '\n')
		    	print a.pp()
		    	a.delete()
	    	    	mparty.commit()
		    	ael.poll()
	line = f.readline()
    out.close()
    f.close()
	
#create_new('C:\\MidasPTY\\Bradley.csv')
#create_new('C:\\MidasPTY\\MidasPTY.csv')
clean_cp('C:\\MidasPTY\\RemoveAliasCPFINAL.csv')
#delete_alias('C:\\MidasPTY\\Bradley.csv')
