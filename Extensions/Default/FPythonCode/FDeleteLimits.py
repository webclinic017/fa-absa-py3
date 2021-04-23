""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/limits/bdp/delete/FDeleteLimits.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FDeleteLimits- Module which delete limits.

DESCRIPTION

----------------------------------------------------------------------------"""


import acm, ael
import FDeleteLimitsPerform
import FBDPCommon
import FBDPCustomSingleDlg
import FBDPGui
import importlib
importlib.reload(FBDPGui)


ScriptName = 'FDeleteLimits'
FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters', 
        ScriptName)

SrcArchiveStatus = 0
Date = None

def archiveStatusCb(index, field_values):
    global SrcArchiveStatus
    SrcArchiveStatus = 1 - int(field_values[index])
    changeDialog(field_values)
    

    return field_values

def dateCb(index, field_values):
    global Date
    Date = field_values[index]
    changeDialog(field_values)

    return field_values


# Tool tips
ttTestMode = 'No changes will be commited to the database.'
ttNonArchived = (
    'Delete non-archived limits only if selected. '
    'Otherwise only archived limits will be deleted.'
)
ttDate = ('Action will be performed on limits '
            'that are created on or before this date.')
ttLimits = 'Select limits.'
days = [
            acm.Time.DateToday(),
            'Today',
            'First of Month',
            'First of Quarter',
            'First of Year'
        ]

ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['NonArchived',
                'Delete non-archived', 'int', [0, 1], 0,
                1, False, ttNonArchived, archiveStatusCb, None],
        ['Date',
                'Not created after', 'string', days, 'Today',
                1, False, ttDate, dateCb, None],
        ['Limits',
                'Limits', 'FSymbol', None, None, 1, 1, ttLimits]
)


def changeDialog(field_values):
    global Date
    global SrcArchiveStatus
    # Limits ael variable
    limitsVariable = ael_variables[3]
    if SrcArchiveStatus == 0:
        acmDate = str(FBDPCommon.toDate(Date))
        limitsVariable[2] = 'FSymbol'
        limitsVariable[4] = getLimitInsertQuery(date = acmDate)
        limitsVariable[10] = None
    else:
        limitsVariable[2] = 'string'
        limitsVariable[4] = None
        limitsVariable[10] = customDialog

    return field_values


def getLimitInsertQuery(date):
    query = FBDPGui.insertLimits(
        greater_equal='', less_equal=date
    )
    return query


def customDialog(shell, dictionary):
    archivedLims = getArchivedLimits()
    cb = lambda: archivedLims.keys()
    customDlg = FBDPCustomSingleDlg.SelectItemCustomDialog(
        shell=shell, params=dictionary,
        selectionName='Limits',
        getObjectChoicesCb=cb
    )
    return customDlg.Create()


def _getAelDate(acmDate, name):
    if not acmDate or acmDate == '':
        raise Exception('Invalid date: %s' % (acmDate or None))

    aelDate = ael.date(acmDate).to_time()
    if aelDate > ael.date_today():
        raise Exception('Date cannot be in the future: %s' % acmDate)

    if name:
        Logme()('%s date: %s' % (name, str(acmDate)))

    return aelDate


def getArchivedLimits():
    acmDate = str(FBDPCommon.toDate(Date))
    date = _getAelDate(acmDate=acmDate, name=None)
    query = (
        'SELECT d.seqnbr FROM limit as d '
        'WHERE d.archive_status = 1'
    )
    docs = FBDPCommon.FBDPQuerySelection(
        name='Limits', query_expr=query,
        result_types=[ael.Limit]
    ).Run()
    archived_docs = {}
    for doc in docs:
        if (date is None) or (doc.creat_time <= date):
            archived_docs[str(doc.seqnbr)] = doc

    return archived_docs


def ael_main(dictionary):

    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPCurrentContext
    import FDeleteLimitsPerform
    importlib.reload(FDeleteLimitsPerform)
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    dictionary['ScriptName'] = ScriptName
    FBDPCommon.execute_script(FDeleteLimitsPerform.perform, dictionary)
