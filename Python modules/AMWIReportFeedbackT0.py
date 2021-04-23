"""----------------------------------------------------------------------------------------------------------
MODULE                  :       AMWIReportFeedback
PROJECT                 :       OTC Clearing
PURPOSE                 :       This module will be used to pick up intra-day T+0 recon breaks, and notify the
                                relevant people of the breaks via an email
                                Extracted file name from Markit Wire:
                                Y:/Jhb/FALanding/Prod/MarkitWire/DEbaseline.csv
DEPARTMENT AND DESK     :       ABSA Capital / IRD Desk and Prime Services Desk
REQUESTER               :       Helder Loio
DEVELOPER               :       Delsayo Lukhele
DEPENDENCY 1            :       Deal Extractor utility on production AMWI Windows Server: JHBPSM020000565
DEPENDENCY 2            :       Source file: Y:/Jhb/FAReports/AtlasEndOfDay/MarkitWireDEbaseline.csv
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer           Description
-------------------------------------------------------------------------------------------------------------
2018-12-13    CHNG0003115685    Delsayo Lukhele        Initial Implementation from the module AMWIReportFeedback
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    This module will be used to pick up intra-day T+0 recon breaks, and notify the relevant people of the breaks
    via an email
"""

import csv
import acm
from datetime import datetime
from AMWIReportFeedback import process_notification, LoadFATrades, GetFATradesRelatedToMarkitWireTrade, \
    ExecuteReconChecks, DetermineStartDate, BiDirectionalCheckForMissingTrades

calendar_to_adjust = acm.FCalendar['ZAR Johannesburg']
date_today = acm.Time.DateToday()
recon_start_date = calendar_to_adjust.AdjustBankingDays(date_today, -5)
RECON_ITEMS = []

def CheckAllMarkitWireTrades(parameters, start_date, reader):
    """
    Pull the Markit Wire trades from the Deal Extractor file and run them through against
    the Front Arena found trades
    the latest Markit Wire deal extractor file. This is a full population download from Markit Serv
    Default source: Y:/Jhb/FALanding/Prod/MarkitWire/DEbaseline.csv
    """
    RECON_ITEMS[:] = []
    markitwire_list = []
    ftrades = LoadFATrades(recon_start_date)
    for markitwire_trade in reader:
        if markitwire_trade[0] == '' or markitwire_trade[0] == 'TradeId':
            continue

        try:
            username = markitwire_trade[2]

            if markitwire_trade[185] != 'Withdrawn' and markitwire_trade[7] not in ('Cancelled', 'Allocated', 'Novated'):
                print('Reconciling MW{0}\n'.format(markitwire_trade[0]))
                markitwire_list.append(markitwire_trade[0])
                trades = GetFATradesRelatedToMarkitWireTrade(ftrades, markitwire_trade[0])
                ExecuteReconChecks(trades, markitwire_trade, parameters, start_date)
        except Exception as e:
            print('Error: Failed to reconcile deal', markitwire_trade[0], str(e))

    if parameters['mwMWCheckMissingTrades']:
        BiDirectionalCheckForMissingTrades(ftrades, start_date, markitwire_list)

ael_variables = \
    [
        ['mwSourceCSVFile', 'AMWI Source CSV file', 'string', None,
         'Y:/Jhb/FALanding/Prod/MarkitWire/DEbaseline.csv', 1],
        ['mwOutputCSV', 'AMWI Output CSV file', 'string', None,
         'C:/Users/ABDL333/Desktop/Mighty/DEbaselineOutput_' + str(datetime.today()).replace(':', '_').
             replace('.', '_').replace('-', '_') + '.csv', 1],
        ['mwEmailGroups', 'AMWI Emailing groups', 'string', None, 'Delsayo.Lukhele@absa.co.za', 1],
        ['mwErrorEmailGroups', 'AMWI Error groups', 'string', None, 'Delsayo.Lukhele@absa.co.za', 1],
        ['mwFromEmail', 'AMWI From Email Address', 'string', None, 'Delsayo.Lukhele@absa.co.za', 1],        
        ['mwMWT0Days', 'T0 Days', 'string', None, 0, 1],
        ['mwCheckMWPopulation', 'Run Entire Historical Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['mwMWNominalDirectionCheck', 'Markit Wire Nominal Direction Check', 'bool', [True, False], True, 0, 0,
         'Roll back', None, 1],
        ['mwMWNominalCheck', 'Markit Wire Nominal Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['mwMWStartEndDateCheck', 'Markit Wire Start End Date Check', 'bool', [True, False], True, 0, 0, 'Roll back',
         None, 1],
        ['mwMWDuplicatePaymentsCheck', 'Markit Wire Duplicate Payments Check', 'bool', [True, False], True, 0, 0,
         'Roll back', None, 1],
        ['mwMWStatusCheck', 'Markit Wire Status Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['mwMWFixedRateCheck', 'Markit Wire Fixed Rate Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['mwMWDuplicateCheck', 'Markit Wire Duplicate Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['mwMWIncorrectUserCheck', 'Markit Wire Incorrect User', 'bool', [True, False], True, 0, 0, 'Roll back', None,
         1],
        ['mwMWInterDeskChecks', 'Markit Wire Inter-Desk Checks', 'bool', [True, False], True, 0, 0, 'Roll back', None,
         1],
        ['mwMWDefaultChecks', 'Markit Wire Default Checks', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['mwMWMirrorChecks', 'Markit Wire Intern Mirror Checks', 'bool', [True, False], False, 0, 0, 'Mirrors', None, 1],
        ['mwMWStstusComparison', 'Markit Wire Status Check', 'bool', [True, False], True, 0, 0, 'Statuses', None, 1],
        ['mwMWValueDateCheck', 'Markit Wire Value Date Check', 'bool', [True, False], True, 0, 0, 'ValueDate', None, 1],
        ['mwMWSpreadCheck', 'Markit Wire Spread Check', 'bool', [True, False], True, 0, 0, 'Spread', None, 1],
        ['mwMWInitialRate', 'Markit Wire Initial Rate Check', 'bool', [True, False], True, 0, 0, 'InitialRate', None,
         1],
        ['mwMWRollingPeriod', 'Markit Wire Rolling Period Check', 'bool', [True, False], True, 0, 0, 'RollingPeriod',
         None, 1],
        ['mwMWClearTradeAttributes', 'Markit Wire Clear Trades Attributes Check', 'bool', [True, False], True, 0, 0,
         'Cleared Trade Attributes', None, 1],
        ['mwMWCheckMissingTrades', 'Markit Wire Missing Trades Check', 'bool', [True, False], True, 0, 0,
         'Markit Wire Missing Trades Check', None, 1]
    ]


def ael_main(parameters):
    mw_inception_date = datetime.strptime(recon_start_date, '%Y-%m-%d').date()
    print(mw_inception_date)
    aging = int(parameters['mwMWT0Days']) * -1
    start_date = DetermineStartDate(parameters['mwCheckMWPopulation'], mw_inception_date, aging)

    print('Run the AMWI Recon at {0} for trades from {1} to {2}'.format(datetime.today(), start_date,
                                                                        datetime.today()))

    print('These are the input parameters:')
    for param in parameters:
        if parameters[param]:
            print(param, ': ', parameters[param])

    with open(parameters['mwSourceCSVFile'], 'rt') as deal_extractor:
        reader = csv.reader(deal_extractor)
        source_rows = list(reader)
    
    CheckAllMarkitWireTrades(parameters, start_date, source_rows)

    RECON_ITEMS.sort(key=lambda k: (k[6]))

    email_subject = 'MarkitWire Recon Report {0} - {1}'.format(start_date, str(datetime.now().date()))
    process_notification(parameters['mwOutputCSV'], parameters['mwFromEmail'], parameters['mwEmailGroups'],
                         email_subject)

    print('AMWI Recon completed succesfully at ' + str(datetime.today()))
