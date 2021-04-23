"""
-------------------------------------------------------------------------------
MODULE
    yield_curve_report

DESCRIPTION
    Date                : 2014-04-11
    Purpose             : This module contains an implementation of generating
                          yield curve report.
    Department and Desk : Credit Desk
    Requester           : Zine Mdleleni
    Developer           : Jakub Tomaga
    CR Number           : CHNG0001886098

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
10/07/2014  2112348     Jakub Tomaga    Report's format changed to excel-tab,
                                        FYieldCurve object returned from GUI.
-------------------------------------------------------------------------------
"""

import math

import os
import acm
from at_ael_variables import AelVariableHandler
import at_report


class YieldCurveReport(at_report.CSVReportCreator):
    """Creates the report."""
    def __init__(self, yield_curve, file_name, file_suffix, path):
        super(YieldCurveReport, self).__init__(file_name, file_suffix, path,
            {'dialect': 'excel-tab'})

        self.yield_curve = yield_curve

    def _collect_data(self):
        """Collect data relevant for the report."""

        # Get data from instrument spreads
        for spread in self.yield_curve.InstrumentSpreads():
            instrument_name = spread.Instrument().Name()
            if spread.Benchmark() is not None:
                underlying_instrument = spread.Benchmark().Name()
            else:
                underlying_instrument = ''

            if spread.UnderlyingYieldCurve() is not None:
                underlying_yield_curve = spread.UnderlyingYieldCurve().Name()
            else:
                underlying_yield_curve = ''

            spread_value = spread.Spread()
            spread_type = spread.SpreadType()
            price_type = spread.PriceType()

            price = acm.FInstrument[instrument_name].used_price()
            market_price = price if not math.isnan(price) else ''

            # Construct the output line
            line = (
                instrument_name,
                underlying_instrument,
                underlying_yield_curve,
                spread_value,
                spread_type,
                price_type,
                market_price
            )

            # Append the line to the output file
            self.content.append(line)

    def _header(self):
        """Return columns of the header."""
        header = [
            'Instrument',
            'Und Ins 1',
            'Und YC',
            'Spread',
            'Spread Type',
            'Price Type',
            'Market Price'
        ]

        return header

    @staticmethod
    def log(message):
        """Basic console logging with time stamp prefix."""
        print("{0}: {1}".format(acm.Time.TimeNow(), message))


ael_variables = AelVariableHandler()
ael_variables.add('yield_curve', label='Yield curve',
    default='ZAR-CORPBONDS-SPREADS', alt='Yield curve',
    collection=acm.FYieldCurve.Select(''),
    cls='FYieldCurve')

ael_variables.add('filename', label='Filename',
    default='YieldCurveReport', alt='Filename')

ael_variables.add('path', label='Path',
    default='F:/', alt='Path')


def ael_main(config):
    """The main entry point of the Run Script window."""
    report = YieldCurveReport(yield_curve=config['yield_curve'],
        file_name=config['filename'], file_suffix='xls',
        path=config['path'])

    report.log('Generating yield curve report...')
    report.create_report()

    filename = os.path.join(config['path'],
        '.'.join([config['filename'], 'xls']))
    report.log('Wrote secondary output to {0}'.format(filename))
    report.log('Completed Successfully')
