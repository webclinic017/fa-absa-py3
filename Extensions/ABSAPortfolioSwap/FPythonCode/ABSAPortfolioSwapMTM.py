"""-----------------------------------------------------------------------
MODULE
    ABSAPortfolioSwapMTM

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Mark to Market script for portfolio swaps.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Sungard
    CR Number           : 455227

2014-11-20  CHNG0002450799  Peter Fabian  Fixing errors and exception handling
ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm
import ael

import ABSAPortfolioSwapGuiUtil
reload(ABSAPortfolioSwapGuiUtil)

from at_logging import getLogger, bp_start

LOGGER = getLogger()

CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')
'''================================================================================================
================================================================================================'''
def getTheorPriceAtDate(calcSpace, ins, date):
    calcSpace.SimulateGlobalValue('Valuation Date', date)
    return calcSpace.CalculateValue(ins, 'Price Theor')
'''================================================================================================
================================================================================================'''
def fillPrice(ins, thPrice):
    Price = getPrice(ins, thPrice)
    if thPrice:
        if Price == None:
            price = acm.FPrice().Clone()
            price.Instrument(ins)
            price.Currency(thPrice.Unit())
            price.Day(thPrice.DateTime())
            price.Settle(thPrice.Value())
            price.Market(acm.FParty['internal'])
            return price
        else:
            price = Price.Clone()
            price.Settle(thPrice.Value())
            Price.Apply(price)
            return Price
    else:
        return None
    
'''================================================================================================
================================================================================================'''
def getPrice(ins, thPrice):
    if thPrice:
        selectStr = "instrument='" + ins.Name() + "' and day='" + thPrice.DateTime() + "' and market='internal' and currency='" + str(thPrice.Unit()) + "'" 
        List = acm.FPrice.Select(selectStr)  # MKLIMKE use Select01
        if len(List) > 0:
            return List[0]
        else:
            return None
    else:
        return None
'''================================================================================================
================================================================================================'''
def commitPrice(ins, thPrices):
    prices = []
    for thPrice in thPrices:
        prices.append(fillPrice(ins, thPrice))
    acm.BeginTransaction()
    try:
        for price in prices:
            if price:
                LOGGER.info("Updating price: Instrument: %s, Currency: %s, Day: %s, Settle: %s, Market: %s", 
                            price.Instrument().Name(),
                            price.Currency().Name(),
                            price.Day(),
                            price.Settle(),
                            price.Market().Name())
                price.Commit()
                ael.poll()    
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        LOGGER.exception("Could not commit price for ins %s.", ins.Name())
        raise
    
    return prices
'''================================================================================================
================================================================================================'''
def storeMtmPrice(ins, dates):
    thPrices = []
    
    for date in dates:
        thPrices.append(getTheorPriceAtDate(CALC_SPACE, ins, date))

    prices = commitPrice(ins, thPrices)
    return prices
'''================================================================================================
================================================================================================'''


'''================================================================================================
================================================================================================'''
ttStartDate = 'The start date (inclusive) of the Portfolio Swap Mark to Market script.'
ttStartDateCustom = 'Custom start date.'
ttEndDate = 'The end date (inclusive) of the Portfolio Swap Mark to Market script.'
ttEndDateCustom = 'Custom end date.'
ttPfSwap = 'Portfolio swap instrument(s).'

StartDateList = ABSAPortfolioSwapGuiUtil.StartDateList
EndDateList = ABSAPortfolioSwapGuiUtil.EndDateList
psquery = ABSAPortfolioSwapGuiUtil.instrumentQuery(instype=('Portfolio Swap',))
# [fieldId, fieldLabel, fieldType, fieldValues, defaultValue, isMandatory, insertItemsDialog, toolTip, callback, enabled]
ael_variables = \
[
    ['startDate', 'Start Date', 'string', StartDateList.keys(), 'Yesterday', 1, 0, ttStartDate],
    ['startDateCustom', 'Start Date Custom', 'string', None, StartDateList['Yesterday'], 1, 0, ttStartDateCustom],
    ['endDate', 'End Date', 'string', EndDateList.keys(), 'Now', 1, 0, ttEndDate],
    ['endDateCustom', 'End Date Custom', 'string', None, EndDateList['Now'], 1, 0, ttEndDateCustom],
    ['portfolioSwaps', 'Portfolio Swap(s)', 'FInstrument', None, psquery, 1, 1, ttPfSwap],
    ['clientName', 'Short name', 'string', None, 'CLIENT', 0, 0]
]
'''================================================================================================
================================================================================================'''
def ael_main(ael_dict):
    process_name = "ps.mtm.{0}".format(ael_dict["clientName"])
    with bp_start(process_name):
        
        PortfolioSwapList = ael_dict['portfolioSwaps']
        
        if ael_dict['startDate'] == 'Custom Date':
            startDate = ael.date(ael_dict['startDateCustom'])
        else:
            startDate = ael.date(StartDateList[ael_dict['startDate']])
        
        if ael_dict['endDate'] == 'Custom Date':
            endDate = ael.date(ael_dict['endDateCustom'])
        else:
            endDate = ael.date(EndDateList[ael_dict['endDate']])
        
        has_exceptions = False
        for portSwap in PortfolioSwapList:
            try:
                dates = []
                localStartDate = startDate
                pfsStartDate = ael.date(portSwap.StartDate())
                
                if localStartDate < pfsStartDate:
                    localStartDate = pfsStartDate
                
                fromDate = localStartDate
    
                while localStartDate <= endDate:
                    dates.append(str(localStartDate))
                    localStartDate = localStartDate.add_banking_day(ael.Calendar['ZAR Johannesburg'], 1)
    
                if len(dates) > 0:
                    storeMtmPrice(portSwap, dates)
                    LOGGER.info('INFO: Saved MtM prices for %s from %s to %s', portSwap.Name(), fromDate, endDate)
            except Exception:
                LOGGER.exception('ERROR: MtM price for Portfolio swap %s was not calculated', portSwap.Name())
                has_exceptions = True
                # Exception is not raised here so the script can process as much data as possible, 
                # it will, however, be raised at the end of processing
        
        if has_exceptions:
            raise RuntimeError("An exception occurred during pswap MtM")
        else:
            LOGGER.info('Completed successfully')
            
'''================================================================================================
================================================================================================'''
def startRunScript(eii):                
    acm.RunModuleWithParameters('ABSAPortfolioSwapMTM', acm.GetDefaultContext()) 
'''================================================================================================
================================================================================================'''
