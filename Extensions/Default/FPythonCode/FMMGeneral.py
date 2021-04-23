from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FMMGeneral- Market Making specific.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.
 ---------------------------------------------------------------------------"""
import acm


""" Reset Hit Actions
"""
def resetHitAction(row, val, type):
    if val == 0 or val == False:
        #print (type)
        try:
            qc = row.QuoteController()
            if qc:
            
                qc.UI().Invoke(type)
                
            else:
                print ('QuoteController not found!')
        except:
            print ('Failed to invoke', type)
            

def resetHitActionMaxHits(row, col, cell, val, operation):
    resetHitAction(row, val, "ResetHitActionMaxHits")

def resetHitActionUnderlyingMaxHits(row, col, cell, val, operation):
    resetHitAction(row, val, "ResetHitActionUnderlyingMaxHits")
   
def resetHitActionExpiryMaxHits(row, col, cell, val, operation):
    resetHitAction(row, val, "ResetHitActionExpiryMaxHits")
            
def resetHitActionExpiryFullImbalance(row, col, cell, val, operation):
    resetHitAction(row, val, "ResetHitActionExpiryFullImbalance")
            
def resetHitActionFullImbalance(row, col, cell, val, operation):
    resetHitAction(row, val, "ResetHitActionFullImbalance")
            
def resetHitActionUnderlyingFullImbalance(row, col, cell, val, operation):
    resetHitAction(row, val, "ResetHitActionUnderlyingFullImbalance")
    

""" Reset Quote Offset 
"""
def resetReactOnHitOffset(row, col, cell, val, operation):
    trading = row.TradingInterface()
    if val != 0 or val != False:
        try:
            hitAction = acm.MarketMaking.GetHitActionQuoteOffset(trading)
            if hitAction:
                hitAction.ResetOffset()    
        except:
            print ('React On Hit Offset could not be reset!')

def saveQuoteValue(row, col, cell, valString, operation, entity):
    if str(operation) == 'remove':
        return
    trading = row.TradingInterface()
    ctx = col.Context()
    acm.SetDefaultValue(trading, entity, ctx, 'FOrderBook', valString)
    cell.Unsimulate()

def postPriceCheckMarketQuote(row, col, cell, val, operation):
    if val == 1:
        valString= 'true'
    else:
        valString= 'false'
    saveQuoteValue(row, col, cell, valString, operation, "qDefPriceCheckMarket")

def postPriceCheckMarketOwnOrder(row, col, cell, val, operation):
    if val == 1:
        valString= 'true'
    else:
        valString= 'false'
    saveQuoteValue(row, col, cell, valString, operation, "ownOrderPriceCheckMarket")
                           
def wantButton(invokationInfo):
    cell = invokationInfo.Parameter("Cell")
    if cell:
        rowObject = cell.RowObject()
        if rowObject and rowObject.IsKindOf('FQuoteLevelRow'):
            if rowObject.OrderDepth() < 0:
                return True
    return False
    
def wantDerivativeButton(invokationInfo):
    cell = invokationInfo.Parameter("Cell")
    if cell:
        rowObject = cell.RowObject()
        if rowObject and rowObject.IsKindOf('FQuoteLevelRow'):
            if rowObject.Instrument().IsKindOf('FDerivative') and rowObject.OrderDepth() < 0:
                return True
    return False
