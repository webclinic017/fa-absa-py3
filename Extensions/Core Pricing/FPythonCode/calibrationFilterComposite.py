import acm
import FUxUtils

'''Filter calibration composite, executes the stored filters in stored order.
   Note! If a stored filter is a composite, it will execute all its members in order,
   before executing the next filter. '''

def UnpackStoredCalibrationParametersByName(storedCalibrationParametersByName):

    result = acm.FArray()
    allStoredCalibrationParameterByName = acm.CalibrationParameters().AllAsDictionary("filterfunctions")
    
    for storedCalibrationParameterByName in storedCalibrationParametersByName:
    
        storedCalibrationParameter = allStoredCalibrationParameterByName.At(storedCalibrationParameterByName)
        
        if storedCalibrationParameter:
            
            result.Add(storedCalibrationParameter)
            
        else:
        
            raise Exception('No StoredCalibrationParameter with name ' + storedCalibrationParameterByName + ' found.' )
            
    return result
    
def PackStoredCalibrationParametersByName(storedCalibrationParameters):

    result = acm.FArray()
    
    for storedCalibrationParameter in storedCalibrationParameters:
    
        result.Add(storedCalibrationParameter.Name())
        
    return result

def ael_custom_dialog_show(shell, params):

    editParameters = None
    initData = FUxUtils.UnpackInitialData(params)
    
    if initData:
        editParametersAsStrings = initData.At('filters')
        editParameters = UnpackStoredCalibrationParametersByName(editParametersAsStrings)
    else:
        editParameters = acm.FArray()
        
    acm.UX().Dialogs().SelectSubset(shell, acm.CalibrationParameters().All("filterfunctions"), "Select Filters", True, editParameters)
    
    resultDict = acm.FDictionary()
    resultDict.AtPut('filters', PackStoredCalibrationParametersByName(editParameters))
    
    return resultDict
  
def ael_custom_dialog_main( parameters, dictExtra ):
    
    #Unpack Filter parameters
    storedFiltersByNames = parameters['filters']
    storedFilters = UnpackStoredCalibrationParametersByName(storedFiltersByNames)
    
    #Unpack extra provided data for filter functions
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    calibrationRowObjects = dict.At('calibrationRowObjects')
    calibrationCostFunctionsResult = dict.At('calibrationCostFunctionsResult')

    #Call the stored filters in stored order
    for storedFilter in storedFilters:
    
        storedFilter.Execute(dict)
        
    return [calibrationCostFunctionsResult]
    
