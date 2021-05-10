
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSlicesAndDurationTestValues - Slice and Duration test values
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    
    This module contains a methods used for generating test values
    to optimize the number of slices and duration of an Algo Execution agent.

-------------------------------------------------------------------------------------------------------"""

import math

durationMinuteInterval = 7.5

def sliceNumbers(n1, nn):
    a, b, c, d = 1.0, 1.0, 1.0, 1.0
    while d < n1:
        a, b, c, d = b, c, d, a + b

    result = []
    prev = None
    i = 0
    while (d <= nn) :
        if prev == None or prev != d:
            result.append(d)
            prev = d
        a, b, c, d = b, c, d, a + b


        
    return result
            
def getSlicesTestValues(xMin, xMax):

    xArray = sliceNumbers(xMin, xMax)
    if xMin != xMax:
        xArray.append(xMax)
        
    return xArray


def getDurationTestValues(yMin, yMax):

    yArray = [yMin]
    
    if yMin != yMax:
        durationHourInterval = durationMinuteInterval / 60.0
        duration = yMin + durationHourInterval
        
        while duration < yMax:
            yArray.append(duration)
            duration = duration + durationHourInterval
        
        yArray.append(yMax)
        
    return yArray
    
    
