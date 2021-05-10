"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PaymentContingencyPlanFileCreatorScript

DESCRIPTION
    This module contains an AEL main script used for the creation of payment
    contingency plan files.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-03-23      FAOPS-681       Cuen Edwards            Linda Breytenbach       Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import datetime

import acm

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from PaymentContingencyPlanFileCreator import PaymentContingencyPlanFileCreator
import SessionFunctions


LOGGER = getLogger(__name__)


def _create_ael_variable_handler():
    """
    Create an AelVariableHandler for this script.
    """
    ael_variable_handler = AelVariableHandler()
    # Output directory path.
    ael_variable_handler.add_directory(
        name='output_directory_path',
        label='Output Directory',
        default=r'/services/frontnt/Task'
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
        output_directory_path = ael_parameters['output_directory_path']
        PaymentContingencyPlanFileCreator.create_files(output_directory_path.AsString())
        end_date_time = datetime.datetime.today()
        LOGGER.info('Completed successfully at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        if SessionFunctions.is_prime():
            _show_error_dialog(exception)
            LOGGER.exception(exception)
        else:
            raise


def _show_error_dialog(exception):
    """
    Display an error dialog to the user.
    """
    message_box = acm.GetFunction('msgBox', 3)
    ok_button = 0
    error_icon = 16
    message_box('Error', str(exception), ok_button | error_icon)
