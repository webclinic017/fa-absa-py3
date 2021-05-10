"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PreSettlementAdviceAmendmentScript

DESCRIPTION
    This module contains an AEL main script used to ensure pre-settlement advices are
    up-to-date.

    This involves the following:

    - Triggering the amendment of any existing pre-settlement advices that require
      updating since initial generation (due to changes to trades, instruments,
      parties, etc.).
    - Triggering the generation of any missing pre-settlement advices (due to
      settlements now existing that did not exist at scheduled creation time,
      changes to parties, etc.).

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-02-05      FAOPS-741       Cuen Edwards            Kgomotso Gumbo          Replaced pre-settlement advice event listener with task.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import datetime

from at_logging import getLogger
import DocumentGeneral
import PreSettlementAdviceGeneral
from PreSettlementAdviceBusinessProcessCreator import PreSettlementAdviceBusinessProcessCreator
from PreSettlementAdviceProcessor import PreSettlementAdviceProcessor


LOGGER = getLogger(__name__)

ael_variables = []


def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    try:
        start_date_time = datetime.datetime.today()
        LOGGER.info('Starting at {start_date_time}'.format(start_date_time=start_date_time))
        _check_existing_advices_for_updates()
        _check_for_missing_scheduled_advices()
        end_date_time = datetime.datetime.today()
        LOGGER.info('Completed successfully at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        DocumentGeneral.handle_script_exception(exception)


def _check_existing_advices_for_updates():
    """
    Check if any updates are required to existing pre-settlement
    advices and, if so, trigger the update.
    """
    LOGGER.info("Checking existing pre-settlement advices for updates...")
    active_advice_business_processes = PreSettlementAdviceGeneral.get_active_advice_business_processes()
    if len(active_advice_business_processes) == 0:
        LOGGER.info("No active pre-settlement advices found, nothing to update.")
        return
    document_processor = PreSettlementAdviceProcessor()
    for business_process in active_advice_business_processes:
        try:
            document_processor.check_for_updates(business_process)
        except:
            # Prevent an exception during the checking of one advice
            # from preventing the checking of others.
            message = "An exception occurred checking pre-settlement advice {oid} for amendments, skipping..."
            message = message.format(oid=business_process.Oid())
            LOGGER.warning(message, exc_info=True)


def _check_for_missing_scheduled_advices():
    """
    Check if any missing scheduled pre-settlement advices need to be
    created and, if so, trigger the creation.
    """
    LOGGER.info("Checking for missing scheduled pre-settlement advices...")
    PreSettlementAdviceBusinessProcessCreator().create_missing_scheduled_advice_business_processes()
