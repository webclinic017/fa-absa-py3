""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/bdp_dashboard/FBDPDashboardDisplay.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import itertools
import collections


import acm


import FUxCore


import FBDPDashboardData
import FBDPDashboardDefaultConfig
import FBDPDashboardUtil


_FCOLOR_RED = acm.UX().Colors().Create(255, 0, 0)
_FCOLOR_GREEN = acm.UX().Colors().Create(0, 255, 0)
_FCOLOR_BLUE = acm.UX().Colors().Create(0, 0, 255)
_FCOLOR_BLACK = acm.UX().Colors().Create(0, 0, 0)


_SERIES_NAME_UNDER_LIMIT = 'Under limit'
_SERIES_NAME_OVER_LIMIT = 'Over limit'
_SERIES_NAME_THRESHOLD = 'Threshold'


class _Display(object):

    def setup(self):

        raise NotImplementedError('To be implemented in the derived class.')

    def display(self, uiData):

        raise NotImplementedError('To be implemented in the derived class.')


class _MenuItem(FUxCore.MenuItem):

    def __init__(self, menuItemSpec, menuItems):

        # Note FUxCore.MenuItem has no __init__() defined.
        self.__menuItemSpec = menuItemSpec
        self.__menuItems = menuItems
        self.__isChecked = False
        self.__isEnabled = True

    @FUxCore.aux_cb
    def Invoke(self, _cd):
        self.__menuItems.handleMenuItemInvoke(self.__menuItemSpec.name)

    def Applicable(self):
        return True

    def Enabled(self):
        return self.__isEnabled

    def Checked(self):
        return self.__isChecked

    def asCommand(self):

        return self.__menuItemSpec._replace(callback=self.getMenuItem)

    def getMenuItem(self):

        return self  # self is an FUxCore.MenuItem

    def setEnabled(self, isEnabled):

        self.__isEnabled = isEnabled

    def setChecked(self, isChecked):

        self.__isChecked = isChecked


class DisplayMenuItems(_Display):

    def __init__(self, menuItemCmdSpecs, dashboard):

        self.__dashboard = dashboard
        self.__menuItemMap = self._initMenuItemMap(menuItemCmdSpecs)

    def _initMenuItemMap(self, menuItemCmdSpecs):

        menuItemMap = {}
        for menuItemSpec in menuItemCmdSpecs:
            menuItemMap[menuItemSpec.name] = _MenuItem(menuItemSpec, self)
        return menuItemMap

    def handleMenuItemInvoke(self, cmdName):

        if cmdName == 'insertItems':
            self.__dashboard.OnInsertItemClicked()
        elif cmdName == 'export':
            self.__dashboard.OnExportClicked()
        elif cmdName == 'import':
            self.__dashboard.OnImportClicked()
        elif cmdName == 'refresh':
            self.__dashboard.OnRefreshClicked()
        elif cmdName == 'up':
            self.__dashboard.OnUpClicked()
        elif cmdName in FBDPDashboardDefaultConfig.DEFAULT_VIEW_TYPES:
            self.__dashboard.SetView(cmdName)
        elif cmdName == 'expiration':
            self.__dashboard.OnExpirationClicked()
        elif cmdName == 'aggregation':
            self.__dashboard.OnAggregationClicked()
        elif cmdName == 'deletePrices':
            self.__dashboard.OnDeletePricesClicked()
        elif cmdName == 'fxAggregation':
            self.__dashboard.OnFXAggregationClicked()
        elif cmdName == 'benchmarktest':
            self.__dashboard.OnBenchmarkTestClicked()
        elif cmdName == 'traderollout':
            self.__dashboard.OnTradeRolloutClicked()
        else:
            raise AssertionError('Undefined MenuItem name "{0}"'.format(
                    cmdName))

    def setup(self):

        self.__menuItemMap['trades'].setChecked(True)
        self.__menuItemMap['up'].setEnabled(True)

    def display(self, uiData):

        for name, menuItem in self.__menuItemMap.iteritems():
            if name in FBDPDashboardDefaultConfig.DEFAULT_VIEW_TYPES:
                menuItem.setChecked(uiData.viewType == name)

    def getCommands(self):

        return [menuItem.asCommand()
                for menuItem in self.__menuItemMap.itervalues()]


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
    def _splitResultDataListByThreshold(resultDataList):

        underLimitSeriesPoints = []
        overLimitSeriesPoints = []
        thresholdSeriesPoints = []
        for resultData in resultDataList:
            valuedSeriesPoint = _SeriesPoint(xLabel=resultData.categoryName,
                    yValue=resultData.count)
            zeroedSeriesPoint = _SeriesPoint(xLabel=resultData.categoryName,
                    yValue=0)
            thresholdSeriesPoint = _SeriesPoint(xLabel=resultData.categoryName,
                    yValue=resultData.threshold)
            if FBDPDashboardUtil.isResultDataOverLimit(resultData):
                underLimitSeriesPoints.append(zeroedSeriesPoint)
                overLimitSeriesPoints.append(valuedSeriesPoint)
            else:
                underLimitSeriesPoints.append(valuedSeriesPoint)
                overLimitSeriesPoints.append(zeroedSeriesPoint)
            thresholdSeriesPoints.append(thresholdSeriesPoint)
        return (underLimitSeriesPoints, overLimitSeriesPoints,
                thresholdSeriesPoints)

    @staticmethod
    def _prepareDataSeriesValues(seriesPointList):

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

    @staticmethod
    def _prepareThresholdSeriesValues(seriesPointList):

        # Prepend and postpend both empty string to x labels and
        # None to the y values
        xLabels = [''] + [sp.xLabel for sp in seriesPointList] + ['']
        yValues = [None] + [sp.yValue for sp in seriesPointList] + [None]
        # extrapolate left
        yValues[0] = yValues[1]
        # extrapolate right
        yValues[-1] = yValues[-2]
        # Make series value
        seriesValues = acm.FArray()
        for xLabel, yValue in itertools.izip(xLabels, yValues):
            seriesValues.Add(_SeriesPoint(xLabel, yValue))
        return seriesValues

    def _populateBarChartSeries(self, resultDataList, showThreshold=False):

        (underLimitSeriesPoints, overLimitSeriesPoints,
                 thresholdSeriesPoints) = (
                        self._splitResultDataListByThreshold(resultDataList))
        # Under limit
        underLimitSeriesValues = self._prepareDataSeriesValues(
                underLimitSeriesPoints)
        underLimitSeries = self._control.AddSeries(
                FBDPDashboardData.CHART_TYPE_BAR,
                underLimitSeriesValues.Size(), _FCOLOR_GREEN,
                _SERIES_NAME_UNDER_LIMIT)
        underLimitSeries.Populate(underLimitSeriesValues)
        # Over limit
        overLimitSeriesValues = self._prepareDataSeriesValues(
                overLimitSeriesPoints)
        overLimitSeries = self._control.AddSeries(
                FBDPDashboardData.CHART_TYPE_BAR,
                overLimitSeriesValues.Size(), _FCOLOR_RED,
                _SERIES_NAME_OVER_LIMIT)
        overLimitSeries.Populate(overLimitSeriesValues)
        # Threshold
        if showThreshold:
            thresholdSeriesValues = self._prepareDataSeriesValues(
                    thresholdSeriesPoints)
            thresholdSeries = self._control.AddSeries(
                    FBDPDashboardData.CHART_TYPE_PLOT,
                    overLimitSeriesValues.Size(), _FCOLOR_BLUE,
                    _SERIES_NAME_THRESHOLD)
            thresholdSeries.Populate(thresholdSeriesValues)
        # x label, take either one will work
        self._control.BaseXAxisLabelsOnSeries(overLimitSeries)

    def _populatePlotChartSeries(self, resultDataList):

        seriesPointList = [_SeriesPoint(xLabel=resultData.categoryName,
                yValue=resultData.count) for resultData in resultDataList]
        seriesValues = self._prepareDataSeriesValues(seriesPointList)
        series = self._control.AddSeries(FBDPDashboardData.CHART_TYPE_PLOT,
                seriesValues.Size(), _FCOLOR_BLACK)
        series.Populate(seriesValues)
        self._control.BaseXAxisLabelsOnSeries(series)

    def _populateChartSeries(self, uiData):

        chartType = uiData.chartType
        if chartType == FBDPDashboardData.CHART_TYPE_PLOT:
            self._populatePlotChartSeries(uiData.resultDataList)
        elif chartType == FBDPDashboardData.CHART_TYPE_BAR:
            self._populateBarChartSeries(uiData.resultDataList)
        else:
            raise NotImplementedError('No charting is implemented with '
                    'StepLine yet.')

    def display(self, uiData):

        if uiData.chartType not in FBDPDashboardData.VALID_2D_CHART_TYPES:
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


class DisplayPieChart(_Display):

    def __init__(self, uxPieChartControl):

        assert uxPieChartControl.IsKindOf('FUxPieChartControl')
        self._control = uxPieChartControl

    def _cbSectorValues(self, args, _cd):

        # args is in the form (object->[...], sectorIndex->1)
        _categoryName, count, _threshold, _recommendedActions = args.At(
                'object')

        pieSize = int(count)
        return pieSize

    def setup(self):

        self._control.ValuesEventHandler().Add(self._cbSectorValues, None)

    def display(self, uiData):

        if uiData.chartType not in FBDPDashboardData.VALID_PIE_CHART_TYPES:
            self._control.Visible(False)
            return
        self._control.Visible(True)
        # Turn off things
        self._control.Clear()
        self._control.ShowLegend(False)
        self._control.ShowValuesInLegend(False)
        self._control.ShowLabels(False)
        self._control.Enable3DView(False)
        # Prepare things
        for resultData in uiData.resultDataList:

            sector = self._control.AddSector(resultData.categoryName)
            sector.Populate(resultData)
        self._control.SetPieChartType(uiData.chartType)
        # Turn on things
        self._control.ShowLegend(True, uiData.viewType.upper())
        self._control.ShowValuesInLegend(True)
        self._control.ShowLabels(True)
        self._control.Enable3DView(True)
        self._control.Redraw()


class _DisplayListControl(_Display):

    def __init__(self, dashboard, uxListControl):

        assert uxListControl.IsKindOf('FUxListControl')
        _Display.__init__(self)
        self._dashboard = dashboard
        self._control = uxListControl

    def _removeAllColumns(self):

        for colIdx in reversed(list(range(self._control.ColumnCount()))):
            self._control.RemoveColumn(colIdx)

    def _adjustAllColumnsWidths(self):

        for colIdx in range(self._control.ColumnCount()):
            self._control.AdjustColumnWidthToFitItems(colIdx)


class DisplayConfigTab(_DisplayListControl):

    def setup(self):

        pass

    def display(self, uiData):

        # Remove and remake columns
        self._removeAllColumns()
        self._control.AddColumn('Drill Down')
        self._control.AddColumn('Description')
        self._control.AddColumn('Action')
        self._control.ShowColumnHeaders()
        self._control.ShowGridLines()
        # Populate rows
        self._control.RemoveAllItems()
        rootItem = self._control.GetRootItem()

        for configData in uiData.configDataList:
            child = rootItem.AddChild()
            child.Label(configData.name)
            child.Label(configData.description, 1)
            child.Label(configData.actionDescription, 2)
        # Adjust width only after all data are populated
        self._adjustAllColumnsWidths()


class DisplayResultTab(_DisplayListControl):

    def setup(self):

        self._control.AddCallback(
                "DefaultAction", self._dashboard.OnResultDoubleClick, self)

    def display(self, uiData):

        # Remove and remake columns
        self._removeAllColumns()
        colName1 = uiData.XAxisLabel
        colName2 = uiData.YAxisLabel
        colName3 = "Action recommendation"
        tooltip = "Double click on the rows below to drill down"
        self._control.AddColumn(colName1, len(colName1), tooltip)
        self._control.AddColumn(colName2, len(colName2), tooltip)
        self._control.AddColumn(colName3, len(colName3), tooltip)
        self._control.ShowColumnHeaders()
        self._control.ShowGridLines()
        # Populate rows
        self._control.RemoveAllItems()
        rootItem = self._control.GetRootItem()
        for resultData in uiData.resultDataList:
            child = rootItem.AddChild()
            child.Label(resultData.categoryName)
            child.Label(resultData.count, 1)
            child.Label(resultData.recommendedActions, 2)
            child.SetData(resultData.categoryName)
        # Adjust width only after all data are populated
        self._adjustAllColumnsWidths()

    def getSelectedItemData(self):

        return self._control.GetSelectedItem().GetData()
