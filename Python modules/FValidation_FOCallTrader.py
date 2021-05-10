"""Validation rules for users with profile FO Call Trader.

History
=======
2015-02-13 Vojtech Sidorin  ABITFA-3354: Refactor rules 85, 53, 54 from deprecated modules.
2015-02-20 Vojtech Sidorin  ABITFA-3403: Fix rule 54b-1.
2015-08-11 Vojtech Sidorin  ABITFA-3732: Fix message in rule 54a.
2015-08-20 Vojtech Sidorin  ABITFA-3743: Include rule numbers in messages.
2016-08-02 Bushy Ngwako     ABITFA-2414: For MM Retro Accounts (Call Accounts).
2019-04-18 Cuen Edwards     FAOPS-425: Change to only restrict instrument update if a column value has actually changed.
"""

import acm

from FValidation_core import (validate_entity,
                              AccessValidationError)

from SAGEN_IT_TM_Column_Calculation import get_TM_Column_Calculation


@validate_entity("Trade", "Update")
def restrict_trade_update(trade, operation):
    """Rule 53: Restrict update of confirmed trades for FO Call Traders.

    Forbid users with profile "FO Call Trader" from updating confirmed
    trades with the following exceptions:
        (1) Users with component "Book Security Loan" can update trades
            on Security Loan.
        (2) Trades on Deposit with a "Call Fixed Adjustable" leg can be
            updated.
        (3) "Cash Payment" trades with InsOverride add_info set to
            Interest Claims
    """

    from FValidation_Utils import (user_has_profile,
                                   is_allowed)

    # Trade statuses this rule applies to.
    CONFIRMED_STATUSES = ["BO Confirmed", "BO-BO Confirmed"]

    original_trade = trade.original()
    original_instrument = original_trade.insaddr
    original_legs = original_instrument.legs()
    user = acm.User()

    # Apply the rule only to users with profile "FO Call Trader".
    if not user_has_profile(user, "FO Call Trader"):
        return

    # Apply only to given trade statuses.
    if original_trade.status not in CONFIRMED_STATUSES:
        return

    # (1) Trade on Security Loan.
    if (original_instrument.instype == "SecurityLoan" and
            is_allowed(user, "Book Security Loan")):
        return

    # (2) Trade on Deposit.
    if (original_instrument.instype == "Deposit" and original_legs and
            original_legs[0].type == "Call Fixed Adjustable"):
        return

    subtype = get_TM_Column_Calculation(
        temp=None,
        context='Standard',
        sheet_type='FTradeSheet',
        obj_id=original_trade.trdnbr,
        obj_type='Trade',
        column_id='fxSubTypeDetail',
        currency=None,
        vector_column=0,
        start_Date=None,
        end_Date=None,
    )

    # (3) Trade on CashPayment
    if ( subtype == "Cash Payment" and
            original_trade.add_info('InsOverride') == "Interest Claims" ) :
        return

    # Forbid otherwise.
    msg = ("FV53: You are not allowed to amend trade {trdnbr}.\n"
           "Users with profile 'FO Call Trader' can only update confirmed "
           "trades:\n"
           "(1) on Security Loans, if they have component "
           "'Book Security Loan'; or\n"
           "(2) on Deposit with a 'Call Fixed Adjustable' leg. or\n"
           "(3) Cash Payment trades with InsOverride add_info set to Interest Claims."
           .format(trdnbr=original_trade.trdnbr))
    raise AccessValidationError(msg)


@validate_entity("Instrument", "Update")
def restrict_instrument_update(instrument, operation):
    """Rule 54a: Restrict update of instruments for FO Call Traders.

    Forbid users with profile "FO Call Trader" from updating instruments
    with confirmed trades with the following exceptions:
        (1) Users with component "Book Security Loan" can update Security
            Loan if they don't change the underlying instrument and ref
            price.
        (2) Deposit with a "Call Fixed Adjustable" leg can be updated.
    """

    from FValidation_Utils import (user_has_profile,
                                   is_allowed,
                                   get_updated_columns,
                                   has_trades_of_statuses)

    # The rule applies only to instruments with confirmed trades.
    CONFIRMED_STATUSES = ["BO Confirmed", "BO-BO Confirmed"]

    original_instrument = instrument.original()
    original_legs = original_instrument.legs()
    user = acm.User()

    # Apply the rule only to users with profile "FO Call Trader".
    if not user_has_profile(user, "FO Call Trader"):
        return

    # Apply only to instruments with trades in relevant statuses.
    if not has_trades_of_statuses(original_instrument, CONFIRMED_STATUSES):
        return

    # Apply only if something has changed.
    if not get_updated_columns(instrument):
        return

    # (1) Allow on Security Loan if the user is allowed to Book Serucity Loand
    # and is not changing the underlying instrument or ref price.
    if (original_instrument.instype == "SecurityLoan" and
            is_allowed(user, "Book Security Loan")):
        if (original_instrument.und_insaddr is instrument.und_insaddr and
                original_instrument.ref_price == instrument.ref_price):
            return
        else:
            msg = ("FV54a-1: You are not allowed to amend the underlying "
                   "instrument on the confirmed Security Loan '{name}'."
                   .format(name=instrument.insid))
            raise AccessValidationError(msg)

    # (2) Allow on Deposit with a Call Fixed Adjustable leg.
    if (original_instrument.instype == "Deposit" and original_legs and
            original_legs[0].type == "Call Fixed Adjustable"):
        return

    # Forbid otherwise.
    msg = ("FV54a: You are not allowed to update instrument '{name}'. "
           "It has confirmed trades."
           .format(name=original_instrument.insid))
    raise AccessValidationError(msg)


@validate_entity("Leg", "Update")
def restrict_leg_update(leg, operation):
    """Rule 54b: Restrict leg update for FO Call Traders.

    Forbid users with profile "FO Call Trader" from updating legs on
    instruments with confirmed trades with the following exceptions:
        (1) Leg of type "Call Fixed Adjustable" on Deposit can be updated.
        (2) Users with component "Book Security Loan" can update legs on
            Security Loans if they do not update fieds:
                fixed_rate, start_day
    """

    from FValidation_Utils import (user_has_profile,
                                   has_trades_of_statuses,
                                   is_allowed)

    CONFIRMED_STATUSES = ["BO Confirmed", "BO-BO Confirmed"]
    original_leg = leg.original()
    original_instrument = original_leg.insaddr
    user = acm.User()

    # Apply only to users with profile "FO Call Trader".
    if not user_has_profile(user, "FO Call Trader"):
        return

    # Apply only to legs on instrument with confirmed trades.
    if not has_trades_of_statuses(original_instrument, CONFIRMED_STATUSES):
        return

    # (1) Leg on Deposit.
    if original_instrument.instype == "Deposit":
        if original_leg.type == "Call Fixed Adjustable":
            # Allow amending Call Fixed Adjustable leg on Deposit.
            return
        else:
            # Forbid amending any other leg types.
            msg = ("FV54b-1: You are not allowed to amend a leg that is not "
                   "of type Call Fixed Adjustable on a confirmed Deposit.")
            raise AccessValidationError(msg)

    # (2) Leg on Security Loan.
    if (original_instrument.instype == "SecurityLoan" and
            is_allowed(user, "Book Security Loan")):
        allow = False
        msg = ("FV54b-2: You are not allowed to amend the {field} on a "
               "confirmed Security Loan.")
        field = ""
        if original_leg.fixed_rate != leg.fixed_rate:
            field = "Fee"
        elif original_leg.start_day != leg.start_day:
            field = "Start Day"
        else:
            allow = True
        if allow:
            return
        else:
            raise AccessValidationError(msg.format(field=field))

    # Forbid otherwise.
    msg = ("FV54b: You are not allowed to amend a leg on an instrument "
           "with confirmed trades.")
    raise AccessValidationError(msg)


@validate_entity("CashFlow", "Delete")
def restrict_cashflow_deletion(cashflow, operation):
    """Rule 85: Restrict cashflow deletion for FO Call Traders.

    Forbid users with profile "FO Call Trader" from deleting cashflows with
    the following exceptions:
        (1) Users with component "Book Security Loan" can delete cashflows
            on Security Loans.
        (2) Cashflows on non-open-ended instruments (open_end == "None") with
            only Simulated trades can be deleted.
    """

    from FValidation_Utils import (user_has_profile,
                                   is_allowed,
                                   has_all_trades_of_statuses)

    instrument = cashflow.legnbr.insaddr
    user = acm.User()

    # Allow the deletion if the user has not profile "FO Call Trader".
    if not user_has_profile(user, "FO Call Trader"):
        return

    # (1) Allow users with component "Book Security Loan" to delete cashflows
    #     on Security Loans.
    if (instrument.instype == "SecurityLoan" and
            is_allowed(user, "Book Security Loan")):
        return

    # (2) Allow on non-open-ended instruments with only simulated trades.
    if (instrument.open_end == "None" and
            has_all_trades_of_statuses(instrument, ["Simulated"])):
        return

    # Forbid otherwise.
    msg = ("FV85: You are not allowed to delete cashflows. "
           "Users with profile 'FO Call Trader' can only delete cashflows:\n"
           "(1) on Security Loans, if they have component "
           "'Book Security Loan'; or\n"
           "(2) on non-open-ended instruments with only Simulated trades.")
    raise AccessValidationError(msg)
