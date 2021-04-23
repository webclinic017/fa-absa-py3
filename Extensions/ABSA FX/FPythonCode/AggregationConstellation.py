'''================================================================================================
================================================================================================'''
import acm, ael
'''================================================================================================
================================================================================================'''
def GetAggregationTrades(trade): # passing aggregate trades 
    tradeIds = ael.dbsql("select trdnbr from trade where aggregate_trdnbr = %d" % trade.Oid() )
    TempPort = acm.FAdhocPortfolio()
    TempPort.Name(trade.Oid())
    [TempPort.Add(acm.FTrade[t[0]]) for t in tradeIds[0]]
    if TempPort.Trades().Size() > 0:     
        tradingMgr = acm.StartApplication('Trading Manager', acm.FTradingSheetTemplate['FX_AggregationView'])
        sheet = tradingMgr.ActiveSheet() #.NewSheet("TradeSheet") #Maybe use existing Trade Sheet or Template
        sheet.InsertObject(TempPort, 0)
'''================================================================================================
================================================================================================'''
def ButtonAction(invokationInfo): #FExtensionInvokationInfo
    trade =  invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedRowObjects()[0].Trade()
    GetAggregationTrades(trade)
'''================================================================================================
================================================================================================'''
def ButtonCreate(invokationInfo): #FExtensionInvokationInfo
    cell = invokationInfo.Parameter("Cell")
    if cell:
        try:
            rowObject = cell.RowObject()
            print rowObject.Trade().Type()
            if rowObject.Class() == acm.FTradeRow and rowObject.Trade().Type() == 'FX Aggregate': 
                return True
        except Exception, e:
            pass
    return False
    
'''================================================================================================
================================================================================================'''
def GetAggregationCount(trade): # passing aggregate trades 
    sqlStr = "select trdnbr from trade where aggregate_trdnbr = %d" % trade.Oid() 
    tradeIds = ael.dbsql(sqlStr)
    return len(tradeIds[0])
