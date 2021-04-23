""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendCommon.py"
from __future__ import print_function
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendCommon

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Common controls and panels used by workbenches.

------------------------------------------------------------------------------------------------"""
from collections import OrderedDict
import hashlib
import traceback
import acm
from FPanelCreator import Creator
from FSheetPanel import SheetPanel
from FACMObserver import SheetObserver
from FWorkbookPanel import DefaultWorkbookPanel
from FWorkbenchObserver import WorkbenchObserver
import FGrouperUtils
from FSecLendUtils import fn_timer
import FIntegratedWorkbench
import FSheetUtils

# ----------------------------------------------------------------------------------------------
#  Workbench common classes

class InsertItemHandlerMixin:
    """Provides functionality for handling insert items in sheets. Implemented as a mixin
    to support both Sheet Panels and sheets in workbooks.
    """

    def DefaultInsertItemQuery(self):
        """Return the default insert item query without any workbench view
        specific filtering applied.
        """
        raise NotImplementedError('Sheet must supply a default insert item query')

    def ApplyAdditionalQueryFilters(self, query):
        """Apply additional filtering to the insert item query based on the
        current state of the workbench view.
        """
        return query

    def UpdateSheetContents(self):
        """Call to refresh the sheet contents based on current workbench state."""
        contents = []
        if self.ShowSheetContents():
            query = self._InsertItemQuery() or self.DefaultInsertItemQuery()
            if query:
                folder = acm.FASQLQueryFolder()
                folder.Name(self.QueryFolderLabel())
                folder.AsqlQuery(self.ApplyAdditionalQueryFilters(query))
                contents = folder
        self._SetSheetContents(contents)
        return contents if contents else None

    def ShowSheetContents(self):
        """Return whether or not to display the insert item query in the sheet."""
        return True

    def QueryFolderLabel(self):
        settings = self.Settings()
        return settings.InsertItemFolderLabel() or settings.Caption()

    @staticmethod
    def InitSheetContents(self):
        # If content is being stored with the sheet, don't initialise
        # additional content programatically also.
        return self.UpdateSheetContents()

    def _SetSheetContents(self, contents):
        self.Sheet().InsertObject(contents)
        self.Sheet().ExpandTree(self.Settings().ExpandTreeLevels())

    def _InsertItemQuery(self):
        name = self.Settings().InsertItemQuery()
        queryClass = self.Settings().InsertItemQueryClass()
        if name and queryClass:
            # Shared queries only
            storedQuery = acm.FStoredASQLQuery.Select01(
                'name="{}" and subType="{}" and user=None'.format(name, queryClass), '')
            if storedQuery:
                return storedQuery.Query()


class CommonSheetPanelBase(SheetPanel):
    """Common extensions to the default Integrated Workbench sheet panel."""

    def InitControls(self, layout):
        # TODO: Move to Integrated Workbench / FSheetUtils?
        super(CommonSheetPanelBase, self).InitControls(layout)
        self.Sheet().ShowRowHeaders(self.Settings().ShowRowHeaders())
        self.Sheet().ShowGroupLabels(self.Settings().ShowGroupLabels())


class InsertItemSheetPanel(CommonSheetPanelBase, InsertItemHandlerMixin):
    """Extends the common sheet panel with functionality for handling
    dynamically changing insert item queries.
    """
    @fn_timer
    def InitSheetContents(self):
        CommonSheetPanelBase.InitSheetContents(self)
        InsertItemHandlerMixin.InitSheetContents(self)

class WorkbenchSheet(object, InsertItemHandlerMixin):
    """Represents a sheet in a workbench workbook."""
    # TODO: Reimplements much of what is provided by the SheetPanel. Should
    # probably be moved to a common base class between them.
    
    ON_IDLE_FREQ = 1

    def __init__(self, workbookPanel, settings):
        self._workbookPanel = workbookPanel
        self._settings = settings
        self._sheetName = self._SheetNameFromTemplate()
        self._sheet = self._SheetFromWorkbook()
        self._sheetObserver = None
        self._workbenchObserver = None
        self._onIdleCallback = None
        assert self._sheet, 'Could not find sheet in workbook'

    def HandleCreate(self):
        self.InitSheetContents()
        self.UxSheet().AddDependent(self.SheetObserver())

    def IsSheetActive(self):
        if self.Settings().Caption() == self.WorkbookPanel().Application().ActiveSheet().Name():
                return True
        return False

    def InitOnIdleCallback(self):
        if self._onIdleCallback is None:
            self._onIdleCallback = acm.Time.Timer().CreatePeriodicTimerEvent(
                    self.ON_IDLE_FREQ, self.OnHandleOnIdle, None)

    def RemoveOnIdleCallback(self):
        if self._onIdleCallback is not None:
            acm.Time.Timer().RemoveTimerEvent(self._onIdleCallback)
            self._onIdleCallback = None

    def HandleDestroy(self):
        # Underlying sheet has been destroyed already, so don't remove subscription
        self.RemoveOnIdleCallback()
        self.WorkbenchObserver().StopObserving()
        self._workbookPanel = None

    @fn_timer
    def InitSheetContents(self):
        settings = self.Settings()
        if settings.Grouper():
            grouper = FGrouperUtils.GetGrouper(settings.Grouper(), settings.SheetType())
            self.Sheet().LastGrouper(grouper)
        if not self.Workbook().StoredWorkbook(): #Add content if no workbook present
            return InsertItemHandlerMixin.InitSheetContents(self)
        return None

    def Sheet(self):
        return self._sheet

    def UxSheet(self):
        # Unwrap sheet utils sheet
        return self.Sheet().Sheet()

    def Settings(self):
        return self._settings

    def WorkbookPanel(self):
        return self._workbookPanel

    def Workbook(self):
        return self.WorkbookPanel().Application().ActiveWorkbook()

    def ActivateSheet(self):
        self.Workbook().ActivateSheet(self.UxSheet())

    def IsValid(self):
        return bool(self._SheetFromWorkbook())

    def SelectionDoubleClick(self, selection):
        pass

    def SelectionChanged(self, selection):
        pass

    def RowSelectionChanged(self, selection):
        pass

    def ColumnSelectionChanged(self, selection):
        pass

    def SetWorkbenchObserver(self, dispatcher=None):
        self._workbenchObserver = WorkbenchObserver(dispatcher, self)

    def WorkbenchObserver(self):
        return self._workbenchObserver

    def SheetObserver(self):
        if self._sheetObserver is None:
            self._sheetObserver = SheetObserver(self)
        return self._sheetObserver

    def SendEvent(self, event):
        return self.WorkbenchObserver().SendEvent(event)

    def ReactOnEvent(self):
        return self.IsValid()

    def AddToEventQueue(self, event):
        # Only occurs if the user has closed the last sheet in the workbook
        # (there is no selection change callback to detect this). Discard
        # the event.
        pass

    def _SheetNameFromTemplate(self):
        # Accessing trading sheet contents can be slow, so this result is stored
        templateName = self.Settings().SheetTemplate()
        if templateName:
            template = acm.FTradingSheetTemplate.Select01(
                "name = '{}'".format(templateName), None)
            if template:
                return template.TradingSheet().Contents().At("sname")

    def _SheetFromWorkbook(self):
        caption = self.Settings().Caption()
        for sheet in self.Workbook().Sheets():
            if self._sheetName:
                if sheet.Name() == self._sheetName:
                    return FSheetUtils.Sheet(sheet)
            elif caption == sheet.Name():
                return FSheetUtils.Sheet(sheet)

    def __eq__(self, other):
        # Compare underlying UxSheets, but only when valid
        if not self.IsValid():
            return False
        otherUxSheet = other
        if isinstance(other, WorkbenchSheet):
            if not other.IsValid():
                return False
            otherUxSheet = other.UxSheet()
        elif isinstance(other, FSheetUtils.Sheet):
            otherUxSheet = other.Sheet()
        return self.UxSheet() == otherUxSheet

    def __neq__(self, other):
        return not self == other

    @classmethod
    def Create(cls, *args):
        return cls(*args)


class ExtendedWorkbookPanel(DefaultWorkbookPanel):
    """Extends the Integrated Workbench workbook panel with the ability to define
    functionality in classes for its contained sheets (see WorkbenchSheet).
    """

    def __init__(self, application):
        super(ExtendedWorkbookPanel, self).__init__(application)
        self._workbenchSheets = {}
        self._RegisterWorkbenchSheets()


    def WorkbenchSheet(self, name):
        workbenchSheet = self._workbenchSheets.get(name, None)
        # Verify that the sheet still exists in the workbook before returning it.
        if workbenchSheet and workbenchSheet.IsValid():
            return workbenchSheet

    def ActiveWorkbenchSheet(self):
        for workbookSheet in self._workbenchSheets.values():
            if workbookSheet == self.Sheet():
                return workbookSheet

    def SheetChanged(self, sheet):
        # A workbench sheet may have been closed by the user here
        for name, workbenchSheet in self._workbenchSheets.items():
            if not workbenchSheet.IsValid():
                workbenchSheet.HandleDestroy()
                del self._workbenchSheets[name]

    def SheetDoubleClick(self, uxSheet):
        workbookSheet = self.ActiveWorkbenchSheet()
        if workbookSheet and workbookSheet == uxSheet:
            workbookSheet.SelectionDoubleClick(uxSheet.Selection())

    def SetWorkbenchObserver(self, dispatcher):
        super(ExtendedWorkbookPanel, self).SetWorkbenchObserver(dispatcher)
        for workbenchSheet in self._workbenchSheets.values():
            workbenchSheet.SetWorkbenchObserver(dispatcher)

    @fn_timer
    def _RegisterWorkbenchSheets(self):
        for settings in self.Settings().Sheets():
            try:
                WorkbenchSheetCreator = Creator(settings).CreateFunction() or WorkbenchSheet
                sheet = WorkbenchSheetCreator(self, settings)
                self._workbenchSheets[settings.Name()] = sheet
                sheet.HandleCreate()
            except StandardError:
                print('Could not register default workbench sheet {0}:"{1}"'.format(settings.Name(), traceback.format_exc()))

    def HandleDestroy(self):
        super(ExtendedWorkbookPanel, self).HandleDestroy()
        for name, workbenchSheet in self._workbenchSheets.items():
            workbenchSheet.HandleDestroy()
            del self._workbenchSheets[name]


# ----------------------------------------------------------------------------------------------
#  UI event handlers

def OnSheetGridDoubleClickCell(eii):
    try:
        extensionObj = eii.ExtensionObject()
        if extensionObj and extensionObj.IsKindOf(acm.FUiTrdMgrFrame):
            view = FIntegratedWorkbench.GetView(extensionObj)
            sheet = eii.Parameter('sheet')
            if view and sheet:
                for panel in view.Panels().values():
                    if isinstance(panel, ExtendedWorkbookPanel):
                        panel.SheetDoubleClick(sheet)
                        return
    except StandardError as e:
        print('Double click exception:', e)

# ----------------------------------------------------------------------------------------------
#  Calculation based UX controls

class UxCalculatedValue(object):

    CALC_SPACES = acm.Calculations().CreateCalculationSpaceCollection()

    def __init__(self, control, columnId, sheetClass):
        self._control = control
        self._columnId = columnId
        self._calcSpace = self.CALC_SPACES.GetSpace(sheetClass, None)
        self._object = None
        self._calculation = None
        self._needToUpdateControl = False
        self.InitialiseControl()

    def InitialiseControl(self):
        self._control.Editable(False)
        self._control.Label(self.GetColumnLabel(self._columnId))

    def GetCalculatedValue(self):
        return self._calculation.Value() if self._calculation else None

    def SetColumnId(self, columnId):
        if columnId != self._columnId:
            self._columnId = columnId
            self.CreateCalculation()

    def SetObject(self, calculationObject):
        if calculationObject != self._object:
            self._object = calculationObject
            self.CreateCalculation()

    def ServerUpdate(self, sender, symbol, parameter):
        self._needToUpdateControl = True
        
    def HandleOnIdle(self):
        if self._needToUpdateControl:
            self.UpdateControl()

    def CreateCalculation(self):
        try:
            self.DestroyCalculation()
            if self._object and self._columnId:
                cs = self._calcSpace
                self._calculation = cs.CreateCalculation(
                    self._object, self._columnId)
                self._calculation.AddDependent(self)
                cs.Refresh()
            self.UpdateControl()
        except StandardError as e:
            self._control.SetData('Error: {}'.format(e))

    def DestroyCalculation(self):
        if self._calculation:
            self._calculation.RemoveDependent(self)
        self._calculation = None

    def UpdateControl(self):
        self._control.SetData(self.GetCalculatedValue())
        self._needToUpdateControl = False

    @staticmethod
    def GetColumnLabel(columnId):
        extension = acm.GetDefaultContext().GetExtension(
            'FColumnDefinition', 'FTradingSheet', columnId)
        cd = extension.Value() if extension else None
        return cd.GetString('Name') if cd and cd.HasValue('Name') else columnId


class UxCalculatedField(UxCalculatedValue):

    def __init__(self, control, columnId, sheetClass):
        super(UxCalculatedField, self).__init__(control, columnId, sheetClass)
        self._formatter = self.GetFormatter(columnId)

    @staticmethod
    def GetFormatter(columnId):
        extension = acm.GetDefaultContext().GetExtension(
            'FColumnDefinition', 'FTradingSheet', columnId)
        cd = extension.Value() if extension else None
        if cd and cd.HasValue('Format'):
            return acm.Get('formats/{}'.format(cd.GetString('Format')))

    def GetCalculatedValue(self):
        value = super(UxCalculatedField, self).GetCalculatedValue()
        return self._formatter.Format(value) if self._formatter else value


class UxCalculatedPieChart(UxCalculatedValue):

    MAX_SECTOR_NAME_LEN = 24
    COLORS = {
        # De-emphasize 'other' bucket
        'Other': acm.UX.Colors().Create(204, 204, 204)
    }

    def InitialiseControl(self):
        c = self._control
        c.SetPieChartType('Pie')
        c.SetLabelStyle('SpiderNoOverlap')
        c.ShowLabels(True)
        c.ShowLabelsInPieChart(True)
        c.ShowValuesAsPercent()
        c.ShowLegend(True)
        c.ShowValuesInLegend(False)
        c.SetLegendPosition('MiddleRight')
        c.Enable3DView(False)
        c.Redraw()

    def UpdateControl(self):
        def SectorName(text, max_len):
            if len(text) > max_len:
                left_len = max_len / 2 - 3
                right_len = max_len - left_len - 3
                text = '{}...{}'.format(text[:left_len], text[-right_len:])
            return text
        def ColorForString(text):
            v = int(hashlib.md5(text).hexdigest()[:8], 16)
            r, g, b = (v >> 16) & 255, (v >> 8) & 255, v & 255
            return self.COLORS.get(text, acm.UX.Colors().Create(r, g, b))
        def ValueHandler(args, values, *rest):
            index = args.At('sectorIndex')
            return values[index]
        self._control.Clear()
        valuesDict = self.GetCalculatedValue()
        if valuesDict:
            d = OrderedDict([(k,valuesDict.At(k)) for k in valuesDict.Keys()])
            sortedDict = OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))
            for sector in (str(k) for k in sortedDict.keys()):
                name = SectorName(sector, self.MAX_SECTOR_NAME_LEN)
                color = ColorForString(sector)
                self._control.AddSector(name, color)
            self._control.ValuesEventHandler().Add(ValueHandler, sortedDict.values())
        self._control.Redraw()

    def GetCalculatedValue(self):
        value = super(UxCalculatedPieChart, self).GetCalculatedValue()
        if value is not None:
            assert hasattr(value, 'IsKindOf') and value.IsKindOf(acm.FDictionary), (
                'Chart calculation must return an FDictionary '
                '(column: {})'.format(self._columnId))
            return value

# ----------------------------------------------------------------------------------------------
#  Calculation based UX panes

class CalculatedPaneBase(object):

    def __init__(self, columnIds, sheetType):
        self._columnIds = columnIds
        self._sheetType = sheetType
        self._paneId = hex(id(self))

    def ColumnIds(self):
        return self._columnIds

    def SheetType(self):
        return self._sheetType

    def _ControlName(self, name, index=-1):
        name = '{}_{}'.format(name, self._paneId)
        if index >= 0:
            name = '{}_{}'.format(name, index)
        return name

    @staticmethod
    def _ColumnIdsFromExtensionValue(name):
        ext = acm.GetDefaultContext().GetExtension('FExtensionValue', 'FObject', name)
        extensionValue = ext.Value() if ext else None
        return extensionValue.split('.') if extensionValue else []


class CalculatedFieldsPane(CalculatedPaneBase):

    def __init__(self, columnIds, sheetType, fieldColumnCount=1):
        super(CalculatedFieldsPane, self).__init__(columnIds, sheetType)
        self._fields = []
        self._fieldColumnCount = fieldColumnCount
        assert self._fieldColumnCount > 0

    @classmethod
    def FromSettings(cls, settings):
        columnIds = cls._ColumnIdsFromExtensionValue(settings.Columns())
        return cls(columnIds, settings.SheetType(), settings.FieldColumns())

    def CreateLayout(self, builder):
        columnsIter = enumerate(self.ColumnIds())
        for fieldCount in self._FieldsInColumns(builder):
            for _ in range(fieldCount):
                index, columnId = next(columnsIter)
                label = UxCalculatedValue.GetColumnLabel(columnId)
                builder.AddInput(self._ControlName('field', index), label)
        return builder

    def InitControls(self, layout):
        for index, columnId in enumerate(self.ColumnIds()):
            ctrl = layout.GetControl(self._ControlName('field', index))
            field = UxCalculatedField(ctrl, columnId, self.SheetType())
            self._fields.append(field)
    
    def HandleOnIdle(self):
        for field in self._fields:
            field.HandleOnIdle()

    def SetObject(self, calculationObject):
        for field in self._fields:
            field.SetObject(calculationObject)

    def _FieldsInColumns(self, builder):
        fieldCount = len(self.ColumnIds())
        columnCount = min(self._fieldColumnCount, fieldCount)
        if columnCount:
            perColumnCount = fieldCount / columnCount
            overflowCount = fieldCount % columnCount
            builder.BeginHorzBox()
            for i in range(columnCount):
                if i != 0:
                    builder.AddSpace(5)
                builder.BeginVertBox()
                yield (perColumnCount + int(overflowCount > 0))
                builder.EndBox()
                overflowCount -= 1
            builder.EndBox()


class CalculatedPieChartsPane(CalculatedPaneBase):


    def __init__(self, columnIds, sheetType, width=-1, height=-1, maxWidth=-1, maxHeight=-1):
        super(CalculatedPieChartsPane, self).__init__(columnIds, sheetType)
        self._width = width
        self._height = height
        self._maxWidth = maxWidth
        self._maxHeight = maxHeight
        self._chartCtrl = None
        self._selectionCtrl = None

    @classmethod
    def FromSettings(cls, settings):
        columnIds = cls._ColumnIdsFromExtensionValue(settings.Columns())
        return cls(columnIds, settings.SheetType(),
            settings.Width(), settings.Height(),
            settings.MaxWidth(), settings.MaxHeight())

    def CreateLayout(self, builder):
        if self.ColumnIds():
            builder.BeginVertBox()
            builder.AddPieChart(self._ControlName('chart'),
                self._width, self._height, self._maxWidth, self._maxHeight)
            builder.AddOption(self._ControlName('chart_opts'), '',
                self._width, self._maxWidth)
            builder.EndBox()
        return builder

    def InitControls(self, layout):
        if layout.HasControl(self._ControlName('chart')):
            self._selectionCtrl = layout.GetControl(self._ControlName('chart_opts'))
            labelToColumnIdMap = OrderedDict([
                (UxCalculatedValue.GetColumnLabel(colId), colId) for colId in self.ColumnIds()])
            for label in labelToColumnIdMap.keys():
                self._selectionCtrl.AddItem(label)
            self._selectionCtrl.AddCallback(
                'Changed', self.OnChartSelectionChanged, labelToColumnIdMap)
            if labelToColumnIdMap:
                firstLabel = labelToColumnIdMap.keys()[0]
                self._selectionCtrl.SetData(firstLabel)

            chart = layout.GetControl(self._ControlName('chart'))
            firstColumnId = self.ColumnIds()[0]
            self._chartCtrl = UxCalculatedPieChart(chart, firstColumnId, self.SheetType())
    
    def HandleOnIdle(self):
        self._chartCtrl.HandleOnIdle()

    def SetObject(self, calculationObject):
        self._chartCtrl.SetObject(calculationObject)

    def OnChartSelectionChanged(self, labelToColumnIdMap, *rest):
        selectedLabel = self._selectionCtrl.GetData()
        columnId = labelToColumnIdMap.At(selectedLabel)
        if columnId:
            self._chartCtrl.SetColumnId(columnId)
