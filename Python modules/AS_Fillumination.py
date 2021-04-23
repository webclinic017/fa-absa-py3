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
2005-09-28  	    Andries Brink   	    	    Added Check for BESA Member Agreement Compliance
ENDDESCRIPTION

-----------------------------------------------------------------------------"""

import ael
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
	# moved to validate_transaction below
#   	    if ((e.counterparty_ptynbr.add_info('BESA_Member_Agree') == 'No') and (e.insaddr.instype == 'Bond')):
#	    	print 'The party that you selected to trade with does not have a BESA Client agreement set up. Please contact BRM Documentations Management'
#		raise 'The party that you selected to trade with does not have a BESA Client agreement set up. Please contact BRM Documentations Management'
	
	
	else:
	    #  Check if a counterparty was filled in
	    print('Please select a Counterparty')
	    raise 'Please select a Counterparty'	
	#   Check that the value date is greater or equal to trade time    	
	if ael.date_from_time(e.time) > e.value_day:
	    print('Trade time can not be after that value date please change the time')        
	    raise 'Trade time can not be after that value date please change the time'        
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





def validate_transaction(transaction_list, *rest):

    e_ins = transaction_list[0][0]
    op1 = transaction_list[0][1]

    if e_ins.record_type == 'Instrument' and op1 != 'Delete':
    	try:
	    e_trd = transaction_list[1][0]
	    op2 = transaction_list[1][1]
	    if e_trd.record_type == 'Trade' and op2 != 'Delete':
	        #  Check for BESA Member Agreement Compliance
    	    	if ((e_trd.counterparty_ptynbr.add_info('BESA_Member_Agree') == 'No') and (e_ins.instype == 'Bond')):
    	    	    print('The party that you selected to trade with does not have a BESA Client agreement set up. Please contact BRM Documentations Management')
    	    	    raise 'The party that you selected to trade with does not have a BESA Client agreement set up. Please contact BRM Documentations Management'

	except:
	    #when only an instrument is booked
	    return 
	    
    return   
	
