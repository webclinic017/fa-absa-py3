
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSliceExtrapolation - Ajdust nbr of slices from optimization if total quantity > expected traded qty.
    
    (c) Copyright 2014 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    
    This module contains a simple slice calculation, example:
    
    SalesOrderQty        = 30k  (ppTAQty)
    AverageDailyVolume   = 25k  (measured between algos startTime and stopTime)
    Participation        = 10%
    
    EstimatedQtyToTrade  = 25k * 10% = 2500  (adjPeriodQty)
    EstimatedSlices      = 5    (optimized using EstimatedQtyToTrade before getSlices() is called)
    
    This implies a slizeSize of 2500 / 5 = 500 (stocks per slice).
    getSlices() simply divides totalQty with sliceSize and returns => 30k / 500 =  60 slices
    

-------------------------------------------------------------------------------------------------------"""
import acm
import math
import string


def Print2Trace(agent, message):
    if agent.IsTraceEnabled() and agent.Log():
        agent.Log().AddStringRecord(message)
    else:
        pass
        
        
def getSlices(agent):
    ppTA         = agent.BaseOrder().PrePostTradeAnalysis()
    ppTAQty      = 0.0
    slices       = agent.EstimatedSlices()
    adjPeriodQty = agent.PeriodVolumeAdjustedForParticipation()
    
    
    
    if ppTA:
        #  The total quantity entered on the sales order (minus any reserved qty)
        ppTAQty = ppTA.Quantity()
        

    if  (ppTAQty > adjPeriodQty) and (adjPeriodQty > 0.0):
        # The slices are estimated from the likely volume to trade.
        # If the total quanity is more than we will likely trade today
        # then the slices should be more to match the total quantity.
        if slices > 0.0 :
            sliceSize = adjPeriodQty / slices
            slices    = ppTAQty / sliceSize
            Print2Trace(agent, 'SlicesSize : ' + str(sliceSize) )
    else:
        Print2Trace(agent, 'No slice extrapolation needed' )        
        
    Print2Trace(agent, 'PeriodVolumeAdjustedForParticipation: ' + str(adjPeriodQty) )
    Print2Trace(agent, 'PrePostTradeAnalysisQuantity: ' + str(ppTAQty) )
 
    return slices
        

