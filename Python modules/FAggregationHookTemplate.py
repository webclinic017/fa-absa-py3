""" AggregationArchiving:2.0.1 """

"""----------------------------------------------------------------------------
MODULE
        faggregation_hooks_template - aggregation hook functions

	(c) Copyright 2002 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
        
        This module contains a number of AEL hook functions, which, if defined,
        is called during aggregation.
        
NOTE		
	To use any hook function this module should be renamed to 
	FAggregationHooks.
        
ENDDESCRIPTION
----------------------------------------------------------------------------"""
import ael




"""----------------------------------------------------------------------------
FUNCTION
    trade_status_to_aggregate - Used to redefine which trades statuses to aggregate

DESCRIPTION
    Default is to aggregate trades with all trade statuses except Simulated,
    Reserved, Void and FO Confirmed. This can be overridden in this AEL hook
    function.
    The function gets the status as a string and should return one of the strings
    "Aggregate", "Archive" or "None".
----------------------------------------------------------------------------"""
def trade_status_to_aggregate_template(status):
    if status != "Void":
    	return "Aggregate"
    else:
    	return "Archive"


"""----------------------------------------------------------------------------
FUNCTION
    aggregated_price_template
    aggregated_quantity_template
    aggregated_premium_template
    aggregated_pl_template
    aggregated_funding_template
    aggregated_dividend_template
    aggregated_fees_template
    aggregated_settled_template
    aggregated_accrued_template
DESCRIPTION
    The functions can be used to override the calculations during aggregation.
----------------------------------------------------------------------------"""
def aggregated_price_template(trades, agg_trade):
    price = 100.0
    return price

def aggregated_quantity_template(trades, agg_trade):
    quantity = 100.0
    return quantity

def aggregated_premium_template(trades, agg_trade):
    premium = 100.0
    return premium

def aggregated_pl_template(trades, agg_trade):
    pl = 100.0
    return pl

def aggregated_funding_template(trades, agg_trade):
    funding = 100.0
    return funding

def aggregated_dividend_template(trades, agg_trade):
    dividend = 100.0
    return dividend

def aggregated_dividend_funding_template(trades, agg_trade):
    dividend_funding = 100.0
    return dividend_funding

def aggregated_fees_template(trades, agg_trade):
    fees = 100.0
    return fees

def aggregated_settled_template(trades, agg_trade):
    settled = 100.0
    return settled

def aggregated_accrued_template(trades, agg_trade):
    accrued = 100.0
    return accrued


