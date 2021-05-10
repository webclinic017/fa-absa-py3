""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionCalculatePositions.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionCalculatePositions - GUI Module to calculate corporate action 
    positions.          

DESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FBDPGui
import FBDPCurrentContext
import FBDPCommon


from FBDPRollback import RollbackWrapper
from FCorpActionElectionController import ElectionController
from FCorpActionInstrumentExclusion import ExclusionListUpdater
from FCorpActionBoxPosition import FCorpActionBoxPosition
from FTransactionHandler import RollbackHandler
from FBDPCurrentContext import Logme, Summary

corpact_tt = ('The corporate actions to calculate positions for.')
calculate_box_tt = ('Should the box position be calculated/updated?')

ael_variables = FBDPGui.TestVariables(
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['CorpActions',
                 'Corporate Actions',
                 'FCorporateAction', None, None,
                 1, 1, corpact_tt, None],
                ['CalcBox',
                'Calculate Box Position',
                'int', ['1', '0'], 1,
                0, 0, calculate_box_tt],
)


def ael_main(dictionary):

    """
    Main function
    """
    FBDPCurrentContext.CreateLog('Corporate action position calculator',
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    
    
    dictionary['ScriptName'] = 'Corporate action position calculator'
    FBDPCommon.execute_script(perform, dictionary)


def perform(dictionary):
    corpActions = dictionary['CorpActions']
    calcBox = dictionary['CalcBox'] if 'CalcBox' in dictionary else 0
    if not corpActions:
        Logme()('Corporate actions must be defined to calculate positions.', 'ERROR')
        return False
    positionSpec = FBDPCommon.positionSpecFromFParameter('FCAVariables', 'PositionSpec')
    if not positionSpec:
        Logme()('Position specification must be defined to calculate positions.', 'ERROR')
        return False
    logName = 'FCorpActionCalculatePositions'
    rollback = RollbackWrapper(logName, bool(dictionary['Testmode']))
    for action in corpActions:
        if calcBox > 0:
            boxCalc = FCorpActionBoxPosition(action, RollbackHandler(rollback))
            box = boxCalc.Calculate(positionSpec)
        controller = ElectionController(action, RollbackHandler(rollback))
        controller.FindCreateOrDeleteElections(positionSpec)
        updater = ExclusionListUpdater(action, RollbackHandler(rollback))
        updater.update()
    Summary().log(dictionary)
    Logme()(None, 'FINISH')
