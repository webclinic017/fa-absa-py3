

"""----------------------------------------------------------------------------
MODULE
    BondOptParams - Option parameters
    
    (c) Copyright 2000 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Extracts common option parameters for a given instrument
    
NOTE        
    Concerning the new naming conventions:
    call_option has been replaced by put_call, since _option is redundant
    and the order put, call makes it easier to associate to the numeric
    representations put=0, call=1.
    
    Backwards compatability:
    OptionParams will detect the use of attributes from AdvancedParams and
    VanillaParams, it will print a message suggesting a name change and then
    return the correct value. So the simplest way to port old code is to use
    FoptionParams and read the warnings in the Console.

DATA-PREP   

EXTERNAL DEPENDENCIES

REFERENCES  
----------------------------------------------------------------------------"""
import ael
import sys
import math

"""----------------------------------------------------------------------------
CLASS           
    FOptionParams - Parameters for vanilla options

INHERITS
    
DESCRIPTION     
    The class extracts all parameters needed to value an ordinary option.

CONSTRUCTION    
    i               Instrument      An instrument that is a vanilla option

MEMBERS         
    valuation_date  date            The valuation date. Information when shifting time.
    price           Float           Price of underlying stock
    texp            Float           Time to expiry (in years)           
    vol             Float           Volatility of stock price
    rate            Float           Risk-free interest rate
    carry_cost      Float           Cost of carry rate
    strike          Float           Strike price
    put_call        Int 0|1         1=call option, 0=put option
    eur_ame Int     0|1             0=European option, 1=American option
    dividends       List            List of dividends, pairs[value,date]
    df              Float           Unknown ?? Probably needs a longer name

----------------------------------------------------------------------------"""
class BondOptParams:
    def __init__(self, ins):
        "Class to extract common option parameters"

        # Contract parameters
    	self.valday = ael.date_today()
    	self.t = self.valday.years_between(ins.exp_day, 'Act/365')
    	if ins.exercise_type == 'American':
	    self.american = 1
    	else:
	    self.american = 0
	self.call = ins.call_option
	self.strike = ins.strike_price
	valday_offset = self.valday.add_banking_day(ins.curr, ins.pay_day_offset)
	expday_offset = ins.exp_day.add_banking_day(ins.curr, ins.pay_day_offset)

	# Valuation parameters 
	self.spot_yield = ins.used_und_price()    
	self.frw_yield = ins.used_und_frw_price()
	self.spot_price = ins.und_insaddr.clean_from_yield(valday_offset, 'RSA', '', self.spot_yield)
	self.frw_price = ins.und_insaddr.clean_from_yield(expday_offset, 'RSA', '', self.frw_yield)
	self.vol = ins.used_vol()/100
	self.cc = math.log(self.frw_price/self.spot_price) / self.t    
	yc = ins.used_yield_curve(ins.curr) 
	self.r = yc.yc_rate(self.valday, ins.exp_day, 'Continuous', 'Act/365', 'Spot Rate')
	self.ycc = math.log(self.frw_yield / self.spot_yield) / self.t
