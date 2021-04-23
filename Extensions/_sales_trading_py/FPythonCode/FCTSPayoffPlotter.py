""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSPayoffPlotter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSPayoffPlotter

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import bisect
from FGraphPlotter import GraphScenarioPlotter, SinglePointPlotter

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

class CTSPayoffPlotter(GraphScenarioPlotter):

    SHIFT_FORMAT_NAME = 'DifferenceType'
    SHIFT_FORMAT_VALUE = 'Replace'
    RISK_FACTOR_TYPE = 'Equity'
    XCOLUMNID = 'MonisStockPDEMatrix'
    SPOTCOLUMNID = 'Portfolio Underlying Future Method Price'
    PDESTYLE = 'Full'
    START = 0.5
    END = 1.5

    def __init__(self):
        self.MIN_INDEX = 0
        self.MAX_INDEX = 0
        GraphScenarioPlotter.__init__(self)

    def Scenario(self):
        buider = acm.FScenarioBuilder()
        scenario = buider.CreateScenario()
        dim = buider.CreateScenarioDimension(scenario)
        buider.CreateRiskFactorScenarioMember(dim, self.RiskFactor(), self.XValues())
        return scenario

    def YValues(self):
        # Remove this pylint msg when SPR 392045 has been fixed
        # pylint: disable-msg=E1101,W0612       
        if not self._yvalues:
            cls = self.__class__
            calc = self.CreateCalculation(cls.YCOLUMNID,
                self.CalculationConfig())
            value_ = calc.Value()
            self._yvalues = (value_ if self.IsArray(value_) else
                [value_ for i in self.XValues()])
        return self._yvalues

    def BorderPoints(self, pdeMatrix):
        s = self.Cut(pdeMatrix)
        return [s[0], s[len(s)-1]]

    def Cut(self, pdeMatrix):
        cls = self.__class__
        if self.MIN_INDEX == 0 and self.MAX_INDEX == 0:
            spotPrice = self.CalculatedValue(self.__class__.SPOTCOLUMNID)
            spotPrice = float(spotPrice)
            startVal = spotPrice*cls.START
            endVal = spotPrice*cls.END
            mat_len = (len(pdeMatrix) - 1)
            self.MIN_INDEX = bisect.bisect_left(pdeMatrix, startVal, lo = 1, hi = mat_len)
            self.MAX_INDEX = bisect.bisect_left(pdeMatrix, endVal, lo = 1, hi = mat_len)
        return pdeMatrix[self.MIN_INDEX:self.MAX_INDEX]

    def Full(self, pdeMatrix):
        return pdeMatrix

    def EditArray(self, pdeMatrix):
        cls = self.__class__
        func = getattr(cls, cls.PDESTYLE)
        return func(self, pdeMatrix)

    def Reset(self, instrument):
        self.MIN_INDEX = 0
        self.MAX_INDEX = 0
        GraphScenarioPlotter.Reset(self, instrument)

@Plot
class PDETheorPlotter(CTSPayoffPlotter):

    AXIS_TITLES = ('Underlying Price', 'Value')
    NAME = 'Theor'
    PDESTYLE = 'Cut'
    YCOLUMNID = 'MonisCBPDEMatrix'
    COLOR = acm.UX().Colors().Create(255, 0, 0)

    def YValues(self):
        # Remove this pylint msg when SPR 392045 has been fixed
        # pylint: disable-msg=E1101,W0612
        if not self._yvalues:
            cls = self.__class__
            calc = self.CreateCalculation(cls.YCOLUMNID)
            
            value_ = calc.Value()
            self._yvalues = (self.EditArray(value_) if self.IsArray(value_) else
                [value_ for i in self.XValues()])
        return self._yvalues

    def __init__(self):
        CTSPayoffPlotter.__init__(self)


@Plot
class FloorPlotter(CTSPayoffPlotter):

    PDESTYLE = 'BorderPoints'
    NAME = 'Floor'
    PDESTYLE = 'BorderPoints'
    YCOLUMNID = 'CB Bond Floor'
    COLOR = acm.UX().Colors().Create(0, 255, 0)

    def __init__(self):
        CTSPayoffPlotter.__init__(self)


@Plot
class MonisParityPlotter(CTSPayoffPlotter):

    PDESTYLE = 'BorderPoints'
    NAME = 'Parity'
    PDESTYLE = 'BorderPoints'
    YCOLUMNID = 'CB Parity'
    COLOR = acm.UX().Colors().Create(0, 0, 255)

    def __init__(self):
        CTSPayoffPlotter.__init__(self)
        
@Plot
class DeltaNukePricePlotter(CTSPayoffPlotter):

    PDESTYLE = 'BorderPoints'
    
    NAME = 'Delta Nuke (Bid)'
    PDESTYLE = 'BorderPoints'
    YCOLUMNID = 'Delta Nuke Price'
    COLOR = acm.UX().Colors().Create(0, 0, 0)

    def __init__(self):
        CTSPayoffPlotter.__init__(self)

@Plot
class MarketPricePlotter(SinglePointPlotter):

    NAME = 'Market Price'
    YCOLUMNID = 'Instrument Market Price'
    XCOLUMNID = 'Portfolio Underlying Future Method Price'
    POINT_SIZE = 10
    POINT_STYLE = 'Cross'
    COLOR = acm.UX().Colors().Create(0, 0, 0)

    def __init__(self):
        SinglePointPlotter.__init__(self)
        
@Plot
class BaseBidPricePlotter(SinglePointPlotter):

    NAME = 'Base Bid'
    YCOLUMNID = 'Delta Nuke Base Bid Price'
    XCOLUMNID = 'Delta Nuke Base Underlying Price'
    POINT_SIZE = 5
    POINT_STYLE = 'Circle'
    COLOR = acm.UX().Colors().Create(0, 0, 0)

    def __init__(self):
        SinglePointPlotter.__init__(self)