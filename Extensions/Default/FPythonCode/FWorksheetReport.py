"""-------------------------------------------------------------------------------------------------------
MODULE
    FWorksheetReport - Run Script GUI for report creation

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    FWorksheetReport is WYSIWYG reporting. The reports are created based on the content
    of workbooks or trading sheet templates. Additional content can be added on the fly,
    such as portfolios, trade filters and trades.

    This is the main GUI for FWorksheetReport. The GUI is split up to several files,
    one for each tab. This module also creates an instance of FReportAPI, sets all its
    properties and runs the script.

-------------------------------------------------------------------------------------------------------"""
import acm
import ael

import FRunScriptGUI

import FAddContentTab
import FPostProcessingTab
import FAdvancedSettingsTab
import FOutputSettingsTab

import FReportAPI
import FReportUtils
import FReportSheetSettingsTab
import FMacroGUI
import FLogger

logger = FLogger.FLogger( 'FAReporting' )

falseTrue = ['False', 'True']
allSheetSettingsBySheetType = None

def runScriptValue(field):
    """ Return value on form suitable for displaying in Run Script GUI. """
    if hasattr(field, 'IsKindOf') and field.IsKindOf('FArray'):
        return field.AsString().replace(']', '').replace('[', '').replace('\'', '')
    else:
        return None

def startRunScript(eii):
    acm.RunModuleWithParameters("FWorksheetReport", acm.GetDefaultContext())

class WorksheetReport(FRunScriptGUI.AelVariablesHandler):
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

    def on_query_name_changes(self, index, fieldvalues):
        """GUI Callback, triggered by user selecting a query in the 'query name' field-
        When the query name changes the macro fields will be reset and the macro names
        from the new query will be displayed."""
        
        macrosIndex = 0
        while self.ael_variables[macrosIndex][0] != 'macros' and macrosIndex < len(self.ael_variables):
            macrosIndex = macrosIndex + 1       
            
        if self.ael_variables[macrosIndex][0] == 'macros':
            macroSet = set()
            for macro in self.ael_variables[macrosIndex][3]:
                macroSet.add(macro)
            query_names = fieldvalues[index]
            if query_names:
                macro_variables=[]
                query_names = query_names.split(',')            
                for query in query_names:
                    macro_variables = macro_variables + FMacroGUI.macro_gui(query, {})

                for i in macro_variables:
                    macroSet.add("%s=%s"%(i[0], i[4]))
                
        newMacroList = []
        for i in macroSet:
            newMacroList.append(i)
        
        self.ael_variables[macrosIndex][3] = newMacroList
            
        return fieldvalues
    
    def getWorkbooks(self):
        workbooks = [wb for wb in acm.FWorkbook.Select('createUser = ' + str(acm.FUser[acm.UserName()].Oid()))]
        workbooks.sort()
        return workbooks
    
    def getTemplates(self):
        return acm.FTradingSheetTemplate.Select('')
    
    def __init__(self):       
        vars = [
                 ['wbName', 'Workbook', 'FWorkbook', self.getWorkbooks, "", 0, 0, \
                  'Choose a work book', self.wbCB, 1],
                 ['template', 'Trading Sheet Template', 'FTradingSheetTemplate', self.getTemplates, None, 0, 1, 'Choose a trading sheet template', self.wbCB, 1],
                 ['instrumentParts', 'Include Instrument Parts', 'string', falseTrue, 'False', 1, 0, 'Instrument parts, and if applicable legs for multi leg instruments, will be visible in report.', None, 1],
                 ['expandTimebucketChildren', 'Expand Sub Time Buckets ', 'string', falseTrue, 'False', 1, 0, 'Sub buckets of Time Buckets will be visible in report.', None, 1],
                 ['snapshot', 'Sheet Snapshot', 'string', falseTrue, 'True', 1, 0, \
                  'Create a snapshot of a report', self.snapshotCB, 1],
                 ['multiThread', 'Run in background', 'string', falseTrue, 'True', 1, 0, \
                  'Start the reporting in a separate thread', None, 0],
                 ['numberOfReports', 'Number of Reports', 'int', None, '5', 1, 0, \
                  'The number of reports that will be created before the script is completed', None, 0],
                 ['updateInterval', 'Update Interval (sec)', 'int', None, '60', 1, 0, \
                  'The update interval, in seconds, between the reports', None, 0]
               ]
                
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)        
        
        #add other tabs
        global allSheetSettingsBySheetType
        
        self.extend(FAddContentTab.getAelVariablesWithCB(self.on_query_name_changes))
        self.extend(FOutputSettingsTab.getAelVariables())
        self.extend(FAdvancedSettingsTab.getAelVariables())
        self.extend(FPostProcessingTab.getAelVariables())
        sheetSettingsVariables, allSheetSettingsBySheetType = FReportSheetSettingsTab.getAelVariables( [ 'FPortfolioSheet', 'FTradeSheet' ], acm.GetDefaultContext(), acm.CreateEBTag()) 
        for guiVariables in sheetSettingsVariables:
            self.extend(guiVariables) 
           
        
ael_gui_parameters = {
    'windowCaption':__name__,
    'helpFileIndex':1132
    }

ael_variables = WorksheetReport()
ael_variables.LoadDefaultValues(__name__)

def ael_main(variableDictionary):
    params=FReportUtils.adjust_parameters(variableDictionary)
    variableDictionary[ 'allSheetSettingsBySheetType' ] = allSheetSettingsBySheetType
    report_params = FReportAPI.FWorksheetReportGuiParameters( guiParams=params )
    report_params.RunScript()
    
    
