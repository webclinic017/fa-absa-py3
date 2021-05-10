import acm


def pswap_execution_fee(trade, start_date, end_date):
    """Return execution fee for a trade."""
    fee = 0.0    
    trade_date = acm.Time.DateFromTime(trade.TradeTime())
    if start_date < trade_date <= end_date:
        trade_value = abs(trade.Price() * trade.Quantity())
        exec_rate = trade.Portfolio().AdditionalInfo().CFD_Fee_Percentage()
        if exec_rate:
            fee = exec_rate * trade_value / 100 / 100
    return -1.0 * fee


def pswap_execution_fee_total(trades, start_date, end_date):
    """Return execution fee for a set of trades."""
    fee = 0.0
    for trade in trades:
        fee += pswap_execution_fee(trade, start_date, end_date)
    return fee
