""" VPS:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FVPSDividendStream - Stores historical dividend streams

        (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
	Functionality for storing and deleting historical entities of
        type DividendStream.

        If there exist no historical dividend stream
        a new will always be created with
        date_from = today
        date_to = BIG_DATE

        If there exist a historical dividend stream with date_to = BIG_DATE,
        this entity's date_to will be set to today and a new historical
        dividend stream will be created with date_from = today and
        date_to = BIG_DATE.
        
	
----------------------------------------------------------------------------"""

import ael
import re
import string
import FVPSPrintout
from FVPSVariables import *

logme = FVPSPrintout.logme
BIG_DATE = ael.BIG_DATE

def delete_all_ds_of_a_day(old_date):
    """ Deletes all dividend streams with date_from < old_date < date_to.
    If date_to = BIG_DATE the dividend stream will not be deleted """
    i = 2
    j = 2

    logme("Deleting historical dividend streams as of %s..." \
          % str(old_date))

    while i>1 and j>0:
    
    	sql_query = """select seqnbr from dividend_stream """ \
    	"""where date_to > '%s' and date_from < '%s' and date_to < '%s'""" \
	% (old_date, old_date, BIG_DATE)

	j = len(ael.dbsql(sql_query))
	for set in ael.dbsql(sql_query):
	    i=len(set)
	    for column in set:
    	        ds = ael.DividendStream[column[0]]
	        try:
     	    	    ds.delete()
	            logme("Deleted %s" % ds.name)
	        except:
	            logme("Unable to delete %s" % yc.name, 'ERROR')
    	    	    return 0
    logme("All historical dividend streams of the date given have been deleted")
    return 1


def test_if_name_in_db(dsname):
    """ Is the new dividend stream name already in the database ? """
    sql_query = """select count(1) from dividend_stream where name = '%s'""" % dsname

    for set in ael.dbsql(sql_query):
    	for column in set:
    	    if int(column[0])>0:
    	    	return dsname
    
    return None


def get_new_ds_name(dsname):
    """ Create a new name for the historical dividend stream
    The new name is on the format: old_name<underscore>historical_date """
    if len(dsname) + len(ael.date_today().to_string()) + 1> 30:
    	length = 30 - len(ael.date_today().to_string()) - 1
	stlist = [dsname[0:length], ael.date_today().to_string()]
    	new_name = string.join(stlist, "_")
	test = test_if_name_in_db(new_name)
	i=0
	while not test == None:
	    nr = '%d' % (i)
	    
    	    length = 30 - len(ael.date_today().to_string()) - 2 - len(nr)

    	    stlist1 = [dsname[0:length], str(nr)]
	    stlist2 = string.join(stlist1, "_")
	    new_name1 = [stlist2, ael.date_today().to_string()]
	    new_name     = string.join(new_name1, "_")
	    
	    
    	    test = test_if_name_in_db(new_name)
    	    i=i+1

    else:
    	stlist = [dsname, ael.date_today().to_string()]
	new_name = string.join(stlist, "_")

	test = test_if_name_in_db(new_name)
	i=0
	while not test == None:
	    
	    nr = '%d' % (i)
	    	    
            if len(dsname) + len(ael.date_today().to_string()) + 2 + len(nr)> 30:
	    	name_len = 30 - 3 -len(ael.date_today().to_string()) 
    	    else:
	    	name_len = len(dsname)

    	    stlist1 = [dsname[0:name_len], str(nr)]
	    stlist2 = string.join(stlist1, "_")
	    new_name1 = [stlist2, ael.date_today().to_string()]
	    new_name     = string.join(new_name1, "_")
    	    test = test_if_name_in_db(new_name)
    	    i=i+1
    
    return new_name

def set_archive_flag_on_children(ds):
    estimates = ds.estimates()
    for estimate in estimates:
	estimate.archive_status = 1

def create_new_ds(ds):
    """ Create a new dividend stream """
    ds_new = ds.new()
    ds_new.date_from = ael.date_today()
    ds_new.date_to = BIG_DATE
    ds_new.original_ds_seqnbr=ds.seqnbr
    ds_new.archive_status=1
    ds_new.name = get_new_ds_name(ds.name)
    set_archive_flag_on_children(ds_new)

    try:
        ds_new.commit()
        logme("Stored historical dividend stream %s" % ds.name)
    except:
        logme("Unable to store historical dividend stream %s" % ds.name, 'ERROR')
    return ds_new


def find_last_historical_ds(orig_ds):
    """ Search for a historical dividend stream with date_to = BIG_DATE """

    sql_query = """select seqnbr from dividend_stream """ \
    	    	"""where original_ds_seqnbr = %d and date_to = '%s'""" % \
		(orig_ds.seqnbr, BIG_DATE)
		
    for set in ael.dbsql(sql_query):
    	for column in set:
    	    if int(column[0])>0:
    	    	ds = ael.DividendStream[column[0]]
    	    	return ds
    return None


def bigdate_ds_equal_live(dslive, dslatest):
    """ Compares two dividend streams. First the dimensions are compared,
    then the values """

    if dslive.div_per_year != dslatest.div_per_year:
	return 0    
    if dslive.annual_growth != dslatest.annual_growth:
	return 0
    if dslive.adjustment_factor != dslatest.adjustment_factor:
	return 0
	
    sellive = dslive.estimates()

    sellatest = dslatest.estimates()

    if not len(sellatest)==len(sellive):
    	return 0 #False = Not equal
    
    divlen = len(sellive)
    k=0
    for i in range(len(sellive)):
    	for j  in range(len(sellatest)):
    	    if sellive[i].pay_day == sellatest[j].pay_day and sellive[i].tax_factor == sellatest[j].tax_factor:
		k=k+1
  	    	
			    
    if not k>=divlen:
    	return 0
		    
    return 1



def copy_complete_ds(orig_ds, lastds):
    """ Copy a dividend stream and commit it into the database """
    if lastds == None:
    	bigdate_ds = create_new_ds(orig_ds)
	return
    else:
    	lastds_clone = lastds.clone()
    	lastds_clone.date_to = ael.date_today()
        lastds_clone.commit()
	bigdate_ds = create_new_ds(orig_ds)

    return	
    	   
def update_ds(ds):
    """ Update a dividend stream and create a new if necessary """
    last_historical_ds = find_last_historical_ds(ds)
    if last_historical_ds == None:
        copy_complete_ds(ds, None)
    	return 1

    if bigdate_ds_equal_live(ds, last_historical_ds):
        logme("Nothing changed for dividend stream %s" % ds.name, 'DEBUG')
    	return 1

   
    if not last_historical_ds.date_from == ael.date_today():
    	copy_complete_ds(ds, last_historical_ds)
    else:
    	#If it already exist a historical data with date_to = today
	#we should use that instead of creating a new one.
	#The DividendEstimate will be kept but all the children
	#will be deleted
    	last_historical_ds.delete()
        copy_complete_ds(ds, None)
     
    return 1



def DefinedExclusions(e):
    for exp in DividendStreamExclusions:
	if e == exp:
	    return 1
    return 0

def DefinedInclusion(e):
    for exp in DividendStreamInclusions:
	if e == exp:
	    return 1

    return 0

def GetDefinedSet():
    """ Returns a list of dividend streams according to the rules
    set in FVPSVariables """
    def_set = []
    if DividendStreamBase == 1:
    	for e in ael.DividendStream.select():
	    if not DefinedExclusions(e.name):
	    	def_set.append(e)

    elif DividendStreamBase == 0:
 	for e in DividendStreamInclusions:
	    if not DefinedExclusions(e):
	    	ds = ael.DividendStream[e]
	    	def_set.append(ds)

    return def_set


def update_all_ds():
    """ Store dividend streams according to the settings in FVPSVariables.
    Main function. """
    logme("\nStart storing dividend streams...\n")
    for ds in GetDefinedSet():
        if (ds.date_to == None):
 	    update_ds(ds) 

    logme("All dividend streams stored")
