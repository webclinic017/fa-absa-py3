import ael, string
mainlist = []
not_cleaned = []
dart_update = []
addinfolist = ['Maize Diff', 'Safex Storage Rate', 'Silo Depot Code', 'Silo Storage Rate', 'Sorghum Diff', 'Sunflower Diff', 'Wheat Diff']

def set_party_add_info(party, add_info, value):
    """Set party's specified additional info to supplied value.
        
    party   	- ael Party entity  - Party that additional info refers to
    add_info	- string    	    - Name of add info field
    value   	- string    	    - Value to set add info field to

    Returns 1 if successful, else 0
    """

    try:
        
	existing_addinfos = {}

	for ai in party.additional_infos():

    	    existing_addinfos[ai.addinf_specnbr.field_name] = ai

	if existing_addinfos.has_key(add_info):

	    clone = existing_addinfos[add_info].clone()
	    clone.value = str(value)
	    clone.commit()

	else:

	    ai_spec = ael.AdditionalInfoSpec[add_info].clone()

	    new = ael.AdditionalInfo.new(ai_spec)

	    new.addinf_specnbr = ael.AdditionalInfoSpec[add_info].specnbr
	    new.value = str(value)
	    new.recaddr = party.ptynbr
	    new.commit()    
	
	return 1
    
    except:
    
    	return 0


def checknewptyid(ptyid, ptynbr):
    """ check the length and if the ID already exists  
    	return True or False.
    """
    party = ael.Party[(int)(ptynbr)]
    if party.ptyid == ptyid:
      	return 'True'
    if ptyid.__len__() > 69:
        return 'False'
    if ael.Party[ptyid]:
        return 'False'
    return 'True'
    
def check_prim_in_list(ptydart):
    ptynbr = []
    for p in ptydart:
    	ptynbr.append(p[1])
    status = 0
    for p in ptydart:
    	if p[3] in ptynbr:
	    print 'Primary party found in Grouping'    
    	else:
	    status = status + 1
	    party = ael.Party[(int)(p[1])]
    	    set_party_add_info(party, 'Cpty_AEL_Comment', 'Primary party not in dart list')	    
    if status > 0:
    	for t in ptydart:
	    not_cleaned.append(t[1])
    	return 0
    else:
    	return 1
    	    
def check_uniquenptyid(ptydart):
    """ Check if the list of parties has unique new partyid """
    list = []
    status = 0
    for p in ptydart:
    	if p[6] != '':
	    party = ael.Party[(int)(p[1])]
	    if p[6] not in list:
	    	list.append(p[6])
	    else:
	    	message = 'The New PartyID specified for the party: ' + party.ptyid + ' is already used, it must be changed to a valid one'
		ael.log(message)
		set_party_add_info(party, 'Cpty_AEL_Comment', 'New Partyid is not unique')
		status = status + 1
    if status == 0:
    	return 1
    else:
    	for p in ptydart:
	    not_cleaned.append(p[1])
    	return 0
	
    
def appendlist(list):
    mainlist.append(list)
    
    
def buildlist(filename):
    try:
    	f = open(filename, 'r')
    except:
    	print 'Error opening file'
    line = f.readline()
    line = f.readline()
    list = []
    while line:
    	line = line.rstrip('\n')
    	list = line.split('\t')
#    	ptynbr,parent,ptyid,type,delete,new_ptyid,nfull,ndart,comments,usecomm,usegen = line.split('\t')
#	print line
	#list.append(ptynbr)
	#list.append(parent)
	#list.append(ptyid)
	#list.append(ptytype)
	line = f.readline()
#	print list
	appendlist(list)
	list = []
   # print '\n----------------------------------------------------------------------------'
   # print mainlist
   # print '------------------------------------------------------------------------------\n'
    f.close()
    return mainlist
   
    
def build_list_per_dart(list, dartno):
    partyperdartlst = []
    for dart in list:
    	if dart[0] == dartno:
	    partyperdartlst.append(dart)
    return partyperdartlst
	    
def build_dartno_list(all_list):
    dartnolist = []
    for	party in all_list:
    	if party[0] not in dartnolist:
	    dartnolist.append(party[0])
    return dartnolist	
	        
def updatedart(party):
    print party[1]
    updateparty = ael.Party[(int)(party[1])]
    if not updateparty:
    	message = 'The party with partynbr: ' + party[1] + 'does not exist'
    	ael.log(message)
	print message
	return 0    
    gotIt = 0
    print updateparty.ptyid
    newdart = party[8]
    print newdart
    for al in updateparty.aliases():         
    	if al.type != None and al.type.alias_type_name == 'Dart_Number':
    	    alc = al.clone()
	    #print alc.type.alias_type_name
	    alc.alias = '%s' %newdart
	    #print alc.alias
	    try:
    	    	CommitMsg = 'Committed party Dart alias info for ' + updateparty.ptyid
    		alc.commit()
		ael.log(CommitMsg)
		ael.poll()
		return 1
	    except:
		ErrMsg = 'Error committing DART numbers in party aliasses on ptynbr:'+ party[1] + ' ,ptyid:' + party[3] + ' ,Alias Value:' + alc.alias
		ael.log(ErrMsg)
		not_cleaned.append(party[1])
		set_party_add_info(updateparty, 'Cpty_AEL_Comment', 'DartNumber not updated')
		return 0
	    gotIt = 1
    if gotIt == 0:
    	aln = al.new()
	aln.alias = newdart
	aln.type = ael.InstrAliasType['Dart_Number']
	aln.ptynbr = updateparty
	try:
	    CommitMsg = 'Committed party new Dart alias info for ' + updateparty.ptyid
	    aln.commit()
	    ael.log(CommitMsg)		    	
	    ael.poll()
	    return 1
	except:
	    ErrMsg = 'Error committing new DART numbers in party aliasses on aln.ptynbr:'+ aln.ptynbr + ' ,ptyid:' + updateparty.ptyid + ' , Alias type:' + aln.type  + ' ,Alias Value:' + aln.alias
    	    print ErrMsg
	    ael.log(ErrMsg)
    	    not_cleaned.append(party[1])
	    set_party_add_info(updateparty, 'Cpty_AEL_Comment', 'DartNumber not updated')
	    return 0
	    
	
def check_ird_trades(partyperdartlst):
    count_irdtrades = 0
    for p in partyperdartlst:
    	if ((p[12] == '1') and (p[11] == '1')):
	   count_irdtrades = count_irdtrades + 1
    if count_irdtrades > 1:
    	for pty in partyperdartlst:
	    party = ael.Party[(int)(pty[1])]
	    set_party_add_info(party, 'Cpty_AEL_Comment', 'More than 1 IRD trades no GenINFO')
	    not_cleaned.append(pty[1])    
    	return 0
    else:   
    	return 1
	
	
def check_comminfo(ptyperdartlist):
    countcomminfo = 0
    countusecom = 0
    for p in ptyperdartlist:
    	if p[5] == '1':
    	    party = ael.Party[(int)(p[1])]
	    if  party:
	    	maizedif = party.add_info('Maize Diff')
	    	safexstoragerate = party.add_info('Safex Storage Rate')
	    	silodepocode = party.add_info('Silo Depot Code')
	    	silostoragerate = party.add_info('Silo Storage Rate')
	    	sorghumdiff = party.add_info('Sorghum Diff')
	    	sundiff = party.add_info('Sunflower Diff')
	    	wheatdiff = party.add_info('Wheat Diff')
#	    print maizedif,safexstoragerate,silodepocode,silostoragerate,sorghumdiff,sundiff,wheatdiff
	    	if ((p[10] == '1') and (p[5] == '1')):
	    	    countusecom = countusecom + 1
	    	if ((maizedif != '') or (safexstoragerate != '') or (silodepocode != '') or 
	    	    (silostoragerate != '') or (sorghumdiff != '') or (sundiff != '') or (wheatdiff != '')):
	    	    countcomminfo = countcomminfo + 1
    	print countusecom, '--', countcomminfo
    if countusecom > 1:
	message = 'There are more than one indicator in the use commodities field for this grouping of the dart number: ' + p[0] + 'pleaase fix this'
	ael.log(message)
	for pty in ptyperdartlist:
    	    party = ael.Party[(int)(pty[1])]
	    set_party_add_info(party, 'Cpty_AEL_Comment', 'Commodity info more than 1 indic')
	    not_cleaned.append(pty[1])
	return 0
    if ((countusecom == 0) or (countusecom == 1)):
	return 1
    if ((countcomminfo > 1) and (countusecom == 0)):
	message = 'There are Commodities information on this party and no use commodities info flag has been set for the following dart number: ' + p[0]     
	ael.log(message)
	for pty in ptyperdartlist:
    	    party = ael.Party[(int)(pty[1])]
	    set_party_add_info(party, 'Cpty_AEL_Comment', 'Commodity info on party')
	    not_cleaned.append(pty[1])
	return 0

def copy_add_info(from_party, to_party, add_infos):
    """Copy additional info fields from one party to another.
    
    from_party 	- ael Party entity  - Copy from this party
    to_party   	- ael Party entity  - Copy to this party
    add_infos	- list	    	    - List of additional info fields to be copied.

    Returns 1 if successful, else 0
    """

    try:

	existing_addinfos = {}

	for ai in to_party.additional_infos():

    	    existing_addinfos[ai.addinf_specnbr.field_name] = ai

	for ai in add_infos:

    	    if existing_addinfos.has_key(ai):

		clone = existing_addinfos[ai].clone()
		clone.value = from_party.add_info(ai)
		clone.commit()

	    else:

		ai_spec = ael.AdditionalInfoSpec[ai].clone()

		new = ael.AdditionalInfo.new(ai_spec)

		new.addinf_specnbr = ael.AdditionalInfoSpec[ai].specnbr
		new.value = from_party.add_info(ai)
		new.recaddr = to_party.ptynbr
		new.commit()
	    ael.poll()
	return 1
	
    except:
    
	return 0
	
def check_HOSTID(partylist):
    counthostid = 0
    host = ''
    primlist = []
    sublist = []
    for pt in partylist:
    	if pt[3] not in primlist:
	    primlist.append(pt[3])
    for pr in primlist:
    	sublist.append(pr)
    	for sp in partylist:
	    if sp[3] == pr and sp[5] == '1':
	    	sublist.append(sp[1])
	for p in sublist:
    	    party = ael.Party[(int)(p)]
	    if party:
    	    	if party.hostid != '' and party.hostid != host:
	    	    counthostid = counthostid + 1
	    	    host = party.hostid
    	if counthostid > 1:
	    print 'fail HOSTID'
    	    message = 'There are more than one HOSTID for this group of parties with dartno: ' + p[0]
	    ael.log(message)
	    for pty in partylist:
    	    	party = ael.Party[(int)(pty[1])]
	    	set_party_add_info(party, 'Cpty_AEL_Comment', 'More than one Hostid')
	    	not_cleaned.append(pty[1])
    	    return 0
	else:
	    sublist = []
	    host = ''
	    counthostid = 0

    message = 'HostID is valid for this grouping of parties with dartno: ' + p[0]
    ael.log(message)
    return 1     
	    
def move_comm_info(ptydart):
    status = 0
    for p in ptydart:
    	if ((p[5] == '1') and (p[10] == '1')):
	    primary = ael.Party[(int)(p[3])]
	    subpty = ael.Party[(int)(p[1])]
	    if copy_add_info(subpty, primary, addinfolist) == 1:
	    	message = 'Successfull in moving the Commodities information from: ' + subpty.ptyid + ' to: ' + primary.ptyid
		ael.log(message)
		status = status
	    else:
	    	status = status + 1
		message = 'Error in moving the Commodities information from: ' + subpty.ptyid + ' to: ' + primary.ptyid
		ael.log(message)
		set_party_add_info(subpty, 'Cpty_AEL_Comment', 'Could not copy com inf')
		not_cleaned.append(p[1]) 
    if status == 0:
    	return 1
    else:
    	return 0


def move_HostID(partylist):
    status = 0
    for p in partylist:
    	if p[5] == '1':
    	    party = ael.Party[(int)(p[1])]
    	    if party:
	    	if party.hostid != '':
	    	    primpty = ael.Party[(int)(p[3])].clone()
	    	    primpty.hostid = party.hostid
	    	    try:
	    	    	primpty.commit()
		    	message = 'HostId has been succesfully move to the pimary party: ' + primpty.ptyid
		    	ael.log(message)
		    	ael.poll()
	    	    except:
	    	    	message = 'The Host Id could not be moved the primary party: ' + primpty.ptyid + ' please look at the detail' 
		    	status = status + 1
		    	set_party_add_info(party, 'Cpty_AEL_Comment', 'Could not move hostid')
		    	not_cleaned.append(p[1])
    if status == 0:
    	return 1
    else:
    	return 0

def move_accounts(from_party, to_party):
    """Move all accounts referencing the from_party to the to_party.
    
    from_party	- ael Party entity  	- Move accounts from this party
    to_party	- ael Party entity  	- Move accounts to this party
 
    This check if there is IRD Accountsalready specified and 
    only moves if there is no ird accounts or if the accounting field is not equal to IRD
    
    Returns 1 if successful, else 0.
    """
    ael.poll()
    name = []
    try:
    	topty_clone = to_party.clone()
	to_acc = to_party.accounts()
	flag = 0
	for acc in to_acc:
	    name.append(acc.name)
	    if acc.accounting == 'IRD':
	    	flag = 1
   	
	accounts = from_party.accounts()
	
	for account in accounts:
	    print account.accounting, flag, from_party.ptyid
	    if (account.accounting == 'IRD') and (flag == 1):
	    	print 'IRD Account already exists'
	    else:
	    	ac = ael.Account.new(topty_clone)
	    	ac.ptynbr = to_party
		ac.name = account.name
		ac.account = account.account		
		ac.account2 = account.account2
		ac.account3 = account.account3
		ac.account4 = account.account4
    	    	ac.accounting = account.accounting		
		ac.correspondent_bank2_ptynbr = account.correspondent_bank2_ptynbr
		ac.correspondent_bank3_ptynbr = account.correspondent_bank3_ptynbr
		ac.correspondent_bank4_ptynbr = account.correspondent_bank4_ptynbr
		ac.correspondent_bank_ptynbr = account.correspondent_bank_ptynbr
		ac.curr = account.curr
		ac.depository = account.depository
		ac.depository2 = account.depository2
		ac.depository3 = account.depository3
		ac.depository4 = account.depository4
		ac.details_of_charges = account.details_of_charges
		ac.network_alias_type = account.network_alias_type
		ac.swift = account.swift
		ac.swift2 = account.swift2
		ac.swift3 = account.swift3
    	    	ac.swift4 = account.swift4
		if ac.name not in name:
		    ac.commit()
		else:
		    print 'Name Exists'
		if account.accounting == 'IRD':
	    	    flag = 1
    	return 1
    except:
	print 'account update failed!!!!!!!!'   
	return 0

def move_acc_all(ptydart):
    status = 0
    for p in ptydart:
    	if p[5] == '1':
	    primpty = ael.Party[(int)(p[3])] 
	    subpty = ael.Party[(int)(p[1])]
	    if (subpty and primpty):
	    	if move_accounts(subpty, primpty) == 1:
	    	    message = 'Success in moving the Accounts on party: ' + subpty.ptyid + ' to: ' + primpty.ptyid
		    ael.log(message)
    	    	else:
	    	    message = 'Failed to move the Accounts on party: ' + subpty.ptyid + ' to: ' + primpty.ptyid
		    ael.log(message)   
		    not_cleaned.append(p[1])
		    set_party_add_info(subpty, 'Cpty_AEL_Comment', 'Acc could not be moved')
		    status = status + 1
	    
    if status > 0:
    	return 0
    else:
    	return 1

def check_contactrule(partylist):
    status = 0
    for p in partylist:
    	for t in partylist:
    	    if p[5] == '1':
	    	pty = ael.Party[(int)(p[1])]
	    	party = ael.Party[(int)(p[1])].contacts()
	    	tcontacts = ael.Party[(int)(t[1])].contacts()
	    	if len(party) > 0 and len(tcontacts) > 0 and t[1] != p[1]:
	    	    for pcontact in party:
		    	for tcontact in tcontacts:
		    	    for prule in pcontact.rules():
			    	for trule in tcontact.rules():
			    	    if ((prule.curr == trule.curr) and (prule.event_chlnbr == trule.event_chlnbr) and (prule.instype == trule.instype)):
				    	message = 'There are contact rules that are the same for these parties and can not be deleted please look into this for party: ' + p[1]
				    	ael.log(message)
					status = status + 1
					set_party_add_info(pty, 'Cpty_AEL_Comment', 'The same contact rule exists already')
					not_cleaned.append(p[1])
    if status > 0:
    	return 0
    else:
    	return 1

def move_contacts(from_party, to_party):
    """Move all contacts referencing the from_party to the to_party.
    
    from_party	- ael Party entity  	- Move contacts from this party
    to_party	- ael Party entity  	- Move contacts to this party
 
    This had to be done using SQL, ael object changes were consistently reversed.
    
    Returns 1 if successful, else 0.
    """

    try:
    
    	ael.dbsql('BEGIN TRANSACTION')
	
	contacts = from_party.contacts()
	for contact in contacts:
	    contactcount = 0
	    for primcontact in to_party.contacts():
	    	#print 'FROM:', contact.fullname, contact.attention, 'TO:', primcontact.fullname, primcontact.attention
	    	if ((contact.fullname == primcontact.fullname) and (contact.attention == primcontact.attention) and (contact.address == primcontact.address) and (contact.address2 == primcontact.address2) and (contact.zipcode == primcontact.zipcode) and (contact.city == primcontact.city) and (contact.country == primcontact.country) and (contact.telephone == primcontact.telephone) and (contact.fax == primcontact.fax)):
		    contactcount = 1
		    for fr_rule in contact.rules():
		    	count = 0
		    	for to_rule in primcontact.rules():
	    	    	    if (to_rule.curr == fr_rule.curr) and (to_rule.event_chlnbr == fr_rule.event_chlnbr) and (to_rule.instype == fr_rule.instype):
    			    	count = count + 1
			if count == 0:
			    SQL = '''UPDATE 
			    	    	contact_rule 
				     SET 
				     	contact_seqnbr = %d
				     where
				     	seqnbr = %d ''' % (primcontact.seqnbr, fr_rule.seqnbr)
			    ael.dbsql(SQL)  
		#	    print 'Move Rule'
	    #print 'COUNT',contactcount
	    if contactcount == 0:
	    	print	
		SQL = '''
	    	    UPDATE
	    	    	contact
	    	    SET
	    	        ptynbr = %d
	    	    WHERE
	    	        ptynbr = %d
	    	    ''' % (to_party.ptynbr, from_party.ptynbr)
	    
    	    	ael.dbsql(SQL)
	    	#print 'Move Contact Line 477'
	  
	ael.dbsql('COMMIT TRANSACTION')
    
    	return 1
    
    except:
    
    	ael.dbsql('ROLLBACK TRANSACTION')
	
	return 0

def move_contacts_all(ptydart):
    status = 0
    for p in ptydart:
    	if p[5] == '1':
	    print p[3]
	    primpty = ael.Party[(int)(p[3])] 
	    subpty = ael.Party[(int)(p[1])]
	    if subpty:
	    	if (move_contacts(subpty, primpty) == 1):
	    	    status = 0
		    message = 'Success in moving the contact information from: ' + subpty.ptyid + ' to: ' + primpty.ptyid
		    ael.log(message)
	    	else:
	    	    status = status + 1
		    message = 'Error in moving the contact information from: ' + subpty.ptyid + ' to: ' + primpty.ptyid    
		    not_cleaned.append(p[1])
		    set_party_add_info(subpty, 'Cpty_AEL_Comment', 'Contacts not moved')
		    ael.log(message)
		
    if status == 0:
    	return 1
    else:
    	return 0	    	
	
def check_alias_value(al, primary):
    for a in primary.aliases():
#    	print al.pp(), a.pp(), al.type.pp(), a.type.pp()
#    	print al.type.alias_type_name, a.type.alias_type_name, a.alias, al.alias, ((al.type.alias_type_name == a.type.alias_type_name) and (a.alias == al.alias)),'line362'     	    
    	if al.type and a.type:
    	    if ((al.type.alias_type_name == a.type.alias_type_name) and (a.alias == al.alias)):
	    	message = 'The Alias Already exists'
	    	ael.log(message)
	    	return 0
    return 1
    
def check_reuters(ptydart):
    count = 0
    primlist = []
    sublist = []
    for pt in ptydart:
    	if pt[3] not in primlist:
	    primlist.append(pt[3])
    for pr in primlist:
    	print pr
    	sublist.append(pr)
    	for sp in ptydart:
	    if sp[3] == pr and sp[5] == '1':
	    	sublist.append(sp[1])
	name = ''
	for p in sublist:
    	    party = ael.Party[(int)(p)]
	    if party:
	    	for al in party.aliases():
	    	    if al.type:
	    	    	if al.type.alias_type_name == 'Reuters' and al.alias != '' and name != al.alias:
		    	    name = al.alias
			    count = count + 1
	print count
	print '***********'
    	if count > 1:
    	    for p in ptydart:
	    	not_cleaned.append(p[1])
		subpty = ael.Party[(int)(p[1])]
    	    	set_party_add_info(subpty, 'Cpty_AEL_Comment', 'More than one reuters code')
	    return 0
    	else:
	    sublist = []
	    count = 0
    return 1
	    
def copy_aliases(from_party, to_party):
    """Copy party aliases from one party to another.
    
    from_party 	- ael Party entity  - Copy from this party
    to_party   	- ael Party entity  - Copy to this party
    aliases	- list	    	    - List of aliases to be copied.
    """
    parent_party = to_party.clone()
    if from_party:
    	for al in from_party.aliases():
    
#    	print al.pp(), parent_party.ptyid, 'line377'
#    	print al.type.alias_type_name, '--', al.alias
    	    if check_alias_value(al, parent_party):
	    	if al.alias != '':
    	    	    new = ael.PartyAlias.new(parent_party)
    	    	    new.type = al.type
    	    	    new.alias = al.alias
    	    	    new.ptynbr = to_party.ptynbr
#		    print new.pp()
#		print 'CCCCCCCCHHHHHHHHHHHEEEEEEEECCCCCCCCCCCCKKKKKKKKK', 'line387'
#		for ppp in parent_party.aliases():
#		    print ppp.alias, ppp.type.alias_type_name
	    	    try:
    	    	    	new.commit()
		    	ael.poll()
		    	message = 'Alias of type ' + al.type.alias_type_name + ' has been moved to the parent party : ' + to_party.ptyid
		    	ael.log(message)
		    	return 1
	    	    except:
	    	    	message = 'Failed to move the alias of type ' + al.type.alias_type_name + ' to the parent party: ' + to_party.ptyid
	    	    	ael.log
		    	return 0
	    else:
	    	message = 'The alias of type: ' + al.type.alias_type_name + ' already exists for party: ' + parent_party.ptyid
	    	ael.log(message)
    return 1



def move_alias(partylist):
    status = 0
    for p in partylist:
    	if p[5] == '1':
	    primpty = ael.Party[(int)(p[3])]
	    subpty = ael.Party[(int)(p[1])]
	    if (primpty and subpty):
    	    	if copy_aliases(subpty, primpty):
	    	    status = status
		    message = 'Successfull in moving the aliases from: ' + subpty.ptyid + ' to: ' + primpty.ptyid
		    ael.log(message)     
	    	else:
	    	    status = status + 1
		    message = 'Unable to move the aliases from: ' + subpty.ptyid + ' to: ' + primpty.ptyid
		    ael.log(message)
		    not_cleaned.append(p[1])
		    set_party_add_info(subpty, 'Cpty_AEL_Comment', 'Not all aliases could be moved')
    if status == 0:
    	return 1
    else:
    	return 0

	    
def move_gen_info(ptydart):
    status = 0
    for p in ptydart:
    	if p[11] == '1':
	    primpty = ael.Party[(int)(p[3])].clone()
	    subpty = ael.Party[(int)(p[1])]
	    primpty.attention = subpty.attention
	    primpty.address = subpty.address
	    primpty.address2 = subpty.address2
	    primpty.zipcode = subpty.zipcode
	    primpty.city = subpty.city
	    primpty.country = subpty.country
	    primpty.telephone = subpty.telephone
	    primpty.fax = subpty.fax
	    primpty.telex = subpty.telex
	    primpty.swift = subpty.swift
	    primpty.email = subpty.email
	    primpty.contact1 = subpty.contact1
    	    primpty.contact2 = subpty.contact2	    	    	    
	    try:
	    	primpty.commit()
		message = 'General information from: ' + subpty.ptyid + ' has been moved to the parent party: ' + primpty.ptyid
		ael.log(message)
		status = status
		ael.poll() 
	    except:
	    	message = 'Error in trying to move the general information from: ' + subpty.ptyid + ' to the parent: ' + primpty.ptyid
	    	ael.log(message)
		status = status + 1
		not_cleaned.append(party[1])
		set_party_add_info(subpty, 'Cpty_AEL_Comment', 'General info not moved')
    if status == 0:
    	return 1
    else:
    	return 0
    		
		
		
def move_issuer(ptydart):
    status = 0
    for p in ptydart:
    	if p[5] == '1':
    	    primpty = ael.Party[(int)(p[3])].clone()
	    subpty = ael.Party[(int)(p[1])]
	    if (subpty and primpty):
	    	if subpty.issuer == 1:
	    	    primpty.issuer = 1	    
	    	if subpty.correspondent_bank == 1:
	    	    primpty.correspondent_bank = 1
	    	if subpty.isda_member == 1:
	    	    primpty.isda_member = 1
	    	if subpty.netting == 1:
	    	    primpty.netting = 1
	    	if subpty.notify_receipt == 1:
	    	    primpty.notify_receipt = 1
	    	try:	
	    	    primpty.commit()
		    status = status
		    message = 'The issuer tick and other ticks has been moved from: ' + subpty.ptyid + ' to party: ' + primpty.ptyid
		    ael.log(message)
		    ael.poll()
	    	except:
	    	    status = status + 1
		    message = 'The issuer tick and other ticks has not been moved from: ' + subpty.ptyid + ' to party: ' + primpty.ptyid
		    ael.log(message)
		    not_cleaned.append(p[1])
		    set_party_add_info(subpty, 'Cpty_AEL_Comment', 'The Issuer and other tick has not been moved')
    if status == 0:
    	return 1
    else:
    	return 0
		
     	    
def update_otherinfo(ptydart):
    status = 0
    for p in ptydart:
    	if p[5] != '1':
	    primpty = ael.Party[(int)(p[3])]
	    print primpty.ptyid, primpty.ptynbr, 'primpty '
	    sub = ael.Party[(int)(p[1])]
	    if sub:
    	    	print sub.ptyid, sub.ptynbr, 'sub	    '
	    	subpty = sub.clone() #ael.Party[(int)(p[1])].clone()	    
	    	if p[4] == 'Full Branch':
	    	    subpty.parent_ptynbr = primpty
		    chlnbr = ael.ChoiceList.read('list = "%s" and entry = "%s"' % ('Relation', 'Full Branch'))
		    subpty.relation_chlnbr = chlnbr
	    	if p[4] == 'Subsidiary':
	    	    subpty.parent_ptynbr = primpty
		    chlnbr = ael.ChoiceList.read('list = "%s" and entry = "%s"' % ('Relation', 'Subsidiary'))
		    subpty.relation_chlnbr = chlnbr
	    	if p[4] == 'Sub Account':
	    	    subpty.parent_ptynbr = primpty
		    chlnbr = ael.ChoiceList.read('list = "%s" and entry = "%s"' % ('Relation', 'Sub Account'))
		    subpty.relation_chlnbr = chlnbr
	    	if p[4] == 'Asset Manager':
	    	    subpty.parent_ptynbr = primpty
		    chlnbr = ael.ChoiceList.read('list = "%s" and entry = "%s"' % ('Relation', 'Fund'))
		    subpty.relation_chlnbr = chlnbr
	    	if p[4] == 'Fund':
	    	    subpty.parent_ptynbr = primpty
		    chlnbr = ael.ChoiceList.read('list = "%s" and entry = "%s"' % ('Relation', 'Fund'))
		    subpty.relation_chlnbr = chlnbr
	    	if p[4] == 'Silo Location':
	    	    subpty.parent_ptynbr = primpty
		    chlnbr = ael.ChoiceList.read('list = "%s" and entry = "%s"' % ('Relation', 'Silo Location'))
		    subpty.relation_chlnbr = chlnbr
		if p[4] == 'Division':
    	    	    subpty.parent_ptynbr = primpty
		    chlnbr = ael.ChoiceList.read('list = "%s" and entry = "%s"' % ('Relation', 'Division'))
		    subpty.relation_chlnbr = chlnbr
	    	try:
	    	    subpty.commit()
		    message = 'Asset Manager/Branch/Subsidary status has been set for the party: ' + subpty.ptyid
		    ael.log(message)
		    ael.poll()
	    	except:
	    	    status = status + 1
		    message = 'Asset Manager/Branch/Subsidary status has not been set for the party: ' + subpty.ptyid
		    ael.log(message)
		    not_cleaned.append(p[1])
		    set_party_add_info(sub, 'Cpty_AEL_Comment', 'Could not set Asset Mngr and other')
    if status == 0:
    	return 1
    else:
    	return 0
	    	

def move_payments(from_party, to_party):
    """Move all payments referencing the from_party to the to_party.  
    
    from_party	    - ael Party entity	- Move payments from this party
    to_party	    - ael Party entity	- Move payments to this party    

    Returns 1 if sucessful, else 0
    """

    try:

	payments = from_party.payments()

	for payment in payments:

    	    clone = payment.clone()
	    clone.ptynbr = to_party
	    clone.commit()
	    
	return 1
	
    except:
    
	return 0
	
def set_trade_add_info(trade, add_info, value):
    """Set trade's specified additional info to supplied value.
        
    trade   	- ael Trade entity  - Trade that additional info refers to
    add_info	- string    	    - Name of add info field
    value   	- string    	    - Value to set add info field to

    No transactions or return value as this function is intended to be called
    from within other functions.
    """
    
    existing_addinfos = {}

    for ai in trade.additional_infos():
    
    	existing_addinfos[ai.addinf_specnbr.field_name] = ai
  
    if existing_addinfos.has_key(add_info):

	clone = existing_addinfos[add_info].clone()
	clone.value = str(value)
	clone.commit()
    else:

	ai_spec = ael.AdditionalInfoSpec[add_info].clone()

	new = ael.AdditionalInfo.new(ai_spec)

	new.addinf_specnbr = ael.AdditionalInfoSpec[add_info].specnbr
	new.value = str(value)
	new.recaddr = trade.trdnbr
	new.commit()    



	
def move_trades(from_party, to_party, add_info):
    """Move all trades referencing the from_party (as broker, acquirer or counterparty) 
    	to the to_party.  
	
    from_party 	- ael Party entity  - Move from this party
    to_party   	- ael Party entity  - Move to this party
    add_info	- string    	    - Name of add info field that will hold
    	    	    	    	    	the ptynbr of the original counterparty.
    Returns 1 if successful, else 0
    """

    try:

	trades = ael.Trade.select('counterparty_ptynbr = %d' % (from_party.ptynbr))

	for trade in trades:

    	    clone = trade.clone()
	    clone.counterparty_ptynbr = to_party
	    if trade.add_info('Cpty_Original_Cpty') == '':	
	    	set_trade_add_info(trade, add_info, from_party.ptynbr)
	    clone.commit()

	trades = ael.Trade.select('acquirer_ptynbr = %d' % (from_party.ptynbr))
    	if len(trades) > 0:
	    if to_party.type == 'Internal Dept':
	    
	    	for trade in trades:
           	    clone = trade.clone()
	    	    clone.acquirer_ptynbr = to_party	    
	    	    clone.commit()
	    else:
	    	return 0

	trades = ael.Trade.select('broker_ptynbr = %d' % (from_party.ptynbr))
    	if len(trades) > 0:
	    if to_party.type == 'Broker':
	    	for trade in trades:
        	    clone = trade.clone()
	    	    clone.broker_ptynbr = to_party
	    	    clone.commit()
	    else:
	    	return 0

	trades = ael.Instrument.select('issuer_ptynbr = %d' % (from_party.ptynbr))
    	if len(trades) > 0:
	    if to_party.issuer == 1:
	    	for trade in trades:
        	    clone = trade.clone()
	    	    clone.issuer_ptynbr = to_party
	    	    clone.commit()
	    else:
	    	return 0
    	ael.poll()
	return 1
    except:
    
	return 0

def move_payments(from_party, to_party):
    """Move all payments referencing the from_party to the to_party.  
    
    from_party	    - ael Party entity	- Move payments from this party
    to_party	    - ael Party entity	- Move payments to this party    

    Returns 1 if sucessful, else 0
    """

    try:

	payments = from_party.payments()

	for payment in payments:

    	    clone = payment.clone()
	    clone.ptynbr = to_party
	    clone.commit()
	ael.poll()    
	return 1
	
    except:
    
	return 0

		
def move_trades_all(ptydart):
    status =  0
    for p in ptydart:
    	if p[5] == '1':
    	    primpty = ael.Party[(int)(p[3])]
	    subpty = ael.Party[(int)(p[1])]
	    if (primpty and subpty):
	    	if move_trades(subpty, primpty, 'Cpty_Original_Cpty') == 1:
	    	    message = 'Success in moving the trades from: ' + subpty.ptyid + ' to: ' + primpty.ptyid    
		    ael.log(message)
		    status = status
    	    	else:
	    	    message = 'Failed in moving the trades from: ' + subpty.ptyid + ' to: ' + primpty.ptyid
		    ael.log(message)
		    status = status + 1
		    not_cleaned.append(p[1])
		    set_party_add_info(subpty, 'Cpty_AEL_Comment', 'Trades/Acq/Issuer not moved')
    if status == 0:
    	return 1
    else:
    	return 0
    
				
def move_all_payments(ptydart):
    status = 0
    for p in ptydart:
    	if p[5] == '1':
	    primpty = ael.Party[(int)(p[3])]
	    subpty = ael.Party[(int)(p[1])]
	    if (subpty and primpty):
	    	if move_payments(subpty, primpty) == 1:
	    	    message = 'Sucess in movin the payments from: ' + subpty.ptyid + ' to: ' + primpty.ptyid
		    ael.log(message)
    	    	    status = status
	    	else:
	    	    message = 'Error in moving the payments from: ' + subpty.ptyid +  ' to: ' + primpty.ptyid
	    	    ael.log(message)
		    status = status + 1
		    not_cleaned.append(p[1])
		    set_party_add_info(pty, 'Cpty_AEL_Comment', 'Payments not moved')
    if status == 0:
    	return 1
    else:
    	return 0

def copy_settle_instruct(from_pty, to_pty):
    ssi = ael.SettleInstruction.select('counterparty_ptynbr = "%d"' %(from_pty.ptynbr))
    for s in ssi:
	sclone = ael.SettleInstruction.new()
	sclone.counterparty_ptynbr = to_pty.ptynbr
	sclone.settleid = s.settleid
	sclone.acquirer_ptynbr = s.acquirer_ptynbr
	sclone.curr = s.curr
	sclone.settle_category_chlnbr = s.settle_category_chlnbr
	sclone.money_us_accnbr = s.money_us_accnbr
	sclone.money_cp_accnbr = s.money_cp_accnbr
	sclone.sec_us_accnbr = s.sec_us_accnbr
	sclone.sec_cp_accnbr = s.sec_cp_accnbr
	sclone.effective_from = s.effective_from
	sclone.effective_to  =  s.effective_to
	try:
    	    sclone.commit()
	    message = 'Success in moving the SSI form: ' + from_pty.ptyid + ' to: ' + to_pty.ptyid
	    ael.log(message)
	    ael.poll()
    	except:
	    message = 'Unable to move the SSI from: ' + from_pty.ptyid + ' to: ' + to_pty.ptyid
    	    ael.log(message)
    	    return 0
    return 1
    
def move_all_SSI(ptydart):
    status = 0
    for p in ptydart:
    	if p[5] == '1':
	    primpty = ael.Party[(int)(p[3])]
	    subpty = ael.Party[(int)(p[1])]
	    if (primpty and subpty):
	    	if copy_settle_instruct(subpty, primpty) == 1:
	    	    print 'SSI has been moved from: ', subpty.ptyid, ' to: ', primpty.ptyid
	    	else:
	    	    status = status + 1
		    not_cleaned.append(p[1])
		    set_party_add_info(subpty, 'Cpty_AEL_Comment', 'Could not move SSI')
    if status > 0:
    	return 0
    else:   
    	return 1
    
def change_ptyid_and_fullname(ptydart):
    status = 0
    for p in ptydart:
    	pt = ael.Party[(int)(p[1])]
	if pt:
    	    party = pt.clone()
	    pc = ael.Party[(int)(p[1])]
	    if (party and pc):
    	    	if p[6] != '' and p[5] != '1':
	    	    if ael.Party[(int)(p[1])].add_info('Cpty_Old_Ptyid') == '':
	    	    	set_party_add_info(pc, 'Cpty_Old_Ptyid', pc.ptyid)
	    	    else:
	    	    	print 'Already has an old ptyid: ', pc.add_info('Cpty_Old_Ptyid')
	    	    id = '%s' %(p[6][0:39])
	    	    id = id.lstrip()
	    	    id = id.rstrip()
	    	    party.ptyid = id
    	    	if ((p[7] != '') and (p[5] != '1')):
	    	    if len(p[7]) > 65:
	    	    	full1 = p[7][0:64]
		    	full1 = full1.lstrip()
		    	full1 = full1.rstrip()
		    	party.fullname = full1
		    	full2 = p[7][65:(len(p[7])-1)]
		    	full2 = full2.lstrip()
		    	full2 = full2.rstrip()
		    	party.fullname2 = full2
	    	    else: 
    	    	    	full = p[7]
		    	full = full.lstrip()
		    	full = full.rstrip()
	    	    	party.fullname = full
	    	try:
	    	    party.commit()
	    	    message = 'Fullname and partyid has been changed for party: ' + pc.ptyid
	    	    ael.log(message)
	    	    ael.poll()
    	    	except:
	    	    status = status + 1
	    	    not_cleaned.append(p[1])
	    	    set_party_add_info(pc, 'Cpty_AEL_Comment', 'Fullname PTYID could not be changed')
	    	    message = 'Failed to update the Fullname or Ptyid for party: ' + pc.ptyid
    	    	    ael.log(message)
    	
    if status == 0:
    	return 1
    else:
    	return 0

def remove_issuer(ptydart):
    status = 0
    for p in ptydart:
    	if p[5] == '1':
	    party = ael.Party[(int)(p[1])]
	    if party:
	    	if party.issuer == 1:
	    	    partyclone = party.clone()
		    partyclone.issuer = 0
		    print party.ptyid
		    try:
		    	partyclone.commit() 
		    
		    except:
		    	message = 'The issuer tab could not be moved for party: ' + party.ptyid
		    	ael.log(message)
		    	status = status + 1
		    	not_cleaned.append(p[1])
    ael.poll()
    if status > 0:
    	return 0
    else:
    	return 1
    	

def set_addinfos(ptydart, add_info):
    status = 0
    for p in ptydart:
    	if p[1] not in not_cleaned:
    	    party = ael.Party[(int)(p[1])]
	    if party:	    
	    	if p[5] == '1':
	    	    if set_party_add_info(party, add_info, 'Yes'):
		    	print 'Delete Addinfo set'
		    else:
		    	print 'Delete Addinfo not set'
		    ael.poll()   
		    party = ael.Party[(int)(p[1])] 
		    pc = party.clone()
  	    	    pc.type = 'None'
	    	    try:    
	    	    	pc.commit()
		    	status = status
		    	message = 'Party type has been set to "None" for party: ' + party.ptyid
		    	ael.log(message)
	    	    except:
	    	    	status = status + 1
		    	message = 'Party type could not be set to "None" for party: ' + party.ptyid
		    	ael.log(message)
		    	not_cleaned.append(p[1])
		    	set_party_add_info(party, 'Cpty_AEL_Comment', 'Could not set to none')
    	    	    print '*****TYPE **********', ael.Party[(int)(p[1])].type, 'line 1070'
    if status == 0:
    	return 1
    else:
    	return 0
	    

def set_aelcleaned(ptydart):
    status = 0
    for p in ptydart:
    	if (p[1] not in not_cleaned) and (p[1] not in dart_update):
    	    party = ael.Party[(int)(p[1])]
	    if set_party_add_info(party, 'Cpty_AEL_Status', 'AEL_Cleaned') == 1:
	    	status = status
		message = 'Cpty_AEL_Status has been updated to AEL_Cleaned for party: ' + p[1]
		ael.log(message)
		set_party_add_info(party, 'Cpty_AEL_Comment', '')    
	    else:
	    	status = status + 1
		message = 'Cpty_AEL_Status could not be updated to AEL_Cleaned for party: ' + p[1]		
		ael.log(message)

    if status == 0:
    	return 1
    else:
    	return 0
	
def set_aelfailed(ptydart):
    status = 0
    for e in not_cleaned:
    	party = ael.Party[(int)(e)]	
	if set_party_add_info(party, 'Cpty_AEL_Status', 'AEL_Failed') == 1:
	    status = status
	    message = 'Cpty_AEL_Status has been updated to AEL_Failed for party: ' + e
	    ael.log(message)
    	else:
	    status = status + 1
	    message = 'Cpty_AEL_Status could not be updated to AEL_Failed for party: ' + e		
	    ael.log(message)
    if status == 0:
    	return 1
    else:
    	return 0    

def move_list(ptydart):
    for p in ptydart:
    	not_cleaned.append(p[1])
		
def ael_main(ae_dict):
    errorlist = []
    completedlist = []
    fullList = buildlist('\\\\atlasprd\\Cpty_Cleanup\\Export.tab')
#    fullList = buildlist('C:\\Export.tab')    
    for l in fullList:
    	flag = 0
	pty = ael.Party[(int)(l[1])]
    	if l[6] != '':
	    if checknewptyid(l[6], l[1]) == 'False':
	    	message =  'Error with new partyid: ' + l[1] + ' new id = ' + l[6]
		ael.log(message)
		not_cleaned.append(l[1])
		set_party_add_info(pty, 'Cpty_AEL_Comment', 'Partyid not correct')				
	    else:
	    	message = 'New partyid is valid for party: ' + l[1]
		ael.log(message)		
		flag = 1
    	else:
	    message = 'No new partyid specified'
	    ael.log(message)
	    flag = 1
#	print message
#	print '------'
#	print l[1]
#	print '------'
	pty = ael.Party[(int)(l[1])]
    	if flag == 0: 
	    errorlist.append(l[0])
	if l[8] != '0':
	    if (updatedart(l) == 1):
	    	print 'DART NO = ', l[8]
	    	message = 'Dart number has been changed'    
		ael.log(message)		
    	    	set_party_add_info(pty, 'Cpty_AEL_Status', 'AEL_DART#')
    	    	dart_update.append(l[1])    		
    alldartno = build_dartno_list(fullList)
    print '*************************************'
    print alldartno	
    print '*************************************'    
    for dartn in alldartno:
    	error = 0
    	ptydart = build_list_per_dart(fullList, dartn)
	print '-------------------------------------------------------------'
	print 'Started the Cleanup process for the dart no: ', ptydart[0][0]
	print '-------------------------------------------------------------'
	print ptydart
	if check_uniquenptyid(ptydart) == 1:
	    message = 'The New  Party Id specified for the dart number: ' + dartn + ' is Valid'
	    ael.log(message)
	    print message
	else:
	    error = 1
	    message = 'There was a duplication of new party id s in the list'
	    ael.log(message)
	    print message
    	    move_list(ptydart)
	if error != 1:
	    if (check_prim_in_list(ptydart) == 1):
	    	print 'Primary parties is in list of dartno'
	    else:
	    	print 'There is a primary party that is not in the list for this darno'
		error = 1	    
	if error != 1:
	    if check_comminfo(ptydart) == 1:
	    	if move_comm_info(ptydart) == 1:
	    	    message = 'Success in moving Commodities info to Primary party'
	    	    ael.log(message)
	    	else:
	    	    message = 'Commodities info could not be moved to the primary party process has been stopped' + dartn
		    ael.log(message)
	    	    error = 1
		    move_list(ptydart)
	    else:
	    	error = 1
		move_list(ptydart)   
	if error != 1:
	    if check_HOSTID(ptydart) == 1:
	    	if move_HostID(ptydart) == 1:
	    	    print 'Success in moving the Host Id'
	    	else:
		    print 'Could not move Host Id'
	    	    error = 1
		    move_list(ptydart)
	    else:
	    	print 'There are more than one Hostid in this party'
	    	error = 1
		move_list(ptydart)
	if error != 1:
	    if ((check_reuters(ptydart)) == 1):
	    	print 'Reuters code check succesfull'
	    else:
	    	print 'Reuters code check Failed'
		error = 1
		move_list(ptydart)
		
#	if error != 1:    
#	    if check_contactrule(ptydart) == 1:
#	    	print 'Contact rules successfull'
#	    else:
#	    	print 'Error with applying the contact rules check. Contact rules are conflicting for dartno: ',dartn  
#	    	error = 1
#		move_list(ptydart)
	if error != 1:
	    if move_contacts_all(ptydart) == 1:
	    	print 'Success in moving the contact rules'
	    else:
	    	print 'Contact rules has not been moved'
		
	if error != 1:
    	    if move_alias(ptydart) == 1:
	    	print 'Success in moving the alias from deleted party to the primary party for the following dart number: ', dartn
	    else:
	    	print 'Alias fields could not be moved'
		
	if error != 1:
    	    if move_gen_info(ptydart) == 1:
	        print 'Success in moving the general information to the primary party for the following dart no: ', dartn   
    	    else:
	        error = 1
		move_list(ptydart)
		
	if error != 1:	    
	    if move_issuer(ptydart):
	    	print 'Success in moving the Issuer and other to the parent party for dartno: ', dartn
    	    else:
	    	print 'Could not move the Issuer and other info to the parent party'
		
    	if error != 1:		
	    if update_otherinfo(ptydart):
	    	print 'Successfull in updating the Branch/Subsidiary/AssetManager information for the dartno: ', dartn
	    else:
    	    	print 'Could not set the other information for the Branch/Subsidiary/AssetManager'
		
	if error != 1:	 
	    if move_trades_all(ptydart):
	    	print 'Trades has been moved to the primary party from parties to be deleted'
	    else:
	    	print 'Trades have not been moved to the primary party'
		
	if move_acc_all(ptydart):
	    print 'Account information was successfully moved for dart number: ', dartn
	else:
	    print 'Account information was not successfully moved for dart number: ', dartn
	    
	if error != 1:
	    if move_all_payments(ptydart):
	    	print 'Additional Payments has been moved to the parent party: ', dartn
	    else:
	    	print 'Additional Payments has not been moved to the parent party' 
		
	if error != 1:
	    if move_all_SSI(ptydart):
	    	print 'Success in moving the SSIs for the dart number: ', dartn
	    else:
	    	print 'Error in moving the SSIs for the dart number: ', dartn
	if error != 1:
	    if remove_issuer(ptydart):
	   	print 'Success in removing the Issuer tick'
	    else:
	    	print 'Unable to remove the Issuer tick on the partie marked for deletion'
	if error != 1:	
	    if set_addinfos(ptydart, 'Cpty_Delete'):
	    	print 'Addinfos has been set on all the parties'
	    else:
	    	print 'Addinfos has not been set on all the parties'
	if error != 1:
	    if change_ptyid_and_fullname(ptydart):
	    	print 'Success in changing the partyids on the list of parties'
	    else: 
	    	print 'Failed to change the id and fullname'
	if set_aelcleaned(ptydart) == 1:
	    print 'The parties has been set to AEL_Cleaned'
	else:
	    print 'Failed to set parties to AEL_Cleaned'
	print not_cleaned
	if set_aelfailed(ptydart) == 1:
	    print 'The parties has been set to AEL_Failed'
	else:
	    print 'Unable to set status to AEL Failed'    
	while len(not_cleaned) > 0:
	    not_cleaned.pop()
#    	s = open('\\\\atlasprd\\Cpty_Cleanup\\Export.tab','w')
