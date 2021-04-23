
import ael, acm

def GetMidasTrades(Key):
    Key = Key + "%"  
    sqlStr = "select trdnbr from trade where optional_key like '%s'" % Key 
    TempPort = acm.FAdhocPortfolio()
    tradeIds = ael.dbsql(sqlStr)
    for t in tradeIds[0]:
        TempPort.Add(acm.FTrade[t[0]])
    tradingMgr = acm.StartApplication('Trading Manager', None)
    sheet = tradingMgr.ActiveWorkbook().NewSheet("TradeSheet")
    sheet.InsertObject(TempPort, 0)

ael_variables =  [['midas_no', 'Midas Key', 'string', None, '', 1, 0]]
       

def ael_main(dict):
    GetMidasTrades(dict['midas_no'])
