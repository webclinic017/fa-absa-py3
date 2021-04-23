import acm 
from at import TP_SWAP_NEAR_LEG, TP_SWAP_FAR_LEG, TP_FX_SPOT
import FRoutingCommon
from FRoutingExtensions import Debug, DB
'''===================================================================================================
==================================================================================================='''
def CommitInTransaction(objects):
    try:
        acm.BeginTransaction()
        for object in objects:
            object.Commit()
        acm.CommitTransaction()
    except Exception, e:
        print 'Abort Transaction',  str(e)
        acm.AbortTransaction()

'''===================================================================================================
==================================================================================================='''
@Debug(DB.TIME)
def RunTest(dict):

    Commit = True

    currencyPair = acm.FCurrencyPair[dict['CP']]
    valueDay = currencyPair.SpotDate( acm.Time.TimeNow() ) if dict['VD'] == 'SPOT' else acm.Time.DateAdjustPeriod( acm.Time.TimeNow(), dict['VD'] )
    trade = acm.FTrade()
    trade.RegisterInStorage()
    trade.TradeTime( acm.Time.TimeNow() )
    trade.AcquireDay(  valueDay )
    trade.ValueDay ( trade.AcquireDay() )
    trade.Instrument( currencyPair.Currency1() )
    trade.Currency( currencyPair.Currency2() )
    trade.Acquirer( dict['AC'] )
    trade.Counterparty( dict['CY'] )
    trade.Portfolio( dict['PF'] )
    trade.Trader( dict['TR'] )
    trade.Price( 11.1 )
    trade.ReferencePrice( 11 )
    trade.Quantity( 100 )
    trade.UpdatePremium( True )
    trade.BaseCostDirty( dict['BC'] )
    trade.TradeProcess( dict['TP'])
    trade.OptionalKey( '{0}|{1}|{0}'.format(acm.Time.TimeOnlyMs().replace(':', ''), dict['SR']))
    trade.Status("Simulated")
    
    if Commit == True: 
        CommitInTransaction([trade])
        #CommitInTransaction([near,far])
        
    result = FRoutingCommon.route(trade, dict['AI'], Commit)
    #print result[0].ArtifactsToBeCommitted()
    #print result[0].ParentTrade()
    #print FRoutingCommon.find_routing_instruction(trade)

    print trade
    #ConnectedTradesViewer.insdefStartApplication 
    
'''===================================================================================================
==================================================================================================='''
#RunTest({'TP':TP_FX_SPOT,'CP':'USD/ZAR','VD':'SPOT','AC':'FX SPOT','CY':'TEST','PF':'ROUT_INTERBANK_BRX','SR':'BRX','TR':'COUSINRO','BC':'100','AI':{}})
RunTest({'TP':TP_FX_SPOT,'CP':'USD/ZAR','VD':'SPOT','AC':'ABSA CAPITAL SALES','CY':'TEST','PF':'ROUT_ABC','SR':'BII','TR':'ATS','BC':'100','AI':{'B2BSptMktPr':11.9,'B2BMktPr':11.9}})









