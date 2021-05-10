import acm


cs = acm.FCalculationSpace('FTradeSheet')


def get_regulatory_notional(trade):
    if trade.IsFxSwap() and (trade.Instrument().InsType() == 'Curr' or 
            trade.Instrument().InsType() == 'Fx Rate'):
        trade = trade.ConnectedTrade()
    return float(cs.CalculateValue(trade, 'Regulatory Notional'))


def get_notional_override_currency(trade):
    val_params = acm.GetFunction('mappedValuationParameters', 0)
    return val_params().Parameter().AccountingCurrency()


def get_notional_override(trade):
    return trade.AdditionalInfo().Notional_Override()


def set_notional_override(trade, enable):
    trade.AdditionalInfo().Notional_Override(enable)
    trade.AdditionalInfo().Notional_Value(0.0)


def get_notional_override_value(trade):
    return trade.AdditionalInfo().Notional_Value()


def set_notional_override_value(trade, value):
    if get_notional_override(trade):
        trade.AdditionalInfo().Notional_Value(value)
