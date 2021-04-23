'''
===================================================================================================
PURPOSE: The HedgeEffectivenessCharts module is responsible for visualising the Hedge Effectiveness
            Test results. It contains the report and output chart definitions and logic.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''
import clr

import acm
import FLogger

import HedgeConstants

clr.AddReference(HedgeConstants.STR_CLR_REFERENCE)
logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE)
# Formatters
intFormatter = acm.FDomain['int'].DefaultFormatter()
doubleFormatter = acm.FDomain['double'].DefaultFormatter()
dateFormatter = acm.FDomain['date'].DefaultFormatter()


def format_tradeNbr_output(trades):
    strTradeNbrs = ''
    for trade in trades:
        strTradeNbrs = strTradeNbrs + trade + ', '
    if strTradeNbrs:
        strTradeNbrs = strTradeNbrs[:-2]
    return strTradeNbrs


def get_max_abs_value(data, hedgeType):
    maxVal = 0
    for date in data:
        if hedgeType == 'Original':
            val = abs(round(data[date]['DOriginal'], 0))
        elif hedgeType == 'External':
            val = abs(round(data[date]['DExternal'], 0))
        else:
            val = 0
        if val > maxVal:
            maxVal = val

    return maxVal


class Chart(object):
    def __init__(self):
        self.m_chart = None
        self.m_chartArea = None
        xAxis = clr.System.Windows.Forms.DataVisualization.Charting.Axis()
        yAxis = clr.System.Windows.Forms.DataVisualization.Charting.Axis()
        xAxis.MajorGrid.Enabled = True
        yAxis.MajorGrid.Enabled = True
        xAxis.MinorGrid.Enabled = False
        yAxis.MinorGrid.Enabled = False
        xAxis.MajorGrid.LineColor = clr.System.Drawing.Color.LightGray
        yAxis.MajorGrid.LineColor = clr.System.Drawing.Color.LightGray
        xAxis.MajorGrid.IntervalOffset = 0.0
        yAxis.MajorGrid.IntervalOffset = 0.0
        xAxis.Crossing = 0.0
        yAxis.Crossing = 0.0
        xAxis.IsMarksNextToAxis = False
        yAxis.IsMarksNextToAxis = False
        xAxis.IsMarginVisible = True
        yAxis.IsMarginVisible = True
        self.m_chart = clr.System.Windows.Forms.DataVisualization.Charting.Chart()
        self.m_chart.BackColor = clr.System.Drawing.Color.White
        self.m_chart.Dock = clr.System.Windows.Forms.DockStyle.Fill
        self.m_chartArea = clr.System.Windows.Forms.DataVisualization.Charting.ChartArea()
        self.m_chartArea.AxisX = xAxis
        self.m_chartArea.AxisY = yAxis
        self.m_chartArea.Name = 'chartarea'
        self.m_chartArea.BackColor = clr.System.Drawing.Color.White
        self.m_chart.ChartAreas.Add(self.m_chartArea)
        self.m_chart.Size = clr.System.Drawing.Size(640, 480)

    def SaveChart(self, location):
        try:
            self.m_chart.SaveImage(location, clr.System.Drawing.Imaging.ImageFormat.Png)
        except Exception as e:
            logger.ELOG("Exception :- Error while saving the chart. %s" % str(e))


class RegressionChart(Chart):
    def __init__(self):
        super(RegressionChart, self).__init__()
        self.LabelAxes()
        self.InitSeries()

    def LabelAxes(self):
        self.m_chartArea.AxisX.Title = 'External Change'
        self.m_chartArea.AxisY.Title = 'Hypo Change'

    def InitSeries(self):
        # External Series
        self.m_seriesExternal = clr.System.Windows.Forms.DataVisualization.Charting.Series()
        self.m_seriesExternal.ChartArea = 'chartarea'
        self.m_seriesExternal.ChartType = clr.System.Windows.Forms.DataVisualization.\
            Charting.SeriesChartType.Line
        self.m_seriesExternal.YValuesPerPoint = 1
        self.m_seriesExternal.BorderWidth = 2
        self.m_seriesExternal.Color = clr.System.Drawing.Color.Black
        self.m_seriesExternal.BorderColor = clr.System.Drawing.Color.Blue
        self.m_seriesExternal.MarkerStyle = clr.System.Windows.Forms.DataVisualization.\
            Charting.MarkerStyle.Diamond
        self.m_seriesExternal.MarkerSize = 7

        # Original Series
        self.m_seriesOriginal = clr.System.Windows.Forms.DataVisualization.Charting.Series()
        self.m_seriesOriginal.ChartArea = 'chartarea'
        self.m_seriesOriginal.ChartType = clr.System.Windows.Forms.DataVisualization.\
            Charting.SeriesChartType.Line
        self.m_seriesOriginal.YValuesPerPoint = 1
        self.m_seriesOriginal.BorderWidth = 2
        self.m_seriesOriginal.Color = clr.System.Drawing.Color.Black
        self.m_seriesOriginal.BorderColor = clr.System.Drawing.Color.Blue
        self.m_seriesOriginal.MarkerStyle = clr.System.Windows.Forms.DataVisualization.\
            Charting.MarkerStyle.Diamond
        self.m_seriesOriginal.MarkerSize = 7

        # Scatter Series (Original vs Hedge), just crosses
        self.m_seriesScatter = clr.System.Windows.Forms.DataVisualization.Charting.Series()
        self.m_seriesScatter.ChartArea = 'chartarea'
        self.m_seriesScatter.ChartType = clr.System.Windows.Forms.DataVisualization.\
            Charting.SeriesChartType.Line
        self.m_seriesScatter.YValuesPerPoint = 1
        self.m_seriesScatter.BorderWidth = 0
        self.m_seriesScatter.Color = clr.System.Drawing.Color.Black
        self.m_seriesScatter.MarkerStyle = clr.System.Windows.Forms.DataVisualization.\
            Charting.MarkerStyle.Cross
        self.m_seriesScatter.MarkerSize = 10

        # Regression Series
        self.m_seriesRegression = clr.System.Windows.Forms.DataVisualization.Charting.Series()
        self.m_seriesRegression.ChartArea = 'chartarea'
        self.m_seriesRegression.ChartType = clr.System.Windows.Forms.DataVisualization.\
            Charting.SeriesChartType.Line
        self.m_seriesRegression.YValuesPerPoint = 1
        self.m_seriesRegression.BorderWidth = 1
        self.m_seriesRegression.Color = clr.System.Drawing.Color.Purple
        self.m_seriesRegression.BorderDashStyle = clr.System.Windows.Forms.DataVisualization.\
            Charting.ChartDashStyle.Solid
        self.m_seriesRegression.MarkerStyle = clr.System.Windows.Forms.DataVisualization.\
            Charting.MarkerStyle.None

        # Add Series to Chart
        self.m_chart.Series.Add(self.m_seriesOriginal)
        self.m_chart.Series.Add(self.m_seriesExternal)
        self.m_chart.Series.Add(self.m_seriesScatter)
        self.m_chart.Series.Add(self.m_seriesRegression)

    def UpdateChart(self, results):
        data = results['data']
        dates = data.keys()
        dates.sort()
        alpha = float(results['alpha'])
        beta = float(results['beta'])
        for date in dates:
            d_x = data[date]['DOriginal']
            d_y = data[date]['DExternal']
            self.m_seriesScatter.Points.AddXY(d_x, d_y)
            value = alpha + (d_x * beta)
            self.m_seriesRegression.Points.AddXY(d_x, value)

        xAxis = self.m_chartArea.AxisX
        yAxis = self.m_chartArea.AxisY
        xVal = round(1.2 * get_max_abs_value(data, 'Original'), 0)
        yVal = round(1.2 * get_max_abs_value(data, 'External'), 0)
        maxVal = max(xVal, yVal)
        xAxis.Minimum = -maxVal
        yAxis.Minimum = -maxVal
        xAxis.Maximum = maxVal
        yAxis.Maximum = maxVal
        xAxis.MajorGrid.Interval = maxVal / 5
        yAxis.MajorGrid.Interval = maxVal / 5

    def ClearChart(self):
        self.m_seriesOriginal.Points.Clear()
        self.m_seriesExternal.Points.Clear()
        self.m_seriesScatter.Points.Clear()
        self.m_seriesRegression.Points.Clear()

    def EnableSeries(self, enableOriginal=False, enableExternal=False, enableScatter=False,
                     enableRegression=False):

        self.m_seriesOriginal.Enabled = enableOriginal
        self.m_seriesExternal.Enabled = enableExternal
        self.m_seriesScatter.Enabled = enableScatter
        self.m_seriesRegression.Enabled = enableRegression


class VRMChart(Chart):

    def __init__(self):
        super(VRMChart, self).__init__()
        self.LabelAxes()
        self.InitSeries()

    def LabelAxes(self):
        self.m_chartArea.AxisX.Title = 'Date'
        self.m_chartArea.AxisY.Title = 'Variable Reduction %'

    def InitSeries(self):
        # Variable Reduction Series
        self.m_seriesVRM = clr.System.Windows.Forms.DataVisualization.Charting.Series()
        self.m_seriesVRM.ChartArea = 'chartarea'
        self.m_seriesVRM.ChartType = clr.System.Windows.Forms.DataVisualization.\
            Charting.SeriesChartType.Line
        self.m_seriesVRM.YValuesPerPoint = 1
        self.m_seriesVRM.BorderWidth = 2
        self.m_seriesVRM.Color = clr.System.Drawing.Color.Black
        self.m_seriesVRM.BorderColor = clr.System.Drawing.Color.Blue
        self.m_seriesVRM.MarkerStyle = clr.System.Windows.Forms.DataVisualization.\
            Charting.MarkerStyle.Diamond
        self.m_seriesVRM.MarkerSize = 7
        self.m_seriesVRM.XValueType = clr.System.Windows.Forms.DataVisualization.\
            Charting.ChartValueType.DateTime

        # Lo Warning Series
        self.m_seriesLoWarning = clr.System.Windows.Forms.DataVisualization.Charting.Series()
        self.m_seriesLoWarning.ChartArea = 'chartarea'
        self.m_seriesLoWarning.ChartType = clr.System.Windows.Forms.DataVisualization.\
            Charting.SeriesChartType.Line
        self.m_seriesLoWarning.YValuesPerPoint = 1
        self.m_seriesLoWarning.BorderWidth = 2
        self.m_seriesLoWarning.Color = clr.System.Drawing.Color.Orange
        self.m_seriesLoWarning.BorderColor = clr.System.Drawing.Color.Blue
        self.m_seriesLoWarning.XValueType = clr.System.Windows.Forms.DataVisualization.\
            Charting.ChartValueType.DateTime

        # Lo Limit Series
        self.m_seriesLoLimit = clr.System.Windows.Forms.DataVisualization.Charting.Series()
        self.m_seriesLoLimit.ChartArea = 'chartarea'
        self.m_seriesLoLimit.ChartType = clr.System.Windows.Forms.DataVisualization.\
            Charting.SeriesChartType.Line
        self.m_seriesLoLimit.YValuesPerPoint = 1
        self.m_seriesLoLimit.BorderWidth = 2
        self.m_seriesLoLimit.Color = clr.System.Drawing.Color.Red
        self.m_seriesLoLimit.BorderColor = clr.System.Drawing.Color.Blue
        self.m_seriesLoLimit.XValueType = clr.System.Windows.Forms.DataVisualization.\
            Charting.ChartValueType.DateTime

        # Add Series
        self.m_chart.Series.Add(self.m_seriesVRM)
        self.m_chart.Series.Add(self.m_seriesLoWarning)
        self.m_chart.Series.Add(self.m_seriesLoLimit)

    def UpdateChart(self, results, warning, limit):
        data = results['data']
        dates = data.keys()
        dates.sort()

        counter = 0
        for date in dates:
            # we don't want to plot the first point since the first point
            # can never have a delta value.
            if counter > 0:
                v_r = results['vr'][date]

                date = clr.System.DateTime.Parse(date)
                self.m_seriesVRM.Points.AddXY(date.ToOADate(), v_r * 100)
                self.m_seriesLoWarning.Points.AddXY(date.ToOADate(), warning * 100)
                self.m_seriesLoLimit.Points.AddXY(date.ToOADate(), limit * 100)

            counter += 1

        xAxis = self.m_chartArea.AxisX
        yAxis = self.m_chartArea.AxisY

        start_date = clr.System.DateTime.Parse(dates[0])
        last_date = clr.System.DateTime.Parse(dates[-1])

        xAxis_range = last_date.Subtract(start_date).TotalDays
        xAxis_range = round(xAxis_range / (365.25 / 12), 0) + 1
        end_date = start_date.AddMonths(xAxis_range)

        xAxis.InterOffsetType = clr.System.Windows.Forms.DataVisualization.\
            Charting.DateTimeIntervalType.Months
        xAxis.IntervalOffset = 0
        xAxis.Interval = xAxis_range

        xAxis.Minimum = start_date.ToOADate()
        xAxis.Maximum = end_date.ToOADate()
        xAxis.MajorGrid.Interval = xAxis_range

        yAxis.Minimum = 50
        yAxis.Maximum = 100

        yAxis.MajorGrid.Interval = 5

    def ClearChart(self):
        self.m_seriesVRM.Points.Clear()
        self.m_seriesLoWarning.Points.Clear()
        self.m_seriesLoLimit.Points.Clear()

    def EnableSeries(self, enableVRM=False, enableWarning=False, enableLimit=False):
        self.m_seriesVRM.Enabled = enableVRM
        self.m_seriesLoWarning.Enabled = enableWarning
        self.m_seriesLoLimit.Enabled = enableLimit


class DOChart(Chart):
    def __init__(self):
        super(DOChart, self).__init__()
        self.LabelAxes()
        self.InitSeries()

    def LabelAxes(self):
        self.m_chartArea.AxisX.Title = 'Date'
        self.m_chartArea.AxisY.Title = 'Dollar Offset %'

    def InitSeries(self):
        # Dollar Offset Series
        self.m_seriesDO = clr.System.Windows.Forms.DataVisualization.Charting.Series()
        self.m_seriesDO.ChartArea = 'chartarea'
        self.m_seriesDO.ChartType = clr.System.Windows.Forms.DataVisualization.\
            Charting.SeriesChartType.Line
        self.m_seriesDO.YValuesPerPoint = 1
        self.m_seriesDO.BorderWidth = 2
        self.m_seriesDO.Color = clr.System.Drawing.Color.Black
        self.m_seriesDO.BorderColor = clr.System.Drawing.Color.Blue
        self.m_seriesDO.MarkerStyle = clr.System.Windows.Forms.DataVisualization.Charting.\
            MarkerStyle.Diamond
        self.m_seriesDO.MarkerSize = 7
        self.m_seriesDO.XValueType = clr.System.Windows.Forms.DataVisualization.\
            Charting.ChartValueType.DateTime

        # Lo Warning Series
        self.m_seriesLoWarning = clr.System.Windows.Forms.DataVisualization.Charting.Series()
        self.m_seriesLoWarning.ChartArea = 'chartarea'
        self.m_seriesLoWarning.ChartType = clr.System.Windows.Forms.DataVisualization.\
            Charting.SeriesChartType.Line
        self.m_seriesLoWarning.YValuesPerPoint = 1
        self.m_seriesLoWarning.BorderWidth = 2
        self.m_seriesLoWarning.Color = clr.System.Drawing.Color.Orange
        self.m_seriesLoWarning.BorderColor = clr.System.Drawing.Color.Blue
        self.m_seriesLoWarning.XValueType = clr.System.Windows.Forms.DataVisualization.\
            Charting.ChartValueType.DateTime

        # Hi Warning Series
        self.m_seriesHiWarning = clr.System.Windows.Forms.DataVisualization.Charting.Series()
        self.m_seriesHiWarning.ChartArea = 'chartarea'
        self.m_seriesHiWarning.ChartType = clr.System.Windows.Forms.DataVisualization.\
            Charting.SeriesChartType.Line
        self.m_seriesHiWarning.YValuesPerPoint = 1
        self.m_seriesHiWarning.BorderWidth = 2
        self.m_seriesHiWarning.Color = clr.System.Drawing.Color.Orange
        self.m_seriesHiWarning.BorderColor = clr.System.Drawing.Color.Blue
        self.m_seriesHiWarning.XValueType = clr.System.Windows.Forms.DataVisualization.\
            Charting.ChartValueType.DateTime

        # Lo Limit Series
        self.m_seriesLoLimit = clr.System.Windows.Forms.DataVisualization.Charting.Series()
        self.m_seriesLoLimit.ChartArea = 'chartarea'
        self.m_seriesLoLimit.ChartType = clr.System.Windows.Forms.DataVisualization.\
            Charting.SeriesChartType.Line
        self.m_seriesLoLimit.YValuesPerPoint = 1
        self.m_seriesLoLimit.BorderWidth = 2
        self.m_seriesLoLimit.Color = clr.System.Drawing.Color.Red
        self.m_seriesLoLimit.BorderColor = clr.System.Drawing.Color.Blue
        self.m_seriesLoLimit.XValueType = clr.System.Windows.Forms.DataVisualization.\
            Charting.ChartValueType.DateTime

        # Hi Limit Series
        self.m_seriesHiLimit = clr.System.Windows.Forms.DataVisualization.Charting.Series()
        self.m_seriesHiLimit.ChartArea = 'chartarea'
        self.m_seriesHiLimit.ChartType = clr.System.Windows.Forms.DataVisualization.\
            Charting.SeriesChartType.Line
        self.m_seriesHiLimit.YValuesPerPoint = 1
        self.m_seriesHiLimit.BorderWidth = 2
        self.m_seriesHiLimit.Color = clr.System.Drawing.Color.Red
        self.m_seriesHiLimit.BorderColor = clr.System.Drawing.Color.Blue
        self.m_seriesHiLimit.XValueType = clr.System.Windows.Forms.DataVisualization.\
            Charting.ChartValueType.DateTime

        # Add Series
        self.m_chart.Series.Add(self.m_seriesDO)
        self.m_chart.Series.Add(self.m_seriesLoWarning)
        self.m_chart.Series.Add(self.m_seriesLoLimit)
        self.m_chart.Series.Add(self.m_seriesHiWarning)
        self.m_chart.Series.Add(self.m_seriesHiLimit)

    def UpdateChart(self, results, warnings, limits):
        data = results['data']
        dates = data.keys()
        dates.sort()

        counter = 0
        for date in dates:
            # we don't want to plot the first point since the first point
            # can never have a delta value.
            if counter > 0:
                d_o = results['do'][date]

                date = clr.System.DateTime.Parse(date)
                self.m_seriesDO.Points.AddXY(date.ToOADate(), d_o * 100)
                self.m_seriesLoWarning.Points.AddXY(date.ToOADate(), warnings[0] * 100)
                self.m_seriesLoLimit.Points.AddXY(date.ToOADate(), limits[0] * 100)
                self.m_seriesHiWarning.Points.AddXY(date.ToOADate(), warnings[1] * 100)
                self.m_seriesHiLimit.Points.AddXY(date.ToOADate(), limits[1] * 100)

            counter += 1

        xAxis = self.m_chartArea.AxisX
        yAxis = self.m_chartArea.AxisY
        start_date = clr.System.DateTime.Parse(dates[0])
        last_date = clr.System.DateTime.Parse(dates[-1])

        xAxis_range = last_date.Subtract(start_date).TotalDays
        xAxis_range = round(xAxis_range / (365.25 / 12), 0) + 1
        end_date = start_date.AddMonths(xAxis_range)

        xAxis.InterOffsetType = clr.System.Windows.Forms.DataVisualization.\
            Charting.DateTimeIntervalType.Months
        xAxis.IntervalOffset = 0
        xAxis.Interval = xAxis_range

        xAxis.Minimum = start_date.ToOADate()
        xAxis.Maximum = end_date.ToOADate()
        xAxis.MajorGrid.Interval = xAxis_range

        yAxis.Minimum = 30
        yAxis.Maximum = 150

        yAxis.MajorGrid.Interval = 5

    def ClearChart(self):
        self.m_seriesDO.Points.Clear()
        self.m_seriesLoWarning.Points.Clear()
        self.m_seriesLoLimit.Points.Clear()
        self.m_seriesHiWarning.Points.Clear()
        self.m_seriesHiLimit.Points.Clear()

    def EnableSeries(self, enableDO=False, enableWarning=False, enableLimit=False):
        self.m_seriesDO.Enabled = enableDO
        self.m_seriesLoWarning.Enabled = enableWarning
        self.m_seriesLoLimit.Enabled = enableLimit
        self.m_seriesHiWarning.Enabled = enableWarning
        self.m_seriesHiLimit.Enabled = enableLimit
