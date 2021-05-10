  
"""
 FVerticalTrading ver 1.0.0 (compatible with PRIME 3.2.0)
 Implementation of vertical trading button action handler when adding or subtracting an order at a specific price
"""

import ael
import acm

def onAddVerticalOrder(invokationInfo):
    sheet = invokationInfo.ExtensionObject().ActiveSheet()
    button = invokationInfo.Parameter("ClickedButton")
    if button:
        priceValueRow = button.BusinessObject()
        bidOrAsk = invokationInfo.Definition().At("BidOrAsk")
        order = priceValueRow.CreateVerticalOrder(bidOrAsk)
        if order:
            sheet.SendOrder(order)

def onDeleteLastVerticalOrder(invokationInfo):
    sheet = invokationInfo.ExtensionObject().ActiveSheet()
    orders = GetVerticalOrders(invokationInfo)
    if orders.Size() > 0:
        last = acm.FArray()
        last.Add(orders.Last())
        sheet.DeleteOrders(last)

def onDeleteVerticalOrders(invokationInfo):
    sheet = invokationInfo.ExtensionObject().ActiveSheet()
    orders = GetVerticalOrders(invokationInfo)
    if orders.Size() > 0:
        sheet.DeleteOrders(orders)

def GetVerticalOrders(invokationInfo):
    button = invokationInfo.Parameter("ClickedButton")
    if button:
        priceValueRow = button.BusinessObject()
        bidOrAsk = invokationInfo.Definition().At("BidOrAsk")
        orders = priceValueRow.TradersOwnOrders(bidOrAsk)
        return orders
    return acm.FArray()

def wantButton(invokationInfo):
    buttonWanted = False
    cell = invokationInfo.Parameter("Cell")
    if cell:
        rowObject = cell.RowObject()
        if rowObject and rowObject.IsKindOf('FPriceValueRow'):
            if rowObject.OrderDepth() < 0:
                buttonWanted = True
    return buttonWanted
