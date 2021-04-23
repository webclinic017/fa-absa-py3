
"""
Called in menu extension CreateCombiantion
combinationType 0 = All legs weights 1
combinationType 1 = Buy one sell one
combinationType 2 = Sell one buy one
"""
import acm

def createCombinationCallPut(invokationInfo):
    orderbooks = acm.FArray()
    combinationType = int(invokationInfo.Definition().At( "CombinationType").AsString())
    cellInfos = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedCells()
    for info in cellInfos:
        bo = info.BusinessObject()
        if bo:
            orderbooks.Add( bo )
    createCombination( invokationInfo, orderbooks, combinationType )

def createCombinationNormal(invokationInfo):
    tradingInterfaces = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedTradingInterfaces()
    combinationType = int(invokationInfo.Definition().At( "CombinationType").AsString())
    createCombination( invokationInfo, tradingInterfaces, combinationType)

def createCombinationInstrument(invokationInfo):
    activeSheet = invokationInfo.Parameter('sheet')
    instruments = activeSheet.Selection().SelectedInstruments()
    combInstr = acm.FCombination()
    
    if instruments.Size() <= 1:
        return
    for ins in instruments:
        combInstr.AddInstrument(ins, 1)
        
    combInstr.RegisterInStorage()
    combInstr.Currency(instruments[0].Currency())
    combInstr.Quotation = "Per Unit"
    combInstr.ContractSize = 1.0
    combInstr.Name = constructName(instruments)

    invokationInfo.ExtensionObject().ActiveSheet().InsertObject( combInstr, "IOAP_ATCURSOR" )    

def constructName(instruments):
    name = instruments.Size() > 2 and "SP" or "BA"
    i = 0
    for instrument in instruments:
        if i < 2:
            name = name + '+' + instrument.Name()
        if i == 2:
            name = name + '...'
        i = i + 1
    return name

def openCopyInInstrumentDefinition(invokationInfo):
    sheet = invokationInfo.ExtensionObject().ActiveSheet()
    instruments = sheet.Selection().SelectedInstruments()
    ins = instruments.Size() == 1 and instruments[0] or None
    if ins:
        clone = ins.Clone()
        clone.Commit()
        acm.StartApplication("Instrument Definition", clone)
    else:
        print ("Please select only one combination at the time.")

def createCombination(invokationInfo, tradingInterfaces, combinationType):
    combInstr = acm.FCombination()
    tradingInterfaces = acm.GetFunction('removeDuplicates', 1)(tradingInterfaces)
    
    if tradingInterfaces.Size() <= 1:
        return
    name = 'SP'
    if tradingInterfaces.Size() > 2:
        name = 'BA '
    try:
        if combinationType == 0: 
            i = 0
            for tradingInterface in tradingInterfaces:
                i = i+1
                combInstr.AddOrderBook(tradingInterface.StoredOrderBook(), 1)
                if i < 4:
                    name = name + '+' + tradingInterface.Instrument().Name()
                if i == 4:
                    name = name + '...'

        if combinationType == 1:
            combInstr.AddOrderBook(tradingInterfaces.At(0).StoredOrderBook(), 1)
            name = name + ' +' + tradingInterfaces.At(0).Instrument().Name()
            combInstr.AddOrderBook(tradingInterfaces.At(1).StoredOrderBook(), -1)
            name = name + ' -' + tradingInterfaces.At(1).Instrument().Name()

        if combinationType == 2:
            combInstr.AddOrderBook(tradingInterfaces.At(0).StoredOrderBook(), -1)
            name = name + ' -' + tradingInterfaces.At(0).Instrument().Name()
            combInstr.AddOrderBook(tradingInterfaces.At(1).StoredOrderBook(), 1)
            name = name + ' +' + tradingInterfaces.At(1).Instrument().Name()

        combInstr.Name(name)
        combInstr.ContractSize(tradingInterfaces.At(0).Instrument().ContractSize())
        combInstr.Quotation(tradingInterfaces.At(0).Instrument().Quotation())
        combInstr.Currency(tradingInterfaces.At(0).Instrument().Currency())

        combInstr.RegisterInStorage()
        basket = acm.Trading.CreateBasketTrading(combInstr)
        invokationInfo.ExtensionObject().ActiveSheet().InsertObject( basket, "IOAP_ATCURSOR" )
    except Exception as e:
        shell = invokationInfo.Parameter('shell')
        acm.UX().Dialogs().MessageBoxOKCancel(shell, 'Error', str(e), 'Failed to create combination')
        
def saveCombination(invokationInfo):
    instruments = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedInstruments()
    instruments.Commit()
