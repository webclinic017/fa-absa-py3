""" MarkToMarket:1.1.10.hotfix1 """

"""----------------------------------------------------------------------------
MODULE
    FMtMCustomization - Module where customization can be done. Used in 
    FMtMExecute.

    (c) Copyright 2002 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    In this module customers can do their own customization for valuation of
    MtM-prices and rounding for example.
     
RENAME this module to FMtMCustomization.
----------------------------------------------------------------------------"""

"""----------------------------------------------------------------------------
FUNCTION
    custom_valuation() - This function allows customers to do their own 
    valuation of MtM-prices for certain instruments.
    
DESCRIPTION
    This function is an example how customers could do their own valuation of 
    certain instruments.
    
ARGUMENTS
    ins_list    Instrument  A list of instruments
----------------------------------------------------------------------------"""
import ael

def custom_valuation(ins_list):
    res = []
    for i in ins_list:
    	try:
    	    ins = ael.Instrument[i]
    	
	    custom_mtm_price = ins.mtm_price_suggest(ael.date_today(), ins.curr.insid, 1, 1)
    	
	    r = [ins, custom_mtm_price]
	    res.append(r)
	except:
	    pass
	
    return res


"""----------------------------------------------------------------------------
FUNCTION
    custom_rounding() - An example of a function where customers can add their 
    own rounding.
    
DESCRIPTION
    This function is an example how customers could use their own rounding. In
    this example the following rounding is used:
    
    Instype	Undinstype	Instrument OTC	Smallest Rounding 
    				Currency	price	
    
    Option	Stock		EUR, USD,  Yes	0,01	two decimal places
    				CHF, JPY		           
    Option	Stock		GBP	   Yes	0,001	three decimal places 
    Option	Equity Index	EUR, GBP   Yes	0,1	one decimal place
    Option	Equity Index	CHF	   Yes	0,1	If 0,1<=price<9,90, 
    							then round to one 
    							decimal place. 
    							If 9,90<=price<19,80, 
    							then round to the 
    							nearest multiple of 0,2 
    							If 19,80<=price<299,5, 
    							then round to the 
    							nearest mutliple of 0,5 
    							If price>=299,5, 
    							then round to the 
    							nearest integer number.
    Option	Equity Index	USD, JPY   Yes	0,01	two decimal places
    Warrant	Stock or	All	   No	0,001	three decimal places
    		Equity Index	
    Otherwise					0,001	three decimal places

    
ARGUMENTS
    ins    	Instrument  An instrument
    sugg_price	double	    A suggested price which should be rounded
    digits  	int 	    If > 0 then we will use rounding
    force_positive_mtm_price int Allow saving 0.01 as MtM price if price is 0.0

----------------------------------------------------------------------------"""
import ael

def custom_rounding(ins, sugg_price, digits, force_positive_mtm_price):
    if ins.instype == 'Option' and ins.otc:
    	if ins.und_insaddr.instype == 'Stock':
    	    if (ins.curr.insid == 'EUR' or ins.curr.insid == 'USD' or 
	    	ins.curr.insid == 'CHF' or ins.curr.insid == 'JPY'):
	    	if force_positive_mtm_price == 1:
		    if sugg_price <= 0.0:
		    	sugg_price = 0.01
	    	if digits > 0:
		    sugg_price = round(sugg_price, 2)
	    elif ins.curr.insid == 'GBP':
	    	if force_positive_mtm_price == 1:
		    if sugg_price <= 0.0:
		    	sugg_price = 0.001
	    	if digits > 0:
		    sugg_price = round(sugg_price, 3)
	    else:
    	    	if force_positive_mtm_price == 1:
	    	    if sugg_price <= 0.0:
		    	sugg_price = 0.001
	    	if digits > 0:
	    	    sugg_price = round(sugg_price, 3)
	
	elif ins.und_insaddr.instype == 'EquityIndex':
    	    if (ins.curr.insid == 'EUR' or ins.curr.insid == 'GBP'):
	    	if force_positive_mtm_price == 1:
		    if sugg_price <= 0.0:
		    	sugg_price = 0.1
	    	if digits > 0:
		    sugg_price = round(sugg_price, 1)
	    elif ins.curr.insid == 'CHF':
	    	if force_positive_mtm_price == 1:
		    if sugg_price <= 0.0:
		    	sugg_price = 0.1
	    	
		if digits > 0:
		    if sugg_price >= 0.1 and sugg_price < 9.90:
		    	sugg_price = round(sugg_price, 1)
		    
		    elif sugg_price >= 9.90 and sugg_price < 19.80:
		    	sugg_price = sugg_price * 10
			sugg_price = int(sugg_price)
			if(float(sugg_price)%2) != 0:
			    sugg_price = sugg_price + 1
			sugg_price = float(sugg_price)/10
			
		    elif sugg_price >= 19.80 and sugg_price < 299.5:
    	    	    	sugg_price_int = int(sugg_price)
			sugg_price_dec = sugg_price - sugg_price_int
			if sugg_price_dec >= 0 and sugg_price_dec < 0.25:
			    sugg_price_dec = 0.0
			elif sugg_price_dec >= 0.25 and sugg_price_dec < 0.75:
			    sugg_price_dec = 0.5
			else:
			    sugg_price_dec = 1.0     			    
		    	sugg_price = sugg_price_int + sugg_price_dec
		    
		    elif sugg_price >= 299.5:
		    	sugg_price = round(sugg_price)
	    
	    elif (ins.curr.insid == 'USD' or ins.curr.insid == 'JPY'):
	    	if force_positive_mtm_price == 1:
		    if sugg_price <= 0.0:
		    	sugg_price = 0.01
	    	if digits > 0:
		    sugg_price = round(sugg_price, 2)
	    else:
    	    	if force_positive_mtm_price == 1:
	    	    if sugg_price <= 0.0:
		    	sugg_price = 0.001
	    	if digits > 0:
	    	    sugg_price = round(sugg_price, 3)
	else:
    	    if force_positive_mtm_price == 1:
	        if sugg_price <= 0.0:
		    sugg_price = 0.001
	    if digits > 0:
	        sugg_price = round(sugg_price, 3)
    else:
    	if force_positive_mtm_price == 1:
	    if sugg_price <= 0.0:
		sugg_price = 0.001
	if digits > 0:
	    sugg_price = round(sugg_price, 3)
         
    return sugg_price

"""----------------------------------------------------------------------------
FUNCTION
    check_instrument() - This function allows customers to select a subset
    of instruments to store mtm-prices for.
    
DESCRIPTION
    The function takes an instrument entity as argument and returns 1 if an
    mtm price should be stored and 0 if not.

    The example implementation below will return 1 for instruments with
    the mtm_from_feed flag toggled and 0 otherwise.
    
ARGUMENTS
    ins    Instrument  An instrument entity
----------------------------------------------------------------------------"""
import ael

def check_instrument(ins):

    if not ins.mtm_from_feed:
        return 0
	
    return 1
