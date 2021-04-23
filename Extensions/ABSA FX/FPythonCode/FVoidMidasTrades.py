
'''================================================================================================
'================================================================================================'''
import acm
for trade in acm.FTradeSelection['MIDAS_delete'].Snapshot():

    if trade.IsSwap():
        if trade.IsFxSwapNearLeg() == True:

            try:            
                acm.BeginTransaction()
                trade.Status('Void')
                FarTrade = acm.FTrade[trade.ConnectedTrdnbr()]
                FarTrade.Status('Void')
                acm.CommitTransaction()
            except: 
                acm.AbortTransaction()
                print('Could not commit transaction')
                pass
    else:
        trade.Status('Void')
        trade.Commit()
'''================================================================================================
'================================================================================================'''
