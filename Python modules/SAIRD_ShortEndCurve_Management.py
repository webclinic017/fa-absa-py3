"""
-------------------------------------------------------------------------------
MODULE
    SAIRD_ShortEndCurve_Management

DESCRIPTION
    Date                : 05/08/2014
    Purpose             : Short end curve management module
    Department and Desk : Middle Office
    Requester           : Helder Loio
    Developer           : Jakub Tomaga
    CR Number           : CHNG0002036323

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
02/10/2014  2325358     Jakub Tomaga    Support for price testing added.
-------------------------------------------------------------------------------
"""

import os
from at_ael_variables import AelVariableHandler
from ShortEndProvisionReport import (ResetRiskReport, ProvisionPerResetReport,
    ProvisionPerResetBucketReportCreator)


def instruments_hook(selected_variable):
    instruments = selected_variable.handler.get('PriceTestingInstruments')
    if selected_variable.value == 'true':
        instruments.enabled = True
    else:
        instruments.enabled = False


ael_variables = AelVariableHandler()
ael_variables.add('InputType',
    label='Report Input Type',
    collection=['Filter', 'Portfolio'],
    default='Filter')

ael_variables.add('Portfolio',
    label='Portfolio',
    cls='FPhysicalPortfolio',
    mandatory=False,
    multiple=True)

ael_variables.add('TrdFilter',
    label='Trade Filter',
    cls='FTradeSelection',
    mandatory=False,
    multiple=True)

ael_variables.add('ReportType',
    label='Report Type',
    collection=['Reset Risk', 'Provision Per Reset Bucket',
        'Provision Per Reset'],
    default='Provision Per Reset')

ael_variables.add('OutputType',
    label='Output Type',
    collection=['Excel', 'CSV'],
    default='Excel')

ael_variables.add('Outpath',
    label='Output Path',
    default='/services/frontnt/Task/')

ael_variables.add('Currency',
    label='Currency',
    cls='FCurrency',
    default='ZAR',
    multiple=True)

ael_variables.add('Curve',
    label='Forward Yield Curve',
    cls='FYieldCurve',
    default='ZAR-SWAP',
    multiple=True)

ael_variables.add_bool('PriceTesting',
    label='Price Testing',
    default=False,
    hook=instruments_hook)

ael_variables.add('PriceTestingInstruments',
    label='Instruments',
    multiple=True,
    cls='FInstrument',
    enabled=False,
    mandatory=False)


def ael_main(config):
    if config['OutputType'] == 'CSV':
        file_suffix = 'csv'
        csv_writer_parameters = None
    else:
        file_suffix = 'xls'
        csv_writer_parameters = {'dialect': 'excel-tab'}

    output_path = config['Outpath']
    input_type = config['InputType']
    if input_type == 'Portfolio':
        source = config['Portfolio'][0]
    else:
        source = config['TrdFilter'][0]

    yield_curve = config['Curve'][0]
    currency = config['Currency'][0]
    report_type = config['ReportType']

    if config['PriceTesting']:
        market_rate_instruments = config['PriceTestingInstruments']
    else:
        market_rate_instruments = None

    if report_type == 'Reset Risk':
        collection = ResetRiskReport(file_suffix, output_path,
            csv_writer_parameters, source, yield_curve,
            currency, market_rate_instruments)
        collection.create_reports()
    elif report_type == 'Provision Per Reset':
        collection = ProvisionPerResetReport(file_suffix,
            output_path, csv_writer_parameters, source, yield_curve,
            currency, market_rate_instruments)
        collection.create_reports()
    elif report_type == 'Provision Per Reset Bucket':
        file_name = '_'.join([output_path + 'Data_File', input_type,
            source.Name(), currency.Name(), yield_curve.Name(),
            report_type.replace(' ', ''), 'Per_Reset'])
        report_parameters = {
            'file_name': file_name,
            'file_suffix': file_suffix,
            'path': output_path,
            'csv_writer_parameters': csv_writer_parameters
        }
        report = ProvisionPerResetBucketReportCreator(report_parameters,
            source, yield_curve, currency, market_rate_instruments)
        report.create_report()
        print('Wrote secondary output to {0}'.format(os.path.join(
            report_parameters['path'], '.'.join([report_parameters['file_name'], report_parameters['file_suffix']]))))

        print('Completed successfully')
