'''
Date                    : ?????, 2010-10-27
Purpose                 : Test if portfolio that is linked to the settlement (normal or netted) rolls up to the GRAVEYARD portfolio. If so, we do not settle.
                          Amended script to use continues instead of breaks which was causing the script to exit without completing.
Department and Desk     : Ops Money Market Settlements
Requester:              : Martie Waite
Developer               : Heinrich Cronje/Anwar Banoo/Bhavnisha Sarawan, Anwar Banoo
CR Number               : ?????, 476845

23/05/2018      Elaine Visagie          Bhavnisha Sarawan       Rollback, excluding counterparties, changed filter to only include BO and BO BO Confirmed trades, added print statements for pseudo dry run
21/11/2018      Bhavnisha Sarawan       Jaysen Naicker          Code refactor
09/05/2019                              Jaysen Naicker          Refactor passing of varibles for reporting
'''

import acm
from at_email import EmailHelper
from at_ael_variables import AelVariableHandler
from SAGEN_IT_Functions import set_AdditionalInfoValue_ACM
import at_logging

LOGGER = at_logging.getLogger()

Today = acm.Time().DateToday()
Ins_zar = acm.FInstrument['ZAR']
Yesterday = Ins_zar.Calendar().AdjustBankingDays(Today, -1)
ael_variables = AelVariableHandler()

ael_variables.add('QueryFolder',
    label='Query Folder:',
    cls=acm.FStoredASQLQuery,
    collection=sorted(acm.FStoredASQLQuery.Select("subType='FSettlement'")),
    mandatory = True,
    alt='Query folder to process')
    
ael_variables.add('EmailAddress',
    label='Email Address:',
    alt='Use a comma as a separator',
    mandatory = False,
    multiple=True)

ael_variables.add('TestMode',
    label='Test Mode',
    collection=['Yes', 'No'],
    alt='Use test mode')


def Call_Rolling_Interest(Settle, To_date):
    # Check that the rolling base date will equal the to_date after it is rolled over
    Leg = Settle.CashFlow().Leg()
    Gendate = Leg.RollingPeriodBase()
    if Leg.RollingPeriod() != '0d': 
        while Gendate <= acm.Time.DateAdjustPeriod(To_date, '-1m'):
            Gendate = acm.Time.DateAdjustPeriod(Gendate, Leg.RollingPeriod())
            
        Gendate = Ins_zar.Calendar().ModifyDate(None, None, Gendate, Leg.ResetDayMethod())   
        if Gendate == To_date:
            return 'in'
    return 'out'
    

def release_Settlement(Settlement, Pay_Type, AddinfoValue, TestMode):
    # Update additionalinfo with appropriate message and release settlement
    LOGGER.info("Releasing %s - %s" % (Pay_Type, Settlement.Oid()))
    if TestMode == 'No':
        set_AdditionalInfoValue_ACM(Settlement, 'Call_Confirmation', AddinfoValue) 
        acm.PollDbEvents()
        try:
            Settlement.Status('Released')
            Settlement.Commit()
            LOGGER.info("Successfully released %s - %s."% (Pay_Type, Settlement.Oid()))
            return True
        except Exception as E:
            LOGGER.error("Failed to release %s - %s. %s" % (Pay_Type, Settlement.Oid(), E))
            return False
    return None


def send_Email(EmailAddress, Tot, Matched, Success, Failed):
    Subject = 'Report %s run for %s' %(__name__, Today)
    MailTo = list(EmailAddress)
    MailFrom = 'ABCapITRTBAMFrontAre@absa.africa'
    Body = "<b>Looped through %s settlements (%s match criteria): </b><br>"\
       "%s successfully released<br>" \
       "%s failed to be released<br>" % (Tot, Matched, Success, len(Failed))
    for Fail in Failed:
        Body = Body + '%s failed <br>' %(Fail)

    Email = EmailHelper(Body, Subject, MailTo, MailFrom)
    Email.sender_type = EmailHelper.SENDER_TYPE_SMTP
    Email.host = EmailHelper.get_acm_host()
    try:
        Email.send()
        LOGGER.info('Email sent')
    except Exception as E:
        LOGGER.error("!!! Exception: {0}\n".format(E))

    return
    
def ael_main(Ael_variables):
    QueryFolder =  Ael_variables['QueryFolder']
    EmailAddress =  Ael_variables['EmailAddress']
    TestMode = Ael_variables['TestMode']
    Tot = 0
    Success = 0
    Matched = 0
    Failed = []

    if TestMode == 'Yes': LOGGER.info('Running in test mode...')
    LOGGER.info("Starting processing in module %s for %s ...." %(__name__, Today))
    if QueryFolder.Query().Select():
        Settlements = QueryFolder.Query().Select()
        Tot = len(Settlements)
        for Settle in Settlements:
            LOGGER.info("Processing settlement %s of type %s in status %s for trade %s." % \
                (Settle.Oid(), Settle.Type(), Settle.Trade().Status(), Settle.Trade().Oid()))
            Fund_instype = Settle.Trade().AdditionalInfo().Funding_Instype()
            Pay_Type = ''
            AddinfoValue = ''
            
            if Fund_instype=='FDI':
                # Check for annuity settlement
                Pay_Type = 'Annuity Settlement'
                AddinfoValue = 'Auto annuity Payment'
                
            if Fund_instype[0:4] == 'Call' or Fund_instype[0:19] == 'Access Deposit Note':
                # Check for call account interest settlement
                CashFlow = Settle.CashFlow()
                if Call_Rolling_Interest(Settle, Today)=='in'\
                    and (Settle.Type()=='Fixed Rate Adjustable' \
                        or (Settle.Type()=='Call Fixed Rate Adjustable' \
                        and ((CashFlow.StartDate() <= Yesterday < CashFlow.EndDate())\
                            or (Ins_zar.Calendar().ModifyDate(None, None, CashFlow.EndDate(), 'Following') != CashFlow.PayDate() and CashFlow.PayDate() == Today)))):
                    Account = acm.FAccount.Select01("name = '%s' and party = '%s'" %(Settle.CounterpartyAccName(), Settle.Counterparty().Name()), '')
                    if Account and Account.Bic():
                        if Account.Bic().Type().Name() == 'SWIFT':
                            Pay_Type = 'Call Account Interest'
                            AddinfoValue = 'Auto Int Payment'
                    
            if Pay_Type <> '':
                # If matched settlements then release
                Matched = Matched + 1
                ret = release_Settlement(Settle, Pay_Type, AddinfoValue, TestMode)
                if ret == True:
                    Success = Success + 1
                if ret == False:
                    Failed.Add('%s - %s' %(Settle.Oid(), Pay_Type))
                    
    if len(EmailAddress):
        # If valid email address/es then send emails
        send_Email(EmailAddress, Tot, Matched, Success, Failed)

    LOGGER.info("Finished processing in module %s ...." %(__name__))
