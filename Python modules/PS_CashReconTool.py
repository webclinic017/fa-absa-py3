"""
-------------------------------------------------------------------------------
MODULE
    PS_CashReconTool

DESCRIPTION
    Date                : 2014-06-05
    Purpose             : This module contains an implementation of Cash Recon
                          Tool for generating reconciliation reports.
    Department and Desk : Prime Services Client Coverage
    Requester           : Ruth Forssman
    Developer           : Jakub Tomaga
    CR Number           : CHNG0001994700

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
12-08-2014  2192483     Jakub Tomaga      List of active clients retrieved from
                                          Front Arena (PB_FINANCING portfolio)
11-12-2014  2512804     Jakub Tomaga      Cash Recon Tool aligned with new
                                          reporting suite.
22-01-2015  2587956     Jakub Tomaga      Start date adjusted based on end date,
                                          tool extended to compare Daily TPL,
                                          label for 'ALL CLIENTS' added.
21-06-2016  3743322     Jakub Tomaga      E-mail notifications added.
21-06-2016  3743322     Jakub Tomaga      End date added to report's filename.
2019-07-17  FAPE-47     Iryna Shcherbina  Settlement control tab.
-------------------------------------------------------------------------------
"""

import os
from datetime import datetime

import acm

import PS_CashReconReport
from at_ael_variables import AelVariableHandler
from at_email import EmailHelper
from at_logging import getLogger
from PS_FormUtils import DateField


LOGGER = getLogger(__name__)
START_DATES = DateField.get_captions([
    'Inception',
    'First Of Year',
    'Last of Previous Year',
    'First Of Month',
    'Last of Previous Month',
    'TwoBusinessDaysAgo',
    'PrevBusDay',
    'Custom Date'])

END_DATES = DateField.get_captions([
    'PrevBusDay',
    'Now',
    'Custom Date'])


OUTPUT_PATH = r"Y:\Jhb\FAReports\AtlasEndOfDay\PrimeForward\CashReconTool"
INPUT_PATH = r"Y:\Jhb\FAReports\AtlasEndOfDay"


def send_email(start_date, end_date, emails, attachments=None):
    """Send generated report."""
    env = acm.FDhDatabase['ADM'].InstanceName()
    start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d/%m/%Y')
    end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d/%m/%Y')
    body = "Hi FO,<BR><BR>" \
           "Please see attached Cash Recon Tool report for {0} - {1}.<BR><BR>" \
           "Regards,<BR>" \
           "Prime and Equities BTB team<BR><BR>".format(start_date, end_date)

    email = EmailHelper(
        body=body,
        subject="Cash Recon Tool report {} - {} ({})".format(start_date, end_date, env),
        mail_to=list(emails),
        mail_from="Front Arena {} <ABCapITRTBFrontArena@absa.africa>".format(env),
        attachments=attachments,
        sender_type=EmailHelper.SENDER_TYPE_SMTP,
        host=EmailHelper.get_acm_host())

    try:
        email.send()
    except Exception as e:
        LOGGER.error("Error sending e-mail with Recon report: {0}\n".format(e))


def custom_start_date_hook(selected_variable):
    """Enable/Disable Custom Start Date base on Start Date value."""
    start_date = ael_variables.get('start_date')
    start_date_custom = ael_variables.get('start_date_custom')

    if start_date.value == 'Custom Date':
        start_date_custom.enabled = True
    else:
        start_date_custom.enabled = False


def custom_end_date_hook(selected_variable):
    """Enable/Disable Custom End Date base on End Date value."""
    end_date = ael_variables.get('end_date')
    end_date_custom = ael_variables.get('end_date_custom')

    if end_date.value == 'Custom Date':
        end_date_custom.enabled = True
    else:
        end_date_custom.enabled = False


ael_variables = AelVariableHandler()

CLIENT_COLLECTION = PS_CashReconReport.get_client_list()
CLIENT_DEFAULT = 'ALL CLIENTS'

ael_variables.add('client_list',
                  label='Clients',
                  default=CLIENT_DEFAULT,
                  collection=CLIENT_COLLECTION,
                  alt='List of clients',
                  multiple=True)

ael_variables.add('start_date',
                  label='Start Date (relative to End Date)',
                  default='PrevBusDay',
                  collection=START_DATES,
                  alt='Start date of the cash reconciliation '
                      '(relative to the end date)',
                  hook=custom_start_date_hook)

ael_variables.add('start_date_custom',
                  label='Start Date Custom',
                  default=DateField.read_date('TwoBusinessDaysAgo'),
                  alt='Custom start date of the cash reconciliation',
                  enabled=False)

ael_variables.add('end_date',
                  label='End Date',
                  default='PrevBusDay',
                  collection=END_DATES,
                  alt='End date of the cash reconciliation',
                  hook=custom_end_date_hook)

ael_variables.add('end_date_custom',
                  label='End Date Custom',
                  default=DateField.read_date('PrevBusDay'),
                  alt='Custom end date of the cash reconciliation',
                  enabled=False)

ael_variables.add('epsilon',
                  label='Epsilon',
                  default='0.01',
                  alt='Epsilon (tolerance) for the break indication')

ael_variables.add_directory('output_path',
                            label='Output path',
                            default=OUTPUT_PATH,
                            alt='Output path for cash reconciliation reports')

ael_variables.add_directory('input_path',
                            label='Input path',
                            default=INPUT_PATH,
                            alt='Input path for static reports')

ael_variables.add_directory('settlements_input_path',
                            label='Settlements report path',
                            default=PS_CashReconReport.SETTLEMENTS_REPORT_DIR,
                            alt='Input path for settlements report')

ael_variables.add("emails",
                  label="Emails",
                  multiple=True,
                  alt="Email destinations. Use comma separated email addresses \
                       if you want to send report to multiple users.",
                  mandatory=False)

ael_variables.add_bool('lookup_enabled',
                       label='Enable Look-up',
                       tab='Look-up')

ael_variables.add('lookup_client',
                  label='Client',
                  default=CLIENT_COLLECTION[0],
                  collection=CLIENT_COLLECTION,
                  alt='Detailed lookup will be performed for this client',
                  tab='Look-up')

ael_variables.add('lookup_position',
                  label='Position',
                  default='Financed',
                  collection=['Financed', 'Fully Funded'],
                  alt='Detailed lookup will be performed for this client',
                  tab='Look-up')

ael_variables.add('lookup_instrument',
                  label='Instrument type',
                  default='CFD',
                  collection=PS_CashReconReport.INS_TYPE_VALUES,
                  alt='Detailed lookup will be performed for this client',
                  tab='Look-up')

ael_variables.add('lookup_start_date',
                  label='Start Date',
                  default=DateField.read_date('TwoBusinessDaysAgo'),
                  alt='Perform look-up from start date',
                  tab='Look-up')

ael_variables.add('lookup_end_date',
                  label='End Date',
                  default=DateField.read_date('PrevBusDay'),
                  alt='Perform look-up to end date',
                  tab='Look-up')

ael_variables.add('lookup_epsilon',
                  label='Epsilon',
                  default='0.01',
                  alt='Epsilon for lookup end',
                  tab='Look-up')

_default_path = os.path.join('C:', os.sep, 'Development', 'CashReconReports')


def ael_main(config):
    xsl_template = acm.GetDefaultContext().GetExtension(
        'FXSLTemplate', 'FObject', 'CashReconReport')
    output_path = str(config['output_path'])
    input_path = str(config['input_path'])
    settlements_input_path = str(config['settlements_input_path'])

    if config['lookup_enabled']:
        # Perform detailed break look-up
        client = config['lookup_client']
        position = config['lookup_position']
        ins_type = config['lookup_instrument']
        start_date = config['lookup_start_date']
        end_date = config['lookup_end_date']
        epsilon = config['lookup_epsilon']

        report = PS_CashReconReport.CashReconLookupReportCreator(
            start_date, end_date, client, epsilon, output_path,
            input_path, position, ins_type, xsl_template)
    else:
        # Perform general reconciliation
        if config['end_date'] == 'Custom Date':
            end_date = config['end_date_custom']
        else:
            end_date = DateField.read_date(config['end_date'])

        if config['start_date'] == 'Custom Date':
            start_date = config['start_date_custom']
        else:
            start_date = DateField.read_date(config['start_date'], end_date)

        if config['client_list'][0] == CLIENT_DEFAULT:
            client_list = CLIENT_COLLECTION
        else:
            client_list = config['client_list']
        # Create 'Cash Recon' report
        file_name = 'CashRecon_{0}_{1}_{2}'.format(
            PS_CashReconReport.FILE_PERF,
            start_date,
            end_date)
        report = PS_CashReconReport.CashReconReportCreator(
            start_date, end_date, client_list,
            config['epsilon'], output_path, input_path, settlements_input_path,
            file_name, xsl_template)

    report.create_report()
    file_path = os.path.join(output_path, report.get_filename())
    if config["emails"]:
        send_email(start_date, end_date, config["emails"], [file_path])
    LOGGER.info('Wrote secondary output to {}'.format(file_path))
    LOGGER.info('Completed Successfully')
