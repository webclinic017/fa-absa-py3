"""-----------------------------------------------------------------------------
PROJECT                 :  Prime Services
PURPOSE                 :  This module can be ran standalone to generate XML, FO
                           and PDF to be used for Prime Brokerage reports.
                           Will be ran from PS_ReportController2 by passing
                           through parameter dictionary to ael_main.
DEPATMENT AND DESK      :  Prime Services
REQUESTER               :  
DEVELOPER               :  Rohan van der Walt
CR NUMBER               :  759616
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer          Description
--------------------------------------------------------------------------------
2011-07-13  759616         Rohan vd Walt      Initial implementation
2012-02-08  889960         Rohan van der Walt Integration with new Prime Portal
2012-06-20  ??????         Anwar Banoo        Added support for RTB scripts by adding the line "Wrote secondary output"
2014-06-05  2018619        Hynek Urban        Handling errors in PB overnight batch correctly
2014-06-05  ??????         Hynek Urban        Split Exposure and NAV into two pages, use different NAV columns,
                                              use at_calculation_space where appropriate.
2014-10-16  2371269        Rohan van der Walt Adding portfolio parameters to XML representation of report
2018-11-26  ABITFA-5607    Tibor Reiss        Changes for special MMIBETA2 reports (requested by business)
2019-03-27  FAPE-65        Tibor Reiss        Revert back changes for MMIBETA2 (requested by business)
2019-11-28  FAPE-155       Tibor Reiss        Replace acm formatters with standard python so that back end diff works
-----------------------------------------------------------------------------"""
import math
import os
import pprint
from xml.etree import ElementTree
from datetime import datetime
from collections import OrderedDict

import acm

import FReportAPI
import PS_XMLReportingTools
from PS_FormUtils import DateField
from PS_Functions import get_pb_fund_shortname
from at_calculation_space import CalculationSpace
from at_logging import getLogger, bp_start


LOGGER = getLogger()
TODAY = acm.Time.DateToday()


def get_root_cr_portfolio(trade):
    cnt = 0
    prf = trade.Portfolio()
    prf1 = prf
    while prf is not None and prf.Name() != 'PB_CR_LIVE':
        cnt += 1
        links = acm.FPortfolioLink.Select('memberPortfolio = %s' % prf.Name())
        if len(links):
            prf1 = prf
            prf = links[0].OwnerPortfolio()
        else:
            break
        if cnt > 50:
            break
    return prf1
    

def get_ex_coupon_value(bond, trades_in_position):
    """
    Get the ex but not yet paid coupon value, if any.
    
    <bond> can be a Bond, Index Linked Bond or FRN.

    """
    # (This method is used by the exCouponValue FExtensionAttribute.)
    
    if bond.InsType() not in ('Bond', 'FRN', 'IndexLinkedBond'):
        return 0.0  # Not really a bond.

    tag = acm.CreateEBTag()  # Whatever.
    total = 0.0

    cashflows = []  # Find the cashflow(s) that have gone ex but aren't paid yet.
    for cf in bond.Legs()[0].CashFlows():
        is_ex = acm.Time.DateDifference(TODAY, cf.ExCouponDate()) >= 0
        not_yet_paid = acm.Time.DateDifference(TODAY, cf.PayDate()) < 0
        if is_ex and not_yet_paid:
            cashflows.append(cf)

    for cf in cashflows:  # Typically, len(cashflows) == 1
        position_on_cf_ex_date = sum(
            trade.Quantity() for trade in trades_in_position.AsList()
            if trade.Status() not in ('Simulated', 'Void')
                and acm.Time.DateDifference(trade.AcquireDay(), cf.ExCouponDate()) < 0
        )
        proj_value = acm.GetCalculatedValueFromString(cf, 'Standard', 'projectedCashFlow', tag).Value().Number()
        total += proj_value * position_on_cf_ex_date

    return total


class ReportXML(object):
    def __init__(self):
        self.root = ElementTree.XML('<PRIMEReport></PRIMEReport>')
        self.count = 0

    @staticmethod
    def _is_empty_section(dict_, section):
        for col in list(dict_.keys()):
            if dict_[col].get(section, {}).get('Total', 0) != 0:
                return False
        return True

    def add_report(self, dict_):
        row_label_mapping = {"Deposit": "Call Account"}
        report_element = ElementTree.SubElement(self.root, 'ReportDetail')
        sections = set(sum([list(dict_[column].keys()) for column in dict_], []))
        for section in sections:
            # Don't populate section in xml if section total is 0.
            if section not in ['Leverage', 'Total', 'NAV']:
                if self._is_empty_section(dict_, section):
                    continue
            section_element = ElementTree.SubElement(report_element, 'ReportSection', attrib={'Name': section})
            rows = []
            for column in dict_:
                for row_label in list(dict_[column].get(section, {}).keys()):
                    # Sometimes dict_[column][section] is an OrderedDict
                    # so we make effort to preserve the order of rows.
                    if row_label not in rows:
                        rows.append(row_label)
            for row in rows:
                if row not in row_label_mapping or section != 'Cash':
                    label = row
                else:
                    label = row_label_mapping[row]
                row_element = ElementTree.SubElement(section_element, 'ReportRow', attrib={'Label': label})
                for column in dict_:
                    if section not in dict_[column] or row not in dict_[column][section]:
                        continue
                    if section == 'Leverage':
                        val = '{:,.2f}'.format(dict_[column][section][row])
                    else:
                        val = '{:,.0f}'.format(dict_[column][section][row])
                    if val == 'NaN' or (isinstance(val, float) and math.isnan(val)):
                        ElementTree.SubElement(row_element, column).text = dict_[column][section][row]
                    else:
                        ElementTree.SubElement(row_element, column).text = val

    def __str__(self):
        return ElementTree.tostring(self.root)
        

def get_values_by_ins_type(column_id, trade_filter, limit_by_financed=None):
    """Get column value by ins type."""
    grouper = acm.FStoredPortfolioGrouper.Select01(
            'name=Fin - InsType', None).Grouper()
    calc_space = CalculationSpace.from_source(trade_filter, grouper=grouper)
    result = {}
    for financed, ins_types in calc_space.items():
        if limit_by_financed and limit_by_financed != financed:
            continue
        for ins_type, cell in ins_types.items():
            # Cannot use cell.column_value because FormattedValue is hard to parse.
            value = cell.calc_space.CalculateValue(cell.node.Tree(), column_id)
            if hasattr(value, 'Number'):
                value = value.Number()
            result[ins_type] = result.get(ins_type, 0) + value
    return result


class NAVReport(object):
    def __init__(self):
        layout = (  # (section, columns)
            ('Equity', ('GrossExposure', 'NetExposure')),
            ('FixedIncome', ('GrossExposure', 'NetExposure')),
            ('Cash', ('GrossExposure', 'NetExposure')),
            ('Total', ('GrossExposure', 'NetExposure')),
            ('Leverage', ('FairValueNAV', 'AccruedValueNAV')),
            ('NAV', ('FairValueNAV', 'AccruedValueNAV')),
            ('FullyFundedBreakDownInsTypes', ('FairValueNAV', 'AccruedValueNAV')),
            ('FullyFundedBreakDownComponents', ('FairValueNAV', 'AccruedValueNAV')),
        )
        self._equity_tf = None
        self._fixed_income_tf = None
        self._values = {}
        for section, columns in layout:
            for column in columns:
                if column not in self._values:
                    self._values[column] = {}
                self._values[column][section] = {'Total': 0}

    def _remove_zero_rows(self, section):
        """Remove rows where all columns are zero from the given section."""
        # First, establish all the rows in the section.
        rows = {}
        for column in self._values:
            if section in self._values[column]:
                for row in self._values[column][section]:
                    rows[row] = rows.get(row, False) or (
                            self._values[column][section][row] != 0)

        # Now delete the rows where all columns are zero.
        for row, is_non_zero in rows.items():
            if not is_non_zero and row != 'Total':
                for column in self._values:
                    if section in self._values[column] and row in self._values[
                            column][section]:
                        del self._values[column][section][row]

    def _populate_section_by_ins_types(self, trade_filter, section_name):
        """Populate a section with per ins_type NAV exposure data."""
        column_mapping = {
            'NetExposure': 'PS NAV Net Exposure',
            'GrossExposure': 'PS NAV Gross Exposure',
        }
        for report_column, fa_column in column_mapping.items():
            exposures = get_values_by_ins_type(fa_column, trade_filter)
            for ins_type, exposure in exposures.items():
                self._values[report_column][section_name][ins_type] = exposure
       
    def populate_equity_section(self, equity_tf):
        self._equity_tf = equity_tf
        self._populate_section_by_ins_types(equity_tf, 'Equity')
        self._remove_zero_rows('Equity')

    def populate_fi_section(self, fixed_income_tf):
        """Populate the Fixed Income section with data."""
        self._fixed_income_tf = fixed_income_tf
        self._populate_section_by_ins_types(fixed_income_tf, 'FixedIncome')
        self._remove_zero_rows('FixedIncome')

    def populate_cash_section(self, cash_tf):
        """Populate the Cash section with data."""
        self._populate_section_by_ins_types(cash_tf, 'Cash')

    def update_totals(self):
        for col in self._values:
            col_total = 0
            for sec in self._values[col]:
                temp_total = 0
                for subSec in self._values[col][sec]:
                    if subSec != 'Total':
                        try:
                            temp_total += self._values[col][sec][subSec]
                        except KeyError:
                            pass  # empty trade filter, skip
                    self._values[col][sec]['Total'] = temp_total
                col_total += temp_total
            if 'Total' in self._values[col]:
                self._values[col]['Total']['Total'] = col_total

    def populate_leverage(self):
        """
        Populate the Leverage section with data.

        To be called after populateNav and updateTotals were called.
        """
        gross_exposure = self._values['GrossExposure']['Total']['Total']
        for column in ('FairValueNAV', 'AccruedValueNAV'):
            try:
                leverage = gross_exposure / self._values[column]['NAV']['Total']
            except ZeroDivisionError:
                leverage = 0
            self._values[column]['Leverage']['Total'] = leverage

    def populate_nav(self, cash_tf, equity_section_tf, fixed_income_tf):
        """Populate the NAV section with data."""
        ins_type_grouper = acm.Risk().GetGrouperFromName('Instrument Type')
        fin_ins_type_grouper = acm.FStoredPortfolioGrouper.Select01(
            'name=Fin - InsType', None).Grouper()
        # {row_code: (trade_filter, grouper, key sequence, {report_column: (fa_column)})}
        ps_fair_nav_column = 'PS Fair Value NAV'
        ps_accrued_nav_column = 'PS Accrued Value NAV'
        row_specs = {
            'closing_balance': (cash_tf, ins_type_grouper, (('Deposit',),), {
                'FairValueNAV': 'PS Fair Value NAV',
                'AccruedValueNAV': 'PS Accrued Value NAV',
            }),
            'accrued_interest': (cash_tf, ins_type_grouper, (('Deposit',),), {
                'FairValueNAV': 'Prime Services Monthly Carry',
                'AccruedValueNAV': 'Prime Services Monthly Carry',
            }),
            'ff_equities_exposure': (equity_section_tf, fin_ins_type_grouper, (('Fully Funded',),), {
                'FairValueNAV': ps_fair_nav_column,
                'AccruedValueNAV': ps_accrued_nav_column,
            }),
            'ff_fixed_income_exposure': (fixed_income_tf, fin_ins_type_grouper, (('Fully Funded',),), {
                'FairValueNAV': 'PS Fair Value NAV',
                'AccruedValueNAV': 'PS Accrued Value NAV',
            }),
            'unsettled_cash_eq': (equity_section_tf, fin_ins_type_grouper, (('Fully Funded',),), {
                'FairValueNAV': 'Unsettled Cash End',
                'AccruedValueNAV': 'Unsettled Cash End',
            }),
            'unsettled_cash_fi': (fixed_income_tf, fin_ins_type_grouper, (('Fully Funded',),), {
                'FairValueNAV': 'Unsettled Cash End',
                'AccruedValueNAV': 'Unsettled Cash End',
            }),
            'accrued_dividends': (equity_section_tf, fin_ins_type_grouper, (('Fully Funded',),), {
                'FairValueNAV': 'Corporate Action Value Sum',
                'AccruedValueNAV': 'Corporate Action Value Sum',
            }),
            'unpaid_coupons': (fixed_income_tf, fin_ins_type_grouper, (('Fully Funded',),), {
                'FairValueNAV': 'Ex Coupon Value',
                'AccruedValueNAV': 'Ex Coupon Value',
            }),
        }

        def get_total(column_id, trade_filter, grouper, key_sequences):
            """Get a sum of the column's values at the given key sequences."""
            calc_space = CalculationSpace.from_source(trade_filter, grouper=grouper)
            calc_space.simulate_value('Portfolio Profit Loss Start Date', 'Inception')
            calc_space.simulate_value('Portfolio Profit Loss End Date', 'Now')
            total = 0.0
            for key_sequence in key_sequences:
                try:
                    cell = calc_space.retrieve(key_sequence)
                except KeyError:  # Specified key sequence is not in the cspace.
                    continue
                value = cell.calc_space.CalculateValue(cell.node.Tree(), column_id)
                if hasattr(value, 'Number'):
                    value = value.Number()
                total += value
            return total

        for report_column in ('FairValueNAV', 'AccruedValueNAV'):
            row_values = {}
            for row_code, row_spec in row_specs.items():
                tf, grouper, keys, column_mapping = row_spec
                row_values[row_code] = get_total(column_mapping[report_column],
                    tf, grouper, keys)

            rv = row_values
            LOGGER.info("NAV section data for %s: %s", report_column, pprint.pformat(rv))

            self._values[report_column]['NAV'] = OrderedDict((  # Keep row order.
                ('Call Account Balance', rv['closing_balance'] - rv['accrued_interest']),
                ('Accrued Interest', rv['accrued_interest']),
                ('Fully Funded', (rv['ff_equities_exposure'] + rv['ff_fixed_income_exposure'])),
                ('Total', rv['ff_equities_exposure'] + rv['ff_fixed_income_exposure'] + rv['closing_balance']),
            ))
            self._values[report_column]['FullyFundedBreakDownComponents'] = {
                'NAV Exposure': (rv['ff_equities_exposure'] + rv['ff_fixed_income_exposure']
                    - rv['accrued_dividends'] - rv['unpaid_coupons']
                    - rv['unsettled_cash_eq'] - rv['unsettled_cash_fi']),
                'Accrued Corporate Action Cash': (rv['accrued_dividends'] + rv[
                    'unpaid_coupons']),
                'Unsettled Cash': (rv['unsettled_cash_eq'] + rv['unsettled_cash_fi']),
                'Total': (rv['ff_equities_exposure'] + rv['ff_fixed_income_exposure']),
            }

    def populate_fully_funded_breakdown_by_ins_type(self, equity_section_tf, fixed_income_tf):
        """Populate the FullyFunded NAV Breakdown section."""

        ps_fair_nav_column = 'PS Fair Value NAV'
        ps_accrued_nav_column = 'PS Accrued Value NAV'

        term_specs = {
            'ff_equities_exposure': (equity_section_tf, {
                'FairValueNAV': ps_fair_nav_column,
                'AccruedValueNAV': ps_accrued_nav_column,
            }),
            'ff_fixed_income_exposure': (fixed_income_tf, {
                'FairValueNAV': 'PS Fair Value NAV',
                'AccruedValueNAV': 'PS Accrued Value NAV',
            }),
        }

        # Merge the different fully-funded ins_types dictionaries and update the _values dictionary
        for report_column in ('FairValueNAV', 'AccruedValueNAV'):
            values_dict = {}
            for term_code, term_spec in term_specs.items():
                tf, column_mapping = term_spec
                values_dict.update(get_values_by_ins_type(column_mapping[report_column], tf,
                                                          limit_by_financed='Fully Funded'))
            self._values[report_column]['FullyFundedBreakDownInsTypes'] = values_dict
            self._values[report_column]['FullyFundedBreakDownInsTypes']['Total'] = sum(
                    self._values[report_column]['FullyFundedBreakDownInsTypes'].values())
            LOGGER.info("FullyFunded NAV Breakdown for %s: %s",
                        report_column, pprint.pformat(self._values[report_column]['FullyFundedBreakDownInsTypes']))
        self._remove_zero_rows('FullyFundedBreakDownInsTypes')

    def to_xml(self):
        """Converts self.Values into XML presentation that will go through the XSLT for FO / PDF conversion"""
        report_xml = ReportXML()
        report_xml.add_report(self._values)
        return str(report_xml)

    @staticmethod
    def _set_report_api_parameters(report, file_path, filename, xls_pdf_template):
        report.ambAddress = ''
        report.ambSender = ''
        report.ambSubject = ''
        report.ambXmlMessage = False
        report.clearSheetContent = False
        report.compressXmlOutput = False
        report.createDirectoryWithDate = False
        report.dateFormat = '%d%m%y'
        report.expiredPositions = False
        report.fileDateFormat = ''
        report.fileDateBeginning = False
        report.fileName = filename
        report.filePath = file_path
        report.function = None
        report.gcInterval = 5000
        report.gridOutput = False
        report.gridUseLoopbackGridClient = False
        report.gridRowPartitionCbArg = None
        report.gridRowPartitionCbClass = None
        report.gridExcludeRowCbClass = "FReportGridCallbacks.ExcludeRowManager"
        report.gridAggregateXmlCbClass = None
        report.gridTimeout = None
        report.gridRowSet = None
        report.grouping = 'Default'
        report.htmlToFile = False
        report.htmlToPrinter = False
        report.htmlToScreen = False
        report.includeDefaultData = False
        report.includeFormattedData = False
        report.includeFullData = False
        report.includeRawData = False
        report.instrumentParts = False
        report.instrumentRows = False
        report.maxNrOfFilesInDir = 1000
        report.multiThread = False
        report.numberOfReports = 1
        report.orders = None
        report.overridePortfolioSheetSettings = False
        report.overrideTimeSheetSettings = False
        report.overrideTradeSheetSettings = False
        report.overwriteIfFileExists = True
        report.param = None
        report.performanceStrategy = 'Periodic full GC to save memory'
        report.portfolioReportName = ''
        report.portfolioRowOnly = False
        report.portfolios = None
        report.preProcessXml = None
        report.printStyleSheet = 'FStandardCSS'
        report.printTemplate = 'FStandardTemplateClickable'
        report.reportName = ''
        report.secondaryFileExtension = '.pdf'
        report.secondaryOutput = True
        report.secondaryTemplate = xls_pdf_template
        report.sheetSettings = {}
        report.snapshot = True
        report.storedASQLQueries = None
        report.template = None
        report.tradeFilters = None
        report.tradeRowsOnly = False
        report.trades = None
        report.updateInterval = 60
        report.workbook = None
        report.xmlToAmb = False
        report.xmlToFile = True  # Let RTB parse the output and display NAV on the dashboard - ABITFA-2914.
        report.zeroPositions = False
        report.guiParams = None
        report.reportApiObject = None
        
    def create_report(self, file_path, filename, xslt, client_name, report_name,
                      output_type, framework_version=None):
        report = FReportAPI.FWorksheetReportApiParameters()
        self._set_report_api_parameters(report, file_path, filename, xslt)
        
        root = ElementTree.XML(self.to_xml())
        report_parameters = root.find("ReportParameters")
        
        if not report_parameters:
            report_parameters = ElementTree.SubElement(root, "ReportParameters")
        else:
            report_parameters = report_parameters[0]
        ElementTree.SubElement(report_parameters, 'DateToday').text = PS_XMLReportingTools._getDate('Now', None)
        try:
            tf = self._equity_tf.Snapshot()
            if not len(tf):
                tf = self._fixed_income_tf.Snapshot()
            if tf:
                prf = get_root_cr_portfolio(tf[0])
                prf_oid = prf.Oid()
                ElementTree.SubElement(report_parameters, 'PortfolioOID').text = str(prf_oid)
                ElementTree.SubElement(report_parameters, 'PortfolioName').text = str(prf.Name())
            else:
                LOGGER.info("The trade filters equity and fixed income have no trades")
        except Exception:
            # Most likely there are no trades in the trade filters. There
            # is no adverse impact; PS_NAV_Aggregator will simply ignore
            # this client.
            LOGGER.exception("Unable to add root prf oid to Report Params.")

        report_xml = ElementTree.tostring(root)
        report_xml = PS_XMLReportingTools._addAddress(report_xml, client_name)
        report_xml = PS_XMLReportingTools._addReportParameter(report_xml, 'ReportName', report_name)
        generated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_xml = PS_XMLReportingTools._addReportParameter(report_xml, 'GeneratedTime', generated_time)
        
        if framework_version:
            report_xml = PS_XMLReportingTools._addReportParameter(report_xml,
                    'FrameworkVersion', framework_version)
        report_xml = PS_XMLReportingTools._addRunLocation(report_xml)
        report.CreateReportByXml(report_xml)
        LOGGER.info('Removing FO file')
        try:
            fo_file_path = os.path.join(file_path, filename + '.fo')
            if os.path.exists(fo_file_path):
                os.remove(fo_file_path)
                LOGGER.info('Removed')
        except Exception:
            LOGGER.exception('An exception occurred while trying to remove the fo file.')
        return filename + '.pdf'


ael_variables = []
ael_variables.append(['reportTitle', 'Report Tilte', 'string', None, 'Exposure and NAV Report', 1, 0, 'Report Title', None, 1])
ael_variables.append(['clientName', 'ClientName', acm.FCounterParty, None, None, 1, 0, 'Client details that will be on report', None, 1])
ael_variables.append(['eqTradeFilters', 'Equity', acm.FTradeSelection, None, None, 0, 0, 'Trade Filters that will be used to populate EQ part of report', None, 1])
ael_variables.append(['fiTradeFilters', 'Fixed Income', acm.FTradeSelection, None, None, 0, 0, 'Trade Filters that will be used to populate FI part of report', None, 1])
ael_variables.append(['cashTradeFilters', 'Cash', acm.FTradeSelection, None, None, 0, 0, 'Trade Filters that will be used to populate Cash part of report', None, 1])
ael_variables.append(['output', 'Output Type', 'string', ['PDF', 'CSV'], 'PDF', 1, 0, 'Report output file type', None, 1])
ael_variables.append(['filePath', 'File Path', 'string', None, 'C:\\Temp2\\', 1, 0, 'Report ouput path', None, 1])
ael_variables.append(['fileName', 'File Name', 'string', None, 'ValReport', 1, 0, 'Report ouput filename WITHOUT any extension', None, 1])

xslt = 'pb_nav_report'


def _convertToParamDictionary(report_controller_dictionary, report_name):
    '''
    Gets called from report controller on custom reports to return a compatible report dictionary
    '''
    date_suffix = DateField.read_date(report_controller_dictionary['date_SoftBroker'],
                                      default=TODAY).replace('-', '')
    filename = report_controller_dictionary['fileID_SoftBroker'] + '_' + \
               report_controller_dictionary['Filename_' + report_name] + '_' + date_suffix
    return {
        'reportTitle': report_controller_dictionary['reportTitle_' + report_name],
        'clientName': acm.FCounterParty[report_controller_dictionary['clientName']],
        'eqTradeFilters': report_controller_dictionary['eqTradeFilter_' + report_name],
        'fiTradeFilters': report_controller_dictionary['fiTradeFilter_' + report_name],
        'cashTradeFilters': report_controller_dictionary['cashTradeFilter_' + report_name],
        'filePath': report_controller_dictionary['OutputPath'],
        'fileName': filename,
        'output': 'PDF',
    }


def ael_main(params):
    process_name = "ps.nav2.{0}".format(get_pb_fund_shortname(params['clientName']))
    with bp_start(process_name):
        nav = NAVReport()
        nav.populate_equity_section(params['eqTradeFilters'])
        nav.populate_fi_section(params['fiTradeFilters'])
        nav.populate_cash_section(params['cashTradeFilters'])
        nav.update_totals()
        nav.populate_nav(params['cashTradeFilters'], params['eqTradeFilters'], params['fiTradeFilters'])
        nav.populate_fully_funded_breakdown_by_ins_type(params['eqTradeFilters'], params['fiTradeFilters'])
        nav.populate_leverage()
        filename = nav.create_report(params['filePath'], params['fileName'], xslt,
                                     params['clientName'].Name(), params['reportTitle'], params['output'],
                                     params.get('frameworkVersion'))
        LOGGER.info('Wrote secondary output to: %s%s', params['filePath'], filename)
