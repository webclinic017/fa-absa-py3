"""ABSA utilities for Deposits.

History
=======

2017-09-25 Vojtech Sidorin  Initial implementation; ABITFA-4912: Add function get_position_per_ins_and_prf.
"""

def get_position_per_ins_and_prf(trade):
    """Return the total position per instrument and portfolio.

    Note: This function is intended as a custom method for the FTrade class.
    """
    # Only trades with those statuses contribute to the total position.
    INCLUDE_TRADE_STATUSES = (
            "FO Confirmed",
            "BO Confirmed",
            "BO-BO Confirmed",
            )
    if trade.IsClone():
        original = trade.Original()
    elif trade.IsInfant():
        return 0.  # No position for infant trades.
    else:
        original = trade
    if original is None:
        return 0.
    if original.Instrument() is None:
        return 0.
    else:
        instrument = original.Instrument()
    total_position = 0.
    for trade_ in instrument.Trades():
        if trade_.Status() not in INCLUDE_TRADE_STATUSES:
            continue
        if trade_.Portfolio() is not trade.Portfolio():
            continue
        # NOTE: The nominal amount is negative for a deposit and positive for a
        # loan. The position field on deposits has the opposite sign.
        total_position -= trade_.Nominal()
    return total_position

