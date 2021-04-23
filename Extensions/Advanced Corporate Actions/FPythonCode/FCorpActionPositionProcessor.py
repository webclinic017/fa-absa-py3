""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionPositionProcessor.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionPositionProcessor - Module which processes corporate action positions

DESCRIPTION


ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme


import FBDPCommon
import FCorpActionUtils

from FCorpActionElectionPosition import PositionCalculator
from FCorpActionPayoutProcessor import ProcessPayouts
from FCorpActionPositionLinkHelper import PositionLinkHelper
from FCorpActionUtils import GetBusinessEventForElection, \
                             validateBusinessProcessTransition, \
                             getBusinessProcessAndEvent
from FTransactionHandler import ACMHandler
try:
    from FBDPHook import should_process_instrument
except:
    should_process_instrument = None

__all__ = ['PositionProcessor']


class PositionProcessor(object):

    def __init__(self, templateHelper, transHandler=ACMHandler()):
        self._templateHelper = templateHelper
        self._transHandler = transHandler
        
    def Process(self, caPositions):
        Logme()('Position Processor: Process')
        result = []
        for caPosition in caPositions:
            if caPosition:
                result.extend(self._ProcessPosition(caPosition))
        return result

    def _UpdateRollbackSpecAddInfo(self, caPosition):
        additionalInfo = FBDPCommon.SetAdditionalInfoValue(caPosition,
                                                           'CorpActionElection', 
                                                           'RollbackElection', 
                                                            self._transHandler.Name())
        self._transHandler.Add(additionalInfo)
                        
    def _IsProcessed(self, caPosition):
        businessEvent = GetBusinessEventForElection(caPosition)
        return bool(businessEvent and (businessEvent.TradeLinks() or 
                    businessEvent.PaymentLinks()))

    def _CreateTradeLinks(self, caPosition, result):
        linkHelper = PositionLinkHelper(caPosition, self._transHandler)
        trades = (obj for obj in result if obj.IsKindOf(acm.FTrade))
        linkHelper.CreateTradeLinks(trades)

    def _ProcessPosition(self, caPosition):
        
        result = []
        if not validateBusinessProcessTransition(caPosition, 'Processed'):
            Logme()('Corporate Action Position %s is not in a state to be processed' % 
			        (caPosition.Oid()), "INFO")
            return result
        
        if should_process_instrument is not None:
            if not should_process_instrument(caPosition):
                return result
        if not self._IsProcessed(caPosition):
            action = caPosition.CaChoice().CorpAction()
            positionInstance = caPosition.PositionInstance()
            for insPosition in PositionCalculator(action).Positions(positionInstance):
                if insPosition.HasValue():
                    result.extend(ProcessPayouts(caPosition, insPosition, self._templateHelper))
            with self._transHandler.Transaction():
                self._UpdateRollbackSpecAddInfo(caPosition)
                self._transHandler.AddAll(result)
                businessProcess, event, sameState = getBusinessProcessAndEvent(caPosition, 'Processed')
                if businessProcess and not sameState and (event or
                    caPosition.CaChoice().CorpAction().CaChoiceType()
                        in ['Mandatory', 'MandatoryWithChoice']):
                    self._transHandler.transit_business_process_state(
                        businessProcess, event, 'Processed', 'Not Voluntary')
            self._CreateTradeLinks(caPosition, result)
        else:
            Logme()('Corporate Action Position %s already processed' % (caPosition.Oid()), "INFO")
        return result
