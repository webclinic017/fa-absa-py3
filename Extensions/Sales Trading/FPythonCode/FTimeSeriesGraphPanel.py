""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FTimeSeriesGraphPanel.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FTimeSeriesGraphPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""
import time

import acm
from FEvent import OnError
from FTimeSeriesObject import TimeSeriesObject
from FIntegratedWorkbenchLogging import logger
from FPanel import Panel

from datetime import datetime


class TimeSeriesGraphPanel(Panel):

    def __init__(self):
        Panel.__init__(self)
        self._graph = None
        self._timeSeriesSpecCtrl = None
        self._endDateCtrl = None
        self._startDateCtrl = None
        self._currentObject = None
        self._latestStartDate = None
        self._latestEndDate = None
        self._timeSeriesObject = None
        self._listCtrl = None
        self._listDateIdx = None
        self._listValueIdx = None
        self._lastSelectedTimeSeriesSpec = None
        self._timeSeriesCache = {}

    def Graph(self):
        return self._graph

    def SetGraphControl(self, layout):
        self._graph = layout.GetControl('graph')

    def ListLayout(self):
        self._listDateIdx = self._listCtrl.AddColumn('Date')
        self._listValueIdx = self._listCtrl.AddColumn('Value')
        self._listCtrl.ShowColumnHeaders()

    def InitControls(self, layout):
        self._timeSeriesSpecCtrl = layout.GetControl('timeSeriesSpecCtrl')
        self._listCtrl = layout.GetControl('listCtrl')
        self._startDateCtrl = layout.GetControl('startDateCtrl')
        self._endDateCtrl = layout.GetControl('endDateCtrl')
        self.SetGraphControl(layout)

        self._timeSeriesSpecCtrl.EnableMultiSelect()
        self._timeSeriesSpecCtrl.Populate([])
        self.ListLayout()

        self.AddEventHandlers()
        self.AddLayoutCallbacks()

    def AddEventHandlers(self):
        self._graph.XValuesEventHandler().Add(self.GetXValue, self)
        self._graph.YValuesEventHandler().Add(self.GetYValue, self)
        self._graph.XAxisLabelsEventHandler().Add(self.XAxisLabels, self)
        self._graph.TooltipsTextEventHandler().Add(self.ToolTip, self)

    def AddLayoutCallbacks(self):
        self._timeSeriesSpecCtrl.AddCallback('Changed', self.TimeSeriesSpecCtrlChanged, None)
        self._startDateCtrl.AddCallback('Activate', self.DateCtrlChanged, self._startDateCtrl)
        self._endDateCtrl.AddCallback('Activate', self.DateCtrlChanged, self._endDateCtrl)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('None')
        b.  BeginVertBox('None')
        b.  Add2DChart('graph', self.Settings().Width(), self.Settings().Height())
        b.  EndBox()
        b.  BeginHorzBox('EtchedIn')
        b.    BeginVertBox()
        b.      AddList('timeSeriesSpecCtrl')
        b.      AddInput('startDateCtrl', 'Start date')
        b.      AddInput('endDateCtrl', 'End date')
        b.    EndBox()
        b.    BeginVertBox()
        b.      AddList('listCtrl')
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b

    def TimeSeriesSpecCtrlChanged(self, evt=None, data=None):
        self.Clear()
        self.LastSelectedSpec(self._timeSeriesSpecCtrl.GetData())
        if self.LastSelectedSpec():
            self._timeSeriesObject = TimeSeriesObject(
                self.LastSelectedSpec(),
                self.CurrentObject(),
                self.TimeSeriesValues(self.CurrentObject(), self.LastSelectedSpec())
                )
            try:
                self._timeSeriesObject.SetStartEndIndices(*self.DefaultStartEndIndices())
            except AssertionError:
                logger.debug('Failed to set default start and end dates since end date wasn\'t later than start date')
            self.Redraw()
            self.PopulateDateCtrls()
            self.ListAsListItems()

    def CurrentObject(self, currentObject=None):
        if currentObject is None:
            return self._currentObject
        self._currentObject = currentObject

    def LastSelectedSpec(self, lastSelectedSpec=None):
        if lastSelectedSpec is None:
            return self._lastSelectedTimeSeriesSpec
        self._lastSelectedTimeSeriesSpec = lastSelectedSpec
        
    def DefaultSpec(self):
        return acm.FTimeSeriesSpec[self.Settings().DefaultTimeSpec()]

    def DateCtrlChanged(self, evt=None, data=None):
        try:
            msg = None
            self._latestStartDate = self.AsDate(self._startDateCtrl.GetData())
            self._latestEndDate = self.AsDate(self._endDateCtrl.GetData())

            startIdx = self.IndexForClosestDate(self._latestStartDate)
            endIdx = self.IndexForClosestDate(self._latestEndDate)
            self._timeSeriesObject.SetStartEndIndices(startIdx, endIdx)
        except (ValueError, TypeError):
            msg = 'Invalid date period format'
        except AssertionError:
            msg = 'End date must be later than start date'
        if msg is not None:
            self.SendEvent(OnError(self, 'Information', msg))
        self.PopulateDateCtrls()
        self.Redraw()
        
    def CurrentObjectChanged(self, currentObject):
        return self.CurrentObject() != currentObject

    def Selected(self, event):
        newObject = event.First()
        if self.CurrentObjectChanged(newObject):
            self.CurrentObject(newObject)
            self.Clear()
            self.ClearTimeSpecListAndPopulate()
            self.SetSelection()
 
    def SetSelection(self):
        timeSeriesSpec = self.LastSelectedSpec() or self.DefaultSpec()
        if timeSeriesSpec:
            items = self._timeSeriesSpecCtrl.GetRootItem().Children()
            selectedItem = next(item for item in items if item.GetData() == timeSeriesSpec)
            selectedItem.Select(True)
    
    def Clear(self):
        self.ClearGraph()
        self.ClearDateCtrls()
        self.ClearListCtrl()
        self._timeSeriesObject = None

    def ClearGraph(self, evt=None, data=None):
        if self._graph:
            self._graph.ClearChart()

    def ClearTimeSpecListAndPopulate(self):
        self._timeSeriesSpecCtrl.Clear()
        if self.CurrentObject():
            self.AddTimeSeriesToListCtrl()

    def ClearListCtrl(self):
        self._listCtrl.Clear()

    def ClearDateCtrls(self):
        self._startDateCtrl.Clear()
        self._endDateCtrl.Clear()

    def PopulateGraph(self):
        try:
            self.AddSeries()
            self._graph.Redraw()
        except StandardError as e:
            logger.error('Failed to populate graph. Reason: %s', e)

    def DefaultStartEndIndices(self):
        startDate = (self._latestStartDate or
                     self.AsDate(self.Settings().StartDate()))
        endDate = (self._latestEndDate or
                   self.AsDate(self.Settings().EndDate()))
        return self.IndexForClosestDate(startDate), self.IndexForClosestDate(endDate)

    def IndexForClosestDate(self, date):
        timeStruct = time.strptime(date, '%Y-%m-%d')
        fullDates = self._timeSeriesObject.FullDates()
        closestDateIndex = min(range(len(fullDates)),
            key=lambda i: abs(time.mktime(timeStruct) - time.mktime(time.strptime(fullDates[i], '%Y-%m-%d'))))
        return closestDateIndex

    def PopulateDateCtrls(self):
        dateList = self._timeSeriesObject.Dates()
        self._startDateCtrl.SetData(dateList[0])
        self._endDateCtrl.SetData(dateList[-1])

    def UpdateCaption(self):
        try:
            self.SetCaption(self.CurrentObject().StringKey())
        except AttributeError:
            pass

    def ResetCaption(self):
        self.SetCaption(self.Settings().Caption())

    def TimeSeriesValues(self, currentObject, spec):
        key = (currentObject.Name(), spec.FieldName())
        try:
            return self._timeSeriesCache[key]
        except KeyError:
            timeSeries = self._CreateTimeSeriesValues(currentObject, spec)
            self._timeSeriesCache[key] = timeSeries
            return timeSeries

    def _CreateTimeSeriesValues(self, obj, spec):
        query = 'recaddr = {0} and timeSeriesSpec = {1} and day > {2}'.format(
            obj.Oid(),
            spec.Oid(),
            self.AsDate(self.Settings().FromDate())
            )
        timeSeries = acm.FTimeSeries.Select(query).SortByProperty('Day')
        if timeSeries:
            start = timeSeries.First().Day()
            timeSeriesValues = [self.Coordinates(ts, start) for ts in timeSeries]
            return timeSeriesValues
        else:
            return []

    def AddTimeSeriesToListCtrl(self):
        root = self._timeSeriesSpecCtrl.GetRootItem()
        for spec in sorted(self.TimeSeriesSpecsToDisplay()):
            item = root.AddChild()
            item.SetData(spec)
            item.Label(spec.FieldName())

    def TimeSeriesSpecsToDisplay(self):
        if list(self.Settings().TimeSeriesSpecs()):
            return [acm.FTimeSeriesSpec[fieldName] for fieldName in self.Settings().TimeSeriesSpecs()]
        else:
            mappedTable = acm.Pom().MappedTable(self.CurrentObject().Class()).Name().Text()
            return [spec for spec in acm.FTimeSeriesSpec.Instances() if spec.RecType() == mappedTable]

    def ListAsListItems(self):
        root = self._listCtrl.GetRootItem()
        vals = self._timeSeriesObject.YValues(filtered=False)
        for a, date in enumerate(self._timeSeriesObject.Dates(filtered=False)):
            item = root.AddChild()
            item.Label(date)
            item.Label(vals[a], 1)
            item.SetData(date)
        self._listCtrl.AdjustColumnWidthToFitItems(0)
        self._listCtrl.AdjustColumnWidthToFitItems(1)
        
    def Dates(self):
        self._timeSeriesObject.Dates()

    def XAxisLabels(self, args, cd):
        return self._timeSeriesObject.Dates()[args.At('objectIndex')]

    def ShowLegend(self):
        self._graph.ShowLegend(True)

    def Redraw(self):
        self.ClearGraph()

        self.PopulateGraph()
        self.SetAxisTitles()

    def SetAxisTitles(self):
        self._graph.SetAxisTitles('Time', 'Value')

    def GetXValue(self, args, cd):
        return args.At('object')

    def GetYValue(self, args, cd):
        return self._timeSeriesObject.YValues()[args.At('objectIndex')]

    def ToolTip(self, args, cd):
        return '{0}\n{1}'.format(
            self.XAxisLabels(args, cd),
            self.Formatted(self.GetYValue(args, cd)))

    def AddSeries(self):
        series = self._graph.AddSeries('Plot', self._timeSeriesObject.Length(), color=self._timeSeriesObject.Color())
        series.SetPointStyle(
            self._timeSeriesObject.PointStyle(),
            self._timeSeriesObject.PointSize(), 
            self._timeSeriesObject.Color())
        series.SetBorderWidth(self._timeSeriesObject.LineWidth())
        series.Populate(self._timeSeriesObject.DateInd())
        self._graph.BaseXAxisLabelsOnSeries(series)

    @classmethod
    def Coordinates(cls, ts, start):
        return (cls.DateDiff(start, ts.Day()),
                ts.TimeValue(),
                ts.Day())

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
        except StandardError:
            return number

    @staticmethod
    def DateDiff(start, end):
        return acm.Time.DateDifference(end, start)

    @staticmethod
    def AsDate(variant):
        return DateVariant(variant).Value()


class DateVariant(object):

    EPOCH = datetime(1970, 1, 1)
    DATE_FORMAT = '%Y-%m-%d'
    DATE_LENGTH = len(EPOCH.strftime(DATE_FORMAT))

    def __init__(self, variant):
        self._variant = str(variant)

    def IsDate(self):
        try:
            return bool(
                        self._variant and
                        len(self._variant) == self.DATE_LENGTH and
                        datetime.strptime(self._variant, self.DATE_FORMAT)
                        )
        except (TypeError, ValueError):
            return False

    def IsDatePeriod(self):
        try:
            return bool(acm.Time.DatePeriodToString(self._variant))
        except TypeError:
            return False

    def Value(self):
        if self.IsDate():
            return self._variant
        elif self.IsDatePeriod():
            return acm.Time.PeriodSymbolToDate(self._variant)
        raise TypeError('Could not convert {0} to a valid date.'.format(self._variant))