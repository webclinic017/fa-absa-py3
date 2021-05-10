"""
This module contains all the FCustomMethod entry points for the extension module.
"""


import acm

from GenericMandatesLogger import getLogger


def RateTolerance(trade):
    """
    Calculate the Rate Tolerance for a specific trade on a FX instrument.
    :param trade: FTrade
    :return: double
    """
    getLogger().debug("Executing - RateTolerance()")

    price = trade.Price()
    pair = trade.CurrencyPair()
    if pair:
        curr1 = pair.Currency1().Name()
        curr2 = pair.Currency2().Name()

        rate = _CalcFXRate(curr1, curr2, None)
        tolerance = ((price/rate - 1) * 100)
        getLogger().debug('Calculated Tolerance: %s' % tolerance)
        return tolerance
    else:
        return 0


def _CalcFXRate(currid1, currid2, date):
    """
    Calculate the FX tolerance
    :param currid1: string
    :param currid2: string
    :param date: date
    :return: float
    """

    # pylint: disable=no-member
    space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()

    curr1 = acm.FInstrument[currid1]
    curr2 = acm.FInstrument[currid2]
    if date is None:
        date = acm.Time().DateNow()
    rate = curr1.Calculation().MarketPrice(space, date, 0, curr2).Value().Number()
    getLogger().debug('Calculated FX Rate: %s' % rate)
    return rate


def GetTradeUsingOptionalKey(optionalKey):
    """
    Locate a trade using the optional_key field as a reference.
    :param optionalKey: string
    :return: FTrade
    """
    # pylint: disable=no-member
    trades = acm.FTrade.Select('optionalKey="%s"' % optionalKey)
    if len(trades) == 1:
        return trades[0]
    else:
        return ' - '


def GetMandateBlockingTypeFromLimit(limit):
    """
    Get limit type (blocking or non-blocking)
    :param limit: FLimit
    :return: string
    """
    if limit:
        return 'Blocking' if limit.Threshold() == 1 else 'Non-Blocking'
    else:
        return ''


def GetTenorMaturity(trade):
    """
    Calculate the amount of days from today till the maturity date.
    :param trade: FTrade
    :return: int
    """
    # pylint: disable=no-member
    if trade.Instrument().ExpiryDate():
        return acm.Time.DateDifference(trade.Instrument().ExpiryDate(), acm.Time.DateToday())
    else:
        return ""


def GetTenorValueDay(trade):
    """
    Calculate the amount of days from today till the Value Day of the trade.
    :param trade: FTrade
    :return: int
    """
    # pylint: disable=no-member
    return acm.Time.DateDifference(trade.ValueDay(), acm.Time.DateToday())


def GetTenorValueDayBusinessDays(trade):
    """
    Calculate the amount of business days from today till the Value Days of the trade.
    :param trade: FTrade
    :return: int
    """
    # pylint: disable=no-member
    calendar = trade.Instrument().Currency().Calendar()
    daysBetween = calendar.BankingDaysBetween(trade.ValueDay(), acm.Time.DateToday())
    return daysBetween
