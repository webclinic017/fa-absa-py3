""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FGraphPlotter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FGraphPlotter

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import math
from FIntegratedWorkbenchLogging import logger

class Plot(object):

    _plotters = []

    def __init__(self, cls):
        self._cls = cls
        if self._cls not in self.__class__._plotters:
            self.__class__._plotters.append(self._cls)

    @classmethod
    def Plotters(cls):
        return cls._plotters

    def __call__(self):
        return self._cls()


class GraphPlotter(object):

    AXIS_TITLES = None
    SPACE_COLLECTION = acm.FCalculationSpaceCollection()
    SPACE = None
    START = None
    END = None
    STEP = None
    NAME = ''
    SHEET_CLASS = 'FPortfolioSheet'
    CONTEXT = acm.GetDefaultContext()
    CONFIG = None
    DISTRIBUTED = False
    COLOR = None
    SHOW_POINTS = False
    POINT_STYLE = None
    POINT_SIZE = None
    XCOLUMNID = None
    YCOLUMNID = None

    def __init__(self):
        self._instrument = None
        self._xvalues = []
        self._yvalues = []

    @staticmethod
    def drange(start, stop, step):
        r = start
        while r < stop:
            yield r
            r += step

    def Space(self):
        cls = self.__class__
        if cls.SPACE is None:
            cls.SPACE = cls.SPACE_COLLECTION.GetSpace(
                cls.SHEET_CLASS,
                cls.CONTEXT,
                cls.CONFIG,
                cls.DISTRIBUTED)
        return cls.SPACE

    @staticmethod
    def IsValid(number):
        try:
            number = float(number)
            return (number and
                not math.isinf(number) and
                not math.isnan(number))
        except StandardError:
            return False

    @staticmethod
    def IsArray(obj):
        return hasattr(obj, 'Size')

    @classmethod
    def ShiftFactors(cls):
        for s in cls.drange(
            cls.START,
            cls.END,
            cls.STEP):
            yield s

    @classmethod
    def AxisTitles(cls):
        return cls.AXIS_TITLES

    @classmethod
    def Color(cls):
        return cls.COLOR
        
    @classmethod
    def ShowPoints(cls):
        return cls.SHOW_POINTS

    @classmethod
    def PointStyle(cls):
        return cls.POINT_STYLE
        
    @classmethod
    def PointSize(cls):
        return cls.POINT_SIZE

    def Name(self):
        return self.__class__.NAME

    def FromValue(self, value_):
        self._xvalues =[value_*s for s in self.ShiftFactors()]
        return self._xvalues

    def FromArray(self, value_):
        self._xvalues = self.EditArray(value_)
        return self._xvalues

    def EditArray(self, value_):
        return value_

    def FromFactors(self):
        self._xvalues = [s for s in self.ShiftFactors()]
        return self._xvalues

    def FromInvalidValue(self):
        # pylint: disable-msg=W0612
        self.Logger().warn(
            'Instrument {0} does\'t have a valid {1}'.format(
                self._instrument.Name(),
                self.__class__.XCOLUMNID))
        self._xvalues = [0 for s in self.ShiftFactors()]
        return self._xvalues

    def XValues(self):
        if not self._xvalues:
            if self.__class__.XCOLUMNID is None:
                return self.FromFactors()
            value_ = self.CalculatedValue(self.__class__.XCOLUMNID)
            if self.IsArray(value_):
                return self.FromArray(value_)
            elif not self.IsValid(value_):
                return self.FromInvalidValue()
            return self.FromValue(value_)
        return self._xvalues

    def YValues(self):
        # Remove this pylint msg when SPR 392045 has been fixed
        # pylint: disable-msg=E1101, W0612      
        if not self._yvalues:
            cls = self.__class__
            calc = self.CreateCalculation(cls.YCOLUMNID,
                self.CalculationConfig())
            value_ = calc.Value()
            self._yvalues = (value_ if self.IsArray(value_) else
                [value_ for i in self.ShiftFactors()])
        return self._yvalues

    def RowObject(self):
        topNode = self.Space().InsertItem(self._instrument)
        self.Space().Refresh()
        return topNode.Iterator().FirstChild().Tree()

    def CreateCalculation(self, columnId, config=None):
        # pylint: disable-msg=E0012,E1101
        # SPR 392045: Make sure that this routine returns the same data type
        # Remove required pylint tags
        if self.__class__.CONTEXT.GetExtension(acm.FColumnDefinition, acm.FTradingSheet, columnId):
            calc = self.Space().CreateCalculation(
                    self.RowObject(),
                    columnId,
                    config)
            self.Space().Refresh()
            return calc
        else:
            self.Logger().warn(
                'Could not find column %s', columnId)
            return [(0,0)]

    def CalculatedValue(self, columnId):
        # pylint: disable-msg=E1101      
        calc = self.CreateCalculation(columnId)
        return calc.Value()

    def SimulateValue(self, value):
        self.Space().SimulateValue(
            self._instrument,
            self.__class__.XCOLUMNID,
            value)

    def RemoveSimulation(self):
        self.Space().RemoveSimulation(
            self._instrument,
            self.__class__.XCOLUMNID)

    def Logger(self):
        return logger

    def Reset(self, instrument):
        self._instrument = instrument
        self._xvalues = []
        self._yvalues = []

    def Coordinates(self, instrument):
        try:
            if instrument is None:
                raise StandardError('Instrument is None')
            elif instrument is self._instrument:
                return list(zip(self._xvalues, self._yvalues))
            self.Reset(instrument)
            return list(zip(self.XValues(), self.YValues()))
        except StandardError as e:
            self.Logger().error(
                'Failed to get coordinates for instrument %s. Reason: %s',
                self._instrument.Name() if instrument else 'None',
                e)
            return [(0,0)]

    def CalculationConfig(self):
        pass

class GraphScenarioPlotter(GraphPlotter):

    SHIFT_FORMAT_NAME = None
    SHIFT_FORMAT_VALUE = None
    RISK_FACTOR_TYPE = None

    def __init__(self):
        GraphPlotter.__init__(self)

    @classmethod
    def ShiftConfig(cls, riskFactor):
        return riskFactor.ShiftConfiguration(
            cls.SHIFT_FORMAT_NAME,
            cls.SHIFT_FORMAT_VALUE)

    @classmethod
    def ShiftValues(cls):
        return [v for v in cls.ShiftFactors()]


    @staticmethod
    def Filter():
        return acm.FObject

    @classmethod
    def RiskFactor(cls):
        priceFactor = acm.RiskFactor.RiskFactorType(cls.RISK_FACTOR_TYPE)
        description = priceFactor.CreateRiskFactorDescription(None, None)
        return description.CreateRiskFactor(cls.Filter(), cls.ShiftConfig(priceFactor))

    def Scenario(self):
        buider = acm.FScenarioBuilder()
        scenario = buider.CreateScenario()
        dim = buider.CreateScenarioDimension(scenario)
        buider.CreateRiskFactorScenarioMember(dim, self.RiskFactor(), self.ShiftValues())
        return scenario

    def CalculationConfig(self):
        return acm.Sheet().Column().ConfigurationFromScenario(self.Scenario())

class SinglePointPlotter(GraphPlotter):
    SHOW_POINTS = True

    @classmethod
    def ShiftFactors(cls):
        return [1.0]