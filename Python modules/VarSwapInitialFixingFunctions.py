'''
Date                    : 2010-02-04
Purpose                 : Checks for initial fixing in varswap, if found, removes the initial exotic event from list, and returns the eventlist for further processing
Department and Desk     : EQ DERV
Requester               : Andrey Chechin
Developer               : Rohan van der Walt
CR Number               : 212697
'''

'''
Date                    : 2010-03-18, 2011-02-07
Purpose                 : Allows fixings on first and last variance prices, and added "PCG Mkt MO" user group to permissions to make fixings.
                          Expanded to include manual fixings on Cliquet
Department and Desk     : PCG Mkt MO
Requester               : Marko Milutinovic, Andrey Chechin
Developer               : Rohan van der Walt, Zaakirah Kajee
CR Number               : 257897, 544578
'''

from FSEQDataMaint import ExoticEventMtMPrice
groupsAllowed = ['FO Eq Derv Trader', 'PCG Mkt MO']

def getEarliestEvent(exoticEvents):
    '''
    Does one pass of the array to find the earliest ExoticEvent.Date, and then returns the ExoticEvent
    Used in checkPriceFixingForVarianceSwapInstrument
    Input:List of FExoticEvent
    Output:FExoticEvent with earliest Date
    '''
    minimum = exoticEvents[0]
    for e in exoticEvents:
        if e.Date() < minimum.Date():
            minimum = e
    return minimum
  
def checkPriceFixingForVarianceSwapInstrument(exoticEvents):
    '''
    Check if the earliest Event has a different value to MtM...then assume fixed pricing, if set by users in defined user groups

    Under fixed pricing:
        The earliest event will just be removed from the eventlist, and normal processing on the rest of the events will continue
        To work the Trader/User that does the fixing must be in one of the usergroups defined in variable: groupsAllowed
    ATT:    If the MtM changes for some reason on the initial date of the variance swap this proc should handle it correctly by checking the update user property.

    Input: 	exoticEvents - list of FExoticEvent only of type "Variance Price", filtered in FSEQDataMaint(FPythonCode) and passed to this module for further filtering.
    Output: 	exoticEvents - list with or without initial variance price event, depends if fixing was found
    '''
    try:
        
        e = getEarliestEvent(exoticEvents)
        varSwap = e.Instrument()
        mtMPrice = ExoticEventMtMPrice(varSwap, e)
        setByAllowed = e.UpdateUser().UserGroup().Name() in groupsAllowed
        if e.EventValue() >= 0.0 and e.EventValue() != mtMPrice and setByAllowed:
            print 'Variance Swap:', varSwap.Name(), 'has initial fixing' 
            exoticEvents.remove(e)
            return exoticEvents
        else:
            return exoticEvents
    except Exception, e:
        return exoticEvents
        
def FixingForCliquetInstrument(exoticEvents):
    try:
        
        e = getEarliestEvent(exoticEvents)
        cliquet = e.Instrument()
        mtMPrice = ExoticEventMtMPrice(cliquet, e)
        setByAllowed = e.UpdateUser().UserGroup().Name() in groupsAllowed
        if e.EventValue() >= 0.0 and e.EventValue() != mtMPrice and setByAllowed:
            print 'Cliquet:', cliquet.Name(), 'has initial fixing' 
            exoticEvents.remove(e)
    except Exception, e:
        print 'Cliquet Fixing error'
    finally:
        return exoticEvents

