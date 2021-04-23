import acm
import FUxCore
import TradeActionUtilityFunctions 

util = TradeActionUtilityFunctions

def SplitPosition(eii):
    shell = eii.ExtensionObject().Shell()
    selectedRows = util.GetSelectedRows(eii)
    if (selectedRows.Size() == 1):
        if util.ValidateNotDistributedRow(selectedRows):        
            if util.ValidateIsPosition(selectedRows):
                row = selectedRows.First()
                trade = util.GetOriginalTrade(row)
                splitValidator = SplitValidator( trade ) 
                
                if splitValidator.ValidateSplit():
                    dialog = SplitDialog(trade, row)
                    acm.UX().Dialogs().ShowCustomDialogModal(shell, dialog.CreateLayout(), dialog)
                else:
                    util.ShowError(shell, splitValidator.GetErrorMessage())
            else:
                util.ShowError(shell, str("Row must be of type FSingleInstrumentAndTrades"))
        else:
            util.ShowError(shell, str("Split of ODFs not supported for distributed sheets"))
    else:
        util.ShowError(shell, str('Exactly one position row must be selected, got %s' % selectedRows.Size()))

class SplitValidator:
    def __init__( self, trade ):
        self.trade = trade
        self.errMsg = ''
        
    def ValidateSplit( self ):
        return self.ValidateIsSingleTrade() and self.ValidateInsTypeODF() and self.ValidateIsNotSplit() and self.ValidateHasRemainingValue()
        
    def GetErrorMessage( self ):
        return self.errMsg
    
    def ValidateIsSingleTrade( self ):
        if(self.trade):
            return True
        else:
            self.errMsg = 'No unique trade for splitting found!'
            return False
        
    def ValidateInsTypeODF( self ):
        ins = self.trade.Instrument()
        if ins.InsType() != 'FXOptionDatedFwd':
            self.errMsg = 'Only ODF instruments can be split!'
            return False
        return True
        
    def ValidateIsNotSplit( self ):
        links = self.trade.BusinessEventTradeLinks()
        for link in links:
            if link.TradeEventType() == "Cancel" and link.BusinessEvent().EventType() == "Split":
                self.errMsg = 'The position is already split!'
                return False
        return True
        
    def ValidateHasRemainingValue( self ):
        if self.trade.RemainingNominal() == 0.0:
            self.errMsg = 'Cannot split a trade with zero remaining amount!'
            return False
        return True
    


# ########################## Split ODF Dialog #####################################
class SplitDialog (FUxCore.LayoutDialog):
    
    POSITION_COLUMN = 'Portfolio Position'
    ORIGINAL_COLUMNS = ['Portfolio Position']
    SPLIT_COLUMNS = ['Trade Quantity', 'Trade Status', 'Trade Counterparty']
    
    
    def __init__(self, trade, positionRow):
        self.m_trade = trade
        self.m_positionRow = positionRow
        self.m_bindings = None
        self.m_minNbrOfSplits = 2
        self.m_nbrOfSplitsCtrl = None
        self.m_tradeStatusCtrl = None
        self.m_splitSheetCtrl = None
        self.m_splitSheet = None
        self.m_originalSheetCtrl = None
        self.m_originalSheet = None
        self.m_generateBtn = None
        self.m_applyBtn = None
        self.m_fuxDialog = None
        self.m_tradeSplitter = None
        self.InitControls()
        
    def Clear(self):
        self.SetColumns(self.m_splitSheet, self.m_splitSheetCtrl, self.SPLIT_COLUMNS)
        self.m_applyBtn.Enabled(False)
        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.      BeginVertBox()
        b.              BeginHorzBox('Invisible', '')
        self.                   m_nbrOfSplitsCtrl.BuildLayoutPart(b, 'Number Of Split Trades')
        self.                   m_tradeStatusCtrl.BuildLayoutPart(b, 'Trade Status')
        b.                      AddButton('generate', 'Generate')
        b.              EndBox()
        b.              BeginVertBox('EtchedIn', 'Original')
        b.                      AddCustom('originalSheet', 'sheet.FPortfolioSheet', 240, 70)
        b.              EndBox()
        b.              BeginVertBox('EtchedIn', 'Split Trades')
        b.                      AddCustom('splitSheet', 'sheet.FTradeSheet', 240, 200)
        b.              EndBox()
        b.      EndBox()
        b.      BeginHorzBox()
        b.              AddFill()
        b.              AddButton('apply', 'Apply')
        b.              AddButton('close', 'Close')
        b.      EndBox()
        b.EndBox()
        return b
        
    def HandleCreate(self, dialog, layout):
        self.m_fuxDialog = dialog
        self.m_bindings.AddLayout(layout)
        
        self.m_generateBtn = layout.GetControl('generate')
        self.m_generateBtn.AddCallback('Activate', OnGenerateButtonClicked, self)
        
        self.m_applyBtn = layout.GetControl('apply')
        self.m_applyBtn.AddCallback('Activate', OnApplyButtonClicked, self)
        
        closeBtn = layout.GetControl('close')
        closeBtn.AddCallback('Activate', OnCloseButtonClicked, self)
        
        self.m_splitSheetCtrl = layout.GetControl('splitSheet')
        self.m_splitSheet = self.m_splitSheetCtrl.GetCustomControl()
        
        self.m_originalSheetCtrl = layout.GetControl('originalSheet')
        self.m_originalSheet = self.m_originalSheetCtrl.GetCustomControl()
        
        dialog.Caption('Split Position')
        self.SetInitialValues()
        self.SetToolTips()
        
    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
        self.m_nbrOfSplitsCtrl = self.m_bindings.AddBinder('m_nbrOfSplitsCtrl', acm.GetDomain('int'), None)
        self.m_tradeStatusCtrl = self.m_bindings.AddBinder('m_tradeStatusCtrl', 
                                                           acm.GetDomain('enum(TradeStatus)'),
                                                           None,
                                                           acm.TradeStatusTransitions( self.m_trade.Status(), self.m_trade.BoTrdnbr() != 0 ))
        
    def PopulateSheet(self):
        self.Clear()
        self.m_splitSheet.InsertObject(self.m_tradeSplitter.GetSplitTrades(), 'IOAP_LAST')
        
    def SetColumns( self, sheet, sheetCtrl, columns):
        sheet.RemoveAllRows()
        sheet.ColumnCreators().Clear()
        columnCreators = acm.GetColumnCreators(columns, acm.GetDefaultContext())
        i = 0
        while i < columnCreators.Size():
            creator = columnCreators.At(i)
            sheet.ColumnCreators().Add(creator)
            i = i + 1

        sheetCtrl.ForceRedraw()
        
    def SetInitialValues(self):
        self.Clear()
        self.m_nbrOfSplitsCtrl.SetValue(self.m_minNbrOfSplits)
        self.m_tradeStatusCtrl.SetValue(self.m_trade.Status())
        self.m_generateBtn.SetFocus()
        self.SetColumns(self.m_originalSheet, self.m_originalSheetCtrl, self.ORIGINAL_COLUMNS)
        self.m_originalSheet.InsertObject(self.m_positionRow, 'IOAP_LAST')
     
    def SetToolTips(self):
        self.m_nbrOfSplitsCtrl.ToolTip("The number of split trades that the position should be divided into.")
        self.m_tradeStatusCtrl.ToolTip("The trade status that should be used for the closing trade and the generated split trades. The status of the split trades can be edited separately in the Split Trades section before applying the split.")
        self.m_generateBtn.ToolTip("Generate trades in the Split Trades section. The generated trades are not commited until the Apply button is clicked.")
        self.m_originalSheetCtrl.ToolTip("This section shows the original position that should be split.")
        self.m_splitSheetCtrl.ToolTip("This section shows the generated split trades. The quantities of the split trades must be entered and they must sum up to the original position. Trade properties for the split trades can be edited before commiting the trades. The trades are commited when the Apply button is clicked.")
        self.m_applyBtn.ToolTip("Commit the split trades if all entered values are valid.")
        
    def ShowError(self, message):
        shell = self.m_fuxDialog.Shell()
        util.ShowError(shell, message)
        
def OnApplyButtonClicked(self, arg):
    if self.m_tradeSplitter:
        if self.m_tradeSplitter.ValidateSplit():
            components = self.m_tradeSplitter.GetBusinessEventComponents()
        
            try:
                acm.BeginTransaction()
                for component in components:
                    component.Commit()
                acm.CommitTransaction()
                self.PopulateSheet()
                self.m_applyBtn.Enabled(False)
                self.m_generateBtn.Enabled(False)
                self.m_nbrOfSplitsCtrl.Enabled(False)
                self.m_tradeStatusCtrl.Enabled(False)
            except Exception as e:
                self.ShowError('Could not commit transaction: ' + str(e))
        else:
            self.ShowError('Invalid split! ' + self.m_tradeSplitter.ValidateSplitErrorMessage())
    else:
        self.ShowError('Invalid split!')

    
def OnCloseButtonClicked(self, arg):
    self.m_fuxDialog.CloseDialogOK()
    
def OnGenerateButtonClicked(self, arg):
    nbrOfSplits = self.m_nbrOfSplitsCtrl.GetValue()
    tradeStatus = self.m_tradeStatusCtrl.GetValue()
    
    if nbrOfSplits < self.m_minNbrOfSplits:
        self.ShowError('Number Of Split Trades can not be less than ' + str(self.m_minNbrOfSplits))
    else:
        self.m_tradeSplitter = acm.FTradeSplitter( self.m_trade, nbrOfSplits, tradeStatus, util.GetPosition(self.m_positionRow), True)
        self.PopulateSheet()
        self.m_applyBtn.Enabled(True)

                
