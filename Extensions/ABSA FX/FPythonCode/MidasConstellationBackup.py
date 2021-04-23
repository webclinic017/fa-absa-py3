'''================================================================================================
ButtonAction = Used when adding an action button. Name of Python function. Action to take when button is selected.
ButtonCreate = Used when adding an action button. Name of Python function. Specifies the row types on which the button appears.
ButtonEnable = Used when adding an action button. Name of Python function.
================================================================================================'''
import ael
import acm
'''================================================================================================
ConnectedTrades
manager.CreateUtilityView( acm.FTradeSheet, 'TradeViewer', 'TradeViewer', None, 'Right', 350 )
acm.StartApplication("Connected Trades Viewer", TempPort)
================================================================================================'''
def GetMidasTrades(Key,OptKey = True):

    if OptKey == True:
        KeySearch = Key + "%"  
        sqlStr = "select trdnbr from trade where optional_key like '%s'" % KeySearch 
    else:
        sqlStr = "select trdnbr from trade where your_ref = '%s'" % Key 


    TempPort = acm.FAdhocPortfolio()
    TempPort.Name(Key)
    tradeIds = ael.dbsql(sqlStr)
    
    for t in tradeIds[0]:
        TempPort.Add(acm.FTrade[t[0]])
        
    tradingMgr = acm.StartApplication('Trading Manager', acm.FTradingSheetTemplate['FX_MidasConstView'])
    sheet = tradingMgr.ActiveSheet() #.NewSheet("TradeSheet") #Maybe use existing Trade Sheet or Template
    sheet.InsertObject(TempPort, 0)

'''================================================================================================
================================================================================================'''
#ael_variables =  [['midas_no','Midas Key','string',None,'',1,0]]
#def ael_main(dict): GetMidasTrades(dict['midas_no'])
def ael_main_ex(dict, params): GetMidasTrades(dict['midas_no'])
def Run(eii): acm.RunModuleWithParameters('MidasConstellation', acm.GetDefaultContext()) 
'''================================================================================================
do we actually want 
================================================================================================'''
def ButtonAction(invokationInfo): #FExtensionInvokationInfo

    trade = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedRowObjects()[0].Trade()
    if trade.Acquirer().Name() == "MIDAS DUAL KEY":
        midas_no =  invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedRowObjects()[0].Trade().OptionalKey()
        if midas_no != '':
            midas_no = midas_no.split('_')
            print midas_no    
            GetMidasTrades(midas_no[0] + '_' + midas_no[1])
    #else:
    #    print trade.YourRef() , 'ZZZZZZZZZZZZZ'
    #    if trade.YourRef() != '':
    #        GetMidasTrades(trade.YourRef(),False)        
            
'''================================================================================================
================================================================================================'''
def ButtonCreate(invokationInfo): #FExtensionInvokationInfo
    return True
    midas_no =  invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedRowObjects()[0].Trade().OptionalKey()
    if midas_no != '':
        return True
    else:
        return False
'''================================================================================================
def showStartStopButtons(invokationInfo):
    cell = invokationInfo.Parameter("Cell")
    if cell:
        try:
            rowObject = cell.RowObject()
            if(rowObject.IsKindOf(acm.FSalesOrder)):
                agent = rowObject.Agent()
                if agent:
                    strategy = acm.FAlgoTradingStrategy[str(agent.Class().DisplayName())]
                    return strategy and rowObject.IsKindOf(strategy.OrderClass())
        except Exception, e:
            print "An error occurred:", e
    return False
================================================================================================'''






