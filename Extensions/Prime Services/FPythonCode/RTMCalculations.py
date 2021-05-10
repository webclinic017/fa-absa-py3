
import acm


calculation_space = acm.FStandardCalculationsSpaceCollection()


def execution_fee(trade):
    """Custom execution fee."""
    return -2.5 * abs(trade.Price() / 100 * trade.Quantity()) / 100 / 100


def daily_cash(trade, date):
    """Settled cash excluding dividendes and with custom fee applied."""
    cash = 0.0
    if trade.Status() in ["Simulated", "Void"]:
        return cash
    for money_flow in trade.MoneyFlows(date, date):
        # Skip settled dividends
        if money_flow.Type() in ("Dividend", "Security Nominal", "None"):
            continue
        # Use custom exec fee calculation
        if money_flow.Type() == "Broker Fee":
            cash += execution_fee(trade)
        else:
            cash += money_flow.Calculation().Projected(calculation_space).Number()
    return cash


def invested_premium(trade, date):
    """Invested premium amount."""
    premium = 0.0
    trade_date = acm.Time.DateFromTime(trade.TradeTime())
    if date >= trade_date and date < trade.ValueDay():
        return -1 * trade.Premium()
    else:
        return 0.0
