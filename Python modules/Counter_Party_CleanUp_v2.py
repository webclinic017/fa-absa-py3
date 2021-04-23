#Counterparty Fix Script that reads the counterparty from d:\Counter_Party\NewParty.TAB file.
#Counter_Party_Cleanup_v2 : 1 November 2003
#Be carefull, if the TAB file is present in the correct location
#by re-loading this script,it will start processing the info in the TAB
#file immediately!

import ael, string, os, time

def cparty_dart_update(file,*rest):

    updated=[]
    #if not file: file = 'c:\c.csv'
    f = open(file)
    ael.log('Started loading from %s.' % file)
    stored = [] # list of stored instruments
    line = f.readline()
    pty_counter=0
    line = line.replace ('"', '')
    ptynbr, newshort, oldshort, newfull, oldfull, dart, newdart= string.split(line, '\t')
    
    while ptynbr != "":
    	
	if ptynbr != 'ptynbr':
	    # Read party record
	    print "ptynbr", ptynbr
	    party_rec=ael.Party.read("ptynbr='%s'" % ptynbr)
	    if party_rec:
	    	pty_counter=pty_counter + 1
	    	# Update party information
	    	pr = party_rec.clone ()
#	    if pr.ptyid != newshort:
#	    	r = ael.Party.read('ptyid="' + newshort + '"')
#		if r == None:
#		    pr.ptyid = newshort[0:39]
#		else:
#	    	    pr.ptyid = newshort[0:30] + " " + ptynbr
#	    pr.ptyid = pr.ptyid.upper ()
    	    # Update PTY fullname only
#	    pr.fullname = newfull
	    	try:
	    	    CommitMsg = 'Committed party info for ' + pr.ptyid 
#	    	    pr.commit ()
#		    ael.log(CommitMsg)	
	    	except:
	    	    ErrMsg = 'Error committing party info on ptynbr ' + ptynbr + ',ptyid ' + pr.ptyid
		    print ErrMsg
		    ael.log(ErrMsg)
		
	    	# Update DART numbers in party aliasses
	    	party_rec_aliases=party_rec.aliases()
	    	#aliases_list=[]
	    	gotIt = 0
	    	for al in party_rec_aliases:
	    	    if al.type != None and al.type.alias_type_name == 'Dart_Number':
    		    	alc = al.clone()
		    	alc.alias = newdart.rstrip()
			print alc.alias
		    	try:
    	    	    	    CommitMsg = 'Committed party Dart alias info for ' + pr.ptyid
    		    	    alc.commit()
		    	    ael.log(CommitMsg)		    				
		    	except:
		    	    ErrMsg = 'Error committing DART numbers in party aliasses on ptynbr:'+ ptynbr + ' ,ptyid:' + pr.ptyid + ' ,Alias Value:' + alc.alias
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
		    	CommitMsg = 'Committed party new Dart alias info for ' + pr.ptyid
		    	aln.commit()
		    	ael.log(CommitMsg)		    	
		    except:
		    	ErrMsg = 'Error committing DART numbers in party aliasses on aln.ptynbr:'+ aln.ptynbr + ' ,ptyid:' + pr.ptyid + ' , Alias type:' + aln.type  + ' ,Alias Value:' + aln.alias
		    	print ErrMsg
		    	ael.log(ErrMsg)		    
	    else:
	    	print 'could not find the parrty with ptynbr = ', ptynbr 	    
	line=f.readline()
	line = line.replace ('"', '')
	ptynbr, newshort, oldshort, newfull, oldfull, dart, newdart= string.split(line, '\t')
	updated.append(ptynbr)
	
    pmsg = 'Processed ' + str(pty_counter) + ' parties.'
    ael.log(pmsg)
    msg = 'The following counterparties updated:' + str(updated)
    ael.log(msg)
    print msg


Start_Time = time.localtime()
print "Start time:", Start_Time
print "Start Counter Party Clean-UP 1..."
ael.log('Processing Party_Update.txt')
cparty_dart_update('C:\\Party.TAB')
Stop_Time=time.localtime()
print "Stop tmie: ", Stop_Time
print 'Finished Counter Party Clean-UP 2...'
