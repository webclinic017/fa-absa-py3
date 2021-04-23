import acm
import math
from itertools import groupby

ael_variables = []

''''''

def FindAtmIndex(calibrationRowObjects):        

    index = 0
    
    currentUnderlyingPrice = calibrationRowObjects[0].Calculation("Portfolio Underlying Forward Price").Value().Number()

    for calibrationRowObject in calibrationRowObjects:
        if currentUnderlyingPrice <= calibrationRowObject.Instrument().StrikePrice():
            break
        index = index + 1
        
    return index
    
def FilterImpl(calibrationRowObjects, calibrationCostFunctionsResultDict, startIndex, stopIndex, step, greaterThan):

    currentCmpPrice = None

    for i in range(startIndex, stopIndex, step):
        calibrationRowObject = calibrationRowObjects[i]
        calibrationCostFunctionResult = calibrationCostFunctionsResultDict.At(calibrationRowObject.Id())
        
        if not calibrationCostFunctionResult.Filtered():
            currentPrice = calibrationRowObject.MarketPrice().Value().Number()
            if not currentCmpPrice:
                currentCmpPrice = currentPrice
            else:
                if (greaterThan and currentPrice >= currentCmpPrice):
                    calibrationCostFunctionResult.FilterReason("Market Price Arbitrage " + "{0:.2f}".format(currentPrice) + ">=" + "{0:.2f}".format(currentCmpPrice))
                elif (not greaterThan and currentPrice <= currentCmpPrice):
                    calibrationCostFunctionResult.FilterReason("Market Price Arbitrage " + "{0:.2f}".format(currentPrice) + "<=" + "{0:.2f}".format(currentCmpPrice))
                else:
                    currentCmpPrice = currentPrice
    
def Filter(calibrationRowObjects, calibrationCostFunctionsResultDict, isCall):

    if len(calibrationRowObjects) > 0:

        atmIndex = FindAtmIndex(calibrationRowObjects)
        FilterImpl(calibrationRowObjects, calibrationCostFunctionsResultDict, atmIndex, len(calibrationRowObjects), 1, isCall) 
        FilterImpl(calibrationRowObjects, calibrationCostFunctionsResultDict, atmIndex, -1, -1, not isCall)
    
def ael_main_ex( parameters, dictExtra ):

    #Unpack extra provided data for filter functions
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()

    calibrationRowObjects = dict.At('calibrationRowObjects')
    calibrationCostFunctionsResult = dict.At('calibrationCostFunctionsResult')
    calibrationCostFunctionsResultDict = calibrationCostFunctionsResult.Results()
    calibrationRowObjects.SortByProperty("Instrument.IsCall, Instrument.StrikePrice")
    
    # Requires more than one equation
    # Silently approve when only on equation
    
    if calibrationRowObjects.Size() > 1:
        
        sortFunc = lambda x: x.Instrument().ActualExpiryCoordinate()
        
        for _, group in groupby(sorted(calibrationRowObjects, key=sortFunc), key=sortFunc):
                
            calibrationRowObjectsList = list(group)
            
            calls = [x for x in calibrationRowObjectsList if x.Instrument().IsCall()]
            puts = [x for x in calibrationRowObjectsList if (not x.Instrument().IsCall())]
        
            Filter(calls, calibrationCostFunctionsResultDict, True)
            Filter(puts, calibrationCostFunctionsResultDict, False)
            
    return [calibrationCostFunctionsResult]
