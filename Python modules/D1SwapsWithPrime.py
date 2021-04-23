"""
Extract equity swaps and their resets that delta one has done with Prime
synthetics from Barclays.

Project                : D1 File too Barcap
Department and Desk    : TCU
Requester              : Mahlangu, Sizwe
Developer              : Mistry, Bhavik
CR Number              : CHNG0002493263

------------------------------------------------------------------------------
HISTORY

===============================================================================
Date        Change no       Developer           Description
-------------------------------------------------------------------------------
2014-12-11  CHNG0002522552  Bhavik Mistry       Amended column order.           
2015-01-07                  Bhavik Mistry       Excluded terminated trades
2015-09-10                  Fancy Dire          Remove the use of Mentis Project Num
                                                and use the counterparty as a filter
                                                instead.
"""

import acm
from at_addInfo import get
from at_email import EmailHelper
import csv

# ========================== Functions ========================================


def write_file(name, data, access='wb'):
    """ Method to write report output to csv file

    Arguments:
        name -- the name of the file.
        data -- the data to write to file.
    """
    fileObj = open(name, access)
    csvWriter = csv.writer(fileObj,  dialect='excel-tab')
    csvWriter.writerows(data)
    fileObj.close()


def resetFwdRate(reset):
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

# ========================== Reporting class ==================================


class Report(object):
    def __init__(self, data):
        self.portfolios = data['Portfolios']
        self.path = data['OutPath']
        self.email = data['Email']
        # Output file names
        self.tradeFileName = self.path + '/D1SwapsWithPrime.xls'
        self.resetFileName = self.path + '/D1SwapsWithPrime_Resets.xls'

        # Headers for trade file
        self.tradeData = [[
            'Portfolio',
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
            'Instrument ID']]

        # Headers for reset file
        self.resetData = [[
            'Trade No.', 'Date', 'Type', 'Value', 'Estimate', 'Pay Day', 'Float Rate']]

# ========================== Main =============================================


# AEL Variables :
# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory,
# Multiple, Description, Input Hook, Enabled

ael_variables = []
ael_variables.append(['OutPath', 'Output Path: ', 'string', None, 'F:\\\\', 1])
ael_variables.append(['Email', 'Email: ', 'string', None, None, 1, 1,
                      'Email parameter', None, 1])
ael_variables.append(['Portfolios', 'Portfolios: ', 'FPhysicalPortfolio',
                      acm.FPhysicalPortfolio.Instances(), None, 1, 1,
                      'Portfolio parameter', None, 1])


def ael_main(data):

    report = Report(data)

    for p in report.portfolios:
        # Get trades in portfolio where trade status is not Simulated or void,
        # and the instrument has not expired
        # and the instrument type is TotalReturnSwap
        # and Counterparty is 'BARCLAYS CAPITAL SECURITIES LTD'.
        trades = p.Trades()
        for t in trades:
            if (t.Status() not in ('Void', 'Simulated', 'Terminated') and
                t.CounterpartyId() == 'BARCLAYS CAPITAL SECURITIES LTD'):

                ins = t.Instrument()
                if (ins.InsType() == 'TotalReturnSwap' and
                   ins.IsExpired() is False):

                    for leg in ins.Legs():

                        if leg.LegType() == 'Float':
                            initial_price = leg.InitialIndexValue()
                            nominal = leg.InitialIndexValue()*t.Quantity()
                            start_date = leg.StartDate()
                            maturity_date = leg.EndDate()
                            spread = leg.Spread()
                            day_count = leg.DayCountMethod()
                            underlying = ('None' if leg.IndexRef() is None
                                          else leg.IndexRef().Name())
                            interest_reset_gap = leg.ResetDayOffset()
                            float_rate = leg.FloatRateReference().Name()
                            float_conv = leg.PayDayMethod()
                            float_rolling_period = leg.RollingPeriodUnit()
                            float_rolling_num = leg.RollingPeriodCount()

                            # Get resets of float legs,
                            # where type of reset is single.
                            for r in leg.Resets():
                                if r.ResetType() == 'Single':
                                    # Add data to the reset output
                                    report.resetData.append([
                                        t.Oid(),
                                        r.Day(),
                                        r.ResetType(),
                                        r.FixingValue(),
                                        resetFwdRate(r),
                                        r.CashFlow().PayDate(),
                                        float_rate])

                        if leg.LegType() == 'Total Return':
                            equity_conv = leg.PayDayMethod()
                            equity_rolling_period = leg.RollingPeriodUnit()
                            equity_rolling_num = leg.RollingPeriodCount()

                    tradeFields = [
                        p.Name(),
                        t.CounterpartyId(),
                        underlying,
                        t.Quantity(),
                        initial_price,
                        spread,
                        'Short' if t.Quantity() > 0 else 'Long',
                        t.ExecutionDate(),
                        maturity_date,
                        nominal,
                        t.Oid(),
                        start_date,
                        float_rolling_period,
                        ins.Currency().Name(),
                        equity_rolling_period,
                        float_conv,
                        equity_conv,
                        float_rolling_num,
                        equity_rolling_num,
                        interest_reset_gap,
                        t.Status(),
                        day_count,
                        ins.DividendFactor(),
                        ins.Name()]

                    # Add data to the trade output
                    report.tradeData.append(tradeFields)

    # Write script output to file
    try:
        write_file(report.tradeFileName, report.tradeData)
        print('Wrote secondary output to:', report.tradeFileName)
        write_file(report.resetFileName, report.resetData)
        print('Wrote secondary output to:', report.resetFileName)

        print('Reports completed successfully.')
    except IOError:
        print('Error writing output to files')

    # Email reports
    print(type(report.email))
    mail_to = list(report.email)
    subject = "D1SwapsWithPrime Reports"
    body = "Delta one swaps with prime synthetics"
    email_from = "Prime Client"
    attachments = [report.tradeFileName, report.resetFileName]

    emailHelper = EmailHelper(body, subject, mail_to, email_from, attachments)

    # Use outlook to send email from front end
    # Use SMTP to send email from back end
    if str(acm.Class()) == "FACMServer":
        emailHelper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        emailHelper.host = EmailHelper.get_acm_host()

    print(EmailHelper.get_acm_host())
    print(acm.Class())

    try:
        emailHelper.send()
    except Exception as e:
        print(("!!! Exception: {0}\n".format(e)))
