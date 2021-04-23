'''-----------------------------------------------------------------------
MODULE
    ABSAPortfolioSwapAveVolumeCalc

DESCRIPTION
    This script calculates The 3m Average Volume from the Volume market.

    Date                : 2010-09-08
    Purpose             : The 3m Average volume is calculed from the Volume market
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Herman Hoon
    CR Number           : 

ENDDESCRIPTION
-----------------------------------------------------------------------'''


import acm
import ael


THREE_MONTH_MARKET = "3m Average Volume"
""" Market holding rolling average volumes over last 3 months. """
DAILY_MARKET = "Volume"
""" Uploaded daily, via a feed. Contains volume traded today"""
AVERAGING_PERIOD = -60
"""3months == 60 business days == 12 weeks """


def aveVolumeCalc(ins, date):
    """ Read the rolling 3m average trade volume, over the past 3 months, 
        from the THREE_MONTH_MARKET. 
        Read the Volume, then use that to get the new 3m average for today
    """
    cal = ins.Currency().Calendar()
    enddate = cal.AdjustBankingDays(date, 0)
    startdate = cal.AdjustBankingDays(date, AVERAGING_PERIOD)

    prices=[]
    histprices = acm.FPrice.Select("instrument = %s and market = '%s' \
                        and day > '%s' and day <='%s'" % 
                        (ins.Oid(), DAILY_MARKET, startdate, enddate))
    
    for price in histprices:
        settle = price.Settle()
        if settle >= 0:
            prices.append(settle)
    
    #upgrade 2013 fix for failure during run - acm.Math().AverageOf seems buggy
    try:
        avgprice = (sum(prices)/len(prices))
    except ZeroDivisionError:
        avgprice = 0
        
    #avgprice = acm.Math().AverageOf(prices, None)
    
    #Overwrite today's price if you find it 
    newPrice = acm.FPrice.Select01("instrument = %s and market = '%s' and day = %s" % 
                                      (ins.Oid(), THREE_MONTH_MARKET, enddate),
                                      'NaN')
    if not newPrice:
        newPrice = acm.FPrice()
        newPrice.Instrument(ins)
        newPrice.Day(enddate)
        newPrice.Market(THREE_MONTH_MARKET)
        newPrice.Currency(ins.Currency())

    newPrice.Settle(avgprice)
    try:
        newPrice.Commit()
        print 'INFO: %s price for %s  was created on %s' %(THREE_MONTH_MARKET, ins.Name(), date)
    except Exception, err:
        print 'ERROR: %s price for %s did not commit: %s' %(THREE_MONTH_MARKET, ins.Name(), str(err))
 
    return newPrice

'''----------------------------------------------------------------------------------------------------------------------------------
    MAIN
----------------------------------------------------------------------------------------------------------------------------------'''

calendar = acm.FCurrency[str(acm.UsedAccountingCurrency())].Calendar().Name()

today           = ael.date_today()
TODAY           = today.to_string(ael.DATE_ISO)
YESTERDAY       = today.add_days(-1)
TWODAYSAGO      = today.add_days(-2)
PREVBUSDAY      = today.add_banking_day(ael.Calendar[calendar], -1)
TWOBUSDAYSAGO   = today.add_banking_day(ael.Calendar[calendar], -2)

dateList     = {'Today':TODAY,
                'TwoDaysAgo':TWODAYSAGO,
                'PrevBusDay':PREVBUSDAY,
                'Yesterday':YESTERDAY,
                'Custom Date':TODAY}
                
dateKeys = dateList.keys()
dateKeys.sort()


instrumentList = []
instrumentList.append('<ALL>')
party = ael.Party['Volume']
prices = ael.PriceDefinition.select('source_ptynbr = %s' %(party.ptynbr))
for p in prices:
    instrumentList.append(p.insaddr.insid)
instrumentList.sort()


def enableCustomDate(index, fieldValues):
    ael_variables[index+1][9] = (fieldValues[index] == 'Custom Date')
    return fieldValues


#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [   
                    ['Date', 'Date', 'string', dateKeys, 'Today', 1, 0, 'Date for which the price will be copied.', enableCustomDate, 1],
                    ['CustomDate', 'Custom Date', 'string', None, TODAY, 0, 0, 'Custom date', None, 0],
                    ['Instruments', 'Instruments', 'string', instrumentList,  '<ALL>', 1, 1, 'The price of this instrument will be copied.']
                ]


def ael_main(ael_dict):
    if ael_dict['Date'] == 'Custom Date':
        date = ael_dict['CustomDate']
    else:
        date = str(dateList[ael_dict['Date']])
    
    if '<ALL>' in ael_dict['Instruments']:
        instruments = instrumentList
    else:
        instruments = ael_dict['Instruments']
        
    for ins in instruments:
        if ins != '<ALL>':
            aveVolumeCalc(acm.FInstrument[ins], date)
