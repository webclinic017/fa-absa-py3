'''
-----------------------------------------------------------------------
MODULE
    OPS_PreSettlement Confirmation

DESCRIPTION
    

    Date                : 2010-04-08
    Purpose             : send emails to the counterparty to confirm details before settlement 
    Department and Desk : Operations
    Requester           : Bruce Dell
    Developer           : Sanele Macanda
    CR Number           : CHNG0001829143
---------------------------------------------------------------------------
'''

import acm
import re
import ael
import OPS_Pre_Confirmation_Config
from datetime import datetime
from at_email import EmailHelper
from zak_funcs import formnum
from string import Template

def money_flow_value(money_flow, end_date, column_id):
    '''This method returns a value for any money flow object'''
    mf_calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FMoneyFlowSheet')

    value = 0

    try:
        mf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        mf_calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', end_date)
            
        calc  = mf_calc_space.CreateCalculation(money_flow, column_id)
        value = calc.Value()
            
        if hasattr(value, "IsKindOf") and value.IsKindOf(acm.FDenominatedValue):
            value = value.Number()
    finally:
        mf_calc_space.Clear()
        mf_calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        mf_calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        
    return value

def send_html_email(email_data, to):

    mail_from = ""
    mail_to =  [to]
    subject = '%s Settlement for %s %s on %s' %(email_data['counterparty_name'],
                                                    email_data['curr'],
                                                    email_data['amount'],
                                                    email_data['date'])
    email = EmailHelper(email_data['email_body'], subject, mail_to, mail_from)
    email.send()

def create_mail(pay_day, trades):
    '''this method creates the body of the email using an HTML template sheet file'''
    table_rows = ''
    sum_projected = 0
    
    #Obtaining the first trade and Money_flow to obtain static data
    trade = trades[0] 
    first_moneyFlow = trade.MoneyFlows(pay_day, pay_day)[0]
    ael_pay_day_format = datetime.strptime(pay_day, '%Y-%m-%d').strftime('%d/%m/%Y')
    table_rows = []
    
    for t in trades:
        if not t.Status() in ('Simulated', 'Void'):
            for money_flow in t.MoneyFlows(pay_day, pay_day):
                if pay_day == money_flow.PayDate():
                
                    projected = money_flow_value(
                                money_flow, 
                                pay_day, 
                                'Cash Analysis Projected')
                                
                    row_template=Template(OPS_Pre_Confirmation_Config.table_row_template)
                    row = row_template.safe_substitute(
                        {'counterparty': money_flow.Counterparty().Name(),
                        'trade_number': t.Oid(),
                        'instype': t.Instrument().InsType(),
                        'trade_nominal': formnum(t.Nominal()),
                        'pay_date': ael_pay_day_format ,
                        'currency': t.Currency().Name(),
                        'projected': formnum(projected)})
                    table_rows.append(row)
                    sum_projected += projected
                
    #calculates the sum of the project cashflow amounts
    row_sum = Template(OPS_Pre_Confirmation_Config.table_row_template)
    row_sum = row_sum.safe_substitute({
                        'counterparty':'',
                        'trade_number': '',
                        'instype': '',
                        'trade_nominal': '',
                        'pay_date': '',
                        'currency': '',
                        'projected': formnum(sum_projected)})
                        
    if (sum_projected >= 0):
    
        account = first_moneyFlow.AcquirerAccount().Account()
        splitAccount = account.split(' ')
        
        #Getting the acquirer details
        email_template=Template(OPS_Pre_Confirmation_Config.email_template)
        email = email_template.safe_substitute(
            {'value_date': ael_pay_day_format,
            'currency': first_moneyFlow.AcquirerAccount().Currency().Name(),
            'action': 'You pay us',
            'projected_payment': formnum(abs(sum_projected)),
            'table_rows': ' '.join(table_rows),
            'table_sum': row_sum,
            'bank': first_moneyFlow.AcquirerAccount().CorrespondentBank().Name(),
            'account_number': splitAccount[1],
            'branch_code': splitAccount[0],
            'swift_addr': first_moneyFlow.AcquirerAccount().Bic().Alias()}
            )
    else:
        
        account= first_moneyFlow.CounterpartyAccount().Account()
        splitAccount= account.split(' ')
        
        #Getting the counterparty details
        email_template=Template(OPS_Pre_Confirmation_Config.email_template)
        email = email_template.safe_substitute(
            {'value_date': ael_pay_day_format,
            'currency': first_moneyFlow.CounterpartyAccount().Currency().Name(),
            'action': 'We pay you',
            'projected_payment': formnum(abs(sum_projected)),
            'table_rows': ' '.join(table_rows),
            'table_sum': row_sum,
            'bank': first_moneyFlow.CounterpartyAccount().CorrespondentBank().Name(),
            'account_number': splitAccount[1],
            'branch_code': splitAccount[0],
            'swift_addr': first_moneyFlow.CounterpartyAccount().Bic().Alias()}
            )
    
    return {'email_body': email, 
            'counterparty_name': trade.Counterparty().Name(),
            'curr':t.Currency().Name(),
            'amount': formnum(sum_projected),
            'date': ael_pay_day_format}
    

ael_variables = [   
                    ['PayDay', 'Pay Day: (yyyy-mm-dd)', 'string', None],
                    ['tradeNo', 'Trade Numbers', acm.FTrade, None, None, None, 1]
                ]  
                
def valid_date_format(date):
    '''Checks if the date enetered is an acm date format'''
    proj = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    if proj.search(date):
        return True
        
    else:
        return False
    
def ael_main(ael_dict):
    
    trades = ael_dict['tradeNo']
    pay_day = ael_dict['PayDay']
    
    if valid_date_format(pay_day):
            
        if trades:
            mail = create_mail(pay_day, trades)
            user = user = acm.User()
            
            '''This emailing solution is not ideal, but is the best solution given the fact that not
            all users on FA have their windows logon as FA username. Best solution would be for email
            to go straight to the client, but business first one to be confident that all static data
            is in order. As such, this is only a temporary functionality.'''
            try:
                send_html_email(mail, user.Name())
                return
            except Exception, e:
                print e
                
            try:
                send_html_email(mail, user.AdditionalInfo().AB_Number())
                return
                
            except Exception, e:
                print e
        else:
            ael.log('Please enter trade(s)') 

    else:
        raise ValueError('Incorrect data format, should be YYYY-MM-DD')
    
