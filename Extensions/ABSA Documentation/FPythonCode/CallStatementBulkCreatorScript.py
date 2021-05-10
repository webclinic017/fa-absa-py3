"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    CallStatementBulkCreatorScript.

DESCRIPTION
    This module contains an AEL main script used for the bulk generation of
    call deposit statements for acquirers.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-08-14      FAOPS-167       Cuen Edwards            Elaine Visagie          Initial Implementation
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import datetime

import acm

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from CallStatementConfirmationCreator import CallStatementConfirmationCreator
import DocumentGeneral


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
        default='Funding Desk,Money Market Desk',
        mandatory=True,
        multiple=True,
        alt='The acquirers to generate statements for.'
    )
    # Ignore Existing Statements.
    ael_variable_handler.add(
        name='ignore_existing_statements',
        label='Ignore Existing Statements?',
        cls='bool',
        collection=[False, True],
        default=False,
        mandatory=False,
        multiple=False,
        alt='Create a statement even if one already exists? ' +
            'This option should normally only be selected in ' +
            'the event that incorrect statements were created ' +
            'and corrected ones must be created.'
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
        ignore_existing_statements = ael_parameters['ignore_existing_statements']
        CallStatementConfirmationCreator().create_scheduled_statement_confirmations(acquirers,
            ignore_existing_statements)
        end_date_time = datetime.datetime.today()
        LOGGER.info('Completed successfully at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        DocumentGeneral.handle_script_exception(exception)
