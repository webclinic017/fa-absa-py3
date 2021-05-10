import acm

"""----------------------------------------------------------------------------

MODULE

    Portfolio Yield Hedger: Template for implementing custom 
    interest rate yield delta hedging agents
    
    (C) Copyright 2015 Front Capital Systems AB. All rights reserved.

DESCRIPTION


NOTES:
    
         
------------------------------------------------------------------------------"""


HEDGE_INSTRUMENT_IRD = acm.FSymbol['YPortfolioYieldHedgerHedgeIRD']
ZERO_QTY_EPSILON = 1e-10

def calculateHedgeQuantity(params, orderPositions, monitoredValue, targetValue, hedgeInstr):

    orderPosInHedge = orderPositions.PositionIn(hedgeInstr)
            
    hedgerAttrib = params.GetParameter(HEDGE_INSTRUMENT_IRD)
            
    hedgerIRD = hedgerAttrib.Value().Number() * hedgeInstr.ContractSize()
            
    if acm.Math.AlmostZero(hedgerIRD, ZERO_QTY_EPSILON):
        raise Exception("Hedge instrument interest rate yield delta is almost 0 : " + str(hedgerIRD))
    
    qtyToHedge = (monitoredValue - targetValue) / hedgerIRD
            
    hedgeIsBuy = True

    if ((targetValue - monitoredValue) < 0):
        if hedgerIRD > 0:
            hedgeIsBuy = False
    else:
        if hedgerIRD < 0:
            hedgeIsBuy = False
            
    if hedgeIsBuy:
        qtyToHedge = abs(qtyToHedge)
    else:
        qtyToHedge = -abs(qtyToHedge)
               
    qtyToHedge = qtyToHedge - orderPosInHedge        
    
            
    return qtyToHedge
        
   
def getInstructions(params, orderPositions, monitoredValue, lowerLimit, upperLimit):

    if monitoredValue < lowerLimit or monitoredValue > upperLimit:
                
        targetValue = lowerLimit + ((upperLimit - lowerLimit) / 2)
        
        hedgeInstr = params.HedgeInstruments().First()           
        qtyToHedge = calculateHedgeQuantity(params, orderPositions, monitoredValue, targetValue, hedgeInstr)
                
        if abs(qtyToHedge) >= 1:        
                        
            instructions = acm.FTradingInstructions()                                        
            instructions.SetQuantity(hedgeInstr, qtyToHedge)            
            return instructions            
    
    return None

def hasInstructions(params, orderPositions, monitoredValue, lowerLimit, upperLimit):
    
    if lowerLimit > upperLimit:
        raise Exception('Lower limit greater than Upper Limit')        
    
    targetValue = lowerLimit + ((upperLimit - lowerLimit) / 2)
    
    hedgeInstr = params.HedgeInstruments().First()   
    
    qtyToHedge = calculateHedgeQuantity(params, orderPositions, monitoredValue, targetValue, hedgeInstr)
                
    if (monitoredValue < lowerLimit or monitoredValue > upperLimit) and (abs(qtyToHedge) >= 1) :                        
        return True
    else:        
        return False
            
    
