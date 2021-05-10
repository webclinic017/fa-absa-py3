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
Date            Change no     Developer         Description
--------------------------------------------------------------------------------
2011-07-13      713436        Rohan vd Walt     Initial Implementation
2011-07-27      724933        Rohan vd Walt     Change report filenames to be
                                                client specific and only remove
                                                client specific fo files.
2011-08-03      750738        Rohan vd Walt     Change structure to support
                                                use template workbook,
                                                and rather insert Trade Filters,
                                                makes column changes/maintanence
2011-08-19      750738        Rohan vd Walt     Misc changes +
                                                Warehousing Report
2011-09-02      759616        Rohan vd Walt     Add NAV report
2011-09-07      762168        Herman Hoon       Added the Bencmark
                                                Delta Risk report
2011-09-13      768482        Rohan vd Walt     Ability to define preprocessors
                                                per FWorksheetReport and shows
                                                expired trades as well
2011-11-23      837929        Herman Hoon       Option to produce CSV output
                                                for reports as well. Added
                                                the Benchmark Delta reports.
2012-10-30      620753        Nidheesh Sharma   Added portfolio parameter
                                                and added PS_FinanceAndFeeReport
                                                and PS_Cashflows.
2012-10-30      620753        Hynek Urban       Descriptor generation refactor.
2013-03-08      857456        Peter Basista     Remove _getCallAccounts
                                                function and use the one
                                                from the PS_Functions module
                                                (getCallAccounts function).
2013-03-19      885480        Peter Basista     Split the core functionality
                                                and static data previously
                                                present in PS_ReportController
                                                into two modules. This file
                                                contains the core functionality.
2014-01-13      1712088       Hynek Urban       Introduce the ReportDescription
                                                classes, don't use the old
                                                REPORT_DESCRIPTIONS.
2014-11-20      2450799       Ondrej Bahounek   Fixing errors and exception
                                                handling.
2015-01-14      2562289       Hynek Urban       Remove a bug in custom reports
                                                error reporting.
2018-12-04      CHG1001190167 Qaqamba Ntshobane Added option to use a different
                                                template for CSV and XLS reports.
"""
import os
import acm
from itertools import chain

import FReportAPI
from PS_FormUtils import DateField
from PS_WebPortal import generate_descriptor, Report
import at_logging


LOGGER = at_logging.getLogger()


START_DATES = DateField.get_captions(['Inception', 'First Of Year',
    'First Of Month', 'PrevBusDay', 'TwoBusinessDaysAgo', 'TwoDaysAgo',
    'Yesterday', 'Custom Date', 'Now'])
END_DATES = DateField.get_captions(['Now', 'TwoDaysAgo', 'PrevBusDay',
    'Yesterday', 'Custom Date'])


class ReportDescription(object):
    """Wraps the information about a report that should be generated."""

    def __init__(self, name, filename, key_prefix):
        """
        Simply store all input arguments on self.

        <name>: name of the report (as in ael_variables)
        <filename>: default value of the file name of the generated report
            (without extension and the date suffix)
        <key_prefix>: prefix of the unique key that goes into the Softbroker descriptor

        """
        self.name, self.filename, self.key_prefix = name, filename, key_prefix

    def get_generated_filename(self, config):
        """
        Get the actual filename that was (or will be) generated.

        Filename doesn't contain the extension.

        <config> is the user input that goes to ael_main.

        """
        filename = config['Filename_%s' % self.name]
        client_id = config['fileID_SoftBroker'].replace(' ', '_')
        date = DateField.read_date(config['date_SoftBroker'],
            default=acm.Time.DateToday()).replace('-', '')

        return '%s_%s_%s' % (client_id, filename, date)


class CustomReportDescription(ReportDescription):
    """Report description for custom reports."""

    def __init__(self, name, filename, key_prefix, callback, module,
            callback_params):
        """
        In addition to the regular report description, the following params are defined:

        <callback>: The callback function that creates ael_variables record.
        <module>: name of the module where report generation takes place
        <callback_params>: A dictionary of parameters for the callback function.

        """
        super(CustomReportDescription, self).__init__(name, filename,
            key_prefix)
        self.callback, self.module = callback, module
        self.callback_params = callback_params


def _set_report_api_parameters(report, report_description, configuration,
        output_type='PDF'):
    """Set the FReportAPI parameters before report generation."""
    report_name = report_description.name
    sheet_settings = {
        'FPortfolioSheet': {
            'Portfolio Profit Loss End Date Custom':
                configuration['Portfolio Sheet End Date Custom_' + report_name],
            'Portfolio Profit Loss End Date':
                configuration['Portfolio Sheet End Date_' + report_name],
            'Portfolio Profit Loss Start Date':
                configuration['Portfolio Sheet Start Date_' + report_name],
            'Valuation Date': '',
            'Portfolio Profit Loss Start Date Custom':
                configuration[('Portfolio Sheet Start Date Custom_' + 
                report_name)],
            'Portfolio Hide Zero Positions Choice': 'Risk Position'},
        'FTimeSheet': {'PL Valuation Date Custom': ''},
        'FTradeSheet': {
            'Portfolio Profit Loss End Date Custom':
                configuration['Trade Sheet End Date Custom_' + report_name],
            'Portfolio Profit Loss End Date':
                configuration['Trade Sheet End Date_' + report_name],
            'Portfolio Profit Loss Start Date Custom':
                configuration['Trade Sheet Start Date Custom_' + report_name],
            'Portfolio Profit Loss Start Date':
                configuration['Trade Sheet Start Date_' + report_name],
            'Portfolio Hide Zero Positions Choice': 'Risk Position'}
    }

    report.ambAddress = ''
    report.ambSender = ''
    report.ambSubject = ''
    report.ambXmlMessage = False
    # If both trade filter and portfolio are selected,
    # then only trade filter will be inserted into the report.
    # Trade filter field needs to be empty
    # for the portfolio to be inserted into the report.
    report.clearSheetContent = False
    report.storedASQLQueries = None
    report.tradeFilters = None
    report.portfolios = None

    # Configuration priority:
    #   1. Stored ASQL query (Query Folder)
    #   2. Trade filter
    #   3. Portfolio
    #   4. if none of the above is set, the workbook is left intact
    if configuration['storedASQLQuery_' + report_name]:
        report.clearSheetContent = True
        report.storedASQLQueries = configuration[
            'storedASQLQuery_' + report_name]
    elif configuration['TradeFilter_' + report_name]:
        report.clearSheetContent = True
        report.tradeFilters = configuration['TradeFilter_' + report_name]
    elif configuration['Portfolio_' + report_name]:
        report.clearSheetContent = True
        report.portfolios = configuration['Portfolio_' + report_name]

    report.compressXmlOutput = False
    report.createDirectoryWithDate = False
    report.dateFormat = '%d%m%y'
    report.expiredPositions = configuration[
        'ExpiredPositions_' + report_name] == 'Yes'
    report.fileDateFormat = ''
    report.fileDateBeginning = False
    report.fileName = report_description.get_generated_filename(configuration)
    report.filePath = configuration['OutputPath']
    report.function = None
    report.gcInterval = 5000
    report.gridOutput = False
    report.gridUseLoopbackGridClient = False
    report.gridRowPartitionCbArg = None
    report.gridRowPartitionCbClass = None
    report.gridExcludeRowCbClass = None
    report.gridAggregateXmlCbClass = None
    report.gridTimeout = None
    report.gridRowSet = None
    report.grouping = (configuration['Grouping_' + report_name] if
        configuration['Grouping_' + report_name] != '' else 'Default')
    report.htmlToFile = False
    report.htmlToPrinter = False
    report.htmlToScreen = False
    report.includeDefaultData = False
    report.includeFormattedData = True
    report.includeFullData = False
    report.includeRawData = True
    report.instrumentParts = False
    report.instrumentRows = (configuration[
        'ShowInstrumentRows_' + report_name] == 'Yes' 
            if configuration['ShowInstrumentRows_' + report_name] 
            else 'Yes')
    report.maxNrOfFilesInDir = 1000
    report.multiThread = False
    report.numberOfReports = 1
    report.orders = None
    report.overridePortfolioSheetSettings = 'True'
    report.overrideTimeSheetSettings = 'False'
    report.overrideTradeSheetSettings = 'True'
    report.overwriteIfFileExists = True
    report.param = (
        configuration['clientName'] + ',' + 
        configuration['reportTitle_' + report_name] + 
        (',Yes' if configuration[('CallAccount_' + report_name)
            ] == 'Yes' else ',') + 
        ',ReportController2'  # Version - to be changed if the framework changes significantly.
    )
    report.performanceStrategy = 'Periodic full GC to save memory'
    report.portfolioReportName = ''
    report.portfolioRowOnly = False
    report.preProcessXml = configuration['XMLProcessor_' + report_name]
    report.printStyleSheet = 'FStandardCSS'
    report.printTemplate = 'FStandardTemplate'
    report.report_name = ''
    if output_type == 'PDF':
        report.secondaryFileExtension = '.pdf'
        report.secondaryTemplate = configuration['XSLT_' + report_name]
    elif output_type == 'XLS':
        # Note: The generated file will actually NOT
        # be an Excel file, but simply a csv file with
        # a different extension.
        report.secondaryFileExtension = '.xls'
        if not configuration['XSLT2_' + report_name]:
            report.secondaryTemplate = 'pb_csvtemplate'
        else:
            report.secondaryTemplate = configuration['XSLT2_' + report_name]
    elif output_type == 'CSV':
        report.secondaryFileExtension = '.csv'
        if not configuration['XSLT2_' + report_name]:
            report.secondaryTemplate = 'pb_csvtemplate'
        else:
            report.secondaryTemplate = configuration['XSLT2_' + report_name]

    report.secondaryOutput = True
    report.sheetSettings = sheet_settings
    report.snapshot = True
    report.template = None
    report.tradeRowsOnly = (True if configuration['TradeRowsOnly_' + 
        report_name] == 'Yes' else False)
    report.trades = None
    report.updateInterval = 60
    report.workbook = configuration['Workbook_' + report_name]
    report.xmlToAmb = False
    report.xmlToFile = False
    report.zeroPositions = configuration[
        'ZeroPositions_' + report_name] == 'Yes'
    report.guiParams = None
    report.reportApiObject = None
    return report


def generate_softbroker_descriptor(report_descriptions, configuration):
    """Gather the necessary data and call PS_WebPortal.generate_descriptor."""
    client_name = configuration['clientName']
    client_id = configuration['fileID_SoftBroker']
    output_path = configuration['OutputPath']

    date = DateField.read_date(configuration['date_SoftBroker'],
        default=acm.Time.DateToday())
    year, month, day = acm.Time.DateToYMD(date)
    date_key = str(year) + str(month).zfill(2) + str(day).zfill(2)

    reports = []
    for report_description in report_descriptions:
        for format_ in ('PDF', 'XLS', 'CSV'):
            expected_filename = report_description.get_generated_filename(
                configuration) + '.' + format_
            for generated_filename in os.listdir(output_path):
                # Go through the generated files and find the relevant one.
                if generated_filename.lower() == expected_filename.lower():
                    # Keep the convention of case ignoring from windows.
                    filename_no_date = generated_filename.replace('_%s' % date_key, '')
                    report_kwargs = {
                        'filename': generated_filename,
                        'file_type': format_,
                        'description': filename_no_date,  # Required by the Portal.
                        'unique_key': '%s_%s_%s_%s' % (
                            report_description.key_prefix,
                            format_, client_id.replace(" ", "_"), date_key)
                    }
                    reports.append(Report(**report_kwargs))
                    # No need to go through the rest of the generated files.
                    break

    # Cleanup the generated .fo files found in the output_path directory.
    for fname in os.listdir(output_path):
        if (fname.lower().startswith(client_id.lower().replace(" ", "_"))
                and fname.lower().endswith('.fo')):
            os.unlink(os.path.join(output_path, fname))

    descriptor_filename = ''.join(
        # PB2_ prefix distinguishes the new suite from the old one.
        # TODO: Change the prefix back to PB_ once the old suite is decomisssioned.
        ['PB2_', client_id.replace(" ", "_"), '_CR_', date_key, '.xml'])
    descriptor_filename = os.path.join(output_path, descriptor_filename)
    generate_descriptor(date, client_name, descriptor_filename, reports)


def add_report(ael_variables, report_name, file_name):
    """
    Adds a checkbox on main tab and a generic report tab for report
    """
    today = acm.Time().DateToday()
    ael_variables.extend([[report_name, report_name, 'string', ['No', 'Yes'],
        'No', 1, 0, 'Generate this report?', None, 1],
        ['reportTitle_' + report_name, 'Report Title_' + report_name,
        'string', None, file_name, 0, 0,
        'Title of report that will appear in PDF, gets passed '
        'to XML Preprocessor', None, 1],
        ['CallAccount_' + report_name, 'Add Call Account Nr_' + report_name,
        'string', ['No', 'Yes'], '', 0, 0,
        'PreProcessor Parameter', None, 1],
        ['Workbook_' + report_name, 'Workbook_' + report_name,
        'string', None, '', 0, 0,
        'Workbook to run Task on', None, 1],
        ['TradeFilter_' + report_name, 'Add Trade Filter_' + report_name,
        'string', None, '', 0, 1,
        'Trade Filter to add to report, this will force clear '
        'of workbook contents', None, 1],
        ['storedASQLQuery_' + report_name,
        'Add stored ASQL query_' + report_name,
        'string', None, '', 0, 0,
        'Stored ASQL query to add to report, this will force '
        'clear of workbook contents', None, 1],
        ['Portfolio_' + report_name, 'Portfolio_' + report_name,
        'FPhysicalPortfolio', None, None, 0, 1,
        'Portfolio to add to report, this will force '
        'clear of workbook contents (Trade Filter field '
        'should be empty for portfolio to be added to the report)'],
        ['Grouping_' + report_name, 'Grouping_' + report_name,
        'string', None, '', 0, 0,
        'Grouping to use in the report', None, 1],
        ['TradeRowsOnly_' + report_name, 'Show Trade Rows Only_' + report_name,
        'string', ['No', 'Yes'], 'No', 1, 0,
        'Show only trade rows in report', None, 1],
        ['ZeroPositions_' + report_name,
        'Include Zero Positions_' + report_name, 'string', ['No', 'Yes'],
        'Yes', 1, 0, 'Include zero positions in the report', None, 1],
        ['ExpiredPositions_' + report_name,
        'Include Expired Positions_' + report_name, 'string', ['No', 'Yes'],
        'Yes', 1, 0, 'Include expired positions in the report', None, 1],
        ['ShowInstrumentRows_' + report_name,
        'Show Instrument Rows_' + report_name, 'string', ['No', 'Yes'],
        'Yes', 1, 0, 'Include expired positions in the report', None, 1],
        ['PDFOutput_' + report_name, 'Generate PDF Output_' + report_name,
        'string', ['No', 'Yes'], 'No', 1, 0,
        'Generate PDF file for Softbroker output as well', None, 1],
        ['CSVOutput_' + report_name, 'Generate CSV Output_' + report_name,
        'string', ['No', 'Yes'], 'No', 1, 0,
        'Generate CSV file for Softbroker output as well', None, 1],
        ['XLSOutput_' + report_name, 'Generate XLS Output_' + report_name,
        'string', ['No', 'Yes'], 'No', 1, 0,
        'Generate XLS file for Softbroker output as well', None, 1],
        ['XSLT_' + report_name, 'XSLT PDF_' + report_name,
        'string', None, '', 0, 0,
        'XSLT template to use for PDF generation', None, 1],
        ['XSLT2_' + report_name, 'XSLT CSV_' + report_name,
        'string', None, '', 0, 0,
        'XSLT template to use for CSV and XLS generation', None, 1],
        ['XMLProcessor_' + report_name, 'XML Preprocessor_' + report_name,
        'string', None, 'PS_XMLReportingTools.PreProcessXML', 0, 0,
        'Method called to do additional processing on XML', None, 1],
        ['Filename_' + report_name, 'Filename_' + report_name,
        'string', None, file_name, 0, 0,
        'Filename of the generated report (without extension)', None, 1],
        ['Trade Sheet Start Date_' + report_name,
        'Trade Sheet Start Date_' + report_name,
        'string', START_DATES, '', 0, 0,
        'PnL Start Date for Trade Sheet', None, 1],
        ['Trade Sheet Start Date Custom_' + report_name,
        'Trade Sheet Start Date Custom_' + report_name,
        'string', None, None, 0, 0,
        'Custom from date example: ' + today, None, 1],
        ['Trade Sheet End Date_' + report_name,
        'Trade Sheet End Date_' + report_name,
        'string', END_DATES, '', 0, 0,
        'PnL End Date for Trade Sheet', None, 1],
        ['Trade Sheet End Date Custom_' + report_name,
        'Trade Sheet End Date Custom_' + report_name,
        'string', None, None, 0, 0,
        'Custom to date example: ' + today, None, 1],
        ['Portfolio Sheet Start Date_' + report_name,
        'Portfolio Sheet Start Date_' + report_name,
        'string', START_DATES, '', 0, 0,
        'PnL Start Date for Portfolio Sheet', None, 1],
        ['Portfolio Sheet Start Date Custom_' + report_name,
        'Portfolio Sheet Start Date Custom_' + report_name,
        'string', None, None, 0, 0,
        'Custom from date example: ' + today, None, 1],
        ['Portfolio Sheet End Date_' + report_name,
        'Portfolio Sheet End Date_' + report_name,
        'string', END_DATES, '', 0, 0,
        'PnL End Date for Portfolio Sheet', None, 1],
        ['Portfolio Sheet End Date Custom_' + report_name,
        'Portfolio Sheet End Date Custom_' + report_name,
        'string', None, None, 0, 0,
        'Custom to date example: ' + today, None, 1]])


def add_report_tabs(ael_variables, report_descriptions):
    """
    For each report, create its report-specific settings
    using ael_variables.
    """
    ael_variables.extend([['clientName', 'Client Name',
        'string', None, None, 1, 0,
        'Client Name that will be passed to all reports', None, 1],
        ['OutputPath', 'Output Path',
        'string', None, 'C:\\output\\', 1, 0,
        'Where reports and SoftBroker Descriptor will be generated', None, 1],
        ['generate_SoftBroker', 'Generate Softbroker XML_SoftBroker',
        'string', ['No', 'Yes'], 'Yes', 1, 0,
        'Generates Softbroker Descriptor XML file from working directory '
        'PDF files, as well as deleting all FO files '
        'left after FOP PDF generation', None, 1],
        ['date_SoftBroker', 'Date_SoftBroker',
        'string', None, None, 0, 0,
        'Date that will be put in descriptor files - Report Date.'
        'If blank, will use current date', None, 1],
        ['fileID_SoftBroker', 'Report Files ID_SoftBroker',
        'string', None, None, 0, 0,
        'The ClientID that will be prepended before the report filename',
        None, 1]])

    for report_description in report_descriptions:
        add_report(ael_variables, report_description.name,
            report_description.filename)


def add_custom_report_tabs(ael_variables, custom_reports):
    """
    For each custom report, call its callBack function.
    This function should be responsible for adding
    a new tab of report-specific settings using ael_variables.
    """
    for custom_report in custom_reports:
        custom_report.callback(ael_variables, custom_report.name,
            custom_report.filename, **custom_report.callback_params)


def generate_reports(configuration, regular_reports, custom_reports):
    """
    Generate all reports and the Portal descriptor.

    <configuration> is an instance of the ael_variables dictionary.
    <regular_reports>, <custom_reports> are lists of ReportDescription
        instances.

    """
    has_errors = False
    for report in regular_reports:
        try:
            if configuration[report.name] != 'Yes':
                continue
            for format_ in ('PDF', 'XLS', 'CSV'):
                if configuration[format_ + 'Output_' + report.name] == 'Yes':
                    report_api_params = FReportAPI.FWorksheetReportApiParameters()
                    report_api_params = _set_report_api_parameters(
                        report_api_params, report, configuration, format_)
                    report_api_params.RunScript()
        except Exception:
            LOGGER.exception('Report %s was not generated.', report.name)
            has_errors = True

    for custom_report in custom_reports:
        try:
            if configuration[custom_report.name] != 'Yes':
                continue
            report_module = __import__(custom_report.module)
            custom_report_parameters = report_module._convertToParamDictionary(
                configuration, custom_report.name)
            custom_report_parameters['frameworkVersion'] = 'ReportController2'
            report_module.ael_main(custom_report_parameters)
        except Exception:
            LOGGER.exception('Report %s was not generated.', custom_report.name)
            has_errors = True

    if configuration['generate_SoftBroker'] == 'Yes':
        generate_softbroker_descriptor(chain(regular_reports, custom_reports),
            configuration)
            
    if has_errors:
        msg = 'Some reports were not created (see the log for details).'
        raise RuntimeError(msg)
