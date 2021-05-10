"""
-------------------------------------------------------------------------------
MODULE
    ResetAdviceCreator


DESCRIPTION
    Module to create adhoc confirmations. This Module uses the core front confirmation 
    modules to manually create a confirmation for the given trade if it meets the business
    criteria.

HISTORY
===============================================================================
2018-08-21   Tawanda Mukhalela   FAOPS:168  initial implementation
-------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
from DocumentConfirmationGeneral import create_document_confirmation
from FConfirmationEventFactory import FConfirmationEventFactory as EventFactory
from ResetAdviceXMLFunctions import ResetAdviceFunctions


LOGGER = getLogger(__name__)


class ResetAdviceGenerator(object):
    
    reset_advice_event = 'Reset Advice'
    date = acm.Time.DateToday()

    def __init__(self, trade, from_date=date, to_date=date, adhoc_request=False):
        self.trade = trade
        self.party = trade.Counterparty()
        self.acquirer = trade.Acquirer()
        self.from_date = from_date
        self.to_date = to_date
        self.adhoc_request = adhoc_request
        self.instype = trade.Instrument().InsType()

    def validate_trade(self):
        """
        Validates if trade meets the minimum requirements for a reset advice generation
        :return: boolean value
        """
        if self.trade:
            if ResetAdviceFunctions.is_valid_swap_trade(self.trade) \
                    or ResetAdviceFunctions.is_valid_fra_trade(self.trade):
                for leg in self.trade.Instrument().Legs():
                    if ResetAdviceFunctions.is_prime_leg(leg):
                        return False
                    for cashflow in leg.CashFlows():
                        for reset in cashflow.Resets():
                            if reset.Day() == self.from_date \
                                    and reset.FixingValue() != 0.00:
                                return True

        return False

    def generate_advice(self):
        """
        Confirmation creation
        :return: boolean
        """
        if self.validate_trade():           
            events = EventFactory().GetConfirmationEvents()
            for event in events:
                if event.eventName == self.reset_advice_event:
                    if ResetAdviceFunctions.evaluate_confinstruction_and_rule_setup(self.party, self.instype,
                                                                                    event.eventName):
                        create_document_confirmation(event.eventName, self.trade, None, self.from_date,
                                                     self.to_date, self.adhoc_request)
                        continue
