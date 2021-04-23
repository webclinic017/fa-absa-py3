""" Compiled: 2017-03-16 11:22:17 """

#__src_file__ = "extensions/vps/etc/FVPSHistoricPerform.py"
"""----------------------------------------------------------------------------
    (c) Copyright 2017 SunGard Front Arena. All rights reserved.
----------------------------------------------------------------------------"""
"""----------------------------------------------------------------------------
MODULE
    FVPSPerform - Called from FVPSHistoricPerform

DESCRIPTION
    Main module for deleting valuation parameters. Reload the module
    to execute the storage procedure.


----------------------------------------------------------------------------"""


import collections


import ael, acm


import FBDPCommon
import FVPSHistoricYieldCurve


# Used to shuffle arguments into FVPSx-modules
class Params(object):
    pass

def _getPerformDates(start, end, calendar, log):
    """
    Generate list of dates to run VPS Perform
    """
    
    
    log.logInfo('Getting dates.')
    acmCal = acm.FCalendar[calendar]
    datesBetween = []
    testDate = start
    if acmCal:
        while testDate <= end:
            datesBetween.append(testDate)
            testDate = FBDPCommon.toDateAEL(acmCal.AdjustBankingDays(testDate, 1))
    else:
        while testDate < end:
            datesBetween.append(testDate)
            testDate = start.add_days(1)
    log.logInfo('Found {0} dates'.format(len(datesBetween)))
    
    return datesBetween

def perform_vps_historic_execute(world, execParam):

    p = Params()
    
    p.start_date = execParam.get('start_date')
    p.end_date = execParam.get('end_date')
    p.yield_curve_base = execParam.get('yield_curve_base') == 1
    p.yield_curves_incl = execParam.get('yield_curves_incl')
    p.yield_curves_excl = execParam.get('yield_curves_excl')
    p.calculate = execParam.get('calculate') == 1
    p.iso_date = execParam.get('iso_date', 0)
    p.calendar = execParam.get('calendar')

    start_date = FBDPCommon.toDateAEL(p.start_date, None)
    assert start_date, 'Start date \'{0}\' is not a proper date.'.format(p.start_date)
    end_date = FBDPCommon.toDateAEL(p.end_date, None)
    assert end_date, 'End date \'{0}\' is not a proper date.'.format(p.end_date)

    date_array = _getPerformDates(start_date, end_date, p.calendar, world)
    for process_date in date_array:
        if (p.yield_curve_base or p.yield_curves_incl):
            world.logInfo('[VPS Execute - Yield Curves] for date %s' % process_date)
            FVPSHistoricYieldCurve.update_all_yield_curves(world, p, process_date)
