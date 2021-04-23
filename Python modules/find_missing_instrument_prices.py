"""
-------------------------------------------------------------------------------
MODULE
    find_missinng_instrument_prices

DESCRIPTION
    Date                : 2013-05-24
    Purpose             : This module looks for instruments of certain types
                          which did not have their SPOT or SPOT_SOB prices
                          updated during the specific time in the past.
                          In case such instruments are found, their
                          descriptions are printed and optionally also
                          sent over e-mail to the desired recipients.
                          This module is scheduled to run regularly
                          at 8:30 and 17:30 every business day
                          as a task called FIND_MISSING_MTM_PRICES_SERVER.
    Department and Desk : Middle Office
    Requester           : Merell Nair
    Developer           : Peter Basista
    CR Number           : 1049254

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
"""

import datetime

import acm

import FBDPCommon

default_instrument_types = "Bond,IndexLinkedBond,FRN"
available_instrument_types = []
# FIXME: Is there any better way to list instrument types?
# Here we suppose that all the instrument types
# have their enum value between 0 and 256,
# but this might change in the future.
for i in range(0, 256):
    # A call to Text() is necessary here, because EnumToString
    # returns an object of type FSymbol, not a Python string.
    enum_string = acm.EnumToString("InsType", i).Text()
    if enum_string != "?":
        available_instrument_types.append(enum_string)

description_instypes = ("Instrument types which will be checked "
    "for the presence of the recent SPOT or SPOT_SOB prices.")
description_datediff = ("Number of days in the past since when "
    "the SPOT or SPOT_SOB prices should have been updated "
    "on the specified instruments. For example, 0 means today, "
    "1 means yesterday, ... etc. If some of these instruments "
    "do not have such a price, it will be reported.")
description_remails = ("The e-mail addresses which will be used "
    "to send out a notification reports about the missing "
    "SPOT or SPOT_SOB prices.")

# Variable Name, Display Name, Type,
# Candidate Values, Default, Mandatory, Multiple,
# Description, Input Hook, Enabled
ael_variables = [["instrument_types", "Instrument types", "string",
    available_instrument_types, default_instrument_types, 1, 1,
    description_instypes, None, 1],
    ["date_diff", "Date difference", "int",
    None, 0, 1, 0,
    description_datediff, None, 1],
    ["reporting_emails", "Reporting e-mails", "string",
    None, None, 0, 1,
    description_remails, None, 1]]

# Returns all the MTM instruments of the provided types.
def get_mtm_instruments(instrument_types):
    all_instruments = []
    for instrument_type in instrument_types:
        all_instruments.extend(
            acm.FInstrument.Select(
                "insType = {0}".format(instrument_type)))
    instruments = [i for i in all_instruments if (i.MtmFromFeed() and
        i.Name().endswith("/MTM"))]
    return instruments

# Checks all the prices of the provided MTM instrument
# for the presence of a recent SPOT and SPOT_SOB price.
# A recent price is a price whose update time
# is after the provided from_date.
def check_mtm_instrument_spot_prices(instrument, from_date):
    prices = instrument.Prices()
    prices.AddAll(instrument.HistoricalPrices())
    if not prices:
        # Instrument which does not have any prices should be reported.
        return ((instrument.InsType(), instrument.Name(),
            "no prices found"))
    spot_prices_found = [False, False]
    # Update times of the most recent SPOT and SPOT_SOB prices.
    update_times = [datetime.date.fromtimestamp(0),
        datetime.date.fromtimestamp(0)]
    for price in prices:
        if price.Market().Name() in ("SPOT", "SPOT_SOB"):
            # price.UpdateTime() should return a number of seconds
            # since midnight 1970-01-01, UTC time.
            # Therefore, this value should be equal to Unix / POSIX time,
            # but there is no reference to these terms
            # in the acm documentation.
            update_time = datetime.date.fromtimestamp(price.UpdateTime())
            # The currently examined SPOT or SPOT_SOB price
            # is sufficiently recent.
            if price.Market().Name() == "SPOT":
                spot_prices_found[0] = True
                if update_times[0] < update_time:
                    update_times[0] = update_time
            else: # price.Market().Name() == "SPOT_SOB"
                spot_prices_found[1] = True
                if update_times[1] < update_time:
                    update_times[1] = update_time
    if spot_prices_found != [True, True]:
        # Instrument without SPOT or SPOT_SOB
        # price should be reported.
        return ((instrument.InsType(), instrument.Name(),
            "SPOT* price missing"))
    if update_times[0] < from_date and update_times[1] < from_date:
        # Instrument with old SPOT price and old SPOT_SOB price
        # should be reported.
        return ((instrument.InsType(), instrument.Name(),
            "old SPOT* prices"))
    if update_times[0] < from_date:
        # Instrument with old SPOT price should be reported.
        return ((instrument.InsType(), instrument.Name(),
            "old SPOT price"))
    if update_times[1] < from_date:
        # Instrument with old SPOT_SOB price should be reported.
        return ((instrument.InsType(), instrument.Name(),
            "old SPOT_SOB price"))
    # The recent SPOT and SPOT_SOB prices are present.
    return None

"""
The main function.
"""
def ael_main(parameters):
    instrument_types = parameters["instrument_types"]
    date_diff = int(parameters["date_diff"])
    reporting_emails = parameters["reporting_emails"]
    today = datetime.date.today()
    tdelta = datetime.timedelta(days=date_diff)
    from_date = today - tdelta
    instruments = get_mtm_instruments(instrument_types)
    if not instruments:
        print ("No matching instruments have been found, "
            "so no price checking has been performed.")
        return
    results = []
    for instrument in instruments:
        result = check_mtm_instrument_spot_prices(instrument, from_date)
        if result:
            results.append(result)
    if results:
        message = ("Found {0} MTM instruments of types {1} with missing "
            "SPOT or SPOT_SOB prices since {2}:\n\n".format(len(results),
            instrument_types, from_date))
        message += ("Instrument type     Instrument name"
            "                   Reason\n")
        message += ("---------------     ---------------"
            "                   ------\n")
        for result in results:
            message += "{0: <20}{1: <20}{2: >20}\n".format(result[0],
                result[1], result[2])
        print(message)
        if reporting_emails:
            for reporting_email in reporting_emails:
                FBDPCommon.sendMail(reporting_email,
                    "[Production] MTM instruments with missing SPOT "
                    "or SPOT_SOB prices found", message)
        else:
            print ("No reporting e-mail addresses have been provided, "
                "so no e-mail has been sent.")
    else:
        print(("All the checked MTM instruments have had their SPOT "
            "and SPOT_SOB prices updated since {0}".format(from_date)))
