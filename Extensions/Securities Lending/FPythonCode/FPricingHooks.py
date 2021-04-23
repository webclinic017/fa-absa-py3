""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FPricingHooks.py"
from __future__ import print_function
"""-------------------------------------------------------------------------------------------
MODULE
    FPricingHooks

    (c) Copyright 2017 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Python Hooks for Pricing Parameters of the Securities Lending solution. 
-------------------------------------------------------------------------------------------"""

''' ************** Column hooks ************** '''
import acm, ael
import FSecLendUtils

# Column: Collateral Cost (Sourcing)
# Usage: Return sourcing cost for a given collateral
# Sheet: PortfolioSheet, TradeSheet
def GetCollateralSourcingCost(object):
    return None

# Column: Collateral Cost (Lending) 
# Usage: Return lending cost for a given collateral
# Sheet: TradeSheet
def GetCollateralReplicationCost(object): 
    return None

# Column: Counterparty Risk Cost
# Usage: Return counterparty risk cost
# Sheet: PortfolioSheet, TradeSheet
def GetCptyCost(object):
    return None

# Column: Margin Bps
# Usage: Return the fixed  margin points added to every order 
# Sheet: TradeSheet
def GetMargin(object):
    client = object.Trade().Counterparty()
    return None

# Column "Additional Cost" handled by Hierarchy Editor & extension attribute secLendAddlCost*

''' ************** Helpers ************** '''

#Used in pricing columns (sourcing) for getting a default price for the returned party 
def GetDefaultSourcingCpty(object):
    return acm.FParty['Markit']

# Columns: 
#  - Edit Bid Rate: stored in Price table + affects calculations of Active Rate/Sourcing Fee
#  - Edit Ask Rate: stored in Price table
#  - Edit Bid Volume: stored in Price table
#  - Edit Ask Volume: stored in Price table
# Usage: Only used for the generic Security Loan or grouped Underlying
# Sheet: PortfolioSheet
def OverrideRate(row, col, calcval, val, operation):
    def Unsimulate(calcval):
        evaluator = calcval.GetEvaluator() if calcval else None
        if evaluator:
            evaluator.RemoveSimulation()

    if str(operation) == 'remove':
        val = None
        #Setting the price rec to None will reset to default functionality
    if row.IsKindOf(acm.FPortfolioInstrumentAndTrades):
        return 

    rowIns = row.SingleInstrumentOrSingleTrade()
    if rowIns and rowIns.IsKindOf(acm.FSecurityLoan):
        rowIns = rowIns.Underlying()
    ins = FSecLendUtils.GetMasterSecurityLoan(rowIns)

    #Remove simulation and return for some special cases when nothing is stored
    if not ins or not FSecLendUtils.IsMasterSecLoan(ins):
        Unsimulate(calcval)
        return

    #Save a Price with the input on the Master SL for the underlying stockOrBond 
    date = ael.date_today()
    market = acm.FMarketPlace['Rate Override']
    c = "insaddr=%d and curr=%d and ptynbr=%d" % \
        (ins.Oid(), ins.Currency().Oid(), market.Oid())
    aelprice = ael.Price.read(c)
    if aelprice:
        price = aelprice.clone()
    else:
        price = ael.Price.new()
    if 'Ask Rate' in col.ColumnId():
        price.ask = val
    elif 'Bid Rate' in col.ColumnId():
        price.bid = val
    elif 'Ask Volume' in col.ColumnId():
        price.high = val
    elif 'Bid Volume' in col.ColumnId():
        price.low = val
        
    price.insaddr = ins.Oid()
    price.curr = ins.Currency().Oid()
    price.ptynbr = market.Oid()
    price.day = date
    price.commit()
    print('Saved ADS price %s for %s with date %s (market, "%s")' % \
        (val, ins.Name(), date, market.Name()))
    Unsimulate(calcval)

def GetLatestPrice(ins, priceDate, marketName):
    price = None
    if ins:
        date = acm.Time.DateToday()
        currency = ins.Currency()
        price = acm.FPrice.Select01("day <='%s' and instrument = '%s' and market ='%s' and currency = '%s'"%(date, ins.Name(), marketName, currency.Name()), None)
    return price
	