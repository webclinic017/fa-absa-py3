""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionPositionLinkHelper.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionPositionLinkHelper

DESCRIPTION
----------------------------------------------------------------------------"""
import acm
import FBDPCommon

from FBDPCurrentContext import Summary, Logme
from FTransactionHandler import ACMHandler
from FCorpActionUtils import GetBusinessEventForElection


__all__ = ['PositionLinkHelper']


class PositionLinkHelper(object):

    def __init__(self, election, transHandler=ACMHandler()):
        self._election = election
        self._transHandler = transHandler
        
    def CreateTradeLinks(self, trades):
        event = self.FindOrCreateBusinessEvent()
        with self._transHandler.Transaction():
            for trd in trades:
                trdLink = self._CreateTradeLink(trd, event)
                self._transHandler.Add(trdLink)

    def FindOrCreateBusinessEvent(self):
        event = GetBusinessEventForElection(self._election)
        if event is None: 
            event = self._CreateBusinessEvent()
        return event

    def _CreateTradeLink(self, trade, event):
        if not trade:
            return
        trdLink = acm.FBusinessEventTradeLink()
        trdLink.Trade(trade)
        trdLink.BusinessEvent(event)
        Logme()('New TradeLink Created %s .' % (trdLink.Oid()), 'DEBUG')
        Summary().ok(trdLink, Summary().CREATE)
        return trdLink
        
    def _CreateBusinessEvent(self):
        event = acm.FBusinessEvent()
        with self._transHandler.Transaction():
            self._transHandler.Add(event)
            self._election.BusinessEvent(event)
            self._transHandler.Add(self._election, ['BusinessEvent'], 'Update')
            
        Logme()('New BusinessEvent Created %s .' % (event.Oid()), 'DEBUG')
        Summary().ok(event, Summary().CREATE, event.Oid())
        return event
