""" MarkToMarket:1.1.10.hotfix1 """

"""----------------------------------------------------------------------------
MODULE
    FMtMTTGeneral - Module including all functions common to the Treasury 
                    Trader Mark to Market procedure.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module stores those functions which are common to run the Treasury 
    Trader Mark to Market procedure.

----------------------------------------------------------------------------"""

import sys
print 'Inside FMtMTTGeneral.'
try:
    import tt    
except ImportError:
    print 'The module tt was not found.'
    print
    
try:
    server = tt.ServerBase()
except:
    print 'Could not call tt.ServerBase()'
    print

"""----------------------------------------------------------------------------
FUNCTION
    get_spot_rate() - Function which retrieves the mid, bid or ask price for 
                      a currency pair in Treasury Trader.

DESCRIPTION
    The function selects all instruments which comes in from a certain Price
    Distributor.
    
ARGUMENTS
    curr1       String      Currency 1's instrument ID.
    curr2       String      Currency 2's instrument ID.
    bid_ask     Integer     0 for Mid price
                            -1 for Ask price
                            1 for Bid price
    
RETURNS
    Ask, Bid or Mid price of currency pair curr1/curr2.
----------------------------------------------------------------------------"""
# Returns the mid, bid or ask price for the curr1/curr2 currency pair.
# bid_ask = 0 for Mid
# bid_ask = -1 for Ask
# bid_ask = 1 for Bid
def get_spot_rate(curr1, curr2, bid_ask):
    result = 0.0
    if bid_ask == 0:
        result = mrp.GetSpotRateExt(curr1, curr2).GetMid()
    if bid_ask == -1:
        result = mrp.GetSpotRateExt(curr1, curr2).GetAsk()
    if bid_ask == 1:
        result = mrp.GetSpotRateExt(curr1, curr2).GetBid()
    return result
 
 
"""----------------------------------------------------------------------------
FUNCTION
    get_fxswap_price() - Function which retrieves the actual PL for an FxSwap
    in Treasury Trader and converts it to a price quoted in Pct of Nominal.
    
ARGUMENTS
    ins		Instrument Object            Fx Swap Instrument
    
RETURNS
    A price quoted in Pct of Nominal.
----------------------------------------------------------------------------"""
def get_fxswap_price(ins, fxSwapHasTwoLegs, report_curr):
    mtm_price = 0.0
    
    if ins.extern_id2[:2] == 'TT':
        trade_code = ins.extern_id2[2:]
        trade = tt.FXCashTrade_New()
        trade.SetKey(trade_code)
        if (trade.Read()): 
            pl_Actual = trade.GetFXFwdPLInCcy(report_curr, 0, fxSwapHasTwoLegs)
            exch = mrp.GetSpotRateExt(report_curr, ins.curr.insid).GetMid()
    
            if ins.quote_type == 'Pct of Nominal':
                mtm_price = pl_Actual / ins.nominal_amount() * 100 * exch
            else:
                mtm_price = 0.0
            
    return mtm_price


"""----------------------------------------------------------------------------
FUNCTION
    Miscellaneous functions.

DESCRIPTION
    In this section help functions are stored.
----------------------------------------------------------------------------"""
# Connects to Treasury Trader.
def connect(args, login, password, database, hostname):
    try:
        server.Open(args);
        server.Connect();
        server.Login(login, password, database, hostname);
    except RuntimeError, msg:
        print "Could not connect to Treasury Trader:", msg
        sys.exit (1)

def set_sys_param():
    global sysparam
    sysparam = server.GetSysParam()

def set_mrp():
    global mrp
    mrp = tt.MRP()
    mrp.Read(sysparam.GetRevalMRP())
    tt.GenPrice_SetMRP(mrp)

def set_price_setup():
    global priceSetup
    priceSetup = tt.PriceSetup()
    priceSetup.SetPLMode(tt.PriceSetup.kInception)
    priceSetup.SetFXOptFwdMethod(sysparam.GetRevalOptionMethod())
    tt.GenPrice_SetPriceSetup(priceSetup)


