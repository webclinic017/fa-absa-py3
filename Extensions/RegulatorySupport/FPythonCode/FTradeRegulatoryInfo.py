"""------------------------------------------------------------------------
MODULE
    FTradeRegulatoryInfo -
DESCRIPTION:
    This file provides the custom instance of RegulatoryInfo on the Trade which has all the RegulatoryInfo related methods
VERSION: 1.0.25(0.25.7)
--------------------------------------------------------------------------"""
import FRegulatoryUtils
def Select(query):
    """Return a collection of FTradeRegulatoryInfo instances matching the constraint specified in the Select query"""
    return FRegulatoryUtils.Select(query, "FTradeRegulatoryInfo")


