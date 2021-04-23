"""
Date                  : 2011-08-01
Purpose               : This checks if margin requirement has been posted
                        for a specific client, if not, sends out email
                        reminders to users that are responsible
Department and Desk   : Prime Service
Requester             : Francois Henrion
Developer             : Rohan van der Walt
CR Number             :

Date            CR          Developer               Change
==========      =========   ======================  ===========================
2011-08-01      750738      Rohan van der Walt      Initial Development
2013-03-08      857456      Peter Basista           Remove _getCallAccounts
                                                    function and use the one
                                                    from the PS_Functions
                                                    module (getCallAccounts
                                                    function).
"""

import acm
import ael
import FBDPCommon

from PS_Functions import getCallAccounts, get_pb_fund_shortname
from at_logging import bp_start, getLogger
from PS_MarginValues import check_margin

LOGGER = getLogger(__name__)

calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()
PREVBUSDAY = calendar.AdjustBankingDays(TODAY, -1)

ael_variables = []
ael_variables.append(['client', 'Client Name', acm.FParty,
    acm.FCounterParty.Instances(), None, 1, 0,
    'Client Name that will be passed to all reports', None, 1])
ael_variables.append(['date', 'Check Date', 'date', None, None, 0, 0,
    'Date for which Time Series value is looked up - '
    'Empty will defaut to previous business day', None, 1])
ael_variables.append(['emailList', 'Email List', 'string', None, None,
    1, 1, 'Notification email recipients that margin requirement '
    'hasn\'t been postet yet', None, 1])
ael_variables.append(['checkEqMargin', 'Check Equity Margin', 'string',
    ['No', 'Yes'], 'Yes', 1, 0,
    'Check if Equity Margin has been posted for selected date', None, 1])
ael_variables.append(['checkFiMargin', 'Check Fixed Income Margin', 'string',
    ['No', 'Yes'], 'Yes', 1, 0,
    'Check if Fixed Income has been posted for selected date', None, 1])
ael_variables.append(['checkCreditMargin', 'Check Credit Margin', 'string',
    ['No', 'Yes'], 'No', 1, 0,
    'Check if Credit margin has been posted for prevBusiness day', None, 1])

def ael_main(parameters):
    process_name = "ps.margin.check.{0}".format(get_pb_fund_shortname(parameters['client']))

    with bp_start(process_name, ael_main_args=parameters):
        if (parameters['checkCreditMargin'] == 'Yes' or
                parameters['checkEqMargin'] == 'Yes' or
                parameters['checkFiMargin'] == 'Yes'):
            
            if parameters['date'] == None:
                parameters['date'] = PREVBUSDAY
                
            marginPosted, alreadyGenerated = check_margin(parameters['client'],
                parameters['date'], parameters['checkEqMargin'],
                parameters['checkFiMargin'], parameters['checkCreditMargin'])
            
            if not marginPosted:
                marginAccount = getCallAccounts(parameters['client']).pop().Trades()[0]
                LOGGER.warning(("Margin requirement has not been posted yet for time series date: %s,\n"
                                "Client Name: %s,\n Call Account Name: %s,\n Call Account Trade Nr: %s\n"),
                               parameters['date'],
                               parameters['client'].Name(),
                               marginAccount.Instrument().Name(),
                               marginAccount.Name())
                
                subject_field = ("WARNING: Margin Requirement not set "
                    "for Party: %s" % (parameters['client'].Name()))
                body = ("Margin requirement has not been posted yet "
                    "for time series date: %s\n\n"
                    "Client Name:\t\t%s\nCall Account Name:\t%s\n"
                    "Call Account Trade Nr:\t%s" % (parameters['date'],
                    parameters['client'].Name(),
                    marginAccount.Instrument().Name(), marginAccount.Name()))
                LOGGER.info('Sending Margin not posted warnings (Client: %s) for email recipients', 
                            parameters['client'].Name())
                for address in parameters['emailList']:
                    FBDPCommon.sendMail(address, subject_field, body)
            LOGGER.info("Completed Successfully")
        else:
            LOGGER.info('You have to check at least one margin requirement')