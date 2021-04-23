""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FRiskCubeWriterBase.py"
from __future__ import print_function
"""---------------------------------------------------------------------------
MODULE
    FRiskCubeWriterBase - Classes to receive results.
    Base + a few other simple classes for writing Risk Cube-format data files.

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

---------------------------------------------------------------------------"""

import os, os.path
import sys
import inspect
import hashlib
import math

import acm
import FMarketRiskExportAttributes
import FBDPCommon

MAX_FILES_IN_DIR = 256
FILE_SUFFIXES = ('.dat', '.txt', '.csv')
DEFAULT_SEPARATORS = ['|', ',']
DESCRIPTION = 'Description'
HEADER_FORMAT = 'Header Format'
DATA_FORMAT = 'Data Format'
COLUMN_COUNT = 'Columns'
SOURCE_ENCODING = 'latin1'
TARGET_ENCODING = 'utf8'

CURVE_DATE = 'Curve Date'
PRICE_DATE = 'Price Date'
   
CURVE_ID = 'ID'
DELTA = 'Delta'
THETA = 'Theta'
GROUP = 'Group'
HORIZON_PARAM = 'Horizon'
HORIZON_DAYS_PARAM = 'Horizon Order'
MONEYNESS = 'Moneyness'
BUMP_LADDER = "Bump Ladder"
PRICE_BUMP = "Underlying Bump"
VOL_BUMP = "Volatility Bump"
SCENARIO = 'Scenario'
SCENARIO_COUNT = 'Scenario Count'
SCENARIO_DATE = 'Scenario Date'
DECAY_FACTOR = 'Decay'
START_DATE = 'Start Date'
END_DATE = 'End Date'
IS_ANTITHETIC = 'Is Antithetic'
PL_SOURCE = 'PL Source'
SENSITIVITY = 'Sensitivity'
STRESS_NAME = 'Stress Name'
STRESS_TYPE = 'Stress Type'
STRESS_PV_CHANGE = 'Stress PV Change'
TYPE = 'Type'
VAR_PV_CHANGE = 'VaR PV Change'
RESIDUAL = 'RESIDUAL'
TOTAL = 'Total'
TRADE_NUMBER = 'Trade Number'

PORTFOLIO_TYPES = set(['FPhysicalPortfolio', 'FCompoundPortfolio'])
TRADE_CLASS_NAME = 'FTrade'


class Header(object):
    DAYS_IN_PERIOD = {'d': 1, 'w': 7, 'y': 365}

    @staticmethod
    def horizonDays(horizon):
        "horizon should be a string e.g. '1d', '1w', '1y'."
        nDays = Header.DAYS_IN_PERIOD.get(horizon[-1], 0)
        try:
            nDays = int(horizon[:-1]) * nDays
        except:
            nDays = 0
        return nDays

    def __init__(self, reportTypes, params, version=2):
        self.reportTypes = reportTypes
        self.params = params
        self.version = version


class BaseWriter(object):
    CALCULATED_COLUMNS = {}
    MEASURES = []
    POSITION_ID = 'Position ID'
    DEFAULT_EXPORT_SUFFIX='dat'
    BOOKSTRUCTURE_PREFIX=''
    NOREPORT_HEADER = False
    TYPE_HEADER=[]
    
    @staticmethod
    def _encodeData(line):
        if sys.version_info[0] >= 3:
            return line    
        else:
            return str(line, SOURCE_ENCODING
                ).encode(TARGET_ENCODING)
    
    @staticmethod
    def _initDirs(filepath):
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    @staticmethod
    def _getPositionID(attributes):
        h = hashlib.md5(attributes.encode("utf-8"))
        return [h.hexdigest()]

    @staticmethod
    def _buildPortfolioTree(portf):
        portTree = []
        while portf:
            portTree.append(portf.Name())
            parent = portf.MemberLinks()
            if not parent:
                break
            portf = parent.First().OwnerPortfolio()
        return portTree

    @staticmethod
    def _getStringValue(posID, colID, fVal, logger):
        try:
            if isinstance(fVal, float):
                return '{0:.4f}'.format(fVal)
        except:
            pass
        strVal = str(0.0)
        try:
            if fVal is None or fVal == '':
                return str(0.0)

            if type(fVal) is str:
                if fVal.isdigit():
                    strVal = '{0:.4f}'.format(fVal)
                else:
                    strVal = '{0:.4f}'.format(float(fVal[:-3]))
            elif fVal.IsKindOf(acm.FDenominatedValue):
                val = fVal.Number()
                if math.isnan(val):
                    val = 0.
                    logger.logDebug("Value nan found at Position:{0} Column:{1}".format(posID, colID))
                strVal = '{0:.4f}'.format(val)

        except Exception as err:
            logger.logError('getStringValue err {0}'.format(str(err)))
            strVal = str(0.0)
        return strVal
    
    def _getNewFileName(self, filename, overwrite):
        dirname = os.path.dirname(filename)
        filebasename = os.path.basename(filename)
        #*****override for Theta files to write to folder for next business day*******
        runDate = acm.Time().DateNow()
        defaultCalendar = 'ZAR Johannesburg'
        nextBusDay = acm.Time.DateAdjustPeriod(runDate, '1d', defaultCalendar, 'Following') 
        if 'Theta' in filebasename and not 'PSWAP' in filebasename:
            format_dirname = dirname[:-10]
            dirname = format_dirname + str(nextBusDay)
            if not os.path.exists(dirname):
                self._logger.logInfo("**** Output folder does not exist, creating directory for Theta PL files: {0} ****".format(dirname))
                try:
                    os.mkdir(dirname)
                except Exception as e:
                    if not os.path.exists(dirname):
                        self._logger.logError("Problem creating output directory: {0}".format(str(e)))
                    else:
                        self._logger.logError("Directory already exists: {0}".format(dirname))
                        
        if filebasename.endswith(FILE_SUFFIXES):
            filebasename, suffix = filebasename.rsplit('.', 1)
        else:
            suffix =  self.__class__.DEFAULT_EXPORT_SUFFIX

        filepath = os.path.join(dirname, '{0}.{1}'.format(filebasename, suffix))
        if not os.path.exists(filepath) or overwrite:
            return filepath

        for i in range(1, MAX_FILES_IN_DIR + 1):
            f = os.path.join(dirname, '{0}{1}.{2}'.format(filebasename, i, suffix))

            if not os.path.exists(f):
                return f
        raise Exception("Maximum no. of {0} files found in {1}. Please clear "
                "out directory or allow overwrites.".format(filename, dirname))

    def __init__(self, logger, separators=DEFAULT_SEPARATORS, horizon='1d'):
        self.separators = separators
        self.horizon = horizon
        self.columnInfoTable = {}
        self.rootPositionInfoTable = {}
        self.positionInfoTable = {}
        self.output = {}
        self.attributeChain = []
        self.bookStructures = {}
        self.portfolioDepth = FMarketRiskExportAttributes.BOOK_STRUCTURE_LEVELS
        # Index of the 'portfolio' column in the attribute chain so you only
        # need to look it up once.
        self._portfolioAttributeIndex = -1
        self._positionHeader = []
        self._getPositionID = lambda x: []
        self._logger = logger

    def addColumn(self, info, ID):
        """
        This, addRootPosition(), addPosition() and addResult() are methods that
        must be provided by the writer, and are called by the
        FExportCalculatedValuesPublisher class to populate the writer with
        results.
        """
        if ID not in self.columnInfoTable and \
                info.name in self.__class__.MEASURES:
            self.columnInfoTable[ID] = info

    def addRootPosition(self, info, ID):
        if ID not in self.rootPositionInfoTable:
            self.rootPositionInfoTable[ID] = info

    def addPosition(self, info, ID):
        if ID not in self.positionInfoTable:
            self.positionInfoTable[ID] = info

    def addResult(self, posInfoID, columnInfoID, values):
        assert (posInfoID, columnInfoID) not in self.output, \
            """Assuming for now that we have not done anything like
            preallocating a place of this value."""
        assert posInfoID in self.positionInfoTable
        if columnInfoID in self.columnInfoTable:
            self.output[(posInfoID, columnInfoID)] = values

    def _initPositionFields(self, rowID):
        # You're expected to be using 'Position ID' if you're not using 'Trade
        # Number' in the Cube.
        if self.__class__.DEFAULT_EXPORT_SUFFIX == 'dat' and rowID != TRADE_NUMBER:
            self._positionHeader = [self.__class__.POSITION_ID]
            self._getPositionID = BaseWriter._getPositionID

    def _buildAttributeChain(self):
        """
        Builds the hierarchical (trade) attribute chain that defines each
        "postion" by traversing the list of PositionInformation linked nodes in
        self.positionInformationTable.
        """
        if not self.output:
            self._logger.logInfo("No results available.")
            return False

        # For the Risk Cube, we only need one, the final/leaf node in the
        # position tree/attribute chain, so that's what we'll assume for now.
        leafID = [k[0] for k in self.output.keys()][0]
        node = self.positionInfoTable[leafID]
        self._initPositionFields(node.dimensionName)
        self.attributeChain = [leafID]
        while node.parentInfoID:
            self.attributeChain.append(node.parentInfoID)
            parent = self.positionInfoTable[node.parentInfoID]
            node = parent
        # Leave out the root node.
        self.attributeChain.pop()
        return True

    def _useBookStructure(self):
        """
        Tests if there is a hierarchical book structure associated with each
        root position node, which could be a physical or compound portfolio,
        trade filter, or stored query. Only the first two are assumed to have a
        book structure.
        """

        posInfo = [self.positionInfoTable[p] for p in self.attributeChain]
        attrTypes = [p.acmDomainName for p in posInfo]
        posTypes = [p.acmDomainName
                for p in self.rootPositionInfoTable.values()]
        return (PORTFOLIO_TYPES.intersection(attrTypes) and
                PORTFOLIO_TYPES.intersection(posTypes))

    def _setPortfolioAttributeIndex(self):
        
        '''
        Need to use the attrbute name to find the portfolio index if we 
        use position specification for the grouper 
        posInfo = [self.positionInfoTable[p] for p in self.attributeChain]
        attrNames = [p.dimensionName for p in posInfo]
        
        if "Portfolio" in attrNames:
            self._portfolioAttributeIndex = attrNames.index("Portfolio")
        '''
  
        posInfo = [self.positionInfoTable[p] for p in self.attributeChain]
        attrTypes = [p.acmDomainName for p in posInfo]
        for t in list(PORTFOLIO_TYPES):
            if t not in attrTypes:
                continue
            self._portfolioAttributeIndex = attrTypes.index(t)
            if self._portfolioAttributeIndex > -1:
                break
        assert self._portfolioAttributeIndex > -1, ("Shouldn't have been "
                "called")

    def _getPortfolio(self, posID):
        posName = self._getAttributeValues(posID)[
                self._portfolioAttributeIndex]
        domain = self.positionInfoTable[posID].acmDomainName
        if domain == 'int' or domain == 'seqnbr':
            trade = acm.FTrade[posName]
            if trade:
                return trade.Portfolio()
            portfolio = acm.FPhysicalPortfolio[posName]
            if portfolio:
                return portfolio
        elif domain =='id':
            return acm.FPhysicalPortfolio[posName]
        elif domain.startswith('string'):
            return acm.FPhysicalPortfolio[posName]
        else:
            return acm.GetDomain(domain)[posName]

    def _buildBookStructure(self):
        if not self._useBookStructure():
            return {}
        
        self._setPortfolioAttributeIndex()
        
        portTrees = []
        positions = set([nodeKey[0] for nodeKey in self.output.keys()])
        for posID in positions:
            portf = self._getPortfolio(posID)
            pTree = self._buildPortfolioTree(portf)
            portTrees.append(pTree)

        for pt in portTrees:
            name = pt[0]
            branch = list(reversed(pt))
            fill = self.portfolioDepth - len(pt)
            self.bookStructures[name] = branch + fill * [branch[-1]]
        return self.bookStructures

    def _buildReportStructure(self):
        """
        Builds the column structure of the report - chain of trade attributes
        and portfolio book structure if requested.
        """
        if not self._buildAttributeChain():
            return False
        self._buildBookStructure()
        return True

    def _getBookStructureHeaders(self, headers):
        if not self.bookStructures:
            return []
        # Leave out the "Portfolio" column when we export to Memory risk cube
        if self.__class__.DEFAULT_EXPORT_SUFFIX == 'dat':
            headers.pop(self._portfolioAttributeIndex)
        bookStructureStr = FMarketRiskExportAttributes.BOOK_STRUCTURE_STRING
        if self.__class__.BOOKSTRUCTURE_PREFIX:
            bookStructureStr = '{0}.{1}'.format(self.__class__.BOOKSTRUCTURE_PREFIX, FMarketRiskExportAttributes.BOOK_STRUCTURE_STRING)
        bookStructureHeaders = [
            bookStructureStr + '{0}'.format(i+1)
                for i in range(self.portfolioDepth)]
        return bookStructureHeaders

    def _getBookStructure(self, posID, attributes):
        if not self.bookStructures:
            return []
        assert self._portfolioAttributeIndex > -1
        portfName = attributes[self._portfolioAttributeIndex]
        # Leave out the "Portfolio" column when we export to Memory risk cube
        if self.__class__.DEFAULT_EXPORT_SUFFIX == 'dat':
            attributes.pop(self._portfolioAttributeIndex)
        if not portfName:
            return []
        return self.bookStructures[portfName]

    def _getAttributeValues(self, posID):
        node = self.positionInfoTable[posID]
        attributes = [node.name]
        while node.parentInfoID:
            parent = self.positionInfoTable[node.parentInfoID]
            attributes.append(parent.name)
            node = parent
        # Leave out the root node.
        attributes.pop()
        attributes = ['' if 'No Trade' in attr else attr for attr in attributes]
        #attributes = map(lambda x: '' if 'No Trade' in x else x, attributes)
        return attributes

    def _createReportHeader(self):
        raise NotImplementedError("To be implemented in subclasses")

    def _getCalculatedColumnHeaders(self):
        return [c.name for c in self.columnInfoTable.values()]

    def _getSingleValue(self, posID, colID, valObj):
        assert len(valObj) == 1 and not valObj[0].projectionCoordinates, (
                "Override in {0} for multi-valued results.".format(
                    self.__class__.__name__))
        return BaseWriter._getStringValue(posID, colID, valObj[0].values, self._logger)

    def _getCalculatedValues(self, posID):
        calcs = []
        for colID in self.columnInfoTable.keys():
            calcs.append(self._getSingleValue(posID, colID, self.output[(posID, colID)]))
        return calcs

    def _writeReportHeader(self, fp, header):
        """
        Writes the relatively static first 4-5 lines of each report based on
        the Header object created in _createReportHeader().

        That method is expected to be implemented in each subclass.
        """
        if not header:
            return

        sep0, sep1 = self.separators
        print('v{0:02d}'.format(header.version), file=fp)
        print('{0}'.format(''.join(self.separators)), file=fp)
        count = str(header.params.get(COLUMN_COUNT, 1))
        print('{0}'.format(sep0.join([sep0.join([report, count])
            for report in header.reportTypes])), file=fp)
        print('{0}'.format(header.params.get(DESCRIPTION, '')), file=fp)
        print('{0}'.format(header.params.get(HEADER_FORMAT, '')), file=fp)
        print('{0}'.format(header.params.get(DATA_FORMAT, '')), file=fp)

    def _writeDataHeader(self, fp):
        """
        Writes the column headings. Expected structure is grouped into:

        <Trade Attributes>|...|<Book Structure>|...|<Calculated Values>|...

        """
        typeheader = self.__class__.TYPE_HEADER
        attributeHeaders = [self.positionInfoTable[p].dimensionName
            for p in self.attributeChain]

        if self.__class__.DEFAULT_EXPORT_SUFFIX == 'csv':
            attributesWithTradePrefix = []
            attributesStr = FBDPCommon.valueFromFParameter(
                'FArtiQMarketExportParameters', 'AttributesWithTradePrefix')
            if attributesStr:
                attributesWithTradePrefix = [i.strip() for i in attributesStr.split(',')]
            newAttrHeaders = ["Trade." + attr if attr in attributesWithTradePrefix else attr for attr in attributeHeaders]
            if newAttrHeaders:
                newAttrHeaders = ["Trade.Instrument Name" if x == "Trade.Instrument" else x for x in newAttrHeaders]
                replace = "Trade.Reference"
                if replace not in newAttrHeaders:
                    if "Trade.Trade No" in newAttrHeaders:
                        newAttrHeaders = ["Trade.Reference" if x == "Trade.Trade No" else x for x in newAttrHeaders] 
                    elif "Trade.Instrument Name" in newAttrHeaders:
                        index = newAttrHeaders.index("Trade.Instrument Name")
                        newAttrHeaders[index] = replace
                attributeHeaders = newAttrHeaders

        bookStructureHeaders = self._getBookStructureHeaders(attributeHeaders)
        columnHeaders = self._getCalculatedColumnHeaders()
        header = self.separators[0].join(typeheader
                + self._positionHeader
                + attributeHeaders
                + bookStructureHeaders
                + columnHeaders)
        print('{0}'.format(header), file=fp)

    def _writeDataRows(self, fp):
        """
        Writes the actual data rows (whaddaya know!).
        """

        positions = set([nodeKey[0] for nodeKey in self.output.keys()])
        for posID in sorted(positions):
            attrs = self._getAttributeValues(posID)
            bs = self._getBookStructure(posID, attrs)
            rowID = self._getPositionID(str(attrs + bs))
            calcs = self._getCalculatedValues(posID)
            line = self.separators[0].join(rowID + attrs + bs + calcs)
            line = self._encodeData(line)
            print(line, file=fp)

    def dump(self, filepath=r'C:\Temp\RiskExport\Export.log'):
        """
        Debugging function for dumping out "raw" values returned by
        ExportCalculatedValues.
        """
        try:
            BaseWriter._initDirs(filepath)
            with open(filepath, 'w') as fp:
                print("Columns", file=fp)
                print(len('Columns') * '=' + '\n', file=fp)
                for colID in sorted(self.columnInfoTable.keys()):
                    print(colID, file=fp)
                    col = self.columnInfoTable[colID]
                    print(col, file=fp)
                    scenarios = col.scenarioInformation
                    print(scenarios, file=fp)
                    if scenarios:
                        print("No. of sub-columns:", len(
                                col.columnPartNames), file=fp)
                        print("No. of dimension names: {0}\n".format(
                                len(scenarios.dimensionNames)), file=fp)
                    print(80 * '-', file=fp)
                print(80 * '=', file=fp)
                for (posID, colID) in sorted(self.output.keys()):
                    print("Column:", file=fp)
                    print(colID, file=fp)
                    print("Position:", file=fp)
                    print(posID, file=fp)
                    print("\nResults:" + '\n', file=fp)
                    for res in self.output[(posID, colID)]:
                        print(res, file=fp)
                    print('\n' + 80 * '-', file=fp)
                print(80 * '=', file=fp)
        except Exception as err:
            tb = inspect.getframeinfo(inspect.trace()[-1][0])
            self._logger.logInfo("{2}.{3}() line {4}: {0} - {1}.".format(type(err).__name__,
                    err, tb.filename, tb.function, tb.lineno))

    def write_parts_to_file(self, fp):
        if not self.__class__.NOREPORT_HEADER:
            header = self._createReportHeader()
            self._writeReportHeader(fp, header)
        self._writeDataHeader(fp)
        self._writeDataRows(fp)

    def _validProperties(self):
        attrHeads = [self.positionInfoTable[p].dimensionName
                for p in self.attributeChain]
        bsHeads = self._getBookStructureHeaders(attrHeads)
        heads = attrHeads + bsHeads
        positions = set([nodeKey[0] for nodeKey in self.output.keys()])

        for posID in sorted(positions):
            attrVals = self._getAttributeValues(posID)
            bsVals = self._getBookStructure(posID, attrVals)
            vals = attrVals + bsVals
            for (val, head) in zip(vals, heads):
                if any([sep in val for sep in self.separators]):
                    self._logger.logError("Attribute {0}: {1} should not "
                            "contain any separator characters {2}.".format(
                                head, val, self.separators))
                    return False
        return True


    def write(self, overwrite, filepath=r'C:\Temp\RiskExport\Export.txt'):
        """
        Writes the output in Risk Cube format in several parts - report header,
        data header, data rows.
        """

        if not (self._buildReportStructure() and self._validProperties()):
            return

        BaseWriter._initDirs(filepath)
        filename = self._getNewFileName(filepath, overwrite)
        id_ = int(hashlib.md5(filename.encode("utf-8")).hexdigest(), 16)
        try:
            with open(filename, 'w') as fp:
                if not self.__class__.NOREPORT_HEADER:
                    header = self._createReportHeader()
                    self._writeReportHeader(fp, header)
                self._writeDataHeader(fp)
                self._writeDataRows(fp)
            self._logger.logInfo("{0} successfully exports into file {1}".format(self.__class__.__name__, filename))
            self._logger.summaryAddOk("File", id_, "Export")
        except Exception as err:
            tb = inspect.getframeinfo(inspect.trace()[-1][0])
            self._logger.logInfo("{2}.{3}() line {4}: {0} - {1}.".format(
                type(err).__name__, err, tb.filename, tb.function, tb.lineno))
            self._logger.logError("{0} failed to export to file {1}".format(self.__class__.__name__, filename))
            self._logger.summaryAddFail("File", id_, "Export", [str(err)])


class MarketValueWriter(BaseWriter):
    REPORT_TYPES = ["Market Value"]
    # Dictionary of column names in output files to ColumnCreator names Prime.
    MEASURES = ["Market Value"]
    DEFAULT_EXPORT_SUFFIX='dat'


    def _createReportHeader(self):
        seps = self.separators
        nDays = Header.horizonDays(self.horizon)
        headerFormat = seps[0].join([
            HORIZON_PARAM, self.horizon,
            HORIZON_DAYS_PARAM, str(nDays)])
        return Header(self.__class__.REPORT_TYPES,
                {COLUMN_COUNT: 1, HEADER_FORMAT: headerFormat})

class ArtiQMarketValueWriter(MarketValueWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True

class ThetaWriter(BaseWriter):
    REPORT_TYPES = [THETA]
    MEASURES = [THETA]
    DEFAULT_EXPORT_SUFFIX='dat'

    def _createReportHeader(self):
        seps = self.separators
        nScenarios = 1
        nDays = Header.horizonDays(self.horizon)
        headerFormat = seps[0].join([
            HORIZON_PARAM, self.horizon,
            HORIZON_DAYS_PARAM, str(nDays),
            STRESS_TYPE, 'Standard',
            CURVE_DATE, acm.Time.DateToday(),
            MONEYNESS, "1.0",
            STRESS_NAME, THETA])
        dataFormat = seps[0].join(
                [self.__class__.MEASURES[0], str(nScenarios)])

        return Header(self.__class__.REPORT_TYPES,
                {COLUMN_COUNT: 1,
                DESCRIPTION: 'Stress Scenario',
                HEADER_FORMAT: headerFormat,
                DATA_FORMAT: dataFormat})

class ArtiQThetaWriter(ThetaWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True

class ProfitAndLossWriter(BaseWriter):
    REPORT_TYPES = ["Profit and Loss"]
    MEASURES = ["Total", "Hypothetical", "DailyTotal"]
    DEFAULT_EXPORT_SUFFIX ='dat'
    
    def __init__(self, logger, separators=DEFAULT_SEPARATORS, horizon='1d', columns=[]):
        super(ProfitAndLossWriter, self).__init__(logger, separators, horizon)
        self._columns = (columns if columns
                else ProfitAndLossWriter.MEASURES)

    def addColumn(self, info, ID):
        if info.name in self._columns:
            self.columnInfoTable[ID] = info

    def _createReportHeader(self):
        seps = self.separators
        nDays = Header.horizonDays(self.horizon)
        headerFormat = seps[0].join([
            HORIZON_PARAM, self.horizon,
            HORIZON_DAYS_PARAM, str(nDays),
            CURVE_DATE, acm.Time.DateToday(),
            MONEYNESS, "1.0"])
        nScenarios = len(self.columnInfoTable.keys())
        dataFormat = seps[0].join([self.__class__.REPORT_TYPES[0],
            str(nScenarios), PL_SOURCE])
        return Header(self.__class__.REPORT_TYPES,
                {COLUMN_COUNT: nScenarios,
                    DESCRIPTION: 'Factor',
                    HEADER_FORMAT: headerFormat,
                    DATA_FORMAT: dataFormat})

    def _getCalculatedColumnHeaders(self):
        return (self.__class__.REPORT_TYPES +
                super(ProfitAndLossWriter, self)._getCalculatedColumnHeaders())

    def _getCalculatedValues(self, posID):
        calcs = super(ProfitAndLossWriter, self)._getCalculatedValues(posID)
        return [''] * len(self.__class__.REPORT_TYPES) + calcs


class ArtiQProfitAndLossWriter(ProfitAndLossWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    TYPE_HEADER=["P&L Source"]
    
    def _getCalculatedColumnHeaders(self):
        return self.__class__.REPORT_TYPES

    def _getCalculatedValues(self, posID, colID):
        return self._getSingleValue(posID, colID, self.output[(posID, colID)])
        
    def _writeDataRows(self, fp):
        for colID in self.columnInfoTable.keys():
            positions = set([nodeKey[0] for nodeKey in self.output.keys()])
            for posID in sorted(positions):
                attrs = self._getAttributeValues(posID)
                bs = self._getBookStructure(posID, attrs)
                rowID = self._getPositionID(str(attrs + bs))
                calcs = self._getCalculatedValues(posID, colID)
                line = self.separators[0].join([colID] + rowID + attrs + bs + [calcs])
                line = self._encodeData(line)
                print(line, file=fp)
