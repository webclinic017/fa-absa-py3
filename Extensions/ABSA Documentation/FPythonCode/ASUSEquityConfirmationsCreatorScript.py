"""------------------------------------------------------------------------------------------------------------------
MODULE
    ASUSEquityConfirmationsCreatorScript

DESCRIPTION
    Task to create 10b10 Confirmation at T+1 for All ASUS Equity Deals

---------------------------------------------------------------------------------------------------------------------
HISTORY
=====================================================================================================================
Date            Change no       Developer               Description
---------------------------------------------------------------------------------------------------------------------
2020-02-17      FAOPS-748       Tawanda Mukhalela       ASUS New Trade Confirmations
---------------------------------------------------------------------------------------------------------------------
"""

import datetime

from ASUS10b10ConfirmationCreator import ASUS10b10ConfirmationCreator
from at_ael_variables import AelVariableHandler
from at_logging import getLogger


LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()


def ael_main(ael_parameters):
    try:
        start_date_time = datetime.datetime.today()
        LOGGER.info('Starting at {start_date_time}'.format(start_date_time=start_date_time))
        valid_trades = ASUS10b10ConfirmationCreator().get_valid_trades()
        for trade in valid_trades:
            ASUS10b10ConfirmationCreator().create_confirmation_for_block_trade(trade)

        ASUS10b10ConfirmationCreator.process_unmatched_allocations_and_block_trades()
        end_date_time = datetime.datetime.today()
        LOGGER.info('Completed successfully at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        LOGGER.exception(exception)
