"""--------------------------------------------------------------------------------------------------------------------
MODULE:
    FFXMMConfirmationOutUtils_Override

DESCRIPTION:
    A module for common functions used across FXMMConfirmation outgoing
    solution.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2021-04-15      FAOPS-978       Tawanda Mukhalela       Nqubeko Zondi           modified get_event_type_MT330 to cater
                                                                                for Adjust Deposits MT330s.
------------------------------------------------------------------------------------------------------------------------
"""


def get_event_type_MT330(confirmation):
    """
    Get event type for Confirmation
    """
    if confirmation.EventChlItem().Name() == 'Adjust Deposit':
        return 'CHNG'

    return 'CONF'
