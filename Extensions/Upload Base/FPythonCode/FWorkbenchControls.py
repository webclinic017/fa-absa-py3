""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../AM_common/FWorkbenchControls.py"
"""--------------------------------------------------------------------------
MODULE
    FWorkbenchControls

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm
from FPositionCreator import FPositionSpecification
from FReconciliationValueMapping import FPositionCalculation
import FOperationsManagerWorkbench
from FAssetManagementUtils import logger


class WorkbenchBusinessProcessControl(FOperationsManagerWorkbench.WorkbenchControl):
    """A control for supporting business process workflow."""

    MAX_EVENTS_COUNT = 20
    PADDING = '_' * 30
    
    @staticmethod
    def GREY():
        return acm.GetDefaultContext().GetExtension(
            'FColor', 'FObject', 'BkgEvalClone').Value()

    def __init__(self, panel):
        super(WorkbenchBusinessProcessControl, self).__init__(panel)
        self._currentStateCtrl = None
        self._commentReaderCtrl = None
        self._commentWriterCtrl = None
        self._executeButton = None
        self._inspectProcessButton = None
        self._saveCommentButton = None        
        self._eventCheckboxCtrls = []

    def CreateLayout(self, builder):
        # Current state
        builder.BeginHorzBox('EtchedIn', '')
        builder.  AddLabel('currentState', self.PADDING)
        builder.EndBox()

        # Available events checkboxes
        builder.BeginVertBox('EtchedIn', 'Available Events')
        builder.  BeginVertBox('None')
        for i in range(self.MAX_EVENTS_COUNT):
            builder.AddCheckbox('event_%i' % i, self.PADDING)
        builder.  EndBox()

        # Comments diary and execution buttons
        builder.  BeginVertBox('EtchedIn', 'Comments')
        builder.    AddText('diaryReader', 280, 80)
        builder.    AddText('diaryWriter', 280, 60)        
        builder.  EndBox()
        builder.  BeginHorzBox('None')
        builder.    AddFill()
        builder.    AddButton('inspect', 'View History', True, False)
        builder.    AddButton('saveComment', 'Save Comment', False, False)
        builder.    AddButton('execute', 'Execute Event', False, False)
        builder.  EndBox()
        builder.EndBox()

    def HandleCreate(self, layout):
        self._currentStateCtrl = self.RegisterFUxControl(layout.GetControl('currentState'))
        self._InitCommentControls(layout)        
        self._executeButton = self.RegisterFUxControl(layout.GetControl('execute'))
        self._inspectProcessButton = self.RegisterFUxControl(layout.GetControl('inspect'))
        self._eventCheckboxCtrls = [self.RegisterFUxControl(layout.GetControl('event_%i' % i)) \
                for i in range(self.MAX_EVENTS_COUNT)]

        self._executeButton.AddCallback('Activate', self.OnExecuteEventClicked, None)
        self._inspectProcessButton.AddCallback('Activate', self.OnInspectProcessClicked, None)
        for i, checkbox in enumerate(self._eventCheckboxCtrls):
            checkbox.AddCallback('Activate', self.OnEventClicked, i)
            
    def _InitCommentControls(self, layout):
        self._commentReaderCtrl = self.RegisterFUxControl(layout.GetControl('diaryReader'))
        self._commentReaderCtrl.Editable(False)
        self._commentReaderCtrl.SetColor('BackgroundReadonly', self.GREY())
        self._commentWriterCtrl = self.RegisterFUxControl(layout.GetControl('diaryWriter'))
        self._saveCommentButton = self.RegisterFUxControl(layout.GetControl('saveComment'))
        self._saveCommentButton.Enabled(False)
        self._commentWriterCtrl.AddCallback('Changed', self.OnCommentWriterChanged, None)
        self._saveCommentButton.AddCallback('Activate', self.OnSaveCommentClicked, None)
        
    def _UpdateCommentControls(self):       
        self._SetCommentReaderCtrl()
        self._commentWriterCtrl.SetData('')

    def OnSelectedItemChanged(self):
        self._SetCurrentStateCtrl()
        self._SetCommentReaderCtrl()
        self._SetEventCheckboxCtrls()
        self._executeButton.Enabled(False)

    def OnEventClicked(self, params, _cd):
        # pylint: disable-msg=W0106
        self._executeButton.Enabled(True)
        for i, checkbox in enumerate(self._eventCheckboxCtrls):
            if i != params:
                checkbox.Checked(False)
            else:
                checkbox.Checked(True) if checkbox.Checked() else checkbox.Checked(False)

    def OnExecuteEventClicked(self, _params, _cd):
        checkbox = self._GetSelectedEventCtrl()
        assert(checkbox and checkbox.Checked())
        bp = self.Panel().BusinessProcess()
        bp.HandleEvent(checkbox.Label())
        bp.Commit()

    def OnInspectProcessClicked(self, _params, _cd):
        acm.StartApplication('Business Process Details', self.Panel().BusinessProcess())
    
    @staticmethod
    def IsSingleNote(notes):
        return notes.IsKindOf(acm.FString)

    def AddNoteToDiary(self, note):
        entry = acm.FBusinessProcessDiaryEntry()
        notes = self._DiaryEntry().Notes()
        newNotes = acm.FArray()
        if self.IsSingleNote(notes):
            notes = [notes]
        newNotes.AddAll(notes)
        newNotes.Add(note)
        entry.Notes(newNotes)
        bp = self.Panel().BusinessProcess()
        bp.Diary().PutEntry(bp, bp.CurrentStep(), entry)
        try:
            bp.Diary().Commit()
            self._UpdateCommentControls()
        except Exception as e:
            logger.error('Save comment failed. Reason: {0}'.format(e))
    
    def OnSaveCommentClicked(self, _params, _cd):
        note = self._commentWriterCtrl.GetData()
        self.AddNoteToDiary(note)
        
    def OnCommentWriterChanged(self, _params, _cd):
        if bool(self._commentWriterCtrl.GetData()):
            self._saveCommentButton.Enabled(True)
        else:
            self._saveCommentButton.Enabled(False)

    def _SetCurrentStateCtrl(self):
        currentState = self.Panel().BusinessProcess().CurrentStep().State().Name().upper()
        self._currentStateCtrl.Label(currentState)
        
    def _DiaryEntry(self):
        bp = self.Panel().BusinessProcess()
        return bp.Diary().GetEntry(bp, bp.CurrentStep())

    def _SetCommentReaderCtrl(self):
        self._commentReaderCtrl.SetData('')
        bp = self.Panel().BusinessProcess()
        allNotes = []
        diary = bp.Diary()
        for s in bp.Steps():
            notes = diary.GetEntry(bp, s).Notes()
            extendedNotes = []
            for n in notes:
                extendedNotes.append(s.EventName()+': '+n)
            allNotes.extend(extendedNotes)
        notes = '\n'.join(allNotes)
        self._commentReaderCtrl.AppendText(notes)

    def _SetEventCheckboxCtrls(self):
        events = self._GetEventNames()
        for i, checkbox in enumerate(self._eventCheckboxCtrls):
            try:
                checkbox.Label(events[i])
                checkbox.Visible(True)
            except IndexError:
                checkbox.Visible(False)
            checkbox.Checked(False)

    def _GetEventNames(self):
        return [str(e).strip("'") for e in self.Panel().BusinessProcess().CurrentStep().ValidEvents()]

    def _GetSelectedEventCtrl(self):
        for checkbox in self._eventCheckboxCtrls:
            if checkbox.Checked():
                return checkbox


class WorkbenchPositionControl(FOperationsManagerWorkbench.WorkbenchControl):
    """A control for displaying the attributes of a position."""
    
    ICON_ATTRIBUTE = 'BlueBall'

    def __init__(self, panel):
        super(WorkbenchPositionControl, self).__init__(panel)
        self._attributesListCtrl = None
        self._viewPositionButton = None
        self._viewTradesButton = None

    def CreateLayout(self, builder):
        builder.BeginHorzBox('EtchedIn', 'Position')
        builder.  BeginVertBox('None')
        builder.    BeginHorzBox('None')
        builder.      AddList('attributesList', 7, -1, -1)
        builder.    EndBox()
        builder.    BeginHorzBox('None')
        builder.      AddFill()
        builder.      AddButton('viewPosition', 'View Position', False, False)
        builder.      AddButton('viewTrades', 'View Trades', True, False)
        builder.    EndBox()
        builder.  EndBox()
        builder.EndBox()

    def HandleCreate(self, layout):
        self._attributesListCtrl = self.RegisterFUxControl(layout.GetControl('attributesList'))
        self._viewPositionButton = self.RegisterFUxControl(layout.GetControl('viewPosition'))
        self._viewTradesButton = self.RegisterFUxControl(layout.GetControl('viewTrades'))

        self._viewPositionButton.AddCallback('Activate', self.OnViewPositionClicked, None)
        self._viewTradesButton.AddCallback('Activate', self.OnViewTradesClicked, None)
        
        attrsListCtrl = self._attributesListCtrl
        attrsListCtrl.ShowGridLines()
        attrsListCtrl.ShowColumnHeaders()
        attrsListCtrl.AddColumn('Name', -1, "Name of the attribute")
        attrsListCtrl.AddColumn('Value', -1, "Value of the attribute")

    @staticmethod
    def GetDisplayableQueryNodes(query):
        # Helper function to retrieve an ASQL query attribute value pairs as a dictionary
        def GetNodes(node, nodes=[]):
            # pylint: disable-msg=W0102
            if hasattr(node, 'AsqlNodes') and node.AsqlNodes():
                for n in node.AsqlNodes():
                    GetNodes(n, nodes)
            if node.IsKindOf(acm.FASQLNode):
                nodes.append(node)
            return nodes
            
        queryNodes = (n for n in GetNodes(query) if n.IsKindOf(acm.FASQLAttrNode))
        attributeValuePairs = ((str(node.AsqlAttribute().AttributeString()), str(node.AsqlValue())) \
                                for node in queryNodes)
        nodeDict = dict()
        for attr, attrValue in attributeValuePairs:
            if not attr in nodeDict:
                nodeDict[attr] = acm.FList()
                nodeDict[attr].Add(attrValue)
            else:
                nodeDict[attr].Add(attrValue)
        for attr in nodeDict:
            nodeDict[attr] = str(nodeDict[attr] if nodeDict[attr].Size() > 1 else nodeDict[attr].First())
        return nodeDict

    def OnSelectedItemChanged(self):
        self._SetAttributesListCtrl()

    def OnViewPositionClicked(self, _params, _cd):
        position = self._GetPosition()        
        acm.StartFASQLEditor(None, None, None, position.Query(), None, '', True)

    def OnViewTradesClicked(self, _params, _cd):
        tradingMgr = acm.StartApplication('Trading Manager', None)
        sheet = tradingMgr.ActiveWorkbook().NewSheet('TradeSheet')
        sheet.InsertObject(self._GetPosition(), 0)
        sheet.RowTreeIterator(True).Tree().Expand(True, 10000)

    def _SetAttributesListCtrl(self):
        self._attributesListCtrl.Clear()
        root = self._attributesListCtrl.GetRootItem()
        for attribute, value in sorted(self._GetPositionAttributes().items()):
            child = root.AddChild()
            child.Label(attribute)
            child.Icon(self.ICON_ATTRIBUTE)
            child.Label(value, 1)
        self._attributesListCtrl.AdjustColumnWidthToFitItems(0)
        self._attributesListCtrl.AdjustColumnWidthToFitItems(1)

    def _GetPosition(self):
        ''' This method is backwards compatible '''
        reconItem = self.Panel().ReconciliationItem()
        storedWildcardedQuery = self.Panel().StoredWildcardedQuery()
        positionStoredQuery = storedWildcardedQuery.Clone()
        query = positionStoredQuery.Query()
        externalValues = reconItem.ExternalValues()
        query = FPositionSpecification.PositionQueryFromWildcardedQuery(query, externalValues)
        positionStoredQuery.Query(query)
        return positionStoredQuery        

    def _GetPositionAttributes(self):
        positionStoredQuery = self._GetPosition()
        return self.GetDisplayableQueryNodes(positionStoredQuery.Query())


class WorkbenchStatisticsListControl(FOperationsManagerWorkbench.WorkbenchControl):
    """A control for displaying statistics on the completion progress of business processes."""
    
    ICON_OTHER_STATE = 'FMethod'
    COLORS = {
        'LightRed': (255, 51, 51),
        'LightGreen': (134, 249, 134),
        'LightYellow': (240, 255, 77),
        'LightOrange': (255, 196, 102), 
        'LightGrey': (204, 204, 204),
        'Blue': (134, 214, 249),
        'LightBlue': (153, 255, 255)
        }
        
    STATE_COLORS = {
            'Discrepancy': 'LightRed',
            'Unidentified': 'LightOrange',
            'Missing in document': 'LightBlue',
            'Closed': 'LightGreen',
            'Comparison': 'LightYellow',
            'Successful': 'LightGreen',
            'Invalid data': 'Blue',
            'Ready': 'LightGrey',
            'Pending upload': 'LightBlue'
            }

    def __init__(self, panel):
        super(WorkbenchStatisticsListControl, self).__init__(panel)
        self._statisticsCtrl = None
        self._dependentBusinessProcesses = []

    def CreateLayout(self, builder):
        builder.BeginHorzBox('EtchedIn', 'Statistics')
        builder.  AddPieChart('statisticsChart', 350, 280)
        builder.EndBox()
        builder.AddFill()

    def HandleCreate(self, layout):
        self._statisticsCtrl = self.RegisterFUxControl(layout.GetControl('statisticsChart'))
        
    def _SetupStatisticsChart(self):
        self._statisticsCtrl.Clear()
        self._statisticsCtrl.SetPieChartType('SmoothEdgePie')
        self._statisticsCtrl.SetLabelStyle('Rim')
        self._statisticsCtrl.ShowLabels(True)      
        self._statisticsCtrl.ShowValuesAsPercent()      
        self._statisticsCtrl.ShowLegend(True)
        self._statisticsCtrl.ShowValuesInLegend(False)
        self._statisticsCtrl.SetLegendPosition('BottomCenter')
        self._statisticsCtrl.Enable3DView(True)
        self._PopulateStatisticsChart()
        self._statisticsCtrl.Redraw()

    def HandleDestroy(self):
        self._RemoveBusinessProcessesDependencies()

    def ServerUpdate(self, _sender, _aspect, _param):
        # Force a redraw of all statistics if any reconciliation item business process has been updated
        self.OnSelectedItemChanged()

    def OnSelectedItemChanged(self):
        self._SetupStatisticsChart()
        
    @classmethod
    def _GetColor(cls, color):
        rgb = cls.COLORS.get(color, (0, 0, 0))
        return acm.UX.Colors().Create(*rgb)
        
    @classmethod
    def _SectorColor(cls, state):
        color = cls.STATE_COLORS.get(state)
        return cls._GetColor(color)
        
    def _PopulateStatisticsChart(self):
        # pylint: disable-msg=W0612
        for state, count, percent in self._GetStatisticsValues():
            self._statisticsCtrl.AddSector(state, self._SectorColor(state))
        self._statisticsCtrl.ValuesEventHandler().Add(self._SectorValues, None)
            
    def _SectorValues(self, args, param):
        values = dict(
            (index, count)
            for index, (state, count, percent) in enumerate(self._GetStatisticsValues())
            )
        sectorIndex = args.At('sectorIndex')
        return values.get(sectorIndex, 0)

    def _GetStatisticsValues(self):
        # Generator method yielding (stateName, count, percentage) tuples
        stateCounts = sorted(self._GetSheetBusinessProcessCurrentStateCounts().items())
        totalCount = sum([count for state, count in stateCounts])
        remainingPercent = 100.0

        for state, count in stateCounts[:-1]:
            percent = self._GetPercentage(count, totalCount)
            remainingPercent -= percent
            yield (state, count, '%00.02f' % percent)
        try:
            state, count = stateCounts[-1]
            yield (state, count, '%00.02f' % remainingPercent)
        except ValueError:
            pass
        
    def _GetSheetBusinessProcessCurrentStateCounts(self):
        stateCounts = {}
        self._RemoveBusinessProcessesDependencies()
        sheet = self.Panel().ActiveSheet()
        rowIter = sheet.RowTreeIterator(True).FirstChild()
        while rowIter:
            row = rowIter.Tree().Item()
            subjectType = self.Panel().SubjectType()
            if row and row.IsKindOf(acm.FBusinessProcess) and row.Subject(): 
                if subjectType is None or row.Subject().IsKindOf(subjectType):
                    state = row.CurrentStep().State().Name()
                    stateCounts[state] = stateCounts.get(state, 0) + 1
                    self._AddDependentBusinessProcess(row)
            rowIter = rowIter.FirstChild() or rowIter.NextUsingDepthFirst()
        return stateCounts

    def _AddDependentBusinessProcess(self, bp):
        # Control should already be dependent on the current business process
        if bp != self.Panel().BusinessProcess():
            bp.AddDependent(self)
            self._dependentBusinessProcesses.append(bp)

    def _RemoveBusinessProcessesDependencies(self):
        for bp in self._dependentBusinessProcesses:
            bp.RemoveDependent(self)
        self._dependentBusinessProcesses = []

    @staticmethod
    def _GetPercentage(count, total):
        try:
            return round(100.0 * count / total, 2)
        except ZeroDivisionError:
            return 0.0


class WorkbenchTradingSheetControl(FOperationsManagerWorkbench.WorkbenchControl):
    """A control to display a generic trading sheet."""

    def __init__(self, panel, sheetType, height=100):
        super(WorkbenchTradingSheetControl, self).__init__(panel)
        self._sheetType = sheetType
        self._ctrlHeight = height
        self._tradingSheetCtrl = None
        self._tradingSheet = None

    def CreateLayout(self, builder):
        builder.AddCustom(self._GetTradingSheetCtrlId(), 'sheet.' + self._sheetType, None, self._ctrlHeight)

    def HandleCreate(self, layout):
        self._tradingSheetCtrl = self.RegisterFUxControl(layout.GetControl(self._GetTradingSheetCtrlId()))
        self._tradingSheet = self._tradingSheetCtrl.GetCustomControl()

    def OnSelectedItemChanged(self):
        self._SetTradingSheetCtrl()

    def _GetTradingSheetCtrlId(self):
        return self._sheetType + '_sheet_' + str(id(self))
        
    def _SetSheetColumns(self):
        columnNames = acm.FArray().AddAll(self._GetSheetColumnNames())
        if columnNames.IsEmpty():
            return

        columnCreators = self._tradingSheet.ColumnCreators()
        while columnCreators.Size() > 0:
            columnCreators.Remove(columnCreators.At(0))

        requiredColumnCreators = acm.GetColumnCreators(columnNames, acm.GetDefaultContext())
        for i in range(requiredColumnCreators.Size()):
            creator = requiredColumnCreators.At(i)
            columnCreators.Add(creator)

    def _GetSheetColumnNames(self):
        # Sub-class and return additional columns to be set on the sheet
        return []

    def _GetSheetInsertableItem(self):
        # Sub-class and return the item to be inserted in to the sheet 
        return None

    def _SetTradingSheetCtrl(self):
        isFxReconciliation = self.Panel().ReconciliationSpecification().IsFXReconciliation()
        self._tradingSheet.RemoveAllRows()
        item = self._GetSheetInsertableItem()
        if item:
            self._tradingSheet.InsertObject(item, 0)
            self._tradingSheet.GridBuilder().Refresh()
            self._SetSheetColumnsWidth(110)
            row = self._tradingSheet.RowTreeIterator(True)
            if row:
                row = row.FirstChild()
                if isFxReconciliation:
                    grouper = FPositionCalculation.PositionGrouper()
                    row.Tree().ApplyGrouper(grouper)                
            while row:
                if row.Tree():
                    if type(row.Tree().Item()).__name__ in ('FSingleInstrumentAndTrades', 'FTradeRow', ):
                        row.Tree().Expand(False)
                    else:
                        row.Tree().Expand(True, 10000)
                row = row.NextUsingDepthFirst()            

    def _SetSheetColumnsWidth(self, width):
        columnIter = self._tradingSheet.GridColumnIterator().First()
        while columnIter:
            column = columnIter.GridColumn()
            column.Width(width)
            columnIter = columnIter.Next()