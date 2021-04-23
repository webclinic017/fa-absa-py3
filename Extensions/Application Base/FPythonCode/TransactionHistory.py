import acm
import FUxCore

class TransactionHistoryPanel(FUxCore.LayoutPanel):
    def __init__(self):
        self.m_ctrlShowChanged = 0
        self.m_ctrlShowFieldValues = 0
        self.m_transObject = 0
        self.m_treeRoot = 0
        self.m_transHistComponent = 0
        pass

    def ServerUpdate(self, sender, aspect, parameter ):
        if str(aspect) == str('SelectionChanged'):
            self.DoSelectionDiff()
            
    def HandleCreate( self ):
        layout = self.m_uxLayoutPanel.SetLayout(self.HandleCreateLayout())
        
        self.m_transHistComponent = acm.UX().Components().TransactionHistory().Create(layout)
        
        asqlFrame = self.Owner()
        asqlFrame.SortColumn('UpdateTime', False)
        self.Owner().AddDependent(self)

    def HandleCreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('EtchedIn', "Transaction diff")
        
        acm.UX().Components().TransactionHistory().BuildLayoutPart(b, "DifferenceTree")
        
        b.EndBox()
        return b

        
    def DoSelectionDiff(self):
        self.ShowSelectionDiff()

    def ShowSelectionDiff(self):
        asqlFrame = self.Owner()
        transHistory = None
        transHistoryOther = None
        transObject = None
        
        selection = asqlFrame.Selection()
        if selection.Size() == 1:
            transHistory = selection.At(0)
        elif selection.Size() == 2:
            transHistory = selection.At(0)
            transHistoryOther = selection.At(1)
            
        if transHistory:
            try:
                arr = acm.FArray()
                arr.Add(transHistory)
                arr.Add(transHistoryOther)

                self.m_transHistComponent.SetTransactionHistoryArray(arr)
            except Exception as ex:
                self.m_transHistComponent.SetTransactionHistoryArray(None)
        else:
            self.m_transHistComponent.SetTransactionHistoryArray(None)

def ShowTransactionHistoryForInstrumentAndTradesMenu(eii):
    insdef = eii.ExtensionObject()
    shell = eii.Parameter('shell')  
    ins =  insdef.OriginalInstrument()
    trade =  insdef.OriginalTrade()
    appname = None
    if ins:
        appname = ins.StringKey()
    if trade:
        appname = trade.Instrument().StringKey() + " " + trade.StringKey()
    ShowTransactionHistoryForInstrumentAndTradesPrivate(ins, trade, shell, appname)
    
def ShowTransactionHistoryForInstrumentAndTradesRightClick(eii):
    shell = eii.Parameter('shell')    
    'ExtensionObject returns a FArray containing the real object'
    ob = eii.ExtensionObject()[0]
    if ob.IsKindOf(acm.FInstrument):    
        ShowTransactionHistoryForInstrumentAndTradesPrivate(ob, None, shell, ob.StringKey())
    elif ob.IsKindOf(acm.FTrade):  
        appname = ob.Instrument().StringKey() + " " + ob.StringKey()
        ShowTransactionHistoryForInstrumentAndTradesPrivate(None, ob, shell, appname)
        
def OpenTransactionHistoryForInstrumentAndTrades(ins, trade, shell):
    appName = None
    if ins:
        appName = ins.StringKey()
    if trade:
        appName = trade.Instrument().StringKey() + " " + trade.StringKey()
    ShowTransactionHistoryForInstrumentAndTradesPrivate(ins, trade, shell, appName)
    
def ShowTransactionHistoryForInstrumentAndTradesPrivate(ins, trade, shell, appname):
    
    query = acm.CreateFASQLQuery(acm.FTransactionHistory, 'AND')

    time = query.AddOpNode('AND')
    time.AddAttrNode('UpdateTime', 'LESS_EQUAL', None)
    time.AddAttrNode('UpdateTime', 'GREATER_EQUAL', None)

    name = query.AddOpNode('OR')
    name.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)

    description = query.AddOpNode('OR')
    description.AddAttrNode('Description', 'RE_LIKE_NOCASE', None)

    version = query.AddOpNode('OR')
    version.AddAttrNode('Version', 'LESS_EQUAL', None)
    version.AddAttrNode('Version', 'GREATER_EQUAL', None)
    
    subquery = query.AddOpNode('OR')

    if ins:
        sub = subquery.AddOpNode('AND')
        typeNode = sub.AddOpNode('OR')
        typeNode.AddAttrNode('TransRecordType', 'EQUAL', 4 )
        name = sub.AddOpNode('OR')
        name.AddAttrNode('Name', 'EQUAL', ins.Name())

    if trade:
        sub = subquery.AddOpNode('AND')
        typeNode = sub.AddOpNode('OR')
        typeNode.AddAttrNode('TransRecordType', 'EQUAL', 19 )
        sub.AddAttrNodeNumerical('RecordId', trade.Oid(), trade.Oid() )

    farTrade = acm.FX.GetSwapFarTrade(trade)
    if farTrade:
        sub = subquery.AddOpNode('AND')
        typeNode = sub.AddOpNode('OR')
        typeNode.AddAttrNode('TransRecordType', 'EQUAL', 19 )
        sub.AddAttrNodeNumerical('RecordId', farTrade.Oid(), farTrade.Oid() )
        
    user = query.AddOpNode('OR')
    user.AddAttrNode('UpdateUser.Name', 'RE_LIKE_NOCASE', None)

    if ins or trade:
        customPanel = TransactionHistoryPanel()
        name = 'Transaction History ' + '\'' + appname + '\''
        ii = acm.StartFASQLEditor(name, None, None, query, None, True, True, customPanel, False, "", True, "", False )
        ii.SortColumn('UpdateTime', False)
    else:
        acm.UX().Dialogs().MessageBoxInformation(shell, 'No instrument selected.')    

    
def ShowTransactionHistoryMenu(eii):
    dialog = eii.ExtensionObject()
    shell = eii.Parameter('shell')    
    ob =  dialog.CurrentObject()    
    ShowTransactionHistoryPrivate(ob, shell)
    

def ShowTransactionHistoryRightClick(eii):    
    shell = eii.Parameter('shell')    
    'ExtensionObject returns a FArray containing the real object'
    ob = eii.ExtensionObject()[0]
    ShowTransactionHistoryPrivate(ob, shell)

def ShowTransactionHistoryPrivate(ob, shell):
    query = acm.CreateFASQLQuery(acm.FTransactionHistory, 'AND')

    time = query.AddOpNode('AND')
    time.AddAttrNode('UpdateTime', 'LESS_EQUAL', None)
    time.AddAttrNode('UpdateTime', 'GREATER_EQUAL', None)

    version = query.AddOpNode('OR')
    version.AddAttrNode('Version', 'LESS_EQUAL', None)
    version.AddAttrNode('Version', 'GREATER_EQUAL', None)

    user = query.AddOpNode('OR')
    user.AddAttrNode('UpdateUser.Name', 'RE_LIKE_NOCASE', None)
        

    subquery = query.AddOpNode('OR')
        
    if ob:        
        enumeration = acm.FEnumeration['enum(B92RecordType)']    
        rectype = enumeration.Enumeration(ob.RecordType())
        sub = subquery.AddOpNode('AND')
        typeNode = sub.AddOpNode('OR')
        typeNode.AddAttrNode('TransRecordType', 'EQUAL', rectype)
        sub.AddAttrNodeNumerical('RecordId', ob.Oid(), ob.Oid() )
    
        customPanel = TransactionHistoryPanel()
        name = 'Transaction History ' + '\'' + ob.StringKey() + '\''
        ii = acm.StartFASQLEditor(name, None, None, query, None, True, True, customPanel, False, "", True )
        ii.SortColumn('UpdateTime', False)
    else:
        acm.UX().Dialogs().MessageBoxInformation(shell, 'No object selected.')
    
    
def ShowTransactionHistory(eii):
    arr = acm.FArray()
    arr.Add(acm.FTransactionHistory)
    customPanel = TransactionHistoryPanel()
    ii = acm.StartFASQLEditor('Transaction History', arr, None, None, None, None, None, customPanel )
    ii.SortColumn('UpdateTime', False)
