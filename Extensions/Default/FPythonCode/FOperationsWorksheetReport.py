""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/scripts/FOperationsWorksheetReport.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FOperationsWorksheetReport - Run Script GUI for report creation

    (c) Copyright 2009 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    FOperationsWorksheetReport is WYSIWYG reporting. The reports are created based on the content
    of workbooks or trading sheet templates.

    This is the main GUI for FOperationsWorksheetReport. The GUI is split up to several files,
    one for each tab. This module also creates an instance of FReportAPI, sets all its
    properties and runs the script.

-------------------------------------------------------------------------------------------------------"""
import acm

import FRunScriptGUI

import FAddContentTab
import FPostProcessingTab
import FAdvancedSettingsTab
import FOutputSettingsTab

import FReportAPI
import FReportUtils
import FReportSheetSettingsTab
import FLogger

logger = FLogger.FLogger( 'FAReporting' )

falseTrue = ['False', 'True']
allSheetSettingsBySheetType = None
defaultParams = []

def runScriptValue(field):
    """ Return value on form suitable for displaying in Run Script GUI. """
    if hasattr(field, 'IsKindOf') and field.IsKindOf('FArray'):
        return field.AsString().replace(']', '').replace('[', '').replace('\'', '')
    else:
        return None

def startRunScript(eii):
    acm.RunModuleWithParameters("FOperationsWorksheetReport", acm.GetDefaultContext())

def appendDefaultParams(params):
    for i in params:
        defaultParams.append((i[0], i[4]))

class FOperationsWorksheetReport(FRunScriptGUI.AelVariablesHandler):
    def wbCB(self, index, fieldValues):
        """vice versa toggle between workbook and sheet template"""
        if self.ael_variables[index][0] == 'wbName':
            changeIndex = index + 1
        else:
            changeIndex = index - 1
        self.ael_variables[changeIndex][9] = (fieldValues[index] == '')
        return fieldValues

    def snapshotCB(self, index, fieldValues):
        """disable/enable settings after snapsheet toggle"""
        for idx in range(index + 1, index + 4):
            self.ael_variables[idx][9] = not (falseTrue.index(fieldValues[index]))
        return fieldValues

    def __init__(self):
        workbooks = [wb for wb in acm.FBackOfficeManagerWorkbook.Select('createUser = ' + str(acm.FUser[acm.UserName()].Oid()))]
        workbooks.sort()

        templates = acm.FArray()
        allTemplates = acm.FTradingSheetTemplate.Select('')
        for template in allTemplates:
            sheetClass = template.SheetClass()
            if sheetClass == acm.FSettlementSheet.Name() or sheetClass == acm.FConfirmationSheet.Name() or acm.FJournalSheet.Name():
                templates.Add(template)

        variables = [
                 ['wbName', 'Workbook', 'FBackOfficeManagerWorkbook', workbooks, "", 0, 0, \
                  'Choose a work book', self.wbCB, 1],
                 ['template', 'Operations Sheet Template', 'FTradingSheetTemplate', templates, None, 0, 1, 'Choose a operations sheet template', self.wbCB, 1],
                 ['snapshot', 'Sheet Snapshot', 'string', falseTrue, 'True', 1, 0, \
                  'Create a snapshot of a report', self.snapshotCB, 1],
                 ['multiThread', 'Run in background', 'string', falseTrue, 'True', 1, 0, \
                  'Start the reporting in a separate thread', None, 0],
                 ['numberOfReports', 'Number of Reports', 'int', None, '5', 1, 0, \
                  'The number of reports that will be created before the script is completed', None, 0],
                 ['updateInterval', 'Update Interval (sec)', 'int', None, '60', 1, 0, \
                  'The update interval, in seconds, between the reports', None, 0],
                 ['macros', 'Macros', 'string', None, '', 0, 0, \
                  'Macro values that should be applied to each row(where applicable) in the sheets', None, 1]
               ]

        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)

        #add other tabs
        global allSheetSettingsBySheetType

        self.extend(FOutputSettingsTab.getAelVariables())
        self.extend(FAdvancedSettingsTab.getAelVariables())

        appendDefaultParams([['instrumentParts', 'Include Instrument Parts', 'string', falseTrue, 'False', 1, 0, 'Instruments belonging to combinations will be visible', None, 1]])
        appendDefaultParams([['expandTimebucketChildren', 'Expand Sub Time Buckets ', 'string', falseTrue, 'False', 1, 0, 'Sub buckets of Time Buckets will be visible in report.', None, 1]])

        appendDefaultParams(FAddContentTab.getAelVariables())

        self.extend(FPostProcessingTab.getAelVariables())
        sheetSettingsVariables, allSheetSettingsBySheetType = FReportSheetSettingsTab.getAelVariables( [ 'FPortfolioSheet', 'FTradeSheet' ], acm.GetDefaultContext(), acm.CreateEBTag())
        for guiVariables in sheetSettingsVariables:
            appendDefaultParams(guiVariables)



ael_gui_parameters = {
    'windowCaption':__name__,
    'helpFileIndex':1151
}

ael_variables = FOperationsWorksheetReport()
ael_variables.LoadDefaultValues(__name__)

def ael_main(variableDictionary):
    params = FReportUtils.adjust_parameters(variableDictionary)
    variableDictionary[ 'allSheetSettingsBySheetType' ] = allSheetSettingsBySheetType
    for j in defaultParams:
        if not params.has_key(j[0]):
            params[j[0]] = j[1]
    report_params = FReportAPI.FWorksheetReportGuiParameters( guiParams=params )
    report_params.RunScript()



