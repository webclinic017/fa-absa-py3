"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    EuroClearMT210Payment

DESCRIPTION
    This module contains a hook to create a EuroClear MT210 Payment

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no        Developer               Requester              Description
-----------------------------------------------------------------------------------------------------------------------------------------
01-04-2020      FAOPS-683       Joash Moodley           Kgomotso Gumbo          Creates a Payment Premium settlement
                                                                                for a buy euroclear trade.
18-08-2020      FAOPS-865       Tawanda Mukhalela       Wandile Sithole         Refactored Code to solve for Duplicate
                                                                                Payments and Race Conditions
2020-09-14      FAOPS-864       Jaysen Naicker          Wandile Sithole         Enable End Cash for Euroclear Repo/Reverse and 
                                                                                incl BSB ins type in Funding
2021-03-11      FAOPS-1030/53   Tawanda Mukhalela       Wandile Sithole         Added Support for Netted Settlements to
                                                                                trigger stand alone payment generation
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
from OperationsSTPHook import OperationsSTPHook
import OperationsSTPFunctions

LOGGER = getLogger(__name__)


class EuroClearMT210PaymentCreation(OperationsSTPHook):
    """
    Definition of a hook used to create a EuroClear MT210 Payment
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Euro Clear MT210 Stand Alone Creation Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FSettlement):
            return False
        settlement = eventObject
        trade = settlement.Trade()
        if not trade:
            return False
        if not _is_valid_trade(trade):
            return False
        if not _is_valid_premium_settlement_or_end_cash(settlement):
            return False
        if _is_stand_alone_present(trade):
            return False

        return True

    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        trade = eventObject.Trade()
        LOGGER.info('Creating MT 210 Stand Alone Payment for Trade {trade}'.format(trade=trade.Oid()))
        self._create_stand_alone_payment(eventObject)

    @staticmethod
    def _create_stand_alone_payment(settlement):
        """
        Create Stand alone settlement from existing
        Premium Settlement
        """
        new_settlement = settlement.Clone()
        new_settlement.Type('Stand Alone Payment')
        new_settlement.Commit()


class EuroClearMT210PaymentUpdate(OperationsSTPHook):
    """
    Definition of a hook used to Update a EuroClear MT210 Stand Alone Payment
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Euro Clear MT210 Updates Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FSettlement):
            return False
        settlement = eventObject
        trade = settlement.Trade()
        if not trade:
            return False
        if not _is_valid_trade(trade):
            return False
        if not _is_valid_premium_settlement_or_end_cash(settlement):
            return False
        if not _is_stand_alone_present(trade):
            return False
        if not self._is_premium_amounts_different(settlement):
            return False

        return True

    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        settlement = eventObject
        trade = settlement.Trade()
        LOGGER.info('Updating MT 210 Stand Alone Payment for Trade {trade}'.format(trade=trade.Oid()))
        premium_amount = settlement.Amount()
        stand_alone_settlement = self._get_stand_alone_settlement(settlement)
        LOGGER.info('Updating amount from {} to {}'.format(stand_alone_settlement.Amount(), premium_amount))
        stand_alone_settlement = stand_alone_settlement.StorageImage()
        stand_alone_settlement.Amount(premium_amount)
        stand_alone_settlement.Commit()

    def _is_premium_amounts_different(self, settlement):
        """
        Checks if Premium amount is different from Stand Alone
        """
        stand_alone_payment = self._get_stand_alone_settlement(settlement)
        if not stand_alone_payment:
            return False
        stand_alone_premium = stand_alone_payment.Amount()
        updated_premium = settlement.Amount()
        if stand_alone_premium == updated_premium:
            return False

        return True

    @staticmethod
    def _get_stand_alone_settlement(settlement):
        """
        Gets Stand Alone Payment
        """
        trade = settlement.Trade()
        settlements = trade.Settlements()
        settlement_type = 'Stand Alone Payment'
        stand_alone_settlements = [
            settlement for settlement in settlements
            if settlement.Type() == settlement_type
        ]
        if len(stand_alone_settlements) > 1:
            LOGGER.error('Found More than one Stand Alone Settlements.. Skipping Update')
            return

        return stand_alone_settlements[0]


def _is_valid_trade(trade):
    """
    Checks if the Trade is valid for MT210
    Stand alone settlement Creation
    """
    instrument_types = (
        'Bill', 'Bond', 'BuySellback', 'FRN', 'Repo/Reverse', 'IndexLinkedBond'
    )
    if trade.Instrument().InsType() not in instrument_types:
        return False
    if not trade.SettleCategoryChlItem():
        return False
    if trade.SettleCategoryChlItem().Name() != 'Euroclear':
        return False

    return True


def _is_valid_premium_settlement(settlement):
    """
    Checks if settlement is a valid premium settlement
    """
    if settlement.Type() != 'Premium':
        return False
    if not OperationsSTPFunctions.is_outgoing_settlement(settlement):
        return False

    return True


def _is_valid_premium_settlement_or_end_cash(settlement):
    """
    Checks if settlement is a valid premium settlement
    """
    if settlement.Type() == 'Premium' or _is_valid_return_leg_settlement(settlement):
        if OperationsSTPFunctions.is_outgoing_settlement(settlement):
            return True

    return False


def _is_valid_return_leg_settlement(settlement):
    """
    Checks if settlement is valid for a return leg end cash
    """
    if settlement.Type() not in ('End Cash', 'None'):
        return False
    if settlement.Trade().Instrument().InsType() not in ('BuySellback', 'Repo/Reverse'):
        return False
    return True


def _is_stand_alone_present(trade):
    """
    Checks if a Stand Alone Settlement Already Exists on the trade
    """
    settlements = trade.Settlements().AsArray()
    settlement_type = 'Stand Alone Payment'
    return any([settlement for settlement in settlements
                if settlement.Type() == settlement_type]
               )
