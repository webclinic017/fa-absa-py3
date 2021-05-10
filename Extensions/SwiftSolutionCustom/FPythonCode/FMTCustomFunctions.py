"""
MODULE

FMTCustomFunctions

DESCRIPTION

This module is to cater for all custom functions that are not MT type specific,
for swift solutions MT Messages.

HISTORY
-------------------------------------------------------------------------------------------------------------
Date            Change no       Developer               Description
-------------------------------------------------------------------------------------------------------------
2020-09-01      FAOPS-821       Tawanda Mukhalela       Initial Implemantation
2021-03-09      FAOPS-1027      Willie vd Bank          Added get_lowest_settlement_from_hierarchy
-------------------------------------------------------------------------------------------------------------
"""
import FSwiftMLUtils


def get_cover_indicator(settlement):
    """
    Gets the the Cover indicator from the Settlement objet
    """
    return settlement.AdditionalInfo().IsCov()


def set_cover_indicator(settlement, value):
    """
    Sets the the Cover indicator on the Settlement objet
    """
    settlement.AdditionalInfo().IsCov(value)


def get_current_state_from_acm_object(fobject):
    business_process = FSwiftMLUtils.get_business_process(fobject, "Outgoing")
    if business_process:
        return business_process.CurrentStateName()
    return ''


def get_lowest_settlement_from_hierarchy(settlement):
    """
    Loops through an infinite hierarchy of combined settlements
    to return the lowest level settlement.
    """
    for child_settlement in settlement.Children():
        if child_settlement.Children():
            return get_lowest_settlement_from_hierarchy(child_settlement)
        else:
            return child_settlement
