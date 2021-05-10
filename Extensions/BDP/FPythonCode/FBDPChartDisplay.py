""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPChartDisplay.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import itertools
import collections


import acm
import FUxCore
import FBDPChartData


_FCOLOR_RED = acm.UX().Colors().Create(255, 0, 0)
_FCOLOR_GREEN = acm.UX().Colors().Create(0, 255, 0)
_FCOLOR_BLUE = acm.UX().Colors().Create(0, 0, 255)
_FCOLOR_BLACK = acm.UX().Colors().Create(0, 0, 0)


class _Display(object):

    def setup(self):

        raise NotImplementedError('To be implemented in the derived class.')

    def display(self, uiData):

        raise NotImplementedError('To be implemented in the derived class.')


_SeriesPoint = collections.namedtuple('_SeriesPoint', ['xLabel', 'yValue'])


class Display2DChart(_Display):

    def __init__(self, ux2DChartControl):

        assert ux2DChartControl.IsKindOf('FUx2DChartControl')
        self._control = ux2DChartControl

    def _cbXValues(self, args, _cd):
        # args is in the form (object->[...], objectIndex->N, seriesIndex->0)
        xval = float(args.At('objectIndex'))
        return xval

    def _cbXAxisLabels(self, args, _cd):
        # args is in the form (object->[...], objectIndex->N, seriesIndex->0)
        xLabel, _yValue = args.At('object')
        return str(xLabel)

    def _cbYValues(self, args, _cd):
        # args is in the form (object->[...], objectIndex->N, seriesIndex->0)
        _xLabel, yValue = args.At('object')
        if yValue is None:
            return 0
        return int(yValue)

    def _cbTooltipsText(self, args, _cd):
        # args is in the form (object->[...], objectIndex->N, seriesIndex->0)
        xLabel, yValue = args.At('object')
        return '{0}\n{1}'.format(xLabel, yValue)

    def setup(self):

        self._control.XValuesEventHandler().Add(self._cbXValues, None)
        self._control.YValuesEventHandler().Add(self._cbYValues, None)
        self._control.TooltipsTextEventHandler().Add(self._cbTooltipsText,
                None)
        self._control.XAxisLabelsEventHandler().Add(self._cbXAxisLabels, None)

    def _lineSplitLegendTitle(self, viewLabel, subTitle):

        vlList = viewLabel.split(':')
        stList = subTitle.split('  ')
        return '\n'.join(vlList + stList)

    def _prepareLegendTitle(self, viewLabel, subTitle):

        legendTitle = self._lineSplitLegendTitle(viewLabel, subTitle)
        return legendTitle

    @staticmethod
    def _prepareDataSeriesValues(seriesPointList):

        zeroSeriesPoint = _SeriesPoint(xLabel='', yValue=0)
        seriesValues = acm.FArray()
        # Prepend zero data (i.e. pad on the left on the chart)
        #seriesValues.Add(zeroSeriesPoint)
        # Fill in the middle (i.e. the actual data point on the chart)
        for seriesPoint in seriesPointList:
            seriesValues.Add(seriesPoint)
        # Postpend zero data (i.e. pad on the right on the chart)
        #seriesValues.Add(zeroSeriesPoint)
        return seriesValues

    @staticmethod
    def _prepareBarDataSeriesValues(seriesPointList):

        zeroSeriesPoint = _SeriesPoint(xLabel='', yValue=0)
        seriesValues = acm.FArray()
        # Prepend zero data (i.e. pad on the left on the chart)
        seriesValues.Add(zeroSeriesPoint)
        # Fill in the middle (i.e. the actual data point on the chart)
        for seriesPoint in seriesPointList:
            seriesValues.Add(seriesPoint)
        # Postpend zero data (i.e. pad on the right on the chart)
        seriesValues.Add(zeroSeriesPoint)
        return seriesValues
        
    def _populatePlotChartSeries(self, seriesList):

        for sData in seriesList:
            seriesPointList = [_SeriesPoint(xLabel=x,
                yValue=y) for x, y in zip(sData.xList, sData.yList)]
            seriesValues = self._prepareDataSeriesValues(seriesPointList)
            series = self._control.AddSeries(FBDPChartData.CHART_TYPE_PLOT,
                seriesValues.Size(), sData.color, sData.name)
            series.SetBorderWidth(2)
            series.Populate(seriesValues)
        self._control.BaseXAxisLabelsOnSeries(series)
        
    def _populateBarChartSeries(self, seriesList):

        for sData in seriesList:
            seriesPointList = [_SeriesPoint(xLabel=x,
                yValue=y) for x, y in zip(sData.xList, sData.yList)]
            seriesValues = self._prepareDataSeriesValues(seriesPointList)
            series = self._control.AddSeries(
                FBDPChartData.CHART_TYPE_BAR,
                seriesValues.Size(), sData.color, sData.name)
            series.Populate(seriesValues)
            # x label, take either one will work
        self._control.BaseXAxisLabelsOnSeries(series)

    def _populateStepLineChartSeries(self, seriesList):

        for sData in seriesList:
            seriesPointList = [_SeriesPoint(xLabel=x,
                yValue=y) for x, y in zip(sData.xList, sData.yList)]
            seriesValues = self._prepareDataSeriesValues(seriesPointList)
            series = self._control.AddSeries(FBDPChartData.CHART_TYPE_STEPLINE,
                seriesValues.Size(), sData.color, sData.name)
            series.SetBorderWidth(2)
            series.Populate(seriesValues)
        self._control.BaseXAxisLabelsOnSeries(series)

    def _populateChartSeries(self, uiData):
        chartType = uiData.chartType
        if chartType == FBDPChartData.CHART_TYPE_PLOT: 
            self._populatePlotChartSeries(uiData.seriesList)
        elif chartType == FBDPChartData.CHART_TYPE_BAR:
            self._populateBarChartSeries(uiData.seriesList)
        elif chartType == FBDPChartData.CHART_TYPE_STEPLINE:
            self._populateStepLineChartSeries(uiData.seriesList)
        else:
            raise NotImplementedError('chart type %s not supported yet' %(chartType))

    def display(self, uiData):

        if uiData.chartType not in FBDPChartData.VALID_2D_CHART_TYPES:
            self._control.Visible(False)
            return
        self._control.Visible(True)
        # Turn off things
        self._control.ClearChart()
        self._control.ShowLegend(False)
        self._control.ShowTooltips(False)
        # Prepare things
        legendTitle = self._prepareLegendTitle(uiData.viewLabel,
                uiData.subTitle)
        self._control.SetAxisTitles(uiData.XAxisLabel, uiData.YAxisLabel)
        self._populateChartSeries(uiData)
        # Turn on things
        self._control.ShowLegend(True, legendTitle)
        self._control.ShowTooltips(True)
        self._control.Redraw()
