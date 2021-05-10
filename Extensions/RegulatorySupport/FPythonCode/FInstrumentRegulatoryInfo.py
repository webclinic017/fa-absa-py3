"""------------------------------------------------------------------------
MODULE
    FInstrumentRegulatoryInfo -
DESCRIPTION:
    This file provides the custom instance of RegulatoryInfo on the Instrument which has all the RegulatoryInfo related methods
VERSION: 1.0.25(0.25.7)
--------------------------------------------------------------------------"""
import FRegulatoryUtils
def Select(query):
    """Return a collection of FInstrumentRegulatoryInfo instances matching constraint specified in the Select query"""
    return FRegulatoryUtils.Select(query, "FInstrumentRegulatoryInfo")


