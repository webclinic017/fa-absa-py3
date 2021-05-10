
import acm

def get_collateral_trades(trade):
    connects = acm.FTrade.Select("connectedTrdnbr = %s" %trade.Oid())
    # exclude self-refferenced trades, voided trades and non-collateral trades
    collaterals = [trade for trade in connects if trade.ConnectedTrdnbr() != trade.Oid() and trade.Status() != 'Void' and trade.TradeCategory() == 'Collateral']
    return collaterals
    
