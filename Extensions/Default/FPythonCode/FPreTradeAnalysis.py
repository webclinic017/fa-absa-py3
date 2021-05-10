import acm
   
def setArrivalPrice(row, col, cell, val, operation):
    row.ArrivalPrice(val)
    row.Changed()
    cell.Unsimulate()
    
def setInitCustFxRate(row, col, cell, val, operation):
    row.InitCustomerCurrencyExchangeRate(val)
    row.Changed()
    cell.Unsimulate()

def onCommitTradeAnalysis(invokationInfo):
    button = invokationInfo.Parameter('ClickedButton')
    shell = invokationInfo.Parameter('shell')
    completion = None
    if shell:
        completion = acm.Trading().CreateCommandCompletion(shell, 'Commit Pre/Post Trade Analysis')
    
    if button:
        order = button.RowObject()
        analysis = order.PrePostTradeAnalysis()
        analysis.CommitToOrder(completion)

def onRefreshTradeAnalysis(invokationInfo):
    button = invokationInfo.Parameter('ClickedButton')
    if button:
        order = button.RowObject()
        analysis = order.PrePostTradeAnalysis()
        analysis.Refresh()
        
def wantButton(invokationInfo):
    cell = invokationInfo.Parameter("Cell")
    if cell:
        rowObject = cell.RowObject()
        if rowObject and rowObject.IsKindOf('FSalesOrder'):
            return True
    return False        
