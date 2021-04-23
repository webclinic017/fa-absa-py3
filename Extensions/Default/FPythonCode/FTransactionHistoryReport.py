from __future__ import print_function
"""-------------------------------------------------------------------------------------------------------
MODULE
    FTransactionHistoryReport - Creates a sheet report from a selection of FTransactionHistory objects

    (c) Copyright 2011 by Sungard FRONT ARENA. All rights reserved.

DESCRIPTION

    The report created is hierarchial with the FTransactionHistory objects as top level rows and the
    attributes of the changed entities as child rows. 

-------------------------------------------------------------------------------------------------------"""

import acm
import ael
import datetime
import os
import uuid

import FReportAPI
import FReportUtils
import FXMLReportWriter

import FRunScriptGUI

import FOutputSettingsTab
import FAdvancedSettingsTab
import FPostProcessingTab
import FDateTime
import FLogger

falseTrue = ['False', 'True']
includeFormattedDataIndex = 0
includeRawDataIndex = 1
includeFullDataIndex = 2
includeDefaultDataIndex = 3

logger = FLogger.FLogger('FAReporting')

class FExtendedXMLReportWriter(FXMLReportWriter.FXMLReportWriter):
    def __init__(self, outputhandler, schema=None, translatedict={}):
        FXMLReportWriter.FXMLReportWriter.__init__(self, outputhandler, schema, translatedict)

reportelems = """RowId ChildReports ChildReport ChildReportId"""

# Add all extended Report elements onto FExtendedXMLReportWriter class
for elemname in reportelems.split(" "):
    elemname = elemname.strip()
    setattr(FExtendedXMLReportWriter, elemname, FXMLReportWriter._ElementDescriptor(elemname))
    
def create_uuid():
    return str(uuid.uuid4())
    
def add_cell_value(writer, val):
    try:
        writer.RawData(val).done()
    except AttributeError as ex:
        print (ex)
        writer.RawData(str(ex)).done()

def add_child_report_row(writer, label, type, values):
    xrow = writer.Row()
    writer.Label(label).done()
    writer.RowType(type).done()
    xcells = writer.Cells()
    for v in values:
        val = v
        if val is None:
            val = ""
        xcell = writer.Cell()
        add_cell_value(writer, val)
        xcell.done()
    xcells.done()
    return xrow

def add_child_report_msg(writer, msg, onlyChanges, appendId):
    msgType = str(msg.Type())
    operation = ""
    overrideOnlyChanges = False
    if msgType[0] == '!':
        operation = "Update"
        msgType = msgType[1:]
    elif msgType[0] == '+':
        operation = "Create"
        msgType = msgType[1:]
        overrideOnlyChanges = True
    elif msgType[0] == '-':
        operation = "Delete"
        msgType = msgType[1:]

    if onlyChanges and len(operation) == 0:
        return;

    if appendId:
        try:
            e = ael.enum_to_string("B92RecordType", ael.enum_from_string("B92RecordType", msgType))
            table = getattr(ael, e)
            seqnbrKey = None
            idKey = None
            for (name, keyType, fields) in table.keys():
                if not seqnbrKey and keyType == "primary":
                    seqnbrKey = fields[0]
                elif not idKey and keyType == "unique" and len(fields) == 1:
                    idKey = fields[0]
                if seqnbrKey and idKey:
                    break
            theKey = acm.FSymbol(idKey.upper()) if idKey else (acm.FSymbol(seqnbrKey.upper()) if seqnbrKey else None)
            if theKey and msg.HasKey(theKey):
                keyValue = msg.At(theKey)
                if keyValue:
                    if idKey:
                        keyValue = "'" + keyValue + "'"
                    msgType += " " + keyValue
        except Exception as e:
            logger.ELOG( "Could not get record id from " + msgType + ". " + str(e))

    xrow = add_child_report_row(writer, msgType, "Type", [operation, None, None, None])
    
    xrowsAttribs = writer.Rows()
    
    for attrib in msg.Keys().Sort():
        if attrib and len(attrib) > 0 and not attrib[0] == '!':
            operation = ""
            
            # For now, just show N/A for textobject blobs. Could be handled by XSLT to
            # insert as child table (or two multiline fields?) to DATA row. Table with two columns, current and old value
            if msgType == 'TEXTOBJECT' and str(attrib) == 'DATA':
                newVal = "N/A"
                oldVal = None
                if msg.HasKey(acm.FSymbol('!' + str(attrib))):
                    operation = "Update"
                    oldVal = "N/A"
            else:
                newVal = msg.At(attrib)
                oldVal = msg.At('!' + str(attrib))
                if oldVal is not None:
                    operation = "Update"
                
            if overrideOnlyChanges or not onlyChanges or len(operation) > 0:
                add_child_report_row(writer, "", "Attribute", [operation, attrib, newVal, oldVal]).done()

    for childMsg in msg.Messages():
        add_child_report_msg(writer, childMsg, onlyChanges, appendId)

    xrowsAttribs.done()
    xrow.done()

def add_child_report(writer, reportId, dataMsg, onlyChanges, appendId):
    xchildReport = writer.ChildReport()
    writer.ChildReportId(reportId).done()
    writer.PRIMEReport()
    writer.Name("").done()
    writer.Type("Child Report").done()
    writer.ReportContents()
    writer.Table()
    columns = ["Operation", "Attribute", "Current", "Previous"]
    writer.NumberOfColumns(len(columns)).done()
    xcolumns = writer.Columns()
    for colname in columns:
        xcolumn = writer.Column()
        writer.ColumnId(colname).done()
        writer.Label(colname).done()
        xcolumn.done()
    xcolumns.done()
    xrows = writer.Rows()
    for msg in dataMsg.Messages():
        add_child_report_msg(writer, msg, onlyChanges, appendId)
    xchildReport.done()
    
def write_to_xml(params, ths, writer):
    """Write all transaction history objects to an FXMLReportWriter
    """
    
    if len(ths):
        gen = acm.FAMBAMessageGenerator()
        gen.ShowAll(True)
        gen.ShowChanges(True)
        msg = gen.GenerateTransactionHistory(ths[0])
        thmsg = msg.Messages()[0]
        columns = thmsg.Keys()
    else:
        logger.ELOG( "Stored ASQL query returned no items, FTransactionhistoryReport will be empty" )
        columns = []
        gen = None
    
    dataMessages = {}
    
    fname = params['File Name']
    reportname = os.path.split(fname)[0]
    
    writer.PRIMEReport()
    writer.Name(reportname).done()
    writer.Type("Transaction History Report").done()
    timestr = FDateTime.iso_utc_now()
    writer.Time(timestr).done()
    localtimestr = FDateTime.iso_utc_now_tz()
    writer.LocalTime(localtimestr).done()
    writer.ReportContents()
    xtable = writer.Table()
    writer.NumberOfColumns(len(columns)).done()
    xcolumns = writer.Columns()
    for colname in columns:
        xcolumn = writer.Column()
        writer.ColumnId(colname).done()
        writer.Label(colname).done()
        xcolumn.done()
    xcolumns.done()
    xrows = writer.Rows()
    for th in ths:
        xrow = writer.Row()
        writer.Label().done()
        rowUuid = create_uuid()
        writer.RowId(rowUuid).done()
        writer.RowType("TransactionHistory").done()
        xcells = writer.Cells()
        msg = gen.GenerateTransactionHistory(th)
        thmsg = msg.Messages()[0]
        
        #store data message for row for later processing
        dataMsgs = thmsg.FindMessages("DATA")
        if dataMsgs and dataMsgs.Size():
            dataMessages[rowUuid] = dataMsgs[0]
        
        for colname in columns:
            cell = thmsg.At(colname)
            if cell is None:
                cell = ""
            xcell = writer.Cell()
            add_cell_value(writer, cell)
            xcell.done()
        xcells.done()    
        xrow.done()
    xrows.done()
    xtable.done()
    
    if len(dataMessages) > 0:
        onlyChanges = falseTrue.index(params['onlyChanges'])
        appendId = falseTrue.index(params['appendId'])
        writer.ChildReports()
        for key in dataMessages.keys():
            add_child_report(writer, key, dataMessages[key], onlyChanges, appendId)
    
    writer.done()

def make_xmlreportwriter(params):
    """Create a suitable FExtendedXMLReportWriter object for report output.

    Arguments:
        aelvardict -- dict from ael_variables should contain the values
                      from getAelVariables() in this module.
    """
    translationdict = {}
    #print (type(params),params)
    transdictfile = params.get('Translation Dictionary File', None)
    if transdictfile:
        translationdict = FDictionaryTranslator.FDictionaryTranslator( [transdictfile] )
        
    return FExtendedXMLReportWriter.make_iostring_writer(translationdict)

def validate_variables(params):
    """Validate variables used for FTransactionHistoryReport"""
    if not params['queryName']:
        raise Exception("Query name must be specified")
    if not (falseTrue.index(params['Include Raw Data']) or falseTrue.index(params['Include Formatted Data']) or \
            falseTrue.index(params['Include Full Data']) or falseTrue.index(params['Include Default Data'])):
        raise Exception("At least one of Include Formatted Data, Include Raw Data, Include Full Data or Include Default Data must be selected")
        
def get_ths(params):
    """Retrieve the Transaction Histories found with query"""

    queryName = params['queryName']
    try:
        storedQuery = acm.FStoredASQLQuery.Select('name="%s"' % queryName)[0]
        return storedQuery.Query().Select().Sort()
    except:
        raise Exception("Exception when retrieving transaction history's from stored query")
    return None

def perform_report(params):
    """Perform report, params is a dictionary"""

    validate_variables(params)
    res = get_ths(params)

    writer, strbuf = make_xmlreportwriter(params)
    write_to_xml(params, res, writer)
    xmltext = strbuf.getvalue()

    report = FReportAPI.FWorksheetReportApiParameters()

    report.snapshot = True
    FReportAPI.init_from_output_settings_tab(report, params)
    FReportAPI.init_from_advanced_settings_tab(report, params)
    FReportAPI.init_from_processing_tab(report, params)
    report.CreateReportByXml(xmltext)

class TransactionHistoryReport(FRunScriptGUI.AelVariablesHandler):
    """Retrieve the complete list of AEL variables used for FASQL report"""
    def __init__(self):
        self.queryOld=''
        allQueries = acm.FStoredASQLQuery.Select('')
        queries = []
        for q in allQueries:
            try:
                if q.QueryClass() == acm.FTransactionHistory:
                    queries.append(q.Name())
            except:
                pass
        queries.sort()

        vars =[
               ['queryName', 'Query Name', 'string', queries, None, 1, 0, 'Name of a stored query', None, 1],
               ['onlyChanges', 'Include Only Changes', 'string', falseTrue, 'True', 1, 0, 'If checked only changes are included', None, 1],
               ['appendId', 'Show Record Id', 'string', falseTrue, 'False', 1, 0, 'If checked record id is appended to table name', None, 1]
              ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)
        self.extend(FOutputSettingsTab.getAelVariables())
        self.extend(FPostProcessingTab.getAelVariables())
        
        advancedSettings = FAdvancedSettingsTab.getAelVariables()
        for var in advancedSettings:
            if var[0] in ['Include Raw Data', 'Include Full Data', 'Include Default Data', 'Include Formatted Data']:
                checked = 'False'
                
                # only data of one type is written
                if (var[0] == 'Include Raw Data'):
                    checked = 'True'
                var[4] = checked
                
                # disable data type checkboxes, they all have descriptions, fill with default values to enable value if any is not set
                if len(var) == 8:
                    var.append(None)
                if len(var) == 9:
                    var.append(0)
                elif len(var) >= 10:
                    var[9] = 0
        self.extend(advancedSettings)

def ael_main(params):
    params = FReportUtils.adjust_parameters(params)

    validate_variables(params)
    perform_report(params)

ael_gui_parameters = {
    'windowCaption':'FTransactionHistoryReport',
    'helpFileIndex':1150
    }

ael_variables = TransactionHistoryReport()
