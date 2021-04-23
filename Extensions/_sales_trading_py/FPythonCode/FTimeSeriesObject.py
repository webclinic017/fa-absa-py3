""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FTimeSeriesObject.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FTimeSeriesObject

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
from FIntegratedWorkbenchUtils import IsKindOf
from FIntegratedWorkbenchLogging import logger

class TimeSeriesObject():

    def __init__(self, spec, obj, timeSeriesValues):
        self._timeSeriesSpec = None
        self._object  = obj
        self._dateInd = None
        self._yValues = None
        self._dates   = None
        self._colorName = 'Blue_10'
        self._pointSize = 2
        self._lineWidth = 1
        self._pointStyle = 'Circle'
        self._startDateIndex = None
        self._endDateIndex = None
        self.TimeSeriesSpec(spec)
        self._SetTimeSeriesValues(timeSeriesValues)
        self.SetStartEndIndices(start=None, end=None)

    def SetStartEndIndices(self, start=None, end=None):
        self._SetStartIndex(start)
        self._SetEndIndex(end)

    def _SetStartIndex(self, start):
        if start is not None:
            if self._endDateIndex:
                assert start < self._endDateIndex
            self._startDateIndex = start

    def _SetEndIndex(self, end):
        if end is not None:
            assert end > self._startDateIndex
            self._endDateIndex = end+1

    def TimeSeriesSpec(self, spec):
        if isinstance(spec, str):
            self._timeSeriesSpec = acm.FTimeSeriesSpec[spec]
        elif IsKindOf(spec, acm.FTimeSeriesSpec):
            self._timeSeriesSpec = spec
        else:
            logger.info('Could not find spec')

    def _SetTimeSeriesValues(self, timeSeriesValues):
        #Gets the values for the time spec and object and populates dateInd,yValues and dates
        self._dateInd, self._yValues, self._dates = list(zip(*timeSeriesValues))

    def FullDates(self):
        return self._dates

    def Length(self):
        return len(self.DateInd())

    def DateInd(self, index=None, filtered=True):
        return self._GetData(index, filtered, '_dateInd')

    def Dates(self, index=None, filtered=True):
        return self._GetData(index, filtered, '_dates')

    def YValues(self, index=None, filtered=True):
        return self._GetData(index, filtered, '_yValues')

    def _GetData(self, index, filtered, attr):
        attrValue = getattr(self, attr)
        if index:
            try:
                return attrValue[index]
            except IndexError as exc:
                logger.error(exc, exc_info=True)
        if filtered:
            return attrValue[self._startDateIndex:self._endDateIndex]
        return attrValue

    def _ColorFromColorName(self, colorName):
        color = acm.GetDefaultContext().GetExtension('FColor', acm.FColor, colorName)
        if color:
            return color.Value()

    def Color(self):
        return self._ColorFromColorName(self._colorName)
        
    def PointStyle(self):
        return self._pointStyle
        
    def LineWidth(self):
        return self._lineWidth
        
    def PointSize(self):
        return self._pointSize