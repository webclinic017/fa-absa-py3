'''----------------------------------------------------------------------------------------------------------
MODULE                  :       SAGEN_IT_TM_Columns
PURPOSE                 :       This module can be called from ACM or ASQL to return any Trading Manager column
                                on any Trading Manager Sheet.
DEPARTMENT AND DESK     :       PCG
REQUASTER               :       Andrew Nobbs
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer          Requester             Description
-------------------------------------------------------------------------------------------------------------
2012-01-23      XXXXXX          Heinrich Cronje    Andrew Nobbs          Initial Implementation

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    This module can be called from ACM or ASQL to return any Trading Manager column on any Trading Manager Sheet.
    
    Two functions are required to retrieve Trading Manager columns:
    
        1.      Trading manager Calculation Space function: This function will define a calculation space for the
                Trading Manager Sheet required.
        2.      Function that calls this calculation space function and get_column_calc to retrieve the necessary
                Trading Manager columns.
'''


import acm, ael

global TS_CALC_SPACE

TS_CALC_SPACE = None

def getTradeSheetCalcSpace(*rest):
    global TS_CALC_SPACE
    if not TS_CALC_SPACE:
        TS_CALC_SPACE = acm.FCalculationSpace('FTradeSheet')
    return TS_CALC_SPACE
    
def get_column_calc(calcSpace, object, columnId):
    calc = calcSpace.CalculateValue(object, columnId)

    return calc

def calcNewPortfolioPL_Date(date):
    diff = ael.date_today().days_between(date)
    newDate = ael.date_today().add_days(diff)
    return newDate
    
def simulateGlobalValue(calcSpace, startDate, endDate, currency):
    if startDate:
        startDate = ael.date(startDate)
        startDate = calcNewPortfolioPL_Date(startDate)

        calcSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
	calcSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', startDate)
    
    if endDate:
        endDate = ael.date(endDate)
        endDate = calcNewPortfolioPL_Date(endDate)
        calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
	calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', endDate)

    if currency:
	calcSpace.SimulateValue(t, 'Portfolio Currency', currency)
    
    return calcSpace

def removeGlobalSimulation(calcSpace, trade):
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    calcSpace.RemoveSimulation(trade, 'Portfolio Currency')
    
    return calcSpace

def formatCalculatedValue(columnValue):
    try:
        value = columnValue.Value()
        try:
            return value.Number()
        except:
            return value
    except:
        return columnValue
    

def get_TradeSheet_Column(temp, tradeNbr, startDate, endDate, currency, columnId, *rest):
    value = 0

    if tradeNbr:
        t = acm.FTrade[tradeNbr]
    
    if t:
        try:
            sheetCalcSpace = simulateGlobalValue(getTradeSheetCalcSpace(), startDate, endDate, currency)
            return formatCalculatedValue(get_column_calc(sheetCalcSpace, t, columnId))
        finally:
            removeGlobalSimulation(sheetCalcSpace, t)
            pass
    return value
