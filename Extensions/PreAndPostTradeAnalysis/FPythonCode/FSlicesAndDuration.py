

"""-------------------------------------------------------------------------------------------------------
MODULE
    FSlicesAndDuration - Find optimal slices and duration
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    
    This module contains a simple grid solver used for optimizing the 
    number of slices and duration of an Algo Execution agent.

-------------------------------------------------------------------------------------------------------"""
import acm
import math
import string
import FSlicesAndDurationTestValues

debug = False

doubleConv =  acm.GetFunction('double', 1)

def Print2Trace(agent, message):
    if agent.IsTraceEnabled() and agent.Log():
        agent.Log().AddStringRecord(message)
    else:
        pass

def doOptimizeDuration(agent):
    if agent.IsKindOf('ExecutionAlgoArrivalPrice') or agent.IsKindOf('ExecutionAlgoMarketOnClose'):
        return True
    return False
    
def setDuration(agent, duration):
    try:
        if agent.IsKindOf('ExecutionAlgoArrivalPrice'):
            agent.StopTime(doubleConv(agent.StartTime()) + (duration / 24.0))
        elif agent.IsKindOf('ExecutionAlgoMarketOnClose'):
            agent.StartTime(doubleConv(agent.StopTime()) - (duration / 24.0))
    except Exception as e:
        if debug:
            print (str(e))
        raise e


def optimizeSlices(agent):
    minCost = 1e99
    bestSlices = 0
    minSlices = agent.SlicesMin()
    maxSlices = agent.SlicesMax()
    
    # At this point we should already have checked that goal volume is a multiple of round lot.
    roundLot = agent.TradingInterface().RoundLot()
    maxSlices = min(maxSlices, agent.GoalVolume() / roundLot)
    
    if (not acm.Math.IsFinite(minSlices)) :
        raise Exception('Min slices not finite: ' + str(minSlices))
    elif (not acm.Math.IsFinite(maxSlices)):
        raise Exception('Max slices not finite: ' + str(maxSlices))
            
    
    xArray = FSlicesAndDurationTestValues.getSlicesTestValues(minSlices, maxSlices)
    results = None   

        
    for x in xArray:
        agent.EstimatedSlices(x)
        f = agent.EstimatedTotalCost()
        Print2Trace(agent, 'EstimatedTotalCost: ' + str(f))
        
        if acm.Math.IsFinite(f):
            if f < minCost:
                minCost = f
                bestSlices = x
                if results:
                    results.append(f)
                    
    return bestSlices, minCost


def optimizeSlicesAndDuration(agent):
    
    yArray = FSlicesAndDurationTestValues.getDurationTestValues(agent.DurationMin(), agent.DurationMax())
            
    minCost = 1e99
    bestSlices = 0
    bestDuration = 0
            
    for y in yArray:
        if y > 0:
            setDuration(agent, y)
                
            x, f = optimizeSlices(agent)
            if f < minCost:
                minCost = f
                bestSlices = x
                bestDuration = y
                            
    return bestSlices, bestDuration
    
 
def optimize(agent):
    success = False
    if doOptimizeDuration(agent):
        x, y = optimizeSlicesAndDuration(agent)
        if x > 0:
            agent.EstimatedSlices(x)
            setDuration(agent, y)
            success = True
    else:
        x, f = optimizeSlices(agent)
        if x > 0:
            agent.EstimatedSlices(x)
            success = True
    if not success:
        raise Exception('Number of slices not found')
