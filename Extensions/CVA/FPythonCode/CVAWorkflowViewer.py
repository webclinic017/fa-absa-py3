import acm
import FUxCore

STATE_CHART_CVA            = 'CVA Workflow'
STATE_PENDING_CVA          = 'Pending CVA'
COLUMN_ID_LIST             = ['Trade Instrument', 'Trade Counterparty', 'Trade Acquirer', 'Trade Trader', 'Trade Portfolio', 'Trade Status']

def CVAWorkflowState(trade):
    stateChart = acm.FStateChart[STATE_CHART_CVA]
    bps = acm.BusinessProcess().FindBySubjectAndStateChart(trade, stateChart)
    for bp in bps:
        if not bp.IsInEndState():
            return bp.CurrentStep().State().Name()
    if bps.Size():
        return "CVA Confirmed"
    return "N/A"


def OnBusinessProcessDetailClicked( self, cd ):    
    trade = self.GetTradeFromSelection()
    if trade:
        stateChart = acm.FStateChart[STATE_CHART_CVA]
        bps = acm.BusinessProcess().FindBySubjectAndStateChart(trade, stateChart)
        lastBp = bps[-1]
        acm.StartApplication('Business Process Details', lastBp )

class CVAWorkflowViewer (FUxCore.LayoutPanel):
    def __init__(self):
        self.m_stateChart = acm.FStateChart[STATE_CHART_CVA]
        
    def CreateQueryResultToFindBySubjectAndStateChart(self):
        enumeration = acm.FEnumeration['enum(B92RecordType)']    
        tradeRecType = enumeration.Enumeration('trade')
        query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
        query.AddAttrNode('subject_type', 'EQUAL', tradeRecType)
        query.AddAttrNode('StateChart.Oid', 'EQUAL', self.m_stateChart.StorageId())
        return query.Select_Triggered()
    
    def UpdateAdHocPortfolio(self):
        updatedResultSet = acm.FSet()
        currentResultSet = acm.FSet()
        shouldBeRemoved = acm.FSet()
        
        for bp in self.m_queryResult.Result():
            updatedResultSet.Add(bp.Subject())
        currentResultSet.AddAll(self.m_tradesInPendingCVA)
        
        shouldBeRemoved.AddAll(currentResultSet)
        shouldBeRemoved.RemoveAll(updatedResultSet)
        updatedResultSet.RemoveAll(currentResultSet)
        
        self.m_tradesInPendingCVA.AddAll(updatedResultSet)
        self.m_tradesInPendingCVA.RemoveAll(shouldBeRemoved)
    
    def RemoveColumns(self):
        columnCreators = self.m_tradeSheet.ColumnCreators()
        while columnCreators.Size() > 0:
            creator = columnCreators.At(0)
            columnCreators.Remove(creator)
        
    def InsertColumns(self):
        creators = acm.GetColumnCreators(COLUMN_ID_LIST, acm.GetDefaultContext())
        i = 0
        while i < creators.Size():
            creator = creators.At(i)
            self.m_tradeSheet.ColumnCreators().Add(creator)
            i = i + 1
            
    def UpdateColums(self):
        self.RemoveColumns()
        self.InsertColumns()
        
    def GetSelectedSheetCell(self):
        if self.m_tradeSheet:
            selection = self.m_tradeSheet.Selection()
            if selection:
                return selection.SelectedCell()
                
    def GetRowObject(self):
        row = None 
        cell = self.GetSelectedSheetCell()
        if cell:
            row = cell.RowObject()
        return row       
        
    def GetTradeFromSelection(self):
        rowObject = self.GetRowObject()
        if rowObject and rowObject.Class() == acm.FTradeRow:
            return rowObject.OriginalTrade()
        return None
        
    def InsertAdHocPortfolioInTradeSheet(self):
        adHocPortfolio = acm.FAdhocPortfolio(self.m_tradesInPendingCVA)
        adHocPortfolio.Name("CVA Trades")
        treeProxy = self.m_tradeSheet.GridBuilder().InsertItem(adHocPortfolio)
        treeProxy.Expand(True)
        treeProxy.ApplyGrouper(acm.FAttributeGrouper("Trade.CVAWorkflowState"))
        self.UpdateAdHocPortfolio()
        
    def UpdateControls(self):
        trade = self.GetTradeFromSelection()
        enableDetails = trade != None
        self.m_businessProcessDetailBtn.Enabled(enableDetails)
            
                    
    def ServerUpdate(self, sender, aspect, parameter ):
        if str(aspect) in ('resultChanged', 'SelectionChanged'):
            if self.m_queryResult: 
                self.m_queryResult.ApplyChanges()
                self.UpdateAdHocPortfolio()
            self.UpdateControls()
            
    def HandleCreate(self):
        layout = self.SetLayout( self.CreateLayout() )
        self.m_tradeSheet = layout.GetControl('sheet').GetCustomControl()
        self.m_tradeSheet.ShowGroupLabels(False)
        self.m_tradeSheet.AddDependent(self)
        self.UpdateColums()
        
        self.m_businessProcessDetailBtn = layout.GetControl('businessProcessDetailBtn')
        self.m_businessProcessDetailBtn.AddCallback( "Activate", OnBusinessProcessDetailClicked, self )
        self.m_businessProcessDetailBtn.Enabled(False)

        self.m_queryResult = self.CreateQueryResultToFindBySubjectAndStateChart()
        self.m_tradesInPendingCVA = acm.FDependentArray()
        
        self.Owner().AddDependent(self)
        self.m_queryResult.AddDependent(self)
        self.m_tradesInPendingCVA.AddDependent(self)
        
        self.InsertAdHocPortfolioInTradeSheet()
        
    def HandleDestroy(self):
        self.Owner().RemoveDependent(self)
        self.m_queryResult.RemoveDependent(self)
        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.    AddCustom('sheet', 'sheet.FTradeSheet', 125, 125)
        b.  BeginHorzBox()
        b.    AddFill()
        b.    AddButton('businessProcessDetailBtn', 'Show Details...')   
        b.  EndBox()
        b.EndBox()
        return b
        
def OnCreate(eii):
    basicApp = eii.ExtensionObject()
    myPanel = CVAWorkflowViewer()
    basicApp.CreateCustomDockWindow(myPanel, 'CVAWorkflowViewer', 'CVA Workflow Viewer', 'Bottom', None, True, False);

