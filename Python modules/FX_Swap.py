"""Helper functions for extension attributes dealing with FXSwaps.

Authors: Lukas Paluzga, Jan Sinkora

"""

import acm, at

_acmserver = acm.FACMServer()

# Only 13th bit of the TradeProcess field is set == FX Swap.
FX_SWAP_TRADE_PROCESS = 2<<13


def _far_trade(trade):
    """Return far trade for an FX Swap trade."""
    return acm.FTrade.Select01('connectedTrade={0} and oid <> {0}'.format(
        trade.Oid()), 'More than one far trade found for near trade {0}'.format(trade.Oid()))


def _zero(curr):
    """Return denominated zero."""
    return _acmserver.DenominatedValue(0.0, curr, None)


def is_fx_swap(trade):
    """Check if the trade is a FX Swap."""
    return trade.Instrument().InsType() == 'Curr' and \
           trade.TradeProcess() == FX_SWAP_TRADE_PROCESS


def daily_interest(ntrade, today_date, currency):
    """Return daily interest of the fx swap."""
    return calc_fx_swap_interest(ntrade, today_date, currency, 'interest')


def nominal_with_interest(ntrade, today_date, currency):
    """Return notional value of an FX Swap trade with interest."""
    return calc_fx_swap_interest(ntrade, today_date, currency, 'nominal_with_interest')


def calc_fx_swap_interest(ntrade, today_date, currency, calc_type):
    """Calculate FX Swap interest or nominal with interest.

    Switch functionality according to the calc_type, which can be one of:
        a) interest
        b) nominal_with_interest

    The currency parameter specifies which of the two currencies in the swap
    is this to be calculated with.

    """

    allowed_types = ('interest', 'nominal_with_interest')
    if calc_type not in allowed_types:
        raise ValueError("Wrong calculation type '{0}'.".format(calc_type))

    if currency.InsType() != 'Curr':
        raise ValueError('Invalid instrument, expected a currency.')

    if not is_fx_swap(ntrade):
        return None

    ftrade = _far_trade(ntrade)
    if not ftrade:
        return _zero(currency)

    # Convert the dates.
    near_day = at.date_to_datetime(ntrade.ValueDay())
    far_day = at.date_to_datetime(ftrade.ValueDay())
    today = at.date_to_datetime(today_date)

    near_currency = ntrade.Instrument()
    far_currency = ntrade.Currency()

    # Get the near and far 'cashflows' of the swap.
    near_nv_curr1 = ntrade.Nominal()
    near_nv_curr2 = -near_nv_curr1 * ntrade.Price()

    far_nv_curr1 = ftrade.Nominal()
    far_nv_curr2 = -far_nv_curr1 * ftrade.Price()

    # Check which of the values is needed.
    if currency == near_currency:
        near_nv = near_nv_curr1
        far_nv = far_nv_curr1
    elif currency == far_currency:
        near_nv = near_nv_curr2
        far_nv = far_nv_curr2
    else:
        cp = ntrade.CurrencyPair()
        raise ValueError('Invalid currency: {0}. Expected {1} or {2}.'.format(
            currency.Name(), cp.Currency1().Name(), cp.Currency2().Name()))

    if calc_type == 'interest':
        result = calc_daily_interest(near_day, far_day, today, near_nv, far_nv, currency)
    elif calc_type == 'nominal_with_interest':
        result = calc_nominal_with_interest(ntrade, near_day, far_day, today,
                near_nv, far_nv, currency)

    return _acmserver.DenominatedValue(result, currency, None)


def calc_daily_interest(near_day, far_day, today, near_nv, far_nv, currency):
    """Calculate the nominal value of daily interest."""
    if far_day <= today or near_day > today:
        return _zero(currency)

    total_days = at.days_between(near_day, far_day, at.DAYCOUNT_ACT_365)
    return (far_nv + near_nv) / total_days


def calc_nominal_with_interest(ntrade, near_day, far_day, today, near_nv, far_nv, currency):
    """Calculated the nominal value of the trade with daily interest."""
    if far_day <= today:
        return far_nv
    else:
        elapsed_days = at.days_between(near_day, today, at.DAYCOUNT_ACT_365) + 1
        return -near_nv + (daily_interest(ntrade, today, currency).Number() * elapsed_days)

