from __future__ import print_function
"""-------------------------------------------------------------------------------------------------------
MODULE
    FASQLReport - Produce a report based on the result of an ASQL query

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.
    (c) Copyright 2011-2008 by Sungard FRONT ARENA. All rights reserved.


DESCRIPTION

MAJOR REVISIONS
2005-03-28  Daniel R    Created
2006-10-16  Ralf J      Added support for ASQL-macros
2006-10-17  Ralf J      Added support for macro files
2006-10-20  Ralf J      Updated script to contain fix for SPR 263903 (included already in current PRIME versions)
2007-05-14  Richard L   Open a new GUI for the ASQL macros.
2008-05-01  Richard L   Use FRunScriptGUI
-------------------------------------------------------------------------------------------------------"""

import acm
import ael
import datetime
import os

import FReportAPI
import FReportUtils
import FXMLReportWriter

import FRunScriptGUI

import FMacroGUI
import FOutputSettingsTab
import FAdvancedSettingsTab
import FPostProcessingTab
import FDateTime
import FLogger

logger = FLogger.FLogger('FAReporting')
falseTrue = ['False', 'True']

def write_asql_to_xml(asqlres, writer, reportname, rowLabelColumns=None):
    """Write an ASQL result to an FXMLReportWriter

        asqlres   --  value as returned by ael.asql
        xmlwriter --  An FXMLReportWriter
    """
    try:
        columns, data = asqlres
    except:
        logger.ELOG( "ASQL query returned no rows, FASQLReport will be empty" )
        columns = []
        data = [[]]
    
    labelColumns = []
    if rowLabelColumns is not None:
        # Compute the indexes for the choosen columns
        for columnName in rowLabelColumns:
            index = -1
            try: # An numeric index 1...N?
                index = int(columnName) - 1
            except ValueError:
                # A column name?
                try:
                    index = columns.index(columnName)
                except ValueError:
                    pass
            if 0 <= index < len(columns):
                labelColumns.append(index)
     
    writer.PRIMEReport()
    writer.Name(reportname).done()
    writer.Type("ASQL Table").done()
    timestr = FDateTime.iso_utc_now()
    writer.Time(timestr).done()
    localtimestr = FDateTime.iso_utc_now_tz()
    writer.LocalTime(localtimestr).done()
    writer.ReportContents()
    writer.Table()
    writer.NumberOfColumns(len(columns)).done()
    xcolumns = writer.Columns()
    for colname in columns:
        xcolumn = writer.Column()
        writer.ColumnId(colname).done()
        writer.Label(colname).done()
        xcolumn.done()
    xcolumns.done()
    writer.Rows()
    for table in data:
        for i, row in enumerate(table, 1):
            xrow = writer.Row()
            if rowLabelColumns is None:
                writer.Label().done()
            elif len(labelColumns) == 0:
                writer.Label('Line%s'%(i,)).done()
            else:
                writer.Label('_'.join([str(row[columnIndex]) for columnIndex in labelColumns])).done()

            writer.RowType("ASQLResult").done()
            writer.Cells()
            for cell in row:
                xcell = writer.Cell()
                writer.RawData(cell).done()
                xcell.done()
            xrow.done()
    writer.done()

def make_xmlreportwriter(params):
    """Create a suitable FXMLREportWriter object for report output.

    Arguments:
        aelvardict -- dict from ael_variables should contain the values
                      from getAelVariables() in this module.
    """
    translationdict = {}
    #print (type(params),params)
    transdictfile = params.get('Translation Dictionary File', None)
    if transdictfile:
        translationdict = FDictionaryTranslator.FDictionaryTranslator( [transdictfile] )
    return FXMLReportWriter.FXMLReportWriter.make_iostring_writer(translationdict)

def fdict_to_pydict( fdict ):
    if isinstance(fdict, dict ):
        return fdict
    elif hasattr( fdict, 'Class' ):
        if fdict.IsKindOf('FDictionary'):
            pydict = {}
            for key in fdict.Keys():
                pydict[key] = fdict.At(key)
            return pydict
    else:
        raise TypeError( "Can't convert %s to %s" % (type(fdict), dict ) )

def validate_variables(params):
    """Validate variables used for FASQLReport"""
    if params['queryText'] and params['queryName']:
        raise Exception("Both Query text and Query name are specified, only one should be used")
    if not ( params['queryText'] or params['queryName'] ):
        raise Exception("Either Query text or Query name must be specified")
    params = fdict_to_pydict(params)
    return params
    
def get_query_text(query_name):
    """Retrieve the SQL text for a named query, RETURNS None if query not found"""
    #return acm.FSQL.Select('name="%s"'%query_name)[0]

    try:
        query_text=acm.FSQL.Select('name="%s"'%query_name)[0]
    except IndexError as msg:
        query_text = None
    return query_text.Text()#.AsString()

def perform_report(params, macros):
    """Perform report, params is a dictionary"""

    params = validate_variables(params)
    query_text = params['queryText']
    query_name = params['queryName']
    fname = params['File Name']
    labelRows = params['labelRows'] == 'True'
    rowLabelColumns = None
    if labelRows:
        rowLabelColumns = [name.strip() for name in params['labelColumns'].split(',') if name.strip()]

    if query_name:
        query_text = get_query_text(query_name)
        #print (type(query_text),query_text)
    mList = []
    mValue = []
    if macros:
        macs = FMacroGUI.searchMacros(query_text)
        mList, mValue = FMacroGUI.mapMacros(macros, macs)
    res = ael.asql(query_text, 0, mList, mValue)

    writer, strbuf = make_xmlreportwriter(params)
    write_asql_to_xml(res, writer, fname, rowLabelColumns=rowLabelColumns)
    xmltext = strbuf.getvalue()

    report = FReportAPI.FWorksheetReportApiParameters()

    report.snapshot = True
    #Output settings tab ------------------------
    FReportAPI.init_from_output_settings_tab(report, params)
    FReportAPI.init_from_advanced_settings_tab(report, params)
    FReportAPI.init_from_processing_tab(report, params)
    report.CreateReportByXml(xmltext)

class ASQLReport(FRunScriptGUI.AelVariablesHandler):
    """Retrieve the complete list of AEL variables used for FASQL report"""
    def on_query_name_changes(self, index, fieldvalues):
        """GUI Callback, triggered by user selecting a query in the 'query name' field-
        When the query name changes the macro fields will be reset and the macro names
        from the new query will be displayed."""

        if self.queryOld == fieldvalues[index]:
            changed = 'False'
        else:
            changed = 'True'

        macrolist=[]
        if changed == 'True':
            query_name = fieldvalues[index]
            self.queryOld = query_name
            if query_name:
                macro_variables=FMacroGUI.macro_gui(query_name, {})

                for i in macro_variables:
                    macrolist.append("%s=%s"%(i[0], i[4]))
                self.ael_variables[index + 1][3]=macrolist

            if macrolist:
                self.ael_variables[index + 1][9]="1"
                self.ael_variables[index + 2][9]="1"
            else:
                self.ael_variables[index + 1][9]="0"
                self.ael_variables[index + 2][9]="0"

        return fieldvalues
        
    def __init__(self):
        self.queryOld=''
        #workbooks = acm.FWorkbook.Select('createUser = ' + str(acm.FUser[acm.UserName()].Oid()))
        #templates = acm.FTradingSheetTemplate.Select('')
        queries = [query.Name() for query in acm.FSQL.Select('')]
        queries.sort()

        vars =[
               ['queryText', 'Query text', 'string', "",     None, 0, 0, 'Query text to be executed', None, 1],
               ['queryName', 'Query name', 'string', queries, None, 0, 0, 'Name of a query to run', self.on_query_name_changes, 1]
              ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)
        self.extend(FMacroGUI.getAelVariables(''))
        self.extend(FOutputSettingsTab.getAelVariables())
        self.extend(FPostProcessingTab.getAelVariables())
        
        advancedSettings = FAdvancedSettingsTab.getAelVariables()
        for var in advancedSettings:
            if var[0] in ['Include Raw Data', 'Include Full Data', 'Include Default Data', 'Include Formatted Data']:
                # Might need to add some entries to be able to set the 9:th.
                while len(var) < FRunScriptGUI.Controls.ENABLED + 1:
                    var.append(None)            
            
                # only data of one type is written
                if var[FRunScriptGUI.Controls.NAME] == 'Include Raw Data':
                    var[FRunScriptGUI.Controls.DEFAULT] = 'True'
                else:
                    var[FRunScriptGUI.Controls.DEFAULT] = 'False'
                
                # disable data type checkboxes
                var[FRunScriptGUI.Controls.ENABLED] = 0
        
        self.extend(advancedSettings)
        self.append(['labelRows', 'Set labels on rows in XML output_Advanced settings', 'string', ('False', 'True'), 'False', 1, 0,
                     'Should the rows in the XML output have labels with names', None, 1])

        self.append(['labelColumns', 'Columns to use as labels_Advanced settings', 'string', "",  "", 0, 0,
                     'Name the columns to use in the row labels', None, 1])
 
def ael_main(params):
    params=FReportUtils.adjust_parameters(params)

    validate_variables(params)
    macros={}
    if params['macros']:
        FMacroGUI.split_macrostring(params['macros'], macros)

    # FMacroGUI.start_macro_gui will show gui depending on params['useMacroGUI']
    FMacroGUI.start_macro_gui(params, params['queryName'], macros, perform_report, block_rerun=True)

ael_gui_parameters = {
    'windowCaption':'FASQLReport',
    'helpFileIndex':1127
    }
ael_variables=ASQLReport()

