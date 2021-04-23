""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/cash_flow_agg/etc/FCashFlowAggregation.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE

    FCashFlowAggregation.py - Script for cash flow aggregation.

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""

# Import Front modules
import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)


SCRIPT_NAME = 'CashFlowAggregation'

#==============================================================================
# Main
#==============================================================================

_strToday = 'Today'
_valToday = acm.Time.DateToday()


# ======== AEL variables setup - candidate values =============================

_cvDateList = [_valToday, _strToday]
_cvToggles = [True, False]


# ======== AEL variables setup - inserters ====================================

_qIns = FBDPGui.insertInstruments(instype=('Deposit',))


# ======== AEL variables setup - tool tips ====================================

_ttDate = 'The aggregation date.'
_ttDeaggregate = 'Open up archived cash flows after aggregation date.'
_ttInstruments = 'The instruments to be handled.'


# ======= AEL variables =======================================================

ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['deaggregate',
                'Deaggregate',
                'bool', _cvToggles, False,
                1, 0, _ttDeaggregate, None, 1],
        ['date',
                'Aggregation Date',
                'string', _cvDateList, _strToday,
                1, 0, _ttDate, None, 1],
        ['instruments',
                'Instrument(s)',
                'FInstrument', None, _qIns,
                1, 1, _ttInstruments, None, 1])


def ael_main(execParam):
    """
    The entry point of FCashFlowAggregation after the Run button of the Run
    Script window is clicked.
    """
    # Import Front modules.
    import FBDPWorld
    importlib.reload(FBDPWorld)
    import FBDPPerform
    importlib.reload(FBDPPerform)
    import FCashFlowAggregationPerform
    importlib.reload(FCashFlowAggregationPerform)
    # Parameter
    execParam['ScriptName'] = SCRIPT_NAME
    from FBDPCommon import toDate
    execParam['date'] = toDate(execParam['date'])
    from FBDPCommon import convertEntityList
    execParam['instruments'] = convertEntityList(execParam['instruments'],
            None)
    # Execute script
    FBDPPerform.execute_perform(FCashFlowAggregationPerform.perform, execParam)
