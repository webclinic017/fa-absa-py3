"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Creates & compares P/L reports to verify 
                           Security Loan Aggregation
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  416955
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2010-08-31 416955    Francois Truter           Updated report grouping
"""

import acm
from datetime import datetime
import os.path
import FReportAPI
import FPortfolioComparison
import sl_aggregation

class SLAggregationComparisonReport:

    def __init__(self, filepath, tradeFilterNames):
        if not os.path.exists(filepath):
            raise Exception('The path [%s] does not exist - please supply a valid path for the Security Loan Aggregation Comparison Reports.' % filepath)
        
        if not tradeFilterNames:
            raise Exception('Please specify a trade filer to run the comparison reports on')
        
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d%H%M%S')
        
        self.__filepath = filepath
        self.__tradeFilterNames = tradeFilterNames
        self.__beforeFilename = 'BeforeSLAggregation_' + timestamp
        self.__afterFilename = 'AfterSLAggregation_' + timestamp
        self.__compareFilename = 'Difference_' + timestamp
        
    def _beforeFilePath(self):
        return os.path.join(self.__filepath, self.__beforeFilename) + '.xml'
        
    def _afterFilePath(self):
        return os.path.join(self.__filepath, self.__afterFilename) + '.xml'
        
    def _compareFilePathNoExt(self):
        return os.path.join(self.__filepath, self.__compareFilename)
        
    def _setReportAPIParameters(self, report, filename):
        report.ambAddress = ''
        report.ambSender = ''
        report.ambSubject = ''
        report.ambXmlMessage = False
        report.clearSheetContent = True
        report.compressXmlOutput = False
        report.createDirectoryWithDate = False
        report.dateFormat = '%d%m%y'
        report.expiredPositions = False
        report.fileDateFormat = ''
        report.fileDateBeginning = False
        report.fileName = filename
        report.filePath = self.__filepath
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
        report.grouping = 'SLUnderlyingPortfolioCParty'
        report.htmlToFile = True
        report.htmlToPrinter = False
        report.htmlToScreen = False
        report.includeDefaultData = False
        report.includeFormattedData = True
        report.includeFullData = False
        report.includeRawData = True
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
        report.portfolioRowOnly = True
        report.portfolios = None
        report.preProcessXml = None
        report.printStyleSheet = 'FStandardCSS'
        report.printTemplate = 'FStandardTemplate'
        report.reportName = ''
        report.secondaryFileExtension = ''
        report.secondaryOutput = False
        report.secondaryTemplate = 'FTABTemplate'
        report.sheetSettings = {}
        report.snapshot = True
        report.storedASQLQueries = None
        report.template= None
        report.tradeFilters = self.__tradeFilterNames
        report.tradeRowsOnly = False
        report.trades = None
        report.updateInterval = 60
        report.workbook = 'SL_Aggregation_Comparison'
        report.xmlToAmb = False
        report.xmlToFile = True
        report.zeroPositions = False
        report.guiParams = None
        report.reportApiObject = None

    def CreateReportBeforeAggregation(self):
        report = FReportAPI.FWorksheetReportApiParameters()
        self._setReportAPIParameters(report, self.__beforeFilename)
        report.RunScript()
        print('Created report before aggregation.')
        
    def CreateReportAfterAggregation(self):
        report = FReportAPI.FWorksheetReportApiParameters()
        self._setReportAPIParameters(report, self.__afterFilename)
        report.RunScript()
        print('Created report after aggregation.')
        
    def Compare(self):
        absolutePrecision = 0.0001
        relativePrecision = 0.0001
        result = FPortfolioComparison.diff(self._beforeFilePath(), self._afterFilePath(), self._compareFilePathNoExt(), absolutePrecision, relativePrecision)
        print('Before and after files compared, difference:')
        if result:
            print(result)
        else:
            print('  no difference found')

