"""-----------------------------------------------------------------------------
PROJECT                 :  Prime Services
PURPOSE                 :  Generate the call account statement.
DEPATMENT AND DESK      :  Prime Services
REQUESTER               :
DEVELOPER               :  Hynek Urban
CR NUMBER               :  1712088
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer              Description
--------------------------------------------------------------------------------
2014-01-13  1712088 Hynek Urban             Initial version - moved from
                                            PS_ReportControllerFunctions.

"""

import acm
import ael

from PS_Functions import getCallAccounts, get_pb_fund_shortname
from PS_MarginValues import check_margin, touch_margin
from PS_ReportControllerFunctions2 import (ReportDescription as RD,
    add_report_tabs, generate_reports)

from at_logging import bp_start, getLogger

LOGGER = getLogger(__name__)

calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()
PREVBUSDAY = calendar.AdjustBankingDays(TODAY, -1)

REPORT_DESCRIPTIONS = [
    RD(
        name='Light cash',
        filename='Report_CallAccount',
        key_prefix='PS2_LCASH',
    ),
    RD(
        name='Heavy cash',
        filename='File_CallAccount',
        key_prefix='PS2_LCASH',
    ),
]

ael_variables = []
add_report_tabs(ael_variables, REPORT_DESCRIPTIONS)

ael_variables.extend([['checkEqMargin', 'Check Equity Margin',
        'string', ['No', 'Yes'], 'Yes', 1, 0,
        'Check if Equity Margin has been posted for prevBusiness day',
        None, 1],
        ['checkFiMargin', 'Check Fixed Income Margin',
        'string', ['No', 'Yes'], 'Yes', 1, 0,
        'Check if Fixed Income has been posted for prevBusiness day', None, 1],
        ['checkCreditMargin', 'Check Credit Margin',
        'string', ['No', 'Yes'], 'No', 1, 0,
        'Check if Credit margin has been posted for prevBusiness day',
        None, 1],
        ['override', 'Override Margin check and Previous Run check',
        'string', ['No', 'Yes'], 'No', 1, 0,
        'If "No" will check if margin has been posted for prevBusinessDay '
        'before generating reports.\nIf reports have already been generated '
        'it will also regenerate them.', None, 1],
        ['emailList', 'Report Generation Notification Emails',
        'string', None, None, 0, 1,
        'Notification emails when margin not set for today '
        'and reports not generated', None, 1]])

def ael_main(configuration):
    """Check margins and generate the client statement."""
    counterparty = acm.FParty[configuration['clientName']]
    process_name = "ps.margin.statement.{0}".format(get_pb_fund_shortname(counterparty))
    
    with bp_start(process_name, ael_main_args=configuration):
        
        margin_posted, already_generated = check_margin(
            counterparty,
            PREVBUSDAY,
            configuration['checkEqMargin'],
            configuration['checkFiMargin'],
            configuration['checkCreditMargin'])
        
        if configuration['override'] == 'Yes' or not already_generated:
            margin_accounts = getCallAccounts(acm.FParty[configuration['clientName']])
            margin_account = margin_accounts.pop().Trades()[0]
            
            if margin_posted or configuration['override'] == "Yes":
                generate_reports(configuration, REPORT_DESCRIPTIONS, [])
                
            if margin_posted:
                touch_margin(acm.FParty[configuration['clientName']],
                    PREVBUSDAY,
                    configuration['checkEqMargin'],
                    configuration['checkFiMargin'],
                    configuration['checkCreditMargin'])
                
                if configuration['emailList']:
                    LOGGER.info('Prime Services Reports generated with Call Account Statement - Sending Notifications to:%s',
                                configuration['emailList'])
                    for address in configuration['emailList']:
                        ael.sendmail(address, 'Prime Services Reports Generated '
                            'for Account Nr %s' % margin_account.Name(),
                            'Hi\n\nPrime Services Reports were generated '
                            'successfully\nClient: %s\nCall Account Nr: %s' % 
                            (margin_account.Counterparty().Name(),
                            margin_account.Name()))
            else:
                if configuration['override'] == 'Yes':
                    LOGGER.warning('Margin requirement missing - '
                        'CALL ACCOUNT STATEMENT GENERATED BECAUSE '
                        'OVERRIDE IS SET - Notifications not sent')
                else:
                    LOGGER.warning('Margin requirement missing - '
                        'CALL ACCOUNT STATEMENT NOT GENERATED - '
                        'Notifications not sent')
    
        if already_generated:
            if configuration['override'] == 'Yes':
                LOGGER.info('Call account statement regenerated using override functionality.')
            else:
                LOGGER.info('Call account statement and notification '
                    'were not generated because Margin has already been Touched '
                    'by System Process. Use override if force generation needed.')
                
        LOGGER.info('Completed Successfully')
