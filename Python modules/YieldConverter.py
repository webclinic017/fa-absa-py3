
import ael, math



####################################################################

"""
 The yield_converter function has been designed to be used with a 
 query and hence the first argument, an object, is not used.

 The other argments are:
   
   inconvention - the  cpn frequency of the 'in' yield
   ylddisc - whether the rate is yield or discount
   rate - the rate to be converted
   outconvention - the output rate convention (NACM, NACA etc)

   Created by Panos Prodromou August 2003
   
   2005-07 Updated with function convert_cont_to_simple. This function
           converts from a continuous rate to a simple rate.
"""
####################################################################

def yield_converter(r,inconvention,ylddisc,days,rate,outconvention,*rest):

# Convert in convention from an integer to named convention

        #print inconvention,ylddisc,days,rate,outconvention
        
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
	elif outconvention == 'NACu':
	    outNA = days    
	else:
	    inNA = 'NACC'
	 
# If yield is the type 

    	if ylddisc == 'Yield':
	    inconvention=float(inconvention)
    	    rate=float(rate)/100
    	    #print 'line 66', inNA,inconvention,rate
    	    Rcont = convert_to_cont(inNA, inconvention, rate)
    	    #print 'Rcont is', Rcont
    	    if outconvention == 'NACu':
                Rperiod = convert_cont_to_simple(Rcont, days)
            else:
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
	    rate=float(rate)/100
	    Rcont = convert_simple_to_cont(rate, days)
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
        #print incon, rate
	Rcont = incon*math.log(1+rate/incon)
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
  
    #print 'line 126' , outNA,Rcont
    Rperiod = outNA*(math.exp(Rcont/outNA)-1)
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

def convert_cont_to_simple(rate, days):

####################################################################
#
# This function takes two (2) arguments:
#
#   rate  - a discount rate
#   days - days in the period
#
# The function converts from a continuous rate to a simple rate 
#
####################################################################

    #print 'cts', rate, days
    simp = (math.exp(rate*float(days)/365.0) -1) * 365.0/float(days)
    return simp



####################################################################
#
# This function calls yield_converter but returns 
# all results in the same format.
#
#
####################################################################

def yield_converter_rate(r,inconvention,ylddisc,days,rate,outconvention,*rest):

    y = yield_converter(r, inconvention, ylddisc, days, rate, outconvention)
    if y < 1:
        return y * 100
    else:
        return y
