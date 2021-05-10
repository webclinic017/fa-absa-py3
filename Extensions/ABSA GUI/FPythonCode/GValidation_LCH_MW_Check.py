"""----------------------------------------------------------------------------------------------------
DESCRIPTION
    This module contains code to validate if a trade being booked is one of LCH portfolios and if it does not have a MW ID then Front Arena must not allow the trade to be booked and it must show an error. 

-------------------------------------------------------------------------------------------------------
HISTORY
=======================================================================================================
Date            JIRA no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-08-25      FAFO-139      Amit Kardile            Kim, Ena and Kalin      Initial Implementation
-------------------------------------------------------------------------------------------------------
"""

import acm


CONFIG_PARAMS = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', 'LCH_MW_Check').Value()


def popup_error(shell, message):
    return acm.UX.Dialogs().MessageBoxOKCancel(shell, 0, message)


def lch_mw_check_failed(shell, obj):

    """ On trade save entry-point from GValidation
    """
    trade_qualifying_query_folder_name = CONFIG_PARAMS['Front_Trade_qualifying_query_folder']
    query_folder = acm.FStoredASQLQuery[trade_qualifying_query_folder_name.Text()]
    trade = obj
    if query_folder:
        if query_folder.Query().IsSatisfiedBy(trade):
            if not trade.AdditionalInfo().CCPmiddleware_id():
                message = 'Cannot book the trade in LCH portfolio.\n\nPlease enter Clearing ID in MarkitWire tab and try again.'
                popup_error(shell, message)
                return True
     
    return False
