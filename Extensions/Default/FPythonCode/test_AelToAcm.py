from __future__ import print_function
import ael
import acm

import unittest


class TestAelToAcm(unittest.TestCase):

	def test_aelToAcm(self):
	    
	    if (ael.archived_mode() == acm.ArchivedMode()):
	        print ('ArchivedMode test ok')
	
	    acmU1 = acm.ConnectedUsers()[0]
	    #Acm version of connected users returns a list of dictionaries whereas the ael version. Creating a tuple.
	    acmU1tuple = (acmU1['Application'], acmU1['User'], acmU1['OS User'], acmU1['Node'], acmU1['#Upd'], acmU1['#Req'], acmU1['Sessid'], acmU1['Connected at'])        
	    #Ael varsion of connected users returns a list of tuples so just grap the first one.
	    aelU1tuple = ael.connected_users()[0]
	    
	    if aelU1tuple == acmU1tuple:
	        print ('ConnectedUsers test ok')
	
	    
	    if acm.ArchivedMode() == ael.archived_mode():
	        print ('ArchivedMode test ok')
	        
	    
	    if ael.enum_from_string('StatusExplanation', 'Change to source data') == acm.EnumFromString('StatusExplanation', 'Change to source data'):
	        print ('EnumFromString test ok')
	    
	    if ael.enum_to_string('StatusExplanation', 9) == acm.EnumToString('StatusExplanation', 9).AsString():
	        print ('EnumToString test ok')
	    
	    if ael.get_config_var('TEMP') == acm.GetConfigVar('TEMP').AsString():
	        print ('GetConfigVar test ok')
	        
	    if ael.hide_password('verySecret') == acm.HidePassword('verySecret').AsString():
	        print ('HidePassword test ok')
	        
	    if ael.used_acc_curr() == acm.UsedAccountingCurrency().AsString():
	        print ('UsedAccountingCurrency test ok')
	       
	    if ael.used_valuation_parameters().name == acm.UsedValuationParameters().Name():
	        print ('UsedValuationParameters test ok')
	        
	def test_dateFunctions(self):        
	    f = acm.GetFunction("dayOfYear", 1)    
	    if f("2007-09-27") == ael.date('2007-09-27').day_of_year():
	        print ('dayOfYear test ok')
	    
	    f = acm.GetFunction("dayOfWeek", 1)    
	    if f("2007-09-27") == ael.date('2007-09-27').day_of_week():
	        print ('dayOfWeek test ok')
	        
	    f = acm.GetFunction("phaseOfTheMoon", 1)        
	    if ael.date('2007-09-27').phase_of_the_moon() == f("2007-09-27"):
	        print ('phaseOfTheMoon test ok')
	    
	    f = acm.GetFunction("dateFromTime", 1)
	    if f(9999999) == str(ael.date_from_time(9999999)):
	        print ('dateFromTime test ok')
	    
	    if acm.FDateTimeUtil().DatePeriodsInYear("1w") == ael.date_periods_in_year("1w"):
	        print ('DatePeriodsInYear test ok')
	    
	    if str(ael.date_valueday()) == acm.FDateTimeUtil().DateValueDay():
        	print ('DateValueDay test ok')
	    
	    





