

"""----------------------------------------------------------------------------
Python script

        FPDE.py - Script for time-step selection in the equity PDE solver
        
        Updated: 2011-01-27
        Added: barrier_monitoring_type,
               barrier_discrete_monitoring_dates,
               barrier_window_monitoring_dates,
               PDEsteps
        
DESCRIPTION
        This module computes the scale factor that multiplies the 
        the base number of time-steps modified in the GUI under 
        model settings in the Administration console.

ENDDESCRIPTION
----------------------------------------------------------------------------"""

def finDiffSteps(isAmerican, isCall, isUpperBarrier, isLowerBarrier, propDivs, barrier_monitoring_type, barrier_discrete_monitoring_dates, barrier_window_monitoring_dates, PDEBaseTimeSteps):
   
    DiscreteBarrier    = 2.0
    WindowBarrier      = 2.0
    ContinuousBarrier  = 1.0
    
    UpperBarrier       = 1.0
    LowerBarrier       = 1.0
    DoubleBarrier      = 1.0
    
    AmericanCall       = 1.0
    AmericanPut        = 1.0

    PropDivs           = 1.0
    

    outFactor = 1.0

    if (barrier_monitoring_type == "Discrete"):
        outFactor = DiscreteBarrier*outFactor
    elif (barrier_monitoring_type == "Window"):
        outFactor = WindowBarrier*outFactor
    elif (barrier_monitoring_type == "Continuous"):
        outFactor = ContinuousBarrier*outFactor

    if (isUpperBarrier and not(isLowerBarrier)):                
        outFactor = UpperBarrier*outFactor
    elif (isLowerBarrier and not(isUpperBarrier)):              
        outFactor = LowerBarrier*outFactor
    elif (isLowerBarrier and isUpperBarrier):
        outFactor = DoubleBarrier*outFactor
       
    if (isAmerican and isCall):         
        outFactor = AmericanCall*outFactor
    elif (isAmerican and (not isCall)): 
        outFactor = AmericanPut*outFactor

    if (propDivs):  
        outFactor = PropDivs*outFactor
    
    return outFactor

