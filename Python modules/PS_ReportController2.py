"""-----------------------------------------------------------------------------
PROJECT                 :  Prime Services
PURPOSE                 :  Create PDF reports and Softbroker Descriptor
DEPATMENT AND DESK      :  Prime Services
REQUESTER               :
DEVELOPER               :  Rohan van der Walt
CR NUMBER               :  713436
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no       Developer            Description
--------------------------------------------------------------------------------
2011-07-13  713436         Rohan vd Walt        Initial Implementation
2011-07-27  724933         Rohan vd Walt        Change report filenames to be
                                                client specific and only remove
                                                client specific fo files.
2011-08-03  750738         Rohan vd Walt        Change structure to support
                                                use template workbook,
                                                and rather insert Trade Filters,
                                                makes column changes/maintanence
2011-08-19  750738         Rohan vd Walt        Misc changes +
                                                Warehousing Report
2011-09-02  759616         Rohan vd Walt        Add NAV report
2011-09-07  762168         Herman Hoon          Added the Bencmark
                                                Delta Risk report
2011-09-13  768482         Rohan vd Walt        Ability to define preprocessors
                                                per FWorksheetReport and shows
                                                expired trades as well
2011-11-23  837929         Herman Hoon          Option to produce CSV output
                                                for reports as well. Added
                                                the Benchmark Delta reports.
2012-10-30  620753         Nidheesh Sharma      Added portfolio parameter and
                                                added PS_FinanceAndFeeReport
                                                and PS_Cashflows.
2012-10-30  620753         Hynek Urban          Descriptor generation refactor.
2013-03-08  857456         Peter Basista        Remove _getCallAccounts
                                                function and use the one
                                                from the PS_Functions module
                                                (getCallAccounts function).
2013-03-19  885480         Peter Basista        Split the static data
                                                and core functionality
                                                previously present in
                                                PS_ReportController into
                                                two modules --- this file
                                                (PS_ReportController) and
                                                PS_ReportControllerFunctions.
2013-06-18  1106832        Hynek Urban          Add curve publication.
2013-06-21  1113508        Hynek Urban          Add the Cash analysis report,
                                                enable CSV output for selected
                                                reports.
2014-01-13  1712088        Hynek Urban          Get rid of REPORT_DESCRIPTIONS,
                                                use ReportDescription classes.
2018-11-09  CHG1001149858  Qaqamba Ntshobane    Added date range for cashflows of
                                                each instrument defined in the
                                                trade.

"""

import acm
from PS_Functions import get_pb_fund_shortname
from at_logging import  getLogger, bp_start
from PS_ReportControllerFunctions2 import (ReportDescription as RD,
    CustomReportDescription as CRD, add_report_tabs, add_custom_report_tabs,
    generate_reports)

LOGGER = getLogger()


# The functions used as callbacks for custom reports
def _add_nav_report(ael_variables, report_name, file_name, report_title,
        eq_trade_filter, fi_trade_filter, cash_trade_filter):

    """Add the NAV report parameters to ael_variables."""
    ael_variables.append([report_name, report_name, 'string',
        ['No', 'Yes'], 'No', 1, 0, 'Generate this report?', None, 1])
    ael_variables.append(['reportTitle_' + report_name,
        'Report Title_' + report_name, 'string', None, report_title,
        0, 0, 'PreProcessor Parameter', None, 1])
    ael_variables.append(['Filename_' + report_name,
        'Filename_' + report_name, 'string', None, file_name,
        0, 0, 'Filename', None, 1])
    ael_variables.append(['eqTradeFilter_' + report_name,
        'Equity Trade Filter_' + report_name, acm.FTradeSelection,
        acm.FTradeSelection.Instances(), eq_trade_filter,
        0, 0, 'This TF specifies positions that will be included '
        'in the Equity section of the report', None, 1])
    ael_variables.append(['fiTradeFilter_' + report_name,
        'Fixed Income Trade Filter_' + report_name, acm.FTradeSelection,
        acm.FTradeSelection.Instances(), fi_trade_filter, 0, 0,
        'This TF specifies positions that will be included '
        'in the Fixed Income section of the report', None, 1])
    ael_variables.append(['cashTradeFilter_' + report_name,
        'Cash Trade Filter_' + report_name, acm.FTradeSelection,
        acm.FTradeSelection.Instances(), cash_trade_filter, 0, 0,
        'This TF specifies positions that will be included '
        'in the Cash section of the report', None, 1])


def _add_reset_risk_report(ael_variables, report_name, file_name,
        input_type, portfolio, trade_filter, report_type,
        output_type, currency, curve):
    """Add the reset risk report parameters to ael_variables."""
    ael_variables.append([report_name, report_name, 'string',
        ['No', 'Yes'], 'No', 1, 0, 'Generate this report?', None, 1])
    ael_variables.append(['Filename_' + report_name,
        'Filename_' + report_name, 'string', None, file_name,
        0, 0, 'Filename', None, 1])
    ael_variables.append(['InputType_' + report_name,
        'Report Input Type_' + report_name, 'string',
        ['Filter', 'Portfolio'], input_type, 1])
    ael_variables.append(['Portfolio_' + report_name,
        'Portfolio_' + report_name, 'FPhysicalPortfolio',
        None, portfolio, 0, 1, 'Name of Portfolio'])
    ael_variables.append(['TrdFilter_' + report_name,
        'Trade Filter_' + report_name, 'FTradeSelection',
        None, trade_filter, 0, 1, 'Name of Trade Filter'])
    ael_variables.append(['ReportType_' + report_name,
        'Report Type_' + report_name, 'string', ['Reset Risk',
        'Provision Per Reset Bucket', 'Provision Per Reset'], report_type])
    ael_variables.append(['OutputType_' + report_name,
        'Output Type_' + report_name, 'string', ['Excel', 'CSV'], output_type])
    ael_variables.append(['Currency_' + report_name,
        'Currency_' + report_name, 'FCurrency', None, currency,
        0, 1, 'Currency'])
    ael_variables.append(['Curve_' + report_name,
        'Yield Curve_' + report_name, 'FYieldCurve', None, curve,
        0, 1, 'Yield Curve'])


def _add_curve_publish_report(ael_variables, report_name, file_name,
        yield_curve):
    """Add the yieldcurve publication report parameters to ael_variables."""
    ael_variables.append([report_name, report_name, 'string', ['No', 'Yes'],
        'No', 1, 0, 'Generate this report?', None, 1])
    ael_variables.append(['Filename_' + report_name, 'Filename_' + report_name,
        'string', None, file_name, 0, 0, 'Filename', None, 1])
    ael_variables.append(['yieldCurve_' + report_name,
        'Yield Curve_' + report_name, acm.FYieldCurve,
        acm.FYieldCurve.Select(''), yield_curve, 0, 0,
        'A curve publication report will be generated for this yieldcurve.',
        None, 1])


def _add_cashflows_report(ael_variables, report_name, file_name, trade_filters):
    ael_variables.append([report_name, report_name, 'string',
        ['No', 'Yes'], 'No', 1, 0, 'Generate this report?', None, 1])
    ael_variables.append(['Filename_' + report_name,
        'Filename_' + report_name, 'string', None, file_name,
        0, 0, 'Filename', None, 1])
    ael_variables.append(['tradeFilters_' + report_name,
        'Trade Filter_' + report_name, acm.FTradeSelection,
        acm.FTradeSelection.Instances(), trade_filters,
        0, 1, 'Trade Filters to add to report.', None, 1])
    ael_variables.append(['addDate_' + report_name,
        'Add date to filename_' + report_name, 'string',
        ['Yes', 'No'], 'Yes',
        1, 0, 'Add date to the file name.', None, 1])
    ael_variables.append(['frameworkVersion_' + report_name,
        'Framework Version_' + report_name, 'string', None, 'ReportController2',
        0, 0, 'String that identifies the framework used to generate the report;'
        ' it will be shown in the report banner.', None, 1])
    ael_variables.append(['cashflow_start_date_' + report_name,
        'From Date_' + report_name, 'string', None, None, 0, 0,
        'How far back you want cashflows to be displayed', None, 1])
    ael_variables.append(['cashflow_end_date_' + report_name,
        'To Date_' + report_name, 'string', None, None, 0, 0,
        'How far in future you want cashflows to be displayed', None, 1])


def _add_riskSwapAttribution_report(ael_variables, report_name, file_name):
    """Add the risk report parameters to ael_variables."""
    ael_variables.append([report_name, report_name, 'string', ['No', 'Yes'], 'No', 0, 0, 'Generate this report?', None, 1])
    ael_variables.append(['reportTitle_' + report_name, 'Report Title_' + report_name, 'string', None, 'Risk Swap Attribution', 0, 0, 'PreProcessor Parameter', None, 1])    
    ael_variables.append(['TrdFilter_' + report_name, 'Trade Filter_' + report_name, 'FTradeSelection', acm.FTradeSelection.Instances(), None, 0, 0, 'Name of Trade Filter\nUsed in both ShortEndDelta and BenchmarkDelta reports'])
    ael_variables.append(['Currency_' + report_name, 'Currency_' + report_name, 'FCurrency', acm.FCurrency.Instances(), 'ZAR', 0, 0, 'Currency'])
    ael_variables.append(['Curve_' + report_name, 'Yield Curve_' + report_name, 'FYieldCurve', acm.FYieldCurve.Instances(), 'ZAR-SWAP', 0, 0, 'Yield Curve'])  
    ael_variables.append(['Filename_' + report_name, 'Filename_' + report_name, 'string', None, 'File_RiskSwapAttribution', 0, 0, 'Filename', None, 1])


def _add_riskBondAttribution_report(ael_variables, report_name, file_name):
    """Add the risk report parameters to ael_variables."""
    ael_variables.append([report_name, report_name, 'string', ['No', 'Yes'], 'No', 0, 0, 'Generate this report?', None, 1])
    ael_variables.append(['reportTitle_' + report_name, 'Report Title_' + report_name, 'string', None, 'Risk Bond Attribution', 0, 0, 'PreProcessor Parameter', None, 1])    
    ael_variables.append(['TrdFilter_' + report_name, 'Trade Filter_' + report_name, 'FTradeSelection', acm.FTradeSelection.Instances(), None, 0, 0, 'Name of Trade Filter\nUsed in BenchmarkDelta report'])
    ael_variables.append(['CollectionTrdFilter_' + report_name, 'Bond Collection Trade Filter_' + report_name, 'FTradeSelection', acm.FTradeSelection.Instances(), acm.FTradeSelection['PS_BondCollectionRiskAttr'], 0, 0, 'Name of Trade Filter\nUsed to select all bonds traded to build risk factor list'])
    ael_variables.append(['Curve_' + report_name, 'Yield Curve_' + report_name, 'FYieldCurve', acm.FYieldCurve.Instances(), 'ZAR-BOND-PRIME', 0, 0, 'Yield Curve'])  
    ael_variables.append(['Filename_' + report_name, 'Filename_' + report_name, 'string', None, 'File_RiskBondAttribution', 0, 0, 'Filename', None, 1])


def _add_resetRisk_report(ael_variables, report_name, file_name):
    """Add the risk report parameters to ael_variables."""
    ael_variables.append([report_name, report_name, 'string', ['No', 'Yes'], 'No', 0, 0, 'Generate this report?', None, 1])
    ael_variables.append(['TrdFilter_' + report_name, 'Trade Filter_' + report_name, 'FTradeSelection', acm.FTradeSelection.Instances(), None, 0, 0, 'Name of Trade Filter\nUsed in Reset Risk report'])
    ael_variables.append(['Currency_' + report_name, 'Currency_' + report_name, 'FCurrency', acm.FCurrency.Instances(), 'ZAR', 0, 0, 'Currency'])
    ael_variables.append(['Filename_' + report_name, 'Filename_' + report_name, 'string', None, 'File_RiskResetDates', 0, 0, 'Filename', None, 1])
    ael_variables.append(['Curve_' + report_name, 'Yield Curve_' + report_name, 'FYieldCurve', acm.FYieldCurve.Instances(), 'ZAR-SWAP', 0, 0, 'Yield Curve'])  
    

# List of regular reports.
REPORTS = [
    RD(
        name='Heavy Trade',
        filename='File_TradeRoll',
        key_prefix='PS2_HTR',
    ),
    RD(
        name='Light Trade',
        filename='Report_TradeActivity',
        key_prefix='PS2_LTR',
    ),
    RD(
        name='Heavy Position',
        filename='File_PositionPNL',
        key_prefix='PS2_HPOS',
    ),
    RD(
        name='Light Position',
        filename='Report_Position',
        key_prefix='PS2_LPOS',
    ),
    RD(
        name='Heavy Instrument Position',
        filename='File_PositionInstrument',
        key_prefix='PS2_HIPOS',
    ),
    RD(
        name='Heavy Corporate Actions',
        filename='File_CorporateActions',
        key_prefix='PS2_HCORP',
    ),
    RD(
        name='Light Corporate Actions',
        filename='Report_CorporateActions',
        key_prefix='PS2_LCORP',
    ),
    RD(
        name='Heavy Financing',
        filename='File_Financing',
        key_prefix='PS2_HFIN',
    ),
    RD(
        name='Light Financing',
        filename='Report_Financing',
        key_prefix='PS2_LFIN',
    ),
    RD(
        name='Light Performance',
        filename='Report_Performance',
        key_prefix='PS2_LPERF',
    ),
    RD(
        name='Heavy Collateral Trades',
        filename='File_CollateralTrades',
        key_prefix='PS2_HCOLT',
    ),
    RD(
        name='Heavy Collateral Positions',
        filename='File_CollateralPositions',
        key_prefix='PS2_HCOLP',
    ),
    RD(
        name='Light Collateral Positions',
        filename='Report_CollateralPositions',
        key_prefix='PS2_LCOLP',
    ),
    RD(
        name='Heavy Risk FX',
        filename='File_RiskFX',
        key_prefix='PS2_HRFX',
    ),
    RD(
        name='Heavy Cash',
        filename='File_CashAnalysis',
        key_prefix='PS2_HCASH',
    ),
    RD(
        name='Heavy Valuations',
        filename='File_Valuations',
        key_prefix='PS2_VHR',
    ),
    RD(
        name='Heavy Risk Yield Delta',
        filename='File_RiskYieldDelta',
        key_prefix='PS2_HRYDR',
    ),
]

CUSTOM_REPORTS = [
    CRD(
        name='Light Valuations',
        filename='Report_Valuations',
        key_prefix='PS2_VLR',
        module='PS_NAV_Report2',
        callback=_add_nav_report,
        callback_params={
            'report_title': 'Valuations Report',
            'eq_trade_filter': 'PB_TEST_NAV_Equity',
            'fi_trade_filter': 'PB_TEST_NAV_FI',
            'cash_trade_filter': 'PB_TEST_NAV_Cash',
        }
    ),
    CRD(
        name='Heavy Cashflows',
        filename='File_CashInstrument',
        key_prefix='PS2_CSH',
        module='PS_Cashflows',
        callback=_add_cashflows_report,
        callback_params={'trade_filters': None},
    ),
    CRD(
        name='Heavy Risk Swap Attribution Report',
        filename='File_RiskSwapAttribution',
        key_prefix='PS2_RSKSWAP',
        module='PS_RiskSwapAttribution_Report',
        callback=_add_riskSwapAttribution_report,
        callback_params={},
    ),
    CRD(
        name='Heavy Risk Bond Attribution Report',
        filename='File_RiskBondAttribution',
        key_prefix='PS2_RSKBOND',
        module='PS_RiskBondAttribution_Report',
        callback=_add_riskBondAttribution_report,
        callback_params={},
    ),
    CRD(
        name='Heavy Risk Report - Reset Dates',
        filename='File_RiskResetDates',
        key_prefix='PS2_RESETRSK',
        module='PS_ResetRisk_Report',
        callback=_add_resetRisk_report,
        callback_params={},
    ),
]

ael_variables = []

add_report_tabs(ael_variables, REPORTS)
add_custom_report_tabs(ael_variables, CUSTOM_REPORTS)


def ael_main(configuration):
    """Simply call the function which does the report generation itself."""
    client = acm.FParty[configuration["clientName"]]
    process_name = "ps.reporting.{0}".format(get_pb_fund_shortname(client))

    with bp_start(process_name):
        generate_reports(configuration, REPORTS, CUSTOM_REPORTS)
        LOGGER.info("Completed Successfully")
