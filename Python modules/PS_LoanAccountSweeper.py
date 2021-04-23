"""
Date                    : 2011-10-01
Purpose                 : Posts the val of the clients loan obligation to a loan account
Department and Desk     : Prime Service
Requester               : Andrew Nobbs
Developer               : Anwar

Date            CR              Developer               Change
==========      =========       ======================  ========================================================
2011-10-01      789213          Anwar Banoo             Initial Development
2011-12-05      849493          Anwar Banoo             Removed PRIME SERVICES DESK as an acquirer filter
2011-12-20      873238          Anwar Banoo             Make an ECR change to prevent processing of the sweep on holidays, also enhanced the logging
2012-06-18      265002          Anwar Banoo             Added new restricted port criteria to cater for multistrategy desks
2012-07-08      318884          Anwar Banoo             Changed the way we take portfolio input - we now take only top level and figure the rest dynamically
2013-01-24      750409          Peter Fabian            Added corpbond and nakedbond ff portfolios to restricted portfolios + do not post almost zero
2014-02-26     1760737          Peter Fabian            Added govibond ff portfolios to restricted portfolios (because last year I apparently forgot about them)
2014-04-10     1871367          Anwar Banoo             Amended code to look at fully funded add info on portfolio rather than naming convention to identify ff portfolios
2014-04-14     2119663          Hynek Urban             Split loan account sweeper among clients.
2015-09-11     3090331          Jakub Tomaga            Portfolio independent sweeping
2019-12-04     FAPE-144         Iryna Shcherbina        Introduce a constant for the minimum precision for rounding
"""


import string

import acm

from at_ael_variables import AelVariableHandler
from sweeping_report import LoanAccountSweepingReport as SweepingReport

from PS_FundingSweeper import CreateCashFlow, TradingManagerSweeper
from PS_FormUtils import DateField
from PS_Functions import (get_pb_fund_counterparties,
                          get_pb_reporting_portfolio,
                          get_pb_loan_account,
                          modify_asql_query,
                          SetAdditionalInfo,
                          get_pb_fund_shortname)

from at_logging import  getLogger, bp_start

LOGGER = getLogger()

TPL_COLUMNS = ['Portfolio Value End']
CALENDAR = acm.FCalendar['ZAR Johannesburg']
PRECISION_MIN = 6


def TimeSeriesSpec(fieldName, port):
    """ Return the time series spec or create one if it doesn't exist.
        New time series is linked to portfolio port by FieldName.
    """
    spec = acm.FTimeSeriesSpec[fieldName]
    if not spec:
        spec = acm.FTimeSeriesSpec()
        spec.Description('%s PnL History' % port)
        spec.FieldName(fieldName)
        spec.RecType(acm.EnumFromString('B92RecordType', 'Portfolio'))
        spec.Commit()
    return spec


def TimeSeries(date, cPort, spec):
    """ Return FTimeSeries object (i.e. an object containing
        value from a time series) for specified time series spec,
        date and portfolio.
    """
    return acm.FTimeSeries.Select01("day = '%s' and recaddr = %i "
        "and timeSeriesSpec = %i and runNo = 1"
        % (date, cPort.Oid(), spec.Oid()), '')


def GetLoanCashFlow(leg, runDate):
    """ Retrun loan cash flow for specifc date from specified leg.
        Loan cash flow is identified by PS_DepositType add info being
        equal to PB_Loan_Sweep.
    """
    query = acm.CreateFASQLQuery('FCashFlow', 'AND')
    query.AddAttrNode('Leg.Oid', 'EQUAL', leg.Oid())
    query.AddAttrNode('PayDate', 'EQUAL', runDate)
    query.AddAttrNode('AdditionalInfo.PS_DepositType', 'EQUAL', 'PB_Loan_Sweep')
    cashFlows = query.Select()
    if cashFlows:
        return cashFlows[0]
    return None


def ProcessPostings(counterparty, date):
    """ Save the total value of financed trades in all portfolios under cPort
        on runDate to time series for the cPort and post a difference
        between yesterday's and today's value to Loan Account
    """
    portfolio = get_pb_reporting_portfolio(counterparty)
    LOGGER.info('Process portfolio %s for %s', portfolio.Name(), date)
    LOGGER.info('------ Enter process postings ------')

    query_folder = acm.FStoredASQLQuery["Loan account sweeping"]
    query = modify_asql_query(
        query_folder.Query(),
        "Portfolio.Name",
        False,
        portfolio.Name())
    trades = query.Select()

    tot = 0
    trade_data = []
    for t in trades:
        tplDictionary = TradingManagerSweeper(t, date, TPL_COLUMNS)
        for instrument_name, tplValues in tplDictionary.items():
            tot += sum(tplValues)
            trade_record = (
                t.Oid(),
                t.Instrument().InsType(),
                instrument_name,
                t.Portfolio().Name(),
                sum(tplValues)
            )
            trade_data.append(trade_record)
            LOGGER.info('%s\t%s\t%s\t%f',
                         t.Oid(), t.Portfolio().Name(), instrument_name, sum(tplValues))

    fieldName = ('%s_PnL' % portfolio.Name())[0:19]

    # get the time series descriptor
    spec = TimeSeriesSpec(fieldName, portfolio.Name())

    # get the previous days' value otherwise post the whole amount
    # assuming that this is the first posting
    prevDay = CALENDAR.AdjustBankingDays(date, -1)
    prevSeries = TimeSeries(prevDay, portfolio, spec)
    if prevSeries:
        # Front Upgrade 2013.3 -- Value amended to TimeValue;
        # method name changed
        prevVal = prevSeries.TimeValue()
    else:
        prevVal = 0

    # get today's value to either create or update with val
    series = TimeSeries(date, portfolio, spec)
    if not series:
        series = acm.FTimeSeries()
        series.Recaddr(portfolio.Oid())
        series.TimeSeriesSpec(spec)
        series.Day(date)
        series.RunNo(1)
    # Front Upgrade 2013.3 -- Value amended to TimeValue; method name changed
    series.TimeValue(tot)
    series.Commit()

    postingVal = prevVal - tot

    LOGGER.info("Previous day %s\nToday %s\nPosting %s",
                prevVal, tot, postingVal)

    trade_data.append(("Previous day", "", "", "", prevVal))
    trade_data.append(("Today", "", "", "", tot))
    trade_data.append(("Posting", "", "", "", postingVal))

    if round(postingVal, PRECISION_MIN) != 0:
        loan_account = get_pb_loan_account(counterparty)
        if loan_account:
            if loan_account.Legs():
                leg = loan_account.Legs()[0]
                cashFlow = GetLoanCashFlow(leg, str(date))
                if not cashFlow:
                    cashFlow = CreateCashFlow(leg, 'Fixed Amount', None, None, date, postingVal)
                    SetAdditionalInfo(cashFlow, 'PS_DepositType', 'PB_Loan_Sweep')
                else:
                    cashFlow.FixedAmount(postingVal)
                    cashFlow.Commit()

    return trade_data
    LOGGER.info('------ Exit process postings ------')


ael_variables = AelVariableHandler()
ael_variables.add("counterparty",
                  label="Counterparty",
                  cls=acm.FCounterParty,
                  collection=get_pb_fund_counterparties())
ael_variables.add("sweep_date",
                  label="Sweep date",
                  default="Now")
ael_variables.add("sweepingReport",
                  label="Sweeping report",
                  alt="'Report with detailed breakdown of swept amounts'",
                  mandatory=False)


def ael_main(config):
    """Performs loan account sweeping for given counterparty and date."""

    process_name = "ps.loan_acc_sweeper.{0}".format(get_pb_fund_shortname(config['counterparty']))
    with bp_start(process_name):

        date = DateField.read_date(config["sweep_date"])
        if not CALENDAR.IsNonBankingDay(None, None, date):
            trade_data = ProcessPostings(config["counterparty"], date)
            report_filename = config["sweepingReport"]
            if report_filename:
                try:
                    fpath_template = string.Template(report_filename)
                    file_path = fpath_template.substitute(DATE=date.replace("-", ""))
                    sweeping_report = SweepingReport(file_path, trade_data)
                    sweeping_report.create_report()
                    LOGGER.info("Wrote secondary output to: %s", file_path)
                except Exception:
                    LOGGER.exception("Sweeping report wasn't generated.")
        else:
            LOGGER.info('Bypassing run on holiday')
        LOGGER.info("Completed Successfully")
