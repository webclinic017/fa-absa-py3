""" VPS:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FVPSRatingHistory - Stores credit history for instruments and parties

        (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
	Handles storing and deletion of entities of type CreditHistory.
 	
----------------------------------------------------------------------------"""
import ael
import FVPSPrintout
from FVPSVariables import *

logme = FVPSPrintout.logme
BIG_DATE = ael.BIG_DATE

def delete_all_credit_history_of_a_day(old_date):
    """ Deletes all credit history elements with date_from < old_date < date_to.
    If date_to = BIG_DATE the credit history will not be deleted """

    i = 2
    j = 2

    logme("\nDeleting historical credit history elements as of %s..." \
                % str(old_date))

    while i>1 and j>0:
    
    	sql_query = """select seqnbr from credit_history """ \
    		"""where date_to > '%s' and date_from < '%s' and date_to < '%s'""" \
		% (old_date, old_date, BIG_DATE)

	j = len(ael.dbsql(sql_query))
	for set in ael.dbsql(sql_query):
	    i=len(set)
	    for column in set:
    	        ch = ael.CreditHistory[column[0]]
                if ch.ptynbr != None:
                    name = ch.ptynbr.ptyid
                else:
                    name = ch.insaddr.insid
	        try:
     	    	    ch.delete()
                    logme("Deleted Credit History for %s" % name)
	        except:
	            logme("Unable to delete Credit History %s" % name, 'ERROR')
		    raise

    logme("All credit history elements as of %s deleted" % str(old_date))


def create_new_ch_ins(ins):
    """ Creates a new instrument credit history entity and commits it """
    hr = ael.CreditHistory.new()
    hr.insaddr = ins.insaddr
    hr.date_from = ael.date_today()
    hr.date_to = BIG_DATE
    hr.rating1_chlnbr = ins.rating1_chlnbr  
    hr.rating2_chlnbr = ins.rating2_chlnbr
    hr.rating3_chlnbr = ins.rating3_chlnbr
    try:
        hr.commit()
        logme("Stored credit history for instrument %s" % ins.insid)
    except:
        logme("Unable to store credit for instrument %s" % ins.insid)

def something_has_changed_ins(ins, hr):
    """ Checks if something has changed since last credit history
    entity """
    return  (hr.rating1_chlnbr != ins.rating1_chlnbr or   
    	    hr.rating2_chlnbr != ins.rating2_chlnbr or
    	    hr.rating3_chlnbr != ins.rating3_chlnbr)
    

def create_new_ch_pty(pty):    
    """ Creates a new party credit history entity and commits it """
    hr = ael.CreditHistory.new()
    hr.ptynbr = pty.ptynbr
    hr.date_from = ael.date_today()
    hr.date_to = BIG_DATE
    hr.rating1_chlnbr = pty.rating1_chlnbr
    hr.rating2_chlnbr = pty.rating2_chlnbr
    hr.rating3_chlnbr = pty.rating3_chlnbr
    hr.bankruptcy = pty.bankruptcy
    hr.obl_default = pty.obl_default
    hr.obl_acceleration = pty.obl_acceleration
    hr.failure_to_pay = pty.failure_to_pay
    hr.repudiation = pty.repudiation
    hr.restructuring = pty.restructuring
    try:
        hr.commit()
        logme("Stored credit history for party %s" % pty.ptyid)
    except:
        logme("Unable to store credit history for party %s" % pty.ptyid)
    
def something_has_changed_pty(pty, hr):
    """ Checks if something has changed since last credit history
    entity """
    return (hr.rating1_chlnbr != pty.rating1_chlnbr or 
    	    hr.rating2_chlnbr != pty.rating2_chlnbr or 
    	    hr.rating3_chlnbr != pty.rating3_chlnbr or 
    	    hr.bankruptcy != pty.bankruptcy or 
    	    hr.obl_default != pty.obl_default or 
    	    hr.obl_acceleration != pty.obl_acceleration or 
    	    hr.failure_to_pay != pty.failure_to_pay or 
    	    hr.repudiation != pty.repudiation or 
    	    hr.restructuring != pty.restructuring)
    
    
def credit_history_name(ch):
    """ Returns the name of the party or the instrument the
    credit history entity is linked to """
    if ch != None:
        if ch.ptynbr != None:
            return ch.ptynbr.ptyid
        else:
            return ch.insaddr.insid
    return ''

def update_instrument_today(Ins):
    """ Takes an instrument as an argument and checks the credit history if
    something has changed. IF so, a new credit history is stored. """
    try:
    	sql_query = """select seqnbr from credit_history """ \
    	    	"""where insaddr = %d and date_to = '%s'""" % (Ins.insaddr, BIG_DATE)
	j = len(ael.dbsql(sql_query))
	for set in ael.dbsql(sql_query):
	    if len(set)!=0:
		for column in set:
    		    old_ch = ael.CreditHistory[column[0]]

	    else:
		old_ch = None

	if old_ch==None:
     	    create_new_ch_ins(Ins)
    	    return

	if something_has_changed_ins(Ins, old_ch):
            name = credit_history_name(old_ch)
	    old_ch_clone = old_ch.clone()
	    old_ch_clone.date_to=ael.date_today()
	    try:
	    	old_ch_clone.commit()
                logme("Saved credit history for %s" % name)
	    except:
	    	logme("Unable to store credit history for instrument %s" % name, 'ERROR')
	else:
            name = credit_history_name(old_ch)
	    logme("Nothing has changed for %s" % name, 'DEBUG')
	    return

    	create_new_ch_ins(Ins)
	
    except:
    	raise "Error for %s " % Ins.insid

	

def update_party_today(Party):
    """ Takes an party as an argument and checks the credit history if
    something has changed. IF so, a new credit history is stored. """
    try:
	
	old_hr=ael.CreditHistory.read(
    	"""ptynbr=%d and date_to='%s'""" 
	% (Party.ptynbr, BIG_DATE) )
	
	if old_hr == None:
    	    create_new_ch_pty(Party)
    	    return   	    	

	if something_has_changed_pty(Party, old_hr):
	    name = credit_history_name(old_hr)
	    old_hr_clone = old_hr.clone()
	    old_hr_clone.date_to=ael.date_today()
	    try:
	    	old_hr_clone.commit()
                logme("Saved credit history for %s" % name)
	    except:
                logme("Unable to store credit history for party %s" % name, 'ERROR')

	else:
            name = credit_history_name(old_hr)
	    logme("Nothing has changed for %s" % name, 'DEBUG')
	    return

    	create_new_ch_pty(Party)
	
    except:
	raise "Error for %s" % Party.ptyid   

def DefinedInstrumentExclusions(e):
    for exp in InstrumentCreditHistoryExclusions:
	if e == exp:
	    return 1
    for exp in InstrumentCreditHistoryExcludeInstype:
        i = ael.Instrument[e]
        if i != None and i.instype == exp:
            return 1
    return 0

def DefinedInstrumentInclusion(e):
    for exp in InstrumentCreditHistoryInclusions:
	if e == exp:
	    return 1
    for exp in InstrumentCreditHistoryIncludeInstype:
        i = ael.Instrument[e]
        if i != None and i.instype == exp:
            return 1

    return 0

def DefinedPartyExclusions(e):
    for exp in PartyCreditHistoryExclusions:
	if e == exp:
	    return 1
    return 0

def DefinedPartyInclusion(e):
    for exp in PartyCreditHistoryInclusions:
	if e == exp:
	    return 1

    return 0
	
def GetInstrumentDefinedSet():

    def_set = []
    if InstrumentCreditHistoryBase == 1:
    	for e in ael.Instrument.select():
	    if not DefinedInstrumentExclusions(e):
	    	def_set.append(e)
	    	
    elif InstrumentCreditHistoryBase == 0:
 	for e in InstrumentCreditHistoryInclusions:
	    if not DefinedInstrumentExclusions(e):
	    	yc = ael.Party[e]
	    	def_set.append(yc) 


    return def_set

def GetPartyDefinedSet():
    def_set = []
    if PartyCreditHistoryBase == 1:
    	for e in ael.Party.select():
	    if not DefinedPartyExclusions(e):
	    	def_set.append(e) 

    elif PartyCreditHistoryBase == 0:
 	for e in PartyCreditHistoryInclusions:
	    if not DefinedPartyExclusions(e):
	    	yc = ael.Party[e]
	    	def_set.append(yc)


    return def_set

def update_all_instrument():
    """ Stores credit history for all instruments defined in FVPSVariables """
    logme("\nStart storing credit history for instruments...\n")
    sel = GetInstrumentDefinedSet()
    for i in range(len(sel)):
	
    	if sel[i].rating1_chlnbr or \
	    sel[i].rating2_chlnbr or \
	    sel[i].rating3_chlnbr:
            update_instrument_today(sel[i])
    logme("All credit history elements for instruments have been stored")
	    

def update_all_party():
    """ Stores credit history for all parties defined in FVPSVariables """
    logme("\nStart storing credit history elements for parties...\n")
    sel = GetPartyDefinedSet()
    for i in range(len(sel)):
    	if sel[i].rating1_chlnbr or \
	   sel[i].rating2_chlnbr or \
	   sel[i].rating3_chlnbr or \
	   sel[i].bankruptcy or \
	   sel[i].obl_default or \
	   sel[i].obl_acceleration or \
	   sel[i].failure_to_pay or \
	   sel[i].repudiation or \
	   sel[i].restructuring:
            update_party_today(sel[i])
    logme("\nAll credit history elements for parties have been stored")


