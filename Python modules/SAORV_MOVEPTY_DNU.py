import ael
#   Ael to move trades from one counterparty of type none to a nother counterparty of type counterparty 
#   and also to move a trade with a broker of type none to a party with type broker.
#   Created Hardus Jacobs
#   Call 54565

def buildNonelist():
    # This is to build a list of parties that is of type 
    # CounterParty, Client, Internal Dept, Broker 

    cplist = []
    cp = ael.Party.select('type="Counterparty"')
    for p in cp:
    	if p.ptyid.find("DO NOT USE") != -1:
    	    cplist.append(p)

    cp = ael.Party.select('type="Broker"')
    for p in cp:
    	if p.ptyid.find("DO NOT USE") != -1:
    	    cplist.append(p)

    cp = ael.Party.select('type="Client"')
    for p in cp:
    	if p.ptyid.find("DO NOT USE") != -1:
    	    cplist.append(p)

    cp = ael.Party.select('type="Intern Dept"')
    for p in cp:
    	if p.ptyid.find("DO NOT USE") != -1:
    	    cplist.append(p)

    nonelist = []
    return nonelist
    
'''    
    for p in cplist:
    	if p.type IN ('Counterparty', 'Broker', 'Client', 'Intern Dept'):
	    cp = ael.Trade.select("counterparty_ptynbr = '%d'" %p.ptynbr)
	    b = ael.Trade.select("broker_ptynbr = '%d'" %p.ptynbr)
	    aq = ael.Trade.select("acquirer_ptynbr = '%d'" %p.ptynbr)
	    g = ael.Trade.select("guarantor_ptynbr = '%d'" %p.ptynbr)

	    i = ael.Instrument.select("issuer_ptynbr = '%d'" %p.ptynbr)

	    cb = ael.Account.select("correspondent_bank_ptynbr = '%d'" %p.ptynbr)
	    cb2 = ael.Account.select("correspondent_bank_ptynbr2 = '%d'" %p.ptynbr)	    
	    cb3 = ael.Account.select("correspondent_bank_ptynbr3 = '%d'" %p.ptynbr)	    
	    cb4 = ael.Account.select("correspondent_bank_ptynbr4 = '%d'" %p.ptynbr)	    

	    pty = ael.Payment.select("ptynbr = '%d'" %p.ptynbr)	    
	    
	    o = ael.Payment.select("owner_ptynbr = '%d'" %p.ptynbr)	    
	    
	    if (len(cp) > 0 or len(b) > 0 or len(aq) > 0 or len(g) > 0 or 
	        len(i) > 0 or len(cb) > 0 or len(cb2) > 0 or len(cb3) > 0 or 
		len(cb4) > 0 or len(pty) > 0 or len(o) > 0):
		
	    	if p.ptyid not in nonelist:
	    	    nonelist.append(p.ptyid)
		    
    nonelist.sort()
'''
    	    


def buildPartyList(flag):
    # This builds the list of all the counterparties
    # returns NotUsed list if Flag == 1, otherwise
    # returns the cplist
    plist = []
    cp = ael.Party.select('type="Counterparty"')
    for p in cp:
    	plist.append(p.ptyid)
    cp = ael.Party.select('type="Broker"')
    for p in cp:
    	plist.append(p.ptyid)
    cp = ael.Party.select('type="Client"')
    for p in cp:
    	plist.append(p.ptyid)
    cp = ael.Party.select('type="Intern Dept"')
    for p in cp:
    	plist.append(p.ptyid)
	
    cplist = []
    NotUsedlist = []
    for p in plist:
    	if p.find("DO NOT USE") != -1:
#    	    print p, p.find("DO NOT USE")
    	    if ael.Party[p].type <> 'None':
	    	NotUsedlist.append(p)
	else:
	    cplist.append(p)
	    
    if flag == 1:
    	return NotUsedlist
    else:
    	return cplist


def moveCpTrades(fromPty, toPty):
    # This will move the trades from one counterparty to the other counterparty 
    # Only where the counterparty to the trade is a 'DO NOT USE' party
    trd = ael.Trade.select("counterparty_ptynbr = '%d'" % fromPty.ptynbr)
    if len(trd) > 0: 
    	if toPty.type != 'None': 	
   	    for t in trd:
    	    	trdclone = t.clone()
    	    	trdclone.counterparty_ptynbr = toPty.ptynbr
		try:
		    trdclone.commit()
    	    	    print 'Trade ', t.trdnbr, ' moved to counterparty ', toPty.ptyid
		except:
		    print 'Unable to commit Trade ', t.trdnbr
	else:   
    	    ael.log('The party that you selected is of type None')
    else:
	ael.log('No Trades where %s is a Counterparty' %fromPty.ptyid)
    ael.poll()	
    
	    
def moveBrokTrades(fromPty, toPty):
    # This will move the trades with 'DO NOT USE' broker to a party of type Broker
    trd = ael.Trade.select("broker_ptynbr = '%d'" % fromPty.ptynbr)
    if len(trd) > 0: 	
	if toPty.type == 'Broker':
    	    for t in trd:
    	    	trdclone = t.clone()
    	    	trdclone.broker_ptynbr = toPty.ptynbr
		try:
		    trdclone.commit()
    	    	    print 'Trade ', t.trdnbr, ' moved to broker ', toPty.ptyid		
		except:
		    print 'Unable to commit Trade ', t.trdnbr
	else:   
    	    ael.log('The party that you selected is not a Broker')
    else:
        ael.log('No Trades where %s is a broker' %fromPty.ptyid)
    ael.poll()
    

def moveAcqTrades(fromPty, toPty):
    # This will move the trades with 'DO NOT USE' acquirer to a party of type Internal Department
    trd = ael.Trade.select("acquirer_ptynbr = '%d'" % fromPty.ptynbr)
    if len(trd) > 0: 	
	if toPty.type == 'Intern Dept':
    	    for t in trd:
    	    	trdclone = t.clone()
    	    	trdclone.acquirer_ptynbr = toPty.ptynbr
		try:
		    trdclone.commit()
    	    	    print 'Trade ', t.trdnbr, ' moved to acquirer', toPty.ptyid		
		except:
		    print 'Unable to commit Trade ', t.trdnbr
	else:   
    	    ael.log('The party that you selected is not an Internal Department')
    else:
	ael.log('No Trades where %s is an Acquirer' %fromPty.ptyid)
    ael.poll()
        
	
def moveGuaranTrades(fromPty, toPty):
    # This will move the trades with 'DO NOT USE' guarantor to a party not of type None
    trd = ael.Trade.select("guarantor_ptynbr = '%d'" % fromPty.ptynbr)
    if len(trd) > 0: 	
	if toPty.type != 'None':
    	    for t in trd:
    	    	trdclone = t.clone()
    	    	trdclone.guarantor_ptynbr = toPty.ptynbr
		try:
		    trdclone.commit()
    	    	    print 'Trade ', t.trdnbr, ' moved to quarantor ', toPty.ptyid		
		except:
		    print 'Unable to commit Trade ', t.trdnbr
	else:   
    	    ael.log('The party that you selected is of type None')
    else:
        ael.log('No trades where %s is a guarantor to the trade.' %fromPty.ptyid)	
    ael.poll()



def moveIssuer(fromPty, toPty):
    # This will change the issuer of an instrument from a 'DO NOT USE' party to a valid issuer
    # where the issuer box is check
    ins = ael.Instrument.select("issuer_ptynbr = '%d'" % fromPty.ptynbr)
    if len(ins) > 0:	
	if toPty.issuer == 1:
    	    for i in ins:
	    	insclone = i.clone()
		insclone.issuer_ptynbr = toPty.ptynbr
		try:
		    insclone.commit()
    	    	    print 'Instrument ', i.insid, ' moved to issuer ', toPty.ptyid		
		except:
		    print 'Unable to commit Instrument ', i.insid
    	else:   
    	    ael.log('The party that you selected is not an issuer')
    else:
    	ael.log('No Instruments where %s is an issuer' %fromPty.ptyid)
    ael.poll()
    
        
def moveCBank(fromPty, toPty):
    # This will move the accounts with 'DO NOT USE' correspondent bank to another party 
    acc = ael.Account.select()
#    ('correspondent_bank_ptynbr = %d' % (fromPty.ptynbr))

    for t in acc:
    	if t.correspondent_bank_ptynbr == fromPty.ptynbr:
	    accClone = t.clone()
    	    accClone.correspondent_bank_ptynbr = toPty.ptynbr
	    try:
	    	accClone.commit()
    	    	print 'Account ', t.accnbr, ' moved to correspondent bank ', toPty.ptyid
	    except:
    	    	print 'Unable to commit Account ', t.accnbr
		
	if t.correspondent_bank2_ptynbr == fromPty.ptynbr:
	    accClone = t.clone()
    	    accClone.correspondent_bank2_ptynbr = toPty.ptynbr
	    try:
	    	accClone.commit()
    	    	print 'Account ', t.accnbr, ' moved to correspondent bank2 ', toPty.ptyid		
	    except:
    	    	print 'Unable to commit Account ', t.accnbr

	if t.correspondent_bank3_ptynbr == fromPty.ptynbr:
	    accClone = t.clone()
    	    accClone.correspondent_bank3_ptynbr = toPty.ptynbr
	    try:
	    	accClone.commit()
    	    	print 'Account ', t.accnbr, ' moved to correspondent bank3 ', toPty.ptyid
	    except:
    	    	print 'Unable to commit Account ', t.accnbr
		
	    
	if t.correspondent_bank4_ptynbr == fromPty.ptynbr:
	    accClone = t.clone()
    	    accClone.correspondent4_bank_ptynbr = toPty.ptynbr
	    try:
	    	accClone.commit()
    	    	print 'Account ', t.accnbr, ' moved to correspondent bank4 ', toPty.ptyid
	    except:
	    	print 'Unable to commit Account ', t.accnbr

#    else:
#        ael.log('No accounts where %s is a corresponding bank.' %fromPty.ptyid)	
    ael.poll()


def movePayment(fromPty, toPty):
    # This will move the payments with 'DO NOT USE' party to a party not of type None
    pay = ael.Payment.select("ptynbr = '%d'" % fromPty.ptynbr)
    if len(pay) > 0: 	
	if toPty.type != 'None':
    	    for t in pay:
    	    	payclone = t.clone()
    	    	payclone.ptynbr = toPty.ptynbr
		try:
		    payclone.commit()
    	    	    print 'Payment ', t.paynbr, ' moved to party ', toPty.ptyid		
	    	except:
	    	    print 'Unable to commit Payment ', t.paynbr

	else:   
    	    ael.log('The party that you selected is of type None')
    else:
        ael.log('No payments where %s is a party.' %fromPty.ptyid)	
    ael.poll()


def movePortfolio(fromPty, toPty):
    # This will move the portfolio with 'DO NOT USE' owner party to a party not of type None
    port = ael.Portfolio.select("owner_ptynbr = '%d'" % fromPty.ptynbr)
    if len(port) > 0: 	
	if toPty.type != 'None':
    	    for t in port:
    	    	portclone = t.clone()
    	    	portclone.owner_ptynbr = toPty.ptynbr
		try:
		    portclone.commit()
    	    	    print 'Portfolio ', t.prfnbr, ' moved to party ', toPty.ptyid		
	    	except:
	    	    print 'Unable to commit Portfolio ', t.prfnbr		    
	else:   
    	    ael.log('The party that you selected is of type None')
    else:
        ael.log('No portfolio where %s is a owner party.' %fromPty.ptyid)	
    ael.poll()


def ChangetoNone(fromPty):
    ptyclone = fromPty.clone()
    ptyclone.type = 'None'
    try:
    	ptyclone.commit()
	print 'Party ', fromPty.ptyid, ' changed to type None'
    except:
    	print 'Unable to commit Party - change to type None'
    ael.poll()


ael_variables = [('noneparty', '1_Do_Not_Use Party', 'string', buildPartyList(1), None, 1, 0),
    	    	('cntrpart', '2_New_Party', 'string', buildPartyList(0), None, 1, 0)]

		 	    
def ael_main(dict):
    # Main function calling all above functions
    cppart = ael.Party[dict["cntrpart"]]
    none = ael.Party[dict["noneparty"]]
    print 'Moving from Party: ', none.ptyid, ' to Party: ', cppart.ptyid
    moveCpTrades(none, cppart)
    moveBrokTrades(none, cppart)
    moveAcqTrades(none, cppart)
    moveGuaranTrades(none, cppart)
    moveIssuer(none, cppart)
    moveCBank(none, cppart)
    movePayment(none, cppart)
    movePortfolio(none, cppart)
    ChangetoNone(none)
    ael.poll()

