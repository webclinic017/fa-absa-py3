
""" Compiled: 2017-03-16 11:22:17 """

#__src_file__ = "extensions/vps/etc/FVPSHistoricExecute.py"
"""----------------------------------------------------------------------------
    (c) Copyright 2017 SunGard Front Arena. All rights reserved.
----------------------------------------------------------------------------"""
"""----------------------------------------------------------------------------
MODULE
    FVPSHistoricExecute - Stores historical valuation parameters

DESCRIPTION
    Main module for storing valuation parameters. Reload the module
    to execute the storage procedure. Make sure that FVPSVariables
    exist and that the variables are set.


----------------------------------------------------------------------------"""

import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)


SCRIPT_NAME = __name__


# Get default values from FVPSVariables and FBDPParameters
FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
                                                       'FVPSVariables')


def cb_allSelected(index, fieldValues):
    """
    Assumes that _incl field is after _base field for yield_curve,
    volatilities, correlations and stream
    """
    allSelected = int(fieldValues[index])
    ael_variables[index + 1].enable(not allSelected)
    return fieldValues


# Create selection lists for the parameter GUI
base_list = ['All', 'None']

cvCalendar = sorted([cal.Name() for cal in acm.FCalendar.Select('')])

ttStartDate = 'Date to start saving data'
ttStopDate = 'Date to stop saving data'
ttYieldCurveBase = 'Store all yield curves in the system'
ttYieldCurvesIncl = ('A list of yield curves to store. Only relevant if '
        'Store All Yield Curves is untoggled')
ttYieldCurvesExcl = ('A list of yield curves to exclude. Only relevant if '
        'Store All Yield Curves is toggled')
ttcalendar = ('If set the Keep options above will be '
        'business day adjusted according to the selected Calendar, '
        'else no such adjustment will be made.')
ttCalculate = ('If selected, the historical parameters created by the VPS '
        'script are recalculated, and new values are stored for these '
        'historical copies. Curves are also calibrated in dependency order '
        'if applicable.')

ael_variables = FBDPGui.LogVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['start_date',
                'Date to start saving VPS data',
                'string', None, None,
                1, 0, ttStartDate, None, 1],
        ['end_date',
                'Date to stop saving VPS data',
                'string', None, None,
                1, 0, ttStopDate, None, 1],
        ['yield_curve_base',
                'Store All Yield Curves',
                'int', [0, 1], 1,
                1, 0, ttYieldCurveBase, cb_allSelected, 1],
        ['yield_curves_incl',
                'Yield Curves',
                'FYieldCurve', None, None,
                0, 1, ttYieldCurvesIncl],
        ['yield_curves_excl',
                'Exceptions',
                'FYieldCurve', None, None,
                0, 1, ttYieldCurvesExcl],
        ['calendar',
                'Calendar',
                'string', cvCalendar, None,
                0, 0, ttcalendar],
        ['calculate',
                ('Recalculate created Yield Curves and Volatility Surfaces'
                        '_Advanced'),
                'int', [0, 1],
                1, 1, 0, ttCalculate, None, 1])


def ael_main(execParam):
    """
    The entry point of FVPSHistoricExecute after the Run button of the Run Script
    window is clicked.
    """
    # Import Front modules.
    import FBDPWorld
    importlib.reload(FBDPWorld)
    import FBDPPerform
    importlib.reload(FBDPPerform)
    import FBDPYieldCurveLib
    importlib.reload(FBDPYieldCurveLib)
    import FVPSHistoricPerform
    importlib.reload(FVPSHistoricPerform)

    # Parameter
    execParam['ScriptName'] = SCRIPT_NAME
    for s in execParam:
        if s in ('yield_curves_incl', 'yield_curves_excl', 'volatilities_incl',
                'volatilities_excl', 'correlations_incl', 'correlations_excl',
                'stream_incl', 'stream_excl'):
            execParam[s] = [acmObj.Name() for acmObj in execParam[s]]
        elif s in ('yield_curve_base', 'volatility_base', 'correlation_base',
                'stream_base'):
            execParam[s] = bool(execParam[s])
    # Execute script
    FBDPPerform.execute_perform(FVPSHistoricPerform.perform_vps_historic_execute, execParam)



