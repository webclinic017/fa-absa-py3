""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/reconciliation_documents/etc/FReconciliationDocuments.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""---------------------------------------------------------------------------
MODULE
    FReconciliationDocuments -
        Reconciliation documents tasks GUI base implementation

DESCRIPTION

NOTE

ENDDESCRIPTION
---------------------------------------------------------------------------"""
import sys

import acm
import ael

import FBDPCustomSingleDlg
import FBDPGui
import FBDPCommon
import FReconciliationDocumentsPerform
import importlib

global ael_vars
ael_vars = None

def init(script_name, ael_variables_to_prepend):
    #Setup GUI with default parameters
    FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters(
        'FBDPParameters', script_name
    )
    ael_v = Gui(
        script_name=script_name,
        ael_variables_to_prepend=ael_variables_to_prepend
    )
    setattr(sys.modules[__name__], 'ael_vars', ael_v)
    return ael_v

class Gui(FBDPGui.TestVariables):
    def __init__(self, script_name, ael_variables_to_prepend):
        #Setup intended AEL variables
        if isinstance(ael_variables_to_prepend, (list, set)):
            ael_variables_to_prepend = tuple(ael_variables_to_prepend)

        assert isinstance(ael_variables_to_prepend, tuple)
        #Tooltips
        ttDate = (
            'Action will be performed on reconciliation documents '
            'that we created on or before this date.'
        )
        ttDocs = 'Select reconciliation documents.'
        days = [
            acm.Time.DateToday(),
            'Today',
            'First of Month',
            'First of Quarter',
            'First of Year'
        ]
        variables = ael_variables_to_prepend + (
            # [VariableName,
            #       DisplayName,
            #       Type, CandidateValues, Default,
            #       Mandatory, Multiple, Description, InputHook, Enabled, Dialog]
            ['Date',
                'Not created after',
                'string', days, 'Today',
                True, False, ttDate, self.dateCb, True, None],
            ['Documents',
                'Reconciliation Documents',
                'string', None, None,
                True, True, ttDocs, None, None, self.customDialog],
        )
        super(Gui, self).__init__(*variables)
        self.script_name = script_name
        self.src_archive_status = 0
        self.date = None

    def changeDialog(self, field_values):
        # Reset selection options according and empty field values
        doc_var = getattr(self, 'Documents')
        if self.src_archive_status == 0:
            acm_date = str(FBDPCommon.toDate(self.date))
            doc_var[2] = acm.FReconciliationDocument
            doc_var[4] = self.getRecDocsInsertQuery(date=acm_date)
            doc_var[10] = None
        else:
            doc_var[2] = 'string'
            doc_var[4] = None
            doc_var[10] = self.customDialog

        return field_values

    def getRecDocsInsertQuery(self, date):
        query = FBDPGui.insertReconciliationDoc(
            greater_equal='', less_equal=date
        )
        return query

    def customDialog(self, shell, params):
        archived_docs = self.getArchivedDocuments()
        cb = lambda: archived_docs.keys()
        customDlg = FBDPCustomSingleDlg.SelectItemCustomDialog(
            shell=shell, params=params,
            selectionName='reconciliation documents',
            getObjectChoicesCb=cb
        )
        return customDlg.Create()

    def getArchivedDocuments(self):
        acm_date = str(FBDPCommon.toDate(self.date))
        date = FReconciliationDocumentsPerform._getAelDate(
            acm_date=acm_date, name=None
        )
        query = (
            'SELECT d.seqnbr FROM reconciliation_document as d '
            'WHERE d.archive_status = 1'
        )
        docs = FBDPCommon.FBDPQuerySelection(
            name='Reconciliation Documents', query_expr=query,
            result_types=[ael.ReconciliationDocument]
        ).Run()
        archived_docs = {}
        for doc in docs:
            if (date is None) or (doc.creat_time <= date):
                archived_docs[str(doc.seqnbr)] = doc

        return archived_docs

    def dateCb(self, index, field_values):
        self.date = field_values[index]
        return self.changeDialog(field_values=field_values)

def aelMain(performer_module, params):
    params['ScriptName'] = ael_vars.script_name
    get_oid = lambda obj: obj.Oid() if hasattr(obj, 'Oid') else int(obj)
    get_rec = lambda obj: ael.ReconciliationDocument[get_oid(obj=obj)]
    check = lambda obj: obj.archive_status == ael_vars.src_archive_status
    docs = [get_rec(obj) for obj in params['Documents']]
    params['Documents'] = [obj for obj in docs if check(obj=obj)]

    #Import Front modules
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPCurrentContext

    #Create logger
    FBDPCurrentContext.CreateLog(
        ScriptName=ael_vars.script_name,
        LogMode=params['Logmode'],
        LogToConsole=params['LogToConsole'],
        LogToFile=params['LogToFile'],
        Logfile=params['Logfile'],
        SendReportByMail=params['SendReportByMail'],
        MailList=params['MailList'],
        ReportMessageType=params['ReportMessageType']
    )
    #Execute relevant perform script
    FBDPCommon.execute_script(performer_module.perform, params)
