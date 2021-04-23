'''================================================================================================
================================================================================================'''
import acm
import FUxCore
def OnChangeGroupType (self, cd): self.UpdateView(self.m_lastSelectedTrade, self.GetGroup())
'''================================================================================================
================================================================================================'''
class FUX_ConnectedTradesDockWindow (FUxCore.LayoutPanel):
    def __init__(self, parent):
        self.m_parent = parent
        self.m_shell = parent.Shell()
        self.m_row = None
        self.m_trade = None
        self.m_group = None
        self.m_tradeLabel = None
        self.m_lastSelectedTrade = None
        self.m_tradeConnRefCalls = None
		
    def ServerUpdate(self, sender, aspect, parameter ):
        if str(aspect) == str('SelectionChanged'):
            self.HandleSelectionChanged( sender )
            
    def HandleCreate( self ):
        layout = self.SetLayout( self.CreateLayout() )
        self.m_sheet = layout.GetControl('sheet').GetCustomControl()
        self.m_sheet.ShowGroupLabels(False)
        
        #Get Control of the Trade and Grouping labels
        self.m_tradeLabel = layout.GetControl('tradeLabel')
        self.m_groupingType = layout.GetControl('groupingType')
        
        #Define the Grouping Types with their associated relational attribute and acm methods
        #<ToDo> Must be a better way to Call and Invoke all the Trade Reference Group Methods..
        self.m_tradeConnRefCalls = acm.FDictionary()
        self.m_tradeConnRefCalls.AtPut('Contract', ('contract', 'Contract()'))
        self.m_tradeConnRefCalls.AtPut('Trans', ('trxTrade', 'TrxTrade()'))
        self.m_tradeConnRefCalls.AtPut('Correct', ('correctionTrade', 'CorrectionTrade()'))
        self.m_tradeConnRefCalls.AtPut('Mirror', ('mirrorTrade', 'MirrorTrade()'))
        self.m_tradeConnRefCalls.AtPut('Connect', ('connectedTrade', 'ConnectedTrade()'))
        self.m_tradeConnRefCalls.AtPut('Group', ('groupTrdnbr', 'GroupTrdnbr()'))
        #Populate the GroupingList drop down
        self.m_groupingType.Populate(self.m_tradeConnRefCalls.Keys())
        
        self.m_tradeLabel.SetData('No Trade Chosen')
        self.m_tradeLabel.Editable(False)
        
        updated = self.UpdateValueInfo()
        if updated:
            self.UpdateView(self.GetTrade(), self.GetGroup())
            
        self.m_groupingType.AddCallback('Changed', OnChangeGroupType, self) 
        self.Owner().AddDependent(self)
		
    def HandleDestroy( self ):
        self.Owner().RemoveDependent(self)
        self.m_groupingType.RemoveDependent(self)
		
    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginHorzBox('EtchedIn', 'Trade Connections View')
        b.    BeginVertBox()
        b.      AddInput('tradeLabel', 'Trade ID')
        b.      AddOption( 'groupingType', 'Grouping Type' )
        b.      AddCustom('sheet', 'sheet.FTradeSheet', 400, 100)
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b

    def UpdateView(self, trade, groupType):
        context = self.GetContext()
        if trade:
            self.m_tradeLabel.SetData(trade.Oid())
            #Update connections only if the Trade or Group selection changed    
            if self.m_trade is None or (trade <> self.m_trade) or (groupType <> self.m_group):
                if groupType:
                    self.m_sheet.RemoveAllRows()
                    connectedTrades = self.GetReferenceTrades(trade, groupType)
                    self.InsertObjects(connectedTrades)
                    self.m_group = groupType
            self.m_trade = trade
            self.m_lastSelectedTrade = trade
        else:
            self.m_trade = None
    
    def UpdateValueInfo(self):
        updated = False
        row = self.GetRowObject()
        context = self.GetContext()
        tag = self.GetTag()
        if row:
            if self.m_row is None or (row <> self.m_row):
                updated = True
        self.m_row = row
        return updated
        
    def InsertObjects(self, objects):
        if objects:
            self.m_sheet.InsertObject(objects, 'IOAP_LAST')
            
    def GetSelectedSheetCell(self):
        sheet = self.m_parent.ActiveSheet()
        if sheet:
            selection = sheet.Selection()
            if selection:
                return selection.SelectedCell()

    def GetContext(self):
        context = None
        cell = self.GetSelectedSheetCell()
        if cell: context = cell.Column().Context()
        if not context: context = acm.GetDefaultContext()
        return context

    def GetRowObject(self):
        row = None 
        cell = self.GetSelectedSheetCell()
        if cell: row = cell.RowObject()
        return row
        
    def GetTag(self):
        tag = acm.GetGlobalEBTag()
        cell = self.GetSelectedSheetCell()
        if cell: tag = cell.Tag()
        return tag

    def GetTrade(self):
        trade = None
        row = self.GetRowObject()
        if row:
            if row.IsKindOf(acm.FTradeRow):
                trade = row.Trade()
        return trade
	
    def GetGroup(self):
        return self.m_groupingType.GetData()

    def GetTrxConnectedTrades(self, trade):
        print 'Getting Trx Connections for Trade : ', trade.Oid()
        trades = acm.FArray()
        if trade.TrxTrade():
            trxTrades = acm.FTrade.Select('trxTrade = %s' % trade.TrxTrade().Oid())
            for trxTrade in trxTrades:
                if not acm.TradeActionUtil().ValidateTradeToClose(trxTrade):
                    trades.Add(trxTrade)
            trades.Remove(trade)
        return trades

    def GetReferenceTrades(self, trade, referenceType):
        # Get all associated trades for any GroupType that was referenced
        #<ToDo> Probably a better way to invoke the relevant db attributes and acm calls
        #
        print 'Getting %s Connections for Trade : %i' %(referenceType, trade.Oid())
        trades = acm.FArray()
        refTrade = trade.Invoke(self.m_tradeConnRefCalls.At(referenceType)[1])
        if refTrade:
            connectedTrades = acm.FTrade.Select(self.m_tradeConnRefCalls.At(referenceType)[0] + ' = %s' % refTrade.Oid())
            for connectedTrade in connectedTrades:
                if not acm.TradeActionUtil().ValidateTradeToClose(connectedTrade):
                    trades.Add(connectedTrade)
            trades.Remove(trade)
        return trades

    def HandleSelectionChanged(self, sender):
        if sender.IsKindOf(acm.FUxValuationViewer):
            self.UpdateView(self.SelectedTrade(), self.GetGroup())
        else:
            if self.m_sheet and self.m_sheet <> sender.ActiveSheet():
                self.m_parent = sender
                updated = self.UpdateValueInfo()
                if updated:
                    self.UpdateView(self.GetTrade(), self.GetGroup())
                    
'''================================================================================================
================================================================================================'''
def OnCreate(eii):
    basicApp = eii.ExtensionObject()
    myPanel = FUX_ConnectedTradesDockWindow(basicApp)
    basicApp.CreateCustomDockWindow(myPanel, 'connectedTrades', 'Connected Trades View', 'Bottom', None, True, False)
