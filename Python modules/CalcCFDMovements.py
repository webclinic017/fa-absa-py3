"""----------------------------------------------------------------------------
MODULE
    CalcCFDMovements

DESCRIPTION
    Date                : 2015-03-10
    Purpose             : Calculate start and end prices, and 
                          Value Weighted Average Price for all 
                          CFD trades in specified portfolios..
    Department and Desk : Prime Services
    Requester           : Tich Mbiri
    Developer           : Rhys Davies
    CR Number           : 699989
ENDDESCRIPTION

HISTORY
===============================================================================
Date       Change no    Developer          Description
-------------------------------------------------------------------------------
2015-03-10  2686452     Rhys Davies        Initial Implementation

"""

import acm
calendar = acm.FCalendar['ZAR Johannesburg']

ael_variables = [
                    ['StartDate', 'Start Date', 'time', None, calendar.AdjustBankingDays(acm.Time().DateToday(), -2), 1, 0, 'Start Date for new trades.', None, 1],
                    ['EndDate', 'End Date', 'time', None, calendar.AdjustBankingDays(acm.Time().DateToday(), -1), 1, 0, 'End Date for new trades.', None, 1],
                    ['Instruments', 'Underlying Instruments', 'FStock', None, 'ZAR/AGL', 1, 1, 'All underlying instruments to run report for', None, 1],
                    ['QueryFolder', 'Query Folder', 'FStoredASQLQuery', None, 'Prime_CFD_TRADES_1', 1, 0, 'Query Folder to use as base query', None, 1]
                ]


def ael_main(parameters):
    startDate = parameters['StartDate']
    endDate = parameters['EndDate']
    instruments = parameters['Instruments']
    queryFolder = parameters['QueryFolder']
    simulatedValues = {
        'Portfolio Profit Loss Start Date': 'Custom Date', 
        'Portfolio Profit Loss Start Date Custom': startDate,
        'Portfolio Profit Loss End Date': 'Custom Date', 
        'Portfolio Profit Loss End Date Custom': endDate,
    }
    
    for instrument in instruments:
        try:
            query = queryFolder.Query()
        except:
            print 'Please provide a valid Query Folder name'
            return
        query.AddAttrNode('ExecutionTime', 'GREATER_EQUAL', calendar.AdjustBankingDays(startDate, 1)) # 00:00:00 is used implicitly.
        query.AddAttrNode('ExecutionTime', 'LESS_EQUAL', endDate.to_string())

        cfdInstrument = instrument.Name() + '/CFD'
        query.AddAttrNode('Instrument.Name', 'EQUAL', cfdInstrument)
        
        trades = query.Select()
        
        if len(trades) == 0:
            continue
        qtySum = 0
        qtyPriceSum = 0
        
        for trade in trades:
            qtySum += trade.Quantity()
            qtyPriceSum += trade.Quantity() * trade.Price()

        vwap = qtyPriceSum / qtySum             # Value Weighted Average Price
        
        prf = _getAdhocPortfolio(trades[0])
        startPrice = _getCalcValue(prf, cfdInstrument, 'Portfolio Profit Loss Price Start Date', simulatedValues)
        endPrice = _getCalcValue(prf, cfdInstrument, 'Portfolio Profit Loss Price End Date', simulatedValues)
        print 'Instrument\t', instrument.Name()
        print 'Start Price \t', startPrice
        print 'End Price\t', endPrice
        print 'VWAP\t\t', vwap
        print trades
    
def _getAdhocPortfolio(trade):
    """
    Returns Adhoc Portfolio to use in calculation space
    """
    portfolio = acm.FAdhocPortfolio()
    portfolio.Add(trade)
    return portfolio
    
def _getCalcValue(portfolio, instrumentName, columnName, simulatedValues):
    calcSpace = acm.FCalculationSpace('FPortfolioSheet')
    instrument = acm.FInstrument[instrumentName]
    builder = acm.Risk.CreateSingleInstrumentAndTradesBuilder(portfolio, instrument)    
    siat = builder.GetTargetInstrumentAndTrades()   # Single Instrument and Trade
    
    for (column_id, value) in simulatedValues.items():
        calcSpace.SimulateValue(portfolio, column_id, value)
    calc = calcSpace.CreateCalculation(siat, columnName)
    return calc.Value()

def CalculateValues(self):
    acm.RunModuleWithParameters('CalcCFDMovements', 'Standard')
