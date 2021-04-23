""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FRiskCubeScenarioWriters.py"
from __future__ import print_function
from collections import defaultdict


"""---------------------------------------------------------------------------
MODULE
    FRiskCubeScenarioWriters - Classes to receive results.
    Writers for scenario-type output e.g. VaR, risk factor sensitivities etc.

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

---------------------------------------------------------------------------"""
import re
import itertools
import math
import time
import acm
from functools import reduce
from FRiskCubeWriterBase import *
import functools
import FMarketRiskExportUtil
import FBDPCommon
import ast

LINE_COUNT = 200
MAX_CALC_TIME = 10

class BaseScenarioWriter(BaseWriter):
    def _countScenarios(self):
        scenarios = [col.scenarioInformation
                for col in self.columnInfoTable.values()
                if col.scenarioInformation]
        dimensions = [s.dimensionCardinalities for s in scenarios]
        products = [reduce(lambda x, y: x*y, dims) for dims in dimensions]
        return sum(products)

    def addColumn(self, info, ID):
        self.columnInfoTable[ID] = info

    def addPosition(self, info, ID):
        self.positionInfoTable[ID] = info

class SpotVolWriter(BaseScenarioWriter):
    REPORT_TYPES = ['Stress']
    SCENARIO_TYPES = (PRICE_BUMP, VOL_BUMP)
    STRESS_TYPE = "Grid"
    SHIFT_TYPES = {acm.FSymbol('market price'): PRICE_BUMP,
            acm.FSymbol('volatility value'): VOL_BUMP,
            acm.FSymbol('volatility information'): VOL_BUMP}
    DEFAULT_EXPORT_SUFFIX ='dat'

    @staticmethod
    def _getReportName():
        return "Spot and Volatility Grid"

    def __init__(self, scenario, stressName, logger,
                separators=DEFAULT_SEPARATORS, horizon='1d'):
        super(SpotVolWriter, self).__init__(logger, separators, horizon)
        self._scenario = scenario
        self._stressName = self._getReportName()
        if stressName:
            self._stressName = stressName

    def _getVolShiftsFromScenario(self):
        dimensions = self._scenario.ShiftDimensions()
        factor = ''
        for i, dim in enumerate(dimensions):
            vectors = dim.ShiftVectors()
            for v in vectors:
                if v.Function() == 'shiftVolatilityPeriods':
                    factors = v[0].Parameters().At(acm.FSymbol('factors'))
                    return str(float(factors[0]) * 100 - 100)
        assert factor, "Require Shift Volatility Periods."

    def _createReportHeader(self):
        seps = self.separators
        headerFormat = seps[0].join([
            "{0} Name".format(self.__class__.REPORT_TYPES[0]),
            self._stressName,
            "{0} Type".format(self.__class__.REPORT_TYPES[0]),
            self.__class__.STRESS_TYPE,
            CURVE_DATE, acm.Time.DateToday(),
            MONEYNESS, "1.0"])
        nScenarios = self._countScenarios()
        column = list(self.columnInfoTable.values())[0]
        assert column.scenarioInformation, ("{0}: Scenarios must be defined "
                "on column {1}.".format(self.__class__.__name__, column.name))
        shiftTypes = seps[1].join(column.scenarioInformation.dimensionNames)
        dataFormat = seps[0].join([STRESS_PV_CHANGE, str(nScenarios),
            shiftTypes])

        return Header(self.__class__.REPORT_TYPES,
                {COLUMN_COUNT: nScenarios,
                    DESCRIPTION: "Stress Scenario",
                    HEADER_FORMAT: headerFormat,
                    DATA_FORMAT: dataFormat})

    def _getSubHeads(self, subHeadings):
        return [self.separators[1].join(
                s.strip('%').strip() for s in subHeading.split(','))
                for subHeading in subHeadings]

    def _getCalculatedColumnHeaders(self):
        headers = []
        sep = self.separators[1]
        for col in self.columnInfoTable.values():
            assert col.scenarioInformation, ("Override in {0} for "
                    "non-scenario or combination results.".format(
                        self.__class__.__name__))
            subHeads = self._getSubHeads(col.columnPartNames)
            headers.extend([col.name] + subHeads)
        return headers

    def _getCalculatedValues(self, posID):
        calcs = []
        for colID, colInfo in self.columnInfoTable.items():
            total = reduce(lambda x, y: x*y,
                    colInfo.scenarioInformation.dimensionCardinalities)
            scenarioVals = self.output[(posID, colID)]
            assert len(scenarioVals) == total, ("{2}: Expecting {0} scenario"
                    " values {0}. Got {1}.".format(total, len(scenarioVals),
                        self.__class__.__name__))
            # For the column descriptor in the data header, see above.
            vals = ['']
            for valObj in scenarioVals:
                vals.append(BaseWriter._getStringValue(
                    self._getAttributeValues(posID), colID, valObj.values, self._logger))
            calcs.extend(vals)
        return calcs

class ArtiQSpotVolWriter(SpotVolWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    TYPE_HEADER=["Factor.ID"]
    
    def _getCalculatedColumnHeaders(self):
        return [c.name for c in self.columnInfoTable.values()]
        
    def _getCalculatedValues(self, posID):
        calcs = []
        for colID, colInfo in self.columnInfoTable.items():
            total = reduce(lambda x, y: x*y,
                    colInfo.scenarioInformation.dimensionCardinalities)
            scenarioVals = self.output[(posID, colID)]
            assert len(scenarioVals) == total, ("{2}: Expecting {0} scenario"
                    " values {0}. Got {1}.".format(total, len(scenarioVals),
                        self.__class__.__name__))
            # For the column descriptor in the data header, see above.
            vals = []
            for valObj in scenarioVals:
                vals.append(BaseWriter._getStringValue(
                    self._getAttributeValues(posID), colID, valObj.values, self._logger))
            
            calcs.append(';'.join(vals))
        return calcs
    
    def _writeDataRows(self, fp):
        reportname = self._getReportName()
        positions = set([nodeKey[0] for nodeKey in self.output.keys()])
        for posID in sorted(positions):
            attrs = self._getAttributeValues(posID)
            bs = self._getBookStructure(posID, attrs)
            rowID = self._getPositionID(str(attrs + bs))
            calcs = self._getCalculatedValues(posID)
            line = self.separators[0].join([reportname] + rowID + attrs + bs + calcs)
            line = self._encodeData(line)
            print(line, file=fp)

class SpotVolTaperWriter(SpotVolWriter):
    REPORT_TYPES = ['Stress']
    SCENARIO_TYPES = (PRICE_BUMP, VOL_BUMP)
    STRESS_TYPE = "Grid"
    SHIFT_TYPES = {acm.FSymbol('market price all'): PRICE_BUMP,
            acm.FSymbol('market price'): PRICE_BUMP,
            acm.FSymbol('volatility value'): VOL_BUMP,
            acm.FSymbol('volatility information'): VOL_BUMP}
    DEFAULT_EXPORT_SUFFIX ='dat'
    
    @staticmethod
    def _getReportName():
        return "Spot and Volatility Taper"

    def _getSubHeads(self, subHeadings):
        subHeadings_new = [s.replace(
                    'Volatility Shifts', self._getVolShiftsFromScenario())
                    for s in subHeadings]
        return [self.separators[1].join(
                s.strip('%').strip() for s in subHeading.split(','))
                for subHeading in subHeadings_new]

class ArtiQSpotVolTaperWriter(SpotVolTaperWriter, ArtiQSpotVolWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True

    def _getCalculatedColumnHeaders(self):
        return ArtiQSpotVolWriter._getCalculatedColumnHeaders(self)

    def _getCalculatedValues(self, posID):
        return ArtiQSpotVolWriter._getCalculatedValues(self, posID)

    def _writeDataRows(self, fp):
        return ArtiQSpotVolWriter._writeDataRows(self, fp)

class IRVolWriter(SpotVolWriter):
    REPORT_TYPES = ['Stress']
    SCENARIO_TYPES = (PRICE_BUMP, VOL_BUMP)
    STRESS_TYPE = "Grid"
    SHIFT_TYPES = {acm.FSymbol('yield curve'): PRICE_BUMP,
            acm.FSymbol('volatility value'): VOL_BUMP,
            acm.FSymbol('volatility information'): VOL_BUMP}
    DEFAULT_EXPORT_SUFFIX ='dat'

    @staticmethod
    def _getReportName():
        return "IR and Volatility Grid"

class ArtiQIRVolWriter(IRVolWriter, ArtiQSpotVolWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    
    def _getCalculatedColumnHeaders(self):
        return ArtiQSpotVolWriter._getCalculatedColumnHeaders(self)

    def _getCalculatedValues(self, posID):
        return ArtiQSpotVolWriter._getCalculatedValues(self, posID)

    def _writeDataRows(self, fp):
        return ArtiQSpotVolWriter._writeDataRows(self, fp)

class FXVolWriter(SpotVolWriter):
    REPORT_TYPES = ['Stress']
    SCENARIO_TYPES = (PRICE_BUMP, VOL_BUMP)
    STRESS_TYPE = "Grid"
    SHIFT_TYPES = {acm.FSymbol('fx matrix'): PRICE_BUMP,
            acm.FSymbol('volatility value'): VOL_BUMP,
            acm.FSymbol('volatility information'): VOL_BUMP}
    DEFAULT_EXPORT_SUFFIX ='dat'

    @staticmethod
    def _getReportName():
        return "FX and Volatility Grid"

    def _getSubHeads(self, subHeadings):
        return [s.split(' ')[0].strip() + self.separators[1] + s.split(' ')[2]
                for s in subHeadings]

class ArtiQFXVolWriter(FXVolWriter, ArtiQSpotVolWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    
    def _getCalculatedColumnHeaders(self):
        return ArtiQSpotVolWriter._getCalculatedColumnHeaders(self)

    def _getCalculatedValues(self, posID):
        return ArtiQSpotVolWriter._getCalculatedValues(self, posID)

    def _writeDataRows(self, fp):
        return ArtiQSpotVolWriter._writeDataRows(self, fp)

class FXVolTaperWriter(SpotVolWriter):
    REPORT_TYPES = ['Stress']
    SCENARIO_TYPES = (PRICE_BUMP, VOL_BUMP)
    STRESS_TYPE = "Grid"
    SHIFT_TYPES = {acm.FSymbol('fx matrix'): PRICE_BUMP,
            acm.FSymbol('volatility value'): VOL_BUMP,
            acm.FSymbol('volatility information'): VOL_BUMP}
    DEFAULT_EXPORT_SUFFIX ='dat'
    
    @staticmethod
    def _getReportName():
        return "FX and Volatility Taper"

    def _getSubHeads(self, subHeadings):
        subHeadings_new = []
        for subHeading in subHeadings:
            non_decimal = re.compile(r'[^\d.,-]+')
            subHeading = subHeading.replace('Volatility Shifts',
                    self._getVolShiftsFromScenario())
            subHeading = non_decimal.sub('', subHeading)
            subHeading = subHeading.replace(',', self.separators[1])
            subHeadings_new.append(subHeading)
        return subHeadings_new

class ArtiQFXVolTaperWriter(FXVolTaperWriter, ArtiQSpotVolWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    
    def _getCalculatedColumnHeaders(self):
        return ArtiQSpotVolWriter._getCalculatedColumnHeaders(self)

    def _getCalculatedValues(self, posID):
        return ArtiQSpotVolWriter._getCalculatedValues(self, posID)

    def _writeDataRows(self, fp):
        return ArtiQSpotVolWriter._writeDataRows(self, fp)
        
class FXMatrixWriter(SpotVolWriter):
    SCENARIO_TYPES = ("Bump Ladder",)
    STRESS_TYPE = "Ladder"
    SHIFT_TYPES = {acm.FSymbol('fx matrix'): BUMP_LADDER}
    GROUPNAME = "FX"
    TYPE = "Type"
    TYPENAME = "FxRate"
    ID = "ID"
    DEFAULT_EXPORT_SUFFIX ='dat'

    def __init__(self, scenario, stressName, logger,
                separators=DEFAULT_SEPARATORS, horizon='1d'):
        super(SpotVolWriter, self).__init__(logger, separators, horizon)
        self._scenario = scenario

    @staticmethod
    def _getSubHeads(subHeadings):
        return [s.split(' ')[0].strip() for s in subHeadings]

    def _getReportName(self):
        cols = [col.columnPartNames for col in self.columnInfoTable.values()]
        cols = list(itertools.chain.from_iterable(cols))
        currencies = list(set([c.split(' ')[-1].strip() for c in cols]))
        if len(currencies) != 1:
            self._logger.logWarning("Multiple currencies {0} found for FX "
                    "scenarios. Using the first: {1}.".format(currencies,
                        currencies[0]))
        self.scenarioCurr = currencies[0]
        return "{0} FX Spot".format(currencies[0])

    def _createReportHeader(self):
        seps = self.separators
        headerFormat = seps[0].join([
            "{0} Name".format(self.__class__.REPORT_TYPES[0]),
            self._getReportName(),
            "{0} Type".format(self.__class__.REPORT_TYPES[0]),
            self.__class__.STRESS_TYPE,
            GROUP, self.__class__.GROUPNAME,
            self.__class__.TYPE, self.__class__.TYPENAME,
            self.__class__.ID, self.scenarioCurr,
            CURVE_DATE, acm.Time.DateToday(),
            MONEYNESS, "1.0"])
        nScenarios = self._countScenarios()
        column = list(self.columnInfoTable.values())[0]
        assert column.scenarioInformation, ("{0}: Scenarios must be defined "
                "on column {1}.".format(self.__class__.__name__, column.name))
        shiftTypes = seps[1].join(column.scenarioInformation.dimensionNames)
        dataFormat = seps[0].join([STRESS_PV_CHANGE, str(nScenarios),
            shiftTypes])

        return Header(self.__class__.REPORT_TYPES,
                {COLUMN_COUNT: nScenarios,
                    DESCRIPTION: "Stress Scenario",
                    HEADER_FORMAT: headerFormat,
                    DATA_FORMAT: dataFormat})

class ArtiQFXMatrixWriter(FXMatrixWriter, ArtiQSpotVolWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    
    def _getCalculatedColumnHeaders(self):
        return ArtiQSpotVolWriter._getCalculatedColumnHeaders(self)

    def _getCalculatedValues(self, posID):
        return ArtiQSpotVolWriter._getCalculatedValues(self, posID)
    
    def _writeDataRows(self, fp):
        return ArtiQSpotVolWriter._writeDataRows(self, fp)

class VegaWriter(BaseScenarioWriter):
    REPORT_TYPES = ["Sensitivity"]
    MEASURES = [DELTA]
    SCENARIO_TYPES = ["Group", "TOTAL"]
    DELTA_TYPE = 'Vol'
    DEFAULT_EXPORT_SUFFIX ='dat'

    def _createReportHeader(self):
        seps = self.separators
        nCols = sum([len(colInfo.columnPartNames) for colInfo in self.columnInfoTable.values()])
        headerFormat = seps[0].join(self.__class__.SCENARIO_TYPES
                + [CURVE_DATE, acm.Time.DateToday(),
                    MONEYNESS, "1.0",
                    STRESS_TYPE, 'Standard',
                    TYPE, self.DELTA_TYPE,])
        dataFormat = seps[0].join([DELTA, str(nCols)])
        return Header(self.__class__.REPORT_TYPES,
                {COLUMN_COUNT: nCols,
                    HEADER_FORMAT: headerFormat,
                    DATA_FORMAT: dataFormat})

    def _getCalculatedColumnHeaders(self):
        return [DELTA]

    def _getCalculatedValues(self, posID):
        calcs = super(VegaWriter, self)._getCalculatedValues(posID)
        return calcs

class ArtiQVegaWriter(VegaWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    
class GreekWriter(BaseScenarioWriter):
    REPORT_TYPES = ["Sensitivity"]
    MEASURES = [DELTA]
    SCENARIO_TYPES = ["Group", "TOTAL"]
    DELTA_TYPE = 'Vol'
    DEFAULT_EXPORT_SUFFIX ='dat'

    def __init__(self, measures, columnNames, logger,
                separators=DEFAULT_SEPARATORS, horizon='1d'):
        super(GreekWriter, self).__init__(logger, separators, horizon)
        self.measures = measures
        self.columnNames = columnNames

    def _createReportHeader(self):
        seps = self.separators
        nCols = sum([len(colInfo.columnPartNames) for colInfo in self.columnInfoTable.values()])
        headerFormat = seps[0].join(self.__class__.SCENARIO_TYPES
                + [CURVE_DATE, acm.Time.DateToday(),
                    MONEYNESS, "1.0",
                    STRESS_TYPE, 'Standard',
                    TYPE, self.DELTA_TYPE,])
        dataFormat = seps[0].join([DELTA, str(nCols)])
        return Header(self.__class__.REPORT_TYPES,
                {COLUMN_COUNT: nCols,
                    HEADER_FORMAT: headerFormat,
                    DATA_FORMAT: dataFormat})

    def _getCalculatedColumnHeaders(self):
        return list(self.measures)

    def _getCalculatedValues(self, posID, colID):
        return self._getSingleValue(posID, colID, self.output[(posID, colID)])
    
    def _writeDataRows(self, fp):
        raise NotImplementedError("Not implemented in GreekWriter")

class ArtiQGreekWriter(GreekWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    TYPE_HEADER=[]
    
    def __init__(self, measures, columnNames, logger,
                separators=DEFAULT_SEPARATORS, horizon='1d'):
        super(ArtiQGreekWriter, self).__init__(measures, columnNames, logger, separators, horizon)
        self._columnMeasureMap = {}
        for measure, colName in zip(measures, columnNames):
            self._columnMeasureMap[colName] = measure 

    
    def _getCalculatedValues(self, posID):
        columnValues = {}
        for colID, colInfo in self.columnInfoTable.items():
            value = self._getSingleValue(posID, colID, self.output[(posID, colID)])
            columnValues[colID] = value

        calcs = []
        for m in self.measures:
            for k, v in self._columnMeasureMap.items():
                if m == v:
                    if k not in columnValues:
                        raise Exception("The column {0} not found in the calculated values.".format(k))
                    calcs.append(columnValues[k])
        return calcs

    def _writeDataRows(self, fp):
        positions = set([nodeKey[0] for nodeKey in self.output.keys()])
        for posID in sorted(positions):
            attrs = self._getAttributeValues(posID)
            bs = self._getBookStructure(posID, attrs)
            rowID = self._getPositionID(str(attrs + bs))
            calcs = self._getCalculatedValues(posID)
            #change to have a one line for muliple measures
            line = self.separators[0].join(rowID + attrs + bs + calcs)
            line = self._encodeData(line)
            print(line, file=fp)


class CreditDeltaWriter(VegaWriter):
    DELTA_TYPE = 'Credit'
    DEFAULT_EXPORT_SUFFIX ='dat'
    
class ArtiQCreditDeltaWriter(CreditDeltaWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    
class IRDeltaWriter(BaseScenarioWriter):
    REPORT_TYPES = ["Sensitivity"]
    MEASURES = [DELTA]
    SCENARIO_TYPES = ["Group", "INTEREST RATE"]
    STRESS_NAME = "Parallel Shift"
    NAME = 'Stress Name'
    DEFAULT_EXPORT_SUFFIX ='dat'
    
    def __init__(self, stressName, logger,
                separators=DEFAULT_SEPARATORS, horizon='1d'):
        super(IRDeltaWriter, self).__init__(logger, separators, horizon)
        self._stressName = self.__class__.STRESS_NAME
        if stressName:
            self._stressName = stressName

    def _createReportHeader(self):
        seps = self.separators
        nCols = sum([len(colInfo.columnPartNames) for colInfo in self.columnInfoTable.values()])
        headerFormat = seps[0].join(self.__class__.SCENARIO_TYPES
                + [CURVE_DATE, acm.Time.DateToday(),
                    MONEYNESS, "1.0",
                    STRESS_TYPE, 'Standard',])
        dataFormat = seps[0].join([DELTA, str(nCols), seps[1].join([CURVE_ID,
            self.__class__.NAME,])])
        return Header(self.__class__.REPORT_TYPES,
                {COLUMN_COUNT: nCols,
                    HEADER_FORMAT: headerFormat,
                    DATA_FORMAT: dataFormat})

    def _getCalculatedColumnHeaders(self):
        heads = [self.separators[1].join([c.name, self._stressName])
                for c in self.columnInfoTable.values()]
        return [DELTA] + heads

    def _getCalculatedValues(self, posID):
        calcs = super(IRDeltaWriter, self)._getCalculatedValues(posID)
        return [''] + calcs

class ArtiQIRDeltaWriter(IRDeltaWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    TYPE_HEADER=["Factor.ID", "Factor.Name", "Factor.Type"]
    
    def _getCalculatedColumnHeaders(self):
        return [DELTA] 
    
    def _getCalculatedValues(self, posID, colID):
        return self._getSingleValue(posID, colID, self.output[(posID, colID)])
        
    def _writeDataRows(self, fp):
        #for col in self.columnInfoTable.values():
        for colID in self.columnInfoTable.keys():
            positions = set([nodeKey[0] for nodeKey in self.output.keys()])
            for posID in sorted(positions):
                attrs = self._getAttributeValues(posID)
                bs = self._getBookStructure(posID, attrs)
                rowID = self._getPositionID(str(attrs + bs))
                calcs = self._getCalculatedValues(posID, colID)
                line = self.separators[0].join([colID] + [colID] + [self._stressName] + rowID + attrs + bs + [calcs])
                line = self._encodeData(line)
                print(line, file=fp)    
 
class ArtiQIRParallelShiftWriter(ArtiQIRDeltaWriter):
    TYPE_HEADER=["Factor.Name", "Factor.Type"]
    
    def __init__(self, measurement, logger,
                separators=DEFAULT_SEPARATORS, horizon='1d'):
        super(ArtiQIRParallelShiftWriter, self).__init__(logger, separators, horizon)
        self._measurement = measurement

    def _getCalculatedColumnHeaders(self):
        return [self._measurement]
        
    def _getCalculatedValues(self, posID, colID):
        return self._getSingleValue(posID, colID, self.output[(posID, colID)])
        
    def _writeDataRows(self, fp):
        for colID, colInfo in self.columnInfoTable.items():
            positions = set([nodeKey[0] for nodeKey in self.output.keys()])
            for posID in sorted(positions):
                attrs = self._getAttributeValues(posID)
                bs = self._getBookStructure(posID, attrs)
                rowID = self._getPositionID(str(attrs + bs))
                calcs = self._getCalculatedValues(posID, colID)
                columnDetails = colInfo.name.split(":")
                columnName = columnDetails
                factorName = columnDetails
                if len(columnDetails) == 2:
                    columnName = columnDetails[0]
                    factorName = columnDetails[1]
                line = self.separators[0].join([factorName] + [self._stressName] + rowID + attrs + bs + [calcs])
                line = self._encodeData(line)
                print(line, file=fp)    
 
class IRBucketDeltaWriter(IRDeltaWriter):
    MEASURES = [DELTA]
    NAME = 'Tenor'
    STRESS_NAME = "Time Bucket Shift"
    DEFAULT_EXPORT_SUFFIX ='dat'
     
    def _createReportHeader(self):
        seps = self.separators
        nCols = sum([len(colInfo.columnPartNames) for colInfo in self.columnInfoTable.values()])
        headerFormat = seps[0].join(self.__class__.SCENARIO_TYPES
                + [ STRESS_NAME, self._stressName,
                    CURVE_DATE, acm.Time.DateToday(),
                    MONEYNESS, "1.0",
                    STRESS_TYPE, 'Standard',])
        dataFormat = seps[0].join([DELTA, str(nCols), seps[1].join([CURVE_ID,
            self.__class__.NAME,])])
        return Header(self.__class__.REPORT_TYPES,
                {COLUMN_COUNT: nCols,
                    HEADER_FORMAT: headerFormat,
                    DATA_FORMAT: dataFormat})

    def _getCalculatedColumnHeaders(self):
        heads = [self.separators[1].join([col.name, p.replace(" ", "")])
                for col in self.columnInfoTable.values()
                for p in col.columnPartNames]
        return [DELTA] + heads

    def _getCalculatedValues(self, posID):
        calcs = ['']
        for colID, colInfo in self.columnInfoTable.items():
            vals = self.output[(posID, colID)]
            assert len(vals) == len(colInfo.columnPartNames), ("{0}: "
                    "Expecting {1} columns, got {2}.".format(
                        self.__class__.__name__, len(colInfo.columnPartNames),
                        len(vals)))
            calcs.extend([BaseWriter._getStringValue(
                self._getAttributeValues(posID), colID, v.values, self._logger) for v in vals])
        return calcs

class ArtiQIRBucketDeltaWriter(IRBucketDeltaWriter, ArtiQIRDeltaWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True

    def _getCalculatedColumnHeaders(self):
        return ArtiQIRDeltaWriter._getCalculatedColumnHeaders(self)
    
    def _getCalculatedValues(self, posID, colID):
        vals = self.output[(posID, colID)]
        calc=[]
        colInfo = self.columnInfoTable[colID]
        for v, p in zip(vals, colInfo.columnPartNames):
            value = BaseWriter._getStringValue(
                self._getAttributeValues(posID), colID, v.values, self._logger)
            strV = "{0}:{1}".format(p, value)
            calc.append(strV)
        return ';'.join(calc) 
        
    def _writeDataRows(self, fp):
        return ArtiQIRDeltaWriter._writeDataRows(self, fp)

class ArtiQIRBucketShiftWriter(ArtiQIRBucketDeltaWriter):
    TYPE_HEADER=["Factor.Bucket", "Factor.Name", "Factor.Type"]
    
    def __init__(self, measurement, logger,
                separators=DEFAULT_SEPARATORS, horizon='1d'):
        super(ArtiQIRBucketShiftWriter, self).__init__(logger, separators, horizon)
        self._measurement = measurement
            
    def _getCalculatedColumnHeaders(self):
        return [self._measurement]
    
    def _getCalculatedValues(self, posID, colID):
        # Don't use this call to get the calculated value. 
        raise NotImplementedError("Not implemented in ArtiQIRBucketShiftWriter")
        
    def _writeDataRows(self, fp):
        #for col in self.columnInfoTable.values():
        for colID, colInfo in self.columnInfoTable.items():
            positions = set([nodeKey[0] for nodeKey in self.output.keys()])
            for posID in sorted(positions):
                attrs = self._getAttributeValues(posID)
                bs = self._getBookStructure(posID, attrs)
                rowID = self._getPositionID(str(attrs + bs))
                vals = self.output[(posID, colID)]
                columnDetails = colInfo.name.split(":")
                columnName = columnDetails
                factorName = columnDetails
                if len(columnDetails) == 2:
                    columnName = columnDetails[0]
                    factorName = columnDetails[1]
                for v, bucket in zip(vals, colInfo.columnPartNames):
                    value = BaseWriter._getStringValue(
                        self._getAttributeValues(posID), colID, v.values, self._logger)
                    line = self.separators[0].join([bucket] + [factorName] + [self._stressName] + rowID + attrs + bs + [value])
                    line = self._encodeData(line)
                    print(line, file=fp)    
    
class IRTwistDeltaWriter(IRBucketDeltaWriter):
    NAME = 'Stress Name'
    STRESS_NAME = ''
    DEFAULT_EXPORT_SUFFIX ='dat'

    def _createReportHeader(self):
        return super(IRBucketDeltaWriter, self)._createReportHeader()

    def _getCalculatedColumnHeaders(self):
        assert all([c.scenarioInformation
            for c in self.columnInfoTable.values()]), ("Twist scenarios must"
                    " be defined for all columns.")
        headers = [DELTA]
        sep = self.separators[1]
        for col in self.columnInfoTable.values():
            scenarioName = col.scenarioInformation.storageName.replace(sep, '')
            YCName = col.name.strip('_' + scenarioName)
            h = [sep.join([YCName, scenarioName])
                for i in range(1, len(col.columnPartNames)+1)]
            headers.extend(h)
        return headers

class ArtiQIRTwistDeltaWriter(IRTwistDeltaWriter, ArtiQIRDeltaWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    
    def _getCalculatedColumnHeaders(self):
        return ArtiQIRDeltaWriter._getCalculatedColumnHeaders(self)
    
    def _getCalculatedValues(self, posID, colID):
        return ArtiQIRDeltaWriter._getCalculatedValues(self, posID, colID)
        
    def _writeDataRows(self, fp):
        return ArtiQIRDeltaWriter._writeDataRows(self, fp)


class ArtiQIRTwistShiftWriter(ArtiQIRTwistDeltaWriter):
    TYPE_HEADER=["Scenario.Scenario", "Factor.Name", "Factor.Type"]
    
    def __init__(self, measurement, logger,
                separators=DEFAULT_SEPARATORS, horizon='1d'):
        super(ArtiQIRTwistShiftWriter, self).__init__(logger, separators, horizon)
        self._measurement = measurement
        self._stressName = "Twisit sensivity"

    def _getCalculatedColumnHeaders(self):
        return [self._measurement]
    
    def _getCalculatedValues(self, posID, colID):
        # Don't use this call to get the calculated value. 
        raise NotImplementedError("Not implemented in ArtiQIRTwistShiftWriter")
        
    def _writeDataRows(self, fp):
        #for col in self.columnInfoTable.values():
        for colID, colInfo in self.columnInfoTable.items():
            positions = set([nodeKey[0] for nodeKey in self.output.keys()])
            for posID in sorted(positions):
                attrs = self._getAttributeValues(posID)
                bs = self._getBookStructure(posID, attrs)
                rowID = self._getPositionID(str(attrs + bs))
                vals = self.output[(posID, colID)]
                columnDetails = colInfo.name.split(":")
                columnName = columnDetails
                factorName = columnDetails
                if len(columnDetails) == 2:
                    columnName = columnDetails[0]
                    factorName = columnDetails[1].split("_")[0]
                for v, scenarioName in zip(vals, colInfo.columnPartNames):
                    value = BaseWriter._getStringValue(
                        self._getAttributeValues(posID), colID, v.values, self._logger)
                    line = self.separators[0].join([scenarioName] + [factorName] + [self._stressName] + rowID + attrs + bs + [value])
                    line = self._encodeData(line)
                    print(line, file=fp)    
    
class StressScenarioWriter(BaseScenarioWriter):
    REPORT_TYPES = ['Stress']
    MEASURES = [STRESS_PV_CHANGE]
    RISK_FACTOR_TYPES = {
            "Commodity": "COMMODITY",
            "Credit": "CREDIT",
            "Equity": "EQUITY",
            "FX": "FX",
            "Interest Rate": "INTEREST RATE",
            "Volatility": "VOLATILITY",
            TOTAL: TOTAL,
            }
    SCENARIO_TYPES = (GROUP, STRESS_NAME)
    DEFAULT_EXPORT_SUFFIX ='dat'
     
    def __init__(self, logger, separators=DEFAULT_SEPARATORS,
        horizon='1d', stressType='Standard'):
        super(StressScenarioWriter, self).__init__(logger, separators, horizon)
        self.stressType = stressType
        self._sortedNames = []
        self._columnIndex = {}
        self._uniqueDates = []
        self._dateIndex = {}

    def _createReportHeader(self):
        seps = self.separators
        nDays = Header.horizonDays(self.horizon)
        headerFormat = seps[0].join([
            HORIZON_PARAM, self.horizon,
            HORIZON_DAYS_PARAM, str(nDays),
            "{0} Type".format(self.__class__.REPORT_TYPES[0]), self.stressType,
            CURVE_DATE, acm.Time.DateToday(),
            MONEYNESS, "1.0"])
        nScenarios = self._countScenarios()
        scenarioTypes = seps[1].join(self.__class__.SCENARIO_TYPES)
        dataFormat = seps[0].join([self.__class__.MEASURES[0],
            str(nScenarios), scenarioTypes])

        return Header(self.__class__.REPORT_TYPES,
                {COLUMN_COUNT: nScenarios,
                    DESCRIPTION: "Stress Scenario",
                    HEADER_FORMAT: headerFormat,
                    DATA_FORMAT: dataFormat})
    
    def _getCalculatedColumnHeaders(self):
        headers = [self.__class__.MEASURES[0]]
        for i, dt in enumerate(self._uniqueDates):
            dateGroup = [self.separators[1].join([name, dt])
                    for name in self._sortedNames]
            headers.extend(dateGroup)
        return headers
                    
    def _buildColumnIndex(self):
        """
        Map of all column IDs to order of column names in header.
        """
        colTable = self.columnInfoTable
        self._sortedNames = sorted([col.name for col in colTable.values()])
        self._columnIndex = dict([(colTable[colID].name, colID)
            for colID in colTable.keys()])
        return True

    def _compare(self, v1, v2):
        if v1.isdigit() and v2.isdigit():
            if int(v1) < int(v2):
                return -1
            else:
                return 1
        try:
            v1Date = FBDPCommon.toDate(v1)
            v2Date = FBDPCommon.toDate(v2)
            
            if FBDPCommon.toDate(v1) < FBDPCommon.toDate(v2):
                return -1
            else:
                return 1
        except Exception as err:
            self._logger.logInfo("Failed to convert to Date Error {0}".format(str(err)))
            if v1 < v2:
                return -1
            else:
                return 1

    def _getUniqueDates(self):
        uniq = set(itertools.chain.from_iterable([col.columnPartNames
            for col in self.columnInfoTable.values()]))
        self._uniqueDates = sorted(uniq, key=functools.cmp_to_key(self._compare), reverse=True)


    def _getCalculatedValues(self, posID):
        # For the 'Var PV Change' heading.
        strVals = ['']
        for i, dt in enumerate(self._uniqueDates):
            for colName in self._sortedNames:
                # Shouldn't assume you've got shifts for all risk factors on
                # all days.
                if not (colName, dt) in self._dateIndex:
                    strVals.append('')
                    continue
                colID = self._columnIndex[colName]
                scenarioVals = self.output.get((posID, colID), [])
                val = scenarioVals[self._dateIndex[(colName, dt)]].values
                strVals.append(BaseWriter._getStringValue(posID, colID, val, self._logger))
        return strVals

    def _buildDateIndex(self):
        """
        Indexes the results for each (Risk Factor, Date) pair in the output
        dictionary.
        """
        for col in self.columnInfoTable.values():
            dateHeaders = col.columnPartNames
            rfDates = dict([((col.name, dt), dateHeaders.index(dt))
                for dt in dateHeaders])
            self._dateIndex.update(rfDates)
        assert (len(self._dateIndex.keys()) ==
                len(list(itertools.chain.from_iterable([c.columnPartNames
                    for c in self.columnInfoTable.values()])))), ("Mismatched"
                            " no. of date columns.")

    def _buildReportStructure(self):
        if not super(StressScenarioWriter, self)._buildReportStructure():
            return False
        if not self._buildColumnIndex():
            return False
        self._buildDateIndex()
        self._getUniqueDates()
        return True

class ArtiQStressScenarioWriter(StressScenarioWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    TYPE_HEADER=["Factor.ID", "Factor.Name", "Factor.Type"]
    
    def _getCalculatedColumnHeaders(self):
        return self.__class__.MEASURES
    
    def _getCalculatedValue(self, posID, colName, dt):
        # Shouldn't assume you've got shifts for all risk factors on
        # all days.
        if not (colName, dt) in self._dateIndex:
            return 0.

        colID = self._columnIndex[colName]
        try:
            scenarioVals = self.output.get((posID, colID), [])
            val = scenarioVals[self._dateIndex[(colName, dt)]].values
        except Exception as err:
            self ._logger.logWarning("Exception in {0}:_getCalcualteValue,"
                " err{1}".format(self.__class__.__name__, str(err)))
            return 0. 
        return BaseWriter._getStringValue(posID, colID, val, self._logger)
        
    def _getCalculatedValues(self, posID, colName):
        strVals = []
        for i, dt in enumerate(self._uniqueDates):
            n = self._getCalculatedValue(posID, colName, dt)
            strV = "{0}:{1}".format(dt, n)
            strVals.append(strV)
        
        if colName == "RESIDUAL":
            strVals = []
            for i, dt in enumerate(self._uniqueDates):
                fVals = []
                for name in self._sortedNames[:-1]:
                    n = float(self._getCalculatedValue(posID, name, dt))
                    fVals.append(n)
                total = float(self._getCalculatedValue(posID, colName, dt))
                residual = total - sum(fVals)
                if math.isnan(residual):
                    residual = 0.
                strV = "{0}:{1}".format(dt, residual)
                strVals.append(strV)
        return ';'.join(strVals)
    
    def _getFactorStrings(self, colName):
        return self.separators[0].join([colName] + [colName] + [self.stressType])
        
    def _writeDataRows(self, fp):
        for colName in self._sortedNames:
            positions = set([nodeKey[0] for nodeKey in self.output.keys()])
            factorString = self._getFactorStrings(colName)
            for posID in sorted(positions):
                attrs = self._getAttributeValues(posID)
                bs = self._getBookStructure(posID, attrs)
                rowID = self._getPositionID(str(attrs + bs))
                calcs = self._getCalculatedValues(posID, colName)
                values = []
                calcItems = calcs.split(";")
                for item in calcItems:
                    result = item.split(':')
                    values.append(result[1])
                v = ';'.join(values)
                line = self.separators[0].join([factorString] + rowID + attrs + bs + [v])
                line = self._encodeData(line)
                print(line, file=fp)    

    
class VaRWriter(StressScenarioWriter):
    REPORT_TYPES = ['VaR']
    MEASURES = [VAR_PV_CHANGE]
    # Map of Front RiskFactorType enum strings to Cube column headings. In
    # addition to these, you must always specify a RiskFactorType enum of 0
    # to get the total PV change for calculating the residual, for which there
    # is no mapped string.
    RISK_FACTOR_TYPES = {
            "Commodity": "COMMODITY",
            "Credit": "CREDIT",
            "Equity": "EQUITY",
            "FX": "FX",
            "Interest Rate": "INTEREST RATE",
            "Volatility": "VOLATILITY",
            TOTAL: RESIDUAL,
            }
    SCENARIO_TYPES = ("Group", "Scenario Date", "Scenario")
    DEFAULT_EXPORT_SUFFIX ='dat'

    def __init__(self, logger, separators=DEFAULT_SEPARATORS, horizon='1d',
                varType='Historical', batchSize = LINE_COUNT,
                maxCalcTime = MAX_CALC_TIME,
                decayFactor = 1.0, path = 'C:\temp\RiskExport\Export.txt',
                scenarioCountFilePath=None,
                scenarioDatesFilePath=None,
                decayFactorFilePath=None,
                histories = [],
                useRiskFactor = False,
                overWrite = 1):
        super(VaRWriter, self).__init__(logger, separators, horizon)
        self.varType = varType
        self.history = ''
        self.decayFactor = decayFactor
        self.outputFilePath = path
        self.resultCount = 0
        self.totalResults = 0
        self.batchSize = batchSize
        self.maxCalcTime = maxCalcTime
        self._writeHeadFlag = {}
        self.scenarioCountFilePath = scenarioCountFilePath
        self.scenarioDatesFilePath = scenarioDatesFilePath
        self.decayFactorFilePath = decayFactorFilePath
        self.histories = histories
        self._lastTimeStamp = None
        self.useRiskFactor = useRiskFactor
        self.overWrite = overWrite

    def _countScenarios(self):
        scenarios = [col.scenarioInformation
                for col in self.columnInfoTable.values()
                if col.scenarioInformation]
        dimensions = [[len(self._uniqueDates)] for s in scenarios]
        products = [reduce(lambda x, y: x*y, dims) for dims in dimensions]
        return sum(products)

    def setVarType(self, varType, history):
        if history:
            self.history = history
            self.varType = '{0}_{1}'.format(varType, history)

    def _buildColumnIndex(self):
        """
        Map of all column IDs to order of column names in header.
        """
        colTable = self.columnInfoTable
        self._sortedNames = sorted([col.name for col in colTable.values()])
        if not self.useRiskFactor:
            if not RESIDUAL in self._sortedNames:
                self._logger.logInfo("Can't calculate {0} without risk factor <{1}>".format(
                        RESIDUAL, TOTAL))
                return False
            self._sortedNames.remove(RESIDUAL)
            self._sortedNames.append(RESIDUAL)
        self._columnIndex = dict([(colTable[colID].name, colID)
            for colID in colTable.keys()])
        return True

    def _getRelevantHistory(self, allDates):
        self._logger.logInfo("historical Period -{0}".format(self.history))
        allDates.sort(reverse=True)
        if not self.history:
            return allDates
        # Dates are strings in 'YYYY-MM-DD' format.
        latest = acm.Time().AsDate(allDates[0])
        if self.history[-1] == 'd':
            nbrOfDays = int(self.history[:-1])
            if len(allDates) < nbrOfDays + 1:
                return allDates
            else:
                earliest = acm.Time().AsDate(allDates[nbrOfDays])
        else:
            earliest = acm.Time().DateAdjustPeriod(latest, '-' + self.history)
        dates = [acm.Time().AsDate(d) for d in allDates]
        while (earliest not in dates and earliest > dates[-1]):
            earliest = acm.Time().DateAdjustPeriod(earliest, '-1d')
        self._logger.logInfo("historical Period dates {0} - {1}".format(earliest, latest))
        return [dt for dt in allDates if acm.Time().AsDate(dt) >= earliest]

    def _getUniqueDates(self):
        if not self.useRiskFactor:
            uniq = set(itertools.chain.from_iterable([col.columnPartNames
                for col in self.columnInfoTable.values()]))
            # Filter out those days without results for TOTAL (column name=RESIDUAL
            # because you can't calculate the residual without those.
            valid = [dt for dt in uniq if (RESIDUAL, dt) in self._dateIndex]
            relevant = self._getRelevantHistory(valid)
            self._uniqueDates = relevant
        else:
            uniq = list(set(itertools.chain.from_iterable([col.columnPartNames
                for col in self.columnInfoTable.values()])))
            self._uniqueDates = sorted(uniq, key=functools.cmp_to_key(self._compare), reverse=True)

    def _createReportHeader(self):
        seps = self.separators
        nDays = Header.horizonDays(self.horizon)
        headerFormat = seps[0].join([
            HORIZON_PARAM, self.horizon,
            HORIZON_DAYS_PARAM, str(nDays),
            "{0} Type".format(self.__class__.REPORT_TYPES[0]), self.varType,
            CURVE_DATE, acm.Time.DateToday(),
            MONEYNESS, "1.0"])
        nScenarios = self._countScenarios()
        scenarioTypes = seps[1].join(self.__class__.SCENARIO_TYPES)
        dataFormat = seps[0].join([self.__class__.MEASURES[0],
            str(nScenarios), scenarioTypes])

        return Header(self.__class__.REPORT_TYPES,
                {COLUMN_COUNT: nScenarios,
                    HEADER_FORMAT: headerFormat,
                    DATA_FORMAT: dataFormat})

    def _getCalculatedColumnHeaders(self):
        headers = [self.__class__.MEASURES[0]]
        for i, dt in enumerate(self._uniqueDates):
            dateGroup = [self.separators[1].join([name, dt, str(i)])
                    for name in self._sortedNames]
            headers.extend(dateGroup)
        return headers

    def _getResidual(self, posID, scenarioDate, rfVals):
        colName = self._sortedNames[-1]
        colID = self._columnIndex[colName]
        scenarioVals = self.output[(posID, colID)]
        assert (colName, scenarioDate) in self._dateIndex, ("All dates should"
                " have valid {0}/{1} columns by this point.".format(TOTAL,
                    RESIDUAL))
        total = scenarioVals[self._dateIndex[(colName, scenarioDate)]].values
        try:
            total = total.Number()
        except:
            total = 0.
        residual = total - sum(rfVals)
        if math.isnan(residual):
            residual = 0.
        return str(residual)

    def _getCalculatedValues(self, posID):
        # For the 'Var PV Change' heading.
        strVals = ['']
        for i, dt in enumerate(self._uniqueDates):
            fVals = []
            for colName in self._sortedNames[:-1]:
                # Shouldn't assume you've got shifts for all risk factors on
                # all days.
                if not (colName, dt) in self._dateIndex:
                    strVals.append('')
                    continue
                colID = self._columnIndex[colName]
                try:
                    scenarioVals = self.output.get((posID, colID), [])
                    val = scenarioVals[self._dateIndex[(colName, dt)]].values
                except:
                    continue
                try:
                    n = val.Number()
                    if math.isnan(n):
                        n = 0.
                    fVals.append(n)
                    s = str(n)
                    strVals.append(s)
                except:
                    strVals.append('')
                    self._logger.logInfo("Invalid result for {0} - column {1} on "
                            "{2}.".format(posID, colName, dt))
            if not self.useRiskFactor:
                residual = self._getResidual(posID, dt, fVals)
                strVals.append(residual)
            # -1 for the 'Var PV Change' column, and * the no. of days.
            assert (len(strVals) - 1) == (len(self._sortedNames) * (i+1)), (
                "Len column headings {0} != len column values {1}".format(
                    len(self._sortedNames) * (i+1), len(strVals) - 1))
        return strVals

    def _writeScenarioFile(self, filepath, header, lines):
        try:
            with open(filepath, 'w') as fp:
                if header:
                    self._writeReportHeader(fp, header)
                for ln in lines:
                    print(ln, file=fp)
        except Exception as err:
            self._logger.logInfo(str(err))

    def writeScenarioCount(self, filepath):
        header = None
        if not self.__class__.NOREPORT_HEADER:
            header = self._createReportHeader()
            header.reportTypes = [SCENARIO_COUNT]
            header.params[COLUMN_COUNT] = 1
            header.params[DATA_FORMAT] = ''
        lines = [SCENARIO_COUNT, len(self._uniqueDates)]
        self._writeScenarioFile(filepath, header, lines)

    def writeScenarioDates(self, filepath):
        header = None
        if not self.__class__.NOREPORT_HEADER:
            header = self._createReportHeader()
            header.reportTypes = [SCENARIO_DATE]
            header.params[COLUMN_COUNT] = len(self._uniqueDates)
            header.params[DATA_FORMAT] = ''
            header.params[HEADER_FORMAT] = self.separators[0].join(
                [header.params[HEADER_FORMAT], IS_ANTITHETIC, 'False'])
        lines = [self.separators[0].join([SCENARIO, END_DATE, START_DATE])]
        lines += [self.separators[0].join([str(i), dt, dt])
                for i, dt in enumerate(self._uniqueDates)]
        self._writeScenarioFile(filepath, header, lines)

    def writeDecayFactor(self, filepath):
        if not self.decayFactor:
            return

        header = None
        if not self.__class__.NOREPORT_HEADER:
            header = self._createReportHeader()
            header.reportTypes = [DECAY_FACTOR]
            header.params[COLUMN_COUNT] = 1
            header.params[DATA_FORMAT] = ''
        lines = [DECAY_FACTOR]
        lines += [str(self.decayFactor)]
        self._writeScenarioFile(filepath, header, lines)

    def checkCalculationTime(self, posInfoID, columnInfoID):
        currentTimeStamp = time.time()
        if self._lastTimeStamp is None:
            self._lastTimeStamp = currentTimeStamp
        timeTaken = currentTimeStamp - self._lastTimeStamp
        if (timeTaken > self.maxCalcTime):
            self._logger.logInfo("({0},{1}) takes {2} seconds to calculate, "
                    "exceeds the maximum time limit.".format(
                    self._getAttributeValues(posInfoID)[0], columnInfoID, 
                        "{0:.3f}".format(timeTaken)))
        self._lastTimeStamp = currentTimeStamp

    def addResult(self, posInfoID, columnInfoID, values):
        self.checkCalculationTime(posInfoID, columnInfoID)
        if columnInfoID in self.columnInfoTable:
            self.output[(posInfoID, columnInfoID)] = values
            self.resultCount = self.resultCount + 1
            self.totalResults = self.totalResults + 1
        
        if self.resultCount == len(self.columnInfoTable) * self.batchSize:
            self.write(self.overWrite, self.outputFilePath)
            self.resultCount = 0
            self.output.clear()
            acm.Memory().GcWorldStoppedCollect()

    @staticmethod
    def _getFilePath(filePath, history):
        if not history:
            return filePath
        prefix, suffix = filePath.rsplit('.', 1)
        return '{0}_{1}.{2}'.format(prefix, history, suffix)

    def doWrite(self, filepath):
        try:
            if self._writeHeadFlag[filepath] == True:
                with open(filepath, 'w') as fp:
                    if not self.__class__.NOREPORT_HEADER:
                        header = self._createReportHeader()
                        self._writeReportHeader(fp, header)
                    self._writeDataHeader(fp)
                    self._writeHeadFlag[filepath] = False
                    self._writeDataRows(fp)
            else:
                with open(filepath, 'a') as fp:
                    self._writeDataRows(fp)

            self._logger.logInfo("{0} grouped positions written.".format(self.resultCount/len(self.columnInfoTable)) )
            self._logger.logInfo("{0} total grouped positions written.".format(self.totalResults/len(self.columnInfoTable)))

        except Exception as err:
            tb = inspect.getframeinfo(inspect.trace()[-1][0])
            self._logger.logInfo("{2}.{3}() line {4}: {0} - {1}.".format(
                type(err).__name__, err, tb.filename, tb.function, tb.lineno))

    def write(self, overwrite, outputFilepath=r'C:\Temp\RiskExport\Export'):
        """
        Writes the output in Risk Cube format in several parts - report header,
        data header, data rows.
        """
        BaseWriter._initDirs(outputFilepath)
        filename = self._getNewFileName(outputFilepath, overwrite)
        for hist in self.histories:
            filepath = VaRWriter._getFilePath(filename, hist)
            id_ = int(hashlib.md5(filepath.encode("utf-8")).hexdigest(), 16)
            if filepath not in self._writeHeadFlag:
                self._writeHeadFlag[filepath] = True
            self.setVarType(self.varType.split('_')[0], hist)

            if not (self._buildReportStructure() and self._validProperties()):
                return

            if self._writeHeadFlag[filepath] == True:
                if self.scenarioCountFilePath:
                    self.writeScenarioCount(
                        self._getFilePath(self.scenarioCountFilePath, hist))
                if self.scenarioDatesFilePath:
                    self.writeScenarioDates(
                        self._getFilePath(self.scenarioDatesFilePath, hist))
                if self.decayFactorFilePath:
                    self.writeDecayFactor(
                        self._getFilePath(self.decayFactorFilePath, hist))
            self.doWrite(filepath)
            self._logger.logInfo("{0} successfully exports into file {1}".format(self.__class__.__name__, filename))
            self._logger.summaryAddOk("File", id_, "Export")
    
class ArtiQVaRWriter(ArtiQStressScenarioWriter, VaRWriter):
    MEASURES = ["PV Change"]
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    TYPE_HEADER=["VaR Type", "Factor.Type", "Factor.Risk Class" ]
    
    def _getCalculatedColumnHeaders(self):
        return self.__class__.MEASURES
    
    def _getFactorStrings(self, colName):
        stored = acm.FStoredScenario[colName]
        riskClass = ''
        riskFactorType = ""
        if stored:
            scenario = stored.Scenario()
            params = [ p for p in scenario.ReferencesIn() if type(p) == type("")]
            if "Risk Factor Type" in params:
                riskFactorType = params[params.index("Risk Factor Type") + 1]
            elif "VaR Risk Total" in params:
                riskClass = params[params.index("VaR Risk Total") + 1]
            else:
                res = [i for i in params if "Risk Class" in i]
                if len(res) == 1:
                    idx = params.index(res[0])
                    riskClass = params[idx + 1]

        return self.separators[0].join([self.varType] + [riskFactorType] + [riskClass])
    
    def writeScenarioDates(self, filepath):
        lines = [self.separators[0].join(["VaR Type", SCENARIO, "Scenario Date Start", \
                    "Scernario Date End", "Is Antithetic", "Scenario Date Linking Measure"])]
        lines += [self.separators[0].join([self.varType, str(i+1), dt, dt, "FALSE", str(0)])
                for i, dt in enumerate(self._uniqueDates)]
        self._writeScenarioFile(filepath, None, lines)

class RiskFactorDeltaWriter(BaseScenarioWriter):
    REPORT_TYPES = ["Sensitivity"]
    MEASURES = [DELTA]
    SCENARIO_TYPES = ["Group", "EQUITY PRICE"]
    STRESS_NAME = "Parallel Shift"
    NAME = 'Stress Name'
    DEFAULT_EXPORT_SUFFIX ='dat'
    
    def __init__(self, stressName, logger, separators=DEFAULT_SEPARATORS, horizon='1d'):
        super(RiskFactorDeltaWriter, self).__init__(logger, separators, horizon)
        self._stressName = self.__class__.STRESS_NAME
        if stressName:
            self._stressName = stressName
        self.priceFactorNames=[]

    def _countScenarios(self):
        return 1

    def addColumn(self, info, ID):
        self.columnInfoTable[ID] = info

    def addPosition(self, info, ID):
        self.positionInfoTable[ID] = info

    def addResult(self, posInfoID, columnInfoID, calculationInfos):

        assert posInfoID in self.positionInfoTable
        for info in calculationInfos:
            priceFactorName = info.projectionCoordinates
            if priceFactorName not in self.priceFactorNames:
                self.priceFactorNames.append(priceFactorName)

            assert (posInfoID, priceFactorName) not in self.output
            self.output[(posInfoID, priceFactorName)] = info.values

    def _createReportHeader(self):
        seps = self.separators
        nCols = len(self.priceFactorNames)
        headerFormat = seps[0].join(self.__class__.SCENARIO_TYPES
                + [CURVE_DATE, acm.Time.DateToday(),
                    MONEYNESS, "1.0",
                    STRESS_TYPE, 'Standard',])
        dataFormat = seps[0].join([DELTA, str(nCols), seps[1].join([CURVE_ID,
            self.__class__.NAME,])])
        return Header(self.__class__.REPORT_TYPES,
                {COLUMN_COUNT: nCols,
                    HEADER_FORMAT: headerFormat,
                    DATA_FORMAT: dataFormat})

    def _getCalculatedColumnHeaders(self):
        heads = [self.separators[1].join([c, self._stressName])
                for c in self.priceFactorNames]
        
        return [DELTA] + heads

    
    def _getCalculatedValues(self, posID):
        calcs = []
        for pos, col in self.output.keys():
            if pos != posID:
                continue
            
            for rfName in self.priceFactorNames:
                if rfName != col:
                    calcs.append('0.0')
                    continue
                    
                valObj = self.output[(pos, rfName)]
                if not valObj:
                    continue
            
                strVal = str(valObj.Number())
                #unit = valObj.Unit()
                calcs.append(strVal)
                
        return [''] + calcs   

class ArtiQRiskFactorDeltaWriter(RiskFactorDeltaWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    TYPE_HEADER=["Factor.Type", "Factor.ID"]
     
    def _getCalculatedColumnHeaders(self):
        return [DELTA] 
    
    def _getCalculatedValues(self, posID, rfName):
        valObj = self.output.get((posID, rfName), 0.0)
        if valObj.IsKindOf(acm.FDenominatedValue):
            strVal = str(valObj.Number())
            return strVal
        else:
            return str(valObj)

    def _writeDataRows(self, fp):
        for factorName in self.priceFactorNames:
            positions = set([nodeKey[0] for nodeKey in self.output.keys()])
            for posID in sorted(positions):
                attrs = self._getAttributeValues(posID)
                bs = self._getBookStructure(posID, attrs)
                rowID = self._getPositionID(str(attrs + bs))
                calcs = self._getCalculatedValues(posID, factorName)
                line = self.separators[0].join([self._stressName] + [factorName] + rowID + attrs + bs + [calcs])
                line = self._encodeData(line)
                print(line, file=fp)    

class ArtiQPLExplainWriter(BaseScenarioWriter):
    DEFAULT_EXPORT_SUFFIX='csv'
    POSITION_ID = 'Trade.Reference'
    BOOKSTRUCTURE_PREFIX='Trade'
    NOREPORT_HEADER = True
    TYPE_HEADER=["Calculation ID.Calculation ID", "Factor.Type", "Factor.ID", "Factor.Sub ID", "Trade.Benchmark Strike"]
    
    def __init__(self, factorTypes, timebucket, logger, separators=DEFAULT_SEPARATORS, horizon='1d'):
        super(BaseScenarioWriter, self).__init__(logger, separators, horizon)
        self.priceFactorNames=[]
        self.volFactorNames=[]
        self.factorTypes = factorTypes
        self.curveFactorNames = [] #yieldCurves
        self.ycCurveTimeBucketsMap = {}
        self.timebuckets= FMarketRiskExportUtil.TimebucketInPeriod(timebucket, logger)
        self.riskfactorExportMaps = FBDPCommon.valueFromFParameter('FArtiQMarketExportParameters', 'RiskFactorExportNames')
        self.riskfactorExportMaps = ast.literal_eval(self.riskfactorExportMaps)

    def _useBookStructure(self):
        return False

    def _getCalculatedColumnHeaders(self):
        return ["_DeltaAndGamma_"] 
    
    def addColumn(self, info, ID):
        self.columnInfoTable[ID] = info

    def _calcualteTimebucketsOnYc(self):
        ycTimeBuckesMap = {}
        for ycName in self.curveFactorNames:
            ycTimeBuckesMap[ycName] = FMarketRiskExportUtil.GetYcTimeBucket(ycName, self._logger)
        
        self._logger.logInfo("Used Yield curve Time buckets {0}".format(ycTimeBuckesMap))
        return ycTimeBuckesMap

    
    def _addResultForVolatility(self, posInfoID, columnInfoID, calculationInfos):
        factorDetailsDict = defaultdict(list)
        for calculationInfo in calculationInfos:
            line = calculationInfo.projectionCoordinates.AsString()
            dateStr, period = FMarketRiskExportUtil.ParseDateStrToPeriod(line, self._logger)
            if dateStr == "" and period == "":
                self._logger.logError('Ignore the row {0} due to unexpected format.'.format(
                    line))
                continue

            if period.find('-') != -1:
                continue
    
            index = line.find('@')
            endindex = line.find(dateStr)-3
            volName = line[index+1: endindex]
            pos = line.rfind('-') 
            strike = line[pos+1 : ]
            
            values = ':'.join([BaseWriter._getStringValue(posInfoID, columnInfoID, v, self._logger) \
                    for v in calculationInfo.values])
            if values == "0.0000:0.0000":
                continue

            volFactorName = "@".join([volName, strike])
            if volFactorName not in self.volFactorNames:
                self.volFactorNames.append(volFactorName)
            factorDetailsDict[volFactorName].append((period, values))
        
        for key in factorDetailsDict:
            valList = factorDetailsDict[key]
            cmp = functools.cmp_to_key(lambda a, b: FMarketRiskExportUtil.Compare(a[0], b[0]))
            valList.sort(key=cmp)
            strValues = []
            for (period, value) in valList:
                strValues.append("{0}::::{1}".format(period, value))
            self.output[(posInfoID, key)] = ";".join(strValues)

    
    def _addResultForCurveBasedRF(self, posInfoID, columnInfoID, calculationInfos):
        colNames = columnInfoID.split('@')
        type = colNames[0]
        priceFactorName = colNames[1]
        if priceFactorName not in self.curveFactorNames:
            self.curveFactorNames.append(priceFactorName)
        values = [calculationInfo.values for calculationInfo in calculationInfos]
        self.output[(posInfoID, columnInfoID)] = values
 
    def addResult(self, posInfoID, columnInfoID, calculationInfos):
        try:
            if columnInfoID == "Inflation Curve":
                curveName = calculationInfos[0].values
                if curveName != '':
                    self.output[(posInfoID, columnInfoID)] = curveName
            elif columnInfoID == "All Yield Curves Name":
                curves = calculationInfos[0].values
                if len(curves) != 0:
                    self.output[(posInfoID, columnInfoID)] = curves
            elif "Instrument Spread" in columnInfoID:
                self.output[(posInfoID, columnInfoID)] = calculationInfos[0].values
            elif "Benchmark" in columnInfoID or \
                "InterestRate" in columnInfoID or \
                "Inflation" in columnInfoID or \
                "Credit" in columnInfoID:
                self._addResultForCurveBasedRF(posInfoID, columnInfoID, calculationInfos)
            elif "Volatility" in columnInfoID:
                self._addResultForVolatility(posInfoID, columnInfoID, calculationInfos)
            elif "Commodity" in columnInfoID:
                for calculationInfo in calculationInfos:
                    calValue = calculationInfo.values
                    if calValue == None:
                        continue
                    if calValue.IsKindOf(acm.FDenominatedValue):
                        value= calValue.Number()
                        unitName= calValue.Unit()
                        if value == 0.0 and unitName == None:
                            continue
                        type = "Delta" if "Delta" in columnInfoID else "Gamma"
                        priceFactorName = unitName if unitName else ''
                        if priceFactorName not in self.priceFactorNames:
                            self.priceFactorNames.append(priceFactorName)
                        columnInfoDetails = "Commodity " + type + '@' + priceFactorName
                        self.output[(posInfoID, columnInfoDetails)] = value
                    else:
                        print("unexptected calc value type", type(calValue), calValue)
            else:
                for calculationInfo in calculationInfos:
                    if not self._hasValidValue(calculationInfo.values):
                        continue
                    priceFactorName = calculationInfo.projectionCoordinates
                    if priceFactorName not in self.priceFactorNames:
                        self.priceFactorNames.append(priceFactorName)
                    columnInfoDetails = columnInfoID + '@' + priceFactorName
                    self.output[(posInfoID, columnInfoDetails)] = calculationInfo.values 
        except Exception as err:
            self._logger.logError('addResult in ArtiQPLExplainWritererr {0}'.format(str(err)))
        
    def _getCalculatedValues(self, posID, columID, rfName):
        columnInfoDetails = columID + '@' + rfName
        valObj = self.output.get((posID, columnInfoDetails), [''])
        values = [BaseWriter._getStringValue(posID, columID, v, self._logger) for v in valObj]
        return values

    def _hasValidValue(self, vals):
        totalVal = 0.0
        for v in vals:
            try:
                if isinstance(v, float):
                    totalVal +=v
                elif type(v) is str:
                    if v:
                        n = v[:-3].replace(" ", "")
                        if n == "":
                            n= str(0.0)
                        v = float(n)
                        totalVal +=v
                elif v.IsKindOf(acm.FDenominatedValue):
                    v = v.Number()
                    if math.isnan(v):
                        v = 0.
                    totalVal +=v
                else:
                    self._logger.logError('Unhandled value type {0} '.format(type(v)))
            except Exception:
                pass
        return totalVal != 0.0

    def _getDeltaGammaCalcValues(self, factorName, Delta_calcs, Gamma_calcs):

        buckets = self.timebuckets if self.timebuckets else self.ycCurveTimeBucketsMap.get(factorName, [])
        if len(buckets) != len(Delta_calcs) or len(Delta_calcs) != len(Gamma_calcs):
            self._logger.logWarning('Unexpected list length, bucket{0}, delta_calcs {1},'
                'gamma_calcs {2}.'.format(len(buckets), len(Delta_calcs), len(Gamma_calcs)))
                
            #Invalid Delta_calcs or Gamma_calcs lengh, default to 0.
            for i in range(1, len(buckets) + 1):
                if len(Delta_calcs) < i:
                    Delta_calcs.append('0.0')
                if len(Gamma_calcs) < i:
                    Gamma_calcs.append('0.0')

        vals = []
        for tb, delta, gamma in zip(buckets, Delta_calcs, Gamma_calcs):
            value = tb + "::::" + delta + ":" + gamma  
            vals.append(value)
        return ';'.join(vals)

    
    def _writeDataRows(self, fp):
        try:
            if not self.timebuckets:
                self.ycCurveTimeBucketsMap = self._calcualteTimebucketsOnYc()
            positions = set([nodeKey[0] for nodeKey in self.output.keys()])
            for fType in self.factorTypes:
                fTypeExportName = self.riskfactorExportMaps.get(fType, fType)
                for posID in sorted(positions):
                    attrs = self._getAttributeValues(posID)
                    bs = self._getBookStructure(posID, attrs)
                    rowID = self._getPositionID(str(attrs + bs))
                    if fType in ['InterestRate', 'Benchmark', 'Credit']:
                        for factorName in self.curveFactorNames:
                            if fType == 'Credit':
                                deltaColName = fType + " Par Delta"
                                gammaColName = fType + " Gamma"
                            if fType == 'Benchmark':
                                deltaColName = fType + " Delta PLE"
                                gammaColName = fType + " Gamma PLE"
                            if fType == 'InterestRate':
                                deltaColName = fType + ' Delta'
                                gammaColName = fType + " Gamma"
                            Delta_calcs = self._getCalculatedValues(posID, deltaColName, factorName)
                            Gamma_calcs = self._getCalculatedValues(posID, gammaColName, factorName)
                            if not self._hasValidValue(Delta_calcs) and not self._hasValidValue(Gamma_calcs):
                                continue
                            calcs = self._getDeltaGammaCalcValues(factorName, Delta_calcs, Gamma_calcs)
                            if calcs:
                                line = self.separators[0].join(["Sensitivity Based", fTypeExportName, str(factorName), "Whole", ""] \
                                    + rowID + attrs + bs + [calcs])
                                line = self._encodeData(line)
                                print(line, file=fp)

                    elif fType == "InstrumentSpread":
                        curves = self.output.get((posID, "All Yield Curves Name"), [])
                        instrumentSpreadCurves = [y.Name() for y in curves if y.Type() == 'Instrument Spread']
                        if instrumentSpreadCurves:
                            deltaColName = "Instrument Spread Delta PLE"
                            gammaColName = "Instrument Spread Gamma PLE"
                            Delta_calc = BaseWriter._getStringValue(posID, deltaColName, \
                                    self.output.get((posID, deltaColName), 0.0), self._logger)
                            Gamma_calc = BaseWriter._getStringValue(posID, gammaColName, \
                                    self.output.get((posID, gammaColName), 0.0), self._logger)
                            posInfo = [self.positionInfoTable[p] for p in self.attributeChain]
                            attrNames = [p.dimensionName for p in posInfo]
                            instAttrNames = ["Instrument", "Instrument Name", "InstrumentName", "Trade.Instrument Name", "Trade.InstrumentName"]
                            instnameAttrName = set(attrNames).intersection(set(instAttrNames))
                            if len(instnameAttrName) == 0:
                                self._logger.logError("No instrument name is specified in the position.")
                                continue
                            idx = attrNames.index(instnameAttrName.pop())
                            instName = self._getAttributeValues(posID)[idx]
                            inst = acm.FInstrument[instName]
                            if not inst:
                                self._logger.logError("No instrument found with name {0}".format(instName))
                                continue
                            
                            exportName = instName
                            expiryDate = inst.ExpiryDateOnly()
                            underlying = inst.ValuationUnderlying()
                            if underlying:
                                exportName = underlying.Name()
                                expiryDate = underlying.ExpiryDateOnly()
                            
                            dateStr, period = FMarketRiskExportUtil.ParseDateStrToPeriod(expiryDate, self._logger)
                            calcs = "{0}::::{1}:{2}".format(period, Delta_calc, Gamma_calc)
                            
                            line = self.separators[0].join(["Sensitivity Based", fTypeExportName, \
                                    "{0}-{1}".format(instrumentSpreadCurves[0], exportName), "Whole", ""] + rowID + attrs + bs + [calcs])
                            line = self._encodeData(line)
                            print(line, file=fp)

                    elif fType == 'Inflation':
                        for factorName in self.curveFactorNames:
                            Delta_calcs = self._getCalculatedValues(posID, fType + " Benchmark Delta", factorName)
                            Gamma_calcs = ['{0:.4f}'.format(0.00) for v in Delta_calcs]
                            if not self._hasValidValue(Delta_calcs):
                                continue
                            curveName = self.output.get((posID, "Inflation Curve"), '')
                            if curveName != '' and curveName != factorName:
                                continue
                            calcs = self._getDeltaGammaCalcValues(factorName, Delta_calcs, Gamma_calcs)
                            if calcs:
                                line = self.separators[0].join(["Sensitivity Based", fTypeExportName, str(factorName), "Whole", ""] + rowID + attrs + bs + [calcs])
                                line = self._encodeData(line)
                                print(line, file=fp)

                    elif fType == "Volatility":
                        for factorName in self.volFactorNames:
                            if (posID, factorName) not in self.output.keys():
                                continue
                           
                            calcs = self.output.get((posID, factorName), None)
                            if calcs:
                                volStrike = factorName.split('@')
                                if len(volStrike) != 2:
                                    self._logger.logError("Wrong volFactorName {0}".format(factorName))
                                    continue
                                line = self.separators[0].join(["Sensitivity Based", fTypeExportName, str(volStrike[0]), "Whole", volStrike[1]] + rowID + attrs + bs + [calcs])
                                line = self._encodeData(line)
                                print(line, file=fp)

                    elif fType == "CommodityPrice":
                        for factorName in self.priceFactorNames:
                            DeltaValObj = self.output.get((posID, "Commodity Delta" + '@' + factorName), 0.0)
                            GammaValObj = self.output.get((posID, "Commodity Gamma" + '@' + factorName), 0.0)
                            if DeltaValObj == 0.0 and GammaValObj == 0.0:
                                continue
                            DeltaValue = BaseWriter._getStringValue(posID, "Commodity Delta", DeltaValObj, self._logger) 
                            GammaValue = BaseWriter._getStringValue(posID, "Commodity Gamma", GammaValObj, self._logger) 
                            calcs = '{0}:{1}'.format(DeltaValue, GammaValue)
                            if calcs:
                                line = self.separators[0].join(["Sensitivity Based", fTypeExportName, str(factorName), "Whole", ""] + rowID + attrs + bs + [calcs])
                                line = self._encodeData(line)
                                print(line, file=fp)

                    else:
                        for factorName in self.priceFactorNames:
                            factorID = factorName if fType == "Equity" else factorName.AsString().replace("Equity@", "")
                            vals = self._getCalculatedValues(posID, fType, factorName)
                            if self._hasValidValue(vals):
                                calcs = ':'.join(vals)
                                line = self.separators[0].join(["Sensitivity Based", fTypeExportName, str(factorID), "Whole", ""] + rowID + attrs + bs + [calcs])
                                line = self._encodeData(line)
                                print(line, file=fp)
        except Exception as err:
            self._logger.logError("Exception in writeDataRows error {0}".format(str(err)))
