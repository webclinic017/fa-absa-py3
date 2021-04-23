"""-----------------------------------------------------------------------------
MODULE	  FValidation

Version: 1.1

DESCRIPTION

This module is for adding extra validation rules to comitted data 
to ensure data integrety.

History:
Date	    	    Who     	    	    	    	    What

2004-03-17  	    Hardus Jacobs   	    	    Created: Prevent party of type None to be used
2004-04-05  	    Kim Madley	    	    	    Updated		    
2005-01-12  	    Hardus  	    	    	    Added Check for FICA Compliance
2005-09-28  	    Andries Brink   	    	    Added Check for BESE Member Agreement Compliance
2006-03-24  	    Aaeda Salejee   	    	    Added check for Bonds booked after 13:00
ENDDESCRIPTION

-----------------------------------------------------------------------------"""

import ael, time
def validate_entity(e, op):
    if e.record_type == 'Trade' and op != 'Delete':
    	if e.counterparty_ptynbr:
    	    #  Check that party is not of type None
	    if e.counterparty_ptynbr.type == 'None':
	    	print('Unable to commit the trade because the counterparty is of type none please pick another counterparty')
	    	raise 'Unable to commit the trade because the counterparty is of type none please pick another counterparty'
	    	exec('Unable to commit the trade because the counterparty is of type none please pick another counterparty')
	    
	    #  Check for FICA Compliance
	    if e.counterparty_ptynbr.add_info('FICA_Compliant') == 'No':	
	    	print('The party that you selected to trade with is Frozen. Please contact ORV Client Maintenance')
		raise 'The party that you selected to trade with is Frozen. Please contact ORV Client Maintenance'
	
	#  Check for BESE Member Agreement Compliance
	    if ((e.counterparty_ptynbr.add_info('BESA_Member_Agree') == 'No') and (e.insaddr.instype == 'Bond')):	
	    	print('The party that you selected to trade with does not have a BESA Client agreement set up. Please contact BRM Documentations Management')
		raise 'The party that you selected to trade with does not have a BESA Client agreement set up. Please contact BRM Documentations Management'
	
	
	else:
	    #  Check if a counterparty was filled in
	    print('Please select a Counterparty')
	    raise 'Please select a Counterparty'	
	#   Check that the value date is greater or equal to trade time    	
	if ael.date_from_time(e.time) > e.value_day:
	    print('Trade time can not be after that value date please change the time')        
	    raise 'Trade time can not be after that value date please change the time'        
	    
	    
	    
   	# Check that no Bonds are booked after 13:00 except by someone with BASE_MO in their profile
#	if e.insaddr.instype == 'Bond' and op == 'Insert':
#    	    for p in e.owner_usrnbr.profile_links():
#    	    	if p.profnbr.profid == 'BASE_MO':
#    	    	    flag = 'yes'
#    	    	else:
#    	    	    flag = 'no'
#
#    	    if e.value_day == ael.date_today():
#    	    	if time.strftime('%H:%M:%S') >= '13:00:00' :
#		    if flag == 'no' :
#    	    	    	print 'Bonds with value date today cannot be booked after 13:00, please contact the Bonds Position Manager'
#    	    	    	raise 'Bonds with value date today cannot be booked after 13:00, please contact the Bonds Position Manager'
	    
	    
	    
	    
	    
    #elif e.record_type == 'Leg': 
    #	if ((e.insaddr.instype in ['Swap','FRA','CAP','FLOOR','Deposit']) and (op == 'Insert' or op == 'Update')):
    #	    if (e.type == 'Fixed' or e.type == 'Zero Coupon Fixed' or e.type == 'Call Fixed'):
    #	    	if e.fixed_rate < 0:
    #	   	    print 'Unable to commit the Instrument. The fixed rate can not be negative'
    #	    	    raise 'Unable to commit the Instrument. The fixed rate can not be negative'
    #	    	    exec('Unable to commit the Instrument. The fixed rate can not be negative')
	 	    
   # elif e.record_type == 'CashFlow':
   # 	if (op == 'Insert' or op == 'Update'):
   # 	    if e.legnbr:
   # 	    	if (e.legnbr.type == 'Fixed' or e.legnbr.type == 'Zero Coupon Fixed' or e.legnbr.type == 'Call Fixed'):
   # 	    	    if e.rate < 0:
   # 		    	print 'Unable to commit the Cashflow. The fixed rate can not be negative'
   # 	    	    	raise 'Unable to commit the Cashflow. The fixed rate can not be negative'
   # 	    	    	exec('Unable to commit the Cashflow. The fixed rate can not be negative')     
    return
    
    	#Trickle feed test ABAW339
    	#out = open('C:\\trickle.txt','w')
	#out.write('%d,%s\n' %(e.trdnbr, e.record_type))
	#print e.pp()


