""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FProcessCorpActions.py"
"""----------------------------------------------------------------------------
MODULE
    FProcessCorpActions - Perform corporate action elections

DESCRIPTION

NOTE

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)

from FCorpActionProcessor import CorpActionProcessor
from FBDPRollback import RollbackWrapper
from FTransactionHandler import RollbackHandler
from FBDPCurrentContext import Summary, Logme, CreateLog

ScriptName = "FProcessCorpActions"

FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FProcessCorpActions')

ttCorpActions = "The corporate action records to process."


ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['CorpActions',
        'Corporate Actions',
        'FCorporateAction', None, None,
        1, 1, ttCorpActions, None, 1, None],
        )

def ael_main(dictionary):

    import FBDPCommon
    importlib.reload(FBDPCommon)

    CreateLog(ScriptName,
              dictionary['Logmode'],
              dictionary['LogToConsole'],
              dictionary['LogToFile'],
              dictionary['Logfile'],
              dictionary['SendReportByMail'],
              dictionary['MailList'],
              dictionary['ReportMessageType'])

    FBDPCommon.execute_script(perform, dictionary)


def perform(dictionary):
    corpActions = dictionary['CorpActions']
    for action in corpActions:
        Logme()('Processing corporate action {0}'.format(action.Name()))
        rollback = RollbackWrapper(action.Name(), 
                                bool(dictionary['Testmode']))
        processor = CorpActionProcessor(action, RollbackHandler(rollback))
        processor.Process()

    Summary().log(dictionary)
    Logme()(None, 'FINISH')
