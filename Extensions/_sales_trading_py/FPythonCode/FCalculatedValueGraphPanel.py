""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCalculatedValueGraphPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCalculatedValueGraphPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
from FPanel import Panel
import FGraphPlotter

class CalculatedValueGraphPanel(Panel):

    def __init__(self):
        Panel.__init__(self)
        plotters = self.GetPlotters()
        self._view = None
        self._graph = None
        self._row = None
        self._lastSelectedRow = None
        self._plotters = plotters
        self._coordinates = []

    def Graph(self):
        return self._graph

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  Add2DChart('graph', self.Settings().Width(), self.Settings().Height())
        b.EndBox()
        return b

    def GetPlotters(self):
        return [cls() for cls in self.PlotterCollection()]

    def PlotterCollection(self):
        return FGraphPlotter.Plot.Plotters()

    def InitControls(self, layout):
        self.SetGraphControl(layout)
        self.SetAxisTitles()
        self.ShowLegend()
        self.Draw()
        self.AddEventHandlers()

    def UpdateCaption(self):
        try:
            self.SetCaption(self._row.StringKey())
        except AttributeError:
            pass

    def ResetCaption(self):
        self.SetCaption(self.Settings().Caption())

    def Clear(self):
        self.ClearGraph()
        self.ResetCaption()

    def Instrument(self):
        try:
            return self._row.Instrument()
        except AttributeError:
            self.Logger().warn('Row {0} does not have attribute '
                'Instrument'. format(self._row.StringKey()))

    def PopulateCoordinates(self):
        instrument = self.Instrument()
        for plotter in self._plotters:
            self._coordinates.append(plotter.Coordinates(instrument))

    def ShowLegend(self):
        self._graph.ShowLegend(True)

    def Redraw(self):
        self.ClearCoordinates()
        self.PopulateCoordinates()
        self.ClearGraph()
        self.PopulateGraph()
        self.SetAxisTitles()
        self.ShowLegend()

    def LastSelectedRowRanged(self, row):
        return self._row != row

    def Selected(self, event):
        row = next((row for row in event.Objects()), None)
        if self.LastSelectedRowRanged(row):
            self._row = row
            self.Draw()

    def Draw(self):
        if self._row is None:
            self.Clear()
        else:
            self.Redraw()

    def SetGraphControl(self, layout):
        self._graph = layout.GetControl('graph')

    def AddEventHandlers(self):
        self._graph.XValuesEventHandler().Add(self.GetXValue, self)
        self._graph.YValuesEventHandler().Add(self.GetYValue, self)
        self._graph.TooltipsTextEventHandler().Add(self.ToolTip, self)

    def SetAxisTitles(self):
        for plotter in self._plotters:
            titles = plotter.AxisTitles()
            if titles:
                self._graph.SetAxisTitles(*titles)
                return True
        return False

    def GetXValue(self, args, cd):
        return args.At('object')

    def GetYValue(self, args, cd):
        return self.GraphYValue(args.At('seriesIndex'),
            args.At('objectIndex'))

    def ToolTip(self, args, cd):
        return '{0}\n{1}'.format(
            self.Formatted(self.GetXValue(args, cd)),
            self.Formatted(self.GetYValue(args, cd)))

    def AddSeries(self):
        for index, plotter in enumerate(self._plotters):
            xValues = self.XValues(index)
            series = self._graph.AddSeries(
                'Plot',
                len(xValues),
                plotter.Color(),
                plotter.Name()
                )
            if plotter.ShowPoints():
                series.SetPointStyle(
                    plotter.PointStyle(),
                    plotter.PointSize(),
                    plotter.Color())
            series.Populate(xValues)

    def ClearCoordinates(self):
        self._coordinates = []

    def PopulateGraph(self):
        try:
            self.AddSeries()
            self._graph.Redraw()
        except Exception as e:
            self.Logger().warn('Failed to populate graph. Reason: %s', e)

    def ClearGraph(self):
        if self._graph:
            self._graph.ClearChart()

    def XValues(self, index):
        try:
            return [c[0] for c in self._coordinates[index]]
        except IndexError:
            return [0]

    def GraphYValue(self, series, index):
        try:
            return self._coordinates[series][index][1]
        except Exception as e:
            self.Logger().warn('Failed to get Y coordinate. Reason: %s', e)
            return 0

    @staticmethod
    def Formatted(number):
        try:
            if (hasattr(number, 'IsKindOf') and
                number.IsKindOf(acm.FDenominatedValue)):
                return acm.DenominatedValue(
                    round(float(number), 2),
                    number.Unit(),
                    None)
            return round(float(number), 2)
        except Exception:
            return number
