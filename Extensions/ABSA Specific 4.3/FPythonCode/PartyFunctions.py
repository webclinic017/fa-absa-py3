"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PartyFunctions

DESCRIPTION
    This module contains general-purpose functions related to parties.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-10-22      FAOPS-287       Cuen Edwards            Kgomotso Gumbo          Initial implementation containing the implementation of 
                                                                                party custom method ShortCode.  The purpose of this custom
                                                                                method is two-fold: implementation hiding (enables changing
                                                                                where this value is stored without having to change several
                                                                                code locations) and enhanced code readability (ShortCode is
                                                                                clearer than Free5/Alias/etc.).
-----------------------------------------------------------------------------------------------------------------------------------------
"""


def get_short_code(party):
    """
    Get a party's short code.

    This function is the getter implementation of the Party custom
    method ShortCode.
    """
    return party.Free5()


def set_short_code(party, short_code):
    """
    Set a party's short code.

    This function is the setter implementation of the Party custom
    method ShortCode.
    """
    party.Free5(short_code)
