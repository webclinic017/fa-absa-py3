"""----------------------------------------------------------------------------
MODULE:
    FSwiftClientSecurityStmtOfHoldingExtension

DESCRIPTION:
    OPEN EXTENSION MODULE
    This module provides extension points for user customization at the exit
    point of the message processing, to allow modification of the trade creation

FUNCTIONS:
    import_exit(swift_data, commit_dict):
        Provision to override the trade data before committing them
        Returns commit dict

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
import acm
def import_exit(swift_message, commit_dict):
    """The dictionary of trades and instruments for a given ISIN before commit are provided for any changes to be done"""
    # sample code to set the counterparty is as show below
    '''
    key = commit_dict.keys()[0]
    val = commit_dict[key]
    if not val[0].Counterparty():
        val[0].Counterparty(acm.FParty['____'])
    commit_dict[key] = val
    '''
    return commit_dict



