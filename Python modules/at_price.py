"""
This module contains functions for setting
the instruments' prices. It is based on the
code which was originally developed by Peter Fabian
for the PS_IntFut_PriceUploader module.
Former name of this module was PS_PriceUploadFunctions.

Date                : 2013-12-05
Department and Desk : Prime Services (originally)
Requester           : Unknown
Developers          : Peter Fabian, Peter Basista
CR Number           : CHNG0001547146

HISTORY
=======

Date        CR number       Developer       Description
-------------------------------------------------------
2014-12-02  CHNG0002472033  Peter Basista   Some PEP 8 related changes.
                                            Also correct the "variable
                                            referenced before assignment"
                                            error.
"""
import traceback

import acm


def set_price_values(acm_price, price_value):
    """
    Set the price values on the provided price to the provided value.
    """
    # The convention says that SPOT prices should also have
    # the bid, ask and last values of the price set.
    if acm_price.Market().Name() == "SPOT":
        acm_price.Bid(price_value)
        acm_price.Ask(price_value)
        acm_price.Last(price_value)
    # The settle price will be set for all the markets.
    acm_price.Settle(price_value)


def create_price(acm_instrument,
                 acm_market,
                 acm_currency,
                 price_value,
                 date_string):
    """
    Create a new price for the provided instrument on a given market
    in a given currency and for a given date with the specified value.
    """
    acm_price = acm.FPrice()
    acm_price.Instrument(acm_instrument)
    acm_price.Market(acm_market)
    acm_price.Currency(acm_currency)
    set_price_values(acm_price, price_value)
    acm_price.Day(date_string)
    acm_price.Commit()


def update_price(acm_price, acm_currency, price_value):
    """
    Set the currency and the value
    of the provided price to the specified values.

    This is a simple form of a price update,
    which will update the currency
    and the price values only.
    """
    acm_price.Currency(acm_currency)
    set_price_values(acm_price, price_value)
    acm_price.Commit()


def update_last_price(acm_last_price, acm_currency, price_value, date_string):
    """
    Update the provided last price by creating a new last price
    with the supplied properties and moving the provided last price
    into the historical price table if necessary.
    """
    # If the date on the provided last price is the same
    # as the desired new price's date.
    if acm.Time.DateDifference(date_string, acm_last_price.Day()) == 0:
        # We just update the provided last price.
        update_price(acm_last_price,
                     acm_currency,
                     price_value)
        # There is no need to set the price's date,
        # because it already has the same value as required.
        return

    # At this point, the current last price has a different date
    # than the date of the new price which we would like to set.
    # So, we have to move the provided last price
    # to the historical price table.

    # At first, we need to create a historical price
    # with the same properties as the current last price has.
    # Of course, we first have to check if such a price already exists.
    # If it does, we have to update it instead of creating it.
    candidate_price_selection = acm.FPrice.Select(
        # The select statement considers only historical prices.
        ("instrument = '{0}' and "
         "market = '{1}' and "
         "day = '{2}'").format(
             acm_last_price.Instrument().Oid(),
             acm_last_price.Market().Oid(),
             acm_last_price.Day()))
    if candidate_price_selection:
        # If the historical price with the desired attributes
        # already exists, we just update it.
        # There can be at most one such price.
        candidate_price = candidate_price_selection[0]
        update_price(candidate_price,
                     acm_last_price.Currency(),
                     # We use the current last price's
                     # settle price value only
                     acm_last_price.Settle())
    else:
        # Otherwise, we just create a new historical price.
        create_price(acm_last_price.Instrument(),
                     acm_last_price.Market(),
                     acm_last_price.Currency(),
                     # We use the current last price's
                     # settle price value only
                     acm_last_price.Settle(),
                     acm_last_price.Day())

    # Then we set the new attributes on the provided last price and commit it.
    acm_last_price.Currency(acm_currency)
    set_price_values(acm_last_price, price_value)
    acm_last_price.Day(date_string)
    acm_last_price.Commit()


def set_instrument_price(acm_instrument,
                         acm_market,
                         price_value,
                         acm_currency=None,
                         date_string=None):
    """
    Set the price of the provided instrument on a given market
    in a given currency for a given date to the specified value.

    The reason why there is a need for such a complicated
    price setting function is the following:
    In Front Arena, prices are split into two tables:
        1. last price
        2. historical price
    In the table last price, it is possible to store only one price
    per instrument and per market.
    This means that there *cannot* be two prices for the same
    instrument and the same market defined for the different dates,
    for example.
    In the historical price table, however, this is perfectly possible.

    If one wants to add a price for the today's date,
    it will automatically be added to the last price table.
    And this poses problems.

    The issue is that if there is already an older price
    in the last price table for the same instrument and the same market,
    one cannot create a new today's price for the same instrument and market,
    simply because that would create a table row with the same key
    as already exists on a database level. And that would result
    in the insert operation being rejected.
    So, we have to manually build the logic around it.
    We need to move the price from the last price table
    to the historical price table if necessary.

    Note that date_string, if supplied, will be used "as is",
    which means that you as a caller of this function
    are responsible for supplying the date
    in the correct format.
    In this case, the correct format is the one used by acm,
    which is basically a standard Python string containing the date.
    In order to be sure that your date will be interpreted
    correctly, always use the ISO 8601 date format (i.e. YYYY-MM-DD).
    """
    if not acm_currency:
        # The default currency is the instrument's currency.
        acm_currency = acm_instrument.Currency()
    if not date_string:
        # The default date is today.
        date_string = acm.Time.DateToday()
    try:
        candidate_price_selection = acm.FPrice.Select(
            # The select statement considers only historical prices.
            ("instrument = '{0}' and "
             "market = '{1}' and "
             "day = '{2}'").format(
                 acm_instrument.Oid(),
                 acm_market.Oid(),
                 date_string))
        if candidate_price_selection:
            # If the price with the desired attributes
            # already exists in the historical price table,
            # we just update it.
            candidate_price = candidate_price_selection[0]
            update_price(candidate_price,
                         acm_currency,
                         price_value)
            return
        # At this point, we would either need to
        # update the last price or create a new price.

        # If the new price's date indicates that it will land
        # into the last price table.
        if acm.Time.DateDifference(date_string, acm.Time.DateToday()) == 0:
            # We have to check if another, conflicting price
            # is not already present in the last price table.
            last_prices = list(acm_instrument.Prices())
            last_prices = [price for price in last_prices
                           if price.Market() == acm_market]
            if last_prices:
                # A conflicting last price has been found.
                # Luckily, there can only be one such price.
                last_price = last_prices[0]
                # We have to use a special function when updating it.
                update_last_price(last_price,
                                  acm_currency,
                                  price_value,
                                  date_string)
                return

        # If there will be no conflict in the last price table,
        # or if the new price will land into the historical price table,
        # we can simply create the price.
        create_price(acm_instrument,
                     acm_market,
                     acm_currency,
                     price_value,
                     date_string)
    except Exception as exc:
        traceback.print_exc()
        print(("Could not set the price for instrument '{0}', "
               "market '{1}', date '{2}', currency '{3}' to {4}. "
               "Error message: {5}").format(
                   acm_instrument.Name(),
                   acm_market.Name(),
                   date_string,
                   acm_currency.Name(),
                   price_value,
                   exc))
        raise
