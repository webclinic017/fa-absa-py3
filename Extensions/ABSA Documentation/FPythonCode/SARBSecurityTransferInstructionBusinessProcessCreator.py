"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SARBSecurityTransferInstructionBusinessProcessCreator

DESCRIPTION
    This module contains objects used for triggering the generation of SARB security
    transfer instructions via the creation of business processes.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-05-04      FAOPS-746       Cuen Edwards            Kgomotso Gumbo          Initial implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import SARBSecurityTransferInstructionGeneral
from SARBSecurityTransferInstructionGeneral import StateNames


LOGGER = getLogger(__name__)


class SARBSecurityTransferInstructionBusinessProcessCreator(object):
    """
    An object responsible for triggering the generation of SARB
    security transfer instructions via the creation of SARB Sec
    Transfer Instruction business processes.
    """

    @classmethod
    def create_instruction_business_processes(cls):
        """
        Create SARB security transfer instruction business processes.
        """
        message = "Creating SARB security transfer instruction business processes "
        message += "for transfer date '{transfer_date}'..."
        transfer_date = acm.Time.DateToday()
        LOGGER.info(message.format(
            transfer_date=transfer_date
        ))
        cls._validate_no_unsent_instructions(transfer_date)
        for event_name in SARBSecurityTransferInstructionGeneral.get_transfer_event_names():
            if not SARBSecurityTransferInstructionGeneral.security_transfers_exist(event_name, transfer_date):
                message = "No security transfers found for event '{event_name}', skipping..."
                LOGGER.info(message.format(
                    event_name=event_name
                ))
                continue
            LOGGER.info("Creating instruction business process for event '{event_name}'.".format(
                event_name=event_name
            ))
            SARBSecurityTransferInstructionGeneral.create_instruction_business_process(event_name, transfer_date)
        LOGGER.info("Completed creating SARB security transfer instruction business processes.")

    @staticmethod
    def _validate_no_unsent_instructions(transfer_date):
        """
        Validate that there are no unsent SARB security transfer
        instruction busness processes for the specified transfer
        date.
        """
        business_processes = SARBSecurityTransferInstructionGeneral._get_existing_instruction_business_processes(
            transfer_date)
        for business_process in business_processes:
            current_state_name = business_process.CurrentStateName()
            if current_state_name in [StateNames.SENT, StateNames.ACKNOWLEDGED]:
                continue
            raise ValueError("Unsent instructions already exists.")
