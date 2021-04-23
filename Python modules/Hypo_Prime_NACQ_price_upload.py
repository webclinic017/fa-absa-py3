"""-----------------------------------------------------------------------------------------
MODULE
    Hypo_Prime_NACQ_price_upload

DESCRIPTION
    Date                : 2020-10-21
    Purpose             : This calculates the quarterly compounded rate and uploads to 
                          new rate index ZAR/Hypo_Prime_NACQ's price entry table
    Requester           : James Moodie
    Developer           : Qaqamba Ntshobane

HISTORY
=============================================================================================
Date            Change No.       Developer               Description
---------------------------------------------------------------------------------------------
2020-10-21      PCGDEV-597       Qaqamba Ntshobane       Initial Implementation

ENDDESCRIPTION
------------------------------------------------------------------------------------------"""

import acm
from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()
ael_variables.add(
    'price_date',
    label = 'Price Date',
    default = acm.Time.DateToday(),
    alt = 'Date for price update.'
    )


def _get_latest_price(index, date):

    return [pr.Settle() for pr in index.Prices() if pr.Market().Name() == 'SPOT' 
                                                        and pr.Day() == date]


def _get_historical_price(index, date):

    return [pr.Settle() for pr in index.HistoricalPrices() if pr.Market().Name() == 'SPOT'
                                                        and pr.Day() == date]


def _get_spot_price(date):

    index = acm.FRateIndex['ZAR-PRIME-1M']

    spot_price = _get_latest_price(index, date)

    if not spot_price:
        spot_price = _get_historical_price(index, date)

    if spot_price:
        return spot_price[0]
    return 1


def _calculate_quartely_compounded_rate(spot_price):

    # Formula: (1+((Prime rate)/100)/12))^(3))-1)*(12/3)*100)

    prime_rate = spot_price/100
    compoundings_per_year = 4
    period = 12

    return (pow((1+prime_rate/period), 3) - 1) * (compoundings_per_year * 100)


def _add_price(spot_price, date):

    index = acm.FRateIndex['ZAR/Hypo_Prime_NACQ']
    price = None

    todays_spot_prices = [p for p in index.Prices() if p.Market().Name() == 'SPOT' and p.Day() == date]

    if todays_spot_prices:
        price = todays_spot_prices[0]
    else:
        price = acm.FPrice()
        price.Market('SPOT')
        price.Day(date)

    price.Instrument(index)
    price.Ask(spot_price)
    price.Bid(spot_price)
    price.Last(spot_price)
    price.Settle(spot_price)
    price.Currency(index.Currency().Name())

    try:
        price.Commit()
    except Exception as e:
        acm.Log('Price did not commit for %s | %s' % (index.Name(), e))


def ael_main(dictionary):

    date = acm.Time.DateAddDelta(dictionary['price_date'], 0, 0, 0)

    price = _get_spot_price(date)
    price = _calculate_quartely_compounded_rate(price)

    if price:
        _add_price(price, date)
        acm.Log('Price successfully updated for '+date)
        return
    acm.Log('No price was updated for '+date)

