'''-----------------------------------------------------------------------------
PROJECT         :  2010.2 Upgrade Fix
PURPOSE         :  Update a price indexes future monthly internal prices with SACPI forward prices.
REQUESTER       :  Shameer Sukha, Jeshma Mowjee
DEVELOPER       :  Paul Jacot-Guillarmod
Date            :  2011-08-23
--------------------------------------------------------------------------------'''
import acm

def MonthIterator(startDate, endDate):
    ''' Iterate by one month from startDate to endDate inclusive.
    '''
    nextDate = startDate
    while nextDate <= endDate:
        yield nextDate
        nextDate = acm.Time().DateAddDelta(nextDate, 0, 1, 0)

def GetForwardPrice(instrument, date):
    ''' Return the forward price for an instrument on the given date.
    '''
    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    forwardPrice = instrument.Calculation().ForwardPrice(calcSpace, date).Number()
    return forwardPrice

def AddPrice(instrument, date, value):
    ''' Insert or update the internal price for the given date.
    '''
    market = acm.FParty['internal']
    priceList = acm.FPrice.Select("instrument = %i and market = %i and day = %s" %(instrument.Oid(), market.Oid(), str(date)))
    if priceList:
        price = priceList.At(0)
    else:
        price = acm.FPrice()
    
    price.Last(value)
    price.Settle(value)
    price.Ask(value)
    price.Bid(value)
    price.Day(date)
    price.Instrument(instrument)
    price.Market(market)
    price.Currency(instrument.Currency())
    try:
        price.Commit()
    except:
        print('Could not update price for %(instrument)s on %(date)' % {'instrument': instrument.Name(), 'date': date})

def GetLatestPrice(instrument):
    ''' Return the latest internal price for the instrument.
    '''
    market = acm.FParty['internal']
    internalPrices = acm.FPrice.Select('instrument = %i and market = %i' %(instrument.Oid(), market.Oid()))
    internalPrices.SortByProperty('Day')
    return internalPrices.Last()
    
def AddForwardPrices(priceIndex, numYears):
    ''' Copy the latest price from the SACPI to the priceIndex and update the priceIndex
        internal prices for the first of each month over the next numYears years with 
        4-month SACPI forward prices.
    '''
    sacpi = acm.FInstrument['SACPI']
    latestPrice = GetLatestPrice(sacpi)
    latestDate = latestPrice.Day()
    latestValue = latestPrice.Settle()
    
    # Add the latest price from the SACPI to the priceIndex
    AddPrice(priceIndex, latestDate, latestValue)
    
    # Add numYears years worth of 4-month forward prices to the priceIndex
    startDate = acm.Time().DateAddDelta(latestDate, 0, 1, 0)
    endDate = acm.Time().DateAddDelta(latestDate, numYears, 0, 0)
    for date in MonthIterator(startDate, endDate):
        forwardDate = acm.Time().DateAddDelta(date, 0, 4, 0)
        forwardPrice = GetForwardPrice(sacpi, forwardDate)
        AddPrice(priceIndex, date, forwardPrice)

# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
'''
ael_variables = [['priceIndex', 'Price Index', 'FInstrument', None, None, 1, 1, 'Price Indices that will be updated with SACPI forward prices.', None, 1],
                 ['numYears', 'Number of Years', 'int', None, None, 1, 1, 'Number of years worth of internal prices to update on the price index.', None, 1]]

def ael_main(ael_dict):
    numYears = ael_dict['numYears']
    for priceIndex in ael_dict['priceIndex']:
        AddForwardPrices(priceIndex, numYears)
'''
