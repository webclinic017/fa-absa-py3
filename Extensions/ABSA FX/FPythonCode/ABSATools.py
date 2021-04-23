           
import FUIEventHandlers  
import acm          
'''================================================================================================
================================================================================================'''
def OpenInsertedItem(eii):
    
    print 'OpenInsertedItem'

    Sheet = eii.ExtensionObject().ActiveSheet()
    RowObject = Sheet.Selection().SelectedCell().RowObject()
    Icon = RowObject.Icon().Text()
    RowName = RowObject.StringKey()
    application = None

    if Icon ==  'FTradeSelection': #trade filter
        object = acm.FTradeSelection[RowName]
        application = 'Trade Filter'
 
    if Icon ==  'FCompoundPortfolio': #portfolio
        object = acm.FPhysicalPortfolio[RowName]
        application = 'Portfolio Tree Definition'
 
    if Icon == 'FPhysicalPortfolio+QueryFolderDecoration': #instrumnet or inseritems
        querylist = acm.FStoredASQLQuery.Select('name = %s' % RowName)
        application = 'Insert items'
        if len(querylist) > 0:
            object = querylist[0]
        else:
            object = acm.FInstrument[RowName]
            application = 'Instrument Definition'

    if Icon == 'InstrumentBkg+FCurrency+FTrade+Inactive': #trade
        object = acm.FTrade[int(RowName)]
        application = 'Instrument Definition'
        
    if application != None:
        acm.StartApplication(application, object)
    else:
        if Sheet.SheetClass() == acm.FPortfolioSheet:
            FUIEventHandlers.PortfolioSheet_DoubleClick(eii)
        if Sheet.SheetClass() == acm.FTradeSheet:
            FUIEventHandlers.TradeSheet_DoubleClick(eii)
'''================================================================================================
================================================================================================'''
def UpdateAdditionalInfo(workbook):
    Addinfo = acm.FAdditionalInfo.Select01("addInf = 'LastUsed' and recaddr = %i" % workbook.Oid(), '')
    if Addinfo == None:
        Addinfo = acm.FAdditionalInfo()
        Addinfo.AddInf(acm.FAdditionalInfoSpec['LastUsed'])
        Addinfo.Recaddr(workbook.Oid())
    Addinfo.FieldValue(acm.Time.TimeNow())
    Addinfo.Commit()
'''================================================================================================
================================================================================================'''
def OpenTradesInWorkbook(eii):
    object = eii.ExtensionObject()
    TempPort = acm.FAdhocPortfolio()
    TempPort.Name(object.AsSymbol())
    
    Row = object.ActiveSheet().Selection().SelectedRowObjects()[0]
    [TempPort.Add(t) for t in Row.Trades()]
    if TempPort.Trades().Size() > 0:     
        tradingMgr = acm.StartApplication('Trading Manager', acm.FTradingSheetTemplate['OptionsCheck'])
        sheet = tradingMgr.ActiveSheet() #.NewSheet("TradeSheet") #Maybe use existing Trade Sheet or Template
        sheet.InsertObject(TempPort, 0)
'''================================================================================================
================================================================================================'''

