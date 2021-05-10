"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    BrokerNoteBulkBusinessProcessCreator

DESCRIPTION
    This module contains objects used for creation of  bulk
    broker note business process based on a block trade being void.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-04-20      FAOPS-702       Joash Moodley                                   Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from at_logging import getLogger
import BrokerNoteBulkGeneral


LOGGER = getLogger(__name__)


class BrokerNoteBulkBusinessProcessCreator(object):
    """
    An object responsible for creation of an bulk broker note business process which is created via
    a business process.
    """

    @classmethod
    def create_broker_note_business_process(cls, block_trade, managing_party):
        """
        Create an broker note business process for
        the specified block trade and counter party.
        """
        cls._create_broker_note_business_process_for_counterparty_and_block_trade(block_trade, managing_party)

    @classmethod
    def _create_broker_note_business_process_for_counterparty_and_block_trade(cls, block_trade, managing_party):
        """
        Create an broker note business process for
        the specified block trade and counter party.

        """
        cls._validate_instrument_type(block_trade.Instrument().InsType())
        LOGGER.info("Creating broker note business process for counterparty '{counterparty_name}'.".format(
            counterparty_name=block_trade.Counterparty().Name()
        ))
        BrokerNoteBulkGeneral.create_broker_note_business_process(
            managing_party, 
            block_trade.Instrument().InsType(),
            block_trade, 
        )

    @staticmethod
    def _validate_instrument_type(instrument_type):
        """
        Validate an instrument type specified for  broker_note
        creation.
        """
        if instrument_type is None:
            raise ValueError('An instrument type must be specified.')
        if instrument_type not in BrokerNoteBulkGeneral.get_supported_broker_note_instrument_types():
            raise ValueError('A supported instrument type must be specified.')
