""" VPS:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FVPSVolatility - Stores historical volatilities

        (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
	Functionality for storing and deleting historical entities of
        type Volatility
 	
----------------------------------------------------------------------------"""


import ael
import string

from FVPSVariables import *
import FVPSPrintout

try:
    import FMtMVariables
    FMtMDefined = 1
except:
    VolatilityIncludeWithSuffix = 0

    if VolatilityBase == 2:
    	VolatilityBase = 1

    FMtMDefined = 0

BIG_DATE = ael.BIG_DATE
MAX_DELETE_ATTEMPTS = 100
vol_dictionary = {}
logme = FVPSPrintout.logme

"""
Performance improvements can be made here by not calling is_referenced_by
when deleting yield curves. The cost will be error messages from dsb92api printed
in the log/batch prompt.
"""

def is_referenced_by(vol, old_date):
    """ Check if the volatility is referenced by another volatility """
    sql_query = """select seqnbr from volatility """ \
    	    	"""where historical_day = '%s'""" % (old_date)
    j = len(ael.dbsql(sql_query))
    for set in ael.dbsql(sql_query):
	i=len(set)
	for column in set:
    	    vol_temp = ael.Volatility[column[0]]

    	    if vol_temp.und_vol_seqnbr != None:	    
    	    	if vol_temp.und_vol_seqnbr.seqnbr == vol.seqnbr:
	    	    return 1
	    
    return 0
    
    
def delete_all_vol_of_a_day(old_date):
    """ Delete all historical volatilities on a specified date. The volatilities
    lowest in the hierarchy will be deleted first """
    
    i = 2
    j = 2

    logme("\nDeleting historical volatilities as of %s...\n" \
          % str(old_date), 'INFO')

    while i>1 and j>0:
    	sql_query = """select seqnbr from volatility """ \
    	    	"""where historical_day = '%s'""" % (old_date)
    	
	j = len(ael.dbsql(sql_query))
	for set in ael.dbsql(sql_query):
	    i=len(set)
	    for column in set:
    	        vol = ael.Volatility[column[0]]
		if not is_referenced_by(vol, old_date):
	            try:
     	    	    	vol.delete()
	            	logme("Deleted %s" % vol.vol_name)
	            except:
	            	logme("ERROR: Unable to delete %s" % vol.vol_name, 'ERROR')
    	    	    	
		else:
		    logme("Volatility %s is referenced by another. Will attempt again." % vol.vol_name, 'DEBUG')
		    
		    
    logme("\nAll historical volatilities as of %s deleted." % str(old_date))



def delete_all_vol_of_today():

    delete_all_vol_of_a_day(ael.date_today())

def test_if_name_in_db(volname):
    """ Is the new volatility name already in the database ? """
    sql_query = """select count(1) from volatility where vol_name = '%s'""" % volname

    for set in ael.dbsql(sql_query):
    	for column in set:
    	    if int(column[0])>0:
    	    	return volname
    
    return None


def get_new_vol_name(volname):
    """ Create a new name for the historical volatility
    The new name is on the format: old_name<underscore>historical_date """
    if len(volname) + len(ael.date_today().to_string()) + 1> 30:
    	length = 30 - len(ael.date_today().to_string()) - 1
	stlist = [volname[0:length], ael.date_today().to_string()]
    	new_name = string.join(stlist, "_")
	test = test_if_name_in_db(new_name)
	i=0
	while not test == None:
	    nr = '%d' % (i)
	    
    	    length = 30 - len(ael.date_today().to_string()) - 2 - len(nr)

    	    stlist1 = [volname[0:length], str(nr)]
	    stlist2 = string.join(stlist1, "_")
	    new_name1 = [stlist2, ael.date_today().to_string()]
	    new_name     = string.join(new_name1, "_")
	    
	    
    	    test = test_if_name_in_db(new_name)
    	    i=i+1

    else:
    	stlist = [volname, ael.date_today().to_string()]
	new_name = string.join(stlist, "_")

	test = test_if_name_in_db(new_name)
	i=0
	while not test == None:
	    
	    nr = '%d' % (i)
	    	    
            if len(volname) + len(ael.date_today().to_string()) + 2 + len(nr)> 30:
	    	name_len = 30 - 3 -len(ael.date_today().to_string()) 
    	    else:
	    	name_len = len(volname)

    	    stlist1 = [volname[0:name_len], str(nr)]
	    stlist2 = string.join(stlist1, "_")
	    new_name1 = [stlist2, ael.date_today().to_string()]
	    new_name     = string.join(new_name1, "_")
    	    test = test_if_name_in_db(new_name)
    	    i=i+1
    
    return new_name

def store_vol(vol):
    """ Create new volatility """
    vol_new = vol.new()
    vol_new.historical_day = ael.date_today()
    vol_new.original_vol_seqnbr=vol.seqnbr
    vol_new.archive_status=1
    vol_new.vol_name = get_new_vol_name(vol.vol_name)
    
    # Archive child tables 
    el_list = [ vol_new.points(), \
    	    	vol_new.beta_benchmarks(), \
		vol_new.beta_points(), \
		vol_new.skews()]
    
    
    for sub_list in el_list:
    	for el in sub_list:
	    el.archive_status = 1 
    
    # Commit
    
    try:
        vol_new.commit()
        return vol_new
    except:
        logme('Failed to store volatility %s' % vol.vol_name, 'ERROR')
    
    return None

 

def find_last_historical_vol(orig_vol):
    """ Find the corresponding volatility with historical_day = today """
    sql_query = """select seqnbr from volatility """ \
    	    	"""where original_vol_seqnbr = %d and historical_day = '%s'""" % \
		(orig_vol.seqnbr, ael.date_today())
		
    for set in ael.dbsql(sql_query):
    	for column in set:
    	    if int(column[0])>0:
    	    	vol = ael.Volatility[column[0]]
    	    	return vol
    return None

def update_base_vol(vol):
    last_hist_vol = find_last_historical_vol(vol)
    if not last_hist_vol == None:
    	vol_dictionary[vol.seqnbr] = last_hist_vol
	return last_hist_vol    
    new_vol = store_vol(vol)
    return new_vol


def recursive_store_vol(vol):
    """ Recursivly store a volatility hierarchy. The underlying vols are
    stored first """
    if not vol.original_vol_seqnbr == None:
    	return None
    try:
        already_stored_vol = vol_dictionary[vol.seqnbr]
        return already_stored_vol
    except:
        # If volatility is base curve
        if vol.und_vol_seqnbr == None:
	    stored_vol = update_base_vol(vol)
	    return stored_vol

        # If volatility has underlying
	stored_vol = update_base_vol(vol)

    	if not stored_vol == None:
	    vol_child = stored_vol.und_vol_seqnbr
    	    if not vol_child == None: 
    	    	stored_und_vol = recursive_store_vol(vol_child)
	    	stored_vol_clone = stored_vol.clone()
	    	stored_vol_clone.und_vol_seqnbr = stored_und_vol.seqnbr
		try:
	    	    stored_vol_clone.commit()
		except:
		    logme('ERROR: Failed to store volatility %s' \
                                % stored_vol_clone.vol_name, 'ERROR')
	    	stored_vol=stored_vol_clone
                
	    return stored_vol


def DefinedExclusions(e):
    for exp in VolatilityExclusions:
	if e == exp:
	    return 1
    return 0

def DefinedInclusion(e):
    for exp in VolatilityInclusions:
	if e == exp:
	    return 1

    return 0

def DefinedSuffix(e):
    target = e.vol_name
    suffix = FMtMVariables.VolSuffix[0]
    string.join(suffix, "$")
    ma = re.search(suffix, target)
    if ma==None:
	return 0
    else:
	return 1


def GetDefinedSet():

    def_set = []
    if VolatilityBase == 1:
    	for e in ael.Volatility.select('original_vol_seqnbr = 0'):
	    if not DefinedExclusions(e.vol_name):
	    	def_set.append(e)
	    	
    elif VolatilityBase == 2:
    	for e in FMtMVariables.VolSurfaces:
	    if not DefinedExclusions(e):
	    	yc = ael.Volatility[e]
	    	def_set.append(yc)
		
	for e in VolatilityInclusions:
	    yc = ael.Volatility[e]
	    def_set.append(yc)

    	for e in ael.Volatility.select():
	    if DefinedSuffix(e):
	    	yc = ael.Volatility[e]
	    	def_set.append(yc)
    
    elif VolatilityBase == 0:
 	for e in VolatilityInclusions:
	    if not DefinedExclusions(e):
	    	yc = ael.Volatility[e]
	    	def_set.append(yc) 

    return def_set

def update_all_vol():
    """ Store historical volatilities according to the settings in FVPSVariables.
    Main function. """
    vol_dictionary = {}
    delete_all_vol_of_today()
    logme("\nStart storing historical volatilities...\n")
    all_vol=GetDefinedSet()
    for vol in all_vol:
        if (vol != None and vol.historical_day == None ):
    	    logme("Storing Volatility %s" % vol.vol_name)
    	    recursive_store_vol(vol)

    logme("All volatilities stored.")
