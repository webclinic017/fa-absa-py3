"""
-------------------------------------------------------------------------------
MODULE
    PS_ResetRisk

DESCRIPTION
    Date                : 05/08/2014
    Purpose             : Reset Risk report for PRIME clients.
    Department and Desk : Middle Office
    Requester           : Helder Loio
    Developer           : Jakub Tomaga
    CR Number           : CHNG0002036323

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
"""

import os
import acm
from at_ael_variables import AelVariableHandler
from ShortEndProvisionReport import ProvisionPerResetClientReportCreator
from PS_FormUtils import DateField


def _convertToParamDictionary(ReportControllerDictionary, reportName):
    '''
    Gets called from report controller on custom reports to return a compatible report dictionary
    '''
    result = {'InputType':ReportControllerDictionary['InputType_' + reportName],
            'Portfolio':ReportControllerDictionary['Portfolio_' + reportName],
            'TrdFilter':ReportControllerDictionary['TrdFilter_' + reportName],
            'ReportType':ReportControllerDictionary['ReportType_' + reportName],
            'OutputType':ReportControllerDictionary['OutputType_' + reportName],
            'Outpath':ReportControllerDictionary['OutputPath'],
            'Currency':ReportControllerDictionary['Currency_' + reportName],
            'Curve':ReportControllerDictionary['Curve_' + reportName]
            }

    # TODO: Consolidate after the old report controller is removed.
    if 'date_Descriptor' in ReportControllerDictionary:
        if ReportControllerDictionary['date_Descriptor'] != '':
            result['fileName'] = ReportControllerDictionary['fileID_Descriptor'] + '_' + ReportControllerDictionary['Filename_' + reportName] + '_' + str(ReportControllerDictionary['date_Descriptor'])
        else:
            result['fileName'] = ReportControllerDictionary['fileID_Descriptor'] + '_' + ReportControllerDictionary['Filename_' + reportName] + '_' + ReportControllerDictionary['date_Descriptor']
    else:
        if reportName == 'Heavy Reset Risk': # PS_ReportController2
            date_suffix = DateField.read_date(ReportControllerDictionary['date_SoftBroker'],
                default=acm.Time.DateToday()).replace('-', '')
            result['fileName'] = ReportControllerDictionary['fileID_SoftBroker'] + '_' +\
                ReportControllerDictionary['Filename_' + reportName] + '_' + date_suffix
        else: # Old ReportController
            result['fileName'] = ReportControllerDictionary['fileID_SoftBroker'] + '_' + ReportControllerDictionary['Filename_' + reportName]

    return result


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
    label='Yield Curve',
    cls='FYieldCurve',
    default='ZAR-SWAP',
    multiple=True)

ael_variables.add('fileName',
    label='File Name',
    default='Provision_Per_Reset_Day')


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
    file_name = config['fileName']

    report_parameters = {
        'file_name': file_name,
        'file_suffix': file_suffix,
        'path': output_path,
        'csv_writer_parameters': csv_writer_parameters
    }
    report = ProvisionPerResetClientReportCreator(report_parameters, source,
        yield_curve, currency)
    report.create_report()
    print('Wrote secondary output to {0}'.format(os.path.join(report_parameters['path'], '.'.join([
        report_parameters['file_name'], report_parameters['file_suffix']]))))

    print('Completed Successfully')
