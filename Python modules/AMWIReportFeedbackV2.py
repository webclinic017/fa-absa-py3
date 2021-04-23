"""----------------------------------------------------------------------------------------------------------
MODULE                  :       AMWIReportFeedbackV2
PROJECT                 :       OTC Clearing
PURPOSE                 :       This module will be used to pick up intra-day T+0 and T+1 recon breaks, and notify the
                                relevant people of the breaks via an email
                                Extracted file name from Markit Wire:
                                Y:/Jhb/FALanding/Prod/MarkitWire/MarkitWire.csv
DEPARTMENT AND DESK     :       ABSA Capital / IRD Desk and Prime Services Desk
REQUESTER               :       Mitesh Kassanjee
DEVELOPER               :       Arthur Grace
CR NUMBER               :       CHNG0003115685
DEPENDENCY 1            :       MarkitWire Recon service on production AMWI Windows Server: JHBPSM020000565
DEPENDENCY 2            :       Source file: Y:/Jhb/FAReports/AtlasEndOfDay/MarkitWire.csv
JIRA                    :       OTC-493 - Schedule the AMWI Email Notification Utility
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer           Description
-------------------------------------------------------------------------------------------------------------
2015-09-24    CHNG0003115685    Arthur Grace        Initial Implementation
2015-10-23    CHNG0003206520    Arthur Grace        Update email component to not default on server user (from)
2015-11-27    CHNG0003284445    Arthur Grace        Check the back-dated value date on novated trades entered
2016-01-27    CHNG0003400622    Arthur Grace        Add requested notification for RTB automated email success criteria
2016-02-10    CHNG0003435014    Ushanta Mooloo      Added checks for trades with Error transition status and missing clearing add infos
2016-03-01    CHNG0003557860    Ushanta Mooloo      Added bidirectional checks=>a live trade in FA must exist in MW and vice versa (OTC-796)
2016-03-08    CHNG0003557860    Ushanta Mooloo      Change the format of the Recon to HTML and CSV (OTC-989)
2016-03-23    CHNG0003557860    Ushanta Mooloo      Add an aging element to the Recon (OTC-1010)
2016-04-08    CHNG0003580519    Ushanta Mooloo      Ignore "Allocated" trades in MarkitWire (OTC-1040)
2016-04-11    CHNG0003580519    Ushanta Mooloo      Add logic to determine the start date (OTC-1041)
2016-04-11    CHNG0003580519    Ushanta Mooloo      Add logic to aging by execution date (OTC-1001)
2016-05-04    CHNG0003634044    Ushanta Mooloo      Removed the logic that excludes trades booked by system accounts from the reconciliation(OTC-1063)
2016-06-24    CHNG0003762782    Ushanta Mooloo      Fixed 3 issues: 
                                                    Take instrument update date into account when calculating aging (OTC-1077)
                                                    Expiry differ on MW & FA (reasons are: Weekends, Public Holiday)=> So do not exclude based on MW expiry date
                                                    rather check based on FA expiry only ("if expired of FA then don't reconcile") (OTC-1074)
                                                    CurrSwap => Check nominal on the leg carrying the same currency as the deal extractor (OTC-1052)
2017-01-30                      Fancy Dire          Use the new file that contains both legs of the CurrSwap and update the logic for checking the Nominal.
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    This module will be used to pick up intra-day T+0 and T+1 recon breaks, and notify the relevant people of the breaks
    via an email
"""

import csv
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

import acm
import ael

RECON_ITEMS = []
PORTFOLIOS_IRD_DESK = ['CD_CorpCDS_Basis',
                       'CD_EC_IR',
                       'CD_QUANTO',
                       'CPI',
                       'ERM_IRP',
                       'FI_OIS_Hedges',
                       'LTFX',
                       'LTFX_LCH',
                       'Non ZAR Fair Value',
                       'Non Zar Liquid Assets',
                       'NZ FI Risk',
                       'PB_FRA_MAP100',
                       'PB_IRS_MAP104SE',
                       'PRIME',
                       'RAJ - FRA Trading',
                       'STIRT - FRA FLO',
                       'STIRT - FRA Trading',
                       'Swap Flow',
                       'Swap Flow NonCSA',
                       'Swap Flow_LCH',
                       ]

HEADINGS = []

def process_notification(csv_file_location, from_email_address, to_email_address, subject):
    """ process_notification will create the email and send an email containing all breaks """
    if len(RECON_ITEMS) > 0:
        server = acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(), 'mailServerAddress').Value()
        # Save the results to the server in CSV format
        WriteCSVFile(csv_file_location)

        mail = EmailWithAttachment(csv_file_location)
        mail['From'] = from_email_address
        mail['To'] = to_email_address
        mail['Subject'] = subject

        smtp = smtplib.SMTP(server)
        smtp.sendmail(from_email_address, to_email_address, mail.as_string())
        smtp.quit()


def GetMarkitWireFrontArenaTradesNotMirrored(trade, markitwire_trade):
    """ Find inter-desk trades that have not been mirrored """
    if trade.Acquirer().Type() == 'Intern Dept' and trade.Counterparty().Type() == 'Intern Dept':
        if trade.MirrorTrade() is None:
            AddNotification('Mirror Link Missing', trade, trade.Counterparty().Name() + '/' + trade.Acquirer().Name(),
                            markitwire_trade, markitwire_trade[HEADINGS.index('CounterPartyLE')])


def GetMWStatusBreaks(trade, markitwire_trade):
    """ Check whether a transition error has been experienced, and if the trade has in fact not moved in status """
    if trade.AdditionalInfo().CCPclearing_status() == 'Error' and trade.Status() in (
            'BO Confirmed', 'FO Confirmed', 'Simulated'):
        AddNotification('Clearing Status Error', trade, trade.AdditionalInfo().CCPclearing_status(), markitwire_trade,
                        markitwire_trade[HEADINGS.index('ContractState')])


def GetConcerningTradeStatus(trade, markitwire_trade):
    """ Check whether there are trades in a concerning status dating back from a released trade on Markit Wire """
    deal_date = datetime.strptime(markitwire_trade[HEADINGS.index('DealDate')][0:10], '%Y-%m-%d').date()
    diff = datetime.today().date() - deal_date
    days = diff.days
    if days > 0 and trade.Status() in ('FO Confirmed', 'BO Confirmed'):
        AppendNotification('Trade is not BO-BO Confirmed', trade.Oid(), trade.Status(), markitwire_trade[HEADINGS.index('TradeId')],
                           markitwire_trade[HEADINGS.index('ContractState')], deal_date, days)



def GetDuplicatePayments(trade, markitwire_trade):
    """ Search for payments that have been duplicated on by comparing a trade to it's contract trade """
    if trade.Payments() is None or trade.Contract():
        return
    if trade.Contract().Payments():
        return

    if trade.Contract().Oid() != trade.Oid() and trade.Contract().Status() not in ('Terminated', 'Void'):
        for payment in trade.Payments():
            for contractTradePayment in trade.Contract().Payments():
                if payment.Amount() == contractTradePayment.Amount() and payment.Type() == contractTradePayment.Type():
                    AddNotification('Payment Duplication', trade, str(payment.Type()), markitwire_trade, '-')


def GetInterdeskChecks(trade, markitwire_trade):
    """ Perform some validation on the inter-desk deals where we have had bugs in managing through the AMWI """
    if trade.Acquirer().Name() == 'IRD DESK' and trade.Counterparty().Name() == 'IRD DESK':
        if trade.Portfolio().Name() not in PORTFOLIOS_IRD_DESK:
            AddNotification('IRD Desk Porfolio', trade, trade.Portfolio().Name(), markitwire_trade, markitwire_trade[HEADINGS.index('BookId')])
    if trade.Acquirer().Name() == 'PRIME SERVICES DESK' and trade.Counterparty().Name() == 'PRIME SERVICES DESK':
        if trade.Portfolio().Name().find('PB_') == -1:
            AddNotification('Prime Services Desk Portfolio', trade, trade.Portfolio().Name(), markitwire_trade,
                            markitwire_trade[HEADINGS.index('BookId')])


def GetIncorrectUserCheck(trade, markitwire_trade):
    """ Check the Markit Wire trader - certain trades are not coming through on the Owner and Trader """
    if trade.Trader() and trade.Owner():
        if trade.Trader().Name() == 'ATS_AMWI_PRD' and trade.Owner().Name() == 'ATS_AMWI_PRD':
            AddNotification('Incorrect Trader', trade, trade.Trader().Name(), markitwire_trade, markitwire_trade[HEADINGS.index('Trader')])


def GetPublicHolidays():
    """ For the start and end date checks, the calendar from Front Arena is required """
    publicHolidays = []
    days = ael.Calendar['ZAR Johannesburg']
    for day in days.dates():
        publicHolidays.append(str(day.daynbr))
    return publicHolidays


def CheckCashFlowIncorrectEndDate(trade):
    """ Get the cash flow end date """
    for leg in trade.Instrument().Legs():
        for cashFlow in leg.CashFlows():
            endDateCashFlow = cashFlow.PayDate()
    return endDateCashFlow


def GetStartEndDateCheck(trade, markitwire_trade):
    """ Check the start and end dates between Markit Wire and Front Arena """
    calendar = acm.FCalendar['ZAR Johannesburg']
    publicHolidays = GetPublicHolidays()
    isPublicHoliday = False

    week_day_start_mw = acm.Time().DayOfWeek(markitwire_trade[HEADINGS.index('StartDate')])
    week_day_end_mw = acm.Time().DayOfWeek(markitwire_trade[HEADINGS.index('EndDate')])
    for publicHoliday in publicHolidays:
        if publicHoliday == markitwire_trade[HEADINGS.index('EndDate')]:
            isPublicHoliday = True
    start_date = acm.Time().DateToday()
    endDate = acm.Time().DateToday()
    for leg in trade.Instrument().Legs():
        if trade.Instrument().InsType() in ('Swap', 'CurrSwap'):
            if leg.LegType() == 'Fixed':
                start_date = leg.StartDate()
                endDate = leg.EndDate()
        elif trade.Instrument().InsType() == 'FRA':
            start_date = leg.StartDate()
            endDate = leg.EndDate()
    endDateCashFlow = acm.Time().DayOfWeek(CheckCashFlowIncorrectEndDate(trade))

    week_day_end_fa = acm.Time().DayOfWeek(endDate)
    week_day_start_fa = acm.Time().DayOfWeek(start_date)
    if week_day_end_mw not in ('Saturday', 'Sunday'):
        if markitwire_trade[HEADINGS.index('EndDate')] != endDate:
            for publicHoliday in publicHolidays:
                if markitwire_trade[HEADINGS.index('EndDate')] == publicHoliday:
                    if endDate != calendar.AdjustBankingDays(markitwire_trade[HEADINGS.index('EndDate')], 1):
                        if endDate != calendar.AdjustBankingDays(markitwire_trade[HEADINGS.index('EndDate')], -1):
                            isPublicHoliday = True
                            if markitwire_trade[HEADINGS.index('FixedCalculationPeriodDatesAdjustBDC')] == 'MODFOLLOWING':
                                AddNotification('End Date (Public Holiday)', trade, endDate, markitwire_trade,
                                                markitwire_trade[HEADINGS.index('EndDate')])
            if not isPublicHoliday:
                if markitwire_trade[HEADINGS.index('FixedCalculationPeriodDatesAdjustBDC')] == 'MODFOLLOWING':
                    AddNotification('End Date', trade, endDate, markitwire_trade, markitwire_trade[HEADINGS.index('EndDate')])

    if week_day_start_mw not in ('Saturday', 'Sunday'):
        if markitwire_trade[HEADINGS.index('StartDate')] != start_date:
            for publicHoliday in publicHolidays:
                if markitwire_trade[HEADINGS.index('StartDate')] == publicHoliday:
                    if start_date != calendar.AdjustBankingDays(markitwire_trade[HEADINGS.index('StartDate')], 1):
                        if start_date != calendar.AdjustBankingDays(markitwire_trade[HEADINGS.index('StartDate')], -1):
                            if markitwire_trade[HEADINGS.index('FixedCalculationPeriodDatesAdjustBDC')] == 'MODFOLLOWING':
                                AddNotification('Start Date (Public Holiday)', trade, start_date, markitwire_trade,
                                                markitwire_trade[HEADINGS.index('StartDate')])
            if not isPublicHoliday:
                if markitwire_trade[HEADINGS.index('FixedCalculationPeriodDatesAdjustBDC')] == 'MODFOLLOWING':
                    AddNotification('Start Date', trade, start_date, markitwire_trade, markitwire_trade[HEADINGS.index('StartDate')])

    if week_day_start_mw in ('Saturday', 'Sunday') and endDateCashFlow in ('Saturday', 'Sunday'):
        if markitwire_trade[HEADINGS.index('StartDate')] == start_date:
            if markitwire_trade[HEADINGS.index('FixedCalculationPeriodDatesAdjustBDC')] == 'MODFOLLOWING':
                AddNotification('Start Date on Weekend', trade, start_date, markitwire_trade, markitwire_trade[HEADINGS.index('StartDate')])

    if week_day_end_mw in ('Saturday', 'Sunday') and endDateCashFlow in ('Saturday', 'Sunday'):
        if markitwire_trade[HEADINGS.index('EndDate')] == endDate:
            if markitwire_trade[HEADINGS.index('FixedCalculationPeriodDatesAdjustBDC')] == 'MODFOLLOWING':
                AddNotification('End Date on Weekend', trade, endDate, markitwire_trade, markitwire_trade[HEADINGS.index('EndDate')])

    if week_day_start_fa in ('Saturday', 'Sunday') and endDateCashFlow in ('Saturday', 'Sunday'):
        if markitwire_trade[HEADINGS.index('StartDate')] == start_date:
            if markitwire_trade[HEADINGS.index('FixedCalculationPeriodDatesAdjustBDC')] == 'MODFOLLOWING':
                AddNotification('Start Date on Weekend', trade, start_date, markitwire_trade, markitwire_trade[HEADINGS.index('StartDate')])

    if week_day_end_fa in ('Saturday', 'Sunday') and endDateCashFlow in ('Saturday', 'Sunday'):
        if markitwire_trade[HEADINGS.index('EndDate')] == endDate:
            if markitwire_trade[HEADINGS.index('FixedCalculationPeriodDatesAdjustBDC')] == 'MODFOLLOWING':
                AddNotification('End Date on Weekend', trade, endDate, markitwire_trade, markitwire_trade[HEADINGS.index('EndDate')])


def MathIsClose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """ Compare equality of 2 numerical value """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def get_nominal_of_leg(trade, currency):
    legs = [itm for itm in trade.Instrument().Legs() if itm.Currency().Name() in currency]
    print '%s has %s legs' % (trade.Oid(), len(legs))
    if len(legs) > 1:
        return trade.Instrument().ContractSize() * legs[0].NominalFactor(), trade.Instrument().ContractSize() * legs[1].NominalFactor()
    elif len(legs) > 0:
        return trade.Instrument().ContractSize() * legs[0].NominalFactor()

    return 0


def get_nominal_check(trades, markitwire_trade):
    """ Check for actual nominal breaks """
    tradeNominal = mwNominal = 0.0
    tradeNominal2 = mwNominal2 = 0.0
    tradeNumbers = []
    NomSame = Leg1 = Leg2 = False
    for trade in trades:
        #Get the nominal of a currency swap from the appropriate leg - match the leg based on currency. 
        nominal = get_nominal_of_leg(trade, [markitwire_trade[HEADINGS.index('Currency')], markitwire_trade[HEADINGS.index('Currency2')]]) if trade.Instrument().InsType() == 'CurrSwap' else trade.Nominal()
       
       
        print '%s nominal is %s' % (trade.Oid(), nominal[0] if type(nominal) == 'tuple' else nominal)
        print 'MW Nominal is %s' % markitwire_trade[HEADINGS.index('Notional')]
        mwNominal += float(markitwire_trade[HEADINGS.index('Notional')])
        mwNominal2 += float(markitwire_trade[HEADINGS.index('Notional2')])
        print 'Instrument type:', trade.Instrument().InsType()
        
        
        if trade.MirrorTrade():
            
            if str(trade.MirrorTrade().Oid()) not in tradeNumbers:
                
                tradeNominal += nominal
                NomSame = MathIsClose(abs(mwNominal), abs(float(tradeNominal)))
                tradeNumbers.append(str(trade.Oid()))
        else:
            if trade.Instrument().InsType() == 'CurrSwap':
                tradeNominal += nominal[0]
                tradeNominal2 += nominal[1]
                Leg1 = MathIsClose(abs(mwNominal), abs(float(tradeNominal)))
                Leg2 = MathIsClose(abs(mwNominal2), abs(float(tradeNominal2)))
                print 'Nominal Check:', Leg1 == Leg2
                NomSame = Leg1 == Leg2

                tradeNumbers.append(str(trade.Oid()))
            else:
                tradeNominal += nominal
                NomSame = MathIsClose(abs(mwNominal), abs(float(tradeNominal)))
                tradeNumbers.append(str(trade.Oid()))

    if not NomSame:
        deal_date = datetime.strptime(markitwire_trade[HEADINGS.index('DealDate')][0:10], '%Y-%m-%d').date()
        trade_execution_time = GetExecutionTime(trades, deal_date)
        diff = datetime.today().date() - trade_execution_time
        days = diff.days
        if trade.Instrument().InsType() == 'CurrSwap':

            #mwNominal.append(str(abs(float(markitwire_trade[HEADINGS.index('Notional')]))))
            markitwire_trade.remove(markitwire_trade[HEADINGS.index('Notional')])
            notionalIndex = markitwire_trade.index(markitwire_trade[HEADINGS.index('Notional')]) 
            markitwire_trade.insert(notionalIndex, mwNominal) 
            #mwNominal.append(str(abs(float(markitwire_trade[HEADINGS.index('Notional2')]))))
            markitwire_trade.remove(markitwire_trade[HEADINGS.index('Notional2')])
            notionalIndex = markitwire_trade.index(markitwire_trade[HEADINGS.index('Notional2')]) 
            #nominal.insert(str(abs(float(tradeNominal))))
            tradeNominal == nominal[0]
            #nominal.insert(str(abs(float(tradeNominal2))))
            tradeNominal2 == nominal[1]

        else:
            mwNominal.append(str(abs(float(markitwire_trade[HEADINGS.index('Notional')]))))
            nominal.append(str(abs(float(tradeNominal))))

        AppendNotification('Nominal', ', '.join(tradeNumbers), nominal, markitwire_trade[HEADINGS.index('TradeId')],
                           mwNominal, trade_execution_time, days)


def GetInternalTrade(trade):
    """ Method to check if the recon is dealing with an inter-desk deal """
    return trade.Acquirer().Type() == 'Intern Dept' and trade.Counterparty().Type() == 'Intern Dept'


def GetHasAddInfoSideId(trade):
    """ Verify that an inter-desk deal in fact has a Side Id which is used by the AMWI to manage them """
    addInfoCCP = acm.FAdditionalInfo.Select('recaddr = %i' % trade.Oid())
    for addinfo in addInfoCCP:
        if addinfo.AddInf().Name() == 'mwire_sideid':
            return addinfo


def GetFixedRateCheck(trade, markitwire_trade):
    """ Fixed rate check between Markit Wire and Front Arena """
    if markitwire_trade[HEADINGS.index('Rate')] == '':
        return

    mwRate = str(float(markitwire_trade[HEADINGS.index('Rate')]) * 100)

    for leg in trade.Instrument().Legs():
        if trade.Instrument().InsType() == 'Swap':
            if leg.LegType() == 'Fixed':
                legFixedRate = str(leg.FixedRate())
                if legFixedRate[0:4] != mwRate[0:4]:
                    AddNotification('Fixed Rate', trade, legFixedRate[0:4], markitwire_trade, mwRate[0:4])
        elif trade.Instrument().InsType() == 'FRA':
            legFixedRate = str(leg.FixedRate())
            if legFixedRate[0:4] != mwRate[0:4]:
                AddNotification('Fixed Rate', trade, legFixedRate[0:4], markitwire_trade, mwRate[0:4])


def GetNominalDirectionCheck(trade, markitwire_trade):
    """ Nominal directions can change especially on inter-desk deals. This has been a known bug in the AMWI """
    if markitwire_trade[HEADINGS.index('ContractState')] != 'Cancelled':
        if GetInternalTrade(trade):
            if trade.Acquirer().Name() != 'IRD DESK' and trade.Counterparty().Name() != 'IRD DESK':
                addinfo = GetHasAddInfoSideId(trade)
                if addinfo:
                    # There is no direction specified for cross currency products
                    if markitwire_trade[HEADINGS.index('Direction')] != '':
                        # side id missing
                        if addinfo.FieldValue() == '' and markitwire_trade[HEADINGS.index('SideId')] != '':
                            AddNotification('Side ID', trade, addinfo.FieldValue(), markitwire_trade,
                                            markitwire_trade[HEADINGS.index('SideId')])
                        # side id for interdesk deals is 1
                        if addinfo.FieldValue() == '1' and markitwire_trade[HEADINGS.index('SideId')] == '1':
                            if trade.Instrument().InsType() == 'FRA':
                                if trade.Direction() != markitwire_trade[HEADINGS.index('Direction')]:
                                    AddNotification('Direction', trade, trade.Direction(), markitwire_trade,
                                                    markitwire_trade[HEADINGS.index('Direction')])
                            elif trade.Instrument().InsType() == 'Swap':
                                if markitwire_trade[HEADINGS.index('Direction')] == 'Receive' and trade.Direction() != 'Receive Fixed' and \
                                                markitwire_trade[HEADINGS.index('ContractState')] != 'Novated':
                                    AddNotification('Direction', trade, trade.Direction(), markitwire_trade,
                                                    markitwire_trade[HEADINGS.index('Direction')])
                                elif markitwire_trade[HEADINGS.index('Direction')] == 'Pay' and trade.Direction() != 'Pay Fixed' and \
                                                markitwire_trade[HEADINGS.index('ContractState')] != 'Novated':
                                    AddNotification('Direction', trade, trade.Direction(), markitwire_trade,
                                                    markitwire_trade[HEADINGS.index('Direction')])
                        # side id for interdesk deal is 2
                        if addinfo.FieldValue() == '2' and markitwire_trade[HEADINGS.index('SideId')] == '2':
                            if trade.Instrument().InsType() == 'FRA':
                                if trade.Direction() != markitwire_trade[HEADINGS.index('Direction')]:
                                    AddNotification('Direction', trade, trade.Direction(), markitwire_trade,
                                                    markitwire_trade[HEADINGS.index('Direction')])
                            elif trade.Instrument().InsType() == 'Swap':
                                if markitwire_trade[HEADINGS.index('Direction')] == 'Receive' and trade.Direction() != 'Receive Fixed' and \
                                                markitwire_trade[HEADINGS.index('ContractState')] != 'Novated':
                                    AddNotification('Direction', trade, trade.Direction(), markitwire_trade,
                                                    markitwire_trade[HEADINGS.index('Direction')])
                                elif markitwire_trade[HEADINGS.index('Direction')] == 'Pay' and trade.Direction() != 'Pay Fixed' and \
                                                markitwire_trade[HEADINGS.index('ContractState')] != 'Novated':
                                    AddNotification('Direction', trade, trade.Direction(), markitwire_trade,
                                                    markitwire_trade[HEADINGS.index('Direction')])
                    else:
                        if GetInternalTrade(trade):
                            AddNotification('Side ID', trade, addinfo.FieldValue(), markitwire_trade,
                                            markitwire_trade[HEADINGS.index('SideId')])
        else:
            if trade.Type() != 'Closing':
                if markitwire_trade[HEADINGS.index('Direction')] == 'Receive' and trade.Direction() == 'Pay Fixed':
                    AddNotification('Direction', trade, trade.Direction(), markitwire_trade, markitwire_trade[HEADINGS.index('Direction')])
                if markitwire_trade[HEADINGS.index('Direction')] == 'Pay' and trade.Direction() == 'Received Fixed':
                    AddNotification('Direction', trade, trade.Direction(), markitwire_trade, markitwire_trade[HEADINGS.index('Direction')])
                if markitwire_trade[HEADINGS.index('Direction')] == 'Buy' and trade.Direction() == 'Sell':
                    AddNotification('Direction', trade, trade.Direction(), markitwire_trade, markitwire_trade[HEADINGS.index('Direction')])
                if markitwire_trade[HEADINGS.index('Direction')] == 'Sell' and trade.Direction() == 'Buy':
                    AddNotification('Direction', trade, trade.Direction(), markitwire_trade, markitwire_trade[HEADINGS.index('Direction')])


def GetDefaultChecks(trade, markitwire_trade):
    """ Defaults are defined in the AMWI to default on certain trade fields if a suitable """
    if trade.Counterparty().Name() == 'MKTWIRE_CTPTY':
        if not trade.IsInfant():
            AddNotification('Default Counterparty', trade, trade.Counterparty().Name(), markitwire_trade,
                            markitwire_trade[HEADINGS.index('CounterPartyLE')])
    if trade.Portfolio().Name() == 'Allocate_MarkitWire':
        if not trade.IsInfant():
            AddNotification('Default Portfolio', trade, trade.Portfolio().Name(), markitwire_trade, markitwire_trade[HEADINGS.index('CounterPartyLE')])
    if trade.Acquirer().Name() == 'MARKITWIRE':
        if not trade.IsInfant():
            AddNotification('Default Acquirer', trade, trade.Acquirer().Name(), markitwire_trade, markitwire_trade[HEADINGS.index('LE')])


def GetStartCashFlowDate(trade):
    """ Get the start date off the cashflow """
    if trade.Instrument().InsType() == 'Swap':
        for leg in trade.Instrument().Legs():
            if leg.LegType() == 'Fixed':
                start_date = leg.StartDate()
        return start_date


def GetValueDateChecks(trade, markitwire_trade):
    """ Check the value dates on novated trades entered """
    if trade.Instrument().InsType() in ('Swap', 'FRA'):
        if trade.Counterparty().Name() == 'IRD DESK' or trade.Acquirer().Name() == 'IRD DESK':
            if trade.Status() == 'BO-BO Confirmed':
                if datetime.strptime(markitwire_trade[HEADINGS.index('StartDate')], '%Y-%m-%d') < datetime.strptime(markitwire_trade[HEADINGS.index('TradeDate')],
                                                                                           '%Y-%m-%d'):
                    if datetime.strptime(trade.ValueDay(), '%Y-%m-%d') < datetime.strptime(str(trade.TradeTime())[0:10],
                                                                                           '%Y-%m-%d'):
                        AddNotification('Value Day', trade, trade.ValueDay(), markitwire_trade, markitwire_trade[HEADINGS.index('StartDate')])


def GetSpreadCheck(trade, markitwire_trade):
    """ Check the spread on the cross currency products """
    for leg in trade.Instrument().Legs():
        if leg.Spread() != 0.0 and markitwire_trade[HEADINGS.index('SpreadOverFloating')] != '' and leg.Currency().Name() == 'ZAR' and str(
                leg.Spread()) != str(float(markitwire_trade[HEADINGS.index('SpreadOverFloating')]) * 100):
            AddNotification(leg.LegType() + ' Leg Spread', trade, leg.Spread(), markitwire_trade, markitwire_trade[HEADINGS.index('SpreadOverFloating')])


def GetInitialRateCheck(trade, markitwire_trade):
    """ Check the intitial rate """
    if markitwire_trade[HEADINGS.index('InitialRate')] != '':
        instrument = trade.Instrument()
        resets = instrument.FirstFloatLeg().Resets()
        if resets > 0:
            firstReset = resets.SortByProperty('StartDate', True)[0]
            fixingValue = float(firstReset.FixingValue())
            mwFixingValue = float(markitwire_trade[HEADINGS.index('InitialRate')]) * 100
            if not MathIsClose(mwFixingValue, fixingValue):
                AddNotification('First Float Leg Fixing Value', trade, fixingValue, markitwire_trade, mwFixingValue)


def GetRollingPeriodCheck(trade, markitwire_trade):
    """ Get the rolling period check """
    if trade.Instrument().InsType() == 'CurrSwap':
        if str(trade.Instrument().PayLeg().RollingPeriod()).upper() != str(markitwire_trade[HEADINGS.index('RollDate')]).upper():
            AddNotification('Pay Leg Rolling Period', trade, trade.Instrument().PayLeg().RollingPeriod(),
                            markitwire_trade, markitwire_trade[HEADINGS.index('RollDate')])


def GetClearTradeAttrCheck(trade, markitwire_trade):
    """
    Clearing trades must have the following add info's  set:
    'CCPccp_id', 'CCPccp_ptynbr', 'CCPclr_broker_ptynb', 'CCPmwire_booking_st', 'CCPmwire_contract_s', 
    'CCPmwire_message_st', 'CCPmwire_new_status', 'CCPmwire_process_st', 'CCPmwire_user_msg', 'CCPoriginal_counter', 
    'ClearingHouseId', 'ClearingMember', 'ClearingMemberCode', 'InsOverride', 'CCPccp_status', 'prior_middleware'
    """
    if markitwire_trade[HEADINGS.index('ContractState')] == 'New-Clearing':
        addInfoKeys = ['CCPccp_id', 'CCPccp_ptynbr', 'CCPclr_broker_ptynb', 'CCPmwire_booking_st', 'CCPmwire_contract_s', 
                        'CCPmwire_message_st', 'CCPmwire_new_status', 'CCPmwire_process_st', 'CCPmwire_user_msg', 'CCPoriginal_counter', 
                        'ClearingHouseId', 'Clearing Member', 'ClearingMemberCode', 'InsOverride', 'CCPccp_status', 'prior_middleware']

        for addInfoKey in addInfoKeys:
            specCCP = acm.FAdditionalInfoSpec[addInfoKey]
            addInfoCCP = acm.FAdditionalInfo.Select01(
                'recaddr=' + str(trade.Oid()) + ' and addInf=' + str(specCCP.Oid()), '')
            if not addInfoCCP:
                AddNotification('Clearing Add Info', trade, specCCP.Name() + ' is blank', markitwire_trade, '-')


def LoadFATrades(inceptionDate):
    """
    Select the MW population from the Front ADS
    """
    trades = []
    query = """select distinct t.trdnbr \
        from trade t,instrument i,AdditionalInfo ai,AdditionalInfoSpec ais \
        where t.insaddr = i.insaddr \
        and t.updat_time >= '{0}' \
        and i.exp_day > '{1}' \
        and ai.recaddr = t.trdnbr and ai.addinf_specnbr = ais.specnbr \
        and (ais.field_name = 'CCPmiddleware_id' or ais.field_name = 'prior_middleware') and ai.value ~='' \
        and i.instype in ('FRA','Swap','CurrSwap') \
        and t.status in ('FO Confirmed','BO-BO Confirmed','BO Confirmed') \
        order by t.trdnbr desc""".format(inceptionDate, datetime.today().date())

    selection = ael.asql(query)

    for selectionFA in selection[1][0]:
        trades.append(acm.FTrade[selectionFA[0]])

    return trades


def GetFATradesRelatedToMarkitWireTrade(ftrades, mw_trade_number):
    """
    Find trades linked to a specific MW trade
    """
    trades = []

    for trade in ftrades:
        if trade.AdditionalInfo().CCPmiddleware_id():
            if trade.AdditionalInfo().CCPmiddleware_id() == mw_trade_number:
                trades.append(trade)
        elif trade.AdditionalInfo().Prior_middleware():
            if trade.AdditionalInfo().Prior_middleware() == mw_trade_number:
                trades.append(trade)
    return trades


def BiDirectionalCheckForMissingTrades(ftrades, start_date, markitwire_list):
    """
    Check for FA trades linked to an unknown MarkitWire trade
    """
    for trade in ftrades:
        try:
            execution_time = datetime.fromtimestamp(trade.UpdateTime()).date()
            if execution_time >= start_date:
                mw_trade_number = GetMarkitWireTradeId(trade)
                if mw_trade_number not in markitwire_list:
                    diff = datetime.today().date() - execution_time
                    days = diff.days
                    AppendNotification('Missing MarkitWire Trade', trade.Oid(), '-', mw_trade_number, '-',
                                       execution_time, days)
        except Exception as e:
            print 'Error: Failed to validate MarkitWire link', trade.Oid(), str(e)

def GetMarkitWireTradeId(trade):
    """
    Get the MW ID linked to a trade
    """
    if trade.AdditionalInfo().CCPmiddleware_id():
        return trade.AdditionalInfo().CCPmiddleware_id()
    elif trade.AdditionalInfo().Prior_middleware():
        return trade.AdditionalInfo().Prior_middleware()
    return 0


def WriteCSVFile(outputFileLocation):
    """
    Create a file to store all breaks
    """
    with open(outputFileLocation, 'wb') as reconBreaksFile:
        reconWriter = csv.writer(reconBreaksFile, quoting=csv.QUOTE_ALL)
        reconWriter.writerow(
            ['Category', 'Front Arena Trade', 'Front Arena Value', 'Markit Wire Trade', 'Markit Wire Value',
             'Execution Date', 'Aging'])
        for itemInList in RECON_ITEMS:
            reconWriter.writerow(itemInList)


def EmailWithAttachment(outputFileLocation):
    """
    Build the email:
    Attach the CSV that contains all breaks to the email and also, set, create and attach the HTML content.
    """
    msg = MIMEMultipart()
    msg.attach(MIMEText(BuildHTML(), 'html'))
    with open(outputFileLocation, 'rb') as reconBreaksFile:
        msg.attach(MIMEApplication(
            reconBreaksFile.read(),
            Content_Disposition='attachment; filename="%s"' % basename(outputFileLocation),
            Name=basename(outputFileLocation)
        ))
    return msg


def BuildHTML():
    """
    Constructs the recon breaks content of the email sent to the audience of the recon.
    """
    htmlReconItemRows = ""
    for item in RECON_ITEMS:
        htmlReconItemRows += """\
            <tr>
                <td>{0}</td>
                <td>{1}</td>
                <td>{2}</td>
                <td>{3}</td>
                <td>{4}</td>
                <td>{5}</td>
                <td>{6}</td>
            </tr>
            """.format(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
    return HTMLTemplate(htmlReconItemRows)


def HTMLTemplate(table):
    """
    Constructs the HTML template of the email sent to the audience of the recon.
    """

    return """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Markit Wire Recon Report</title>
    <style type="text/css">
        /* Default CSS */
        body, #body_style {
            margin: 0;
            padding: 0;
            background: #f1f1f1;
            color: #5b656e;
            width: 640
        }
        a {
            color: #09c;
        }
        a img {
            border: none;
            text-decoration: none;
        }
        table, table td {
            border-collapse: collapse;
        }
        td, th, h1, h2, h3, p {
            font-family: arial, helvetica, sans-serif;
            color: #313a42;
            align: left
        }
        h1, h2, h3, h4 {
            color: #313a42 !important;
            font-weight: normal;
            line-height: 1.2;
        }
        h1 {
            font-size: 24px;
        }
        h2 {
            font-size: 18px;
        }
        h3 {
            font-size: 16px;
        }
        p {
            margin: 0 0 1.6em 0;
        }

        /* Force Outlook to provide a "view in browser" menu link. */
        #outlook a {
            padding: 0;
        }

        /* Whitespace (imageless spacer) */
        .whitespace {
            font-family: 0px;
            line-height: 0px;
        }

        /* Header */
        .header {
            background: rgb(22, 140, 204);
        }

        .headerTitle {
            color: #ffffff;
            font-size: 28px;
            padding: 0px 0px 10px 0px;
            width: 640;
            align:left
        }

        .headerContent {
            color: #ffffff;
            font-size: 22px;
            align:left
        }

        /* One horizontal section of content: e.g. */
        .section {
            padding: 20px 0px 0px 0px;
       }

        .sectionOdd {
            background-color: #f1f1f1;
        }

        .sectionEven {
            background-color: #ffffff;
        }

        .sectionOdd, .sectionEven {
            padding: 30px 0px 30px 0px;
        }

        /* An article */
        .sectionArticleTitle, .sectionArticleContent {
            text-align: center;
        }

        .sectionArticleTitle {
            font-size: 18px;
            padding: 10px 0px 5px;
        }

        .sectionArticleContent {
            font-size: 13px;
            line-height: 18px;
        }

        .sectionArticleImage {
            text-align: center;
        }

        .sectionArticleImage img {
            padding: 0px 0px 0px 0px;
            -ms-interpolation-mode: bicubic;
        }

        .sectionTitle, .sectionSubTitle {
            text-align: center;
        }

        .sectionTitle {
            font-size: 23px;
            padding: 0px 10px 10px 10px;
        }

        .sectionSubTitle {
            padding: 0px 10px 20px 10px;
        }

        /* Footer */
        .footer {
            background: rgb(22, 140, 204);
        }

        .footer a {
            color: #ffffff;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <table border='0' cellspacing='0' cellpadding='0' width='100%'  class='header'>
        <tr><td class="whitespace" height="20">&nbsp;</td></tr>
        <tr>
            <th class='headerTitle'>
                Markit Wire Recon Report
            </th>
        </tr>
        <tr><td class="whitespace" height="20">&nbsp;</td></tr>
    </table>

    <table border='0' cellspacing='0' cellpadding='0' width='100%'>
        <tr>
            <td class='sectionOdd'>
                <table border="1" style="padding:4px 7px 2px 4px; font-size:smaller; width:100%; border:1px solid grey;">
                    <tr>
                        <th>Category</th>
                        <th>Front Arena Trade</th>
                        <th>Front Arena Value</th>
                        <th>Markit Wire Trade</th>
                        <th>Markit Wire Value</th>
                        <th>Execution Time</th>
                        <th>Aging</th>
                    </tr>
                    """ + table + """
                </table>
            </td>
        </tr>
    </table>
</body>
</html>

"""


def ReconcileMWTradeToFrontTrades(ftrades, markitwire_trade, parameters, start_date):
    """
    This function reconciles each pivotal MarkitWire trade attribute to it's corresponding Front Arena trade
    attribute. Each check is configurable to accommodate different types of recons, ie: T0, T1 or Exception recon.
    """
    
    for trade in ftrades:
        if parameters['mwMWNominalDirectionCheck']:
            GetNominalDirectionCheck(trade, markitwire_trade)
        # Check the start and end dates
        if parameters['mwMWStartEndDateCheck']:
            GetStartEndDateCheck(trade, markitwire_trade)
        # Check the error status on trades
        if parameters['mwMWStatusCheck']:
            GetMWStatusBreaks(trade, markitwire_trade)
        # Check the actual status of the trades and only run this check for T+1 recons
        if parameters['mwMWStatusCheck'] and datetime.today().date() > start_date:
            GetConcerningTradeStatus(trade, markitwire_trade)
        # Check the fixed rate
        if parameters['mwMWFixedRateCheck']:
            GetFixedRateCheck(trade, markitwire_trade)
        # Check the incorrect user check
        if parameters['mwMWIncorrectUserCheck']:
            GetIncorrectUserCheck(trade, markitwire_trade)
        # Check the overall inter-desk deals
        if parameters['mwMWInterDeskChecks']:
            GetInterdeskChecks(trade, markitwire_trade)
        # Defaults of the AMWI checks - E.g. default portfolio: Allocate_MarkitWire
        if parameters['mwMWDefaultChecks']:
            GetDefaultChecks(trade, markitwire_trade)
        # Check for back-dated trade checks where IRD Desk enter into novated deal
        if parameters['mwMWValueDateCheck']:
            GetValueDateChecks(trade, markitwire_trade)
        # Check the cross currency spread
        if parameters['mwMWSpreadCheck']:
            GetSpreadCheck(trade, markitwire_trade)
        # Check the initial rate
        if parameters['mwMWInitialRate']:
            GetInitialRateCheck(trade, markitwire_trade)
        # Check the rolling period
        if parameters['mwMWRollingPeriod']:
            GetRollingPeriodCheck(trade, markitwire_trade)
        # Check for valid clearing attributes on cleared trades
        if parameters['mwMWClearTradeAttributes']:
            GetClearTradeAttrCheck(trade, markitwire_trade)
        if parameters['mwMWDuplicatePaymentsCheck']:
            GetDuplicatePayments(trade, markitwire_trade)
        if parameters['mwMWMirrorChecks']:
            GetMarkitWireFrontArenaTradesNotMirrored(trade, markitwire_trade)

    # Check the actual nominal
    if parameters['mwMWNominalCheck']:
        get_nominal_check(ftrades, markitwire_trade)


def ExecuteReconChecks(ftrades, markitwire_trade, parameters, start_date):
    """
    Execute logic to identify reconciliation breaks between a MW trade and it's matching FA trade(s).
    """
    deal_date = datetime.strptime(markitwire_trade[HEADINGS.index('DealDate')][0:10], '%Y-%m-%d').date()
    trade_execution_time = GetExecutionTime(ftrades, deal_date)
    

    if trade_execution_time >= start_date:
        if len(ftrades) > 0:
            ReconcileMWTradeToFrontTrades(ftrades, markitwire_trade, parameters, start_date)
        else:
            expiry_date = markitwire_trade[HEADINGS.index('EndDate')][0:10]  # expiry date of the FRA ans Swap trade in Markit Wire
            matured = False
            if expiry_date != '':
                if datetime.strptime(expiry_date, '%Y-%m-%d').date() <= datetime.today().date():
                    matured = True

            if not matured:
                diff = datetime.today().date() - trade_execution_time
                days = diff.days
                AppendNotification('Missing Front Trade', '-', '-', markitwire_trade[HEADINGS.index('TradeId')], '-', trade_execution_time, days)


def CheckAllMarkitWireTrades(parameters, start_date, reader):
    """
    Pull the Markit Wire trades from the Deal Extractor file and run them through against
    the Front Arena found trades
    the latest Markit Wire deal extractor file. This is a full population download from Markit Serv
    Default source: Y:/Jhb/FALanding/Prod/MarkitWire/DEbaseline.csv
    """
    global HEADINGS
    RECON_ITEMS[:] = []
    markitwire_list = []
    ftrades = LoadFATrades(parameters['mwMWTradingDate'])
    for markitwire_trade in reader:
        if markitwire_trade[0] == '' or markitwire_trade[0] == 'TradeId':
            HEADINGS = markitwire_trade
            continue

        try:
            username = markitwire_trade[HEADINGS.index('Trader')]
            if markitwire_trade[HEADINGS.index('PrivateProcessState')] != 'Withdrawn' and markitwire_trade[HEADINGS.index('ContractState')] not in ('Cancelled', 'Allocated', 'Novated'):
                markitwire_list.append(markitwire_trade[HEADINGS.index('TradeId')])
                trades = GetFATradesRelatedToMarkitWireTrade(ftrades, markitwire_trade[HEADINGS.index('TradeId')])
                ExecuteReconChecks(trades, markitwire_trade, parameters, start_date)
            
        except Exception as e:
            print 'Error: Failed to reconcile deal', markitwire_trade[HEADINGS.index('TradeId')], str(e)
    
    if parameters['mwMWCheckMissingTrades']:
        BiDirectionalCheckForMissingTrades(ftrades, start_date, markitwire_list)

    print 'MW Population:', len(markitwire_list)
    print markitwire_list
    print 'FA Population:', len(ftrades)
    for trade in ftrades:
        print trade.Oid()


def GetExecutionTime(ftrades, mw_trade_execution_time):
    """
    The execution time indicates when last a trade was altered (or it's creation time in the case new trades).
    The execution time is used for aging. And; due to there being 2 platforms the execution may differ.
    We use the latest of execution from either MW or FA to determine the aging and also, in the case of the T0
    recon, to perform recon checks or not.
    """
    execution_times = [mw_trade_execution_time]

    for trade in ftrades:
        execution_times.append(datetime.fromtimestamp(trade.Instrument().UpdateTime()).date())
        execution_times.append(datetime.fromtimestamp(trade.UpdateTime()).date()) 

    return max(execution_times)


def AddNotification(template, ftrade, ftrade_value, markitwire_trade, markitwire_trade_value):
    """
    Determines the aging of a break and adds it to the recon process output.
    Appends it to the recon process output.
    Parameters:
    Template: A general description of the break.
    ftrade_number: The front arena trade number
    ftrade_value: The front arena value hat being reconciled.
    markitwire_trade: The MarkitWire trade
    markitwire_trade_value: The MarkitWire value that being reconciled.
    """

    mw_trade_execution_time = datetime.strptime(markitwire_trade[HEADINGS.index('DealDate')][:10], '%Y-%m-%d').date()
    execution_time = GetExecutionTime([ftrade], mw_trade_execution_time)

    diff = datetime.today().date() - execution_time
    days = diff.days

    AppendNotification(template, ftrade.Oid(), ftrade_value, markitwire_trade[HEADINGS.index('TradeId')], markitwire_trade_value,
                       execution_time, days)


def AppendNotification(template, ftrade_number, ftrade_value, mw_tradenumber, markitwire_trade_value, execution_time,
                       aging):
    """
    Appends it to the recon process output.
    Parameters:
    template: A general description of the break.
    ftrade_number: The Front Arena trade number
    ftrade_value: The Front Arena value hat being reconciled.
    mw_tradenumber: The MarkitWire trade number
    markitwire_trade_value: The MarkitWire value that being reconciled.
    execution_time: Last known execution time on either the Front or MarkitWire trade.
    aging: The aging of the break
    """
    RECON_ITEMS.append(
        [template, ftrade_number, ftrade_value, mw_tradenumber, markitwire_trade_value, execution_time, aging])


ael_variables = \
    [
        ['mwSourceCSVFile', 'AMWI Source CSV file', 'string', None,
         'Y:/Jhb/FALanding/Prod/MarkitWire/MarkitWire.csv', 1],
        ['mwOutputCSV', 'AMWI Output CSV file', 'string', None,
         'Y:/Jhb/FALanding/Prod/MarkitWire/MarkitWireOutput_' + str(datetime.today()).replace(':', '_').
             replace('.', '_').replace('-', '_') + '.csv', 1],
        ['mwEmailGroups', 'AMWI Emailing groups', 'string', None, 'ABCAPFrontArenaMWI@barclayscapital.com', 1],
        ['mwErrorEmailGroups', 'AMWI Error groups', 'string', None, 'ABCAPFrontArenaMWI@barclayscapital.com', 1],
        ['mwFromEmail', 'AMWI From Email Address', 'string', None, 'ABCAPFrontArenaMWI@barclayscapital.com', 1],
        ['mwMWTradingDate', 'Markit Wire Trade Inception Date', 'string', None, '2005-01-01', 1],
        ['mwMWT0Days', 'T0 Days', 'string', None, 0, 1],
        ['mwCheckMWPopulation', 'Run Entire Historical Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['mwMWNominalDirectionCheck', 'Markit Wire Nominal Direction Check', 'bool', [True, False], True, 0, 0,
         'Roll back', None, 1],
        ['mwMWNominalCheck', 'Markit Wire Nominal Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['mwMWStartEndDateCheck', 'Markit Wire Start End Date Check', 'bool', [True, False], True, 0, 0, 'Roll back',
         None, 1],
        ['mwMWDuplicatePaymentsCheck', 'Markit Wire Duplicate Payments Check', 'bool', [True, False], True, 0, 0,
         'Roll back', None, 1],
        ['mwMWStatusCheck', 'Markit Wire Status Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['mwMWFixedRateCheck', 'Markit Wire Fixed Rate Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['mwMWIncorrectUserCheck', 'Markit Wire Incorrect User', 'bool', [True, False], True, 0, 0, 'Roll back', None,
         1],
        ['mwMWInterDeskChecks', 'Markit Wire Inter-Desk Checks', 'bool', [True, False], True, 0, 0, 'Roll back', None,
         1],
        ['mwMWDefaultChecks', 'Markit Wire Default Checks', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['mwMWMirrorChecks', 'Markit Wire Intern Mirror Checks', 'bool', [True, False], True, 0, 0, 'Mirrors', None, 1],
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


def DetermineStartDate(run_historical_check, mw_inception_date, recon_num_days):
    """
    The start date is the date from which the recon will evaluate trades. If the execution date
    of a trade is on or after the start date then it will be reconciled.
    """
    if run_historical_check:
        return mw_inception_date
    else:
        return (datetime.today() + timedelta(days=recon_num_days)).date()

        
def ael_main(parameters):
    mw_inception_date = datetime.strptime(parameters['mwMWTradingDate'], '%Y-%m-%d').date()
    aging = int(parameters['mwMWT0Days']) * -1
    start_date = DetermineStartDate(parameters['mwCheckMWPopulation'], mw_inception_date, aging)

    print 'Run the AMWI Recon at {0} for trades from {1} to {2}'.format(datetime.today(), start_date,
                                                                        datetime.today())
    for param in parameters:
        if parameters[param]:
            print param, ': ', parameters[param]

    with open(parameters['mwSourceCSVFile'], 'rt') as deal_extractor:
        reader = csv.reader(deal_extractor)
        CheckAllMarkitWireTrades(parameters, start_date, reader)

    RECON_ITEMS.sort(key=lambda k: (k[6]))

    email_subject = 'MarkitWire Recon Report {0} - {1}'.format(start_date, str(datetime.now().date()))
    process_notification(parameters['mwOutputCSV'], parameters['mwFromEmail'], parameters['mwEmailGroups'],
                         email_subject)

    print 'AMWI Recon completed succesfully at ' + str(datetime.today())
