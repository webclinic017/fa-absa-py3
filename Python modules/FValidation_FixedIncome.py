"""FValidation rules related to Fixed Income instruments.

History
=======

2014-11-20 Vojtech Sidorin   CHNG0002443195 Initial implementation, add rule 16
2014-12-04 Vojtech Sidorin   CHNG0002493866 Rule 16: Add handling bonds without spot price
2015-01-22 Ondrej Bahounek   CHNG0002584851 Rule 58: Remove BasketRepo/Reverse from the simulated list
2015-03-23 Vojtech Sidorin   FXFA-262 Move rule 58 to FValidation_General.
2015-03-23 Vojtech Sidorin   Introduce new naming convention: Rule functions start with 'rule_##'.
2015-08-20 Vojtech Sidorin   ABITFA-3743: Include rule numbers in messages.
"""

import ael
import acm
from FValidation_core import (ValidationError,
                              validate_entity,
                              show_validation_warning)

def _get_bond_fair_price(bond):
    """Return fair price for bond.

    Arguments:
    bond -- instrument (ael entity).  The function doesn't constrain
            the instrument type.  It was however tested with Bond and
            IndexLinkedBond.

    The fair price is first looked in the instrument spread yield curve
    ZAR-CORPBONDS-SPREADS.  If it cannot be determined from this curve,
    the fair price is taken as the instrument spot price (method
    used_price with default arguments).  If the fair price cannot be
    determined even as the spot price, None is returned.

    Note: Will return nan if any term in the equation for the fair
    price is nan.
    """

    # Instrument spread curve to look fair prices in.
    INSTRUMENT_SPREAD_CURVE_NAME = "ZAR-CORPBONDS-SPREADS"

    bond_spreads = acm.FInstrumentSpread.Select(
        "curve='{0}' and instrument={1}"
        .format(INSTRUMENT_SPREAD_CURVE_NAME, bond.insaddr))
    # According to the data model, the combination of keys 'curve' and
    # 'instrument' should be unique.
    assert len(bond_spreads) <= 1, \
        "Spread for '{0}' on curve '{1}' is not unique." \
        .format(bond.insid, INSTRUMENT_SPREAD_CURVE_NAME)

    fair_price = None
    # (1) Try deriving the fair price from the yield curve.
    if bond_spreads:
        bond_spread = bond_spreads[0]
        benchmark_price = None
        if bond_spread.Benchmark():
            # NOTE: acm method used_price can return None.
            benchmark_price = bond_spread.Benchmark().used_price()
        if benchmark_price is not None:
            spread = bond_spread.Spread()
            quotation_factor = (bond_spread.Instrument().Quotation()
                                .QuotationFactor())
            fair_price = benchmark_price + spread/quotation_factor
    # (2) Try deriving the fair price from the spot price.
    if fair_price is None:
        acm_bond = acm.FInstrument[bond.insaddr]
        fair_price = acm_bond.used_price()

    return fair_price

@validate_entity("Trade", "Insert")
@validate_entity("Trade", "Update")
def rule_16_warn_if_bond_price_out_of_market(entity, operation):
    """Show warning if bond price is out of market.

    Compare the booking price and the fair price.  If the prices differ
    more than a given threshold, a warning is issued.  This rule won't
    stop the transaction; it will only issue a warning.
    """

    import math

    # Users in these groups bypass this rule.
    EXCLUDE_GROUPS = ("FO TCU")
    # Fraction of the fair price.  If the booking price differs from the
    # market price by more than this fraction of the fair price, a warning
    # is issued to the user.
    OUT_OF_MARKET_THRESHOLD = 0.1
    # Instruments covered by this rule.  Other instruments will be skipped.
    COVERED_INSTRUMENTS = ("Bond", "IndexLinkedBond")

    trade = entity
    instrument = trade.insaddr

    # Exclude users in EXCLUDE_GROUPS.
    if ael.user().grpnbr.grpid in EXCLUDE_GROUPS:
        return

    # Test covered instruments.
    if instrument.instype not in COVERED_INSTRUMENTS:
        return

    # Show a warning if the booking price is out of the market.
    booking_price = trade.price
    fair_price = _get_bond_fair_price(instrument)
    if fair_price is None or math.isnan(fair_price) or fair_price == 0:
        # Fair price unknown.
        message = ("FV16: Unknown fair price. Cannot check the booking "
                   "price for out of the market value.")
        show_validation_warning(message, popup=False)
    elif abs(1 - booking_price/fair_price) > OUT_OF_MARKET_THRESHOLD:
        message = ("FV16: The booking price seems to be out of the market.\n"
                   "Booking price = {0}\n"
                   "Last known fair price = {1}"
                   .format(booking_price, fair_price))
        show_validation_warning(message)
