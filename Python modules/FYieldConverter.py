'''FYieldConverter: last updated on Thu Aug 21 14:13:55 2003. Extracted by Stowaway on 2003-10-28.'''
import ael
from math import exp, log

####################################################################
#
# The yield_converter function has been designed to be used with a 
# query and hence the first argument, an object, is not used.
#
# The other argments are:
#   
#   inconvention - the  cpn frequency of the 'in' yield
#   ylddisc - whether the rate is yield or discount
#   rate - the rate to be converted
#   outconvention - the output rate convention (NACM, NACA etc)
#
#   Created by Panos Prodromou August 2003
#
####################################################################

def yield_converter(inst,inconvention,ylddisc,days,rate,outconvention,*rest):

# Convert in convention from an integer to named convention
#    	print inst.insid
	if inconvention == 1:
	    inNA = 'NACA'
	elif inconvention == 2:
	    inNA = 'NACS'
	elif inconvention == 4:
	    inNA = 'NACQ'
	elif inconvention == 12:
	    inNA = 'NACM'
	elif inconvention == 52:
	    inNA = 'NACW'
	elif inconvention == 365:
	    inNA = 'NACD'
	elif inconvention == 1000:
	    inNA = 'NACC'
	else:
	    inNA = 'NACC'

# Convert out convention from named convention to integer
	    
	if outconvention == 'NACA':
	    outNA = 1
	elif outconvention == 'NACS':
	    outNA = 2
	elif outconvention == 'NACQ':
	    outNA = 4
	elif outconvention == 'NACM':
	    outNA = 12
	elif outconvention == 'NACW':
	    outNA = 52
	elif outconvention == 'NACD':
	    outNA = 365
	elif outconvention == 'NACC':
	    outNA = 1000
	else:
	    inNA = 'NACC'
	    
# If yield is the type 

    	if ylddisc == 'Yield':
	    inconvention=float(inconvention)
    	    rate=float(rate)/100
    	    Rcont = convert_to_cont(inNA, inconvention, rate)
    	    Rperiod = convert_from_cont(outNA, Rcont)
	    
	elif ylddisc == 'Discount':
#	    print 'Discount'
#	    print rate, days, inNA, outNA
	    rate = float(rate)/100
	    simple = convert_discount_to_simple(rate, days)
#	    print 'Simple is', simple
	    simple = simple/100
    	    Rcont = convert_simple_to_cont(simple, days)
#	    print 'Discount Rcont is', Rcont
	    Rperiod = convert_from_cont(outNA, Rcont)
	elif ylddisc == 'Simple':
#	    print 'Simple'
	    rate=float(rate)/100
	    Rcont = convert_simple_to_cont(rate, days)
#	    print Rcont
	    Rperiod = convert_from_cont(outNA, Rcont)
	else:
	    raise 'Invalid type definition'

	return Rperiod
	
def convert_to_cont(inNA, incon, rate):

####################################################################
#
# This function takes three (3) arguments:
#
#   inNA  - input convention NACA, NACM, NACQ, etc
#   incon - input frequency
#   rate - rate to be converted to continuous rate
#
# The function converts from an NACx rate to a continuous rate
#
####################################################################

    if inNA != 'NACC':
	Rcont = incon*log(1+rate/incon)
#    	print 'Rcont is', Rcont
    else:
	Rcont = rate/100
    return Rcont
    
def convert_from_cont(outNA, Rcont):

####################################################################
#
# This function takes two (2) arguments:
#
#   outNA  - input convention e.g. NACA expressed as an integer
#   Rcont - a continuous
#
# The function converts from a continuous rate to an NACx rate 
#
####################################################################
  
    Rperiod = outNA*(exp(Rcont/outNA)-1)
#    print Rperiod

    return Rperiod*100


def convert_discount_to_simple(rate, days):

####################################################################
#
# This function takes two (2) arguments:
#
#   rate  - a discount rate
#   days - days in the period
#
# The function converts from a discount rate to a simple rate 
#
####################################################################

    
    simple = 100*((1/(1-rate*(float(days)/365))-1))*365/days
    return simple

def convert_simple_to_cont(rate, days):

####################################################################
#
# This function takes two (2) arguments:
#
#   rate  - a discount rate
#   days - days in the period
#
# The function converts from a simpe rate to a continuous rate 
#
####################################################################

    cont = log(1+(rate * float(days)/365 + 1)**(365/float(days)) - 1)
    return cont

