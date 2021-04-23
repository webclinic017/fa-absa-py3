import acm
import PositionSnapshotCorrectCreateTask

valueSession_tt = 'The value session that needs to be corrected'
positionFilter_tt = 'A filter specifying which positions to correct'
calculationEnvironment_tt = 'The calculation environment used to get the correct numbers'
storeHistory_tt = 'Decides whether the original value should be kept in the database or not'
correctionComment_tt = 'A comment describing the correction'

def StartPositionCorrection(eii):
    acm.RunModuleWithParameters("PositionCorrection", acm.GetDefaultContext()) 

valueSessions = acm.FValueSession.Select("parent = 0")
valueSessionStringKeys = []
valueSessionPerStringKey = {}
for vSession in valueSessions:
    if acm.FPositionDataDisposition[vSession.DataDisposition()]:
        valueSessionStringKey = vSession.StringKey()
        valueSessionPerStringKey[valueSessionStringKey] = vSession
        valueSessionStringKeys.append(valueSessionStringKey)

calculationEnvironments = acm.FStoredCalculationEnvironment.Select('').SortByProperty('Name', True)
defaultEnvironment = acm.GetFunction("DefaultCalculationEnvironmentName", 1)(acm.User())
falseTrue = ['False', 'True']

def DefinitionFromAelVariables( aelVariables ):
    definition = acm.FDictionary()
    definition.AtPut(acm.FSymbol('valueSession'), valueSessionPerStringKey[aelVariables['valueSession']])
    definition.AtPut(acm.FSymbol('sessionType'), definition.At(acm.FSymbol('valueSession')).Type().StringKey())
    definition.AtPut(acm.FSymbol('disposition'), acm.FPositionDataDisposition[definition.At('valueSession').DataDisposition()])
    definition.AtPut(acm.FSymbol('positionFilter'), aelVariables['positionFilter'])
    definition.AtPut(acm.FSymbol('storeHistory'), falseTrue.index(aelVariables['storeHistory']))
    if falseTrue.index(aelVariables['storeHistory']):
        definition.AtPut(acm.FSymbol('correctionComment'), aelVariables['correctionComment'])
    if aelVariables['calculationEnvironment']:
        definition.AtPut(acm.FSymbol('calculationEnvironment'), aelVariables['calculationEnvironment'].StringKey())
    return definition

def storeHistoryCB(index, fieldValues):
    ael_variables[index + 1][9] = (falseTrue.index(fieldValues[index]))
    return fieldValues
    
def valueSessionCB(index, fieldValues):
    if fieldValues[index]:
        valueSession = valueSessionPerStringKey[fieldValues[index]]
        dataDisposition = acm.FPositionDataDisposition[valueSession.DataDisposition()]
        positionSpecification = dataDisposition.PositionSpecification()
        filterType = acm.PositionStorage.FilterType(positionSpecification)
        parameterisedDialog = lambda shell, params: posFilterCustomDialog(shell, params, filterType)
        ael_variables[index + 1][10] = parameterisedDialog
        if len(fieldValues[index + 1]):
            currentType = acm.FStoredASQLQuery[fieldValues[index + 1]].TypeDisplayName()
            if not acm.FSymbol(currentType[:currentType.rfind('Filter')-1]).IsEqual(filterType):
                fieldValues[index + 1] = None
        ael_variables[index + 1][9] = True
    else:
        ael_variables[index + 1][9] = False
        fieldValues[index + 1] = None
    return fieldValues
    
def posFilterCustomDialog(shell, params, filterType):
    query = [acm.UX().Dialogs().SelectStoredASQLQuery(shell, filterType)]
    if query[0] is None:
        query = params['selected']
    resultDic = acm.FDictionary()
    resultDic.AtPut('result', query)
    return resultDic

def startDlg(shell, definition, extraData):
    dlgStr = ('Note that updates on corrected historical values are not automatically propagated in open ARENA BI views.\n' +
                'A reload of the affected workbenches is required for the views to reflect the corrected values.')
    acm.UX().Dialogs().MessageBoxInformation(shell, dlgStr)
    return True
    
ael_gui_parameters = {'validateBeforeRun' : startDlg}

ael_variables = [
  ['valueSession',  'Value Session',  'string', valueSessionStringKeys, None, 1, 0, valueSession_tt, valueSessionCB, True],
  ['positionFilter',  'Position Filter',  'FStoredASQLQuery', None, None, 0, 0, positionFilter_tt, None, False, None],
  ['storeHistory',  'Store History',  'string', falseTrue, False, 1, 0, storeHistory_tt, storeHistoryCB, True],
  ['correctionComment',  'Correction Comment',  'string', None, None, 0, 0, correctionComment_tt, None, False],
  ['calculationEnvironment',  'Calculation Environment',  'FStoredCalculationEnvironment', calculationEnvironments, defaultEnvironment, 0, 0, calculationEnvironment_tt, None, True]
]

def ael_main(vars):
    definition = DefinitionFromAelVariables(vars)
    return PositionSnapshotCorrectCreateTask.CreateActivity(definition)
