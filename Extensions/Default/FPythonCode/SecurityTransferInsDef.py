
import acm

def InitSecurityTransferTrade(trade):
    if trade.IsInfant():
        trade.ValueDay(acm.Time().DateToday())        
    if not trade.Counterparty():
        trade.Counterparty('FMAINTENANCE')
    trade.AcquireDay(trade.ValueDay())
    trade.Quantity(-1)
    trade.Price(0)
    trade.Premium(0)
    trade.FlatAccrued(True)
    if not trade.Acquirer():
        trade.Acquirer('FMAINTENANCE')
    trade.Type('Security Transfer')    
    
def StartSecurityTransferApplication(invokationInfo):
    sourceTrade = acm.DealCapturing().CreateNewCustomTrade('Security Transfer', None)
    initData = acm.DealCapturing().UX().InitDataFromTemplate(sourceTrade, 'Security Transfer')
    acm.StartApplication('Instrument Definition', initData)
