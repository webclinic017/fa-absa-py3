"""---------------------------------------------------------------------------------------------------------------------
MODULE
    SessionFunctions.

DESCRIPTION
    This module contains functionality for obtaining information about the current
    Front Arena session (connection to an environment).

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Description
------------------------------------------------------------------------------------------------------------------------
2020-07-31                      Cuen Edwards            Initial implementation.
------------------------------------------------------------------------------------------------------------------------
"""

import acm


def is_prime():
    """
    Determine whether or not the current session is executing via
    Prime.
    """
    return str(acm.Class()) == 'FTmServer'
