import acm
import at_calculation_space as acs


trades = acm.FStoredASQLQuery['returned_quantity_trades'].Query().Select()

for trade in trades:
    parent_trade = trade.TrxTrade()

    parent_qty = acs.calculate_value('FTradeSheet', parent_trade, 'Quantity')
    trade_qty = acs.calculate_value('FTradeSheet', trade, 'Quantity')
    returned_qty = parent_qty - trade_qty

    trade.AdditionalInfo().SL_ReturnedQty(returned_qty)
    trade.Commit()

