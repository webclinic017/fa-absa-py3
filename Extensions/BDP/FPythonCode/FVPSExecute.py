""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/vps/etc/FVPSExecute.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FVPSExcecute - Stores historical valuation parameters

DESCRIPTION
    Main module for storing valuation parameters. Reload the module
    to execute the storage procedure. Make sure that FVPSVariables
    exist and that the variables are set.


----------------------------------------------------------------------------"""


import FBDPGui
import importlib
importlib.reload(FBDPGui)


SCRIPT_NAME = 'FVPSExecute'


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


ttYieldCurveBase = 'Store all yield curves in the system'
ttYieldCurvesIncl = ('A list of yield curves to store. Only relevant if '
        'Store All Yield Curves is untoggled')
ttYieldCurvesExcl = ('A list of yield curves to exclude. Only relevant if '
        'Store All Yield Curves is toggled')
ttVolatilityBase = 'Store all volatilities in the system'
ttVolatilitiesIncl = ('A list of volatilities to store. Only relevant if '
        'Store All Volatilities is untoggled')
ttVolatilitiesExcl = ('A list of volatilities to exclude. Only relevant if '
        'Store All Volatilities is toggled')
ttCorrelationBase = 'Store all Correlation Matrices in the system'
ttCorrelationsIncl = ('A list of correlations to store. Only relevant if '
        'Store All Correlation Matrices is untoggled')
ttCorrelationsExcl = ('A list of correlations to exclude. Only relevant if '
        'Store All Correlation Matrices is toggled')
ttStreamBase = 'Store all dividend streams in the system.'
ttStreamIncl = ('A list of dividend streams to store. Only relevant if '
        'Store All Dividend Streams is untoggled')
ttStreamExcl = ('A list of dividend streams to exclude. Only relevant if '
        'Store All Dividend Streams is toggled')
ttCalculate = ('If selected, the historical parameters created by the VPS '
        'script are recalculated, and new values are stored for these '
        'historical copies. Curves are also calibrated in dependency order '
        'if applicable.')
ttRealtimeUpdated = ('If selected created historical yield curves will '
        'have setting \'RealTimeUpdated\' unchanged in order to enable '
        'full coverage for yield curve risk in historical valuation. '
        'If this setting is cleared \'RealTimeUpdated\' is always '
        'disabled for the created curves.')

ael_variables = FBDPGui.LogVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
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
        ['volatility_base',
                'Store All Volatilities',
                'int', [0, 1], 1,
                1, 0, ttVolatilityBase, cb_allSelected, 1],
        ['volatilities_incl',
                'Volatilities',
                'FVolatilityStructure', None, None,
                0, 1, ttVolatilitiesIncl],
        ['volatilities_excl',
                'Exceptions',
                'FVolatilityStructure', None, None,
                0, 1, ttVolatilitiesExcl],
        ['correlation_base',
                'Store All Correlation Matrices',
                'int', [0, 1], 1,
                1, 0, ttCorrelationBase, cb_allSelected],
        ['correlations_incl',
                'Correlations',
                'FCorrelationMatrix', None, None,
                0, 1, ttCorrelationsIncl],
        ['correlations_excl',
                'Exceptions',
                'FCorrelationMatrix', None, None,
                0, 1, ttCorrelationsExcl],
        ['stream_base',
                'Store All Dividend Streams',
                'int', [0, 1], 1,
                1, 0, ttStreamBase, cb_allSelected],
        ['stream_incl',
                'Dividend Streams',
                'FDividendStream', None, None,
                0, 1, ttStreamIncl],
        ['stream_excl',
                'Exceptions',
                'FDividendStream', None, None,
                0, 1, ttStreamExcl],
        ['calculate',
                ('Recalculate created Yield Curves and Volatility Surfaces'
                        '_Advanced'),
                'int', [0, 1],
                0, 1, 0, ttCalculate, None, 1],
        ['RealTimeUpdatedUnchanged',
                ('Create curves with RealTimeUpdated setting unchanged'
                        '_Advanced'),
                'int', [0, 1],
                0, 1, 0, ttRealtimeUpdated, None, 1])


def ael_main(execParam):
    """
    The entry point of FVPSExecute after the Run button of the Run Script
    window is clicked.
    """
    # Import Front modules.
    import FBDPWorld
    importlib.reload(FBDPWorld)
    import FBDPPerform
    importlib.reload(FBDPPerform)
    import FBDPYieldCurveLib
    importlib.reload(FBDPYieldCurveLib)
    import FVPSPerform
    importlib.reload(FVPSPerform)
    import FVPSYieldCurve
    importlib.reload(FVPSYieldCurve)
    import FVPSVolatility
    importlib.reload(FVPSVolatility)
    import FVPSCorrelationMatrix
    importlib.reload(FVPSCorrelationMatrix)
    import FVPSDividendStream
    importlib.reload(FVPSDividendStream)
    # Parameter
    execParam['ScriptName'] = SCRIPT_NAME
    for s in execParam:
        if s in ('yield_curve_base', 'volatility_base', 'correlation_base',
                'stream_base'):
            execParam[s] = bool(execParam[s])
    # Execute script
    FBDPPerform.execute_perform(FVPSPerform.perform_vps_execute, execParam)
