from FRoutingCommon import route
import acm
from at import TP_FX_FORWARD
from FXUtils import CommitInTransaction
'''================================================================================================
================================================================================================'''
def CreateClosingTrade(trade, commit):

    if trade.IsFxSwap(): 
        NearLeg  = trade.FxSwapNearLeg()
        closing_far_leg = trade.Clone()
        closing_far_leg.Quantity(-1 * closing_far_leg.Quantity() )
        closing_far_leg.Premium(-1 * closing_far_leg.Premium() )
        closing_far_leg.Type('Closing')
        closing_far_leg.ContractTrdnbr(trade.Oid())
      
        if NearLeg.ValueDay() > acm.Time.DateToday():  #have to close bothe legs of swap.
            closing_near_leg = NearLeg.Clone()
            closing_near_leg.Quantity(-1 * closing_near_leg.Quantity() )
            closing_near_leg.Premium(-1 * closing_near_leg.Premium() )
            closing_near_leg.Type('Closing')
            closing_near_leg.ContractTrdnbr(NearLeg.Oid())
            ClosingTrades = [closing_near_leg, closing_far_leg]
        else:
            closing_far_leg.TradeProcess(TP_FX_FORWARD)
            ClosingTrades = [closing_far_leg]

    else:
        closing_trade = trade.Clone()
        closing_trade.Quantity(-1 * closing_trade.Quantity() )
        closing_trade.Type('Closing')
        closing_trade.ContractTrdnbr(trade.Oid())
        ClosingTrades = [closing_trade]

    if commit == True: 
        CommitInTransaction(ClosingTrades)
        
    return ClosingTrades

'''================================================================================================
================================================================================================'''
def Reversal(trade,routingparams = None,commit = False,rebook_trade = None,Route = True):
    
    assert trade.Instrument().InsType() == 'Curr'
    Constellation = acm.FArray()
    if trade.GroupTrdnbr() != None:
        for t in acm.FTrade.Select('groupTrdnbr = %d' % trade.Oid()): # we only pass far trades.
            if t.IsFxSwapNearLeg() != True:
                Constellation.AddAll(CreateClosingTrade(t, commit))
    else:
        if trade.IsFxSwapNearLeg():
            trade = trade.FxSwapFarLeg()
        Constellation.AddAll(CreateClosingTrade(trade, commit))

    if rebook_trade != None and Route == True:
        Constellation.AddAll(route(rebook_trade, routingparams, commit))  #
        
    return Constellation
'''================================================================================================
print acm.FTrade[70434646].IsFxSwapFarLeg()
Const = Reversal(acm.FTrade[70434646],None,True,None)
acm.StartApplication("Instrumnet Definition",Const.At(0))
================================================================================================'''
