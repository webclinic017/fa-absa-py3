"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FOperationsTradesFromInstrument

DESCRIPTION
    This module is used to improve the behaviour of the core FOperationsTradesFromInstrument
    module.

    The following customisations have been done:

    - Reimplementation of GetTradesFromInstrument (and replacement of all private helper functions) to:
        - Improve extremely poor performance of core implementation (caused
          primarily by use of __AddToListNoDuplicates).
        - Improve selection of derivatives to find derivatives recursively.
        - Improve selection of TRSes to include instrument types other than Stocks.
        - Fix coding issues such as iteration over FPersistentSets.
        - Improve code structure.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2021-03-29      FAOPS-1140      Cuen Edwards                                    Initial implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTradesFromInstrument.py"
import acm
import FOperationsUtils as Utils
from FOperationsEnums import InsType, LegType


def GetTrades(obj):
    trades = list()
    if obj.IsKindOf(acm.FTrade):
        trades.append(obj)
    elif obj.IsKindOf(acm.FInstrument):
        for trade in GetTradesFromInstrument(obj):
            trades.append(trade)
    return trades


def GetTradesFromInstrument(instrument):
    instruments = set()
    instruments.add(instrument)
    instruments.update(_get_derivatives_for_instrument(instrument))
    instruments.update(_get_trses_for_instrument(instrument))
    instruments.update(_get_combinations_for_instruments(instruments))
    return _get_trades_for_instruments(instruments)


def _get_derivatives_for_instrument(instrument):
    derivatives = set()
    select_expression = 'underlying = {oid}'.format(oid=instrument.Oid())
    for derivative in acm.FInstrument.Select(select_expression).AsArray():
        derivatives.add(derivative)
        # Core version of this doesn't recursively find derivatives...
        derivatives.update(_get_derivatives_for_instrument(derivative))
    return derivatives


def _get_trses_for_instrument(instrument):
    trses = set()
    # Core version only looks for TRSes related to Stocks...
    query = acm.CreateFASQLQuery(acm.FLeg, 'AND')
    query.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', InsType.TOTAL_RETURN_SWAP))
    query.AddAttrNode('LegType', 'EQUAL', Utils.GetEnum('LegType', LegType.TOTAL_RETURN))
    query.AddAttrNode('IndexRef.Oid', 'EQUAL', instrument.Oid())
    for leg in query.Select():
        trses.add(leg.Instrument())
    return trses


def _get_combinations_for_instruments(instruments):
    combinations = set()
    for instrument in instruments:
        combinations.update(_get_combinations_for_instrument(instrument))
    return combinations


def _get_combinations_for_instrument(instrument):
    combinations = set()
    select_expression = 'instrument = {oid}'.format(oid=instrument.Oid())
    combination_links = acm.FCombInstrMap.Select(select_expression).AsArray()
    for combination_link in combination_links:
        combination = combination_link.Combination()
        combinations.add(combination)
        combinations.update(_get_combinations_for_instrument(combination))
    return combinations


def _get_trades_for_instruments(instruments):
    trades = list()
    for instrument in instruments:
        trades.extend(instrument.Trades().AsArray())
    return trades
