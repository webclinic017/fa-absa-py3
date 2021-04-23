""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/scripts/FOperationsArchive.py"
import acm, ael
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOperationsPerformArchiving

import os
import re

from FAccountingEnums import JournalType

def CreateSettlementQuery():
    query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    op = query.AddOpNode('OR')
    op.AddAttrNode('Oid', 'EQUAL', None)
    op2 = query.AddOpNode('OR')
    op2.AddAttrNode('Status', 'EQUAL', None)
    op3 = query.AddOpNode('OR')
    op3.AddAttrNode('Trade.Oid', 'EQUAL', None)
    op4 = query.AddOpNode('OR')
    op4.AddAttrNode('ValueDay', 'EQUAL', None)
    op5 = query.AddOpNode('OR')
    op5.AddAttrNode('Currency.Name', 'EQUAL', None)
    op6 = query.AddOpNode('OR')
    op6.AddAttrNode('AcquirerName', 'EQUAL', None)
    op7 = query.AddOpNode('OR')
    op7.AddAttrNode('AcquirerAccName', 'EQUAL', None)
    op8 = query.AddOpNode('OR')
    op8.AddAttrNode('CounterpartyName', 'EQUAL', None)
    op9 = query.AddOpNode('OR')
    op9.AddAttrNode('CounterpartyAccName', 'EQUAL', None)

    return query

def CreateConfirmationQuery():
    query = acm.CreateFASQLQuery(acm.FConfirmation, 'AND')
    op = query.AddOpNode('OR')
    op.AddAttrNode('Oid', 'EQUAL', None)
    op2 = query.AddOpNode('OR')
    op2.AddAttrNode('Status', 'EQUAL', None)
    op3 = query.AddOpNode('OR')
    op3.AddAttrNode('Trade.Oid', 'EQUAL', None)
    op4 = query.AddOpNode('OR')
    op4.AddAttrNode('CreateTime', 'EQUAL', None)

    return query

def CreateJournalQuery():
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    op = query.AddOpNode('OR')
    op.AddAttrNode('JournalType', 'EQUAL', ael.enum_from_string('JournalType', JournalType.REVERSAL))
    op.AddAttrNode('JournalType', 'EQUAL', ael.enum_from_string('JournalType', JournalType.REVERSED))
    op.AddAttrNode('JournalType', 'EQUAL', ael.enum_from_string('JournalType', JournalType.PERIODIC_REVERSAL))
    op.AddAttrNode('JournalType', 'EQUAL', ael.enum_from_string('JournalType', JournalType.PERIODIC_REVERSED))
    op.AddAttrNode('JournalType', 'EQUAL', ael.enum_from_string('JournalType', JournalType.REALLOCATION_REVERSAL))
    op.AddAttrNode('JournalType', 'EQUAL', ael.enum_from_string('JournalType', JournalType.REALLOCATION_REVERSED))
    op2 = query.AddOpNode('OR')
    op2.AddAttrNode('JournalInformation.Trade.Instrument.InsType', 'EQUAL', None)
    op3 = query.AddOpNode('OR')
    op3.AddAttrNode('JournalInformation.Book.Name', 'EQUAL', None)
    op4 = query.AddOpNode('OR')
    op4.AddAttrNode('ValueDate', 'EQUAL', None)
    op5 = query.AddOpNode('OR')
    op5.AddAttrNode('JournalInformation.Trade.Oid', 'EQUAL', None)
    op6 = query.AddOpNode('OR')
    op6.AddAttrNode('JournalInformation.AccountingInstruction.Name', 'EQUAL', None)

    return query
#==============================================================================
# Main
#==============================================================================
dat_filevect = []
default_report_path = 'c:\\temp'
module = 'FOperationsArchive'
if os.path.exists(default_report_path):
    for name in os.listdir(default_report_path):
        if re.search("%s.*\.dat" % module, name, re.I):
            dat_filevect.append(os.path.normpath(
                                        os.path.join(default_report_path,
                                                     name)))

# ======== AEL variables setup - tool tips ====================================
ttSettlements = 'Settlement Selection'
ttConfirmations = 'Confirmation Selection'
ttJournals = 'Journal Selection'
ttRepPath = 'An execution report will be saved in this directory.'
ttLogReport = "Print an execution report in the AEL console."

ael_variables = FBDPGui.TestVariables(
['rollback', 'Enable Rollback', 'int', [1, 0], 1, 0, 0, 'Enables the creation of a rollback specification needed to execute the rollback script ', None, 1],
['settlements', 'Settlements to archive', 'FSettlement', None, CreateSettlementQuery(), 0, 1, ttSettlements],
['confirmations', 'Confirmations to archive', 'FConfirmation', None, CreateConfirmationQuery(), 0, 1, ttConfirmations],
['journals', 'Journals to archive', 'FJournal', None, CreateJournalQuery(), 0, 1, ttJournals],
['report_path', 'Report Directory Path_Logging', 'string', [], default_report_path, 0, 0, ttRepPath, None, 1],
['log_report', 'Log Report In Console_Logging', 'int', [1, 0], None, 0, 0, ttLogReport, None, 1]
)

def ael_main(dictionary):
    # Import Front modules.
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPCurrentContext
    importlib.reload(FBDPCurrentContext)

    title = "Operations Archiving"
    FBDPCurrentContext.CreateLog(title,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    FBDPCommon.execute_script(FOperationsPerformArchiving.PerformOperationsArchiving, dictionary)
