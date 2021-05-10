"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    MultiTradeConfirmationOwnerCreatorScript.
    
DESCRIPTION
    This module contains an AEL main script that is used to ensure that 
    a dummy trade exists to own the confirmation created for a document 
    related to multiple trades.
    
    This process is run periodically and is necessary as not all users 
    have the access rights required to create trade objects.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-08-01      FAOPS-127       Cuen Edwards            Elaine Visagie          Refactored from a term deposit statement specific 
                                                                                implementation to one that can be used for other multi-
                                                                                trade documents.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import datetime

import acm

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
import DocumentGeneral
from MultiTradeConfirmationOwnerProvider import MultiTradeConfirmationOwnerProvider


LOGGER = getLogger(__name__)


def _create_ael_variable_handler():
    """
    Create an AelVariableHandler for this script.
    """
    ael_variable_handler = AelVariableHandler()
    # Acquirers.    
    ael_variable_handler.add(
        name='acquirers',
        label='Acquirers',
        cls=acm.FInternalDepartment,
        mandatory=True,
        multiple=True,
        alt='The acquirers for which multi-trade documents may be generated.'
    )
    # Counterparties.
    ael_variable_handler.add(
        name='counterparties',
        label='Counterparties',
        cls=acm.FParty,
        mandatory=True,
        multiple=True,
        alt='The counterparties for which multi-trade documents may be generated.'
    )
    return ael_variable_handler


ael_variables = _create_ael_variable_handler()


def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    try:
        start_date_time = datetime.datetime.today()
        LOGGER.info('Starting at {start_date_time}'.format(start_date_time=start_date_time))
        acquirers = ael_parameters['acquirers']
        counterparties = ael_parameters['counterparties']
        _create_missing_confirmation_owner_trades(acquirers, counterparties)
        end_date_time = datetime.datetime.today()
        LOGGER.info('Completed successfully at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        DocumentGeneral.handle_script_exception(exception)


def _create_missing_confirmation_owner_trades(acquirers, counterparties):
    """
    Ensure that confirmation owner trades exist for all combinations 
    of acquirer and counterparty.
    """
    confirmation_owner_trade_provider = MultiTradeConfirmationOwnerProvider()
    for counterparty in counterparties:
        for acquirer in acquirers:
            confirmation_owner_trade_provider.provide_owner_trade(acquirer, counterparty)
