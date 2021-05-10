import acm
import math

ael_variables = []

'''Filter calibration equations with NaN market price, if not already filtered.
   For a surface with no explict nor implicit instrument,
   the equation will not be filtered.'''
   
def ael_main_ex( parameters, dictExtra ):

    #Unpack Filter parameters
    #No parameters used, hence nothing to unpack.

    #Unpack extra provided data for filter functions
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    calibrationRowObjects = dict.At('calibrationRowObjects')
    calibrationCostFunctionsResult = dict.At('calibrationCostFunctionsResult')
    
    calibrationCostFunctionsResultDict = calibrationCostFunctionsResult.Results()

    for calibrationRowObject in calibrationRowObjects:

        calibrationCostFunctionResult = calibrationCostFunctionsResultDict.At(calibrationRowObject.Id())

        if not calibrationCostFunctionResult.Filtered() and calibrationRowObject.Instrument() and not acm.Math.IsFinite(calibrationRowObject.MarketPrice().Value().Number()):
        
            calibrationCostFunctionResult.FilterReason("Market price is NaN or infinite")        
    
    return [calibrationCostFunctionsResult]
