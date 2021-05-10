import acm
import time
import PositionDeleteCore
import StartTaskDlg

def StartPositionDelete(eii):
    acm.RunModuleWithParameters("PositionDelete", acm.GetDefaultContext()) 
    
def DefinitionFromAelVariables( aelVariables ):
    definition = acm.FDictionary()
    definition.AtPut(acm.FSymbol('sessionType'), aelVariables['sessionType'])
    definition.AtPut(acm.FSymbol('dateFrom'), aelVariables['dateFrom'])
    definition.AtPut(acm.FSymbol('dateTo'), aelVariables['dateTo'])
    definition.AtPut(acm.FSymbol('dataDisposition'), aelVariables['dataDisposition'])
    return definition
    
def ReturnStringOrDefault(element, defaultString):
    returnStr = defaultString
    if element:
        try: 
            returnStr = element.StringKey()
        except:
            returnStr = element
    return returnStr

def CreateDlgStrFromDefinition(inputStr, definition):
    dialogStr = inputStr
    dialogStr = dialogStr + "  * with Position Data Disposition: %s;\n" % ReturnStringOrDefault( definition.At(acm.FSymbol('dataDisposition')), "Any" )
    dialogStr = dialogStr + "  * of Type: %s; and\n" % ReturnStringOrDefault( definition.At(acm.FSymbol('sessionType')), "Any" )
    dialogStr = dialogStr + "  * with time stamp after: %s and before: %s.\n" \
        % (ReturnStringOrDefault( definition.At(acm.FSymbol('dateFrom')), "Inception" ),  ReturnStringOrDefault( definition.At(acm.FSymbol('dateTo')), "Big Date" ))
    dialogStr = dialogStr + "Matching Value Sessions will also be deleted.\n"
    dialogStr = dialogStr + "Are you sure you want to proceed?"
    return dialogStr
    
def warningDlgRun(shell, definition, extraData):
    inputStr = "You are about to delete Position Calculations associated with Value Sessions:\n"
    ret = StartTaskDlg.Show(shell, "Attention!", "attention",  CreateDlgStrFromDefinition(inputStr, definition))
    return ret
    
def warningDlgSave(shell, definition, extraData):
    inputStr = "You are about to save a task which will delete Position Calculations associated with Value Sessions:\n"
    ret = StartTaskDlg.Show(shell, "Attention!", "attention",  CreateDlgStrFromDefinition(inputStr, definition))
    return ret

dispositions = acm.FPositionDataDisposition.Select('').SortByProperty('Name', True)
sessionTypes = acm.FValueSessionType.Select('').SortByProperty('Name', True)
columns = acm.FStoredColumnCreator.Select('').SortByProperty('Name', True)

ael_variables = [
[       'dataDisposition',      'Data Disposition',     'FPositionDataDisposition',     dispositions,   None, 0, 0, PositionDeleteCore.disposition_tt, None, True],
[       'sessionType',          'Value Session Type',   'FValueSessionType',            sessionTypes,   None, 0, 0, PositionDeleteCore.type_tt, None, True],
[       'dateFrom',             'Value Session Start',  'string',                       None,           None, 0, 0, PositionDeleteCore.from_tt, None, True],
[       'dateTo',               'Value Session End',    'string',                       None,           None, 0, 0, PositionDeleteCore.to_tt, None, True]
]


ael_gui_parameters = {  'validateBeforeRun' : warningDlgRun,
                        'validateBeforeSave' : warningDlgSave}


def ael_main(vars):
    definition = DefinitionFromAelVariables(vars)
    return PositionDeleteCore.CreateActivity(definition)

