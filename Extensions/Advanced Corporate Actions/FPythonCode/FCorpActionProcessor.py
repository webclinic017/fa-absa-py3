""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionProcessor.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionProcessor - Corporate action processor

DESCRIPTION

NOTE

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import FBDPCommon
from FCorpActionElectionController import ElectionController
from FCorpActionPositionProcessor import PositionProcessor
from FCorpActionInstrumentExclusion import ExclusionListUpdater
from FTransactionHandler import ACMHandler
from FCorpActionPayoutProcessor import CreateTemplateHelper


class CorpActionProcessor(object):

    def __init__(self, corpAction, transHandler=ACMHandler()):
        self._action = corpAction
        self._transHandler = transHandler
        self._templateHelper = CreateTemplateHelper(corpAction)

    def __SetCorporateActionStatus(self, ca, status):
        aelCAClone = FBDPCommon.acm_to_ael(ca).clone()
        aelCAClone.status = status
        with self._transHandler.Transaction():
            self._transHandler.Add(aelCAClone, ['status'])

    def Process(self):
        positionSpec = FBDPCommon.positionSpecFromFParameter(
                    'FCAVariables', 'PositionSpec')
        if not positionSpec:
            raise ValueError('No position spec')
        result = []
        controller = ElectionController(self._action, self._transHandler)
        caPositions = controller.FindCreateOrDeleteElections(positionSpec)
        updater = ExclusionListUpdater(self._action, self._transHandler)
        updater.update()
        self.__SetCorporateActionStatus(self._action, 'Active')
        processor = PositionProcessor(self._templateHelper, self._transHandler)
        result.extend(processor.Process(caPositions))
        self.__SetCorporateActionStatus(self._action, 'Processed')
        return result
