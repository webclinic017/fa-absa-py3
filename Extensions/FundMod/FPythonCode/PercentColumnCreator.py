
"""-------------------------------------------------------------------------------------------------------
MODULE
    PercentColumnCreator - 

    (c) Copyright 2011 by Sungard FRONT ARENA. All rights reserved.

DESCRIPTION
    FAUX based dialog that enables users to create percent columns from within a portfolio sheet
    One new column definition and one new extension attribute will be created when run
-------------------------------------------------------------------------------------------------------"""

import acm
import FLogger
from ColumnCreator import ColumnCreator

class PercentColumnCreator(ColumnCreator):

    PCT = 'Pct'
    NAMESPACE = '%'
    PARAMETERS = 'PercentageColumns'
    ACCOUNTING_CURRENCY = 'Accounting Curr'
    POSITION_CURRENCY_CHOICE = 'PosCurrChoice'
    AGGREGATE_CURRENCY_CHOICE = 'AggCurrChoice'
    FORMAT = 'Percent'
    LOGGER = FLogger.FLogger(__name__)
    
    def __init__(self, eii):
        self.shell = None
        self.activeSheet = None
        self.column = None
        self.context = None
        self.columnId = None
        self.module = None
	self.attrs = None
        ColumnCreator.__init__(self, eii)
    
    def CreateExtensionAttribute(self, extensionId, attr):
        pass
        
    def NewColumnPreffix(self):
        return ''.join((self.prefix, self.PCT))
            
    def NewAttributeId(self, attr):
        return attr
        
    def NewParametersFixedValues(self):
        return [self.POSITION_CURRENCY_CHOICE + '=' + self.ACCOUNTING_CURRENCY, \
                self.AGGREGATE_CURRENCY_CHOICE + '=' + self.ACCOUNTING_CURRENCY]

class RatioOfRootColumnCreator(PercentColumnCreator):

    TREE_DEPENDENT_POST_PROCESSING = 'RatioOfRoot'
    
    def __init__(self, eii):
        self.prefix = 'Root'
        PercentColumnCreator.__init__(self, eii)

class RatioOfParentColumnCreator(PercentColumnCreator):

    TREE_DEPENDENT_POST_PROCESSING = 'RatioOfParent'
    
    def __init__(self, eii):
        self.prefix = 'Parent'
        PercentColumnCreator.__init__(self, eii)
        
def TopLevel(eii):        
    creator = RatioOfRootColumnCreator(eii)
    if creator.IsValidColumn():
        creator.CreateColumn()

def ParentLevel(eii):        
    creator = RatioOfParentColumnCreator(eii)
    if creator.IsValidColumn():
        creator.CreateColumn()
