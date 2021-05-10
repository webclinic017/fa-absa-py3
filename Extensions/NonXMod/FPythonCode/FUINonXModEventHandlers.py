import acm

def TradingSheet_doubleClick(eii):
    trdMgrFrame = eii.ExtensionObject()
    sheet = trdMgrFrame.ActiveSheet()
    
    sel = sheet.Selection()
    cell = sel.SelectedCell()
    
    if not cell:
        return
    
    orderKindEnum  = acm.GetDomain('enum(OrderKind)')
    fillOrJoinEnum = acm.GetDomain('enum(FillOrJoin)')
    
    orderKind   = orderKindEnum.Enumeration('okFill')
    fillOrJoin  = fillOrJoinEnum.Enumeration('Fill')

    orderDict   = sheet.CreateOrderForCurrentCell(orderKind, True, fillOrJoin)

    if not orderDict:
        return
    order = orderDict.At('order')

    instrOrTrade = 0
    if order:
        order = order.Clone()
        buyOrSellEnum = acm.GetDomain('enum(BuyOrSell)')
        instrOrTrade = acm.Trading().CreateTradeFromOwnOrder(order, buyOrSellEnum.Enumeration('Buy'))
    else:
        rowObject = cell.RowObject()
        try:
            instrOrTrade = rowObject.SingleInstrumentOrSingleTrade()
        except:
            pass

    if instrOrTrade:
        cmpTrdEntries = acm.FindInstancesOfApplication("Compact Trade Entry")
    
        if cmpTrdEntries.Size():
            for cmpTrdEntry in cmpTrdEntries:
                cmpTrdEntry.SetContents(instrOrTrade)
        else:
            acm.StartApplication("Compact Trade Entry", instrOrTrade)
