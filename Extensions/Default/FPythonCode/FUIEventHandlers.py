import acm

try:
    from SalesRFQDialog import StartSalesRFQDialogFromQuoteRequest
    canStartRfqDialog = True
except:
    canStartRfqDialog = False

'''#######################################################
 Helper functions
#######################################################'''

def StartInstrumentDefinition(entity, eii):
    try:
        acm.StartApplication("Instrument Definition", entity)
    except RuntimeError as e:
        msg = "Cannot open Instrument Definition Application.\n"
        msg = msg + e.message.split(':')[0]
        acm.UX().Dialogs().MessageBox(eii.ExtensionObject().Shell(), 'Error', msg, 'OK', None, None, 'Button1', 'Button1')

def StartInsDef(instrOrTrade, eii):
    if instrOrTrade:
        openedAsDP = OpenAsDealPackage(instrOrTrade, eii)
        if not openedAsDP:
            instrOrTrade = instrOrTrade.Originator()
            instrument = Instrument(instrOrTrade)
            if instrument.IsKindOf(acm.FPortfolioSwap):
                acm.StartApplication("Portfolio Swap", instrument)
            else:
                trade = Trade(instrOrTrade)
                if trade and not trade.IsInfant():
                    StartInstrumentDefinition(trade, eii)
                elif InstrumentCanBeOpened(instrument):
                    StartInstrumentDefinition(instrument, eii)
                else:
                    raise Exception("Cannot open Infant Objects in Instrument Definition window")

def InstrumentCanBeOpened(instrument):
    if instrument and (not instrument.IsInfant() or instrument.Class().IsEqual(acm.FFxRate) or instrument.Class().IsEqual(acm.FPreciousMetalRate)):
        return True
    return False
      
def GetDealPackageApplication(dealPackage):
    customApplName = "" 
    if dealPackage:
        definition = dealPackage.Definition()
        if definition and definition.CustomApplicationName():
            customApplName = definition.CustomApplicationName()
    return customApplName
                     
def OpenAsDealPackage(instrOrTrade, eii):
    openedAsDP = False
    dealPackage = DealPackage(instrOrTrade, eii)
    customApplName = GetDealPackageApplication(dealPackage)
    if dealPackage and customApplName:
        try:
            acm.StartApplication(customApplName, dealPackage)
            openedAsDP = True
        except:
            pass
    return openedAsDP

def FindInstrOrTrade(cell):
    instrOrTrade = None
    rowObject = cell.RowObject()
    try:
        try:
            instrOrTrade = rowObject.SingleInstrumentOrSingleTrade()
        except:
            pass
        if not instrOrTrade:
            instrOrTrade = rowObject.Trade()
            if not instrOrTrade:
                instrOrTrade = rowObject.Instrument()
    except:
        instrOrTrade = None
    return instrOrTrade

def Instrument(instrOrTrade):
    instrument = None
    if instrOrTrade:
        if instrOrTrade.IsKindOf(acm.FTrade):
            instrument = instrOrTrade.Instrument()
        elif instrOrTrade.IsKindOf(acm.FInstrument):
            instrument = instrOrTrade
    return instrument
    
def Trade(instrOrTrade):
    trade = None
    if instrOrTrade:
        if instrOrTrade.IsKindOf(acm.FTrade):
            trade = instrOrTrade
    return trade
    
def DealPackageParent(dealPackage):
    if dealPackage and dealPackage.Type() != 'Life Cycle Event':
        parent = dealPackage.ParentDealPackage()
        if parent:
            return DealPackageParent(parent)
    return dealPackage

def IsOneTradeInstrument(ins):
    toReturn = False
    if ins and ins.InsType() in ['Portfolio Swap']:
        toReturn = ins.Trades().Size() == 1
    return toReturn
    
def TradeFromOneTradeInstrument(ins):
    trade = None
    if IsOneTradeInstrument(ins):
        trade = ins.Trades().First()
    return trade

def UniqueTrade(instrOrTrade):
    trade = Trade(instrOrTrade)
    if not trade:
        trade = TradeFromOneTradeInstrument( Instrument(instrOrTrade) )
    return trade

def DealPackage(instrOrTrade, eii):
    dealPackage = None
    trade = UniqueTrade(instrOrTrade)
    if trade and not trade.IsClone():
        try:
            dealPackage = DealPackageParent(trade.DealPackage())
        except:
            dealPackage = None
            msg = 'Trade is part of more than one dealpackage and will not be opened in Deal Package Application.'
            acm.UX().Dialogs().MessageBoxInformation(eii.ExtensionObject().Shell(), msg)
    return dealPackage

def CreateOwnOrderDict(sheet):
    orderKindEnum = acm.GetDomain('enum(OrderKind)')
    fillOrJoinEnum = acm.GetDomain('enum(FillOrJoin)')

    kind = orderKindEnum.Enumeration('okFill')
    fillOrJoin = fillOrJoinEnum.Enumeration('Fill')

    return sheet.CreateOrderForCurrentCell( kind, True, fillOrJoin )
 
def GetSheetCell(eii):   
    sheet = eii.Parameter( "sheet" )
    sel = sheet.Selection()
    return sel.SelectedCell()
    
    

'''#######################################################
  UI Event Handler functions
#######################################################'''

def TradeSheet_DoubleClick(eii):
    cell = GetSheetCell(eii)
    if cell and cell.IsHeaderCell():
        instrOrTrade = FindInstrOrTrade(cell)
        instrument = Instrument(instrOrTrade)
        StartInsDef(instrOrTrade, eii)
            
def PortfolioSheet_DoubleClick(eii):
    cell = GetSheetCell(eii)
    if cell:
        bo = cell.BusinessObject()
        
        if bo and bo.IsKindOf("FOrderBook"):
            tm = eii.ExtensionObject()
            sheet = tm.ActiveSheet()
            sheet.DoOrderDblClickActionFromCurrentCell()
        elif cell.IsHeaderCell():
            instrOrTrade = FindInstrOrTrade(cell)
            StartInsDef(instrOrTrade, eii)
    
def DealSheet_DoubleClick(eii):
    eo = eii.ExtensionObject()
    if not eo.Class() in ( acm.FUiTrdMgrFrame, acm.CCalculatorAppFrame ):
        return
        
    cell = GetSheetCell(eii)
    if cell and cell.IsHeaderCell():
        instrOrTrade = FindInstrOrTrade(cell)
        StartInsDef(instrOrTrade, eii)

def MoneyFlowSheet_DoubleClick(eii):
    tm = eii.ExtensionObject()
    if not tm.Class() == acm.FUiTrdMgrFrame:
        return
    cell = GetSheetCell(eii)
    if cell and cell.IsHeaderCell():
        instrOrTrade = FindInstrOrTrade(cell)
        StartInsDef(instrOrTrade, eii)
        

def VerticalPortfolioSheet_DoubleClick(eii):
    tm = eii.ExtensionObject()
    if not tm.Class() == acm.FUiTrdMgrFrame:
        return
    cell = GetSheetCell(eii)
    if cell and cell.IsHeaderCell():
        instrOrTrade = FindInstrOrTrade(cell)
        StartInsDef(instrOrTrade, eii)

            
def ThinSheet_DoubleClick(eii):
    tm = eii.ExtensionObject()
    if not tm.Class() == acm.FUiTrdMgrFrame:
        return
    cell = GetSheetCell(eii)
    
    if cell and cell.RowObject():
        try:
            ins = cell.RowObject().Instrument()
            if ins:
                acm.StartApplication("Instrument Definition", ins)            
        except:
            pass

def QuoteRequestPriceSheet_DoubleClick(eii):
    sheet = eii.Parameter( "sheet" )
    result = sheet.DoOrderDblClickActionFromCurrentCell()
    if not result and canStartRfqDialog:
        cell = GetSheetCell(eii)
        if cell:
            bo = cell.BusinessObject()
            if bo:
                quoteRequestInfo = bo.QuoteRequestInfo()
                if quoteRequestInfo:
                    StartSalesRFQDialogFromQuoteRequest(eii.ExtensionObject().Shell(), quoteRequestInfo)
    
def TradingManager_Selchanged(eii, viewChanged):
    tm = eii.ExtensionObject()
    sheet = tm.ActiveSheet()
    
    if not sheet:
       return
       
    sel = sheet.Selection()
    cell = sel.SelectedCell()
    
    if cell:
        
        userPref = acm.GetUserPreferences()
        
        singleOE = userPref.IsSingleOrderEntryEnabled()
        fillOE = userPref.FillOrderEntryOnClick()
       
        showOE = ( tm.IsDockedOrderEntryVisible() or singleOE ) and fillOE
        showCTE = userPref.IsSingleCompactTradeEntryEnabled()
        
        if  showOE or showCTE:
            dict = CreateOwnOrderDict(sheet)
            ownOrder = 0
            if dict :
                ownOrder = dict.At('order')
                fillOrJoin = dict.At('fillOrJoin')

                if showOE:
                    tm.UpdateOrderInOrderEntry( ownOrder, fillOrJoin )
            
            if showCTE:

                if ownOrder:
                    buyOrSellEnum = acm.GetDomain('enum(BuyOrSell)')
                    instrOrTrade = acm.Trading().CreateTradeFromOwnOrder(ownOrder, buyOrSellEnum.Enumeration('Buy'))
                else:
                    instrOrTrade = FindInstrOrTrade(cell)
                    
                if instrOrTrade:
                    cmpTrdEntries = acm.FindInstancesOfApplication("Compact Trade Entry")
                    
                    if cmpTrdEntries.Size():
                        for cmpTrdEntry in cmpTrdEntries:
                            cmpTrdEntry.SetContents(instrOrTrade)
                            

def BusinessProcessSheet_DoubleClick(eii):
    try:
        cell = GetSheetCell(eii)
        if cell.RowObject().Class() == acm.FBusinessProcess:
            acm.StartApplication("Business Process Details", cell.RowObject())
    except AttributeError:
        pass

def CorporateActionElectionSheet_DoubleClick(eii):
    try:
        cell = GetSheetCell(eii)
        if cell.RowObject().Class() == acm.FCorporateActionElection:
            acm.StartRunScript(cell.RowObject(), "Modify")
    except AttributeError:
        pass

def CorporateActionSheet_DoubleClick(eii):
    try:
        cell = GetSheetCell(eii)
        if cell.RowObject().Class() == acm.FCorporateAction:
            acm.StartRunScript(cell.RowObject(), "Modify")
    except AttributeError:
        pass
