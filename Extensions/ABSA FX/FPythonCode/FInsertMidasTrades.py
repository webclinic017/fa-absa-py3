import acm
import FUxCore

#SHEET_COLUMN_LABELS = ["Trade Instrument","Trade Price","Trade Quantity","Trade Counterparty", "Trade Date & Time", "Trade Acquire Day"]

SHEET_TEMPLATE = "MidasDealNrLookup"

def CreateQueryFolder(midasDealNo):
        midasDealStr = '%|' + str(midasDealNo) + '|%'
        
        newFilter = acm.FTradeSelection()
        cond = acm.FMatrix()
        cond.AddRow(['', '', 'CP Ref / Your Reference', 'like', midasDealStr, ''])
        cond.AddRow(['And', '(', 'Instrument.Type', 'equal to', 'Curr', ''])
        cond.AddRow(['Or', '', 'Instrument.Type', 'equal to', 'FXOptionDatedFwd', ')'])
        
        newFilter.FilterCondition(cond)
        newFilter.RegisterInStorage()
        return newFilter.Snapshot()
        
def OnTradesClicked(self, cd):
    trades = CreateQueryFolder(self.m_tradeNbrCtrl.GetValue())
    self.m_sheet.RemoveAllRows()
    self.m_sheet.InsertObject(trades, 'IOAP_LAST')
 
'''   
def OnOkClicked(self,cd):
    print self.m_sheet
    trades=self.m_sheet.Selection().SelectedTrades()
    self.m_activeSheet.InsertObject(trades,1)
'''

class midasTradeNoDialog(FUxCore.LayoutDialog):

    def __init__(self, sheet):
        self.m_activeSheet = sheet
        self.m_tradeNbrCtrl = None
        self.m_okBtn = None
        self.m_trdBtn = None  
        self.m_sheet = sheet
        self.m_sheetCtrl = None
    
    def SetSheetColumns(self, sheet):
        #Remove existing default columns
        columnCreators=sheet.ColumnCreators()
        while columnCreators.Size() > 0:
            creator = columnCreators.At(0)
            columnCreators.Remove(creator)
        
        #Insert new columns
        usedContext=acm.GetDefaultContext()
        createContext = acm.FColumnCreatorCreateContext(usedContext)
        template=acm.FTradingSheetTemplate[SHEET_TEMPLATE]
        columns=template.TradingSheet().ColumnCollection(createContext)
        columnList=[]
        for column in columns:
            columnList.append(column.ColumnId())
        creators = acm.GetColumnCreators(columnList, usedContext)
        i = 0
        while i < creators.Size():
            creator = creators.At(i)
            sheet.ColumnCreators().Add(creator)
            i = i+1
            
    def UpdateControls(self):
        pass
        
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Insert Midas TradeNo' )
        self.m_trdBtn = layout.GetControl('trades')
        self.m_okBtn = layout.GetControl("ok")
        self.m_sheetCtrl = layout.GetControl('sheet')
        self.m_sheet = self.m_sheetCtrl.GetCustomControl()
        self.SetSheetColumns(self.m_sheet)
        self.m_trdBtn.AddCallback( "Activate", OnTradesClicked, self )
        #self.m_okBtn.AddCallback( "Activate", OnOkClicked, self )
        self.m_bindings.AddLayout(layout)
        
        self.UpdateControls()
        
    def HandleApply(self):
        self.m_activeSheet.InsertObject(self.m_sheet.Selection().SelectedTrades(), 1)
        self.m_fuxDlg.CloseDialogCancel()
    
    
    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        self.m_tradeNbrCtrl = self.m_bindings.AddBinder( 'tradeNbrCtrl', acm.GetDomain('string'), None )
    
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.BeginHorzBox('None')
        self.m_tradeNbrCtrl.BuildLayoutPart(b, 'Midas TradeNo')
        b.AddButton('trades', 'Get Trades')
        b.  EndBox()
        b.  AddCustom('sheet', 'sheet.FTradeSheet', 990, 120)
        b.  BeginHorzBox('None')
        b.    AddSpace(50)
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b


def ReallyStartDialog(shell, activeSheet):
    customDlg = midasTradeNoDialog(activeSheet)
    customDlg.InitControls()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg )
    
def StartDialog(eii):
    shell = eii.ExtensionObject().Shell()
    activeSheet=eii.ExtensionObject().ActiveSheet()
    ReallyStartDialog(shell, activeSheet)

