""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionBoxPosition.py"
"""---------------------------------------------------------------------------
MODULE
    FCorpActionBoxPosition - Module to calculate the box position
    for corporate actions

DESCRIPTION


ENDDESCRIPTION
---------------------------------------------------------------------------"""

import acm
from FCorpActionElectionPosition import PositionCalculator
from FTransactionHandler import ACMHandler
from FPositionUtils import PositionCreator, PositionSummary
from FCorpActionUtils import GetTradesForAction
import FCorpActionElectionHandler
import FBDPCommon
from FBDPCurrentContext import Summary, Logme

class FCorpActionBoxPosition():
    # constructor
    def __init__(self, corpAction, transHandler=ACMHandler()):
        self._action = corpAction
        self._transHandler = transHandler
        self._portName = FBDPCommon.valueFromFParameter('FCAVariables', 'BoxTradePortfolioName')
        self._acqName = FBDPCommon.valueFromFParameter('FCAVariables', 'BoxTradeAcquirerName')
        self._cptyName = FBDPCommon.valueFromFParameter('FCAVariables', 'BoxTradeCounterpartyName')
        self._status = FBDPCommon.valueFromFParameter('FCAVariables', 'BoxTradeStatus')
    
    def GetorCreateBusinessEvent(self):
        Logme()('GetorCreateBusinessEvent', 'INFO')
        bEvent = None
        if self._action:
            bEvent = self._action.BusinessEvent()
            if not bEvent:
                bEvent = acm.FBusinessEvent()

        return bEvent
    
    def GetorCreateTradeLink(self, bEvent, boxTrade):
        Logme()('GetorCreateTradeLink', 'INFO')        
        if len(bEvent.TradeLinks()) > 0:
            tradeLinks = bEvent.TradeLinks()
            #there can only be one
            tradeLink = tradeLinks[0]
            tradeLink.TradeEventType(0)
            return tradeLink
        else:
            tradeLink = acm.FBusinessEventTradeLink()
            tradeLink.Trade(boxTrade.Oid())
            tradeLink.BusinessEvent(bEvent)
            tradeLink.TradeEventType(0)
        return tradeLink
    
    # override
    def Calculate(self, positionSpec):
        #don't include the box trade
        trades = GetTradesForAction(self._action)
        boxTrade = self.FindBoxTrade()
        trades.Remove(boxTrade)
        
        #all trades for this corporate action
        posCalc = PositionCalculator(self._action)
        boxPosition = 0
        positions = posCalc.EligiblePositions(trades, acm.FPositionSpecification())
        for position in positions:
            boxPosition += position.Value()
        
        instrument = self._action.Instrument()
        self.FindorCreateBoxTrade(instrument, boxPosition, 'SEK')
    
    def FindBoxTrade(self):
        if self._action:
            bEvent = self._action.BusinessEvent()
            if bEvent:
                tradeLinks = bEvent.TradeLinks()
            else:
                return None
            #there can only be one
            if len(tradeLinks) > 0:
                tradeLink = tradeLinks[0]
                trade = tradeLink.Trade()
                return trade
            else:
                return None
    
    def FindorCreateBoxTrade(self, instrument, boxPosition, currency):
        boxTrade = self.FindBoxTrade()
        if not boxTrade:
            boxTrade = acm.FTrade()
            boxTrade.Instrument(instrument)
            boxTrade.Currency('SEK')
            boxTrade.TradeTime(acm.Time.DateToday())
            boxTrade.ValueDay(acm.Time.DateToday())
            boxTrade.AcquireDay(acm.Time.DateToday())
            boxTrade.Acquirer('FMAINTENANCE')
            boxTrade.Counterparty('FMAINTENANCE')
            boxTrade.Type('Corporate Action')
            boxTrade.Status('Simulated')
        
        boxTrade.Portfolio(acm.FPhysicalPortfolio[self._portName])
        boxTrade.Acquirer(acm.FParty[self._acqName])
        boxTrade.Counterparty(acm.FParty[self._cptyName]) 
        boxTrade.Status(self._status)
        boxTrade.Quantity(boxPosition)
        bEvent = self.GetorCreateBusinessEvent()
        bEvent.Commit()
        tradeLink = self.GetorCreateTradeLink(bEvent, boxTrade)
        self._action.BusinessEvent(bEvent)
        self._action.Commit()
        with self._transHandler.Transaction():
            self._transHandler.Add(boxTrade)
            self._transHandler.Add(tradeLink)
        
        Logme()('New Corporate Action box trade created %s .' % (boxTrade.Oid()), 'DEBUG')
        Summary().ok(boxTrade, Summary().CREATE, boxTrade.Oid())
        Summary().ok(bEvent, Summary().CREATE, bEvent.Oid())
        Summary().ok(tradeLink, Summary().CREATE, tradeLink.Oid())

