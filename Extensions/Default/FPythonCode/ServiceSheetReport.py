
import os
import acm
import time
import FUxCore
import FRunScriptGUI
import FReportUtils

def GetServiceName(varDict):
    if varDict:
        return varDict.At(acm.FSymbol("serviceName"))
    return None

def GetSheetType(varDict):
    if varDict:
        return varDict.At(acm.FSymbol("sheetType"))
    return None

def GetViewType(varDict):
    if varDict:
        return varDict.At(acm.FSymbol("viewType"))
    return None

def GetUseTemplate(varDict):
    if varDict:
        return varDict.At(acm.FSymbol("useTemplate")) != 'False'
    return None

def GetSheetTemplate(varDict):
    if varDict:
        return varDict.At(acm.FSymbol("sheetTemplate"))
    return None

def GetCalculationEnvironment(varDict):
    if varDict:
        return varDict.At(acm.FSymbol("calculationEnvironment"))
    return None

def GetRowItems(varDict):
    if varDict:
        return varDict.At(acm.FSymbol("rowItems"))
    return acm.FArray()
    
def GetGrouper(varDict):
    if varDict:
        return varDict.At(acm.FSymbol("grouper"))
    return None
    
def GetColumns(varDict):
    if varDict:
        return varDict.At(acm.FSymbol("columns"))
    return acm.FArray()
    
def CreateDefinition(varDict):
    definition = None
    if GetUseTemplate(varDict):
        definition = acm.Report.CreatePredefinedServiceSheetReport(GetServiceName(varDict), GetSheetTemplate(varDict))
        definition.ReportName(GetSheetTemplate(varDict))
    else:
        definition = acm.Report.CreateOpenServiceSheetReport(GetServiceName(varDict), GetSheetType(varDict), GetViewType(varDict))
        definition.RowItems(GetRowItems(varDict))
        definition.Grouper(GetGrouper(varDict))
        definition.Columns(GetColumns(varDict))
        definition.ReportName('')
    definition.CalculationEnvironment(GetCalculationEnvironment(varDict))
    return definition
    
def RunReport(definition, varDict):
    xmlFileName = GetFileNameWithPath(varDict, '.xml')
    report = acm.Report.RunServiceSheetReport(definition, xmlFileName)
    return report

def GetFilePath(varDict):
    if varDict:
        p = varDict.At(acm.FSymbol("filePath"))
        if not os.path.exists(str(p)):
            raise Exception("Invalid directory")
        return str(p)
    return ""

def GetFileNameWithPath(varDict, ext):
    if varDict:
        p = GetFilePath(varDict)
        f = varDict.At(acm.FSymbol("fileName"))
        fileName = os.path.join(p, str(f) + ext)
        return fileName
    return None

def CreateOutputFileFromXml(xmlFileName, varDict, templateName, css, fileExt, writeMode):
    outputFileName = GetFileNameWithPath(varDict, fileExt)
    filePath = GetFilePath(varDict)
    return TransformXmlFile(xmlFileName, outputFileName, filePath, templateName, css, writeMode)

def TransformXmlFile(xmlFileName, outputFileName, filePath, templateName, css, writeMode):
    file = open(xmlFileName, "r")
    reportXml = str(file.read())
    file.close()
    extraParams = acm.FDictionary()
    extraParams.AtPut('outputDir', filePath)
    try:
        transformedStr = FReportUtils.transformXML(reportXml, templateName, css, extraParams)
        outputFile = open(outputFileName, writeMode)
        outputFile.write(transformedStr)
        outputFile.close()
        print 'Result written to file:', outputFileName
    except Exception, e:
        print 'Failed to create file:', outputFileName
        print str(e)
    return outputFileName

def CreateExtendedOutput(xmlFileName, varDict):
    if varDict.At(acm.FSymbol("enableHtmlOutput")) == 'True':
        CreateOutputFileFromXml(xmlFileName, varDict, 'FStandardTemplate', 'FStandardCSS', '.html', 'w')
    if varDict.At(acm.FSymbol("enableCsvOutput")) == 'True':
        CreateOutputFileFromXml(xmlFileName, varDict, 'FCSVTemplate', None, '.csv', 'wb')
    if varDict.At(acm.FSymbol("enableXlsOutput")) == 'True':
        CreateOutputFileFromXml(xmlFileName, varDict, 'FTABTemplate', None, '.xls', 'wb')

class AsyncReport():
    def __init__(self):
        self._report = None
        self._varDict = None

    def ServerUpdate(self, sender, aspect, param):
        if sender.IsDone():
            message = sender.StatusMessage()
            if message and len(message) > 0:
                print 'Failed to run', sender.StringKey(), ':', message
            else:
                xmlFileName = GetFileNameWithPath(self._varDict, '.xml')
                print 'Result written to file:', xmlFileName
                CreateExtendedOutput(xmlFileName, self._varDict)
            sender.RemoveDependent(self)
            sender.Destroy()
        
    def Run(self, varDict):
        self._varDict = varDict
        self._report = RunReport(CreateDefinition(varDict), varDict)
        self._report.AddDependent(self)
        return self._report
        

def CreateAelVariableDictionary( aelVariables ):
    varDict = acm.FDictionary()
    varDict.AtPut(acm.FSymbol('serviceName'), aelVariables['serviceName'])
    varDict.AtPut(acm.FSymbol('useTemplate'), aelVariables['useTemplate'])
    varDict.AtPut(acm.FSymbol('sheetTemplate'), aelVariables['sheetTemplate'])
    varDict.AtPut(acm.FSymbol('sheetType'), aelVariables['sheetType'])
    varDict.AtPut(acm.FSymbol('viewType'), aelVariables['viewType'])
    varDict.AtPut(acm.FSymbol('rowItems'), aelVariables['rowItems'])
    varDict.AtPut(acm.FSymbol('grouper'), aelVariables['grouper'])
    varDict.AtPut(acm.FSymbol('columns'), aelVariables['columns'])
    varDict.AtPut(acm.FSymbol('calculationEnvironment'), aelVariables['calculationEnvironment'])
    varDict.AtPut(acm.FSymbol('filePath'), aelVariables['filePath'])
    varDict.AtPut(acm.FSymbol('fileName'), aelVariables['fileName'])
    varDict.AtPut(acm.FSymbol('enableHtmlOutput'), aelVariables['enableHtmlOutput'])
    varDict.AtPut(acm.FSymbol('enableCsvOutput'), aelVariables['enableCsvOutput'])
    varDict.AtPut(acm.FSymbol('enableXlsOutput'), aelVariables['enableXlsOutput'])
    return varDict

def ClearInsertedContent(fieldValues):
    fieldValues[indexOfVar['rowItems']] = ''
    fieldValues[indexOfVar['grouper']] = ''
    fieldValues[indexOfVar['columns']] = ''
        
def GetTypesFinder(fieldValues, locals):
    serviceName = fieldValues[indexOfVar['serviceName']]
    serviceTypesFinder = locals.At('typesFinder')
    if serviceTypesFinder and serviceTypesFinder.ServiceName() != serviceName:
        serviceTypesFinder.Destroy()
        serviceTypesFinder = None
    if serviceTypesFinder == None:
        serviceTypesFinder = acm.Report.CreateEnumeratedTypesFinder(serviceName)
        locals.AtPut('typesFinder', serviceTypesFinder)
    return serviceTypesFinder
            
def OnServiceNameChanged(index, fieldValues, locals):
    serviceName = fieldValues[index]
    environmentNames = []
    if serviceName == "FrontArena.HierarchicalGrid.Sheets":
        environments = acm.FStoredCalculationEnvironment.Select("").SortByProperty('Name', True)
        for e in environments:
            environmentNames.append(e.Name())

    serviceTypesFinder = GetTypesFinder(fieldValues, locals)
    
    if WaitUntilFinderDone(serviceTypesFinder):
    
        sheetTypes = serviceTypesFinder.SheetTypes()
        sheetTemplates = serviceTypesFinder.SheetTemplates()
        
        for i, var in enumerate(ael_variables):
            if var[FRunScriptGUI.Controls.NAME] == 'sheetTemplate':
                ael_variables[i][FRunScriptGUI.Controls.VALUES] = sheetTemplates
                if not fieldValues[i] in sheetTemplates:
                    fieldValues[i] = ''
            if var[FRunScriptGUI.Controls.NAME] == 'sheetType':
                ael_variables[i][FRunScriptGUI.Controls.VALUES] = sheetTypes
                if not fieldValues[i] in sheetTypes:
                    fieldValues[i] = ''
            if var[FRunScriptGUI.Controls.NAME] == 'calculationEnvironment':
                ael_variables[i][FRunScriptGUI.Controls.ENABLED] = len(environmentNames) > 0
                ael_variables[i][FRunScriptGUI.Controls.VALUES] = environmentNames
                if not fieldValues[i] in environmentNames:
                    fieldValues[i] = ''

    return fieldValues

def OnSheetTypeChanged(index, fieldValues, locals):
    sheetType = fieldValues[index]
    
    serviceTypesFinder = GetTypesFinder(fieldValues, locals)
    serviceTypesFinder.ViewType(None)
    serviceTypesFinder.SheetType(sheetType)
    
    if WaitUntilFinderDone(serviceTypesFinder):

        viewTypes = serviceTypesFinder.ViewTypes()

        for i, var in enumerate(ael_variables):
            if var[FRunScriptGUI.Controls.NAME] == 'viewType':
                ael_variables[i][FRunScriptGUI.Controls.VALUES] = viewTypes
                if not fieldValues[i] in viewTypes:
                    fieldValues[i] = ''

    return fieldValues
    
def OnViewTypeChanged(index, fieldValues, locals):

    viewType = fieldValues[index]
    serviceTypesFinder = GetTypesFinder(fieldValues, locals)
    serviceTypesFinder.ViewType(viewType)

    if WaitUntilFinderDone(serviceTypesFinder):

        pass

    return fieldValues
    
def OnUseTemplateChanged(index, fieldValues, locals):
    useTemplate = fieldValues[index]
    serviceTypesFinder = GetTypesFinder(fieldValues, locals)

    sheetTemplateVar = ael_variables[indexOfVar['sheetTemplate']]
    sheetTemplateVar[FRunScriptGUI.Controls.ENABLED] = useTemplate == 'True'
    if useTemplate == 'True':
        sheetTemplateVar[FRunScriptGUI.Controls.VALUES] = serviceTypesFinder.SheetTemplates()
    elif useTemplate == 'False':
        fieldValues[indexOfVar['sheetTemplate']] = ''

    for i, var in enumerate(ael_variables):
        if var[FRunScriptGUI.Controls.NAME] in ['sheetType', 'viewType', 'rowItems', 'grouper', 'columns']:
            ael_variables[i][FRunScriptGUI.Controls.ENABLED] = useTemplate == 'False'
            if useTemplate == 'True':
                if var[FRunScriptGUI.Controls.NAME] == 'grouper':
                    ael_variables[i][FRunScriptGUI.Controls.VALUES] = None
                else:
                    ael_variables[i][FRunScriptGUI.Controls.VALUES] = []
                fieldValues[i] = ''
            elif useTemplate == 'False':
                if var[FRunScriptGUI.Controls.NAME] == 'sheetType':
                    ael_variables[i][FRunScriptGUI.Controls.VALUES] = serviceTypesFinder.SheetTypes()
                    serviceTypesFinder.SheetType(None)
           
    return fieldValues

def OnSheetTemplateChanged(index, fieldValues, locals):
    sheetTemplateName = fieldValues[index]
    serviceTypesFinder = GetTypesFinder(fieldValues, locals)
   
    ael_variables[indexOfVar['sheetTemplate']][FRunScriptGUI.Controls.VALUES] = serviceTypesFinder.SheetTemplates()
    if not sheetTemplateName in serviceTypesFinder.SheetTemplates():
        fieldValues[index] = ''

    return fieldValues

def WaitUntilFinderDone(typesFinder):
    typesFinder.Run(10)
    return typesFinder.IsDone()

def SelectRowItems(shell, params):
    return SelectFromDialog(shell, 'RowItems', params)

def SelectGrouper(shell, params):
    return SelectFromDialog(shell, 'Grouper', params)

def SelectColumns(shell, params):
    return SelectFromDialog(shell, 'Columns', params)

def SelectFromDialog(shell, what, params):
    initiallySelected = params.At('selected')
    locals = params.At('locals')
    resultDict = acm.FDictionary()
    resultDict.AtPut('result', initiallySelected)
    serviceTypesFinder = locals.At('typesFinder')

    if WaitUntilFinderDone(serviceTypesFinder):
        selected = []
        if what == 'RowItems':
            selected = acm.UX().Dialogs().SelectSubset(shell, serviceTypesFinder.AllRowItems(), 'Insert Items', False, initiallySelected)
        if what == 'Grouper':
            grouper = acm.UX().Dialogs().SelectObject(shell, 'Grouper', '', serviceTypesFinder.AllGroupers(), None)
            if grouper:
                selected = [grouper]
        if what == 'Columns':
            selected = acm.UX().Dialogs().SelectSubset(shell, serviceTypesFinder.AllColumns(), 'Select Columns', False, initiallySelected)
        if selected:
            resultDict.AtPut('result', selected)
    return resultDict
    
def OnEnableHtmlChanged(index, fieldValues, locals):
    return fieldValues

def OnEnableCsvChanged(index, fieldValues, locals):
    return fieldValues

def OnEnableXlsChanged(index, fieldValues, locals):
    return fieldValues

def HandleLocals(event, locals):
    if event == 'clear':
        serviceTypesFinder = locals.RemoveKey('typesFinder')
        if serviceTypesFinder:
            serviceTypesFinder.Destroy()
        

serviceNameList = ["FrontArena.HierarchicalGrid.Sheets", "FrontArena.HierarchicalGrid.PositionSheet"]

directorySelection=FRunScriptGUI.DirectorySelection()
trueFalse = ['False', 'True']
ael_variables = [
['serviceName', 'Service', 'string', serviceNameList, serviceNameList[0], True, False, '', OnServiceNameChanged, True],
['useTemplate', 'Use Template',  'string', trueFalse, 'True', True, False, 'Use sheet contents in template or select below', OnUseTemplateChanged, True],
['sheetTemplate', 'Sheet Template',  'string', [], None, True, False, '', OnSheetTemplateChanged, True],
['sheetType', 'Sheet Type',  'string', [], None, True, False, '', OnSheetTypeChanged, True],
['viewType', 'View Type',  'string', [], None, False, False, '', OnViewTypeChanged, True],
['rowItems', 'Insert Items', 'string', [], None, False, True, 'Select row items to include in report', None, 1, SelectRowItems],
['grouper', 'Grouper', 'string', None, None, False, False, 'Select grouper for inserted row items', None, 1, SelectGrouper],
['columns', 'Columns', 'string', [], None, False, True, 'Select columns to include in report', None, 1, SelectColumns],
['calculationEnvironment',  'Calculation Environment',  'string', [], None, True, False, '', None, True],
['filePath', 'File Path', directorySelection, None, directorySelection, False, True, 'The file path to the ouput file directory.', None, True],
['fileName', 'File Name', 'string', None, "Report", False, False, 'The name of the output file', None, None],
['enableHtmlOutput', 'Include HTML output file', 'string', trueFalse, 'False', True, False, 'Create an HTML output file', OnEnableHtmlChanged, True],
['enableCsvOutput', 'Include CSV output file', 'string', trueFalse, 'False', True, False, 'Create a .csv output file with comma separated values', OnEnableCsvChanged, True],
['enableXlsOutput', 'Include Excel output file', 'string', trueFalse, 'False', True, False, 'Create an Excel97 .xls output file', OnEnableXlsChanged, True]
]
indexOfVar = {}
for i, var in enumerate(ael_variables):
    indexOfVar[var[FRunScriptGUI.Controls.NAME]] = i

ael_gui_parameters = {
    'windowCaption':'Service Sheet Report',
    'helpFileIndex':1152,
    'runButtonLabel':'Run Report',
    'enableCollectiveRun':True,
    'handleLocals':HandleLocals
    }

def ael_main(vars):
    varDict = CreateAelVariableDictionary(vars)
    report = AsyncReport().Run(varDict)
    return {'activity': report}
