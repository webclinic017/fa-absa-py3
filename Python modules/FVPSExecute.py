""" VPS:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FVPSExcecute - Stores historical valuation parameters

(c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
	Main module for storing valuation parameters. Reload the module
	to execute the storage procedure. Make sure that FVPSVariables
	exist and that the variables are set.
		
 	
----------------------------------------------------------------------------"""
# Import builtin modules
import ael
import time

# Import parameter and help Front modules
import FVPSPrintout
import FVPSVariables


# Inititalise logging
try:
    FVPSPrintout.logme.setLogmeVar(FVPSVariables.ScriptName, \
                  FVPSVariables.LogMode, \
                  FVPSVariables.LogToConsole, \
                  FVPSVariables.LogToFile, \
                  FVPSVariables.Logfile)
    
except AttributeError, msg:  
    err_msg = "\nError in FVPSVariables:\t"+str(msg)+ \
    "\nMake sure the attribute (=variable) exists" \
    "\nIf it does exist try reloading the AEL module FVPSVariables\n"
    raise err_msg

logme = FVPSPrintout.logme
logme(None, 'START')

# Import Front modules
import FVPSCombinationLink
reload(FVPSCombinationLink)
import FVPSCorrelationMatrix
import FVPSDividendStream
import FVPSRatingHistory
import FVPSYieldCurve
import FVPSVolatility


run_vps = 1
type_of_object = 'All'

def help_text():
    msg = 'Available arguments to FVPSExecute.py: \n ' + \
          '\t-a ads address\n' +\
          '\t-u username\n' +\
          '\t-p password\n' +\
          '\t-h help   \toptional\n' +\
          '\t-d date to delete\toptional\n' +\
          '\t-t object to delete\toptional\n' +\
          '\t   Valid values for -t argument:\n' +\
          '\t\tAll\n' +\
          '\t\tYieldCurve\n' +\
          '\t\tVolatility\n' +\
          '\t\tCombinationLink\n' +\
          '\t\tCorrelationMatrix\n' +\
          '\t\tDividendStream\n' +\
          '\t\tCreditHistory\n'
    return msg

def delete_all_on_a_date(olddate, subject):
    
    logme("Start deleting...")
    if subject in ("CombinationLink", "All"):
        FVPSCombinationLink.delete_all_cl_of_a_day(olddate)
    if subject in ("CorrelationMatrix", "All"):
        FVPSCorrelationMatrix.delete_all_cm_of_a_day(olddate)
    if subject in ("DividendStream", "All"):
        FVPSDividendStream.delete_all_ds_of_a_day(olddate)
    if subject in ("CreditHistory", "All"):
        FVPSRatingHistory.delete_all_credit_history_of_a_day(olddate)
    if subject in ("YieldCurve", "All"):
        FVPSYieldCurve.delete_all_yc_of_a_day(olddate)
    if subject in ("Volatility", "All"):
        FVPSVolatility.delete_all_vol_of_a_day(olddate)
    logme("\nValuation Parameter deletion finished %s" % time.ctime(time.time()))    


"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""

if __name__ == "__main__":
    import sys, getopt

    

    try:
        opts, args = getopt.getopt(sys.argv[1:], 
	    	    	    	   's:u:p:v:f:h:d:t:')
    except getopt.error, msg:
        print help_text()
        sys.exit(2)

    date_to_delete = None
    type_of_object = None
    ads_address = None
    ads_user = None
    ads_passw = None
    for o, a in opts:
        if o == '-s': ads_address = a
        if o == '-u': ads_user = a
        if o == '-p': ads_passw = a
        if o == '-h': print help_text()
	if o == '-d': date_to_delete = a
        if o == '-t' : type_of_object = a

    try:
        ael.connect(str(ads_address), str(ads_user), str(ads_passw))
        logme("Connected to %s as %s" % (ads_address, ads_user), 'INFO')
    except:
        logme("Could not connect to AEL with the following arguments", 'ERROR')
        logme("ads_address: %s" % ads_address, 'ERROR')
        logme("ads_user: %s" % ads_user, 'ERROR')
        logme("ads_password: %s" % ads_passw, 'ERROR')
        raise

    if type_of_object == None:
        type_of_object = 'All'
    if type_of_object not in ('All', 'YieldCurve', 'Volatility', 'CombinationLink', \
                              'CorrelationMatrix', 'DividendStream', 'CreditHistory'):
        logme(help_text(), 'ERROR')
        sys.exit(2)
    
    if date_to_delete != None:
	try:
            if date_to_delete == 'TODAY':
                checkdate = ael.date_today()
            else:
                checkdate = ael.date(date_to_delete)
	except:
	    logme("Unable to read the date. The deletion will be terminated", 'ERROR')
	    ael.disconnect()
	    raise
	
	delete_all_on_a_date(checkdate, type_of_object)
    	ael.disconnect()

        run_vps = 0


if run_vps:
    if type_of_object in ('All', 'CombinationLink'):
        FVPSCombinationLink.update_all_cl()    
    if type_of_object in ('All', 'CorrelationMatrix'):
        FVPSCorrelationMatrix.update_all_cm()
    if type_of_object in ('All', 'DividendStream'):
        FVPSDividendStream.update_all_ds()
    if type_of_object in ('All', 'CreditHistory'):
        FVPSRatingHistory.update_all_instrument()
    if type_of_object in ('All', 'YieldCurve'):
        FVPSYieldCurve.update_all_yield_curve()
    if type_of_object in ('All', 'Volatility'):
        FVPSVolatility.update_all_vol()
        
logme(FVPSVariables.ScriptName, 'FINISH')    


