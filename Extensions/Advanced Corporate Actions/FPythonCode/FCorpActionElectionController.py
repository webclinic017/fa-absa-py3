""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionElectionController.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionElectionController 

DESCRIPTION
----------------------------------------------------------------------------"""


import acm
import FBDPCommon

import FCorpActionElectionStatesSetup
import FBusinessProcessUtils
from FBDPCurrentContext import Summary, Logme
from FPositionUtils import PositionCreator, GetAttributeValue, PositionSummary
from FCorpActionElectionPosition import PositionCalculator
from FTransactionHandler import ACMHandler
from FCorpActionUtils import GetTradesForAction


__all__ = ['ElectionController',
           'ElectionCreator']


def _GetParty(positionInstance):
    party = None
    name = GetAttributeValue(positionInstance, 'Counterparty.Name')
    if name is not None:
        party = acm.FParty[name]
    return party

def _GetPortfolio(positionInstance):
    portfolio = None
    name = GetAttributeValue(positionInstance, 'Portfolio.Name')
    if name is not None:
        portfolio = acm.FPhysicalPortfolio[name]
    return portfolio

def _GetInstrument(positionInstance):
    instrument = None
    name = GetAttributeValue(positionInstance, 'Instrument.Name')
    if name is not None:
        instrument = acm.FInstrument[name]
    return instrument

class ElectionController(object):

    def __init__(self, corpAction, transHandler=ACMHandler()):
        self._action = corpAction
        self._transHandler = transHandler

    @staticmethod
    def LogPositions(posSummary):

        for posOid in posSummary.NewPositions():
            Logme()('New Position Created %s .' % (posOid), 'DEBUG')
            Summary().ok(acm.FCalculationRow[posOid], Summary().CREATE, posOid)

        for posOid in posSummary.ExistingPositions():
            Logme()('Exising Position %s found.' % (posOid), 'DEBUG')

    def FindCreateOrDeleteElections(self, positionSpec):
        elections = []
        posCreator = PositionCreator(positionSpec, self._transHandler)
        posSummary = PositionSummary()
        Logme()('Started creating positions.', 'DEBUG')        
        poscalc = PositionCalculator(self._action)
        positions = poscalc.EligiblePositions(GetTradesForAction(self._action), positionSpec)
        for position in positions:
            if not position.HasValue():
                continue

            positionInstances = posCreator.FindOrCreatePositions(position.Trades())
            for positionInstance in positionInstances:
                for choice in self._Choices():
                    election = self._GetElection(positionInstance, choice)
                    if election is None:
                        creator = ElectionCreator(choice, self._transHandler)
                        election = creator.CreateElection(positionInstance)
                    else:
                        Logme()('Existing corporate action position %s Found.' % (election.Oid()), 'DEBUG')
                        self._UpdateElection(election, positionInstance)
                    elections.append(election)
        Logme()('Finished creating positions.', 'DEBUG')
        self.LogPositions(posSummary)
        
        #lastly, create or update the election for the box position trade
        bEvent = self._action.BusinessEvent()
        if bEvent:
            trades = bEvent.Trades(0)
            boxPositions = posCreator.FindOrCreatePositions(trades)
            if len(boxPositions) == 1:
                positionInstance = boxPositions[0]
                for choice in self._Choices():
                    election = self._GetElection(positionInstance, choice)
                    if election is None:
                        creator = ElectionCreator(choice, self._transHandler)
                        election = creator.CreateElection(positionInstance)
                    else:
                        Logme()('Existing corporate action box position %s Found.' % (election.Oid()), 'DEBUG')
                        self._UpdateElection(election, positionInstance)
                    elections.append(election)
        
        return elections

    def _Choices(self):
        return self._action.CaChoices()

    def _GetElection(self, positionInstance, choice):
        query = 'positionInstance={0}'.format(positionInstance.Oid())
        #one election per choice and action
        elections = acm.FCorporateActionElection.Select(query)
        for election in elections:
            if election:
                if choice.CorpAction() == self._action and election.CaChoice() == choice:
                    return election
        return None
    
    def _UpdateElection(self, election, positionInstance):
        #update properties which may have changed
        
        election.Party(_GetParty(positionInstance))
        try:
            election.Instrument(_GetInstrument(positionInstance))
        except:
            pass
        
        try:
            election.PositionInstance(positionInstance)
        except:
            pass
        
        election.Portfolio(_GetPortfolio(positionInstance))
        #Don't update properties if the status is not Ready
        status = FCorpActionElectionStatesSetup.GetStatus(election)
        if status == 'Ready':
            if self._action.WithdrawalDate() != '':
                #the actual deadline to respond to the issuer
                election.Deadline(self._action.WithdrawalDate())
                #the deadline given to the borrower/lender 
                election.ReplyDate(self._action.WithdrawalDate())
            
        election.Commit()
        bp = FBusinessProcessUtils.GetOrCreateBusinessProcess(election,
                                    'CorpActionElectionStateChart')
        bp.Commit()

class ElectionCreator(object):

    def __init__(self, choice, transHandler=ACMHandler()):
        self._choice = choice
        self._transHandler = transHandler

    def CreateElection(self, positionInstance):
        portfolio = _GetPortfolio(positionInstance)
        party = _GetParty(positionInstance)
        instrument = _GetInstrument(positionInstance)
        if portfolio:
            return self._CreateElection(positionInstance, portfolio, party, instrument)
        return None

    def _CreateElection(self, positionInstance, portfolio, party, instrument):
        election = acm.FCorporateActionElection()
        election.CaChoice(self._choice)
        election.Portfolio(portfolio)
        election.Party(party)
        election.Instrument(instrument)
        
        #the actual deadline to respond to the issuer
        election.Deadline(self._choice.CorpAction().WithdrawalDate())
        
        #the deadline given to the borrower/lender 
        election.ReplyDate(self._choice.CorpAction().WithdrawalDate())
        
        if self._choice.IsDefault():
            election.Percentage(100.0)
        else:
            election.Percentage(0.0)
        
        try:
            election.PositionInstance(positionInstance)
        except:
            pass
        
        dividendFactor = None
        try:
            divFactor = instrument.DividendFactor()
            if instrument.Underlying() and divFactor == 0.0:
                divFactor = instrument.Underlying().DividendFactor()
            dividendFactor = FBDPCommon.SetAdditionalInfoValue(election,
                                                           'CorpActionElection', 
                                                           'TaxRate', 
                                                            divFactor)
        except:
            pass
        
        traderElection = FBDPCommon.SetAdditionalInfoValue(election,
                                                       'CorpActionElection',
                                                       'TraderElection',
                                                        'N/A')
        with self._transHandler.Transaction():
            self._transHandler.Add(election)
            self._transHandler.Add(dividendFactor)
            self._transHandler.Add(traderElection)
        if not self._transHandler.TestMode() and \
              FCorpActionElectionStatesSetup.CorporateActionUsingBusinessProcess():
            bp = FBusinessProcessUtils.GetOrCreateBusinessProcess(election,
                                    'CorpActionElectionStateChart')
            with self._transHandler.Transaction():
                self._transHandler.Add(bp)
        Logme()('New Corporate Action Position Created %s .' % (election.Oid()), 'DEBUG')
        Summary().ok(election, Summary().CREATE, election.Oid())
        return election
