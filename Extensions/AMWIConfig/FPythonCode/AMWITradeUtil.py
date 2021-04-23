"""
    AMWITradeUtil
"""
import FFpMLConfigParamReader
import acm

from AMWICommon import log_debug, log_error
from AMWIIdentity import find_trades_by_markitwire_id

# Code that acts on this has no way to communicate
# with code that detects this issue, so we have to
# use a global.
IS_PROBLEM_BASIS_SWAP = False


def _generate_payment_key(payment, include_amount=True):
    amount = payment.Amount() if include_amount else 0.0
    return "%s:%s %.02f:%s:%s" % (payment.Type(),
                                  payment.Currency().Name(),
                                  amount,
                                  payment.PayDay(),
                                  payment.Party().Name())


def _generate_pay_map(trade):
    r = {}
    for payment in trade.Payments():
        r[_generate_payment_key(payment, False)] = payment

    return r


# Because we move or alter payments that get resent in later messages, we
# often need to check for duplicates. If we are adding a payment that already
# exists, delete the new one and update the existing one.
def _keep_or_update_payment(pay_map, trade, new_payment):
    pay_key = _generate_payment_key(new_payment, False)
    if pay_key in pay_map:
        payments = trade.Payments()
        payment = pay_map[pay_key]
        # If fee already exists, update amount and remove original.
        log_debug("Updating trade %i, setting %s amount to %.2f" % (trade.Oid(),
                                                                    payment.Type(),
                                                                    new_payment.Amount()))
        payment.Amount(new_payment.Amount())

        i = payments.IndexOf(new_payment)
        if i < 0:
            raise Exception("Attempting to remove a payment that is not there on trade %i" % trade.Oid())

        payments.RemoveAt(i)
        if payment.IsRegisteredInStorage():
            payment.Unsimulate()


def get_default_party():
    config_parameters = FFpMLConfigParamReader.FFpMLConfigParamReader()
    return acm.FParty[config_parameters.get_paramvalue("FSWML_DEFAULT_COUNTERPARTY")]


def set_instrument_start(instrument, start_date):
    instrument.StartDate(start_date)
    for leg in instrument.Legs():
        leg.StartDate(start_date)


def delete_addinfos(trade, addinfo_names):
    aip = trade.AddInfos()
    for i in reversed(list(range(0, aip.Size()))):
        ai = aip[i]
        if ai.AddInf().FieldName() in addinfo_names:
            log_debug("Removing addinfo %s=%s on trade %i" % (ai.AddInf().FieldName(), ai.FieldValue(), trade.Oid()))
            aip.RemoveAt(i)
            if ai.IsRegisteredInStorage():
                ai.Unsimulate()


def find_closing_trades_by_markitwire_id(mw_id, ignore_trade_ids, match_version=None):
    return find_trades_by_markitwire_id("%s_closing" % str(mw_id), ignore_trade_ids, match_version)


def find_payments_by_markitwire_id(mw_id, payment_types, ignore_trade_ids):
    r = []
    for trade in find_trades_by_markitwire_id(mw_id, ignore_trade_ids):
        r.extend(find_payments_by_type(trade, payment_types))

    for trade in find_closing_trades_by_markitwire_id(mw_id, ignore_trade_ids):
        r.extend(find_payments_by_type(trade, payment_types))

    return r


def delete_payments_by_date(trade, before_date):
    payments = trade.Payments()
    for i in reversed(list(range(0, payments.Size()))):
        payment = payments[i]
        if payment.PayDay() > before_date:
            log_debug("Removing payment on %i: %s (%s) %.2f" % (trade.Oid(),
                                                                payment.Type(),
                                                                payment.PayDay(),
                                                                payment.Amount()))
            payments.RemoveAt(i)
            if payment.IsRegisteredInStorage():
                payment.Unsimulate()


def delete_payments_by_type(trade, payment_types, before_date=None, text_filter=None):
    payments = trade.Payments()
    for i in reversed(list(range(0, payments.Size()))):
        payment = payments[i]
        if payment.Type() in payment_types:
            if not before_date or payment.PayDay() < before_date:
                if not text_filter or payment.Text() == text_filter:
                    log_debug("Removing payment on %i: %s (%s) %.2f" % (trade.Oid(),
                                                                        payment.Type(),
                                                                        payment.PayDay(),
                                                                        payment.Amount()))
                    payments.RemoveAt(i)
                    if payment.IsRegisteredInStorage():
                        payment.Unsimulate()


def delete_matching_payments(trade, payments_to_match):
    r = []
    pay_map = {}
    for payment in payments_to_match:
        pay_map[_generate_payment_key(payment)] = payment

    payments = trade.Payments()
    for i in reversed(list(range(0, payments.Size()))):
        key = _generate_payment_key(payments[i])
        if key in pay_map:
            log_debug("Removing payment %s from trade %i" % (key, trade.Oid()))
            payments.RemoveAt(i)
            if payment.IsRegisteredInStorage():
                payment.Unsimulate()

    return r


def delete_duplicate_payments_on_trade(trade):
    ignore_ids = [trade.Oid(), trade.ConnectedTrdnbr()]

    existing_payments = find_payments_by_markitwire_id(trade.AdditionalInfo().CCPmiddleware_id(),
                                                       ["Termination Fee"],
                                                       ignore_ids)

    delete_matching_payments(trade, existing_payments)


def alter_payment_type(trade, from_type, to_type):
    payments = trade.Payments()
    pay_map = _generate_pay_map(trade)
    for i in reversed(list(range(0, payments.Size()))):
        payment = payments[i]
        if payment.Type() == from_type:
            log_debug("Altering payment type from '%s' to '%s' on trade %i" % (from_type,
                                                                               to_type,
                                                                               trade.Oid()))
            payment.Type(to_type)
            _keep_or_update_payment(pay_map, trade, payment)


def move_payments_by_type(from_trade, to_trade, payment_types):
    payments = from_trade.Payments()
    pay_map = _generate_pay_map(to_trade)
    for i in reversed(list(range(0, payments.Size()))):
        payment = payments[i]
        if payment.Type() in payment_types:
            log_debug("Moving payment from %i to %i: %s (%s) %.2f" % (from_trade.Oid(),
                                                                      to_trade.Oid(),
                                                                      payment.Type(),
                                                                      payment.PayDay(),
                                                                      payment.Amount()))
            new_payment = to_trade.CreatePayment()
            new_payment.Apply(payment)
            _keep_or_update_payment(pay_map, to_trade, new_payment)

            payments.RemoveAt(i)
            if payment.IsRegisteredInStorage():
                payment.Unsimulate()


def reverse_payments(trade, exclude_types):
    for payment in trade.Payments():
        if payment.Type() not in exclude_types:
            log_debug("Reversing payment on %i: %s (%s) %.2f" % (trade.Oid(),
                                                                 payment.Type(),
                                                                 payment.PayDay(),
                                                                 payment.Amount()))
            payment.Amount(-1.0 * payment.Amount())


def find_payments_by_type(trade, payment_types):
    r = []
    for payment in trade.Payments():
        if payment.Type() in payment_types:
            r.append(payment)

    return r


def roll_date_to_next_month(date, to_day=-1, currency=None):
    s = date.split("-")
    if to_day < 0:
        to_day = int(s[2])

    new_date = "%4i-%02i-%02i" % (int(s[0]), int(s[1]), to_day)
    new_date = acm.Time.DateAddDelta(new_date, 0, 1, 0)

    if currency:
        calendar = currency.Calendar()
        if calendar.IsNonBankingDay(None, None, new_date):
            return calendar.AdjustBankingDays(new_date, 1)

    return new_date


def set_trade_dates(trade, trade_date=None, trade_datetime=None):
    if not trade_datetime:
        if trade_date:
            trade_datetime = "%s %s" % (trade_date, acm.Time.TimeNow()[11:])
        else:
            trade_datetime = acm.Time.TimeNow()

    if not trade_date:
        trade_date = acm.Time.AsDate(trade_datetime)

    log_debug("Setting dates on trade %i: %s -- %s" % (trade.Oid(), trade_date, trade_datetime))
    trade.TradeTime(trade_datetime)
    trade.ValueDay(trade_date)
    trade.AcquireDay(trade_date)


def is_problem_basis_swap(trade):
    global IS_PROBLEM_BASIS_SWAP

    IS_PROBLEM_BASIS_SWAP = False

    instrument = trade.Instrument()

    if instrument.InsType() != "CurrSwap":
        return False

    # All the legs will have a nominal factor of 1 on a problem XCcy swap.
    for leg in instrument.Legs():
        if leg.NominalFactor() != 1.0:
            return False

    IS_PROBLEM_BASIS_SWAP = True

    return True


def _get_locked_unlocked_leg(instrument):
    free_leg = None
    locked_leg = None
    for leg in instrument.Legs():
        if leg.IsLocked():
            locked_leg = leg
        else:
            free_leg = leg

    return locked_leg, free_leg


def unfix_basis_swap_resets(instrument, from_date):
    if IS_PROBLEM_BASIS_SWAP and instrument.InsType() == "CurrSwap":
        locked_leg, free_leg = _get_locked_unlocked_leg(instrument)

        amended = list()

        # Only a basis swap will have a free leg
        if locked_leg and free_leg:
            for cashflow in free_leg.CashFlows():
                for reset in cashflow.Resets():
                    if reset.ResetType() in ("Nominal Scaling", "Return"):
                        if reset.IsFixed() and reset.Day() > from_date:
                            print("Clearing reset: %i" % reset.Oid())
                            reset.FixFixingValue(None)
                            reset.IsFixedAt(None)

                            amended.append(reset)

        return amended


def fix_basis_swap(trade):
    locked_leg, free_leg = _get_locked_unlocked_leg(trade.Instrument())

    if not free_leg:
        log_error("Ignoring basis swap - no free leg")
    elif not locked_leg:
        log_error("Ignoring basis swap - no locked leg?!?")
    else:
        lock_ccy = locked_leg.Currency()
        ccy_pair = lock_ccy.CurrencyPair(free_leg.Currency())

        if ccy_pair.Currency2().Name() == free_leg.Currency().Name():
            rate = ccy_pair.SpotPrice(locked_leg.StartDate(), False)
        else:
            # Invert rate
            rate = ccy_pair.SpotPrice(locked_leg.StartDate(), True)

        free_leg.NominalFactor(rate)
        free_leg.InitialIndexValue(rate)
        free_leg.GenerateCashFlowsFromDate(free_leg.StartDate())

        unfix_basis_swap_resets(trade.Instrument(), acm.Time.DateToday())
