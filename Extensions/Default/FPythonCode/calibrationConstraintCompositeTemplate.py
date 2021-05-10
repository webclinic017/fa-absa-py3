import acm
import FUxUtils

'''Constraint calibration composite, adds the stored constraints to the calibration problem.'''

def UnpackStoredCalibrationParametersByName(storedCalibrationParametersByName):

    result = acm.FArray()
    allStoredCalibrationParameterByName = acm.CalibrationParameters().AllAsDictionary("variablesconstraints")
    
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
        editParametersAsStrings = initData.At('constraints')
        editParameters = UnpackStoredCalibrationParametersByName(editParametersAsStrings)
    else:
        editParameters = acm.FArray()
        
    acm.UX().Dialogs().SelectSubset(shell, acm.CalibrationParameters().All("variablesconstraints"), "Select Constraints", True, editParameters)
    
    resultDict = acm.FDictionary()
    resultDict.AtPut('constraints', PackStoredCalibrationParametersByName(editParameters))
    
    return resultDict
  
def ael_custom_dialog_main( parameters, dictExtra ):
    
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()   
    calibrationConstraintsFunctions = dict.At('calibrationConstraintsFunctions')
    
    #Unpack Constraints parameters
    storedConstraintsByNames = parameters['constraints']
    storedConstraints = UnpackStoredCalibrationParametersByName(storedConstraintsByNames)
    
    #Unpack extra provided data for constraints functions
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()

    #Call the stored filters in stored order
    for storedConstraints in storedConstraints:
    
        storedConstraints.Execute(dict)
        
    return calibrationConstraintsFunctions
    
