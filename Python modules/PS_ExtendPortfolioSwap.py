"""-----------------------------------------------------------------------------
Project: Prime Brokerage Project
Department: Prime Services
Requester: Francois Henrion
Developer: Paul Jacot-Guillarmod
CR Number: 666125 (Initial Deployment)

HISTORY
================================================================================
Date       Change no     Developer          Description
--------------------------------------------------------------------------------
2011-06-17 685737        Paul J.-Guillarmod Added a function call add TPL to the portfolio swap
2011-12-08 850928        Herman Hoon        Added the Provision function call
2012-05-08               Peter Kutnik       Fixed earlier undocumented change for non cash collateral
2014-11-20 2450799       Peter Fabian       Fixing errors and exception handling
2015-09-11 3090331       Jakub Tomaga       Portfolio independent sweeping
2018-11-12 CHG1001113453 Tibor Reiss        Enable fully funded CFD for MMIBETA2
2019-03-27 FAPE-65       Tibor Reiss        Remove fully funded CFD for MMIBETA2 (yes, you are reading it correctly)
2019-07-15 FAPE-47       Iryna Shcherbina   Create a sweeping report
2019-11-21 FAPE-147      Tibor Reiss        Propagate error
-----------------------------------------------------------------------------"""
import acm

from PS_Functions import (CALENDAR, TODAY, START_DATE_KEYS, START_DATE_LIST, END_DATE_KEYS, END_DATE_LIST, DateGenerator)
import PS_FundingSweeper
import PS_TimeSeriesFunctions
from at_logging import getLogger, bp_start
from sweeping_report import PSwapSweepingReport


LOGGER = getLogger()


def enable_custom_start_date(index, field_values):
    ael_variables[2][9] = (field_values[1] == 'Custom Date')
    return field_values


def enable_custom_end_date(index, field_values):
    ael_variables[4][9] = (field_values[3] == 'Custom Date')
    return field_values


# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [['portfolioSwaps', 'Portfolio Swaps', 'FInstrument', None, None, 1, 1, 'Portfolio swaps that will have their funding cashflows extended', None, 1],
                 ['startDate', 'Start Date', 'string', START_DATE_KEYS, 'Now', 1, 0, 'Date from which the portfolio swaps will be extended.', enable_custom_start_date, 1],
                 ['startDateCustom', 'Start Date Custom', 'string', None, TODAY, 0, 0, 'Custom from date', None, 0],
                 ['endDate', 'End Date', 'string', END_DATE_KEYS, 'Now', 1, 0, 'Date to which the portfolio swaps will be extended.', enable_custom_end_date, 1],
                 ['endDateCustom', 'End Date Custom', 'string', None, TODAY, 0, 0, 'Custom to date', None, 0],
                 ['compoundPortfolio', 'Compound Client Portfolio', 'FCompoundPortfolio', None, None, 0, 0, 'Fixed Income ValStart will be calculated for the compound portfolio to select the overnight funding spread.', None, 1],
                 ['collateralPortfolios', 'Compound Collateral Portfolio', 'FCompoundPortfolio', None, None, 0, 1, 'Compound portfolio where the Collateral trades are booked.', None, 1],
                 ['resweepTPL', 'Re-Sweep TPL', 'string', ['Yes', 'No'], 'No', 1, 0, 'When running backdated sweeping, indicate whether TPL should be reswept', None, 1],
                 ['clientName', 'Short name', 'string', None, 'CLIENT', 0, 0],
                 ['sweepingReport', 'Sweeping Report', 'string', None, None, 0, 0, 'Report with detailed breakdown of swept amounts', None, 1],
                ]


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    process_name = "ps.extend_pswap.{0}".format(ael_dict["clientName"])

    with bp_start(process_name):  
        if ael_dict['startDate'] == 'Custom Date':
            start_date = ael_dict['startDateCustom']
        else:
            start_date = START_DATE_LIST[ael_dict['startDate']]
        
        if ael_dict['endDate'] == 'Custom Date':
            end_date = ael_dict['endDateCustom']
        else:
            end_date = END_DATE_LIST[ael_dict['endDate']]
        
        resweep_tpl = ael_dict['resweepTPL'] == 'Yes'
        
        portfolio_swaps = ael_dict['portfolioSwaps']
        report_data = {}
        for portfolio_swap in portfolio_swaps:
            report_data[portfolio_swap.Name()] = ExtendPortfolioSwap(
                portfolio_swap, resweep_tpl, start_date, end_date)
    
        collateral_portfolios = ael_dict['collateralPortfolios']
        if portfolio_swaps:
            portfolio_swap = portfolio_swaps[0]
            portfolio = portfolio_swap.FundPortfolio()
            call_account = acm.FDeposit[portfolio.add_info('PSClientCallAcc')]
            if collateral_portfolios:
                collateral_portfolio = collateral_portfolios[0]
                for date in DateGenerator(start_date, end_date):
                    _SetCollateralTimeSeries(collateral_portfolio, date, call_account, 'Collateral Value')

        report_filename = ael_dict["sweepingReport"]
        if report_filename:
            try:
                file_path = report_filename.format(date=end_date.replace("-", ""))
                report = PSwapSweepingReport(file_path, report_data)
                report.create_report()
                LOGGER.info("Wrote secondary output to %s", file_path)
            except Exception:
                LOGGER.exception("Sweeping report wasn't generated.")

        if LOGGER.msg_tracker.errors_counter:
            raise RuntimeError("ERRORS occurred. Please check the log.")

        LOGGER.info("Completed Successfully")


def _SetCollateralTimeSeries(collateral_portfolio, date, call_account, column_name):
    time_series_dict = {'FI': 'PS_Collateral_FI',
                        'EQ': 'PS_Collateral_EQ',
                        'Cash': 'PS_Collateral_MM'
                       }
    collateral_type_grouper = acm.FAttributeGrouper('Instrument.CollateralType')
    query_folder = _GenerateValStartQuery(collateral_portfolio)
    collateral_dict = PS_FundingSweeper.TradingManagerSweeper(query_folder, date, [column_name], False,
                                                              collateral_type_grouper, 'ZAR')
    collateral_dict_keys = iter(collateral_dict.keys())

    if collateral_dict_keys:
        for key in collateral_dict_keys:
            time_series_name = time_series_dict[key]
            value = collateral_dict[key]
            if value:
                value = value[0]
                PS_TimeSeriesFunctions.UpdateTimeSeriesValue(time_series_name, call_account, value, date)
                LOGGER.info('Set time series %s, value %s for %s on %s to %s',
                            time_series_name, column_name, call_account.Name(), date, value)


def _GenerateValStartQuery(compound_portfolio):
    """Generate a query folder that will be used to calculate Overnight Spread ValStart for the compound portfolio."""
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Simulated'))
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))
    
    # Add the sub portfolios to the query
    or_node = query.AddOpNode('OR')
    if not compound_portfolio.AllPhysicalPortfolios():
        raise ValueError("Portfolio %s has no physical subportfolios" % compound_portfolio.Name())
    for portfolio in compound_portfolio.AllPhysicalPortfolios():
        or_node.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
    
    return query


def _CalculateOvernightSpreadValStart(query, date):
    """
    Calculate the total value of Overnight Spread ValStart for the previous banking day. This will be
    used to decide on the spread to be used in the overnight funding.
    """
    previous_banking_day = CALENDAR.AdjustBankingDays(date, -1)
    total_val_start = 0
    instrument_val_starts = PS_FundingSweeper.TradingManagerSweeper(query, previous_banking_day,
                                                                    ['Overnight Spread ValStart'], True)
    for ins, valStartList in instrument_val_starts.items():
        val_start = valStartList[0]
        total_val_start += val_start
    return total_val_start


def ExtendPortfolioSwap(portfolioSwap, resweepTPL, startDate, endDate):
    """Run all the modules needed to extend a portfolio swap for each date between startDate and endDate inclusive."""
    report_data = {}
    portfolio = portfolioSwap.FundPortfolio()
    for date in DateGenerator(startDate, endDate):
        PS_TimeSeriesFunctions.UpdateTimeSeries('PSExtExecPremRate', 'PSExtExecPremRate', portfolio, date)
        PS_TimeSeriesFunctions.UpdateTimeSeries('PSExtExecPremNonDMA', 'PSExtExecPremNonDMA', portfolio, date)
        PS_TimeSeriesFunctions.UpdateTimeSeries('PSShortPremRate', 'PSShortPremRate', portfolioSwap, date)
        funding = PS_FundingSweeper.GenerateFunding(portfolioSwap, date)
        provision = PS_FundingSweeper.GenerateProvision(portfolioSwap, date)

        # In general we don't want to overwrite the historical TPL resets, unless explicitly choosing to do so.
        tpl = {}
        if date == TODAY or resweepTPL:
            tpl = PS_FundingSweeper.GenerateTotalTPL(portfolioSwap, date)
        report_data[date] = (funding, provision, tpl)

    return report_data
