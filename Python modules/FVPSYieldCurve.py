""" VPS:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FVPSYieldCurve - Stores historical yield curves

        (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
	Functionality for storing and deleting historical entities of
        type YieldCurve
	
----------------------------------------------------------------------------"""
import string
import ael
import amb
import FVPSPrintout
from FVPSVariables import *

logme = FVPSPrintout.logme

try:
    import FMtMVariables
    FMtMDefined = 1
except:
    if YieldCurveBase == 2:
    	YieldCurveBase = 1

    FMtMDefined = 0

BIG_DATE = ael.BIG_DATE
MAX_DELETE_ATTEMPTS = 100
yc_dictionary = {}

"""
Performance improvements can be made here by not calling is_referenced_by
when deleting yield curves. The cost will be error messages from dsb92api printed
in the log/batch prompt.
"""

def is_referenced_by(yc, old_date):
    """ Check if yield curve is referenced by another yield curve """
    sql_query = """select seqnbr from yield_curve """ \
    	    	"""where historical_day = '%s'""" % (old_date)
    j = len(ael.dbsql(sql_query))
    for set in ael.dbsql(sql_query):
	i=len(set)
	for column in set:
    	    yc_temp = ael.YieldCurve[column[0]]

    	    if yc_temp.underlying_yield_curve_seqnbr != None:	    
    	    	if yc_temp.underlying_yield_curve_seqnbr.seqnbr == yc.seqnbr:
	    	    return 1
		
    sql_query = """select seqnbr from instrument_spread """ 
    
    j = len(ael.dbsql(sql_query))
    for set in ael.dbsql(sql_query):
	i=len(set)
	for column in set:
    	    is_temp = ael.InstrumentSpread[column[0]]
    	    if is_temp.underlying_yield_curve_seqnbr != None:
	    	if is_temp.underlying_yield_curve_seqnbr.seqnbr == yc.seqnbr:
	    	    return 1
		
     	    if is_temp.yield_curve_seqnbr != None:
		if is_temp.yield_curve_seqnbr.seqnbr == yc.seqnbr:
	    	    return 1
	    
    return 0

    
def delete_all_yc_of_a_day(old_date):
    """ Delete all historical yield curves on a specified date. The yield curves
    lowest in the hierarchy will be deleted first """
    
    i = 2
    j = 2

    #def yc_names(o):
    #    return o.yield_curve_name

    failures = {}
    # defined_objects = GetDefinedSet()
    # defined_set = map(yc_names,defined_objects)
    
    logme("\nDeleting historical yield curves as of %s...\n" % \
          str(old_date), 'INFO')
                      
    while i>1 and j>0:
    	sql_query = """select seqnbr from yield_curve """ \
    	    	"""where historical_day = '%s'""" % (old_date)
    	
	j = len(ael.dbsql(sql_query))
	for set in ael.dbsql(sql_query):
	    i=len(set)
	    for column in set:
    	        yc = ael.YieldCurve[column[0]]
                #live_yc = yc.original_yc_seqnbr
                #if live_yc.yield_curve_name not in defined_set:
                #    i = i - 1
                #    continue
                if not is_referenced_by(yc, old_date):
	            try:
     	    	    	yc.delete()
	            	logme("Deleted %s" % yc.yield_curve_name, 'INFO')
	            except:
                        name = yc.yield_curve_name
	            	logme("Unable to delete %s, will attempt again" % name, 'DEBUG')
                        if failures.has_key(name):
                            failures[name] = failures[name] + 1
                        else:
                            failures[name] = 1
                        if failures[name] > MAX_DELETE_ATTEMPTS:
                            logme("Unable to delete %s" % name, 'ERROR')
                            return 0
		else:
                    try:
                        yc.delete()
                        logme("Deleted %s" % yc.yield_curve_name, 'INFO')
                    except:
                        name = yc.yield_curve_name
                        logme("Unable to delete referenced yield curve %s, attempting again" \
                              % name, 'DEBUG')
                        if failures.has_key(name):
                            failures[name] = failures[name] + 1
                        else:
                            failures[name] = 1
                        if failures[name] > MAX_DELETE_ATTEMPTS:
                            logme("Unable to delete %s" % name, 'ERROR')
                            return 0
		    
    logme("\nAll historical yield curves as of %s deleted\n" % str(old_date), 'INFO')

    return 1


def test_if_name_in_db(ycname):
    """ Is the new yield curve name already in the database ? """
    sql_query = """select count(1) from yield_curve where yield_curve_name = '%s'""" % ycname

    for set in ael.dbsql(sql_query):
    	for column in set:
    	    if int(column[0])>0:
    	    	return ycname
    
    return None

def get_new_yc_name(cmname):
    """ Create a new name for the historical yield curve
    The new name is on the format: old_name<underscore>historical_date """
    if len(cmname) + len(ael.date_today().to_string()) + 1> 30:
    	length = 30 - len(ael.date_today().to_string()) - 1
	stlist = [cmname[0:length], ael.date_today().to_string()]
    	new_name = string.join(stlist, "_")
	test = test_if_name_in_db(new_name)
	i=0
	while not test == None:
	    nr = '%d' % (i)
    	    length = 30 - len(ael.date_today().to_string()) - 2 - len(nr)

    	    stlist1 = [cmname[0:length], str(nr)]
	    stlist2 = string.join(stlist1, "_")
	    new_name1 = [stlist2, ael.date_today().to_string()]
	    new_name     = string.join(new_name1, "_")
	    
    	    test = test_if_name_in_db(new_name)
    	    i=i+1

    else:
    
    	stlist = [cmname, ael.date_today().to_string()]
	new_name = string.join(stlist, "_")


	test = test_if_name_in_db(new_name)
	i=0
	while not test == None:
    
	    nr = '%d' % (i)
	    	    
            if len(cmname) + len(ael.date_today().to_string()) + 2 + len(nr)> 30:
	    	name_len = 30 - 3 -len(ael.date_today().to_string()) 
    	    else:
	    	name_len = len(cmname)

    	    stlist1 = [cmname[0:name_len], str(nr)]
	    stlist2 = string.join(stlist1, "_")
	    new_name1 = [stlist2, ael.date_today().to_string()]
	    new_name     = string.join(new_name1, "_")
    	    test = test_if_name_in_db(new_name)
    	    i=i+1
    
    
    return new_name

def find_last_historical_yc(origyc):
    """ Search for an historical yield curve with historical_day = today.
    If no yield curve exist the function will return None """
    sql_query = """select seqnbr from yield_curve """ \
    	    	"""where original_yc_seqnbr = %d and historical_day = '%s'""" % \
		(origyc.seqnbr, ael.date_today())
		
    for set in ael.dbsql(sql_query):
    	for column in set:
    	    if int(column[0])>0:
    	    	yc = ael.YieldCurve[column[0]]
    	    	return yc
    return None

def set_archive_flag_on_children(yc):
    yc_points = yc.points()
    
    for point in yc_points:
	point.archive_status = 1

    yc_is_spreads = yc.instrument_spreads()

    for child_is in yc_is_spreads:
	child_is.archive_status = 1

def store_yield_curve(liveyc):
    """ Stores a yield curve. If the yield curve has underlying curve(s)
    the children will be stored first """
    try:
    	already_stored_yc = yc_dictionary[liveyc.seqnbr]
        return already_stored_yc
    except:    
        newyc = liveyc.new()
    	newyc.yield_curve_name=get_new_yc_name(liveyc.yield_curve_name)
    	newyc.original_yc_seqnbr=liveyc.seqnbr
    	newyc.historical_day=ael.date_today()
    	newyc.archive_status=1
	set_archive_flag_on_children(newyc)

    	try:
    	    newyc.commit()
	except:
	    logme("Unable to make yield curve %s historical. Check your logfile." % \
                  liveyc.yield_curve_name, 'ERROR')
	    return None
    
    	yc_dictionary[liveyc.seqnbr] = newyc

   
   	return newyc



def UpdateBaseYieldCurve(yc):
    last_hist_yc = find_last_historical_yc(yc)
    if not last_hist_yc == None:
    	yc_dictionary[yc.seqnbr] = last_hist_yc
	return last_hist_yc
    
    newyc = store_yield_curve(yc)
    
    return newyc
    
   
def update_is(yc):
    """ Stores instrument spread curves """    
    is_spr = ael.InstrumentSpread.select('yield_curve_seqnbr=%d' % yc.seqnbr)
    i=0
    for is_child in is_spr:
    	i=i+1
	if not is_child.underlying_yield_curve_seqnbr == None:
	    yc_child = ael.YieldCurve[is_child.underlying_yield_curve_seqnbr.seqnbr]
    	    stored_yc_child = UpdateBaseYieldCurve(yc_child)
	    if not stored_yc_child==None:
	    	is_child_clone = is_child.clone()
	    	is_child_clone.underlying_yield_curve_seqnbr = stored_yc_child.seqnbr
	    	is_child_clone.commit()
    	    		    	
    
def all_yc_children(yc):
    """ Returns a list of underlying yield curves """
    yc_list = {}
    
    m = yc.get_data_message()
    if m==None:
    	return None
	
    und_yc_object = m.mbf_find_object( "ATTRIBUTE_SPREAD", "MBFE_BEGINNING")
    
    if und_yc_object==None:
    	return None
    
    while not und_yc_object == None:
    	
	curr_object = und_yc_object.mbf_first_object()
    	while not curr_object == None:
	    if curr_object.mbf_get_name() == 'UND_YC':
    	    	try:
		    child_yc = ael.YieldCurve[curr_object.mbf_get_value()]
    	    	    stored_und_yc = update_yield_curve(child_yc)
    	    	    yc_list[child_yc.yield_curve_name] = stored_und_yc.yield_curve_name
    	    	except:
		    logme("Failed loading %s" % curr_object.mbf_get_value(), 'ERROR')
		    return None
            curr_object = und_yc_object.mbf_next_object()
	und_yc_object = m.mbf_next_object()
    
    return yc_list
 
 
def update_yc(yc, pair_list):
    """ Updates a yield curve with references to historical underlyings """
    yc_list = []

    cloned_yc = yc.clone()
    m = cloned_yc.get_data_message()
    if m==None:
    	return yc

    und_yc_object = m.mbf_find_object( "ATTRIBUTE_SPREAD", "MBFE_BEGINNING")
    
    if und_yc_object==None:
    	return yc
    
    while not und_yc_object == None:
	curr_object = und_yc_object.mbf_first_object()
    	while not curr_object == None:
	    if curr_object.mbf_get_name() == 'UND_YC':
		und_yc_object.mbf_replace_string("UND_YC", pair_list[curr_object.mbf_get_value()])
            curr_object = und_yc_object.mbf_next_object()
	und_yc_object = m.mbf_next_object()
    
    
   
    cloned_yc.set_data_message(m)
    cloned_yc.commit()
    yc_dictionary[yc.seqnbr] = cloned_yc

    return cloned_yc
    

   
def update_yield_curve(yc):
    """ Runs a recursive storage of a yield curve hierarchy """
    if not yc.historical_day == None:
	logme("ERROR: You tried to make a copy of a historical yield curve " + yc.yield_curve_name \
              + "\nThe execution will be stopped.", 'ERROR')
	return
    try:
    	
	already_stored_yc = yc_dictionary[yc.seqnbr]
	return already_stored_yc
	
    except:
    
        if yc.yield_curve_type == 'Benchmark':
	    stored_yc = UpdateBaseYieldCurve(yc)
	    return stored_yc
	
	
	stored_yc = UpdateBaseYieldCurve(yc)
    

    	if not stored_yc == None:
	    yc_child = stored_yc.underlying_yield_curve_seqnbr
    	    if not yc_child == None: 
    	    	stored_und_yc = update_yield_curve(yc_child)
	    	stored_yc_clone = stored_yc.clone()
		try:
	    	    stored_yc_clone.underlying_yield_curve_seqnbr = stored_und_yc.seqnbr
		except:
	            logme("Unable to find underlying yield curve to %s." % \
                          stored_und_yc.yield_curve_name, 'WARNING')
	    	stored_yc_clone.commit()
	    	stored_yc=stored_yc_clone
	    
    	if stored_yc<>None and yc.yield_curve_type == 'Attribute Spread':
    	    yc_children = all_yc_children(stored_yc)
	    child_dict = {}
	    
	    if not yc_children == None:
        	stored_yc=update_yc(stored_yc, yc_children)	        
	    
    	    
	    return stored_yc



    	if stored_yc <> None and stored_yc.yield_curve_type == 'Instrument Spread':
	    update_is(stored_yc)

    	return stored_yc
  

def DefinedExclusions(e):
    for exp in YieldCurveExclusions:
	if e == exp:
	    return 1
    return 0

def DefinedInclusion(e):
    for exp in YieldCurveInclusions:
	if e == exp:
	    return 1

    return 0

def GetDefinedSet():

    def_set = []
    if YieldCurveBase == 1:
    	for e in ael.YieldCurve.select('original_yc_seqnbr = 0'):
            if not DefinedExclusions(e.yield_curve_name):
	    	def_set.append(e) 
	    	
    elif YieldCurveBase == 2:
    	for e in FMtMVariables.YieldCurves:
	    if not DefinedExclusions(e):
	    	yc = ael.YieldCurve[e]
	    	def_set.append(yc) 
		
	for e in YieldCurveInclusions:
	    yc = ael.YieldCurve[e]
	    def_set.append(yc)     
    elif YieldCurveBase == 0:
 	for e in YieldCurveInclusions:
	    if not DefinedExclusions(e):
	    	yc = ael.YieldCurve[e]
	    	def_set.append(yc) 


    return def_set
    
def update_all_yield_curve():
    """ Store historical yield curves according to the settings in FVPSVariables.
    Main function. """
    delete_all_yc_of_a_day(ael.date_today())

    logme("\nStart storing historical yield curves...\n", 'INFO')
    yc_dictionary = {}
    all_yc=GetDefinedSet()
    for yc in all_yc:
        if yc != None and yc.historical_day == None:
	    logme("Storing yield curve %s " % yc.yield_curve_name, 'INFO')
   	    update_yield_curve(yc)
    	

    logme("All yield curves stored", 'INFO')
