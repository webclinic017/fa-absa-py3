import acm

enbleRealTimePrices = 'enableRealTimePrices'

def TriggerLatch(invokationInfo, toggleName):
    cellInfo = invokationInfo.Parameter('ClickedButton')
    tag = cellInfo.Tag()
    context = cellInfo.Column().Context()
    toggleEval = acm.GetCalculatedValueFromString(None, context, toggleName, tag)
    if (toggleEval.Value() == False):
        toggleEval.Simulate(True, False)
        toggleEval.Simulate(False, False)    

def TriggerPriceLatch(invokationInfo):
    TriggerLatch(invokationInfo, enbleRealTimePrices)

def ShowButton(invokationInfo):
    cell = invokationInfo.Parameter("Cell")
    if cell:
        rowObject = cell.RowObject()
        return (rowObject and rowObject.IsKindOf('FPortfolioInstrumentAndTrades'))
    return False

