"""----------------------------------------------------------------------------
MODULE
    FQuoteSheetHooks - Input-and post input hooks for quote sheets.

    (c) Copyright 2014 by SunGard FRONT ARENA. All rights reserved.
 ---------------------------------------------------------------------------"""
import acm
                     
""" Changes Spread Bias Factor according 
    to Spread Bias
"""
def onInputSpreadBias(row, col, calcval, str, operation):
    quoteController = row.QuoteController()
    dataSpace = quoteController.DataSpace()
    dataSource = dataSpace.GetDataSource('Spread Bias Factor', 0)
    if str == 'Bid': 
        dataSource.Set(0.0)
    elif str == 'Mid': 
        dataSource.Set(0.5)
    elif str == 'Ask': 
        dataSource.Set(1.0)

    # ignore input in this cell
    return 0

