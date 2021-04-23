""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/vps/etc/FVPSDelete.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FVPSDelete - Deletes historical valuation parameters

DESCRIPTION
    Main module for deleting valuation parameters. Reload the module
    to execute the storage procedure.


----------------------------------------------------------------------------"""


import acm


import FBDPGui
import importlib
importlib.reload(FBDPGui)

field_cache = {}

SCRIPT_NAME = 'FVPSDelete'

# Get default values from FVPSVariables and FBDPParameters
FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FVPSDeleteVariables')


def disable_variables(variables, enable=0, mandat=0):

    for i in variables:
        getattr(ael_variables, i).enable(enable, mandat)

def setVarValue(index, fieldValues, enabled, default):
    ael_variables[index].enable(enabled)
    if enabled:
        fieldValues[index] = fieldValues[index] or field_cache.setdefault(
            index, default)
    else:
        field_cache[index] = fieldValues[index]
        fieldValues[index] = ''

    return fieldValues

def cb(index, fieldValues):

    if ael_variables[index][0] == 'day_or_period':
        if (fieldValues[ael_variables.day_or_period.sequenceNumber] ==
                'Single Day'):
            enable_single = 1
        else:
            enable_single = 0
        tooltip_single = ('Choose "Delete for a Single Day" to enable this '
                'field.')
        tooltip_period = 'Choose "Delete for a Period" to enable this field.'
        disable_variables(['date'], enable_single, tooltip_single)
        disable_variables(['start_date', 'end_date'], not enable_single,
                tooltip_period)
        disable_variables(['corr_matrices_base', 'corr_matrices_incl',
                'corr_matrices_excl'], not enable_single, tooltip_period)
        disable_variables(['dividend_streams_base', 'dividend_streams_incl',
                'dividend_streams_excl'], not enable_single, tooltip_period)
        #update in case of checked
        cb_allSelected(ael_variables.corr_matrices_base.sequenceNumber,
                fieldValues)
        cb_allSelected(ael_variables.dividend_streams_base.sequenceNumber,
                fieldValues)
    else:
        fieldValues = cb_allSelected(index, fieldValues)
    return fieldValues


def cb_allSelected(index, fieldValues):
    """
    Assumes that _incl field is after _base field for yield_curve,
    volatilities, correlations and stream
    """
    inclEnabled = not int(fieldValues[index]) and ael_variables[index][9] != 0
    excludedEnabled = not inclEnabled

    includedIndex = index + 1
    excludedIndex = includedIndex + 1

    fieldValues = setVarValue(includedIndex, fieldValues, inclEnabled, '')
    fieldValues = setVarValue(excludedIndex, fieldValues, excludedEnabled, '')
    return fieldValues

def cb_timebucket(index, fieldValues):

    enabled = fieldValues[index] != ''
    ael_variables.first_of_year.enable(not enabled)
    ael_variables.first_of_quarter.enable(not enabled)
    ael_variables.first_of_month.enable(not enabled)

    return fieldValues

def cb_KeepOnfirstPeriods(index, fieldValues):

    enabledYear = int(
        fieldValues[ael_variables.first_of_year.sequenceNumber]) != 0
    enabledQuarter = int(
        fieldValues[ael_variables.first_of_quarter.sequenceNumber]) != 0
    enabledMonth = int(
        fieldValues[ael_variables.first_of_month.sequenceNumber]) != 0
    enabled = enabledYear or enabledQuarter or enabledMonth
    ael_variables.timeBuckets.enable(not enabled)
    return fieldValues

cvCalendar = sorted([cal.Name() for cal in acm.FCalendar.Select('')])
cvDayOrPeriod = ('Single Day', 'Period')


ttDayOrPeriod = ('Delete valuation parameters for a series of days or one '
        'single day')
ttDate = 'Delete valuation parameters on this date'
ttStartDate = ('First day of the period for which to delete parameters '
        '(inclusive)')
ttEndDate = ('Last day of the period for which to delete parameters '
        '(inclusive)')
ttyield_curve_base = 'Delete all yield curves'
ttyield_curves_incl = 'Select the yield curves to delete'
ttyield_curves_excl = 'Select the yield curves to not delete'
ttvolatility_base = 'Delete all volatilities'
ttvolatilities_incl = 'Select the volatilities to delete'
ttvolatilities_excl = 'Select the volatilities to not delete'
ttcorr_matrices_base = 'Delete all correlation matrices'
ttcorr_matrices_incl = 'Select the correlation matrices to delete'
ttcorr_matrices_excl = 'Select the correlation matrices to not delete'
ttdividend_streams_base = 'Delete all dividend streams'
ttdividend_streams_incl = 'Select the dividend streams to delete'
ttdividend_streams_excl = 'Select the dividend streams to not delete'
ttTimeBuckets = ('Define a time bucket grouper to specify the dates on which '
        'market data should be kept i.e. not deleted. By default, data will '
        'be retained for the first day of each year, quarter and month.')
ttfirst_of_year = ('Do not delete records for the first business '
        'day of the year or first calendar day if the Calendar menu '
        'below has not been set')
ttfirst_of_quarter = ('Do not delete records for the first business '
        'day of the quarter or first calendar day if the Calendar menu '
        'below has not been set')
ttfirst_of_month = ('Do not delete records for the first business '
        'day of the month or first calendar day if the Calendar menu '
        'below has not been set')

ttcalendar = ('If set the Keep options above will be '
        'business day adjusted according to the selected Calendar, '
        'else no such adjustment will be made.')


ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['day_or_period',
                'Delete for a Single Day or a Period',
                'string', cvDayOrPeriod, None,
                1, 0, ttDayOrPeriod, cb, None],
        ['date',
                'Date to Delete',
                'string', None, None,
                0, 0, ttDate, 0, 0],
        ['start_date',
                'First Day in Period',
                'string', None, None,
                0, 0, ttStartDate, 0, 0],
        ['end_date',
                'Last Day in Period',
                'string', None, None,
                0, 0, ttEndDate, 0, 0],
        ['yield_curve_base',
                'Delete All Yield Curves',
                'int', [0, 1], None,
                0, 0, ttyield_curve_base, cb_allSelected, None],
        ['yield_curves_incl',
                'Yield Curves',
                'FYieldCurve', None, None,
                0, 1, ttyield_curves_incl, None, 1],
        ['yield_curves_excl',
                'Exceptions',
                'FYieldCurve', None, None,
                0, 1, ttyield_curves_excl, None, 1],
        ['volatility_base',
                'Delete All Volatilities', 'int',
                [0, 1], None, 1, 0, ttvolatility_base, cb, None],
        ['volatilities_incl',
                'Volatilities',
                'FVolatilityStructure', None, None,
                0, 1, ttvolatilities_incl],
        ['volatilities_excl',
                'Exceptions',
                'FVolatilityStructure', None, None,
                0, 1, ttvolatilities_excl],
        ['corr_matrices_base',
                'Delete All Correlation Matrices',
                'int', [0, 1], None,
                0, 0, ttcorr_matrices_base, cb_allSelected, None],
        ['corr_matrices_incl',
                'Correlation Matrices',
                'FCorrelationMatrix', None, None,
                0, 1, ttcorr_matrices_incl, None, 1],
        ['corr_matrices_excl',
                'Exceptions',
                'FCorrelationMatrix', None, None,
                0, 1, ttcorr_matrices_excl, None, 1],
        ['dividend_streams_base',
                'Delete All Dividend Streams',
                'int', [0, 1], None,
                0, 0, ttdividend_streams_base, cb_allSelected, None],
        ['dividend_streams_incl',
                'Dividend Streams',
                'FDividendStream', None, None,
                0, 1, ttdividend_streams_incl, None, 1],
        ['dividend_streams_excl',
                'Exceptions',
                'FDividendStream', None, None,
                0, 1, ttdividend_streams_excl, None, 1],
        ['timeBuckets',
                'Keep on',
                'FStoredTimeBuckets', None, None,
                0, 1, ttTimeBuckets, cb_timebucket, 1],
        ['first_of_year',
                'Keep first day of Year',
                'int', ['1', '0'], None,
                1, 0, ttfirst_of_year, cb_KeepOnfirstPeriods, 1],
        ['first_of_quarter',
                'Keep first day of Quarter',
                'int', ['1', '0'], None,
                1, 0, ttfirst_of_quarter, cb_KeepOnfirstPeriods, 1],
        ['first_of_month',
                'Keep first day of Month',
                'int', ['1', '0'], None,
                1, 0, ttfirst_of_month, cb_KeepOnfirstPeriods, 1],
        ['calendar',
                'Calendar',
                'string', cvCalendar, None,
                0, 0, ttcalendar]
)


def ael_main(execParam):
    """
    The entry point of FVPSDelete after the Run button of the Run Script
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
        if s in ('yield_curve_base', 'volatility_base',
                'corr_matrices_base', 'dividend_streams_base',
                'first_of_year', 'first_of_quarter',
                'first_of_month', 'first_of_week'):
            execParam[s] = bool(execParam[s])
    # Execute script
    FBDPPerform.execute_perform(FVPSPerform.perform_vps_delete, execParam)
