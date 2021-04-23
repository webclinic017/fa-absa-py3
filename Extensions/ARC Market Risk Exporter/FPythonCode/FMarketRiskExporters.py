""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExporters.py"
"""---------------------------------------------------------------------------
MODULE
    FMarketRiskExporters - Classes to create export files

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

---------------------------------------------------------------------------"""

import os.path
import re

import acm
import FBDPCommon
import FBDPWorld
import FFileUtils
import FExportCalculatedValuesMain
import FMarketRiskExportAttributes
import FRiskCubeWriterBase
import FRiskCubeScenarioWriters
import FExportCalculatedValuesMain as CalcMain
from FRiskCubeWriterBase import ProfitAndLossWriter
from FRiskCubeWriterBase import ArtiQProfitAndLossWriter
from FRiskCubeScenarioWriters import SpotVolWriter
from FRiskCubeScenarioWriters import ArtiQSpotVolWriter
from FRiskCubeScenarioWriters import IRVolWriter
from FRiskCubeScenarioWriters import ArtiQIRVolWriter
from FRiskCubeScenarioWriters import FXVolWriter
from FRiskCubeScenarioWriters import ArtiQFXVolWriter
from FRiskCubeScenarioWriters import FXVolTaperWriter
from FRiskCubeScenarioWriters import ArtiQFXVolTaperWriter
from FRiskCubeScenarioWriters import SpotVolTaperWriter
from FRiskCubeScenarioWriters import ArtiQSpotVolTaperWriter
from FRiskCubeScenarioWriters import FXMatrixWriter
from FRiskCubeScenarioWriters import ArtiQFXMatrixWriter
from FRiskCubeScenarioWriters import IRDeltaWriter
from FRiskCubeScenarioWriters import ArtiQIRDeltaWriter
from FRiskCubeScenarioWriters import VegaWriter
from FRiskCubeScenarioWriters import ArtiQVegaWriter
from FRiskCubeScenarioWriters import CreditDeltaWriter
from FRiskCubeScenarioWriters import ArtiQCreditDeltaWriter
from FRiskCubeScenarioWriters import IRBucketDeltaWriter
from FRiskCubeScenarioWriters import ArtiQIRBucketDeltaWriter
from FRiskCubeScenarioWriters import IRTwistDeltaWriter
from FRiskCubeScenarioWriters import ArtiQIRTwistDeltaWriter
from FRiskCubeScenarioWriters import RiskFactorDeltaWriter
from FRiskCubeScenarioWriters import ArtiQRiskFactorDeltaWriter
from FRiskCubeScenarioWriters import GreekWriter
from FRiskCubeScenarioWriters import ArtiQGreekWriter
from FRiskCubeScenarioWriters import ArtiQIRBucketShiftWriter
from FRiskCubeScenarioWriters import ArtiQIRParallelShiftWriter
from FRiskCubeScenarioWriters import ArtiQIRTwistShiftWriter
from FRiskCubeScenarioWriters import ArtiQPLExplainWriter
import MarketDataWriter
import FRiskCubeCustomWriters
from FBookTagWriter import BookTagWriter
from FTradeTagWriter import TradeTagWriter
import FMarketRiskExportUtil

FILE_SUFFIXES = ('.dat', '.txt', '.csv')
CSV_SUFFIXES = '.csv'
DAT_SUFFIXES = '.dat'
MAX_FILES_IN_DIR = 256
ALL_CURVES = set(['All', 'None', 'All Curves'])
DISPLAY_RELATIVE = 'Relative'
_SPOT_VOL = 'SpotVol'
_FX_MATRIX = 'FXMatrix'
SPOT_VOL_RELATIVE = 'mulrelpercent'
SPOT_VOL_ABSOLUTE_PERCENT_POINTS = 'deltapercentpoints'
SPOT_VOL_ABSOLUTE_BASIS_POINTS = 'deltabasispoints'
SPOT_VOL_PERIODS = 'shiftVolatilityPeriods'
FX_RELATIVE = 'shiftFXMatrixRelativePercent'
STOCK_PRICE_SCENARIOS = [acm.FSymbol('market price'),
                        acm.FSymbol('market price all')]
STOCK_VOL_SCENARIOS = [acm.FSymbol('volatility value'),
        acm.FSymbol('volatility information')]
STOCK_VOL_SCENARIOS_PERIODS = [
        acm.FSymbol('volatility valueshiftVolatilityPeriods'),
        acm.FSymbol('volatility informationshiftVolatilityPeriods')]
FX_SCENARIO = acm.FSymbol('fx matrix')

ExportToMemoryCube = 'Adaptiv Memory Cube'
ExportToArtiQCube = 'Adaptiv ArtiQ Cube' 
ExportType = [acm.FSymbol(ExportToMemoryCube), acm.FSymbol(ExportToArtiQCube)]

CLEAN_PL = "Portfolio Total Profit and Loss Excluding Trades After Start Date"
DAILY_PL = "Portfolio Total Profit and Loss Daily"
THEO_VAL = "Portfolio Theoretical Value"
THETA_PL = "Portfolio Theta ThTPL"
TPL = "Portfolio Total Profit and Loss"
VEGA = "Portfolio Vega"

CREDIT_DELTA = "Flat Credit Par Delta"
CREDIT_DAY_COUNT = acm.FSymbol("CreditParDeltaDayCountChoice")
CREDIT_RATE_TYPE = acm.FSymbol("CreditParDeltaDisplayedRateChoice")
CREDIT_FREQUENCY = acm.FSymbol("CreditParDeltaRateTypeChoice")

PORTFOLIO_DELTA = "Portfolio Delta"
YIELD_DELTA = "Portfolio Delta Yield"
YIELD_DELTA_BUCKET = "Interest Rate Yield Delta Bucket"

YIELD_CURVE_FILTER = acm.FSymbol('InterestRateDeltaGammaCurveFilter')
BENCHMARK_CURVE_FILTER = acm.FSymbol('BenchmarkDeltaCurveFilter')
YIELD_CURVE_SCENARIO = acm.FSymbol('yield curve')
falseTrue = ["False", "True"]


def AadditionalAttributes():    
    attributesStr = FBDPCommon.valueFromFParameter(
                'FArtiQMarketExportParameters', 'AdditionalAttributes')
    if attributesStr:
        return [i.strip() for i in attributesStr.split(',')]
    return []

def MethodFromAttribute(attribute):
    return FBDPCommon.valueFromFParameter(
                'FArtiQExportAttributeMethodMap', attribute)

def AdditionalAttributesSpecs(attributeSpecs):
    specs = []
    additional_attributes = AadditionalAttributes()
    existedAttributes = [a.label for a in attributeSpecs]
    for a in additional_attributes:
        if a in existedAttributes:
            continue
        m = MethodFromAttribute(a)
        specs.append(FMarketRiskExportAttributes.AttributeSpec(label=a, method=m, required=False))
    return specs

def createAttributesObject():
    portf = FMarketRiskExportAttributes.AttributeSpec('Portfolio', None, False)
    instr = FMarketRiskExportAttributes.AttributeSpec('Instrument', None, False)
    cls = acm.FTrade
    config = acm.FArray()

    attributeSpecs = FMarketRiskExportAttributes.getAttributeSpecs()
    if not attributeSpecs:
        raise Exception("Invalid attribute specification.")
    
    additionAttributesSpecs = AdditionalAttributesSpecs(attributeSpecs)
    for extra in additionAttributesSpecs:
        config.Add(extra)

    for a in attributeSpecs:
        config.Add(a)

    grouper = acm.Risk().CreateChainedGrouperDefinition(cls, portf.label,
            portf.required, instr.label, instr.required, config)
    return grouper

def createArtiQAttributesObject():
    
    portf = FMarketRiskExportAttributes.AttributeSpec('Portfolio', None, False)
    instr = FMarketRiskExportAttributes.AttributeSpec('Instrument', None, False)
    cls = acm.FTrade
    config = acm.FArray()

    attributeSpecs = FMarketRiskExportAttributes.getArtiQAttributeSpecs()
    if not attributeSpecs:
        raise Exception("Invalid attribute specification.")
    
    additionAttributesSpecs = AdditionalAttributesSpecs(attributeSpecs)
    for extra in additionAttributesSpecs:
        config.Add(extra)
    
    for a in attributeSpecs:
        config.Add(a)

    grouper = acm.Risk().CreateChainedGrouperDefinition(cls, portf.label,
        portf.required, instr.label, instr.required, config)
    
    return grouper

def configureAttributes(params):
    attributes = None
    if ExportToMemoryCube == params.export_fileformat():
        attributes = createAttributesObject()
    elif params.grouper:
        attributes = params.grouper
    else:
        attributes = createArtiQAttributesObject()
    
    return attributes

class CommonParameters(FBDPWorld.WorldInterface):
    """
    Base class for all the parameter helper classes
    """
    def __init__(self, ael_parameters, tab_name, default_column, logger):
        FBDPWorld.WorldInterface.__init__(self, logger)
        self.ael_params = ael_parameters
        self.today = acm.Time().DateToday()
        self.filePrefix = ''
        self.dateToTheName = falseTrue.index(self.ael_params.get("Output File Date", 'False'))
        selectedColumns = self.ael_params.get('column_name_' + tab_name, default_column)
        if selectedColumns:
            self.columnName = selectedColumns
        self.trade_header, self.grouping_attrs, self.grouper = self._createTradeGrouper()
    
    def delimiter(self):
        if ExportToArtiQCube == self.export_fileformat():
            return ','
        return self.ael_params.get("delimiter", '|')

    def sub_delimiter(self):
        if ExportToArtiQCube == self.export_fileformat():
            return ';'
        return self.ael_params.get("sub_delimiter", ',')

    def separators(self):
        return [self.delimiter(), self.sub_delimiter()]

    def distributedCalculations(self):
        if 'distributedCalculations' in self.ael_params:
            return self.ael_params['distributedCalculations']
        else:
            return 0
    
    def horizon(self):
        if 'horizon' in self.ael_params:
            return self.ael_params['horizon']
        else:
            return '1d'

    def portfolios(self):
        return self.ael_params['portfolios']

    def tradeFilters(self):
        return self.ael_params['tradeFilters']

    def storedQueries(self):
        return self.ael_params['storedASQLQueries']
    
    def positionSpecification(self):
        return self.ael_params['positionSpec']

    def export_fileformat(self):
        fileformat = self.ael_params.get('ExportFormats', ExportToMemoryCube)
        return fileformat

    def do_create_report(self):
        positions = (self.portfolios() or self.tradeFilters()
                or self.storedQueries())
        if not positions:
            self._logInfo("{0}: No positions specified.".format(
                self.__class__.__name__))
        return positions

    def _dir_path(self):
        fp = self.ael_params["output_dir"]
        if isinstance(fp, str):
            outdir = fp
        else:
            outdir = fp.AsString()
        outdir = FFileUtils.expandEnvironmentVar(outdir)
        return outdir

    def _do_date_dir(self):  
        return falseTrue.index(self.ael_params["Create directory with date"])

    def _output_directory(self):
        outdir = self._dir_path()
        subdir = ''
        if not self._do_date_dir():
            return outdir
        return os.path.join(outdir, self.today)

    def overwrite(self):
        return falseTrue.index(self.ael_params["Overwrite if file exists"])

    def _baseFileName(self):
        return ''
    
    # Should the count file parameters really be in the base class (are they
    # needed at all?)
    def getOutputFileName(self, is_count_file=False, count_file_name=''):
        outdir = self._output_directory()
        count_file_postfix = is_count_file

        file_name = self._baseFileName()
        prefix = self.ael_params.get('Output File Prefix', '')
        if prefix:
            file_name = '{0}_{1}'.format(prefix, file_name)

        if is_count_file and count_file_name:
            file_name = self.filePrefix + count_file_name
            count_file_postfix = False

        if self.dateToTheName:
            file_name = '{0}_{1}'.format(file_name, self.today)

        filepath = os.path.join(outdir, file_name)
        return filepath
    
    def _extendedFileName(self, name):
        #assert self.getOutputFileName().endswith(FILE_SUFFIXES), (
        #            "Should have appended a suffix.")
        ext = re.sub(r'[,.+ &%/\\()]', '_', name)
        if self.getOutputFileName().endswith(FILE_SUFFIXES):
            prefix, suffix = self.getOutputFileName().rsplit('.', 1)
            return '{0}_{1}.{2}'.format(prefix, ext, suffix)
        else:
            return '{0}_{1}'.format(self.getOutputFileName(), ext)
    
    def _createTradeGrouper(self):
        # Return the positions and positions info to use in the calculation
        # and export file, respectively.
        context_name = acm.GetDefaultContext().Name()
        grouping_attrs = []
        has_trade_ref = False
        positionSpec = self.ael_params.get("positionSpec", None)
        if not positionSpec:
            return None, None, None

        existedAttributes = []
        for attr_def in positionSpec.AttributeDefinitions():
            method_chain = attr_def.Definition()
            display_name = acm.Sheet.Column().MethodDisplayName(
                acm.FTrade, method_chain, context_name)
            existedAttributes.append(display_name)
            grouping_attrs.append([display_name, method_chain, False])

        additional_attributes = AadditionalAttributes()
        for a in additional_attributes:
            if a in existedAttributes:
                continue
            m = MethodFromAttribute(a)
            grouping_attrs.append([a, m, False])
            
        trade_header = [h[0] for h in grouping_attrs]
        grouper = acm.Risk().CreateChainedGrouperDefinition(
            acm.FTrade, 'Portfolio', False, 'Instrument', True, grouping_attrs
        )
        return trade_header, grouping_attrs, grouper


class StressParameters(CommonParameters):

    def valid(self):
        return (self.stored_scenarios() or self.scenario_file_exists()) \
            and self._baseFileName()
    
    def _baseFileName(self):
        return self.ael_params.get("Stress File Name", '')

    def risk_factor_types(self):
        unadj_risk_factor_types = self.ael_params.get("stress_risk_types", None)
        return unadj_risk_factor_types

    def scenario_file(self):
        file_path = self.ael_params.get("stress_scenario_file", None)
        if not file_path or not file_path.SelectedFile():
            return None
        return file_path.SelectedFile()

    def scenario_file_exists(self):
        try:
            f = self.scenario_file()
            if f: return True
            else: return False
        except:
            return False

    def stress_type(self):
        stress_type = self.ael_params.get('stress_type', "Standard")
        return stress_type
    
    def stored_scenarios(self):
        scenarioNames = self.ael_params.get('stress_Scenarios', [])
        return scenarioNames
    
class PvScenarioParameters(StressParameters):

    def __init__(self, ael_parameters, tab_name, default_column, logger):
        super(PvScenarioParameters, self).__init__(ael_parameters, tab_name, default_column, logger)
        self.hist = ['']

    def do_create_report(self):
        if not super(PvScenarioParameters, self).do_create_report():
            return False
        return self.scenario_file_exists() and self._validHistory()

    def _baseFileName(self):
        return self.ael_params.get("VaR File Name", '')

    def risk_factor_types(self):
        unadj_risk_factor_types = self.ael_params.get("var_risk_types", None)
        return unadj_risk_factor_types

    def scenario_file(self):
        file_path = self.ael_params.get("var_scenario_file", None)
        if not file_path or not file_path.SelectedFile():
            return None
        return file_path.SelectedFile()
 
    def valid(self):
        isValid = (self.stored_scenarios() or self.scenario_file_exists()) \
            and self._validHistory() and self._baseFileName()
        return isValid

    def stored_scenarios(self):
        scenarioNames = self.ael_params.get('var_Scenarios', [])
        return scenarioNames
    
    def var_type(self):
        var_type = self.ael_params.get("var_type", "Historical")
        return var_type

    def batchSize(self):
        if "batchSize" in self.ael_params:
            batchSize = self.ael_params["batchSize"]
            if batchSize is None:
                batchSize = 200
        else:
            batchSize = 200
        return batchSize

    def maxCalcTime(self):
        maxTime = self.ael_params.get("maxCalcTime", 10)
        if maxTime is None:
            maxTime = 10
        return maxTime

    def split_buckets(self, buckets):
        dates = re.compile(r"""
                        ([\d]+(?:m|y|d|w))                # match 11m, -1d """
                        , re.I + re.VERBOSE).findall(buckets)
        return dates

    def _validHistory(self):
        periodsStr = self.ael_params.get('vaRHistory', '')
        periods = []
        if periodsStr:
            periods = periodsStr.split(',')
        try:
            self.hist = self.split_buckets(periodsStr)
        except ValueError as ex:
            self._logError(ex)

        if len(self.hist) != len(periods):
            self._logWarning('Invalid History Periods Ignored.')

        if not self.hist:
            self.hist = ['']
        return True

    def history(self):
        return self.hist

    def decay_factor(self):
        if "decay_factor" in self.ael_params:
            decay_factor = self.ael_params["decay_factor"]
            return decay_factor
        else:
            return None

    def scenario_count_file_name(self):
        if "scenario_count_file_name" in self.ael_params:
            file_path = self.ael_params.get("scenario_count_file_name")
            return self.getOutputFileName(True, file_path)
        else:
            return self.getOutputFileName(True)

    def scenario_dates_file_name(self):
        if "scenario_dates_file_name" in self.ael_params:
            file_path = self.ael_params.get("scenario_dates_file_name")
            return self.getOutputFileName(True, file_path)
        else:
            return self.getOutputFileName(True)

    def decay_factor_file_name(self):
        if "decay_factor_file_name" in self.ael_params:
            file_path = self.ael_params.get("decay_factor_file_name")
            return self.getOutputFileName(True, file_path)
        else:
            return self.getOutputFileName(True)


class MarketValueParameters(CommonParameters):
    """
    Helper class for all user defined parameters used for the market value
    calculations and reporting.
    """
    def _baseFileName(self):
        return self.ael_params.get("Market Value File Name", '')


class ThetaParameters(CommonParameters):
    """
    Helper class for all user defined parameters used for the market value
    calculations and reporting.
    """
    def _baseFileName(self):
        return self.ael_params.get("Theta File Name", '')


class PLParameters(CommonParameters):
    """
    Helper class for all user defined parameters used for the profit and
    loss calculations and reporting.
    """
    def total_pl_source(self):
        return self.ael_params.get("total_pl_source", 'Total')
        
    def daily_pl_source(self):
        return self.ael_params.get("daily_pl_source", 'DailyTotal')

    def clean_pl_source(self):
        return self.ael_params.get("clean_pl_source", 'Hypothetical')

    def _baseFileName(self):
        return self.ael_params.get("PL File Name", '')

    def do_create_report(self):
        if not super(PLParameters, self).do_create_report():
            return False
        return self.total_pl_source() != ''


def _calculate_distributed_mode(portfolios, tradeFilters, storedQueries, 
        columnConfigs, attributes, writers, distributedCalculations):
    
    try:
        FExportCalculatedValuesMain.main(portfolios, tradeFilters, 
                storedQueries, columnConfigs, attributes, writers, distributedCalculations)
    except Exception as err:
        print(" Exception in _calculate_distributed_mode {0}".format(str(err)))
        if distributedCalculations:
            print(" Try none distributed mode instead")
            FExportCalculatedValuesMain.main(portfolios, tradeFilters, 
                storedQueries, columnConfigs, attributes, writers)
    
class FMarketRiskExporterBase(FBDPWorld.WorldInterface):
    def __init__(self, ael_params, world):
        FBDPWorld.WorldInterface.__init__(self, world)
        self.params = self.buildParameters(ael_params)
        self.outputFilePath = self.params.getOutputFileName()
        self.writers = []

    def buildParameters(self, ael_params):
        raise NotImplementedError("Use derived class")

    def validateParameters(self):
        return self.params.do_create_report()

    def calculatedColumns(self):
        raise NotImplementedError("Use derived class")

    def createWriters(self):
        raise NotImplementedError("Use derived class")
    
    def createColumnConfigurations(self):
        columnConfigurations = []
        for custom, col in self.calculatedColumns().items():
            columnConfigurations.append(
                FExportCalculatedValuesMain.createColumnConfiguration(
                    columnID=col,
                    extensionContext=acm.GetDefaultContext(),
                    customName=custom))
        return columnConfigurations
    
    def configureExport(self):
        raise NotImplementedError("Use derived class")
    
    def export(self):
        self.configureExport()
        attributes = configureAttributes(self.params)
        _calculate_distributed_mode(self.params.portfolios(),
                self.params.tradeFilters(), self.params.storedQueries(),
                                         self.columnConfigurations,
                                         attributes,
                                         self.writers,
                                         self.params.distributedCalculations())
        for w in self.writers:
            w.write(self.params.overwrite(), self.outputFilePath)


class FMarketRiskMVExporter(FMarketRiskExporterBase):
    def buildParameters(self, ael_params):
        return MarketValueParameters(ael_params, 'Market Value', THEO_VAL, self._getWorldRef())

    def configureExport(self):
        self.columnConfigurations = self.createColumnConfigurations()
        self.createWriters()

    def calculatedColumns(self):
        return {"Market Value": self.params.columnName}

    def createWriters(self):
        if ExportToMemoryCube == self.params.export_fileformat():
            self.writers.append(FRiskCubeWriterBase.MarketValueWriter(
            self._getWorldRef(), self.params.separators(),
            self.params.horizon()))
        elif ExportToArtiQCube == self.params.export_fileformat():
            self.writers.append(FRiskCubeWriterBase.ArtiQMarketValueWriter(
            self._getWorldRef(), self.params.separators(), 
            self.params.horizon()))

class FMarketRiskThetaExporter(FMarketRiskExporterBase):
    def buildParameters(self, ael_params):
        return ThetaParameters(ael_params, 'Theta', THETA_PL, self._getWorldRef())

    def configureExport(self):
        self.columnConfigurations = self.createColumnConfigurations()
        self.createWriters()

    def calculatedColumns(self):
        return {"Theta": self.params.columnName}

    def createWriters(self):
        if ExportToMemoryCube == self.params.export_fileformat():
            self.writers.append(FRiskCubeWriterBase.ThetaWriter(
            self._getWorldRef(), self.params.separators(),
            self.params.horizon()))
        elif ExportToArtiQCube == self.params.export_fileformat():
            self.writers.append(FRiskCubeWriterBase.ArtiQThetaWriter(
            self._getWorldRef(), self.params.separators(),
            self.params.horizon()))

class FMarketRiskPnLExporter(FMarketRiskExporterBase):
    CALCULATED_COLUMNS = {"Total": TPL, "Hypothetical": CLEAN_PL, "Daily" : DAILY_PL}
    TOTAL = CALCULATED_COLUMNS["Total"]
    HYPO = CALCULATED_COLUMNS["Hypothetical"]
    DAILY = CALCULATED_COLUMNS["Daily"]
    # EnumPLStartDate = Yesterday
    CLEAN_PL_PARAM = {acm.FSymbol("PortfolioProfitLossStartDate"): 4}

    def buildParameters(self, ael_params):
        return PLParameters(ael_params, 'Profit and Loss', '', self._getWorldRef())

    def configureExport(self):
        self.columnConfigurations = self.createColumnConfigurations()
        self.createWriters()

    def calculatedColumns(self):
        columns = {FMarketRiskPnLExporter.TOTAL: self.params.total_pl_source()}
        if self.params.clean_pl_source():
            columns[FMarketRiskPnLExporter.HYPO] = self.params.clean_pl_source()
        if self.params.daily_pl_source():
            columns[FMarketRiskPnLExporter.DAILY] = self.params.daily_pl_source()
        return columns

    def createColumnConfigurations(self):
        columns = self.calculatedColumns()

        columnConfigurations = []

        columnConfigurations.append(
            FExportCalculatedValuesMain.createColumnConfiguration(
                columnID=FMarketRiskPnLExporter.TOTAL,
                extensionContext=acm.GetDefaultContext(),
                customName=columns[FMarketRiskPnLExporter.TOTAL]))

        if self.params.clean_pl_source():
            columnConfigurations.append(
                FExportCalculatedValuesMain.createColumnConfiguration(
                    columnID=FMarketRiskPnLExporter.HYPO,
                    extensionContext=acm.GetDefaultContext(),
                    customName=columns[FMarketRiskPnLExporter.HYPO],
                    parameters=FMarketRiskPnLExporter.CLEAN_PL_PARAM))
        
        if self.params.daily_pl_source():
            columnConfigurations.append(
                FExportCalculatedValuesMain.createColumnConfiguration(
                    columnID=FMarketRiskPnLExporter.DAILY,
                    extensionContext=acm.GetDefaultContext(),
                    customName=columns[FMarketRiskPnLExporter.DAILY]))
        
        return columnConfigurations

    def createWriters(self):
        if ExportToMemoryCube == self.params.export_fileformat():
            self.writers.append(FRiskCubeWriterBase.ProfitAndLossWriter(
            self._getWorldRef(), self.params.separators(),
            self.params.horizon()))
        elif ExportToArtiQCube == self.params.export_fileformat():
            self.writers.append(FRiskCubeWriterBase.ArtiQProfitAndLossWriter(
            self._getWorldRef(), self.params.separators(),
            self.params.horizon()))


class FMarketRiskStressExporter(FMarketRiskExporterBase):
    
    def __init__(self, ael_params, world):
        super(FMarketRiskStressExporter, self).__init__(ael_params, world)
        self.validScenarios = []
        self.log = world

    def _validateScenario(self, scenario):
        return True

    def buildParameters(self, ael_params):
        return StressParameters(ael_params, 'Stress', THEO_VAL, self._getWorldRef())

    def validateParameters(self):
        if not self.params.valid():
            self.log.logInfo("{0}: Invalid parameters.".format(
                self.__class__.__name__))
            return False

        if self.params.scenario_file_exists():
            return True
        
        if not self.params.stored_scenarios():
            return False
    
        for name in self.params.stored_scenarios():
            stored = acm.FStoredScenario.Select('name="{0}"'.format(name))[0]
            if not stored:
                self.log.logInfo("{0}: Invalid scenario name {1}. "
                        "Skipping.".format(self.__class__.__name__, name))
                continue
            scenario = stored.Scenario()
            if not self._validateScenario(scenario):
                self.log.logInfo("{0}: Invalid scenario "
                        "{1}. Skipping.".format(self.__class__.__name__, name))
                continue
            self.validScenarios.append(scenario)
        return len(self.validScenarios) != 0

    def configureExport(self):
        self.rfTypes =  self.params.risk_factor_types()
        self.scenarioFilePath = self.params.scenario_file()
        self.columnConfigurations = self.createColumnConfigurations()
        self.createWriters()

    def calculatedColumns(self):
        return {FRiskCubeWriterBase.STRESS_PV_CHANGE: self.params.columnName}

    def createWriters(self):
        if ExportToMemoryCube == self.params.export_fileformat():
            self.writers.append(FRiskCubeScenarioWriters.StressScenarioWriter(
            self._getWorldRef(), self.params.separators(),
            self.params.horizon(), self.params.stress_type()))
        elif ExportToArtiQCube == self.params.export_fileformat():
            self.writers.append(FRiskCubeScenarioWriters.ArtiQStressScenarioWriter(
            self._getWorldRef(), self.params.separators(),
            self.params.horizon(), self.params.stress_type()))
    
    def createVaRScenariosBasedOnFile(self):
        builder = acm.GetFunction("createRiskFactorScenarioBuilder", 0)()
        scenarios = []
        dimNames = []
        for frontType in self.rfTypes:
            riskType = self.getRiskType(frontType) 
            if not riskType:
                self._logInfo('{0}: Invalid risk factor type - {1}'.format(
                    self.__class__.__name__, frontType))
                continue
        
            if frontType != 'Total':
                num = acm.FACMServer().EnumFromString("RiskFactorType",
                        frontType)
            else:
                num = 0
            
            scen = builder.CreateScenario(self.scenarioFilePath, 0, 0, num)
            if not scen:
                self._logInfo("{3}: No {0} ({1} {2}) scenario".format(riskType,
                    frontType, num, self.__class__.__name__))
                continue
            scenarios.append(scen)
            dimNames.append([riskType])
        self._logInfo("Total dimNames {0}".format(dimNames))
        return scenarios, dimNames
    
    def createVaRScenariosBasedOnStoredScens(self):
        scenarios = []
        dimNames = []
        for scenario in self.validScenarios:
            scenarios.append(scenario)
            dimNames.append([scenario.Name()])
        return scenarios, dimNames
    
    def getRiskType(self, frontType):
        riskType = FRiskCubeScenarioWriters.StressScenarioWriter.RISK_FACTOR_TYPES.get(
                    frontType, '')
        return riskType

    def createVaRScenarios(self):
        if self.params.scenario_file_exists():
            return self.createVaRScenariosBasedOnFile()
        else:
            return self.createVaRScenariosBasedOnStoredScens()

    def createVaRColumns(self, scenarios, dimNames):
        columnConfigurations = []
        
        for scenario, dim in zip(scenarios, dimNames):
            #Note: affects everyone holding the same reference!
            scenario.DisplayType(DISPLAY_RELATIVE)
            columnConfigurations.append(
                CalcMain.createColumnConfiguration(
                   columnID=self.params.columnName,
                   extensionContext=acm.GetDefaultContext(),
                   customName=dim[0],
                   scenario=scenario,
                   scenarioDimensionNames=dim))
            self._logInfo("Creata column {0}".format(dim[0]))

        return columnConfigurations

    def createColumnConfigurations(self):
        scenarios, dimNames = self.createVaRScenarios()
        columnConfigurations = self.createVaRColumns(scenarios, dimNames)
        return columnConfigurations

    def export(self):
        self.configureExport()
        attributes = configureAttributes(self.params)
        _calculate_distributed_mode(self.params.portfolios(),
                self.params.tradeFilters(), self.params.storedQueries(),
                                         self.columnConfigurations,
                                         attributes,
                                         self.writers,
                                         self.params.distributedCalculations())
        for w in self.writers:
            w.write(self.params.overwrite(), self.outputFilePath)


class FMarketRiskVaRExporter(FMarketRiskStressExporter):
    def __init__(self, ael_params, world):
        super(FMarketRiskVaRExporter, self).__init__(ael_params, world)
        self.scenarioCountFilePath = ''
        self.scenarioDatesFilePath = ''
        self.decayFactorFilePath = ''
        self.validScenarios = []

    def _validateScenario(self, scenario):
        return True

    def buildParameters(self, ael_params):
        return PvScenarioParameters(ael_params, 'Value at Risk', THEO_VAL, self._getWorldRef())

    def configureExport(self):
        self.rfTypes =  self.params.risk_factor_types()
        self.scenarioFilePath = self.params.scenario_file()
        self.scenarioCountFilePath = self.params.scenario_count_file_name()
        self.scenarioDatesFilePath = self.params.scenario_dates_file_name()
        self.decayFactorFilePath = self.params.decay_factor_file_name()
        self.columnConfigurations = self.createColumnConfigurations()
        self.createWriters()

    def calculatedColumns(self):
        raise NotImplementedError("Not implemented in VaR Exporter")

    def createWriters(self):
        if ExportToMemoryCube == self.params.export_fileformat():
            self.writers.append(FRiskCubeScenarioWriters.VaRWriter(
            self._getWorldRef(), self.params.separators(),
            self.params.horizon(), self.params.var_type(),
            self.params.batchSize(),
            self.params.maxCalcTime(),
            self.params.decay_factor(), self.outputFilePath,
            self.scenarioCountFilePath, self.scenarioDatesFilePath,
            self.decayFactorFilePath, self.params.history(), False,
            self.params.overwrite()))
        elif ExportToArtiQCube == self.params.export_fileformat():
            self.writers.append(FRiskCubeScenarioWriters.ArtiQVaRWriter(
            self._getWorldRef(), self.params.separators(),
            self.params.horizon(), self.params.var_type(),
            self.params.batchSize(),
            self.params.maxCalcTime(),
            self.params.decay_factor(), self.outputFilePath,
            self.scenarioCountFilePath, self.scenarioDatesFilePath,
            self.decayFactorFilePath, self.params.history(), True,
            self.params.overwrite()))

    def getRiskType(self, frontType):
        riskType = FRiskCubeScenarioWriters.VaRWriter.RISK_FACTOR_TYPES.get(
                    frontType, '')
        return riskType
    
class StressGridParameters(CommonParameters):
    def __init__(self, aelParams, logger):
        super(StressGridParameters, self).__init__(aelParams, 'Stress Grid', THEO_VAL, logger)
        self.filePrefix = self.ael_params.get('stress_grid_file', '')
        self.scenarioNames = self.ael_params.get('stress_grid_scenarios', [])
        self.stressName = self.ael_params.get('stress_name', None)

    def valid(self):
        if not super(StressGridParameters, self).do_create_report():
            return False
        return self.scenarioNames and self.filePrefix

    def _baseFileName(self):
        return self.filePrefix

class StressGridExporter(object):
    scenarioWriters = {}

    @classmethod
    def _getScenarioWriter(cls, sceneType, exportType):
        if cls.scenarioWriters:
            return cls.scenarioWriters[sceneType][exportType]

        for sceneTypes, eType, writer in (
            ((STOCK_PRICE_SCENARIOS[0], STOCK_VOL_SCENARIOS[0]), ExportType[0], SpotVolWriter),
            ((STOCK_PRICE_SCENARIOS[0], STOCK_VOL_SCENARIOS[1]), ExportType[0], SpotVolWriter),
            ((STOCK_PRICE_SCENARIOS[0], STOCK_VOL_SCENARIOS_PERIODS[0]), ExportType[0], SpotVolTaperWriter),
            ((STOCK_PRICE_SCENARIOS[0], STOCK_VOL_SCENARIOS_PERIODS[1]), ExportType[0], SpotVolTaperWriter),
            ((STOCK_PRICE_SCENARIOS[1], STOCK_VOL_SCENARIOS_PERIODS[0]), ExportType[0], SpotVolTaperWriter),
            ((STOCK_PRICE_SCENARIOS[1], STOCK_VOL_SCENARIOS_PERIODS[1]), ExportType[0], SpotVolTaperWriter),
            ((STOCK_VOL_SCENARIOS[0], YIELD_CURVE_SCENARIO), ExportType[0], IRVolWriter),
            ((STOCK_VOL_SCENARIOS[1], YIELD_CURVE_SCENARIO), ExportType[0], IRVolWriter),
            ((YIELD_CURVE_SCENARIO), ExportType[0], IRVolWriter),
            ((YIELD_CURVE_SCENARIO), ExportType[0], IRVolWriter),
            ((FX_SCENARIO, STOCK_VOL_SCENARIOS[0]), ExportType[0], FXVolWriter),
            ((FX_SCENARIO, STOCK_VOL_SCENARIOS[1]), ExportType[0], FXVolWriter),
            ((FX_SCENARIO, STOCK_VOL_SCENARIOS_PERIODS[0]), ExportType[0], FXVolTaperWriter),
            ((FX_SCENARIO, STOCK_VOL_SCENARIOS_PERIODS[1]), ExportType[0], FXVolTaperWriter),
            ((FX_SCENARIO,), ExportType[0], FXMatrixWriter),
            ((STOCK_PRICE_SCENARIOS[0], STOCK_VOL_SCENARIOS[0]), ExportType[1], ArtiQSpotVolWriter),
            ((STOCK_PRICE_SCENARIOS[0], STOCK_VOL_SCENARIOS[1]), ExportType[1], ArtiQSpotVolWriter),
            ((STOCK_PRICE_SCENARIOS[0], STOCK_VOL_SCENARIOS_PERIODS[0]), ExportType[1], ArtiQSpotVolTaperWriter),
            ((STOCK_PRICE_SCENARIOS[0], STOCK_VOL_SCENARIOS_PERIODS[1]), ExportType[1], ArtiQSpotVolTaperWriter),
            ((STOCK_PRICE_SCENARIOS[1], STOCK_VOL_SCENARIOS_PERIODS[0]), ExportType[1], ArtiQSpotVolTaperWriter),
            ((STOCK_PRICE_SCENARIOS[1], STOCK_VOL_SCENARIOS_PERIODS[1]), ExportType[1], ArtiQSpotVolTaperWriter),
            ((STOCK_VOL_SCENARIOS[0], YIELD_CURVE_SCENARIO), ExportType[1], ArtiQIRVolWriter),
            ((STOCK_VOL_SCENARIOS[1], YIELD_CURVE_SCENARIO), ExportType[1], ArtiQIRVolWriter),
            ((YIELD_CURVE_SCENARIO), ExportType[1], ArtiQIRVolWriter),
            ((YIELD_CURVE_SCENARIO), ExportType[1], ArtiQIRVolWriter),
            ((FX_SCENARIO, STOCK_VOL_SCENARIOS[0]), ExportType[1], ArtiQFXVolWriter),
            ((FX_SCENARIO, STOCK_VOL_SCENARIOS[1]), ExportType[1], ArtiQFXVolWriter),
            ((FX_SCENARIO, STOCK_VOL_SCENARIOS_PERIODS[0]), ExportType[1], ArtiQFXVolTaperWriter),
            ((FX_SCENARIO, STOCK_VOL_SCENARIOS_PERIODS[1]), ExportType[1], ArtiQFXVolTaperWriter),
            ((FX_SCENARIO,), ExportType[1], ArtiQFXMatrixWriter)):
            if sceneTypes in cls.scenarioWriters:
                cls.scenarioWriters[sceneTypes][eType] = writer
            else:
                cls.scenarioWriters[sceneTypes] = {}
                cls.scenarioWriters[sceneTypes][eType] = writer
        assert sceneType in cls.scenarioWriters, ("Invalid scenario type "
                "{0}".format(sceneType))
        return cls.scenarioWriters[sceneType][exportType]

    @classmethod
    def _getDimensionNames(cls, sceneType, scenario):
        dimNames = []
        dimensions = scenario.ShiftDimensions()
        # Should have been validated.
        assert dimensions.Size() < 3, ("Invalid no. of dimensions {0}.".format(
            dimensions.Size()))
        for i, dim in enumerate(dimensions):
            vectors = dim.ShiftVectors()
            assert vectors.Size() == 1, "Invalid scenario shifts."
            vect = vectors.At(0)
            objType = vect.EntitiesGroupItem()
            dname = cls._getScenarioWriter(sceneType, acm.FSymbol(ExportToMemoryCube)).SHIFT_TYPES.get(
                    objType, '')
            assert dname, "Invalid object type on dimension {0}.".format(i)
            dimNames.append(dname)
        return dimNames

    def createColumns(self, sceneType, scenario):
        # Boilerplate you need (for now?) to actually register scenarios on a
        # column creator.
        dimNames = StressGridExporter._getDimensionNames(sceneType, scenario)
        
        #Note: affects everyone holding the same reference!
        scenario.DisplayType(DISPLAY_RELATIVE)
        
        columnConfigurations = []
        
        columnConfigurations.append(
            CalcMain.createColumnConfiguration(
               columnID=self.params.columnName,
               extensionContext=acm.GetDefaultContext(),
               customName=FRiskCubeWriterBase.STRESS_PV_CHANGE,
               scenario=scenario,
               scenarioDimensionNames=dimNames))
        
        return columnConfigurations

    def __init__(self, aelParams, log):
        self.log = log
        self.params = StressGridParameters(aelParams, log)
        # List of (scenarioType, scenario) tuples.
        self.validScenarios = []

    def _validFXScenario(self, scenario, vector):
        shiftType = vector.Function()
        if not shiftType == FX_RELATIVE:
            self.log.logInfo("{0}: Shift on {1} scenario, {2}, must "
                    "be of type {3}, not {4}".format(
                        self.__class__.__name__, FX_SCENARIO,
                        scenario.Name(), FX_RELATIVE, shiftType))
            return None

        currencies = set([vector.At(i).Parameters().At(acm.FSymbol('currency'))
                for i in range(vector.Size())])
        if not len(currencies) == 1:
            self.log.logInfo("{0}: {1} scenario {2} should be defined for "
                    "only 1 currency. Found {3} - {4}.".format(
                        self.__class__.__name__, FX_SCENARIO, scenario.Name(),
                        len(currencies), [c.Name() for c in currencies]))
            return None
        return FX_SCENARIO

    def _validateScenario(self, scenario):
        name = scenario.Name()
        dimensions = scenario.ShiftDimensions() # ExplicitDimensions()
        if not dimensions:
            self.log.logInfo("{0}: Scenario {1} has no dimensions.".format(
                self.__class__.__name__, name))
            return None

        if not any([dim.ShiftVectors() for dim in dimensions]):
            self.log.logInfo("{0}: Scenario {1} has no shifts defined.".format(
                self.__class__.__name__, name))
            return None

        if dimensions.Size() > 2:
            self.log.logInfo("{0}: Scenario has {1} dimensions - expecting 2 "
                    "dimensions max.".format(name, dimensions.Size()))
            return None

        found = []
        sceneType = None
        for i, dim in enumerate(dimensions):
            vectors = dim.ShiftVectors()
            if vectors.Size() != 1:
                self.log.logInfo("{0}: Scenario {1} - only 1 set of shifts can "
                        "be defined on each dimension - found {2} on "
                        "dimension {3}.".format(self.__class__.__name__, name,
                            vectors.Size(), i))
                return None

            vect = vectors.At(0)

            sceneType = vect.EntitiesGroupItem()
            if sceneType == FX_SCENARIO:
                if self._validFXScenario(scenario, vect):
                    found.append(sceneType)
                    continue
                else:
                    return None

            if not sceneType in STOCK_PRICE_SCENARIOS + STOCK_VOL_SCENARIOS \
                        + [YIELD_CURVE_SCENARIO]:
                self.log.logInfo("{0}: Invalid scenario type {1} on dimension "
                        "{2} of scenario {3}.".format(self.__class__.__name__,
                            sceneType, i, name))
                return None

            shiftType = vect.Function()
            if not shiftType in [SPOT_VOL_RELATIVE,
                    SPOT_VOL_ABSOLUTE_PERCENT_POINTS,
                    SPOT_VOL_ABSOLUTE_BASIS_POINTS, SPOT_VOL_PERIODS] and \
                    sceneType in STOCK_PRICE_SCENARIOS + STOCK_VOL_SCENARIOS:
                self.log.logInfo("{0}: Shifts on scenario {1} must be "
                        "defined in '% Relative', not {2} terms.".format(
                            self.__class__.__name__, name, vect.Function()))
                return None

            if sceneType in STOCK_VOL_SCENARIOS and \
                        shiftType == SPOT_VOL_PERIODS:
                sceneType = acm.FSymbol(sceneType.Text() + shiftType)

            if sceneType in found:
                self.log.logInfo("{0}: Both dimensions in scenario {1} "
                        "have the same {2} type.".format(
                            self.__class__.__name__, name, sceneType))
                return None

            found.append(sceneType)
        return tuple(sorted(found))

    def validateParameters(self):
        if not self.params.valid():
            self.log.logInfo("{0}: Invalid parameters.".format(
                self.__class__.__name__))
            return False

        for name in self.params.scenarioNames:
            storedScenarios = acm.FStoredScenario.Select('name="{0}"'.format(name))
            stored = None
            if storedScenarios:
                stored = storedScenarios[0]
            if not stored:
                self.log.logInfo("{0}: Invalid scenario name {1}. "
                        "Skipping.".format(self.__class__.__name__, name))
                continue
            scenario = stored.Scenario()
            sceneType = self._validateScenario(scenario)
            if not sceneType:
                self.log.logInfo('{0}: Invalid spot-vol scenario {1}. '
                        'Skipping.'.format(self.__class__.__name__, name))
                continue
            self.validScenarios.append((sceneType, scenario))
        return self.validScenarios

    def export(self):
        attributes = configureAttributes(self.params)
        for sceneType, scenario in self.validScenarios:
            columns = self.createColumns(sceneType, scenario)
            cls = self._getScenarioWriter(sceneType, acm.FSymbol(self.params.export_fileformat()))
            writer = cls(scenario, self.params.stressName,
                    self.log, self.params.separators())
            _calculate_distributed_mode(self.params.portfolios(),
                    self.params.tradeFilters(),
                    self.params.storedQueries(),
                    columns, attributes, [writer],
                    self.params.distributedCalculations())
            filepath = self.params._extendedFileName(scenario.Name())
            writer.write(self.params.overwrite(), filepath)

class VegaParameters(CommonParameters):
    def __init__(self, aelParams, tab_name, default_column, logger):
        super(VegaParameters, self).__init__(aelParams, tab_name, default_column, logger)

    def valid(self):
        if not super(VegaParameters, self).do_create_report():
            return False
        if not self._baseFileName():
            return False
        return True

    def _baseFileName(self):
        return self.ael_params.get('vega_file', '')


class IRDeltaParameters(CommonParameters):
    def __init__(self, aelParams, tab_name, default_column, logger):
        super(IRDeltaParameters, self).__init__(aelParams,
                                tab_name, default_column, logger)
        self.yieldCurves = self.ael_params.get('yield_curves', [])
        self.stressName = self.ael_params.get(
                                'stress_name_parallel', None)
        
    def valid(self):
        if not super(IRDeltaParameters, self).do_create_report():
            return False
        if not self._baseFileName():
            return False
        return True

    def _baseFileName(self):
        return self.ael_params.get('parallel_shift_file', '')


class IRDeltaExporter(FMarketRiskExporterBase):

    def __init__(self, aelParams, log):
        self.log = log
        self.params = IRDeltaParameters(aelParams, 'Delta', YIELD_DELTA, log)
        if ExportToMemoryCube == self.params.export_fileformat():
            self.writers = [IRDeltaWriter(self.params.stressName, 
                        self.log, self.params.separators())]
        elif ExportToArtiQCube == self.params.export_fileformat():
            self.writers = [ArtiQIRDeltaWriter(self.params.stressName, 
                        self.log, self.params.separators())]
        
    def validateParameters(self):
        if not self.params.valid():
            self.log.logInfo("{0}: Invalid parameters.".format(
                self.__class__.__name__))
            return False
        return True

    def _curveParam(self, curveName):
        yc = acm.FYieldCurve[curveName]
        if not yc:
            self._logInfo('{0}: Invalid yield curve - {1}. Skipping.'.format(
                self.__class__.__name__, curveName))
            return None
        # Each key in the dictionary should be the name of a
        # FColumnParameterDefinition instance found in the Extension Manager,
        # and each value should be the corresponding value for that parameter
        return {YIELD_CURVE_FILTER: yc,}
    
    def createColumns(self):
        yieldCurves = set(self.params.yieldCurves)
    
        columnConfigurations = []

        if not yieldCurves or yieldCurves.intersection(ALL_CURVES):
            yieldCurves = yieldCurves.difference(ALL_CURVES)
            
            columnConfigurations.append(
                CalcMain.createColumnConfiguration(
                    columnID=self.params.columnName,
                    extensionContext=acm.GetDefaultContext(),
                    customName='All Curves'))

        for name in yieldCurves:
            paramDict = self._curveParam(name)
            if not paramDict:
                continue
            columnConfigurations.append(
                CalcMain.createColumnConfiguration(
                    columnID=self.params.columnName,
                    extensionContext=acm.GetDefaultContext(),
                    customName=name,
                    parameters=paramDict))

        return columnConfigurations

    def export(self):
        columns = self.createColumns()
        attributes = configureAttributes(self.params)
        _calculate_distributed_mode(self.params.portfolios(),
                self.params.tradeFilters(),
                self.params.storedQueries(),
                columns,
                attributes,
                self.writers,
                self.params.distributedCalculations())
        filepath = self.params.getOutputFileName()
        for w in self.writers:
            w.write(self.params.overwrite(), filepath)


class GreeksParameters(CommonParameters):
    def __init__(self, aelParams, tab_name, default_column, logger):
        super(GreeksParameters, self).__init__(aelParams, tab_name, default_column, logger)
        self.measures = self.ael_params.get('measures_Greeks', 'Delta')
        self.logger = logger
        
    def valid(self):
        if not super(GreeksParameters, self).do_create_report():
            return False
        if not self._baseFileName():
            return False
        if len(self.measures) != len(self.columnName):
            self.logger.logInfo("Mismatch of the measures {0} and the selected columns {1} in GreeksParameters".format(
                self.measures, self.columnName))
            return False
        return True

    def _baseFileName(self):
        return self.ael_params.get('greeks_file', '')

   
class GreeksExporter(FMarketRiskExporterBase):

    def __init__(self, aelParams, log):
        self.log = log
        self.params = GreeksParameters(aelParams, 'Greeks', PORTFOLIO_DELTA, log)
        

    def validateParameters(self):
        if not self.params.valid():
            self.log.logInfo("{0}: Invalid parameters.".format(
                self.__class__.__name__))
            return False
        return True
    
    def createColumns(self):
        columnConfigurations = []
        for cName in list(self.params.columnName):
            columnConfigurations.append(
                CalcMain.createColumnConfiguration(
                    columnID=cName,
                    extensionContext=acm.GetDefaultContext(),
                    customName=cName))

        return columnConfigurations

    def export(self):
        attributes = configureAttributes(self.params)
        columns = self.createColumns()
        writers=[]
        if ExportToMemoryCube ==  self.params.export_fileformat():
            writers.append(GreekWriter(self.params.measures,\
                    self.params.columnName,\
                    self.log, self.params.separators()))
        elif ExportToArtiQCube == self.params.export_fileformat():
            writers.append(ArtiQGreekWriter(self.params.measures,\
                    self.params.columnName,\
                    self.log, self.params.separators()))
        _calculate_distributed_mode(self.params.portfolios(),
                self.params.tradeFilters(),
                self.params.storedQueries(),
                columns,
                attributes,
                writers,
                self.params.distributedCalculations())
        filepath = self.params.getOutputFileName()
        for w in writers:
            w.write(self.params.overwrite(), filepath)


class VegaExporter(FMarketRiskExporterBase):

    def __init__(self, aelParams, log):
        self.log = log
        self.params = VegaParameters(aelParams, 'Vega', VEGA, log)

    def validateParameters(self):
        if not self.params.valid():
            self.log.logInfo("{0}: Invalid parameters.".format(
                self.__class__.__name__))
            return False
        return True
    
    def createColumns(self):
    
        columnConfigurations = []
        columnConfigurations.append(
                CalcMain.createColumnConfiguration(
                    columnID=self.params.columnName,
                    extensionContext=acm.GetDefaultContext(),
                    customName='Vega'))

        return columnConfigurations

    def export(self):
        attributes = configureAttributes(self.params)
        columns = self.createColumns()
        writers=[]
        if ExportToMemoryCube ==  self.params.export_fileformat():
            writers.append(VegaWriter(self.log, self.params.separators()))
        elif ExportToArtiQCube == self.params.export_fileformat():
            writers.append(ArtiQVegaWriter(self.log, self.params.separators()))
    
        _calculate_distributed_mode(self.params.portfolios(),
                self.params.tradeFilters(),
                self.params.storedQueries(),
                columns,
                attributes,
                writers,
                self.params.distributedCalculations())
        filepath = self.params.getOutputFileName()
        for w in writers:
            w.write(self.params.overwrite(), filepath)


class CreditDeltaParameters(CommonParameters):
    # Enums to AEL variable names
    PARAMS = {CREDIT_DAY_COUNT: "creditDayCount",
            CREDIT_RATE_TYPE: "creditRateType",
            CREDIT_FREQUENCY: "creditFrequency"}

    def _baseFileName(self):
        return self.ael_params.get("creditOutputFile", '')

    def _validCreditParams(self):
        return all([self.ael_params.get(param, None)
            for param in self.PARAMS.values()])

    def getCreditParams(self):
        return dict([(k, self.ael_params[v]) for k, v in self.PARAMS.items()])

    def valid(self):
        if not super(CreditDeltaParameters, self).do_create_report():
            return False
        if not self._baseFileName():
            return False
        if not self._validCreditParams():
            return False
        return True


class CreditDeltaExporter(FMarketRiskExporterBase):
    def __init__(self, aelParams, log):
        self.log = log
        self.params = CreditDeltaParameters(aelParams, 'Credit', CREDIT_DELTA,
                log)

    def validateParameters(self):
        if not self.params.valid():
            self.log.logInfo("{0}: Invalid parameters.".format(
                self.__class__.__name__))
            return False
        return True

    def createColumns(self):
        paramDict = self.params.getCreditParams()
        return [CalcMain.createColumnConfiguration(
                        columnID=CREDIT_DELTA,
                        extensionContext=acm.GetDefaultContext(),
                        customName='Delta',
                        parameters=paramDict)]

    def export(self):
        attributes = configureAttributes(self.params)
        columns = self.createColumns()
        writers=[]
        if ExportToMemoryCube == self.params.export_fileformat():
            writers.append(CreditDeltaWriter(self.log, self.params.separators()))
        elif ExportToArtiQCube == self.params.export_fileformat():
            writers.append(ArtiQCreditDeltaWriter(self.log, self.params.separators()))
        _calculate_distributed_mode(self.params.portfolios(),
                self.params.tradeFilters(),
                self.params.storedQueries(),
                columns,
                attributes,
                writers,
                self.params.distributedCalculations())
        filepath = self.params.getOutputFileName()
        for w in writers:
            w.write(self.params.overwrite(), filepath)



class IRBucketDeltaParameters(IRDeltaParameters):
    def __init__(self, aelParams, tab_name, default_column, logger):
        super(IRBucketDeltaParameters, self).__init__(aelParams, tab_name, default_column, logger)
        self.storedBuckets = set(self.ael_params.get('time_buckets', []))
        self.stressName = self.ael_params.get(
                                'stress_name_timebucket', None)

    def valid(self):
        return (super(IRBucketDeltaParameters, self).valid()
                and self.storedBuckets)

    def _baseFileName(self):
        return self.ael_params.get('bucket_shift_file')


class IRBucketDeltaExporter(IRDeltaExporter):

    def __init__(self, aelParams, log):
        self.log = log
        self.params = IRBucketDeltaParameters(aelParams, 'Delta', YIELD_DELTA_BUCKET, log)
        if ExportToMemoryCube == self.params.export_fileformat():
            self.writers = [IRBucketDeltaWriter(self.params.stressName, self.log,
                self.params.separators())]
        elif ExportToArtiQCube == self.params.export_fileformat():
            self.writers = [ArtiQIRBucketDeltaWriter(self.params.stressName, self.log,
                self.params.separators())]
    
    def createColumns(self, timeBuckets):
        yieldCurves = set(self.params.yieldCurves)
        columnConfigurations = []
        
        if not yieldCurves or yieldCurves.intersection(ALL_CURVES):
            yieldCurves = yieldCurves.difference(ALL_CURVES)

            columnConfigurations.append(
                CalcMain.createColumnConfiguration(
                    columnID=self.params.columnName,
                    extensionContext=acm.GetDefaultContext(),
                    customName='All Curves',
                    timebuckets=timeBuckets))
            
        for name in yieldCurves:
            paramDict = self._curveParam(name)
            if not paramDict:
                continue
            
            columnConfigurations.append(
                CalcMain.createColumnConfiguration(
                    columnID=self.params.columnName,
                    extensionContext=acm.GetDefaultContext(),
                    customName=name,
                    timebuckets=timeBuckets,
                    parameters=paramDict))

        return columnConfigurations
   
    def _curveParam(self, curveName):
        yc = acm.FYieldCurve[curveName]
        if not yc:
            self._logInfo('{0}: Invalid yield curve - {1}. Skipping.'.format(
                self.__class__.__name__, curveName))
            return None
        # Each key in the dictionary should be the name of a
        # FColumnParameterDefinition instance found in the Extension Manager,
        # and each value should be the corresponding value for that parameter
        if 'Benchmark Delta' in self.params.columnName:
            return {BENCHMARK_CURVE_FILTER: yc,}
        else:
            return {YIELD_CURVE_FILTER: yc,}

    def export(self):
        attributes = configureAttributes(self.params)
        for name in self.params.storedBuckets:
            stored = acm.FStoredTimeBuckets.Select('name="{0}"'.format(name))
            if not stored or not stored[0]:
                self.log.logInfo("{0}: Invalid time bucket name {1}. "
                        "Skipping.".format(self.__class__.__name__, name))
                continue
            timeBuckets = stored[0].TimeBuckets()
            columns = self.createColumns(timeBuckets)
            
            _calculate_distributed_mode(self.params.portfolios(),
                    self.params.tradeFilters(),
                    self.params.storedQueries(),
                    columns,
                    attributes,
                    self.writers,
                    self.params.distributedCalculations())
            filepath = self.params._extendedFileName(name)
            for w in self.writers:
                w.write(self.params.overwrite(), filepath)


class IRTwistDeltaParameters(IRDeltaParameters):
    def __init__(self, aelParams, tab_name, default_column, logger):
        super(IRTwistDeltaParameters, self).__init__(aelParams, tab_name, default_column, logger)
        self.scenarioNames = self.ael_params.get('twist_scenarios', [])
        self.stressName = ''

    def valid(self):
        if not super(IRTwistDeltaParameters, self).valid():
            return False
        if not self.scenarioNames:
            return False
        return True

    def _baseFileName(self):
        return self.ael_params.get('curve_twist_file')


class IRTwistDeltaExporter(IRDeltaExporter):
    def __init__(self, aelParams, log):
        self.log = log
        self.params = IRTwistDeltaParameters(aelParams, 'Delta', YIELD_DELTA, log)
        self.validScenarios = []
        if ExportToMemoryCube == self.params.export_fileformat():
            self.writers = [IRTwistDeltaWriter(self.params.stressName, self.log,
            self.params.separators())]
        elif ExportToArtiQCube == self.params.export_fileformat():
            self.writers = [ArtiQIRTwistDeltaWriter(self.params.stressName, self.log,
            self.params.separators())]

    def _validateScenario(self, scenario):
        name = scenario.Name()
        dimensions = scenario.ShiftDimensions()
        if not dimensions:
            self.log.logInfo("{0}: Scenario {1} has no dimensions.".format(
                self.__class__.__name__, name))
            return False

        if not any([dim.ShiftVectors() for dim in dimensions]):
            self.log.logInfo("{0}: Scenario {1} has no shifts defined.".format(
                self.__class__.__name__, name))
            return False

        for i, dim in enumerate(dimensions):
            if dim.Cardinality() != 1:
                self.log.logInfo("{0}: Scenario {1} - expecting 1 axis on "
                        "dimension {2}. Got {3}.".format(
                            self.__class__.__name__, name, i,
                            dim.Cardinality()))
                return False

            vectors = dim.ShiftVectors()
            if not vectors:
                continue

            if any([vect.EntitiesGroupItem() == YIELD_CURVE_SCENARIO
                for vect in vectors]):
                return True
        return False

    def validateParameters(self):
        if not self.params.valid():
            self.log.logInfo("{0}: Invalid parameters.".format(
                self.__class__.__name__))
            return False

        for name in self.params.scenarioNames:
            stored = acm.FStoredScenario.Select('name="{0}"'.format(name))[0]
            if not stored:
                self.log.logInfo("{0}: Invalid scenario name {1}. "
                        "Skipping.".format(self.__class__.__name__, name))
                continue
            scenario = stored.Scenario()
            if not self._validateScenario(scenario):
                self.log.logInfo("{0}: Invalid interest rate twist scenario "
                        "{1}. Skipping.".format(self.__class__.__name__, name))
                continue
            self.validScenarios.append(scenario)
        return self.validScenarios

    def createColumns(self, scenario):
        yieldCurves = set(self.params.yieldCurves)
    
        nDims = len(scenario.ShiftDimensions())
        dimNames = ['_'.join([scenario.Name(), str(i)])
                    for i in range(nDims)]
        scenario.DisplayType(scenario.DefaultSettings().ShiftDisplayType())
        columnConfigurations = []

        if not yieldCurves or yieldCurves.intersection(ALL_CURVES):
            yieldCurves = yieldCurves.difference(ALL_CURVES)
            
            colName='{0}_{1}'.format('All Curves', scenario.Name()) 
            
            columnConfigurations.append(
                CalcMain.createColumnConfiguration(
                    columnID=self.params.columnName,
                    extensionContext=acm.GetDefaultContext(),
                    customName=colName,
                    scenario=scenario,
                    scenarioDimensionNames=dimNames))

        for name in yieldCurves:
            paramDict = self._curveParam(name)
            if not paramDict:
                continue
            
            colName='{0}_{1}'.format(name, scenario.Name())
            
            columnConfigurations.append(
                CalcMain.createColumnConfiguration(
                    columnID=self.params.columnName,
                    extensionContext=acm.GetDefaultContext(),
                    customName=colName,
                    parameters=paramDict,
                    scenario=scenario,
                    scenarioDimensionNames=dimNames))

        return columnConfigurations
    

    def export(self):
        columns = []
        attributes = configureAttributes(self.params)
        for scenario in self.validScenarios:
            columns.extend(self.createColumns(scenario))

        _calculate_distributed_mode(self.params.portfolios(),
                self.params.tradeFilters(),
                self.params.storedQueries(),
                columns, attributes, self.writers,
                self.params.distributedCalculations())
        filepath = self.params.getOutputFileName()
        for w in self.writers:
            w.write(self.params.overwrite(), filepath)

class IRParallelShiftDeltaParameters(IRDeltaParameters):
    def __init__(self, aelParams, tab_name, default_column, logger):
        super(IRParallelShiftDeltaParameters, self).__init__(aelParams, tab_name, default_column, logger)

        self.yieldCurves = self.ael_params.get('yield_curves_parallel', [])
        self.stressName = self.ael_params.get(
                                'stress_name_parallel', None)
        self.measurement = self.ael_params.get(
                                'measurement_parallel_shift', None)
    
    def _baseFileName(self):
        return self.ael_params.get('parallel_shift_file', '')

    def _measurement(self):
        return  self.measurement
    
class IRParallelShiftDeltaExporter(IRDeltaExporter):

    def __init__(self, aelParams, log):
        self.log = log
        self.params = IRParallelShiftDeltaParameters(aelParams, 'Parallel Shift Sensitivity', {YIELD_DELTA}, log)
        self.attributes = self.params.grouper
        self.writers = [ArtiQIRParallelShiftWriter(self.params._measurement(), self.params.stressName, 
                        self.log, self.params.separators())]

    def createColumns(self):
        columnConfigurations = []
        yieldCurves = set(self.params.yieldCurves)
        for cName in list(self.params.columnName):
            if not yieldCurves or yieldCurves.intersection(ALL_CURVES):
                yieldCurves = yieldCurves.difference(ALL_CURVES)
                columnConfigurations.append(
                    CalcMain.createColumnConfiguration(
                        columnID=cName,
                        extensionContext=acm.GetDefaultContext(),
                        customName=cName + ':' + 'All Curves'))
    
            for name in yieldCurves:
                paramDict = self._curveParam(name)
                if not paramDict:
                    continue
                columnConfigurations.append(
                    CalcMain.createColumnConfiguration(
                        columnID=cName,
                        extensionContext=acm.GetDefaultContext(),
                        customName=cName + ':' + name,
                        parameters=paramDict))

        return columnConfigurations

class IRBucketShiftParameters(IRBucketDeltaParameters):
    def __init__(self, aelParams, tab_name, default_column, logger):
        super(IRBucketShiftParameters, self).__init__(aelParams, tab_name, default_column, logger)
        self.storedBuckets = set(self.ael_params.get('time_buckets', []))
        self.stressName = self.ael_params.get(
                                'stress_name_timebucket', None)
        self.yieldCurves = self.ael_params.get('yield_curves_timebucket', [])
        self.measurement = self.ael_params.get(
                                'measurement_timebucket', 'Delta')
    
    def _measurement(self):
        return self.measurement
    
        
class IRBucketShiftExporter(IRBucketDeltaExporter):

    def __init__(self, aelParams, log):
        self.log = log
        self.params = IRBucketShiftParameters(aelParams, 'Bucket Shift Sensitivity', {YIELD_DELTA_BUCKET}, log)
        self.attributes = self.params.grouper
        self.writers= [ArtiQIRBucketShiftWriter(self.params._measurement(), self.params.stressName, self.log,
                        self.params.separators())]
            
    def createColumns(self, timeBuckets):
        yieldCurves = set(self.params.yieldCurves)
        columnConfigurations = []
        for cName in list(self.params.columnName):
            if not yieldCurves or yieldCurves.intersection(ALL_CURVES):
                yieldCurves = yieldCurves.difference(ALL_CURVES)
                columnConfigurations.append(
                    CalcMain.createColumnConfiguration(
                        columnID=cName,
                        extensionContext=acm.GetDefaultContext(),
                        customName=cName + ':' + 'All Curves',
                        timebuckets=timeBuckets))
                
            for name in yieldCurves:
                paramDict = self._curveParam(name)
                if not paramDict:
                    continue
                columnConfigurations.append(
                    CalcMain.createColumnConfiguration(
                        columnID=cName,
                        extensionContext=acm.GetDefaultContext(),
                        customName=cName + ':' + name,
                        timebuckets=timeBuckets,
                        parameters=paramDict))

        return columnConfigurations
    
class IRTwistShiftParameters(IRTwistDeltaParameters):
    def __init__(self, aelParams, tab_name, default_column, logger):
        super(IRTwistShiftParameters, self).__init__(aelParams, tab_name, default_column, logger)
        self.yieldCurves = self.ael_params.get('yield_curves_twist', [])
        self.measurement = self.ael_params.get('measurement_twist', None)
    
    def _measurement(self):
        return self.measurement

class IRTwistShiftExporter(IRTwistDeltaExporter):
    def __init__(self, aelParams, log):
        self.log = log
        self.params = IRTwistShiftParameters(aelParams, 'Twist Sensitivity', {YIELD_DELTA}, log)
        self.validScenarios = []
        self.attributes = self.params.grouper
        self.writers = [ArtiQIRTwistShiftWriter(self.params._measurement(), self.params.stressName, self.log,
            self.params.separators())]

    def createColumns(self, scenario):
        yieldCurves = set(self.params.yieldCurves)
    
        nDims = len(scenario.ShiftDimensions())
        dimNames = ['_'.join([scenario.Name(), str(i)])
                    for i in range(nDims)]
        scenario.DisplayType(scenario.DefaultSettings().ShiftDisplayType())
        
        columnConfigurations = []
        for cName in list(self.params.columnName):
            if not yieldCurves or yieldCurves.intersection(ALL_CURVES):
                yieldCurves = yieldCurves.difference(ALL_CURVES)
                colName='{0}:{1}_{2}'.format(cName, 'All Curves', scenario.Name()) 
                columnConfigurations.append(
                    CalcMain.createColumnConfiguration(
                        columnID=cName,
                        extensionContext=acm.GetDefaultContext(),
                        customName=colName,
                        scenario=scenario,
                        scenarioDimensionNames=dimNames))

            for name in yieldCurves:
                paramDict = self._curveParam(name)
                if not paramDict:
                    continue
            
                colName='{0}:{1}_{2}'.format(cName, name, scenario.Name())
            
                columnConfigurations.append(
                    CalcMain.createColumnConfiguration(
                        columnID=cName,
                        extensionContext=acm.GetDefaultContext(),
                        customName=colName,
                        parameters=paramDict,
                        scenario=scenario,
                        scenarioDimensionNames=dimNames))
        return columnConfigurations

class CustomParameters(CommonParameters):
    TABNAME = 'Custom'
    DEFAULT_COLUMN = 'Portfolio Delta Yield Full Per Currency'
    DEFAULT_WRITER = 'VectorWriter'

    def __init__(self, aelParams, log):
        super(CustomParameters, self).__init__(aelParams,
                CustomParameters.TABNAME, CustomParameters.DEFAULT_COLUMN, log)
        self.exportName = self.ael_params.get("exportName", '')
        self.columnName = self.ael_params.get('column_name_{0}'.format(
            CustomParameters.TABNAME), CustomParameters.DEFAULT_COLUMN)
        self.writerName = self.ael_params.get('customWriter',
                CustomParameters.DEFAULT_WRITER)

    def _baseFileName(self):
        return self.ael_params.get("customFileName", '')

    def valid(self):
        if not super(CustomParameters, self).do_create_report():
            return False
        if not self._baseFileName():
            self._logInfo("No output file specified.")
            return False
        return True


class CustomExporter(FMarketRiskExporterBase):
    def __init__(self, aelParams, log):
        self.log = log
        self.params = CustomParameters(aelParams, log)
        try:
            cls = getattr(FRiskCubeCustomWriters, self.params.writerName)
            self.writer = cls(self.log, self.params.separators()) if cls else None
            self.columnParams = self.writer.getColumnParameters()
        except:
            pass 

    def validateParameters(self):
        if not self.params.valid() or not self.writer:
            return False
        if self.writer.hasColumnParameters() and not self.columnParams:
            return False
        return True

    def createColumns(self):
        columnConfigurations = []
        for param in self.columnParams:
            config = CalcMain.createColumnConfiguration(
                    columnID=self.params.columnName,
                    extensionContext=acm.GetDefaultContext(),
                    vector={"currenciesSetExternally": param, },
                    customName=param.Name())
            columnConfigurations.append(config)
        return columnConfigurations
        
    def export(self):
        attributes = configureAttributes(self.params)
        columns = self.createColumns()
        _calculate_distributed_mode(self.params.portfolios(),
                self.params.tradeFilters(), self.params.storedQueries(),
                columns, attributes, [self.writer],
                self.params.distributedCalculations())

        filepath = self.params.getOutputFileName()
        self.writer.write(self.params.overwrite(), filepath)

class RiskFactorParameters(CommonParameters):
    TABNAME = 'Risk Factor'
    DEFAULT_COLUMN = 'Position Delta Per Equity Price Risk Factor'
    #DEFAULT_WRITER = 'VectorWriter'

    def __init__(self, aelParams, log):
        super(RiskFactorParameters, self).__init__(aelParams,
                RiskFactorParameters.TABNAME, RiskFactorParameters.DEFAULT_COLUMN, log)
        #self.exportName = 'export name for column'
        self.columnName = self.ael_params.get('column_name_{0}'.format(
            RiskFactorParameters.TABNAME), RiskFactorParameters.DEFAULT_COLUMN)
        self.exportName = self.columnName
        
    def _baseFileName(self):
        return self.ael_params.get("Risk Factor File Name", '')

    def valid(self):
        if not super(RiskFactorParameters, self).do_create_report():
            return False
        if not self._baseFileName():
            self._logInfo("No output file specified.")
            return False
        return True


class RiskFactorExporter(FMarketRiskExporterBase):
    def __init__(self, aelParams, log):
        self.log = log
        self.params = RiskFactorParameters(aelParams, log)
        self.writers=[]
        if ExportToMemoryCube == self.params.export_fileformat():
            self.writers.append(RiskFactorDeltaWriter('Equity Price RiskFactor', log, self.params.separators()))
        elif ExportToArtiQCube == self.params.export_fileformat():
            self.writers.append(ArtiQRiskFactorDeltaWriter('Equity Price RiskFactor', log, self.params.separators()))
        #self.columnParams = self.writer.getColumnParameters()

    def validateParameters(self):
        if not self.params.valid() or not self.writers:
            return False
        return True

    def export(self):
        attributes = configureAttributes(self.params)
        columns = [CalcMain.createColumnConfiguration(
                        columnID=self.params.columnName,
                        extensionContext=acm.GetDefaultContext(),
                        customName=self.params.exportName)]

        _calculate_distributed_mode(self.params.portfolios(),
                self.params.tradeFilters(), self.params.storedQueries(),
                columns, attributes, self.writers,
                self.params.distributedCalculations())

        filepath = self.params.getOutputFileName()
        for w in self.writers:
            w.write(self.params.overwrite(), filepath)

class PLExplainParameters(CommonParameters):
    TABNAME = 'PL Explain'
    DEFAULT_COLUMN = None
    #DEFAULT_WRITER = 'VectorWriter'

    def __init__(self, aelParams, log):
        super(PLExplainParameters, self).__init__(aelParams,
                PLExplainParameters.TABNAME, PLExplainParameters.DEFAULT_COLUMN, log)
        
        self.exportName = 'export name for column'
        self.riskfactors =  self.ael_params.get('riskFactors', [])
        self.inputYCs = self.ael_params.get('yieldCurve_PLExplain', [])
        self.storedBuckets = self.ael_params.get('timebucket_name_PLExplain', None)
        self.stressName = 'PL Explain'

    def valid(self):
        return True

    def _baseFileName(self):
        return self.ael_params.get("plExplainOutputFile", '')

    
class PLExplainExporter(FMarketRiskExporterBase):
    
    riskfactorColumnsMap = {"InterestRate": ["Interest Rate Yield Delta Bucket Vertical", "Interest Rate Yield Gamma Bucket Vertical"],
                            "Inflation": ["Inflation Benchmark Delta"],
                            "InstrumentSpread": ["Instrument Spread Delta", "Instrument Spread Gamma"],
                            "Benchmark": ["Benchmark Delta", "Benchmark Gamma"],
                            "CommodityPrice": ["Portfolio Delta Implicit Commodity", "Portfolio Gamma Implicit Commodity"],
                            "Credit": ["Credit Par Delta", "Credit Gamma"],
                            "FXRate": ['Portfolio Profit And Loss Explain FX Per Risk Factor'],
                            "EquityPrice": ["Portfolio Profit And Loss Explain Equity Per Risk Factor"],
                            "Volatility": ["Portfolio Profit And Loss Explain Volatility Per Risk Factor"], 
                            }

    def __init__(self, aelParams, log):
        self.log = log
        self.params = PLExplainParameters(aelParams, log)
        timeBucketName = self.params.storedBuckets
        self.timeBuckets = None
        if timeBucketName:
            stored = acm.FStoredTimeBuckets.Select('name="{0}"'.format(timeBucketName))
            self.timeBuckets = stored[0].TimeBuckets() if len(stored) > 0 else None
        self.writers=[]
        self.writers.append(ArtiQPLExplainWriter(self.params.riskfactors, self.timeBuckets, self.log, self.params.separators()))
        
    def validateParameters(self):
        if not self.params.valid() or not self.writers:
            return False
        return True
    
    def iterateCalcSpaceTree(self, calcSpace, node, columnName):
        if not node.Iterator().HasChildren():
            results = []
            vals = calcSpace.CreateCalculation(node, columnName).Value()
            if type(vals) is str and vals !='':
                results.append(vals)
            else:
                results.extend([v.Name() for v in vals] if vals else [])
            return results
        it = node.Iterator().FirstChild()
        results = []
        while it:
            tree = it.Tree()
            rowName = tree.StringKey()
            vals = calcSpace.CreateCalculation(tree, columnName).Value()
            currentList = []
            if type(vals) is str and vals != '':
                currentList.append(vals)
            elif vals and type(vals) is list:
                currentList.extend([v.Name() for v in vals] if vals else [])
            newYcs = set(currentList) - set(results)
            if newYcs:
                results.extend(list(newYcs))    
            yieldCurves = self.iterateCalcSpaceTree(calcSpace, tree, columnName)
            newYcs = set(yieldCurves) - set(results)
            if newYcs:
                results.extend(list(newYcs))    
            it = it.NextSibling()
        return results

    def getPosReferredYieldCurves(self, posObj, columnName):
        if not posObj:
            return None

        yieldCurves = []
        calcSpace = acm.FCalculationSpace('FPortfolioSheet')
        selectedNode = calcSpace.InsertItem(posObj)
        if self.params.grouper:
            grouper = self.params.grouper.AsPortfolioSheetGrouper()
        else:
            grouper = createArtiQAttributesObject().AsPortfolioSheetGrouper()
        selectedNode.ApplyGrouper(grouper)
        calcSpace.Refresh()
        
        yieldCurves = self.iterateCalcSpaceTree(calcSpace, selectedNode, columnName)
        self.log.logInfo("getPosReferredYieldCurves {0}".format(yieldCurves))
        return yieldCurves
    
    def getYieldCurves(self, columnName, extendList=[]):
        yieldCurves = []
        for pName in self.params.portfolios():
            p = acm.FPhysicalPortfolio[pName]
            curves = self.getPosReferredYieldCurves(p, columnName)
            yieldCurves.extend(curves)
        for fName in self.params.tradeFilters():
            f = acm.FTradeSelection[fName]
            curves = self.getPosReferredYieldCurves(f, columnName)
            yieldCurves.extend(curves)
        for qName in self.params.storedQueries():
            q = acm.FStoredASQLQuery[qName]
            curves = self.getPosReferredYieldCurves(q, columnName)
            yieldCurves.extend(curves)

        yieldCurves.extend(list(extendList))
        return list(set(yieldCurves))
 
   
    def createInterestRateColumns(self, columnConfigurations, curves):
        columnIDs = PLExplainExporter.riskfactorColumnsMap["InterestRate"]
        for col in columnIDs:
            type = "Delta" if "Delta" in col else "Gamma"
            for ycName in curves:
                params = {acm.FSymbol("InterestRateDeltaGammaCurveFilter"): ycName}
                colName = "InterestRate {0}@{1}".format(type, ycName)
                tb = self.timeBuckets if self.timeBuckets else \
                    FMarketRiskExportUtil.CreateYcTimeBucket(ycName, self.log)
                columnConfigurations.append(
                    CalcMain.createColumnConfiguration(
                        columnID=col,
                        extensionContext=acm.GetDefaultContext(),
                        customName=colName,
                        parameters=params,
                        timebuckets=tb))
        return columnConfigurations

    def createVolatilityColumns(self, columnConfigurations):
        columnId = PLExplainExporter.riskfactorColumnsMap["Volatility"]
        params = {
            acm.FSymbol("ProfitAndLossExplainIncludeGamma") : True,
            acm.FSymbol("PortfolioProfitAndLossExplainVolatilityTimeBucketsFromStructure") : True
        }
        config = CalcMain.createColumnConfiguration(
                columnID=columnId,
                extensionContext=acm.GetDefaultContext(),
                parameters=params,
                customName= "Volatility")
        columnConfigurations.append(config)
    
        return columnConfigurations

    def createRfColumns(self, columnConfigurations, curves, rfType):
        if rfType == "Inflation":
            col = "Inflation Curve"
            columnConfigurations.append(
                    CalcMain.createColumnConfiguration(
                        columnID=col,
                        extensionContext=acm.GetDefaultContext(),
                        customName=col))

        for ycName in curves:
            tb = self.timeBuckets if self.timeBuckets else \
                    FMarketRiskExportUtil.CreateYcTimeBucket(ycName, self.log)
            if tb:
                self.log.logInfo("Timebucket explict dates. {0}".format(
                    sorted([t.EndDate() for t in tb])))
            params = {BENCHMARK_CURVE_FILTER: ycName}
            columnIDs = PLExplainExporter.riskfactorColumnsMap[rfType]
            for col in columnIDs:
                colName = col + '@' + ycName
                columnConfigurations.append(
                    CalcMain.createColumnConfiguration(
                        columnID=col,
                        extensionContext=acm.GetDefaultContext(),
                        customName=colName,
                        timebuckets=tb,
                        parameters=params))
        return columnConfigurations

    def createInstSpreadColumns(self, columnConfigurations, curves, rfType):
        col = "All Yield Curves Name"
        columnConfigurations.append(
                CalcMain.createColumnConfiguration(
                    columnID=col,
                    extensionContext=acm.GetDefaultContext(),
                    customName=col))
        columnIDs = PLExplainExporter.riskfactorColumnsMap[rfType]
        for col in columnIDs:
            type = "Delta" if "Delta" in col else "Gamma"
            for ycName in curves:
                columnConfigurations.append(
                    CalcMain.createColumnConfiguration(
                        columnID=col,
                        extensionContext=acm.GetDefaultContext()))
        return columnConfigurations
        
    def createColumns(self):
        columnConfigurations = []
        needYc = len(set(list(self.params.riskfactors)).intersection(set(["Benchmark", "InterestRate", "InstrumentSpread"]))) != 0
        yieldCurves = self.getYieldCurves("All Yield Curves Name", list(self.params.inputYCs)) if needYc else []
        inflationCurves = self.getYieldCurves("Inflation Curve", list(self.params.inputYCs)) \
                if 'Inflation' in self.params.riskfactors else []
        creditCurvesL = self.getYieldCurves("Credit Curve", list(self.params.inputYCs)) \
                if 'Credit' in self.params.riskfactors else []
        instrumentSpreadCurves = [y for y in yieldCurves if acm.FInstrumentSpreadCurve[y] != None]
        creditCurves=[]
        if creditCurvesL:
            creditCurves = list(set([n.split(',')[0] for n in creditCurvesL]))
        rfCurveMap = {"Benchmark":yieldCurves, "Inflation": inflationCurves, "Credit":creditCurves}
        for rf in self.params.riskfactors:
            if rf in ["Benchmark", "Inflation", "Credit"]:
                curves = rfCurveMap[rf] 
                columnConfigurations = self.createRfColumns(columnConfigurations, curves, rf)
            elif rf == "InstrumentSpread" and len(instrumentSpreadCurves) !=0 :
                columnConfigurations = self.createInstSpreadColumns(columnConfigurations, instrumentSpreadCurves, rf)
            elif rf == "InterestRate":
                columnConfigurations = self.createInterestRateColumns(columnConfigurations, yieldCurves)
            elif rf == "Volatility":
                columnConfigurations = self.createVolatilityColumns(columnConfigurations)
            else:
                columnIDs = PLExplainExporter.riskfactorColumnsMap[rf]
                params = {acm.FSymbol("ProfitAndLossExplainIncludeGamma") : True}
                for col in columnIDs:
                    if rf in ['EquityPrice', 'FXRate']:
                        columnConfigurations.append(
                            CalcMain.createColumnConfiguration(
                                columnID=col,
                                extensionContext=acm.GetDefaultContext(),
                                customName=rf,
                                parameters=params))
                    else:
                        columnConfigurations.append(
                            CalcMain.createColumnConfiguration(
                                columnID=col,
                                extensionContext=acm.GetDefaultContext(),
                                customName=col))
        return columnConfigurations

    def export(self):
        attributes = configureAttributes(self.params)
        columns = self.createColumns()
        _calculate_distributed_mode(self.params.portfolios(),
                self.params.tradeFilters(),
                self.params.storedQueries(),
                columns,
                attributes,
                self.writers,
                self.params.distributedCalculations())
        filepath = self.params.getOutputFileName()
        for w in self.writers:
            w.write(self.params.overwrite(), filepath)

class MarketDataParameters(CommonParameters):
    TABNAME = 'Market Data'
    DEFAULT_COLUMN = None
    
    def __init__(self, aelParams, log):
        super(MarketDataParameters, self).__init__(aelParams,
                MarketDataParameters.TABNAME, MarketDataParameters.DEFAULT_COLUMN, log)
        self.insts = self.ael_params.get('Instruments_MarketData', None)
        self.yieldCurves = self.ael_params.get('yieldCurve_MarketData', None)
        self.volatilities = self.ael_params.get('volatility_MarketData', None)
        self.storedBuckets = self.ael_params.get('timebucket_name_MarketData', None)
        self.exportBenchmarkPrice = self.ael_params.get('ExportBenchmarkPrice', 1)
        
    def valid(self):
       return True

    def _baseFileName(self):
        return self.ael_params.get("rateFileOutputName", '')

class MarketDataExporter(object):

    def __init__(self, aelParams, log):
        self.log = log
        self.params = MarketDataParameters(aelParams, log)
        insts = set(self.params.insts)
        yieldCurves = set(self.params.yieldCurves)
        volatilities = set(self.params.volatilities)
        exportBenchmarkPrice = self.params.exportBenchmarkPrice
        timeBucketName = self.params.storedBuckets
        self.timeBuckets = None
        if timeBucketName:
            stored = acm.FStoredTimeBuckets.Select('name="{0}"'.format(timeBucketName))
            self.timeBuckets = stored[0].TimeBuckets() if len(stored) > 0 else None
        self.writer = MarketDataWriter.MarketDataWriter(self.log, insts, yieldCurves, volatilities, exportBenchmarkPrice, self.timeBuckets)
   
    def validateParameters(self):
        if not self.params.valid() or not self.writer:
            return False
        return True

    def export(self):
        filepath = self.params.getOutputFileName()
        self.writer.write(self.params.overwrite(), filepath)

class BookTradeTagsParameters(CommonParameters):
    TABNAME = 'Book Trade Tag'
    DEFAULT_COLUMN = None
    
    def __init__(self, aelParams, log):
        super(BookTradeTagsParameters, self).__init__(aelParams,
                BookTradeTagsParameters.TABNAME, BookTradeTagsParameters.DEFAULT_COLUMN, log)
        self.BookTagFileName = self.ael_params.get('BookTagsFile', 'Book Tags.csv')
        self.TradeTagFileName = self.ael_params.get('TradeTagsFile', 'Trade Tags.aap')
        self.PositionSpec = self.ael_params.get('positionSpecForBookTags', None)
        
    def valid(self):
       return True

    def outputFileName(self, rawName):        
        name, extension = rawName.rsplit('.', 1)
        fileName = self.getOutputFileName(True, name)
        fileName = '{}.{}'.format(fileName, extension)
        return fileName

class BookTradeTagsExporter(object):

    def __init__(self, aelParams, log):
        self.log = log
        self.params = BookTradeTagsParameters(aelParams, log)
        self.bookNodePositionSpec = self.params.PositionSpec

    def _getPostionTrades(self):
        trades = []
        portfs = self.params.portfolios()
        for pName in portfs:
            portf = acm.FPhysicalPortfolio[pName]
            if portf:
                trades = portf.Trades()
        tradeFilters = self.params.tradeFilters()
        for fName in tradeFilters:
            filter = acm.FTradeSelection[fName]
            if filter:
                trades.extend(filter.Trades())
        storedQueries = self.params.storedQueries()
        for qName in storedQueries:
            query = acm.FStoredASQLQuery[qName]
            if query:
                trades.extend(query.Query().Select())
        return trades

    def _getAttrValues(self, attrDefs,  trade):
        values = []
        for attrDef in attrDefs:
            methodChain = attrDef.Definition().split('.')
            value = trade
            for methodName in methodChain:
                method = getattr(value, methodName, None)
                if method is None:
                    value = None
                    break
                else:                
                    value = method()
            values.append(str(value))
        return tuple(values)

    def validateParameters(self):
        if not self.params.valid():
            return False
        return True

    def calculate(self):
        attrDefs = self.bookNodePositionSpec.AttributeDefinitions()
        trades = self._getPostionTrades()
        bookNodes = sorted(set(self._getAttrValues(attrDefs, t) for t in trades))
        tradeNodeList= []
        for t in trades:
            idx = bookNodes.index(self._getAttrValues(attrDefs, t))
            tradeNodeList.append((idx, t))
        return tradeNodeList, bookNodes, attrDefs

    def export(self):
        tradeNodeL, bookNodes, attrDefs = self.calculate()
        bookTagFileName = self.params.outputFileName(self.params.BookTagFileName)
        bookTagWriter = BookTagWriter(attrDefs, bookNodes, self.log)
        bookTagWriter.write(self.params.overwrite(), bookTagFileName)

        tradeTagFileName = self.params.outputFileName(self.params.TradeTagFileName)
        tradeTagWriter = TradeTagWriter(tradeNodeL, self.log)
        tradeTagWriter.write(self.params.overwrite(), tradeTagFileName)

def do_run_bulk_exports(ael_params, world):
    result = False
    if 'runPnLReports' in ael_params and (ael_params['runPnLReports'] == '1' or ael_params['runPnLReports'] == 1 or falseTrue[ael_params['runPnLReports']] == 'True'):
        result = True
    else:
        world.logInfo("Skipping PnL Reports.")

    if 'runMarketValueReports' in ael_params and (ael_params['runMarketValueReports'] == '1' or ael_params['runMarketValueReports'] == 1 or falseTrue[ael_params['runMarketValueReports']] == 'True'):
        result = True
    else:
        world.logInfo("Skipping Market Value Reports.")

    if 'runThetaReports' in ael_params and (ael_params['runThetaReports'] == '1' or ael_params['runThetaReports'] == 1 or falseTrue[ael_params['runThetaReports']] == 'True'):
        result = True
    else:
        world.logInfo("Skipping Theta Reports.")

    return result
                                                                              

def run_createBulkExporters(ael_params, world):
    columnConfigurations = []
    writers = []
    marketvalue_params = MarketValueParameters(ael_params, 'Market Value', THEO_VAL, world)
    pnl_params = PLParameters(ael_params, 'Profit and Loss', '', world)
    theta_params = ThetaParameters(ael_params, 'Theta', THETA_PL, world)

    if 'runMarketValueReports' in ael_params and (ael_params['runMarketValueReports'] == '1' or ael_params['runMarketValueReports'] == 1 or falseTrue[ael_params['runMarketValueReports']] == 'True'):

        if marketvalue_params.do_create_report():
            world.logInfo("Exporting Market Value Report.")
            mv_exporter = FMarketRiskMVExporter(ael_params, world)
            mv_exporter.configureExport()
            columnConfigurations.extend(mv_exporter.columnConfigurations)
            writers.extend(mv_exporter.writers)
        else:
            world.logError("Invalid parameters - skipping Market Value Report. No exported file generated.")

    if 'runPnLReports' in ael_params and (ael_params['runPnLReports'] == '1' or ael_params['runPnLReports'] == 1 or falseTrue[ael_params['runPnLReports']] == 'True'):
        if pnl_params.do_create_report():
            world.logInfo("Exporting Profit and Loss Report.")
            pnl_exporter = FMarketRiskPnLExporter(ael_params, world)
            pnl_exporter.configureExport()
            columnConfigurations.extend(pnl_exporter.columnConfigurations)
            writers.extend(pnl_exporter.writers)

        else:
            world.logError("Invalid parameters - skipping Profit and Loss Report. No exported file generated.")

    if 'runThetaReports' in ael_params and (ael_params['runThetaReports'] == '1' or ael_params['runThetaReports'] == 1 or falseTrue[ael_params['runThetaReports']] == 'True'):
        if theta_params.do_create_report():
            world.logInfo("Exporting Theta Report.")
            theta_exporter = FMarketRiskThetaExporter(ael_params, world)
            theta_exporter.configureExport()
            columnConfigurations.extend(theta_exporter.columnConfigurations)
            writers.extend(theta_exporter.writers)

        else:
            world.logError("Invalid parameters - skipping Theta Report. No exported file generated.")

    attributes = configureAttributes(marketvalue_params)
    _calculate_distributed_mode(marketvalue_params.portfolios(),
            marketvalue_params.tradeFilters(), marketvalue_params.storedQueries(),
                                     columnConfigurations,
                                     attributes,
                                     writers,
                                     marketvalue_params.distributedCalculations())
    for w in writers:
        filepath = None
        risktype = ''
        if type(w) == FRiskCubeWriterBase.ProfitAndLossWriter or type(w) == FRiskCubeWriterBase.ArtiQProfitAndLossWriter:
            filepath = pnl_params.getOutputFileName()
            risktype = 'Profit and Loss'
        elif type(w) == FRiskCubeWriterBase.MarketValueWriter or type(w) == FRiskCubeWriterBase.ArtiQMarketValueWriter:
            filepath = marketvalue_params.getOutputFileName()
            risktype = 'Market Value'
        elif type(w) == FRiskCubeWriterBase.ThetaWriter or type(w) == FRiskCubeWriterBase.ArtiQThetaWriter:
            filepath = theta_params.getOutputFileName()
            risktype = 'Theta'

        if filepath:
            w.write(marketvalue_params.overwrite(), filepath)
            world.logInfo("Wrote %s output to %s." % (risktype, filepath))
