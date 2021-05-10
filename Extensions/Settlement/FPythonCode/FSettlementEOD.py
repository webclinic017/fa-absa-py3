""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementEOD.py"
"""----------------------------------------------------------------------------
MODULE
    FSettlementEOD - Module which executes the End of Day script for settlements

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module executes the night update of the Settlement table. It
    populates and updates the Settlement table with data from the trade,
    cashflow, payment, account, dividend, reset, party, settle instruction,
    instrument and netting rule tables.

DATA-PREP

REFERENCES
    See modules FSettlementUtils
----------------------------------------------------------------------------"""

import FRunScriptGUI
import FOperationsUtils as Utils

from FOperationsLoggers import CreateLogger

from FSettlementTradeFilter import SettlementEODTradeFilterHandler
from FSettlementEODUtils import EODProcessSelector, EODParameters, RunEODSteps
from FSettlementNettingRuleQueryCache import SettlementNettingRuleQueryCache

def eod_start(dictionary, logger):

    eod_run = dictionary['eod_run']
    ack_to_pc = dictionary['ack_to_pc']
    exclude_post_sec = dictionary['exclude_post_sec']
    create_offsetting_settlements = dictionary['create_offsetting_settlements']
    handle_redemption_securities = dictionary['handle_redemption_securities']

    eodTradeFilterHandler = SettlementEODTradeFilterHandler()
    eodProcessSelector = EODProcessSelector(eodTradeFilterHandler)
    eodParameters = EODParameters(eod_run, ack_to_pc, exclude_post_sec,
                                  True, create_offsetting_settlements, handle_redemption_securities, 7, 'Settlement End of Day Procedure')
    nettingRuleQueryCache = SettlementNettingRuleQueryCache()
    RunEODSteps(eodProcessSelector, eodParameters, nettingRuleQueryCache, logger)

class SettlementEODGUI(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):
        variables = self.__CreateAelVariables()
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)

    def __CreateAelVariables(self):
        ttEODRun = "Generate settlements for trades."
        ttPostToPc = "This option will change the statuses of all Acknowledged settlements to Pending Closure."
        ttExcludePostSec = "This option will prevent Acknowledged security settlements from having their statuses set to Pending Closure."
        ttCreateOffsettingSettlements = "This option will create offsetting settlements and transfers for not fully settled trades."
        ttSettleRedemptionSettlements = "This option will settle Redemption Security settlements if the trade is settled"
        
        return [('eod_run', 'Run End Of Day procedure', 'bool', [False, True], True, True, False, ttEODRun),
                ('ack_to_pc', 'Set Acknowledged settlements to Pending Closure', 'bool', [False, True], True, True, False, ttPostToPc, self.__OnPostToPendingClosure),
                ('exclude_post_sec', 'Exclude Acknowledged security settlements', 'bool', [False, True], False, True, False, ttExcludePostSec),
                ('create_offsetting_settlements', 'Create offsetting settlements', 'bool', [False, True], False, True, False, ttCreateOffsettingSettlements),
                ('handle_redemption_securities', 'Settle applicable Redemption Security settlements', 'bool', [False, True], False, True, False, ttSettleRedemptionSettlements)]

    def __OnPostToPendingClosure(self, index, fieldValues):
        postToPC = fieldValues[index]
        if postToPC == "true":
            self.exclude_post_sec.enable(True)
        else:
            self.exclude_post_sec.enable(False)
        return fieldValues

def ael_main(params):
    import FSettlementParameters as Params
    try:
        Utils.InitFromParameters(Params)
        logger = CreateLogger(True, False, Params.detailedLogging, "", "")
        pr = '<< End of Day - %s >>' % (__file__)
        logger.LP_Log(pr)
        logger.LP_Flush()
        eod_start(params, logger)
    except Exception as e:
        logger.LP_Log("FSettlementEOD could not be completed: %s" % e)
        logger.LP_Flush()


ael_gui_parameters = {
    'runButtonLabel' : 'Run',
    'hideExtraControls' : False,
    'windowCaption' : 'FSettlementEOD',
    'version' : '%R%'
    }

ael_variables = SettlementEODGUI()

