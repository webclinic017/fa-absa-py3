import ael  
import acm
'''================================================================================================
Description :

Enhancements:
    * Add YourRef and the Additional Info "Source Trade Id"
    * Filters , maybe we should only get FX Trades  ?
    
================================================================================================'''
ael_gui_parameters = {'runButtonLabel': '&&Run',
                      'hideExtraControls': True,
                      'windowCaption': 'Find Midas Trades',
                      'closeWhenFinished': True}
'''================================================================================================
================================================================================================'''
ael_variables = [
    ('midasCode', 'Midas Code', 'string', None, '', 1, 0),
    ('template', 'Trade Sheet Template', acm.FTradingSheetTemplate, [ts.Name() for ts in acm.FTradingSheetTemplate.Select('').SortByProperty('Name')], 'FX_AggregationView', 1, 0),
    ]
'''================================================================================================
================================================================================================'''
def ael_main(dict):
    
    midasCode = dict['midasCode']
    key = midasCode + "%"  
    sqlStr = """ 
    select 
        trdnbr
    from 
        trade t,
        instrument i
    where 
        i.insaddr = t.insaddr
    and i.instype = 21    
    and (t.optional_key like '%s' or t.your_ref = '%s')   
    """ % (key, midasCode)
    
    TempPort = acm.FAdhocPortfolio()
    TempPort.Name(midasCode)
    tradeIds = ael.dbsql(sqlStr)
    for t in tradeIds[0]:
        TempPort.Add(acm.FTrade[t[0]])
    
    tradingMgr = acm.StartApplication('Trading Manager', dict['template'])
    sheet = tradingMgr.ActiveSheet()
    sheet.InsertObject(TempPort, 0)
'''================================================================================================
================================================================================================'''
def RunModule(eii):
    acm.RunModuleWithParameters('MidasCodeSearch', acm.GetDefaultContext())
