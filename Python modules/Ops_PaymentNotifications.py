"""-----------------------------------------------------------------------------
PURPOSE                 :  This script will evaluate all trades contained within a specified compound portfolio. 
                           If there's a valid trade (in specified statusses) with pay date within specified range from report date, 
                           the money flow will be included in the report.
                           Then the script will send out an email notification to the specified destinations as well as save down the report.
                           AAM Query folder used: AAM_PaymentNotifications
                           
DEPATMENT AND DESK      :  AAM
REQUESTER               :  Chris Watts
DEVELOPER               :  Rohan van der Walt
CR NUMBER               :  
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no  Developer                 Description
--------------------------------------------------------------------------------
2015-02-26  2419446    Rohan vd Walt             Initial Implementation
"""

import acm
from at_time import add_delta, bankingday_timediff, date_today
import NamespaceTimeFunctions
from at_email import EmailHelper
import string
import FBDPGui

from at_ael_variables import AelVariableHandler


def enable_email_hook(selected_variable):
    test = (selected_variable.value == 'Yes')
    ael_variables[3][9] = test
    ael_variables[3][5] = test
    return selected_variable

ael_variables = AelVariableHandler()

ael_variables.add('PositionsQF',
                  mandatory=True,
                  cls='FStoredASQLQuery',
                  collection=acm.FStoredASQLQuery.Instances(),
                  multiple=True,
                  label='Position Filter',
                  alt='The Query Folder that returns the positions to be checked for due payments')

ael_variables.add('DaysToPayDate',
                  mandatory=True,
                  cls='int',
                  label='Business Days to PayDate',
                  alt='How many days before PayDate should the cashflow be included in the report')

ael_variables.add('SendEmail',
                  mandatory=True,
                  label='Send Email',
                  collection=['Yes', 'No'],
                  default='Yes',
                  hook=enable_email_hook,
                  alt='This will send email to receipients in addition to the file report')

ael_variables.add('EmailDestinations',
                  mandatory=True,
                  label='Email Destinations',
                  alt='Email Destinations - Comma Seperated')

ael_variables.add('OutputLocation',
                  mandatory=True,
                  label='Report Output Location',
                  alt='Location where report will be saved')

class PayDateReport:

    def __init__(self, positionQF, business_days):
        self.cashflows = set()
        self.positionQF = positionQF
        self.business_days = business_days

    def add_cashflow(self, cashflow):
        self.cashflows.add(cashflow)

    def __str__(self):
        result = 'Payments Due Notification on %s \n' % str(date_today())
        result += '\nChecking within Query Folder:\t%s\n' % self.positionQF.Name()
        result += '\nThe following cashflows are due within %s business days:\n' % self.business_days
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        for cf in sorted(self.cashflows, key=lambda x: (x.PayDate()[:10], x.Trade().Name(), x.Type() )):
            try:
                proj_cf = cf.Calculation().Projected(calcSpace).Number()
            except:
                proj_cf = 'ERROR'

            result += '\tPay Date: %s Instrument: %-50s Amount: %-15s (%s)\n' % (cf.PayDay(), cf.Trade().Instrument().Name() + '(' + cf.Trade().Name() + ')', proj_cf, cf.Type())
        return result

    def write_to_file(self, fullpath):
        try:
            f = open(fullpath, "w+")
            f.write(str(self))
            f.close()
            print 'Secondary output written to', fullpath
        except Exception, e:
            print 'ERROR: Could not write report', e
            raise e

    def send_mail(self, email_from, email_to, email_subject):
        import smtplib
        email_host = acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(),
                'mailServerAddress').Value()
        email_body = string.join((
            "From: %s" % email_from,
            "To: %s" % email_to,
            "Subject: %s" % email_subject,
            "", str(self)), "\r\n")
        if not email_host:
            raise Exception("Could not initialise the smtp Host")
        server = smtplib.SMTP(email_host)
        server.sendmail(email_from, email_to.split(','), email_body)
        server.quit()

def pays_within(moneyflow, business_days):
    pay_date = moneyflow.PayDay()
    if pay_date:
        today = str(date_today())
        date_end = add_delta(today, business_days)
        timediff = bankingday_timediff(moneyflow.Currency().Calendar(), today, pay_date)
        if timediff.days >= 0 and timediff.days <= business_days:
            return True
        else:
            return False
    else:
        return False

def ael_main(param_dict):
    paydate_report = PayDateReport(param_dict['PositionsQF'][0], param_dict['DaysToPayDate'])
    today = acm.Time().DateToday()
    endDate = NamespaceTimeFunctions.DateAddDeltaType(None, today, 1, 'm')
    print 'Checking trades in Query Folder'
    for trade in param_dict['PositionsQF'][0].Query().Select():
        for mf in trade.MoneyFlows(today, endDate):
            if pays_within(mf, param_dict['DaysToPayDate']) and mf.Type() not in ['Redemption Amount', 'Call Fixed Rate Adjustable']:
                paydate_report.add_cashflow(mf)

    print 'Writing to file'
    paydate_report.write_to_file(param_dict['OutputLocation'])
    if (param_dict['SendEmail'] == 'Yes'):
        print 'Sending email'
        try:
            ENVIRONMENT = ' - ' + acm.FInstallationData.Select('').At(0).Name()
        except:
            ENVIRONMENT = ''        
        paydate_report.send_mail('ABCapITRTBFrontArena@absacapital.com', 
            param_dict['EmailDestinations'], 
            'Instrument Expiry Notification - ' + str(date_today()) + ENVIRONMENT)
    print 'Completed Successfully'
