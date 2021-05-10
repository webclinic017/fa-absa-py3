import acm
import math

ael_variables = [

['almostzerolessthan', 'Almost zero less than', 'double', None, 1.0e-07, 1, 0, 'Value is regarded as zero if its absolute value is less than this value.', None, True],

]

'''Filter calibration equations with zero or close to zero market price, if not already filtered..
   For a surface with no explict nor implicit instrument,
   the equation will not be filtered.'''
   
def ael_main_ex( parameters, dictExtra ):

    #Unpack Filter parameters
    almostZeroLessThan = parameters['almostzerolessthan']
    
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    
    #Unpack extra provided data for filter functions
    calibrationRowObjects = dict.At('calibrationRowObjects')
    calibrationCostFunctionsResult = dict.At('calibrationCostFunctionsResult')
    
    calibrationCostFunctionsResultDict = calibrationCostFunctionsResult.Results()

    for calibrationRowObject in calibrationRowObjects:

        calibrationCostFunctionResult = calibrationCostFunctionsResultDict.At(calibrationRowObject.Id())

        if not calibrationCostFunctionResult.Filtered() and calibrationRowObject.Instrument() and acm.Math.AlmostZero(calibrationRowObject.MarketPrice().Value().Number(), almostZeroLessThan):
        
            calibrationCostFunctionResult.FilterReason("Market price is considered zero")
    
    return [calibrationCostFunctionsResult]
    
