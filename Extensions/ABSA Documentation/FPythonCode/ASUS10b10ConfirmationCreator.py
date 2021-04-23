"""------------------------------------------------------------------------------------------------------------------
MODULE
    ASUS10b10ConfirmationCreator

DESCRIPTION
    create 10b10 Confirmation at T+1 for All ASUS Equity Deals

---------------------------------------------------------------------------------------------------------------------
HISTORY
=====================================================================================================================
Date            Change no       Developer               Description
---------------------------------------------------------------------------------------------------------------------
2020-04-29      FAOPS-748       Tawanda Mukhalela       ASUS New Trade Confirmations
---------------------------------------------------------------------------------------------------------------------
"""

import acm

import ASUSNewTradeConfirmationGeneral
from at_logging import getLogger
import DocumentConfirmationGeneral

LOGGER = getLogger(__name__)


class ASUS10b10ConfirmationCreator(object):

    def __init__(self):
        pass

    @classmethod
    def create_confirmation_for_block_trade(cls, trade):
        """
        Creates the confirmation object for the given block trade
        """
        document_event_name = ASUSNewTradeConfirmationGeneral.get_asus_event_name()
        confirmation_owner_trade = trade
        DocumentConfirmationGeneral.create_document_confirmation(document_event_name,
                                                                 confirmation_owner_trade,
                                                                 from_date=acm.Time.DateToday(),
                                                                 to_date=acm.Time.DateToday()
                                                                 )

    @classmethod
    def get_valid_trades(cls):
        """
        Returns all valid block trades
        """
        valid_trades = list()
        trades = ASUSNewTradeConfirmationGeneral.get_all_block_trades()
        allocations = ASUSNewTradeConfirmationGeneral.get_all_applicable_allocations()
        for block_trade in trades:
            if ASUSNewTradeConfirmationGeneral.has_valid_10b10_confirmation_already_created(block_trade):
                continue
            if 'STL' not in block_trade.Portfolio().Name():
                continue
            if cls._allocate_block(block_trade, allocations):
                valid_trades.append(block_trade)

        return valid_trades

    @classmethod
    def _allocate_block(cls, block_trade, allocations):
        """
        Links applicable allocations to the block
        """
        block_quantity = block_trade.Quantity()
        total_quantinty = 0

        block_allocations = cls._get_allocations_for_block(block_trade, allocations)
        message = 'Found {0} applicable allocations for Block Trade {1}'
        LOGGER.info(message.format(len(block_allocations), block_trade.Oid()))
        if len(block_allocations) == 0:
            return False

        for allocation in block_allocations:
            if abs(allocation.Quantity()) == abs(block_quantity):
                if cls._apply_trx_trade_to_allocation(allocation, block_trade):
                    return True
            total_quantinty += allocation.Quantity()

        if abs(block_quantity) == abs(total_quantinty):
            for allocation in block_allocations:
                cls._apply_trx_trade_to_allocation(allocation, block_trade)
            return True

        return False

    @classmethod
    def _get_allocations_for_block(cls, block_trade, allocations):
        """
        Gets all applicable allocations for the block
        """
        applicable_allocations = list()
        price = block_trade.Price()
        quantity = block_trade.Quantity()
        for allocation in allocations:
            if allocation.TrxTrade():
                continue
            if round(allocation.Price(), 2) != round(price, 2):
                continue
            if abs(allocation.Quantity()) > abs(quantity):
                continue
            if allocation.Portfolio() is not block_trade.Portfolio():
                continue
            if allocation.Instrument().Name() != block_trade.Instrument().Name():
                continue
            applicable_allocations.append(allocation)

        return applicable_allocations

    @classmethod
    def _apply_trx_trade_to_allocation(cls, allocation, block_trade):
        """
        Stamps TrxTrade on Allocation Trade
        """
        try:
            allocation.TrxTrade(block_trade)
            allocation.Commit()
        except Exception as e:
            error_message = 'Failed to stamp TrxTrade {0} on Allocation Trade: {1} , {2}'
            LOGGER.exception(error_message.format(block_trade.Oid(), allocation.Oid(), e))
            return False

        return True

    @classmethod
    def process_unmatched_allocations_and_block_trades(cls):
        """
        Processes all block trades that could not be matched to specific
        allocations
        """
        block_trades = ASUSNewTradeConfirmationGeneral.get_unprocessed_blocks()
        unallocated_blocks_dict = ASUSNewTradeConfirmationGeneral.get_unmatched_block_trades(block_trades)
        if len(list(unallocated_blocks_dict.keys())) == 0:
            return

        unprocessed_trades_dict = ASUSNewTradeConfirmationGeneral.get_allocations_and_blocks_to_process(
            unallocated_blocks_dict)
        for block_trade_list, matching_allocations in list(unprocessed_trades_dict.items()):
            cls._link_allocations_to_block_trade(matching_allocations, block_trade_list[0])
            cls._generate_confirmations_for_trades(block_trade_list)

    @classmethod
    def _link_allocations_to_block_trade(cls, allocations, block_trade):
        """
        Stamps allocations onto the block
        """
        for allocation in allocations:
            cls._apply_trx_trade_to_allocation(allocation, block_trade)

    @classmethod
    def _generate_confirmations_for_trades(cls, trade_list):
        """
        Generates confirmations for trades
        """
        for trade in trade_list:
            cls.create_confirmation_for_block_trade(trade)
