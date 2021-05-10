import acm
import math

ael_variables = [

['intrinsicValueInPercent', 'Intrinsic Value in %', 'double', None, 50.0, 1, 0, 'Threshold value for the relation between the options intrinsic vs time value. Only out of the money options will be used if percentage value is set to zero', None, True]

]

'''Filter calibration equations where , if not already filtered.
   For a surface with no explict nor implicit instrument,
   the equation will not be filtered.'''
   
def ael_main_ex( parameters, dictExtra ):

    #Unpack Filter parameters
    #No parameters used, hence nothing to unpack.
    intrinsicValueInPercentBarrier = parameters['intrinsicValueInPercent']

    #Unpack extra provided data for filter functions
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    calibrationRowObjects = dict.At('calibrationRowObjects')
    calibrationCostFunctionsResult = dict.At('calibrationCostFunctionsResult')
    
    calibrationCostFunctionsResultDict = calibrationCostFunctionsResult.Results()

    for calibrationRowObject in calibrationRowObjects:
    
        calibrationCostFunctionResult = calibrationCostFunctionsResultDict.At(calibrationRowObject.Id())

        #Only possible to filter if calibrationRowObject has an instrument
        if not calibrationCostFunctionResult.Filtered() and calibrationRowObject.Instrument():
        
            intrinsicValuePercent = 100.0 * calibrationRowObject.Calculation("Intrinsic Option Market Value %").Value().Number()
            
            if intrinsicValuePercent >= intrinsicValueInPercentBarrier:

                calibrationCostFunctionResult.FilterReason("Intrinsic Value " + "{0:.2f}".format(intrinsicValuePercent) + "% >" + "{0:.2f}".format(intrinsicValueInPercentBarrier) + "%")        

    return [calibrationCostFunctionsResult]
