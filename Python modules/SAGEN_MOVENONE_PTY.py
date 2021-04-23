import ael
#   Ael to move trades from one counterparty of type none to a nother counterparty of type counterparty 
#   and also to move a trade with a broker of type none to a party with type broker.
#   Created Hardus Jacobs
#   Call 54565

def buildNonelist():
    # This is to build a list of parties that is of type none 
    nonelist = []
    nonepty = ael.Party.select('type="None"')
    for p in nonepty:
    	if p.type == 'None':
	    t = ael.Trade.select("counterparty_ptynbr = '%d'" %p.ptynbr)
	    b = ael.Trade.select("broker_ptynbr = '%d'" %p.ptynbr)
	    i = ael.Instrument.select("issuer_ptynbr = '%d'" %p.ptynbr)
	    g = ael.Trade.select("guarantor_ptynbr = '%d'" %p.ptynbr)
	    if (len(b) > 0 or len(t) > 0 or len(i) > 0 or len(g) > 0):
	    	if p.ptyid not in nonelist:
	    	    nonelist.append(p.ptyid)
    nonelist.sort()
    return nonelist	    

def buildPartyList():
    # This builds the list of all the counterparties
    cplist = []
    cp = ael.Party.select('type="Counterparty"')
    for p in cp:
    	cplist.append(p.ptyid)
    cp = ael.Party.select('type="Broker"')
    for p in cp:
    	cplist.append(p.ptyid)
    return cplist

def moveCpTrades(fromPty, toPty):
    # This will move the trades from one counterparty to the other counterparty 
    # Only where the counterparty to the trade is of type None
    trd = ael.Trade.select("counterparty_ptynbr = '%d'" % fromPty.ptynbr)
    if len(trd) > 0:  
    	if toPty.type == 'Broker' or toPty.type == 'Counterparty': 	
         
    	    for t in trd:
    	    	trdclone = t.clone()
    	    	trdclone.counterparty_ptynbr = toPty.ptynbr
	    	trdclone.commit()
	else:   
    	    ael.log('The party that you selected is not an Counterparty or Broker')
    else:
	ael.log('No Trades where %s is a Counterparty' %fromPty.ptyid)
    ael.poll()	
	    
def moveBrokTrades(fromPty, toPty):
    # This will move the trades with broker of type none to a party of type Broker
    trd = ael.Trade.select("broker_ptynbr = '%d'" % fromPty.ptynbr)
    if len(trd) > 0: 	
	if toPty.type == 'Broker':
    	    for t in trd:
    	    	trdclone = t.clone()
    	    	trdclone.broker_ptynbr = toPty.ptynbr
	    	trdclone.commit()
	else:   
    	    ael.log('The party that you selected is not a Broker')
    else:
        ael.log('No Trades where %s is a broker' %fromPty.ptyid)
    ael.poll()
	
def moveIssuer(fromPty, toPty):
    # This will change the issuer of an instrument from a party of type none to a valid issuer
    # where the issuer box is check
    ins = ael.Instrument.select("issuer_ptynbr = '%d'" % fromPty.ptynbr)
    if len(ins) > 0:	
	if toPty.issuer == 1:
    	    for i in ins:
	    	insclone = i.clone()
		insclone.issuer_ptynbr = toPty.ptynbr
    		insclone.commit()
    	else:   
    	    ael.log('The party that you selected is not an issuer')
    else:
    	ael.log('No Instruments where %s is an issuer' %fromPty.ptyid)
    ael.poll()
    
def moveGuaranTrades(fromPty, toPty):
    # This will move the trades with broker of type none to a party of type Broker
    trd = ael.Trade.select("guarantor_ptynbr = '%d'" % fromPty.ptynbr)
    if len(trd) > 0: 	
	if toPty.type == 'Broker' or toPty.type == 'Counterparty':
    	    for t in trd:
    	    	trdclone = t.clone()
    	    	trdclone.guarantor_ptynbr = toPty.ptynbr
	    	trdclone.commit()
	else:   
    	    ael.log('The party that you selected is not a Broker')
    else:
        ael.log('No trades where %s is a gaurantor to the trade.' %fromPty.ptyid)	
    ael.poll()
        
ael_variables = [('noneparty', '1_PartyOfNone', 'string', buildNonelist(), None, 1, 0),
    	    	('cntrpart', '2_PartyOfCounterPty', 'string', buildPartyList(), None, 1, 0)]
		 	    
def ael_main(dict):
    # Main function calling all above functions
    cppart = ael.Party[dict["cntrpart"]]
    none = ael.Party[dict["noneparty"]]
    print 'Moving from Party: ', none.ptyid, ' to Party: ', cppart.ptyid
    moveCpTrades(none, cppart)
    moveBrokTrades(none, cppart)
    moveIssuer(none, cppart)
    moveGuaranTrades(none, cppart)
