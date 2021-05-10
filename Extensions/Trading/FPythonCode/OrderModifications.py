
import acm

def CreateOrderHandler(ownOrder, invokationInfo):
    session = invokationInfo.ExtensionObject().ActiveSheet().TradingSession()
    if session:
        return session.AttachOrder(ownOrder, True)
    return None
    
def tickPriceUpDown(invokationInfo, up):
    try:
        cell = invokationInfo.Parameter('ClickedButton')
        orderHandler = CreateOrderHandler(cell.RowObject(), invokationInfo)
    
        if orderHandler and orderHandler.IsModifyAllowed('Price') and not orderHandler.UpdateInProgress():
            newPrice = orderHandler.TickUpDown(up, 1, orderHandler.Price().Number())
            orderHandler.Price(newPrice)
            if orderHandler.IsOrderActive():
                orderHandler.SendOrder()
    except Exception as e:
        shell = invokationInfo.Parameter('shell')
        acm.UX().Dialogs().MessageBoxInformation(shell, str(e))

def onPriceTickUp(invokationInfo):
    tickPriceUpDown(invokationInfo, True)
   
def onPriceTickDown(invokationInfo):
    tickPriceUpDown(invokationInfo, False)
    
def onWantButton(invokationInfo):
    buttonNeeded = False
    cell = invokationInfo.Parameter('Cell')
    if cell:
        rowObject = cell.RowObject()
        if rowObject and rowObject.IsKindOf('FOwnOrder') and rowObject.TradingInterface() != None:
            buttonNeeded = True
    return buttonNeeded
    

        
    

