"""-----------------------------------------------------------------------
MODULE
    PreviousBusinessDayData

DESCRIPTION

    Date                : 2012-09-19
    Purpose             : Returns the data using virtual trading manager for a specific date
    Department and Desk : Prime Services
    Requester           : Danilo Mantoan
    Developer           : Nidheesh Sharma
    CR Number           : 556348

ENDDESCRIPTION
-----------------------------------------------------------------------"""

import acm

#Function to check if object is a number
def Is_Number(object):
    try:
        if object != object:
            isNumber = False
        else:
            object = float(object)
            isNumber = True
    except:
        isNumber = False

    return isNumber


#Function to create the virtual trading manager
def Get_Trading_Manager_Column_Value(queryFolder, date, columnNames, setPrevBusDay = False, grouper = None):
    ''' Return a dictionary of grouper rownames (default will be instruments) mapped to a list of column values corresponding to the list of column names.
    '''
    calculationSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
    calculationSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calculationSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', date)

    if setPrevBusDay:
        calculationSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'PrevBusDay')

    topNode = calculationSpace.InsertItem(queryFolder)
    if grouper:
        topNode.ApplyGrouper(grouper)
    calculationSpace.Refresh()

    valueDictionary = {}
    instrumentIterator = topNode.Iterator().FirstChild()
    while instrumentIterator:
        rowName = instrumentIterator.Tree().Item().StringKey()

        # Create a list of column values corresponding to column names which will get updated in the dictionary
        columnValues = []
        for columnName in columnNames:
            value = 0
            value = calculationSpace.CalculateValue(instrumentIterator.Tree(), columnName)
            try:
                value = value.Number()
            except:
                value = value

            # If a value is a NaN, # or #QNaN return 0
            if Is_Number(value):
                columnValues.append(value)
            else:
                columnValues.append(0)

        valueDictionary[rowName] = columnValues
        instrumentIterator = instrumentIterator.NextSibling()

    calculationSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    calculationSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    if setPrevBusDay:
        calculationSpace.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')

    return valueDictionary


def ReturnClosingMarketValue(trade, previousBusinessDate):
    data = Get_Trading_Manager_Column_Value(trade, previousBusinessDate, ['Closing Market Value'])
    closingMarketValue = 0.0
    for row in data:
        closingMarketValue = data[row][0]

    return closingMarketValue

