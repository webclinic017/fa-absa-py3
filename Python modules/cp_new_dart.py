import ael, string
def change_dart(file):
    f = open(file)
    ael.log('Started loading from %s.' % file)
    stored = [] # list of stored instruments
    line = f.readline()
    pty_counter=0
    line = f.readline()
    olddart, ptynbr, ptyid, newdart = string.split(line, ',')   
    while ptynbr != "":
    	if newdart != '':
    	    party_rec=ael.Party.read("ptynbr='%s'" % ptynbr)
	    pty_counter=pty_counter + 1
	    # Update party information
	    print 'New Dart number for party: ', party_rec.ptyid
    	    print 'New Dart = ', newdart 
	    # Update DART numbers in party aliasses
	    party_rec_aliases=party_rec.aliases()
	    print party_rec_aliases
    	    #aliases_list=[]
    	    gotIt = 0
    	    for al in party_rec_aliases:
    	    	if al.type != None and al.type.alias_type_name == 'Dart_Number':
	    	    alc = al.clone()
        	    alc.alias = newdart.rstrip()
		    print alc.alias
		    print alc.pp()
	    	    try:
    	    	    	# CommitMsg = 'Committed party Dart alias info for ' + pr.ptyid
			# Thys
			CommitMsg = 'Committed party Dart alias info for ' + party_rec.ptyid
    	   	    	alc.commit()
	    	    	ael.log(CommitMsg)		    				
	    	    except:
	    	    	# ErrMsg = 'Error committing DART numbers in party aliasses on ptynbr: '+ ptynbr + ' , ptyid: ' + pr.ptyid + ' ,Alias Value:' + alc.alias
			# Thys
			ErrMsg = 'Error committing DART numbers in party aliasses on ptynbr: '+ ptynbr + ' , ptyid: ' + party_rec.ptyid + ' ,Alias Value:' + alc.alias
		    	print ErrMsg
		    	ael.log(ErrMsg)
	    	    gotIt = 1
	    	#al.delete() 
    	    if gotIt == 0:
	    	aln = al.new()
	    	aln.alias = newdart.rstrip()
	    	print aln.alias
	    	aln.type = ael.InstrAliasType['Dart_Number']
	    	aln.ptynbr = party_rec
	    	try:
	    	    #CommitMsg = 'Committed party new Dart alias info for ' + pr.ptyid
		    # Thys
		    CommitMsg = 'Committed party new Dart alias info for ' + party_rec.ptyid
	    	    aln.commit()
	    	    ael.log(CommitMsg)		    	
	    	except:
	    	    #ErrMsg = 'Error committing DART numbers in party aliasses on aln.ptynbr:'+ aln.ptynbr + ' ,ptyid:' + pr.ptyid + ' , Alias type:' + aln.type  + ' ,Alias Value:' + aln.alias
		    # Thys
		    ErrMsg = 'Error committing DART numbers in party aliasses on aln.ptynbr:'+ aln.ptynbr + ' ,ptyid:' + party_rec.ptyid + ' , Alias type:' + aln.type  + ' ,Alias Value:' + aln.alias
	    	    print ErrMsg
	    	    ael.log(ErrMsg)		    
    	    line=f.readline()
	    olddart, ptynbr, ptyid, newdart = string.split(line, ',')
change_dart('C:\\CPNewDart.csv')
