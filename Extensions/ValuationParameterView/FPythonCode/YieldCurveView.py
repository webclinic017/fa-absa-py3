import acm
import FUxCore
import FLogger
logger = FLogger.FLogger("YieldCurveView")

lotToArray = acm.GetFunction("arrayAny", 1)

def TurnLotIntoArray(someLot):
    return lotToArray(someLot)

def OnSimulateCurves(self, cd):
    if self.m_curve:
        curveClone = self.m_curve.CloneAndSimulateRecursive()
        acm.SynchronizedMessageSend(curveClone, 'Calculate', [])
        acm.SynchronizedMessageSend(self.m_curve, 'Apply', [curveClone])
        logger.LOG( 'Calc + Sim YC  %s' % self.m_curve.Name() )

def OnUnsimulateCurve(self, cd):
    if self.m_curve:
        acm.SynchronizedMessageSend(self.m_curve, 'Undo', [])
        logger.LOG( 'Unsimulate YC  %s' % self.m_curve.Name())

class YieldCurveView (FUxCore.LayoutPanel):
    def __init__(self, parent):
        self.m_parent = parent
        self.m_shell = parent.Shell()
        self.m_curve = None
        self.m_yieldCurveBox = None
        self.m_valViewerBox = None
        self.m_curveLabel = None
        self.m_calcSim = None
        self.m_unsimulate = None
        self.m_row = None
        self.m_columnLabels = None
        self.m_isBaseCurve = None

    def ServerUpdate(self, sender, aspect, parameter ):
        if str(aspect) == str('SelectionChanged'):
            self.HandleSelectionChanged( sender )

    def HandleCreate( self ):
        layout = self.SetLayout( self.CreateLayout() )
        self.m_sheet = layout.GetControl('sheet').GetCustomControl()
        self.m_sheet.ShowGroupLabels(False)
        self.m_curveLabel = layout.GetControl('yieldCuveLabel')
        self.m_curveLabel.SetData('No curve chosen')
        self.m_curveLabel.Editable(False)
        self.RemoveColumns()
        self.m_valViewer = layout.GetControl('viewer').GetCustomControl()
        self.m_valViewer.Init(180, True, False, 'Yield Curve', False, True)
        self.m_calcSim = layout.GetControl('calculateSimulate')
        self.m_unsimulate = layout.GetControl('unsimulate')
        self.m_calcSim.AddCallback( "Activate", OnSimulateCurves, self )
        self.m_unsimulate.AddCallback( "Activate", OnUnsimulateCurve, self )
        self.m_columnLabels = acm.FDictionary()
        self.m_columnLabels.AtPut(acm.FPriceCurve, ["Yield Curve View Price", "Yield Curve View Expiry", "Yield Curve View Price Theor"])
        self.m_columnLabels.AtPut(acm.FBenchmarkCurve, ["Yield Curve View Price Theor", "Yield Curve View Expiry", "Yield Curve View Rate"])
        self.m_isBaseCurve = acm.FDictionary()
        self.m_isBaseCurve.AtPut(acm.FPriceCurve, True)
        self.m_isBaseCurve.AtPut(acm.FBenchmarkCurve, True)
        updated = self.UpdateValuInfo()
        if updated:
            self.UpdateView(self.GetDiscountCurve())
        self.Owner().AddDependent(self)
        self.m_valViewer.AddDependent(self)
        
    def HandleDestroy( self ):
        self.Owner().RemoveDependent(self)
        self.m_valViewer.RemoveDependent(self)
        self.m_curve = None

    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginHorzBox('Invisible')
        b.    BeginVertBox()
        b.      AddInput('yieldCuveLabel', 'Yield Curve')
        b.      AddCustom('sheet', 'sheet.FDealSheet', 335, 380)
        b.      BeginHorzBox()
        b.        AddSpace(75)
        b.        AddButton('calculateSimulate', '   Calc + Sim   ', True, False)
        b.        AddButton('unsimulate', '   Unsimulate   ', True, False)
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox('Invisible')
        b.    AddCustom('viewer', 'ValuationViewer', 300, -1)
        b.  EndBox()
        b.EndBox()
        return b

    def UpdateView(self, object):
        context = self.GetContext()
        if object:
            baseCurve = self.GetBaseCurveFromHierarchy(object)
            if baseCurve:
                if self.m_curve is None or (baseCurve != self.m_curve):
                    self.RemoveColumns()
                    scenario = self.CreateScenario()
                    self.AddCurveShift(baseCurve, scenario)
                    self.InsertColumn(self.m_columnLabels.At(baseCurve.Class()), context, scenario)
                    self.m_sheet.RemoveAllRows()
                    benchmarks = self.GetBenchmarksFromCurve(baseCurve)
                    self.InsertObjects(benchmarks)
                    self.ModifyColumns()
                    self.m_curveLabel.SetData(baseCurve.Name())
                    self.UpdateButtons(baseCurve)
            else:
                self.m_sheet.RemoveAllRows()
                self.RemoveColumns()
            self.m_curve = baseCurve
        else:
            self.m_sheet.RemoveAllRows()
            self.RemoveColumns()
            self.m_curve = None

    def UpdateValuInfo(self):
        updated = False
        row = self.GetRowObject()
        context = self.GetContext()
        tag = self.GetTag()
        if row:
            if self.m_row is None or (row != self.m_row):
                evaluator = acm.GetCalculatedValueFromString(row, context, 'theoreticalValue', tag)
                self.m_valViewer.Populate(evaluator, context, "parameter view", "yield curve")
                updated = True
        self.m_row = row
        return updated

    def GetDiscountCurve(self):
        curve = None
        row = self.GetRowObject()
        if row:
            context = self.GetContext()
            tag = self.GetTag()
            parameterEvaluator = acm.GetCalculatedValueFromString(row, context, 'snoop(theoreticalValue, "discountYieldCurveHierarchy")', tag)
            if parameterEvaluator:
                object = None
                try:
                    object = parameterEvaluator.Value()
                except:
                    pass
                if object:
                    keepGoing = True
                    while keepGoing:
                        if object.IsLot():
                            object = TurnLotIntoArray(object)
                        if object.IsCollection() and object.Size() > 0:
                            object = object.At(0)
                        else:
                            keepGoing = False
                    if object.IsKindOf(acm.FYieldCurveHierarchy):
                        curve = object
        return curve

    def RemoveColumns( self ):
        columnCreators = self.m_sheet.ColumnCreators()
        while columnCreators.Size() > 0:
            creator = columnCreators.At(0)
            columnCreators.Remove(creator)

    def InsertColumn(self, columnIds, context, scenario):
        creators = acm.GetColumnCreators(columnIds, context)
        i = 0
        while i < creators.Size():
            creator = creators.At(i)
            if scenario:
                creator = creator.ApplyScenario(scenario)
                self.m_sheet.GridBuilder().ScenarioManager().RegisterScenario(scenario)
                self.m_sheet.ColumnCreators().Add(creator)
                i = i + 1

    def ModifyColumns( self ):
        colCreators = self.m_sheet.ColumnCreators()
        i = 0
        while i < colCreators.Size():
            colCreator = colCreators.At(i)
            j = 0
            while j < colCreator.Columns().Size():
                column = colCreator.Columns().At(j)
                if str(column.ColumnName()) ==  "Theoretical Price":
                    column.Label("Theor")
                if str(column.ColumnName()) ==  "Yield Curve View Expiry":
                    column.Label("LastIRDay")
                if str(column.ColumnName()) ==  "Rate":
                    column.Label("Rate")
                if str(column.ColumnName()) ==  "Market Price":
                    column.Label("Price")
                j = j + 1
            i = i + 1

    def InsertObjects(self, objects):
        if objects:
            self.m_sheet.InsertObject(objects, 'IOAP_LAST')

    def GetBenchmarksFromCurve(self, curve):
        if curve:
            return curve.BenchmarkInstruments().SortByProperty("LastIRSensDay")
        return None

    def GetSelectedSheetCell(self):
        sheet = self.m_parent.ActiveSheet()
        if sheet:
            selection = sheet.Selection()
            if selection:
                return selection.SelectedCell()

    def GetContext(self):
        context = None
        cell = self.GetSelectedSheetCell()
        if cell:
            context = cell.Column().Context()
        if not context:
            context = acm.GetDefaultContext()
        return context
        
    def GetRowObject(self):
        row = None 
        cell = self.GetSelectedSheetCell()
        if cell:
            row = cell.RowObject()
        return row
        
    def GetTag(self):
        tag = acm.GetGlobalEBTag()
        cell = self.GetSelectedSheetCell()
        if cell:
            tag = cell.Tag()
        return tag
        
    def SelectedYieldCurveHierarchy(self):
        selected = None
        selection = self.m_valViewer.GetSelected()
        if selection:
            for selected in selection:
                object = selected.Value()
                if object.IsKindOf(acm.FYieldCurveHierarchy):
                    selected = object
        return selected
        
    def GetBaseCurveFromHierarchy(self, yieldCurveHierarchy):
        if not yieldCurveHierarchy:
            return None
        yieldCurveComponent = yieldCurveHierarchy.YieldCurveComponent()
        if self.m_isBaseCurve.At(yieldCurveComponent.Class()):
            return yieldCurveComponent
        else:
            return self.GetBaseCurveFromHierarchy(yieldCurveHierarchy.UnderlyingComponent())

    def CreateScenario(self):
        scenario = acm.FExplicitScenario()
        return scenario
        
    def AddCurveShift(self, curve, scenario):
        if curve and scenario:      
            shiftVector = acm.CreateShiftVector('shiftMappingLinkWithMatchingForwardPeriod', 'yield curve mapped parameter', None)
            shiftVector.AddShiftItem(curve)
            scenario.AddShiftVector(shiftVector)
        
    def HandleSelectionChanged(self, sender):
        if sender.IsKindOf(acm.FUxValuationViewer):
            self.UpdateView(self.SelectedYieldCurveHierarchy())
        else:
            if self.m_sheet and self.m_sheet != sender.ActiveSheet():
                self.m_parent = sender
                updated = self.UpdateValuInfo()
                if updated:
                    self.UpdateView(self.GetDiscountCurve())
                    
    def UpdateButtons(self, curve):
        if curve:
            if curve.RealTimeUpdated():
                self.m_calcSim.Enabled(False)
                self.m_unsimulate.Enabled(False)
            else:
                self.m_calcSim.Enabled(True)
                self.m_unsimulate.Enabled(True)

def OnCreate(eii):
    basicApp = eii.ExtensionObject()
    myPanel = YieldCurveView(basicApp)
    basicApp.CreateCustomDockWindow(myPanel, 'yieldCurveView', 'Yield Curve View', 'Left', None, True, False)
