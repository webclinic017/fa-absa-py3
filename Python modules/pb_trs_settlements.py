'''
Created on 20 Oct 2016

@author: conicova
'''
import ael
import acm
from collections import defaultdict
import os
from datetime import datetime
from collections import namedtuple

from at_ael_variables import AelVariableHandler
from at_email import EmailHelper
from at_logging import getLogger
from at_report import CSVReportCreator
from PS_FormUtils import DateField
from at_time import ael_date

LOGGER = getLogger()

DELIMETER = ","

EXCLUDE_CP = ['ACQ STRUCT DERIV DESK', 'EQ Derivatives Desk']

class SettlementsReport(CSVReportCreator):

    def __init__(self, full_file_path, content, header):
        file_name = os.path.basename(full_file_path)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(full_file_path)

        super(SettlementsReport, self).__init__(file_name_only, file_suffix, file_path)
        self.content = content
        self.header = header

    def _collect_data(self):
        LOGGER.info("Outputing Data (%s):", len(self.content))
        for row in self.content:
            LOGGER.info(";".join(row))

    def _header(self):
        return self.header

def _check_type(trade):
    for leg in trade.Instrument().Legs():
        if leg.LegType() == 'Total Return':
            und_ins = leg.IndexRef()
            if und_ins.InsType() == 'Stock':
                return (und_ins, True)
            else:
                return (und_ins, False)

    return (None, None)

def _get_dividends(ins, ex_div_day, is_stock):
    """ Method to obtain the dividends
    """
    result = []
    if not is_stock:
        for link in ins.CombinationMaps():
            for div in link.Instrument().Dividends():
                if ex_div_day == div.ExDivDay():
                    idxpt = link.Weight() / ins.Factor()
                    result.append(idxpt, div.ExDivDay(), div.PayDay(), div.Amount())
    else:
        for div in ins.Dividends():
            if ex_div_day == div.ExDivDay():
                result.append(1, div.ExDivDay(), div.PayDay(), div.Amount())
                break

    return result

def _reset_order(reset_vector):
    """ Method to obtain the min and max resets, ordered by date

    Arguments:
        reset_vector -- [(type, date, value)]
    """
    reset_vector = filter(lambda item: item[0] == 'Return', reset_vector)
    min_pair = min(reset_vector, key=lambda t: t[1])
    max_pair = max(reset_vector, key=lambda t: t[1])

    return (str(min_pair[1]), str(min_pair[2]), str(max_pair[1]), str(max_pair[2]))

def _reset_fwd_rate(reset):
    """ Method to obtain estimate value of reset

    Arguments:
        reset -- the reset object.
    """
    context = acm.GetDefaultContext()
    sheetType = 'FMoneyFlowSheet'
    columnName = 'Cash Analysis Fixing Estimate'
    calcSpace = acm.Calculations().CreateCalculationSpace(context, sheetType)
    fwdRateDenomValue = calcSpace.CalculateValue(reset, columnName).Value()
    try:
        fwdRate = fwdRateDenomValue.Number() * 100.0
    except:
        fwdRate = 0.0
    return fwdRate

def send_email(pay_date_start, pay_date_end, portfolio_names, emails, attachments=None):
    """Send generated report."""
    env = acm.FDhDatabase['ADM'].InstanceName()
    pay_date_start = datetime.strptime(pay_date_start, '%Y-%m-%d').strftime('%d/%m/%Y')
    pay_date_end = datetime.strptime(pay_date_end, '%Y-%m-%d').strftime('%d/%m/%Y')
    portfolio_name = ";".join(portfolio_names)
    portfolio_name_subject = portfolio_name[0:min(20, len(portfolio_name))]
    subject = "Settlement amounts for TRSs for '{3}' {0} - {1} ({2})".format(pay_date_start,
                                                                           pay_date_end,
                                                                           env,
                                                                           portfolio_name_subject)
    body = "Hi,<BR><BR>" \
           "Please see attached TRSs reports for '{2}' {0} - {1}.<BR><BR>" \
           "Regards,<BR>" \
           "Prime and Equities BTB team<BR><BR>".format(pay_date_start, pay_date_end, portfolio_name)
    emailHelper = EmailHelper(body, subject, list(emails), attachments=attachments)

    if str(acm.Class()) == "FACMServer":
        emailHelper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        emailHelper.host = EmailHelper.get_acm_host()

    try:
        emailHelper.send()
    except Exception:
        LOGGER.exception("Error sending e-mail with Recon report.")

def email_hook(selected_variable):
    """Modify e-mail address based on user's organisation."""
    user = '.'.join([name.lower() for name in acm.User().FullName().split(' ')])
    address = '@'.join([user, 'barclayscapital.com'])

    emails = selected_variable.handler.get('emails')
    if emails.value == "":
        emails.value = address

ael_variables = AelVariableHandler()

ael_variables.add('pay_date_start',
                  label='Star Pay Date Delta',
                  default='0',
                  alt='Start pay date delta (the number of business days to add to current date)')

ael_variables.add('pay_date_end',
                  label='End Pay Date Delta',
                  default='0',
                  alt='End pay date delta (the number of business days to add to current date)')

ael_variables.add('portfolios',
                    label='Portfolio names',
                    cls='FPhysicalPortfolio',
                    default='',
                    multiple=True,
                    alt='Physical portfolio names.'
                )

ael_variables.add("cf_report_filename",
                  label="CF Report Filename",
                  mandatory=True)

ael_variables.add("reset_report_filename",
                  label="Reset Report Filename",
                  mandatory=True)

ael_variables.add("emails",
                  label="Emails",
                  multiple=True,
                  alt="Email destinations. Use comma seperated email addresses \
                       if you want to send report to multiple users.",
                  hook=email_hook,
                  mandatory=False)

def _work(report_filename, pay_date_start, pay_date_end, content, header):
    report_filename = "{0}_{1}_{2}.csv".format(report_filename, pay_date_start, pay_date_end)
    report = SettlementsReport(report_filename, content, header)
    report.create_report()
    LOGGER.info("Secondary output wrote to %s", report_filename)

    return report_filename


RESET_COLUMNS = ['Trade No.', 'Date', 'Type', 'Value', 'Estimate', 'Pay Day', 'Float Rate']
CF_COLUMNS = ['Portfolio',
'Counterparty',
'Underlying',
'Quantity',
'Initial Price',
'Spread',
'Long or Short',
'Execution Date',
'Maturity Date',
'Nominal',
'Trade No.',
'Start Date',
'Instrument Currency',
'Float Roling Days/Month/Years',
'Equity Roling Days/Month/Years',
'Float Convention',
'Equity Convention',
'Float Rolling Number',
'Equity Rolling Number',
'Interest Rate Reset Gap',
'Status',
'Day Count Method',
'Dividend Factor',
'Instrument ID',
'CF Type',
'Div Factor',
'Nominal Scale',
'Start',
'Start Fix',
'End',
'End Fix',
'Pay Day',
'Projected CF',
'Leg Currency',
'Index Pt']

CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()
def get_projected_cf(cashflow, trd):
    return cashflow.Calculation().Projected(CALC_SPACE, trd).Number()

def get_reset_row(rs, t, leg):
    result = [t.Oid(), rs.Day(), rs.ResetType(), rs.FixingValue(), _reset_fwd_rate(rs),
            rs.CashFlow().PayDate(), leg.FloatRateReference().Name()]

    return map(lambda i: str(i), result)

def get_cf_row(cf, t, leg, nominal_scale=1, min_date="", min_value="", max_date="", max_value="", ex_div_day="", pay_date="", dividend="", idxpt=""):
    underlying = ('None' if leg.IndexRef() is None
                  else leg.IndexRef().Name())


    float_conv = ""
    float_rolling_period = ""
    float_rolling_num = ""
    interest_reset_gap = ""
    day_count = ""

    if leg.LegType() == 'Float':
        float_conv = leg.PayDayMethod()
        float_rolling_period = leg.RollingPeriodUnit()
        float_rolling_num = leg.RollingPeriodCount()
        interest_reset_gap = leg.ResetDayOffset()
        day_count = leg.DayCountMethod()

    equity_conv = ""
    equity_rolling_period = ""
    equity_rolling_num = ""
    if leg.LegType() == 'Total Return':
        equity_conv = leg.PayDayMethod()
        equity_rolling_period = leg.RollingPeriodUnit()
        equity_rolling_num = leg.RollingPeriodCount()

    ins = t.Instrument()
    projected_cf = get_projected_cf(cf, t)

    result = [t.Portfolio().Name(),
            t.CounterpartyId(),
            underlying,
            t.Quantity(),
            leg.InitialIndexValue(),
            leg.Spread(),
            'Short' if t.Quantity() > 0 else 'Long',
            t.ExecutionDate(),
            leg.EndDate(),
            leg.InitialIndexValue() * t.Quantity(),
            t.Oid(),
            leg.StartDate(),
            ins.Currency().Name(),
            float_rolling_period,
            equity_rolling_period,
            float_conv,
            equity_conv,
            float_rolling_num,
            equity_rolling_num,
            interest_reset_gap,
            t.Status(),
            day_count,
            ins.DividendFactor(),
            ins.Name(),
            cf.CashFlowType(),
            ins.DividendFactor(),
            nominal_scale,
            min_date,
            min_value,
            max_date,
            max_value,
            cf.PayDate(),
            projected_cf,
            leg.Currency().Name(),
            idxpt
            ]

    return map(lambda i: str(i), result)

def ael_main(config):

    today = acm.Time.DateToday()
    calendar = acm.FCalendar['ZAR Johannesburg']
    pay_date_start = calendar.AdjustBankingDays(today, config['pay_date_start'])
    pay_date_end = calendar.AdjustBankingDays(today, config['pay_date_end'])

    report_data = defaultdict(list)
    reset_data = []
    cf_data = []

    portfolios = config['portfolios']
    for portfolio in portfolios:
        for t in portfolio.Trades():
            if t.Status() in ('Void', 'Simulated', 'Terminated'):
                continue
            if t.Counterparty().Name() in EXCLUDE_CP:
                continue
            if (t.Instrument().InsType() != 'TotalReturnSwap' or t.Instrument().IsExpired()):
                continue

            LOGGER.info("Trd: %s, YourRef: %s", t.Oid(), t.YourRef())
            for leg in t.Instrument().Legs():
                for cf in leg.CashFlows():
                    if cf.PayDate() < pay_date_start or cf.PayDate() > pay_date_end :
                        continue

                    if cf.CashFlowType() == 'Total Return':
                        resets_v = []
                        for rs in cf.Resets():
                            reset_data.append(get_reset_row(rs, t, leg))
                            resets_v.append([rs.ResetType(), rs.Day(), rs.FixingValue()])
                        min_date, min_value, max_date, max_value = _reset_order(resets_v)
                        item = get_cf_row(cf, t, leg, "", min_date, min_value, max_date, max_value)
                        cf_data.append(item)
                    elif cf.CashFlowType() == 'Float Rate':
                        nominal_scale = 0
                        for rs in cf.Resets():
                            if rs.ResetType() == 'Single' or rs.ResetType() == 'Compound':
                                reset_data.append(get_reset_row(rs, t, leg))
                            if rs.ResetType() == 'Nominal Scaling':
                                reset_data.append(get_reset_row(rs, t, leg))
                                nominal_scale = rs.FixingValue()

                        item = get_cf_row(cf, t, leg, nominal_scale)
                        cf_data.append(item)
                    elif cf.CashFlowType() == 'Dividend' and leg.LegType() == 'Total Return':
                        und_ins = leg.IndexRef()
                        if und_ins.InsType() == 'Stock':
                            dividends = _get_dividends(und_ins, cf.StartDate(), True)
                        else:
                            dividends = _get_dividends(und_ins, cf.StartDate(), False)

                        for idxpt, ex_div_day, pay_date, dividend in dividends:
                            item = get_cf_row(cf, t, leg, ex_div_day=ex_div_day, pay_date=pay_date, dividend=dividend, idxpt=idxpt)
                            cf_data.append(item)


    attachements = []
    attachements.append(_work(config['cf_report_filename'], pay_date_start, pay_date_end, cf_data, CF_COLUMNS))
    attachements.append(_work(config['reset_report_filename'], pay_date_start, pay_date_end, reset_data, RESET_COLUMNS))

    if config["emails"]:
        portfolios_names = [p.Name() for p in portfolios]
        send_email(pay_date_start, pay_date_end, portfolios_names, config["emails"], attachements)

    print "completed successfully"
