import acm
import PositionSnapshotCorrectCreateTask

type_tt = "The type of value session to be created."
disposition_tt = "The data disposition for which the value session will be created."
calcEnv_tt = 'Defines the calculation environment used when calculating values to be stored. If left blank, the default environment will be used.'

def StartPositionSnapshot(eii):
    acm.RunModuleWithParameters("PositionSnapshot", acm.GetDefaultContext()) 
    
def DefinitionFromAelVariables( aelVariables ):
    definition = acm.FDictionary()
    definition.AtPut(acm.FSymbol('disposition'), aelVariables['disposition'])
    definition.AtPut(acm.FSymbol('sessionType'), aelVariables['sessionType'].StringKey())
    if aelVariables['calculationEnvironment']:
        definition.AtPut(acm.FSymbol('calculationEnvironment'), aelVariables['calculationEnvironment'].StringKey())
    return definition

dispositions = acm.FPositionDataDisposition.Select('').SortByProperty('Name', True)
sessionTypes = acm.FValueSessionType.Select('').SortByProperty('Name', True)
calculationEnvironments = acm.FStoredCalculationEnvironment.Select('').SortByProperty('Name', True)
defaultEnvironment = acm.GetFunction("DefaultCalculationEnvironmentName", 1)(acm.User())

ael_variables = [
[       'disposition',  'Data Disposition',     'FPositionDataDisposition', dispositions, None, 1, 0, disposition_tt, None, True],
[       'sessionType',  'Value Session Type',  'FValueSessionType',      sessionTypes, None, 1, 0, type_tt, None, True],
[       'calculationEnvironment', 'Calculation Environment', acm.FStoredCalculationEnvironment, calculationEnvironments, defaultEnvironment, 0, 0, calcEnv_tt, None, True]
]

def ael_main(vars):
    definition = DefinitionFromAelVariables(vars)
    return PositionSnapshotCorrectCreateTask.CreateActivity(definition)
