'''-----------------------------------------------------------------------
MODULE
    SAGEN_PriceCopy

DESCRIPTION
    This script copies the  (bid, ask, last, settle) price from one instrument 
    to another instrument for specific dates and markets.

    Date                : 2010-08-05
    Purpose             : Copies the today's internal price from ZAR-CFD-SABOR to the previous business day
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Herman Hoon
    CR Number           : 395005


HISTORY
================================================================================
Date         Change no    Developer           Description
--------------------------------------------------------------------------------
2012-01-20   C879940      Peter Fabian        Fix numbers of parameters when catching exceptions 
2013-03-11   C862828      Peter Fabian        Fix price upload function (creating new price)
ENDDESCRIPTION
-----------------------------------------------------------------------'''
import ael, acm

from at_logging import  getLogger, bp_start


LOGGER = getLogger()

def update_price(fromIns, fromDate, fromMarket, toIns, toDate, toMarket, *rest):
    '''Copies the price from one instrument to another instrument '''

    fromName = fromIns.Name()
    toName = toIns.Name()
    
    priceFound = 0
    # Copy from lastprice table
    for p in fromIns.Prices():
        if p.Market().Name() == fromMarket:
            bidPrice = p.Bid()
            askPrice = p.Ask()
            lastPrice = p.Last()
            settlePrice = p.Settle()
            priceFound = 1

    # Copy from historical price table
    if not priceFound:
        for p in fromIns.HistoricalPrices():
            if p.Market().Name() == fromMarket:
                if ael.date_from_string(p.Day()) == fromDate:
                    bidPrice = p.Bid()
                    askPrice = p.Ask()
                    lastPrice = p.Last()
                    settlePrice = p.Settle()
                    priceFound = 1

    if not priceFound:
        LOGGER.warning('No %s price found for %s on %s', fromMarket, fromName, fromDate)
        return
    
    priceUpdated = 0
    # Update lastprice table
    for p in toIns.Prices():
        if p.Market().Name() == toMarket:
            if ael.date_from_string(p.Day()) == toDate:
                p.Bid(bidPrice)
                p.Ask(askPrice)
                p.Last(lastPrice)
                p.Settle(settlePrice)
                priceUpdated = 1
                try:
                    p.Commit()
                    LOGGER.info('INFO: %s %s price on %s was copied to %s %s price on %s',
                                fromName, fromMarket, fromDate, toName, toMarket, toDate)
                except Exception:
                    LOGGER.exception('WARNING: %s price on %s not committed. ', toName, toMarket)


    
    # Update historical price
    if not priceUpdated:
        for p in toIns.HistoricalPrices():
            if p.Market().Name() == toMarket:
                if ael.date_from_string(p.Day()) == toDate:
                    p.Bid(bidPrice)
                    p.Ask(askPrice)
                    p.Last(lastPrice)
                    p.Settle(settlePrice)
                    priceUpdated = 1
                    try:
                        p.Commit()
                        LOGGER.info('INFO: %s %s price on %s was copied to %s %s price on %s',
                                     fromName, fromMarket, fromDate, toName, toMarket, toDate)
                    except Exception:
                        LOGGER.exception('WARNING: %s price on %s not committed', toName, toMarket)
    
    # Create price
    if not priceUpdated:
        p = acm.FPrice()
        p.Instrument(toIns)
        p.Currency(toIns.Currency())
        p.Day(toDate)
        p.Market(acm.FParty[toMarket])
        p.Bid(bidPrice)
        p.Ask(askPrice)
        p.Last(lastPrice)
        p.Settle(settlePrice)
        try:
            p.Commit()
            LOGGER.info('INFO: %s %s price on %s was copied to %s %s on %s',
                        fromName, fromMarket, fromDate, toName, toMarket, toDate)
        except Exception:
            LOGGER.exception('WARNING: %s price on %s not committed', toName, toMarket)
            
    return
         
'''----------------------------------------------------------------------------------------------------------------------------------
    MAIN
----------------------------------------------------------------------------------------------------------------------------------'''

today = ael.date_today()
TODAY = today.to_string(ael.DATE_ISO)
YESTERDAY = today.add_days(-1)
TWODAYSAGO = today.add_days(-2)
PREVBUSDAY = today.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)
TWOBUSDAYSAGO = today.add_banking_day(ael.Calendar['ZAR Johannesburg'], -2)

dateList = {'Today':TODAY,
'TwoDaysAgo':TWODAYSAGO,
'PrevBusDay':PREVBUSDAY,
'Yesterday':YESTERDAY,
'Custom Date':TODAY}
dateKeys = dateList.keys()
dateKeys.sort()

fromDateDefault = 'Today'
fromInsDefault = 'ZAR-CFD-SABOR'
fromMarketDefault = 'internal'
toDateDefault = 'PrevBusDay'
toInsDefault = 'ZAR-CFD-SABOR'
toMarketDefault = 'internal'

marketList = []
for market in acm.FParty.Select('type = "Market"'):
    marketList.append(str(market.Name()))
    
for market in acm.FParty.Select('type = "MtM Market"'):
    marketList.append(str(market.Name()))
marketList.sort()

def enableCustomFromDate(index, fieldValues):
    ael_variables[1][9] = (fieldValues[0] == 'Custom Date')
    return fieldValues

def enableCustomToDate(index, fieldValues):
    ael_variables[5][9] = (fieldValues[4] == 'Custom Date')
    return fieldValues

# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [   
                    ['FromDate', 'From Date', 'string', dateKeys, fromDateDefault, 1, 0, 'Date for which the price will be copied.', enableCustomFromDate, 1],
                    ['FromDateCustom', 'From Date Custom', 'string', None, TODAY, 0, 0, 'Custom from date', None, 0],
                    ['FromInstrument', 'From Instrument', 'FInstrument', None, fromInsDefault, 1, 1, 'The price of this instrument will be copied.'],
                    ['FromMarket', 'From Market', 'FParty', marketList, fromMarketDefault, 1, 0, 'The price will be copied from this market.'],
                    ['ToDate', 'To Date', 'string', dateKeys, toDateDefault, 1, 0, 'Date for which the price will be updated.', enableCustomToDate, 1],
                    ['ToDateCustom', 'To Date Custom', 'string', None, TODAY, 0, 0, 'Custom to date', None, 0],
                    ['ToInstrument', 'To Instrument', 'FInstrument', None, toInsDefault, 1, 1, 'The price of this instrument will be updated.'],
                    ['ToMarket', 'To Market', 'FParty', marketList, toMarketDefault, 1, 0, 'The price will be copied to this market.']
                ]

def ael_main(ael_dict):

    process_name = "sagen_price_copy"
    with bp_start(process_name):
        
        if ael_dict['FromDate'] == 'Custom Date':
            fromDate = ael_dict['FromDateCustom']
        else:
            fromDate = str(dateList[ael_dict['FromDate']])
            
        if ael_dict['ToDate'] == 'Custom Date':
            toDate = ael_dict['ToDateCustom']
        else:
            toDate = str(dateList[ael_dict['ToDate']])
            
        fromDate = ael.date_from_string(fromDate)
        toDate = ael.date_from_string(toDate)
        
        fromIns = ael_dict['FromInstrument']
        toIns = ael_dict['ToInstrument']
        fromMarket = ael_dict['FromMarket']
        toMarket = ael_dict['ToMarket']
    
        update_price(fromIns[0], fromDate, fromMarket.Name(), toIns[0], toDate, toMarket.Name())
