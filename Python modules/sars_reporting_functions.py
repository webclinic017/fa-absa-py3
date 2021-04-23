'''-------------------------------------------------------------------------------------------------
MODULE
    sars_reporting_functions

DESCRIPTION
    Date      : 2020-02-28
    Purpose   : General functions for IT3 reports and FATCA/CRS
    Developer : Qaqamba Ntshobane
    Requester : Nhlanhleni Mchunu
    Department: PCG

=======================================================================================================
HISTORY:
    Date:               Change No:      Developer:              Description:   
-------------------------------------------------------------------------------------------------------
    2020-02-28          PCGDEV-325      Qaqamba Ntshobane       Initial Design
    2020-09-28          PCGDEV-540      Qaqamba Ntshobane       Added BoUV function
    2021-03-18          PCGDEV-686      Qaqamba Ntshobane       Extended functions for FATCA/CRS report

ENDDESCRIPTION
----------------------------------------------------------------------------------------------------'''

import acm
import math
import currentNominal

from at_time import acm_date
from collections import defaultdict
from FUploaderFunctions import add_row, send_report
from FUploaderParams import TODAY, ENV, EMAIL_SENDER, CALENDAR

PROJECTED_AMOUNT = 'Cash Analysis Projected'
MONEYFLOW_CS = acm.Calculations().CreateCalculationSpace('Standard', 'FMoneyFlowSheet')
DEALSHEET_CS = acm.FCalculationMethods().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')


def usd_rate(curr_to, date, *rest):

    currency = acm.FInstrument[curr_to.insid]
    return get_rate(currency, date)


def get_rate(currency, date):

    if acm.Time.DateToYMD(date)[1] in [3, 9]:
        date = acm.Time.DateAddDelta(date, 0, 0, -1)

    usd = acm.FInstrument['USD']
    usd_zar = usd.UsedPrice(date, 'ZAR', 'SPOT')
    curr_usd = usd.UsedPrice(date, currency, 'SPOT')

    if not curr_usd == 0.0:
        return float(usd_zar / curr_usd)

    set_global_variables(date)
    return float(1.0)


def ins_expires_in_period(ael_ins, end_period_date, *rest):

    ins = acm.FInstrument[ael_ins.insaddr]
    return ins_expires_in_period_(ins, end_period_date)


def ins_expires_in_period_(ins, end_period_date):

    end_period_date = fa_date(end_period_date)
    end_month = acm.Time.DateToYMD(end_period_date)[1]
    start_period_date = (acm.Time.DateAddDelta(end_period_date, 0, -12, 0) if end_month == 3 else 
                        acm.Time.DateAddDelta(end_period_date, 0, -6, 0))

    if ins.ExpiryDate():
        if ins.ExpiryDate().split(' ')[0] >= start_period_date:
            return 1
        return 0
    return 1


def get_nominal(ael_trade, date, *rest):

    if acm.Time.DateToYMD(date)[1] in [3, 9]:
        date = acm.Time.DateAddDelta(date, 0, 0, -1)

    trade = acm.FTrade[ael_trade.trdnbr]
    instrument = trade.Instrument()

    if instrument.InsType() == 'Deposit':
        leg = instrument.Legs()

        if not leg:
            return 0
        nom = currentNominal.currentNominal(leg[0], date, [trade])
    else:
        nom = trade.Nominal()

    if is_foreign_currency(trade):
        return nom * get_rate(trade.Currency().Name(), date)
    return nom


def get_bouv(ael_trade, date, *rest):

    trade_object = acm.FTrade[ael_trade.trdnbr]
    instrument = trade_object.Instrument()

    cash_end = get_cash_end(trade_object, date)
    val_end = get_val_end(trade_object, date)

    bouv = cash_end + val_end
    if math.isnan(bouv):
        return 0
    return bouv


def get_premium(ael_trade, date, *rest):

    trade = acm.FTrade[ael_trade.trdnbr]
    instrument = trade.Instrument()

    if instrument.InsType() in ['Deposit', 'CD']:
        prem = trade.FaceValue()
    else:
        prem = trade.Premium()

    if is_foreign_currency(trade):
        return prem * get_rate(trade.Currency().Name(), date)
    return prem


def sold(ael_trade, *rest):

    return not acm.FTrade[ael_trade.trdnbr].Bought()


def is_foreign_currency(ael_trade):

    return ael_trade.Currency().Name() != 'ZAR'


def get_closing_balance(trade, start_date, end_date):

    closing_balance = 0
    start_date = fa_date(start_date)
    end_date = fa_date(end_date)
    account_close_date = trade.Instrument().ExpiryDate().split(' ')[0]

    set_global_variables(start_date, end_date)
    cash_end = DEALSHEET_CS.CalculateValue(trade, 'Portfolio Cash End').Number()
    cash_balance = DEALSHEET_CS.CalculateValue(trade, 'Deposit balance').Number()
    accrued_interest = DEALSHEET_CS.CalculateValue(trade, 'Portfolio Accrued Interest').Number()

    if trade.Instrument().IsCallAccount():
        closing_balance = cash_balance + accrued_interest
    else:
        closing_balance = cash_end - accrued_interest

    remove_global_simulations()
    return amount(trade, end_date, closing_balance)


def fa_date(date):

    return CALENDAR.AdjustBankingDays(date, 0)


def get_period_dates(end_date):

    end_month = acm.Time.DateToYMD(end_date)[1]
    validate_date(end_month)

    start_date = (acm.Time.DateAddDelta(end_date, 0, -12, 0) if end_month in [3, 1] else 
                 acm.Time.DateAddDelta(end_date, 0, -6, 0))

    return start_date, acm.Time.DateAddDelta(end_date, 0, 0, -1)


def validate_date(end_month):

    if end_month not in [3, 9, 1]:
        raise Exception('Incorrect end of period month. Period end month should '
                        'be 3 or 9 (Mar or Sep) for IT3B or FATCA/CRS, and 1 (Jan) for VAT')


def get_instrument_start_date(trade):

    ins_start_date = trade.Instrument().StartDate()

    if not ins_start_date:
        return trade.ValueDay()
    return ins_start_date


def get_instrument_end_date(trade, end_date):

    ins_exp_date = trade.Instrument().ExpiryDate()
    end_date = fa_date(end_date)

    ins_end_date = (ins_exp_date if (ins_exp_date and ins_exp_date < end_date) else end_date)
    return str(ins_end_date)[:10]


def get_account_number(money_flow):

    if not money_flow:
        return 'N/A'

    money_flow = money_flow[0]
    
    if money_flow.CounterpartyAccount():
         return money_flow.CounterpartyAccount().Account()

    if money_flow.AcquirerAccount():
        return money_flow.AcquirerAccount().Account()
    return 'N/A'


def send_success_notification(email_addresses, report_type, report_name=None):

    report_name = report_name if report_name else 'Report'

    if email_addresses:
        row_info = ['SUCCESS', '{0} produced successfully. Check TradingManager folder'.format(report_name)]
        add_row('SUCCESS', row_info)
        send_report(email_addresses, EMAIL_SENDER,
                    '{type} Report Status {today} - {env}'.format(type=report_type, today=TODAY, env=ENV),
                    '{type} Report Status'.format(type=report_type))


def amount(trade, date, value):

    if isinstance(value, float):
        if is_foreign_currency(trade):
            return value * get_rate(trade.Currency().Name(), date)
        return value

    if math.isnan(value) or not hasattr(value, "Number"):
        return 0

    if is_foreign_currency(trade):
        return value.Number() * get_rate(trade.Currency().Name(), date)
    return value.Number()


def get_val_end(trade, date, set_global_vars=True):

    if set_global_vars:
        set_global_variables(fa_date(date))
    val_end = DEALSHEET_CS.CalculateValue(trade, 'Total Val End')

    return amount(trade, date, val_end)


def get_cash_end(trade, date, set_global_vars=True):

    if set_global_vars:
        set_global_variables(fa_date(date))
    cash_end = DEALSHEET_CS.CalculateValue(trade, 'Portfolio Cash End')

    return amount(trade, date, cash_end)


def get_accrued_interest(trade, start_date, end_date):

    set_global_variables(fa_date(end_date), fa_date(start_date))
    accrued_interest = DEALSHEET_CS.CalculateValue(trade, 'Portfolio Accrued Interest')

    return amount(trade, end_date, accrued_interest)


def get_settled_interest(trade, start_date, end_date):

    set_global_variables(fa_date(end_date), fa_date(start_date))
    settled_interest = DEALSHEET_CS.CalculateValue(trade, 'Portfolio Settled Interest')

    return amount(trade, end_date, settled_interest)


def get_projected_amount(moneyflow, end_date):

    projected_amount = MONEYFLOW_CS.CalculateValue(moneyflow, PROJECTED_AMOUNT)

    return amount(moneyflow, end_date, projected_amount)


def get_moneyflows(trade, start_date, end_date):

    moneyflows_dict = {}
    moneyflows = trade.MoneyFlows()
    payments = trade.Payments()

    for moneyflow in moneyflows:
        if start_date <= moneyflow.PayDay() < end_date and moneyflow.Type() != 'None':
            moneyflows_dict.setdefault(moneyflow.Type(), 0.0)

            amount = get_projected_amount(moneyflow, end_date)
            moneyflows_dict[moneyflow.Type()] += amount if amount < 0 else 0
        
    for payment in payments:
        if start_date <= payment.PayDay() < end_date and payment.Type() == 'Aggregated Forward Premium':
            moneyflows_dict.setdefault(payment.Type(), 0.0)
            
            amount = payment.Amount()
            moneyflows_dict[payment.Type()] += amount if amount < 0 else 0
    return moneyflows_dict


def set_global_variables(end_date, start_date='Inception'):

    if start_date == 'Inception':
        start_date = acm_date(start_date)

    global_simulations = [('Portfolio Profit Loss Start Date', 'Custom Date'),
                          ('Portfolio Profit Loss Start Date Custom', start_date),
                          ('Portfolio Profit Loss End Date', 'Custom Date'),
                          ('Portfolio Profit Loss End Date Custom', end_date),
                          ('Valuation Date', end_date),
                          ('Valuation Parameter Date', end_date),
                         ]

    for column, value in global_simulations:
        DEALSHEET_CS.SimulateGlobalValue(column, value)


def remove_global_simulations():

    DEALSHEET_CS.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')
    DEALSHEET_CS.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
    DEALSHEET_CS.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    DEALSHEET_CS.RemoveGlobalSimulation('Portfolio Profit Loss End Date')

    DEALSHEET_CS.RemoveGlobalSimulation('Valuation Date')
    DEALSHEET_CS.RemoveGlobalSimulation('Valuation Parameter Date')

