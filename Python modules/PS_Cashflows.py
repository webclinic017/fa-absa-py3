"""------------------------------------------------------------------------------
MODULE
    PS_Cashflows

DESCRIPTION
    Date                : 2012-10-01
    Purpose             : Creates a report with all the cashflows of the
                          instruments defined in the trade filter.
    Requester           : Danilo Mantoan
    Developer           : Nidheesh Sharma

HISTORY
=================================================================================
Date        CR Number   Developer               Description
---------------------------------------------------------------------------------
2012-10-01  556348         Nidheesh Sharma      Initial Implementation
2012-10-30  C620753        Nidheesh Sharma      Integration with
                                                PS_ReportController
2013-01-23  C748782        Nidheesh Sharma      Added try-except statements
                                                to avoid errors caused by
                                                python casting FDenominatedValue
                                                as integer
2014-03-21  C1866846       Hynek Urban          Bug fix (do not ignore
                                                non-initial trades) and
                                                major refactor.
2018-11-09  CHG1001149858  Qaqamba Ntshobane    Added date range for cashflows of
                                                each instrument defined in the
                                                trade.
ENDDESCRIPTION
------------------------------------------------------------------------------"""
import os
import csv
import acm
import at_time
import operator
import itertools
from datetime import datetime
from collections import defaultdict
from at_logging import getLogger, bp_start
from PS_Functions import get_pb_fund_shortname
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)

EPSILON = 1E-6  # Define almost zero.
STANDARD_CALC_SPACE = acm.FStandardCalculationsSpaceCollection()


def get_ael_variables():
    variables = AelVariableHandler()
    variables.add('trade_filters',
                  label='Trade Filter',
                  cls=acm.FTradeSelection,
                  collection=acm.FTradeSelection.Instances(),
                  alt='Trade filter that will be used to create report.'
                  )
    variables.add('trade_path',
                  label='File Path',
                  default='F:\\',
                  alt='Location of where the csv file will be created and the full file name.'
                  )
    variables.add('short_name',
                  label='Short Name',
                  alt='Name of the file to save the report in.'
                  )
    variables.add('cashflow_start_date',
                  label='From Date',
                  mandatory=False,
                  alt='How far back you want cashflows to be displayed'
                  )
    variables.add('cashflow_end_date',
                  label='To Date',
                  mandatory=False,
                  alt='How far in future you want cashflows to be displayed'
                  )
    return variables
ael_variables = get_ael_variables()


def _convertToParamDictionary(ReportControllerDictionary, reportName):
    """Convert a PS_ReportController dictionary to a local configuration."""
    return {
        'trade_filters': ReportControllerDictionary['tradeFilters_' + reportName][0],
        'trade_path': ''.join([
            ReportControllerDictionary['OutputPath'],
            ReportControllerDictionary['fileID_SoftBroker'],
            '_',
            ReportControllerDictionary['Filename_' + reportName],
            '.csv'
        ]),
        # Allow PS_ReportController2 to request addition of a date to the filename.
        # (Can be removed once PS_ReportController is made obsolete.)
        'add_date': ReportControllerDictionary.get('addDate_' + reportName, 'No'),
        'short_name': get_pb_fund_shortname(acm.FParty[ReportControllerDictionary["clientName"]]),
        'cashflow_start_date': ReportControllerDictionary["cashflow_start_date_" + reportName],
        'cashflow_end_date': ReportControllerDictionary["cashflow_end_date_" + reportName]
    }


def _get_number(denominated_value):
    """
    Extract number from the value.

    If not present, the original value is returned.

    """
    if hasattr(denominated_value, 'Number'):
        return denominated_value.Number()
    return denominated_value


def _get_callaccount_data(cashflow):
    """
    Extract the callaccount-specific data.

    These columns will be empty for most instruments.

    """
    deposit_type = cashflow.AdditionalInfo().PS_DepositType()
    ps_cash_type = cashflow.AdditionalInfo().PSCashType()
    cash_type_portfolio = ''

    if ps_cash_type and acm.FPortfolioSwap[ps_cash_type]:
        fund_portfolio = acm.FPortfolioSwap[ps_cash_type].FundPortfolio()
        if fund_portfolio:
            cash_type_portfolio = fund_portfolio.Name()
    ps_instrument_type = cashflow.AdditionalInfo().PS_InstrumentType()

    return deposit_type, ps_cash_type, cash_type_portfolio, ps_instrument_type


def _get_rows_for_instrument(instrument, trades, start_date, end_date):
    """Return an iterator over all rows for the given instrument."""
    outputReceiveLeg = []
    outputPayLeg = []

    if not end_date:
        end_date = acm.Time.AsDate(instrument.ExpiryDate())

    for leg in instrument.Legs():
        legCurrency = leg.Currency().Name()

        for cashflow in leg.CashFlows():
            # Only add to report cashflows that fall within the specified dates
            if cashflow.StartDate() == '' or cashflow.EndDate() == '' or\
              start_date <= cashflow.StartDate() and\
              end_date >= cashflow.EndDate():

                cashflow_calc = cashflow.Calculation()

                def _cash_calc(function_name, *args):
                    return getattr(cashflow_calc, function_name)(
                                    STANDARD_CALC_SPACE, *args)

                forwardRate = 0.0
                if _cash_calc('ForwardRate'):
                    forwardRate = round(_cash_calc('ForwardRate') * 100, 4)

                nominal, projected, PV = (sum(round(_get_number(_cash_calc(column, trade)), 2)
                                          for trade in trades)
                                          for column in ('Nominal', 'Projected', 'PresentValue')
                                          )
                (deposit_type, ps_cash_type,
                 cash_type_portfolio, ps_instrument_type) = _get_callaccount_data(cashflow)

                row = {
                      'Instrument': instrument.Name(),
                      'Cash Flow Number': cashflow.Oid(),
                      'Pay/Receive': 'Pay' if leg.PayLeg() else 'Receive',
                      'Action Type': cashflow.CashFlowType(),
                      'Currency': legCurrency,
                      'Start Date': cashflow.StartDate(),
                      'End Date': cashflow.EndDate(),
                      'Pay Date': cashflow.PayDate(),
                      'Forward Rate': forwardRate,
                      'Projected Cash': projected,
                      'Present Value': PV,
                      'Nominal': nominal,
                      'Deposit Type': deposit_type,
                      'PS_Descriptor': cashflow.AdditionalInfo().PS_Descriptor(),
                      'PSwap Cash Type': ps_cash_type,
                      'PSwap Cash Type Portfolio': cash_type_portfolio,
                      'PSwap Instrument Type': ps_instrument_type,
                      }

                if leg.PayLeg():
                    outputPayLeg.append(row)
                else:
                    outputReceiveLeg.append(row)

    return itertools.chain(
        sorted(outputReceiveLeg, key=operator.itemgetter('Pay Date')),
        sorted(outputPayLeg, key=operator.itemgetter('Pay Date'))
    )


def _get_relevant_instruments(trade_collection):
    """Return non-expired, non-terminated instruments with non-zero position."""
    context = acm.GetDefaultContext()
    sheet_type = 'FPortfolioSheet'  # Groups by instrument by default.
    calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)
    calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'PrevBusDay')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Now')
    calc_space.InsertItem(trade_collection)
    portfolio_iter = calc_space.RowTreeIterator().FirstChild()
    calc_space.Refresh()
    tree_proxy = portfolio_iter.Tree()

    instruments = set()

    # Iterate over all children, i.e. instruments.
    if tree_proxy.NumberOfChildren():
        instrument_node = tree_proxy.Iterator().FirstChild()

        while instrument_node:
            instrument_tree = instrument_node.Tree()
            instrument = instrument_tree.Item().Instrument()
            instrument_node = instrument_node.NextSibling()

            if (instrument.IsExpiredAt(acm.Time.DateToday()) or
                    instrument.IsTerminated()):
                continue
            position = _get_number(calc_space.CalculateValue(
                instrument_tree, 'Portfolio Position'))

            # Skip zero positions instruments.
            if position is None or abs(position) < EPSILON:
                continue
            instruments.add(instrument.Name())

    return instruments


def _exclude_unconfirmed_trades(tradefilter):
    """Return an ad hoc portfolio with simulated or void trades filtered out."""
    adhoc_prf = acm.FAdhocPortfolio()
    for trade in tradefilter.Trades():
        if trade.Status() not in ('Simulated', 'Void'):
            adhoc_prf.Add(trade)
    return adhoc_prf


def _get_banner(framework_version):
    """Create the banner in line with other CSV reports."""
    generated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    UTC_offset = (datetime.now() - datetime.utcnow()).seconds / 3600
    generated_time += ' (UTC+0%i:00)' % UTC_offset
    # The spaces below are in place in order to bring the banner format
    # in line with the version that comes from pb_csvtemplate.
    lines = (
        ('', ''),
        ('            Report Name:', 'File_CashInstrument'),
        ('            Generated Time:', generated_time),
        ('            Report Date:', acm.Time.DateToday()),
        ('            Version:', framework_version),
        ('', ''),
    )
    for part1, part2 in lines:
        row = defaultdict(str)
        row['Instrument'], row['Cash Flow Number'] = part1, part2
        yield row


def convert_date(start_date, end_date):
        """
        The following converts either the full date range or shorthand version (e.g. -3m)
        to an actual date that FA understands.

        """
        if not start_date:
            start_date = acm.Time.AsDate('1970-01-01')
        
        start_date = str(at_time.to_date(start_date))
        end_date = str(at_time.to_date(end_date))

        if end_date and start_date > end_date:
            raise ValueError('Check if "From Date" is not after "To Date"')
        return (start_date, end_date)


def ael_main(ael_dict):
    """Generate the CashFlows report."""
    process_name = "ps.cashflows.{0}".format(ael_dict["short_name"])
    with bp_start(process_name, ael_main_args=ael_dict):

        fieldnames = ['Instrument', 'Cash Flow Number', 'Pay/Receive',
                      'Action Type', 'Currency', 'Start Date', 'End Date',
                      'Pay Date', 'Forward Rate', 'Projected Cash',
                      'Present Value', 'Nominal', 'Deposit Type',
                      'PS_Descriptor', 'PSwap Cash Type',
                      'PSwap Cash Type Portfolio', 'PSwap Instrument Type']

        if ael_dict.get('add_date') == 'Yes':
            basename, extension = os.path.splitext(ael_dict['trade_path'])
            basename += '_' + acm.Time.DateToday().replace('-', '')
            filename = basename + extension
        else:
            filename = ael_dict['trade_path']

        cf_start_date, cf_end_date = convert_date(ael_dict['cashflow_start_date'],
                                                  ael_dict['cashflow_end_date'])

        with open(filename, 'wb') as fout:
            writer = csv.DictWriter(fout, delimiter=',', fieldnames=fieldnames)

            if ael_dict.get('frameworkVersion') is not None:
                for banner_row in _get_banner(ael_dict['frameworkVersion']):
                    writer.writerow(banner_row)
            # Despite the plural, there's only one tradefilter.
            tf = ael_dict['trade_filters']
            # Generally, the tradefilters contain simulated and void trades but
            # we don't want to include them.
            adhoc_prf = _exclude_unconfirmed_trades(tf)
            instruments_to_be_reported = _get_relevant_instruments(adhoc_prf)

            trades_sorted = adhoc_prf.Trades().SortByProperty('Instrument')
            writer.writerow(dict((fn, fn) for fn in fieldnames))

            for instrument, trades in itertools.groupby(trades_sorted,
               operator.methodcaller('Instrument')):

                if instrument.Name() not in instruments_to_be_reported:
                    continue
                if instrument.Legs():
                    writer.writerows(_get_rows_for_instrument(instrument,
                                     list(trades), cf_start_date, cf_end_date))

        LOGGER.info('Wrote secondary output to:%s', filename)
        LOGGER.info('Completed successfully')
