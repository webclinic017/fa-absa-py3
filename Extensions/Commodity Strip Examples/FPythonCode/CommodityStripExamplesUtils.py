
from __future__ import print_function
import acm


# #################################################
# Set contract size for contracts quoted in hours
# #################################################

def IsQuotedInHoursPerPeriod( i ):
    # Note: This could be changed to use instrument category, page group etc depending on system configuration
    if i.Name() in ('NORDPOOL - SYS',): 
        return True
    return False

def HoursInMonth( lastDayOfMonth ):  # Here with European daylight savings adjustment
    hoursUnadjusted = 24 * acm.Time.DayOfMonth( lastDayOfMonth )
    if acm.Time.DateToYMD( lastDayOfMonth )[ 1 ] == 3: #March
        return hoursUnadjusted - 1 
    elif acm.Time.DateToYMD( lastDayOfMonth )[ 1 ] == 10: #October
        return hoursUnadjusted + 1
    return hoursUnadjusted

def GetContractSizeForQuotedInHours(deal):
    i = deal.Instruments().First()
    if IsStandardMonthContract( i ):
        return HoursInMonth( i.Legs().First().EndDate() )
    else:
        print ("WARNING: Calculaing contract size for odd period electricity not implemented")
        return 1.0


# #################################################
# Set default price to theor price
# #################################################
def theoreticalPriceStrip( componentInstrumentTheoreticalPrices, componentInstrumentDiscountFactors, componentTradeQuantities, componentInstrumentContractSizes ):
    # Approach: Retrieve the price that makes the sum of the quantity weighted discounted difference of trade price and traded instrument's theoretical price zero
    sumOfDiscountedQuantityWeightedTheors, sumOfQuantityWeightedDfs = 0.0, 0.0
    if len( componentInstrumentTheoreticalPrices  ) == 1: # If there is just one component componentInstrumentDiscountFactors will not be a list
        return componentInstrumentTheoreticalPrices[ 0 ]
    for nbr in range( len( componentInstrumentTheoreticalPrices ) ):
        sumOfDiscountedQuantityWeightedTheors += componentInstrumentTheoreticalPrices[ nbr ] * componentTradeQuantities[ nbr ] * componentInstrumentContractSizes[ nbr ] * componentInstrumentDiscountFactors[ nbr ]
        sumOfQuantityWeightedDfs += componentTradeQuantities[ nbr ] * componentInstrumentContractSizes[ nbr ] * componentInstrumentDiscountFactors[ nbr ]
    return sumOfDiscountedQuantityWeightedTheors / float( sumOfQuantityWeightedDfs )

def GetInstrumentPricingParameters(dealPackage, cs):
    componentInstrumentSettlementDates, componentInstrumentTheoreticalPrices, componentTradeQuantities, componentInstrumentContractSizes = [], [], [], []
    for t in dealPackage.AllOpeningTrades():
        i = t.Instrument()
        componentTradeQuantities.append( t.Quantity() )
        componentInstrumentContractSizes.append( i.ContractSizeInQuotation() )
        componentInstrumentSettlementDates.append( i.Legs().First().CashFlows().First().PayDate() ) #currently built for Asian Future/Forward. Needs adjustment for Bullets!
        componentInstrumentTheoreticalPrices.append( i.Calculation().TheoreticalPrice( cs ).Number() )
    return componentInstrumentSettlementDates, componentInstrumentTheoreticalPrices, componentTradeQuantities, componentInstrumentContractSizes

def GetSuggestedPriceAsian(dealPackage):
    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection( acm.GetDefaultContext() )
    discountCurve = dealPackage.Instruments().First().Calculation().MappedDiscountCurve( cs )
    discountToDate = acm.Time.DateToday()
    componentInstrumentSettlementDates, componentInstrumentTheoreticalPrices, componentTradeQuantities, componentInstrumentContractSizes = GetInstrumentPricingParameters(dealPackage, cs)
    componentInstrumentDiscountFactors = discountCurve.Discount( discountToDate, componentInstrumentSettlementDates )
    return theoreticalPriceStrip( componentInstrumentTheoreticalPrices, componentInstrumentDiscountFactors, componentTradeQuantities, componentInstrumentContractSizes )    

# #################################################
# Suggested name
# #################################################
monthTLAs = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

def StandardLinearAsianStripName( dealPackage, type ):
    und = dealPackage.GetAttribute('underlying')
    undName = und.Name()
    startDateAsISO = dealPackage.GetAttribute('stripDates_startDate')
    startYearAsInteger, startMonthAsInteger = acm.Time.DateToYMD( startDateAsISO )[ 0 ], acm.Time.DateToYMD( startDateAsISO )[ 1 ]
    startYearString = str( startYearAsInteger )[2:4]
    startMonthTLA = monthTLAs[ startMonthAsInteger - 1 ] # Start month expressed as three letters
    endDateAsISO = dealPackage.GetAttribute('stripDates_endDate')    
    endYearAsInteger, endMonthAsInteger = acm.Time.DateToYMD( endDateAsISO )[ 0 ], acm.Time.DateToYMD( endDateAsISO )[ 1 ]
    endYearString = str( endYearAsInteger )[2:4]
    endMonthTLA = monthTLAs[ endMonthAsInteger - 1 ] # End month expressed as three letters
    otc = dealPackage.GetAttribute('otc')
    curr = dealPackage.GetAttribute('currency').Name()
    name = undName 
    if curr != und.Currency().Name():
            name = name + '/' + curr 
    name = name + '/' + type + '/' + startMonthTLA + startYearString + '-' + endMonthTLA + endYearString
    if otc:
        name = name + '/' + 'OTC'
    return name

# #################################################
# Utility methods
# #################################################

def MondayBeforeThirdWednesday(year, month):
    weekDays = {'Monday': 2,
                'Tuesday': 1,
                'Wednesday': 0,
                'Thursday': 6,
                'Friday': 5,
                'Saturday': 4,
                'Sunday': 3}

    start = acm.Time.DateFromYMD(year, month, 1)
    thirdWednesday = acm.Time.DateFromYMD(year, month, 15 + weekDays[acm.Time.DayOfWeek(start)])
    previousMonday = acm.Time.DateAddDelta(thirdWednesday, 0, 0, -2)
    return previousMonday

def IsAgricultural( commodity ):
    if commodity.Name() == 'EURONEXT - MILLING WHEAT': # in a real case use category, product type or similar instead
        return True
    return False

def GetFirstFuture( dealPackage, date ):
    allReferenceInstruments = dealPackage.GetAttributeMetaData('underlying', 'choiceListSource')().GetChoiceListSource()
    futs = [i for i in allReferenceInstruments if i.InsType() == 'Future/Forward']
    firstFuture = None
    if len(futs) > 0:
        for f in futs:
            if acm.Time.DateDifference(f.ExpiryDateOnly(), date) >= 0 and (firstFuture is None or acm.Time.DateDifference(f.ExpiryDateOnly(),firstFuture.ExpiryDateOnly()) < 0):
                firstFuture = f
    return firstFuture

def IsStandardMonthContract( i ):
    if i.InsType() == 'Average Future/Forward':
        startDate = i.Legs().First().StartDate()
        endDate = i.Legs().First().EndDate()
        # Note: assuming not a "day-ahead market"
        return ( startDate == acm.Time.FirstDayOfMonth( startDate ) and endDate == acm.Time.DateAddDelta( acm.Time.FirstDayOfMonth( startDate ), 0, 1, -1 ) )
    return False

def IsStandardMonthStrip(dealPackage):
    for i in dealPackage.Instruments():
        standard = IsStandardMonthContract(i)
        if not standard:
            return False
    return True
