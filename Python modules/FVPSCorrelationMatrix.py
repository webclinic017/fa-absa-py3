""" VPS:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FVPSCorrelationMatrix - Stores historical correlation matrices

        (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
	Functionality for storing and deleting historical entities of
        type CorrelationMatrix.

        If there exist no historical correlation matrix
        a new will always be created with
        date_from = today
        date_to = BIG_DATE

        If there exist a historical correlation matrix with date_to = BIG_DATE,
        this entity's date_to will be set to today and a new historical
        correlation matrix will be created with date_from = today and
        date_to = BIG_DATE.
        
	
----------------------------------------------------------------------------"""


import ael
import re
import string
import FVPSPrintout
from FVPSVariables import *

BIG_DATE = ael.BIG_DATE
logme = FVPSPrintout.logme

def delete_all_cm_of_a_day(old_date):
    """ Deletes all correlation matrices with date_from < old_date < date_to.
    If date_to = BIG_DATE the correlation matrix will not be deleted """
    i = 2
    j = 2

    logme("\nDeleting correlation matrices as of %s...\n" %
          str(old_date))

    while i>1 and j>0:
    
    	sql_query = """select seqnbr from correlation_matrix """ \
    	"""where date_to > '%s' and date_from < '%s' and date_to < '%s'""" \
	% (old_date, old_date, BIG_DATE)
	j = len(ael.dbsql(sql_query))
	for set in ael.dbsql(sql_query):
	    i=len(set)
	    for column in set:
    	        cm = ael.CorrelationMatrix[column[0]]
	        try:
     	    	    cm.delete()
	            logme("Deleted correlation matrix %s" % cm.name)
	        except:
	            logme("Unable to delete correlation matrix %s" % cm.name, 'ERROR')
    logme("All historical correlation matrices as of %s are deleted." \
          % str(old_date))

    return 1


def test_if_name_in_db(dsname):
    """ Is the new correlation matrix name already in the database ? """
    sql_query = """select count(1) from correlation_matrix where name = '%s'""" % dsname

    for set in ael.dbsql(sql_query):
    	for column in set:
    	    if int(column[0])>0:
    	    	return dsname
    
    return None


def read_bucket(bucket):
    """ Parse a bucket. Example '2y' will return ['2','Years'] """
    str1 = re.search("[dwmy]", bucket)

   
    unit=bucket[str1.start()]
    count = string.replace(bucket, unit, "")
    if unit=="d":
    	unit = "Days"
    if unit=="w":
    	unit = "Weeks"
    if unit=="m":
    	unit = "Months"    
    if unit=="y":
    	unit = "Years"    

    return [count, unit]

def delete_all_elements_in_matrix(cm):
    """ Deletes all volelements and correlations in a matrix """
    cm_clone = cm.clone()
    correlations = cm_clone.correlations()
    for i in range(len(correlations)):
        correlations[i].delete()
    	    
    volelements = cm_clone.volelements()
    for i in range(len(volelements)):
        volelements[i].delete()

    cm_clone.commit()
    

def get_new_corr_matrix_name(cmname):
    """ Create a new name for the historical correlation matrix
    The new name is on the format: old_name<underscore>historical_date """
    if len(cmname) + len(ael.date_today().to_string()) + 1> 30:
    	length = 30 - len(ael.date_today().to_string()) - 1
	stlist = [cmname[0:length], ael.date_today().to_string()]
    	new_name = string.join(stlist, "_")
	test = ael.CorrelationMatrix[new_name]
	i=0
	while not test == None:
	    nr = '%d' % (i)
	    
    	    length = 30 - len(ael.date_today().to_string()) - 2 - len(nr)

    	    stlist1 = [e.name[0:length], str(nr)]
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

def create_new_corr_matrix(corrmatrix):
    """ Creates a new historical correlation matrix """
    cm = corrmatrix.new()
    cm.date_from = ael.date_today()
    cm.date_to = BIG_DATE
    cm.original_cm_seqnbr=corrmatrix.seqnbr
    cm.archive_status=1
    cm.name = get_new_corr_matrix_name(corrmatrix.name)
    cm.commit()
    logme("Stored correlation matrix %s" % cm.name)
    return cm

def make_corr_matrix_historical(corrmatrix):
    """ Create a historical correlation matrix from a live one """
    cm = corrmatrix.clone()
    cm.date_to = ael.date_today()
    cm.commit()

def compare_corr_element(live, hist):
    """ Compares two correlation elements in from two correlation matrices """

    return (live.corr == hist.corr 
            and live.rec_type0 == hist.rec_type0
            and live.rec_type1 == hist.rec_type1
            and live.recaddr0 == hist.recaddr0
            and live.recaddr1 == hist.recaddr1
            and live.bucket0 == hist.bucket0
            and live.bucket1 == hist.bucket1)
    

def compare_vol_element(live, hist):
    """ Compares two volelements from two correlation matrices """

    return (live.vol == hist.vol
            and live.rec_type == hist.rec_type
            and live.recaddr == hist.recaddr
            and live.type == hist.type
            and live.bucket == hist.bucket)
        
def find_last_historical_matrix(origmatrix):
    """ Finds a historical correlation matrix with date_to = BIG_DATE """

    sql_query = """select seqnbr from correlation_matrix """ \
    	    	"""where original_cm_seqnbr = %d and date_to = '%s'""" % \
		(origmatrix.seqnbr, BIG_DATE)

    for set in ael.dbsql(sql_query):
    	for column in set:
    	    if int(column[0])>0:
    	    	ds = ael.CorrelationMatrix[column[0]]
    	    	return ds

    return None


def bigdate_matrix_equal_live(cmlive, cmbd):
    """ Compares two correlation matrices. First the dimensions are compared,
    then the values """
       
    sellive = cmlive.volelements()
    selbd = cmbd.volelements()

    if not len(selbd)==len(sellive):
        logme("Corr matrices %s %s has different number of volelements" % \
              (cmlive.name, cmbd.name), 'DEBUG')
    	return 0 #False = Not equal

    # Compare individual vol elements
    k = 0
    for i in range(len(sellive)):
        for j in range(len(selbd)):
            if compare_vol_element(sellive[i], selbd[j]):
                k = k + 1
                
    if k < len(sellive):
        logme("Corr matrices %s %s has at least one volelement that differs" % \
              (cmlive.name, cmbd.name), 'DEBUG')        
        return 0
    
    sellive = cmlive.correlations()
    selbd = cmbd.correlations()
    
    if not len(selbd)==len(sellive):
        logme("Corr matrices %s %s has different number of correlements" % \
              (cmlive.name, cmbd.name), 'DEBUG')
    	return 0 #False = Not equal

    k = 0
    for i in range(len(sellive)):
        for j in range(len(selbd)):
            if compare_corr_element(sellive[i], selbd[j]):
                k = k + 1
                
    if k < len(sellive):
        logme("Corr matrices %s %s has at least one corr element that differs" % \
              (cmlive.name, cmbd.name), 'DEBUG')
        return 0

    return 1

def copy_complete_cm(origmatrix, lastcm):
    """ Transfer all correlation and vol elements to a
    historical correlation matrix """
    if lastcm == None:
        logme("Creating new corr matrix %s" % origmatrix.name, 'DEBUG')
    	bigdate_cm = create_new_corr_matrix(origmatrix)
    else:
        logme("Using big date matrix %s" % origmatrix.name, 'DEBUG')
    	bigdate_cm = lastcm
	
    
    bigdate_cm_clone = bigdate_cm.clone()
    logme("Cloning big date correlation matrix", 'DEBUG')
    sel_corr = bigdate_cm_clone.correlations()
    for i in range(len(sel_corr)):
        logme("Correlation element archived", 'DEBUG')
    	sel_corr[i].archive_status = 1
	
    sel_vol = bigdate_cm_clone.volelements()
    for i in range(len(sel_vol)):
        logme("Volelement archived", 'DEBUG')
    	sel_vol[i].archive_status = 1
    try:
        bigdate_cm_clone.commit()
        logme("Stored correlation matrix %s" % bigdate_cm_clone.name)
    except:
        logme("Unable to store correlation matrix %s" % bigdate_cm_clone.name)
    

def update_correlation_matrix(cm):
    """ Update an existing matrix and create a new historical
    if necessary """

    last_historical_cm = find_last_historical_matrix(cm)

    if last_historical_cm == None:
        copy_complete_cm(cm, None)
    	return 1

    if bigdate_matrix_equal_live(cm, last_historical_cm):
        logme("Nothing changed for correlation matrix %s" % cm.name, 'DEBUG')
    	return 1
    
    if not last_historical_cm.date_from == ael.date_today():
    	make_corr_matrix_historical(last_historical_cm)
	new_historical = None
    else:
    	#If it already exist a historical data with date_to = today
	#we should use that instead of creating a new one.
	#The CorrelationMatrix will be kept but all the children
	#will be deleted
    	#delete_all_elements_in_matrix(last_historical_cm)
        # The comments above  re probably not correct.
	new_historical = None #last_historical_cm
	
    copy_complete_cm(cm, new_historical)
    
    return 1

def DefinedExclusions(e):
    for exp in CorrelationMatrixExclusions:
	if e == exp:
	    return 1
    return 0

def DefinedInclusion(e):
    for exp in CorrelationMatrixInclusions:
	if e == exp:
	    return 1

    return 0

def GetDefinedSet():

    def_set = []
    if CorrelationMatrixBase == 1:
    	for e in ael.CorrelationMatrix.select('original_cm_seqnbr = 0'):
	    if not DefinedExclusions(e.name):
	    	def_set.append(e) 
	    	
    elif CombinationLinkBase == 0:
 	for e in CorrelationMatrixInclusions:
	    if not DefinedExclusions(e):
	    	cm = ael.CorrelationMatrix[e]
	    	def_set.append(cm) 


    return def_set


def update_all_cm():
    """ Stores correlation matrices according to the settings in FVPSVariables.
    Main function. """

    logme("\nStart storing historical correlation matrices... \n")

    for e in GetDefinedSet():
        if (e.original_cm_seqnbr == None and e.date_to == None):
            update_correlation_matrix(e)

    logme("All correlation matrices stored")



