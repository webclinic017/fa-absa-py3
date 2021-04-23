"""-----------------------------------------------------------------------------
PURPOSE                 :  Updates the CFD Rate Indices prices
DEPATMENT AND DESK      :  Prime Services, CFD
REQUESTER               :  Francois Henrion
DEVELOPER               :  Francois Truter
CR NUMBER               :  565934
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer              Description
--------------------------------------------------------------------------------
2011-02-10 565934    Francois Truter        Initial Implementation
"""

import acm

def _isNumber(object):
    try:
        if object != object:
            isNumber = False
        else:
            object = float(object)
            isNumber = True
    except:
        isNumber = False
    
    return isNumber

def _getPrice(instrument, currency, date, market):
    query = "instrument = '%(instrument)s' and currency = '%(currency)s' and day = '%(day)s' and market = '%(market)s'" % \
        {'instrument': instrument.Name(), 'currency': currency.Name(), 'day': date, 'market': market.Name()}
    message = 'Query returned more than one Price for %(instrument)s, %(currency)s, %(day)s, %(market)s' % \
        {'instrument': instrument.Name(), 'currency': currency.Name(), 'day': date, 'market': market.Name()}
    return acm.FPrice.Select01(query, message)
    
def _updateRate(instrument, date, rate):
    SPOT_MARKET = acm.FMarketPlace['SPOT']
    currency = instrument.Currency()
    updated = False
    prevRate = None
    message = ''
    
    latestPrice = None
    for price in instrument.Prices():
        if price.Market() == SPOT_MARKET and price.Currency() == currency and (not latestPrice or latestPrice.Day() < price.Day()):
            latestPrice = price
            
    if latestPrice and date >= latestPrice.Day():
        message = 'Updating rate from %.6f ' % latestPrice.Settle()
        latestPrice.Day(date)
        latestPrice.Settle(rate)
        latestPrice.Commit()
    else:
        try:  
            price = _getPrice(instrument, currency, date, SPOT_MARKET)
            if not price:
                price = acm.FPrice()
                price.Instrument(instrument)
                price.Currency(currency)
                price.Day(date)
                price.Market(SPOT_MARKET)
                message = 'New rate '
            else:
                message = 'Updating rate from %.6f ' % price.Settle()
            
            price.Settle(rate)
            price.Commit()
        except Exception, ex:
            if latestPrice:    
                message = 'Updating rate from %.6f ' % latestPrice.Settle()
                latestPrice.Day(date)
                latestPrice.Settle(rate)
                latestPrice.Commit()
            else:
                message = 'Could not update rate '
    
    message += 'for %(instrument)s %(date)s: %(rate).6f' % {'instrument': instrument.Name(), 'date': date, 'rate': rate}
    print(message)
    
def _insertRate(feeDict, instrument, rate):
    if _isNumber(rate):
        rate = round(rate, 6)
        if not instrument in feeDict:
            feeDict[instrument] = rate
        else:
            oldRate = feeDict[instrument]
            if rate > oldRate:
                feeDict[instrument] = rate
    
def _readRates(item, feeDict, date):
    underlyingGrouper = acm.FAttributeGrouper('Instrument.SLUnderlying')
    calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Inception')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', date)
    
    top_node = calc_space.InsertItem(item)
    top_node.ApplyGrouper(underlyingGrouper)
    calc_space.Refresh()
    
    feeColumn = 'Fee Weighted Average'    
    instrumentIterator = top_node.Iterator().FirstChild()
    while instrumentIterator:
        instrumentName = instrumentIterator.Tree().Item().StringKey()
        instrument = acm.FInstrument[instrumentName]
        if not instrument:
            raise Exception('Could not load instrument [%s].' % instrumentName)
        
        rate = calc_space.CalculateValue(instrumentIterator.Tree(), feeColumn)
        _insertRate(feeDict, instrument, rate)
        
        instrumentIterator = instrumentIterator.NextSibling()
        
    return feeDict
    
def _getSblQueryFolder(date, instruments):
    sblQuery = None
    
    portfolioQuery = acm.CreateFASQLQuery('FPhysicalPortfolio', 'AND')
    op = portfolioQuery.AddOpNode('AND')
    op.AddAttrNode('AdditionalInfo.SL_Portfolio_Type', 'EQUAL', 'Fee')
    op.AddAttrNode('AdditionalInfo.SL_Sweeping', 'EQUAL', True)
    portfolios = portfolioQuery.Select()
    
    if portfolios:
        sblQuery = acm.CreateFASQLQuery('FTrade', 'AND')
        op = sblQuery.AddOpNode('OR')
        for portfolio in portfolios:
            op.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
            
        op = sblQuery.AddOpNode('AND')
        op.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'SecurityLoan'))
        
        op = sblQuery.AddOpNode('AND')
        op.AddAttrNode('Instrument.AdditionalInfo.SL_ExternalInternal', 'EQUAL', 'External')
        
        op = sblQuery.AddOpNode('AND')
        op.AddAttrNode('MirrorTrade.Portfolio.Name', 'EQUAL', 'ACS - Script Lending')
            
        op = sblQuery.AddOpNode('AND')
        for status in ['Terminated', 'Void', 'Simulated', 'Confirmed Void']:
            op.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', status))
        
        op = sblQuery.AddOpNode('AND')
        op.AddAttrNode('Instrument.StartDate', 'LESS_EQUAL', str(date))
                
        op = sblQuery.AddOpNode('AND')
        op.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', str(date))
        
        op = sblQuery.AddOpNode('OR')
        for instrument in instruments:
            op.AddAttrNode('Instrument.Underlying.Oid', 'EQUAL', instrument.Oid())
        
    return sblQuery
    
def _getRateIndices():
    query = acm.CreateFASQLQuery('FAdditionalInfo', 'AND')
    op = query.AddOpNode('AND')
    op.AddAttrNode('addInf.Name', 'EQUAL', 'PSShortPremCost')
    
    instruments = {}
    
    for addInfo in query.Select():
        instrument = acm.FInstrument[addInfo.Recaddr()]
        rateIndex = acm.FRateIndex[addInfo.FieldValue()]
        instruments[instrument] = rateIndex
        
    return instruments    

def _toAcmDate(aelDate):
    [y, m, d] = aelDate.to_ymd()
    return acm.Time().DateFromYMD(y, m, d)
    
def enableCustomDate(index, fieldValues):
    ael_variables[2][9] = (fieldValues[1] == CUSTOM_DATE)
    return fieldValues

PORTFOLIO_KEY = 'PORTFOLIO'
DEFAULT_POTFOLIO = acm.FPhysicalPortfolio['SBL LinTradingCFD Loans ACS']
DATE_KEY = 'DATE'
CUSTOM_DATE_KEY = 'CUSTOM_DATE'
CUSTOM_DATE = 'Custom Date'
TODAY_STR = 'Today'
TODAY_DATE = acm.Time().DateNow()
YESTERDAY_STR = 'Yesterday'
YESTERDAY_DATE = acm.Time().DateAddDelta(TODAY_DATE, 0, 0, -1)
DATE_DICT = {CUSTOM_DATE: None, TODAY_STR: TODAY_DATE, YESTERDAY_STR: YESTERDAY_DATE}
DATE_LIST = DATE_DICT.keys()
DATE_LIST.sort()
RATE_FLOOR_KEY = 'RATE_FLOOR'

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [PORTFOLIO_KEY, 'Primary Portfolio', 'FPhysicalPortfolio', None, DEFAULT_POTFOLIO, 1, 1, 'The portfolio where the rates should be read from', None, 1],
    [DATE_KEY, 'Date', 'string', DATE_LIST, TODAY_STR, 1, 0, 'Date for which rates should be updated', enableCustomDate, 1],
    [CUSTOM_DATE_KEY, 'Custom Date', 'date', None, None, 0, 0, 'Custom Date: YYYY-MM-DD', None, 0],
    [RATE_FLOOR_KEY, 'Rate Floor', 'float', None, 0.543, 0, 0, 'The minimum rate to be assigned', None, 1]
]

def ael_main(parameters):
    try:
        dateStr = parameters[DATE_KEY]
        if dateStr == CUSTOM_DATE:
            runDate = parameters[CUSTOM_DATE_KEY]
            inputType = type(runDate)
            
            from ael import ael_date
            if inputType == ael_date:
                runDate = _toAcmDate(runDate)
        elif dateStr in DATE_DICT:
            runDate = DATE_DICT[dateStr]
        else:
            raise Exception('Unknown date: ' + dateStr)
            
        rateFloor = parameters[RATE_FLOOR_KEY]
        
        rateIndexDict = _getRateIndices()
            
        primaryPortfolio = parameters[PORTFOLIO_KEY]
        
        feeDict = {}
        _readRates(primaryPortfolio, feeDict, runDate)
        
        sblQuery = _getSblQueryFolder(runDate, rateIndexDict.keys())
        if sblQuery:
            _readRates(sblQuery, feeDict, runDate)
        
        instruments = rateIndexDict.keys()
        instruments.sort()
        
        for instrument in instruments:
            index = rateIndexDict[instrument]
            if instrument in feeDict:
                rate = feeDict[instrument]
                if rateFloor and rate < rateFloor:
                    rate = rateFloor
                _updateRate(index, runDate, rate)
            else:
                print('No new rate for %(instrument)s for %(date)s' % {'instrument': instrument.Name(), 'date': runDate})
                
    except Exception, ex:
        print('ERROR:', str(ex))
    else:
        print('SUCCESS: The process completed without any errors.')
