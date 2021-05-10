'''
Code provided by FIS to replace function QuoteToRoundedCleanUnitValueOverrideUnitDate
on FInstruments from FA2017 onwards. The function is private and was removed between FA2014 and FA2017
'''
import acm

# Constants for price conversions
PRICE_TYPE_DIRTY = "dirty"
PRICE_TYPE_CLEAN = "clean"
PRICE_TYPE_YIELD = "yield"
QUOTATION_NAME_PCT_OF_NOMINAL = "Pct of Nominal"
QUOTATION_NAME_CLEAN = "Clean"
QUOTATION_NAME_YIELD = "Yield"
QUOTATION_NAME_DISCOUNT_RATE = "Discount Rate"

def priceTypeToQuotationName(priceType):
    """
    Converts the price type to the quotation name
    :param priceType: the price type e.g. clean, dirty, yield
    :return: the quotation name
    """
    # Determine to quotation name for price convert
    if priceType == PRICE_TYPE_DIRTY:
        # Set to quotation as percentage of nominal i.e. price is dirty price
        return QUOTATION_NAME_PCT_OF_NOMINAL
    elif priceType == PRICE_TYPE_CLEAN:
        # Set to quotation as clean i.e. price is clean price
        return QUOTATION_NAME_CLEAN
    elif priceType == PRICE_TYPE_YIELD:
        # Set to quotation as yield i.e. price is yield
        return QUOTATION_NAME_YIELD
    else:
        raise Exception("Price type '%s' is not valid" % priceType)


def convertPriceForInstrument(calculationSpace, instrument, valueDate, price, fromQuotation, toQuotation):
    """
    Converts the given price from the a given quotation to another quotation using the specified instrument and value
    date
    :param calculationSpace:
    :param instrument:
   :param valueDate:
    :param price:
    :param fromQuotation:
    :param toQuotation:
    :return: the converted price
    """
    calculation = instrument.Calculation().PriceConvert(calculationSpace, price, fromQuotation, toQuotation, valueDate)
    value = calculation.Value().Number()

    return value

def getPriceForTrade(priceType, trade, valueDate=None, calcOnUnderlying=False):
    """
    Converts the price of the trade to the price type specified e.g. dirty, clean or yield.
    :param priceType: the type of price to calculate
    :param calculationSpace: the calculation space
    :param trade: the trade to find the price of
    :param price: the price of the trade
    :param valueDate: the value day of the trade (defaults to the trade value date)
    :param calcOnUnderlying: sets if the calculation must use the instrument or underlying
    :return: the price in the price type
    """
    # If calculation is on underlying
    calculationSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    price = trade.Price()
    if calcOnUnderlying:
        # Set instrument as underlying instrument of traded instrument
        instrument = trade.Instrument().Underlying()
    # Else
    else:
        # Set instrument as traded instrument
        instrument = trade.Instrument()

    # If value day is not set
    if not valueDate:
        # Get value day from trade
        valueDate = trade.ValueDay()

    # Set from quotation as current instrument quotation
    fromQuotation = instrument.Quotation()

    # Determine to quotation name for price convert
    toQuotationName = priceTypeToQuotationName(priceType)
    # Get to quotation
    toQuotation = acm.FQuotation[toQuotationName]

    return convertPriceForInstrument(calculationSpace, instrument, valueDate, price, fromQuotation, toQuotation)/100
