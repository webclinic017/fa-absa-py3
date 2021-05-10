"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PreSettlementAdviceBulkCreatorScript

DESCRIPTION
    This module contains an AEL main script used for the bulk generation of
    pre-settlement advice for instrument types.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import datetime

from at_logging import getLogger
import DocumentGeneral
from PreSettlementAdviceBusinessProcessCreator import PreSettlementAdviceBusinessProcessCreator


LOGGER = getLogger(__name__)

ael_variables = []


def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    try:
        start_date_time = datetime.datetime.today()
        LOGGER.info('Starting at {start_date_time}'.format(start_date_time=start_date_time))
        PreSettlementAdviceBusinessProcessCreator().create_scheduled_advice_business_processes()
        end_date_time = datetime.datetime.today()
        LOGGER.info('Completed successfully at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        DocumentGeneral.handle_script_exception(exception)
