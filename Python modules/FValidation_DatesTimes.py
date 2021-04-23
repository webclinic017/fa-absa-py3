"""Rules for date and time fields, e.g. Value Day, Expiry Day, or Trade Time.

Please consult the Developer's Guide before changing the code.  The guide can
be found at
<http://confluence.barcapint.com/display/ABCAPFA/FValidation+Developer's+Guide>.


History
=======
2015-11-06 Vojtech Sidorin  ABITFA-3910 Initial implementation; add rule FV126; add refactored rules FV14 and FV15.
"""

import ael

from FValidation_core import (validate_entity,
                              DataValidationError)


@validate_entity("Trade", "Insert")
@validate_entity("Trade", "Update")
def fv14_check_dates_times_on_funding_desks_trades(entity, operation):
    """FV14: Check dates and times on Funding Desk's trades.

    Forbid trades with Acquire Day < Trade Time <= Value Day, where
    the Acquirer is Funding Desk.
    """
    FUNDING_DESK_OID = 2247
    trade = entity
    acquirer = trade.acquirer_ptynbr
    if acquirer and acquirer.ptynbr == FUNDING_DESK_OID:
        trade_time = ael.date_from_time(trade.time)
        value_day = trade.value_day
        acquire_day = trade.acquire_day
        if acquire_day < trade_time <= value_day:
            msg = ("FV14: Trades with Acquire Day < Trade Time <= Value Day "
                   "are forbidden on the Funding Desk.")
            raise DataValidationError(msg)


@validate_entity("Trade", "Insert")
@validate_entity("Trade", "Update")
def fv15_ensure_consistent_dates_times_on_currswaps(entity, operation):
    """FV15: Ensure consistent dates and times on Currency Swap trades.

    For Currency Swap trades, check if Value Day == Acquire Day == Trade Time.
    If not, set Value Day = Trade Time, and Acquire Day = Trade Time.
    """
    trade = entity
    instrument = trade.insaddr
    if instrument.instype == "CurrSwap":
        trade_time = ael.date_from_time(trade.time)
        if not (trade.value_day == trade.acquire_day == trade_time):
            print("FV15: Setting Value Day = Acquire Day = Trade Time.")
            trade.value_day = trade_time
            trade.acquire_day = trade_time


@validate_entity("Trade", "Insert")
@validate_entity("Trade", "Update")
def fv126_check_value_day(entity, operation):
    """FV126: Check Value Day.

    For an FX Swap/FX Cash, the Value Day must not be greater than the
    Acquire Day.
    """
    trade = entity
    instrument = trade.insaddr
    if instrument.instype in ("FxSwap", "Curr"):
        if trade.value_day > trade.acquire_day:
            msg = ("FV126: Cannot have a Value Day greater than the Acquire "
                   "Day on an FX Swap/FX Cash.")
            raise DataValidationError(msg)
