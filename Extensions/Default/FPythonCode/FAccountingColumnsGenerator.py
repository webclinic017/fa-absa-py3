""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/subledgermigration/FAccountingColumnsGenerator.py"
import acm
import inspect
import time
import FOperationsUtils
import FRunScriptGUI

try:
    import FAccounting
except ImportError:
    errorMsg = 'Could not import module FAccounting. The module needs to be stored either directly in the database or as an extension'
    FOperationsUtils.LogAlways(errorMsg)
    raise ImportError(errorMsg)


COLUMNIDPREFIX = 'FAccounting'
EXTATTRIBUTEPREFIX = 'fAccounting'

EXTATTRIBUTECLASSESTRADESHEETCOLUMN = ['FTrade', 'FLegAndTrades']
EXTATTRIBUTECLASSESMFSHEETCOLUMN = ['FMoneyFlow']
EXTATTRIBUTEROWCLASSESTRADESHEETCOLUMN = ['FTradeRow']
EXTATTRIBUTEROWCLASSESMFSHEETCOLUMN = ['FMoneyFlowAndTrades']

COLUMNDEFTEMPLATE = 'FTradingSheet:<ColumnID> =\n\
    Access=ReadOnly\n\
    ExtensionAttribute=<ExtAttribute>\n\
    GroupLabel=FAccounting\n\
    Name=<ColumnName>'

ROWCLASSEXTATTRIBUTETEMPLATE = '<FClass>:<ExtAttribute> = <CalcObjectAttribute>:<ExtAttribute> [profitAndLossEndDate];'

CALCOBJECTATTRIBUTETEMPLATE = '<FClass>:<ExtAttribute> =\n\
    object:fAccountingValue [fAccountingFunctionName = \"<FunctionName>\", profitAndLossEndDate];'

ROWCLASSCALCOBJECTATTRIBUTEDICT = dict({'FTradeRow': 'trade', 'FMoneyFlowAndTrades': 'moneyFlow'})

TEMPCONTEXT = acm.Create('FExtensionContext')



def CreateColumnDefinition(columnID, columnName, extensionAttributeName, definitionTemplate):
    columnDefinition = definitionTemplate
    columnDefinition = columnDefinition.replace('<ColumnID>', columnID)
    columnDefinition = columnDefinition.replace('<ExtAttribute>', extensionAttributeName)
    columnDefinition = columnDefinition.replace('<ColumnName>', columnName)

    return columnDefinition

def CreateExtensionAttributeDefinition(fClass, extensionAttribute, functionName, definitionTemplate):
    attributeDefinition = definitionTemplate
    attributeDefinition = attributeDefinition.replace('<FClass>', fClass)
    attributeDefinition = attributeDefinition.replace('<ExtAttribute>', extensionAttribute)
    attributeDefinition = attributeDefinition.replace('<FunctionName>', functionName)

    return attributeDefinition

def CreateRowClassExtensionAttributeDefinition(rowClass, extensionAttribute, functionName, definitionTemplate):
    attributeDefinition = CreateExtensionAttributeDefinition(rowClass, extensionAttribute, functionName, definitionTemplate)
    if ROWCLASSCALCOBJECTATTRIBUTEDICT.has_key(rowClass):
        attributeDefinition = attributeDefinition.replace('<CalcObjectAttribute>', ROWCLASSCALCOBJECTATTRIBUTEDICT[rowClass])

    return attributeDefinition

def GetFunctionNames(module, minNumberOfArguments):
    functionNames = []
    for functionName in dir(module):
        fAccountingFunction = getattr(FAccounting, functionName)
        if type(fAccountingFunction).__name__ == 'function':
            args = inspect.getargspec(fAccountingFunction)[0]
            if len(args) >= minNumberOfArguments:
                functionNames.append(functionName)
    return functionNames

def SuggestColumnName(functionName):
    suggestedColumnName = None
    for nameSegment in functionName.split('_'):
        if suggestedColumnName is None:
            suggestedColumnName = nameSegment.capitalize()
        else:
            suggestedColumnName = suggestedColumnName + ' ' + nameSegment.capitalize()

    return suggestedColumnName

def SuggestExtensionAttributeName(functionName):
    suggestedExtensionAttributeName = EXTATTRIBUTEPREFIX
    for nameSegment in functionName.split('_'):
        suggestedExtensionAttributeName = suggestedExtensionAttributeName + nameSegment.capitalize()

    return suggestedExtensionAttributeName

def SuggestColumnID(columnName):
    return COLUMNIDPREFIX + ' ' + columnName

def CreateFAccountingColumn(columnName, extensionAttributeName, extAttributeClasses, extAttributRowClasses, functionName, sheetGroupNames, context):
    columnID = SuggestColumnID(columnName)
    columnDefinition = CreateColumnDefinition(columnID, columnName, extensionAttributeName, COLUMNDEFTEMPLATE)
    context.EditImport('FColumnDefinition', columnDefinition)
    for sheetGroupName in sheetGroupNames:
        context.AddMember(columnID, 'FColumnDefinition', 'sheet columns', sheetGroupName)

    for fClass in extAttributeClasses:
        extensionAttributeDefinition = CreateExtensionAttributeDefinition(fClass, extensionAttributeName, functionName, CALCOBJECTATTRIBUTETEMPLATE)
        context.EditImport('FExtensionAttribute', extensionAttributeDefinition)

    for rowClass in extAttributRowClasses:
        extensionAttributeDefinition = CreateRowClassExtensionAttributeDefinition(rowClass, extensionAttributeName, functionName, ROWCLASSEXTATTRIBUTETEMPLATE)
        context.EditImport('FExtensionAttribute', extensionAttributeDefinition)

    return columnID

def CreateFAccountingColumns(functionNames, extAttributeClasses, extAttributRowClasses, sheetGroupNames, context):
    createdColumns = []
    for functionName in functionNames:
        columnName = SuggestColumnName(functionName)
        extensionAttributeName = SuggestExtensionAttributeName(functionName)

        createdColumn = CreateFAccountingColumn(columnName, extensionAttributeName, extAttributeClasses, extAttributRowClasses, functionName, sheetGroupNames, context)
        createdColumns.append(createdColumn)

    return createdColumns

def CreateColumnsExtensionModule(moduleName, functionNamesForTradeColumns, functionNamesForMFColumns):
    extensionModule = acm.FExtensionModule()
    extensionModule.Name(moduleName)

    TEMPCONTEXT.AddModule(extensionModule)
    extensionModule = acm.FExtensionModule[moduleName] #Need to do this as Addmodule also commits the module

    createdTradeColumns = CreateFAccountingColumns(functionNamesForTradeColumns, EXTATTRIBUTECLASSESTRADESHEETCOLUMN, EXTATTRIBUTEROWCLASSESTRADESHEETCOLUMN, ['tradesheet', 'dealsheet'], TEMPCONTEXT)
    createdMFColumns = CreateFAccountingColumns(functionNamesForMFColumns, EXTATTRIBUTECLASSESMFSHEETCOLUMN, EXTATTRIBUTEROWCLASSESMFSHEETCOLUMN, ['moneyflowsheet'], TEMPCONTEXT)

    extensionModule.Commit()

    return [createdTradeColumns, createdMFColumns]

#--------------------------------------------------------------------------------------------------------------------------------------------------------------#
class ColumnsGeneratorRunScript(FRunScriptGUI.AelVariablesHandler):

    def __UseExistingModuleCB(self, index, fieldValues):
        useExistingColumn = fieldValues[index]

        moduleNameField = self.ModuleName
        existingModuleNameField = self.ExistingModuleName
        moduleNameField.enable(useExistingColumn != 'true') #useExistingColumn is of type 'str'
        existingModuleNameField.enable(useExistingColumn == 'true')

        return fieldValues

    def __init__(self):
        fAccountingColumnsModule = acm.FExtensionModule['FAccountingColumns']
        fAccountingColumnsModuleExists = (fAccountingColumnsModule != None)
        if fAccountingColumnsModuleExists:
            moduleNameFieldDefault = None
            existingModuleNameFieldDefault = 'FAccountingColumns'
            moduleNameFieldEnabled = 0
            existingModuleNameFieldEnabled = 1
        else:
            moduleNameFieldDefault = 'FAccountingColumns'
            existingModuleNameFieldDefault = None
            moduleNameFieldEnabled = 1
            existingModuleNameFieldEnabled = 0

        allFunctionNames = GetFunctionNames(FAccounting, 8)

        variables = [['ModuleName', 'Create module', 'string', None, moduleNameFieldDefault, 1, 0, None, None, 0, moduleNameFieldEnabled],
                 ['UseExistingModule', 'Use existing module', 'bool', [False, True], fAccountingColumnsModuleExists, 0, 0, None, self.__UseExistingModuleCB, 1],
                 ['ExistingModuleName', 'Module', 'string', GetAllModules(), existingModuleNameFieldDefault, 2, 0, None, None, existingModuleNameFieldEnabled],
                 ['TradeColumns', 'Trade columns', 'string', allFunctionNames, None, 0, 1, None, None, 1],
                 ['MoneyFlowColumns', 'Money flow columns', 'string', allFunctionNames, None, 0, 1, None, None, 1]]

        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)


def GetAllModules():
    return acm.FExtensionModule.Instances()

def GetSelectedModuleName(variablesDict):
    selectedModuleName = variablesDict['ModuleName']

    return selectedModuleName

def GetSelectedExistingModuleName(variablesDict):
    selectedExistingModuleName = variablesDict['ExistingModuleName']

    return selectedExistingModuleName

def GetSelectedTradeColumns(variablesDict):
    return variablesDict['TradeColumns']

def GetSelectedMoneyFlowColumns(variablesDict):
    return variablesDict['MoneyFlowColumns']

ael_variables = ColumnsGeneratorRunScript()

def ael_main(variablesDict):
    validInput = True

    selectedModuleName = GetSelectedModuleName(variablesDict)
    if selectedModuleName is None or selectedModuleName == '':
        selectedModuleName = GetSelectedExistingModuleName(variablesDict)
    elif acm.FExtensionModule[selectedModuleName] is not None:
        FOperationsUtils.LogAlways('The module %s already exists. Check \'Use existing module\' and select it in the drop down list if you wish to use it.' % selectedModuleName)
        validInput = False

    if validInput:
        tradeColumns = GetSelectedTradeColumns(variablesDict)
        moneyFlowColumns = GetSelectedMoneyFlowColumns(variablesDict)

        createdTradeColumns, createdMFColumns = CreateColumnsExtensionModule(selectedModuleName, tradeColumns, moneyFlowColumns)

        FOperationsUtils.LogAlways('Created %d trade column(s):' % len(createdTradeColumns))
        for createdTradeColumn in createdTradeColumns:
            FOperationsUtils.LogAlways(createdTradeColumn)

        FOperationsUtils.LogAlways('Created %d money flow column(s):' % len(createdMFColumns))
        for createdMFColumn in createdMFColumns:
            FOperationsUtils.LogAlways(createdMFColumn)

        timeNowAsString = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        FOperationsUtils.LogAlways('FAccountingColumnsGenerator FINISHED at %s' % timeNowAsString)