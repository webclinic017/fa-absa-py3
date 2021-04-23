""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/aggr_arch/etc/faggregation.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FAggregation - Perform aggregation

DESCRIPTION
        This module perform trade aggregation in a ARENA Database. It reads
        configuration information from the AggregationSpec and AggregationRule
        tables and the aggregation rules must have been set up before the
        aggregation can be performed.

NOTE
    The module uses the aggregation rules set up in the PRIME Explorer, BDP,
    Aggregation Rules.

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import os


import acm


import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FAggruleSelectItem


# Name of this script used in START, STOP and FINISH messages:
ScriptName = 'Trade Aggregation'


ttLog = ("Log real time information during the aggregation process to the "
        "prime log. The amount of logging will be determined by Logmode.")
ttRule = ("If set, only run the set of aggregation rules defined by these "
        "trade filters. If not set, all aggregation rules will be used.")
ttPnLTest = ("Compare Profit and Loss Values for the aggregated positions "
        "before and after aggregation.")
ttRepPath = ("Log the result of Profit and Loss Comparison Test to this "
        "directory.")
ttLogRep = "Log the result of Profit and Loss Comparison Test to the Console."
ttContext = "The context to be used for the Diff Test."
ttWorkbook = ("The columns to be compared are taken from the selected "
        "workbook. If no workbook is specified, default columns will be used.")
ttSheet = ("The union of the columns in the selected portfolio sheets will "
        "be used in the comparison. ")
ttSheet_inactive = "A workbook has to be selected to use this field. "
ttNoDiffTest = ("Run Profit and Loss Comparison Test must be selected to "
        "use this field.")
ttbypassTradeValidation = ("Select this check box to perform batch updating "
    "while archiving/de-archiving trades. FValidation and FBDPHook will "
    "not be called. This will reduce the trade aggregation processing time.")
ttIgnorePrecision = ("Ignore the Precision when running the Profit and Loss "
    "Comparison Test. ")
ttAbsolutePrecision = ("The absolute precision when running the Profit "
    "and Loss Comparison Test. ")
ttRelativePrecision = ("The relative precision when running the Profit "
    "and Loss Comparison Test. ")

default_report_path = os.path.join(FBDPGui.defaultLogDir(),
        "Trade Aggregation")

def diff_test_cb(index, fieldValues):
    enable = fieldValues[index] != '0'
    ael_variables.used_context.enable(enable, ttNoDiffTest)
    ael_variables.workbook.enable(enable, ttNoDiffTest)
    ael_variables.sheet_names.enable(enable, ttNoDiffTest)
    ael_variables.report_path.enable(enable, ttNoDiffTest)
    ael_variables.ignore_precision.enable(enable, ttNoDiffTest)
    ael_variables.absolute_precision.enable(enable, ttNoDiffTest)
    ael_variables.relative_precision.enable(enable, ttNoDiffTest)

    fieldValues = ael_variables.workbook.callbackIfEnabled(fieldValues)
    return fieldValues


def wb_cb(index, fieldValues):
    workbookNames = fieldValues[index].split(',')
    for wbName in workbookNames:
        wb = acm.FWorkbook[wbName]
        ael_variables.sheet_names.enable(wb, ttSheet_inactive)
        if wb:
            sheets = [s.SheetName() for s in wb.Sheets() if
                    s.IsKindOf('FPortfolioSheet')]
            ael_variables.sheet_names[3] = sheets
            fieldValues[ael_variables.sheet_names.sequenceNumber] = ",".join(
                    sheets)
        else:
            fieldValues[ael_variables.sheet_names.sequenceNumber] = ""
    return fieldValues


def contexts():
    contextList = [""]
    for c in acm.Contexts(''):
        contextList.append(c)
    contextList.sort()
    return contextList


def get_default_context():
    contextList = contexts()
    if "Standard" in contextList:
        return "Standard"
    else:
        return contextList[0]

workbooks = acm.FWorkbook.Select('createUser = {0}'.format(
        acm.FUser[acm.UserName()].Oid()))


def customDialog(shell, params):
    customDlg = FAggruleSelectItem.SelectAggrulesCustomDialog(params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


ael_variables = FBDPGui.LogVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['date',
                'Date_Aggregation',
                'string', [acm.Time.DateToday(), 'Today'], 'Today',
                0, 0],
        ['aggrule_filters',
                'Aggregation filters_Aggregation',
                'int', [], '',
                0, 1, ttRule, None, 1, customDialog],
        ['diff_test',
                'Run Profit and Loss Comparison Test_Test',
                'int', [1, 0], 0,
                1, 0, ttPnLTest, diff_test_cb],
        ['bypassTradeValidation',
                'Use batch updates_Aggregation',
                'int', [1, 0], 0,
                0, 0, ttbypassTradeValidation, None, None],
        ['ignore_precision',
                'Ignore Precision_Test',
                'int', [1, 0], 0,
                1, 0, ttIgnorePrecision, 1],
        ['absolute_precision',
                'Absolute Precision_Test',
                'string', None, "0.0001",
                0, 0, ttAbsolutePrecision, 1],
        ['relative_precision',
                'Relate Precision_Test',
                'string', None, "0.0001",
                0, 0, ttRelativePrecision, 1],
        ['used_context',
                'Context_Test',
                'string', contexts(), get_default_context(),
                0, 0, ttContext, None, 1],
        ['workbook',
                'Workbook_Test',
                'FWorkbook', workbooks, None,
                0, 2, ttWorkbook, wb_cb, 1],
        ['sheet_names',
                'Portfolio Sheets_Test',
                'string', [], None,
                0, 1, ttSheet, None, 1],
        ['report_path',
                'Output File Path_Test',
                'string', [], default_report_path,
                0, 0, ttRepPath, None, 1])


def ael_main(dictionary):
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FAggregatePerform
    importlib.reload(FAggregatePerform)

    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    sheets = []
    for name in dictionary['sheet_names']:
        for wb in dictionary['workbook']:
            for s in wb.Sheets():
                if s.IsKindOf('FPortfolioSheet') and s.SheetName() == name:
                    sheets.append(s)
                    break

    dictionary['sheet_templates'] = sheets

    FBDPCommon.execute_script(FAggregatePerform.perform_aggregation,
            dictionary)
