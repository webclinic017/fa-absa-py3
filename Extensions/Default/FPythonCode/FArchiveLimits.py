""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/limits/bdp/archive/FArchiveLimits.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FArchiveLimits- Module which archive limits.

DESCRIPTION

----------------------------------------------------------------------------"""


import acm, ael
import FArchiveLimitsPerform
import FBDPCommon
import FBDPCustomSingleDlg
import FBDPGui
import importlib
importlib.reload(FBDPGui)


ScriptName = 'FArchiveLimits'
FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters', 
        ScriptName)

SrcArchiveStatus = 0
Date = None


def archiveStatusCb(index, field_values):
    global SrcArchiveStatus
    SrcArchiveStatus = int(field_values[index])
    changeDialog(field_values)
    

    return field_values


def dateCb(index, field_values):
    global Date
    Date = field_values[index]
    changeDialog(field_values)

    return field_values


# Tool tips
ttTestMode = 'No changes will be commited to the database.'
ttDearchive = 'Select to dearchive limits.'
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
        ['Dearchive',
                'De-archive', 'int', [0, 1], 0,
                1, False, ttDearchive, archiveStatusCb, None],
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
    archivedDocs = getArchivedLimits()
    cb = lambda: archivedDocs.keys()
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
    import FArchiveLimitsPerform
    importlib.reload(FArchiveLimitsPerform)
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    dictionary['ScriptName'] = ScriptName
    FBDPCommon.execute_script(FArchiveLimitsPerform.perform, dictionary)
