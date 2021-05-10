"""
This module contains the Python method that will be executed from ADFL that will evaluate a specific trade.
"""

import acm
from GenericMandatesDefinition import Mandate
from GenericMandatesConstants import MANDATE_ALLOWED_TEXT, MANDATE_NOT_ALLOWED_TEXT, MANDATE_NOT_FOUND_TEXT
from GenericMandatesUtils import GetLimits


def Get_Evaluated_Mandate_Number(trade, mandateType):
    """
    Method called from ADFL to evaluate a specific trade against the applicable mandates.

    IMPORTANT: ONLY checks modified trades.

    :param trade: FTrade
    :param mandateType: string
    :return: string
    """
    # applicableLimits = acm.Limits.FindByTrade(trade)
    applicableLimits = GetLimits(trade)
    tradeBreach = False

    if trade.IsModified() is True or trade.IsInfant() is True or trade.Oid() <0:
        # Check all Mandates
        for applicableLimit in applicableLimits:
            if applicableLimit.LimitSpecification().Name() == mandateType:
                mandate = Mandate(applicableLimit)
                if len(mandate.QueryFolders()) > 0:
                    if mandate.IsTradeValid(trade) is False:
                        return MANDATE_NOT_ALLOWED_TEXT
                else:
                    return MANDATE_NOT_FOUND_TEXT
        return MANDATE_ALLOWED_TEXT
    else:
        return MANDATE_ALLOWED_TEXT
