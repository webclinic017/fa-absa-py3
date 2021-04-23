""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FPortfolioRouter.py"
"""--------------------------------------------------------------------------
MODULE
    FPortfolioRouter
    
    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Utilities for getting a Portfolio from a Hierarchy Table.
    Main functions: GetPortfolio and GetDefaultPortfolio.
        GetPortfolio: Retrieve a portfolio from the Hierarchy Table using a Trade as input.
        GetDefaultPortfolio: Fallback to the Default Portfolio on the Hierarchy Table. 
    HierarchyTable: name of the methods to use should be stored in Column Description, separated by '.'
-----------------------------------------------------------------------------"""

import acm
import HierarchyHelpers


def SetPortfolio(trade, hierarchyTableName='Portfolio Router', resultColumn = 'Portfolio'):
    portfolio = GetPortfolio(trade, hierarchyTableName, resultColumn)
    if portfolio:
        trade.Portfolio(portfolio)


def GetDefaultPortfolio(hierarchyTableName='Portfolio Router'):
    trade = None
    return GetPortfolio(trade, hierarchyTableName)

def GetPortfolio(trade, hierarchyTableName='Portfolio Router', resultColumn = 'Portfolio'):
    inputColumns = _GetInputAttrFromTrade(trade, hierarchyTableName)
    del inputColumns[resultColumn]
    columnNames = [key for key in inputColumns.keys()]
    columnValues = [value for value in inputColumns.values()]
    tree = HierarchyHelpers.GetTree( hierarchyTableName, columnNames)
    result = HierarchyHelpers.GetTreeResult( tree, columnValues )
    return result.Result()[resultColumn].DataValueVA()
        
def _GetInputAttrFromTrade(trade, hierarchyTableName):
    hierarchyTable = acm.FHierarchy[hierarchyTableName]
    hierarchyType = hierarchyTable.HierarchyType()
    columns = hierarchyType.HierarchyColumnSpecifications()
    if trade:
        inputColumns = dict([(column.Name(), _GetAttrValue(trade, column.Description())) for column in columns])
    else: 
        #Default Portfolio case
        inputColumns = dict([(column.Name(), None) for column in columns])
    return inputColumns
    
def _GetAttrValue(obj, name):
    try:
        for attr in name.split('.'):
            obj = getattr(obj, attr)()
        return obj
    except AttributeError as e:
        raise e
    
