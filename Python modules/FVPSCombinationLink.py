""" VPS:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FVPSCombinationLink - Stores historical combination links

        (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
	Functionality for storing and deleting historical entities of
        type CombinationLink for instruments of type EquityIndex.

        The historical combination links are archived and linked to a dummy
        instrument which have date stamps date_from and date_to. 

        If there exist no historical instrument
        a new will always be created with
        date_from = today
        date_to = BIG_DATE

        If there exist an historical instrument with date_to = BIG_DATE,
        this entity's date_to will be set to today and a new historical
        instrument will be created with date_from = today and
        date_to = BIG_DATE.
        
	
----------------------------------------------------------------------------"""

import ael
import re
import string
import FVPSPrintout
from FVPSVariables import *

logme = FVPSPrintout.logme
BIG_DATE = ael.BIG_DATE

def delete_all_cl_of_a_day(old_date):
    """ Deletes all equity indices with date_from < old_date < date_to.
    If date_to = BIG_DATE the instrument will not be deleted """
    i = 2
    j = 2

    logme("Start deleting combination links...")

    while i>1 and j>0:
    
    	sql_query = """select insaddr from instrument """ \
    	"""where date_to > '%s' and date_from < '%s' and date_to < '%s'""" \
	""" and instype = 22 """ \
	% (old_date, old_date, BIG_DATE)
	j = len(ael.dbsql(sql_query))
	for set in ael.dbsql(sql_query):
	    i=len(set)
	    for column in set:
    	        ins = ael.Instrument[column[0]]
	        try:
     	    	    ins.delete()
	            logme("Deleted historical combination links for %s" % ins.insid)
	        except:
	            logme("Unable to delete %s" % ins.insid, 'ERROR')
    	    	    raise

    logme("All historical combination links of the date given are deleted.")
    return 1

def test_if_name_in_db(insname):
    sql_query = """select count(1) from instrument where insid = '%s'""" % insname

    for set in ael.dbsql(sql_query):
    	for column in set:
    	    if int(column[0])>0:
    	    	return insname
    
    return None


def get_new_cl_name(clname):
    """ Create a new name for the historical instrument """
    if len(clname) + len(ael.date_today().to_string()) + 1> 30:
    	length = 30 - len(ael.date_today().to_string()) - 1
	stlist = [clname[0:length], ael.date_today().to_string()]
    	new_name = string.join(stlist, "_")
	test = test_if_name_in_db(new_name)
	i=0
	while not test == None:
	    nr = '%d' % (i)
	    
    	    length = 30 - len(ael.date_today().to_string()) - 2 - len(nr)

    	    stlist1 = [clname[0:length], str(nr)]
	    stlist2 = string.join(stlist1, "_")
	    new_name1 = [stlist2, ael.date_today().to_string()]
	    new_name     = string.join(new_name1, "_")
	    
	    
    	    test = test_if_name_in_db(new_name)
    	    i=i+1

    else:
    	stlist = [clname, ael.date_today().to_string()]
	new_name = string.join(stlist, "_")

	
	test = test_if_name_in_db(new_name)
	i=0
	while not test == None:
	    nr = '%d' % (i)
	    	    
            if len(clname) + len(ael.date_today().to_string()) + 2 + len(nr)> 30:
	    	name_len = 30 - 3 -len(ael.date_today().to_string()) 
    	    else:
	    	name_len = len(clname)

    	    stlist1 = [clname[0:name_len], str(nr)]
	    stlist2 = string.join(stlist1, "_")
	    new_name1 = [stlist2, ael.date_today().to_string()]
	    new_name     = string.join(new_name1, "_")
    	    test = test_if_name_in_db(new_name)
    	    i=i+1
    
    return new_name

def create_new_cl(cl):
    """ Create a new instrument """
    cl_new = cl.new()
    cl_new.date_from = ael.date_today()
    cl_new.date_to = BIG_DATE
    cl_new.original_insaddr=cl.insaddr
    cl_new.archive_status=1
    cl_new.isin = ""
    cl_new.extern_id1 = ""
    cl_new.extern_id2 = ""    
    cl_new.insid = get_new_cl_name(cl.insid)

    aliases = cl_new.aliases()
    for a in aliases:
    	a.delete()

    try:
        cl_new.commit()
        logme("Stored combination links for %s" % cl.insid)
    except:
        logme("Could not store combination links for %s" % cl.insid, 'ERROR')
    return cl_new

def find_last_historical_cl(orig_cl):
    """ Search for a historical instrument with date_to = BIG_DATE """
    sql_query = """select insaddr from instrument """ \
    	    	"""where original_insaddr = %d and date_to = '%s'""" % \
		(orig_cl.insaddr, BIG_DATE)
		
    for set in ael.dbsql(sql_query):
    	for column in set:
    	    if int(column[0])>0:
    	    	cl = ael.Instrument[column[0]]
    	    	return cl
    return None



def bigdate_cl_equal_live(cmlive, cmbd):
    """ Compares two instruments. First the dimensions are compared,
    then the index weights """
    
    sellive = cmlive.combination_links()

    selbd = cmbd.combination_links()

    if not len(selbd)==len(sellive):
    	return 0 

    for i in range(len(sellive)):
    	for j  in range(len(selbd)):
    	    if selbd[j].member_insaddr.insid == sellive[i].member_insaddr.insid:
       	    	if sellive[i].weight != selbd[j].weight:
		    return 0
		    
    return 1



def copy_complete_cl(orig_cl, lastcl):
    """ Copy an instrument and its combination links and commit it """

    if lastcl == None:
    	bigdate_cl = create_new_cl(orig_cl)
	return
    else:
    	lastcl_clone = lastcl.clone()
    	lastcl_clone.date_to = ael.date_today()
        try:
            lastcl_clone.commit()
            logme("Stored combination links for %s" % orig_cl.insid)
        except:
            logme("Could not store combination links for %s" % orig_cl.insid, 'DEBUG')
	bigdate_cl = create_new_cl(orig_cl)

    return	
    	   
def update_cl(cl):
    """ Update an instrument and create a new if necessary """
    last_historical_cl = find_last_historical_cl(cl)
    if last_historical_cl == None:
        copy_complete_cl(cl, None)
    	return 1

    if bigdate_cl_equal_live(cl, last_historical_cl):
    	return 1
	
    if not last_historical_cl.date_from == ael.date_today():
    	copy_complete_cl(cl, last_historical_cl)
    else:
    	last_historical_cl.delete()
        copy_complete_cl(cl, None)
	
    return 1

  

def DefinedExclusions(e):
    for exp in CombinationLinkExclusions:
	if e == exp:
	    return 1

    return 0

def DefinedInclusion(e):
    for exp in CombinationLinkInclusions:
	if e == exp:
	    return 1

    return 0

def GetDefinedSet():

    def_set = []
    if CombinationLinkBase == 1:
    	for e in ael.Instrument.select("""instype = 'EquityIndex'"""):
	    if not DefinedExclusions(e.insid):
	    	def_set.append(e) 
	    	
    elif CombinationLinkBase == 0:
 	for e in CombinationLinkInclusions:
	    if not DefinedExclusions(e.insid):
	    	def_set.append(e) 


    return def_set


def update_all_cl():
    """ Store combination links according to the settings in FVPSVariables.
    Main function. """
    logme("\nStart storing historical combination links ... \n")
    for cl in GetDefinedSet():
        if (cl != None and cl.date_to == None):
    	    logme("Checking combination links for  %s" % cl.insid, 'DEBUG')
    	    update_cl(cl)

    logme("All combination links stored")




