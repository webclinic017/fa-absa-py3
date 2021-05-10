
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_SELECTION
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will contain the data based on any data selection method implemented
                                int he getDataSelection method. The selection will be done based on the scope
                                number and name.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules
----------------------------------------------------------------------------------------------------------'''
from FC_DATA_SELECTION_AEL_ASQL import FC_DATA_SELECTION_AEL_ASQL as DATA_SELECTION_AEL_ASQL

'''----------------------------------------------------------------------------------------------------------
Class defining the DATA SELECTION
----------------------------------------------------------------------------------------------------------'''
class FC_DATA_SELECTION():
    def __init__(self, selectionType, scopeNumber, scopeName, isEOD, tradeCreateCutOffDate):
        self._selectionType = selectionType
        self._scopeNumber = scopeNumber
        self._scopeName = scopeName
        self._isEOD = isEOD
        self._tradeCreateCutOffDate = tradeCreateCutOffDate
        self.dataSelectionClass = None
    
    def getDataSelection(self):
        if not self.dataSelectionClass:
            self.dataSelectionClass = DATA_SELECTION_AEL_ASQL(self._selectionType, self._scopeNumber, self._scopeName, self._isEOD, self._tradeCreateCutOffDate)
            
        aelAsqlDataSelection = self.dataSelectionClass.getAelASQLDataSelection()
        
        aelAsqlTradeSelection = [data[0] for data in aelAsqlDataSelection]
        return aelAsqlTradeSelection

    def getDataSelectionReturnNameandNumber(self):
        if not self.dataSelectionClass:
            self.dataSelectionClass = DATA_SELECTION_AEL_ASQL(self._selectionType, self._scopeNumber, self._scopeName, self._isEOD, self._tradeCreateCutOffDate)

        aelAsqlDataSelection = self.dataSelectionClass.getAelASQLDataSelection()

        aelAsqlTradeSelection = [data for data in aelAsqlDataSelection]
        return aelAsqlTradeSelection
        
'''
from FC_UTILS import FC_UTILS as UTILS
UTILS.Initialize('FC_RT_01_ATS')
t = FC_DATA_SELECTION('PORTFOLIO_TRADES', 13, None, 0, '2014-04-24')
data = t.getDataSelection()
print type(data[0])
'''
