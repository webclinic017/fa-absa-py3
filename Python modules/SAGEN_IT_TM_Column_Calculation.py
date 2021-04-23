"""
-------------------------------------------------------------------------------------------------------------
MODULE                  :       SAGEN_IT_TM_Column_Calculation
PROJECT                 :       NOP Reporting
PURPOSE                 :       THis module will cated for any column calculation.
DEPARTMENT AND DESK     :       Market Risk
REQUASTER               :       Rishaan Ramnarain
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXXXXXX
-------------------------------------------------------------------------------------------------------------
DESCRIPTION OF MODULE:

    This module will be able to calculate Vector and Normal Trading Manager columns on any Trading sheet.

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description-
-------------------------------------------------------------------------------------------------------------
2013-09-06      XXXXXXXXXX      Heinrich Cronje                 Initial Implementation
2013-09-27      XXXXXXXXXX      Heinrich Cronje                 Front Arena Upgrade - Changed Calculation Sapce
2014-09-27      XXXXXXXXXX      Sanele Macanda                  Added a money_flow_value function that calculates 
                                                                a column value for any money flow object and the
                                                                GetValueForObj function which calculates column 
                                                                values which are derived from methond
2017-04-13      XXXXXXXXXX      Bhavik Mistry                   Upgrade 2017 - Vector column config based on 
                                                                column definition
2020-07-24      FAOPS-853       Tawanda Mukhalela               Refactored money_flow_value
-------------------------------------------------------------------------------------------------------------
"""

import acm, ael
from at_logging import getLogger

LOGGER = getLogger(__name__)
global CALC_SPACE
CALC_SPACE = None


COL_DEFINITION = 'FColumnDefinition'
COL_VECTOR_ITEM = acm.FSymbol('VectorItem')
MONEY_FLOW_CALC_SPACE = acm.Calculations().CreateCalculationSpace('Standard', 'FMoneyFlowSheet')


class SAGEN_IT_TM_Column_Calucation():
    def __init__(self, context, sheet_type, object, column_id, currencies, vector_column_flag=0):
        self.CONTEXT = context
        self.SHEET_TYPE = sheet_type
        self.OBJECT = object
        self.COLUMN_ID = column_id
        self.CURRENCIES = currencies
        self.VECTOR_COLUMN = vector_column_flag
        self.COLUMN_CONFIG = None
        self._getCalcSpace()
    
    def _getCalcSpace(self):
        global CALC_SPACE
        if not CALC_SPACE:
            #CALC_SPACE = acm.Calculations().CreateCalculationSpace(self.CONTEXT, self.SHEET_TYPE)
            CALC_SPACE = acm.FCalculationSpace(self.SHEET_TYPE)

    def _createNamedParameter(self, vector, currency):
        param = acm.FNamedParameters();
        param.AddParameter('currency', acm.FCurrency[currency])
        vector.Add(param)

    def _getNewPortfolioPLDate(self, date):
        diff = ael.date_today().days_between(date)
        newDate = ael.date_today().add_days(diff)
        return newDate
    
    def _setColumnConfig(self):
        vector = acm.FArray()
        for currency in self.CURRENCIES:
            self._createNamedParameter(vector, currency)
        
        colDef = acm.GetStandardExtension(COL_DEFINITION, self.SHEET_TYPE, self.COLUMN_ID)
        if COL_VECTOR_ITEM in colDef.Keys():
            self.COLUMN_CONFIG = acm.Sheet.Column().ConfigurationFromVectorItem(vector)
        else:
            self.COLUMN_CONFIG = acm.Sheet.Column().ConfigurationFromVector(vector)
    
    def simulateGlobalValue(self, startDate, endDate, currency):
        global CALC_SPACE
        if startDate:
            startDate = ael.date(startDate)
            startDate = self._getNewPortfolioPLDate(startDate)

            CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
            CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', startDate)
        
        if endDate:
            endDate = ael.date(endDate)
            endDate = self._getNewPortfolioPLDate(endDate)
            
            CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
            CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', endDate)
            CALC_SPACE.SimulateGlobalValue('Valuation Date', endDate)
        
        if currency:
            CALC_SPACE.SimulateValue(self.OBJECT, 'Portfolio Currency', currency)
    
    def removeGlobalSimulation(self):
        global CALC_SPACE
        CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
        CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')
        CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        CALC_SPACE.RemoveGlobalSimulation('Valuation Date')
        CALC_SPACE.RemoveSimulation(self.OBJECT, 'Portfolio Currency')

    def formatTMColumnCalculationValue(self, columnValue):
        formattedValue = 0.00
        
        try:
            formattedValue = columnValue.Number()
        except:
            try:
                formattedValue = columnValue[0].Number()
            except:
                formattedValue = columnValue
        
        if str(formattedValue) == 'nan':
            return 0.00
        return formattedValue

    def getTMCalucationColumn(self):
        global CALC_SPACE
        TMColumnCalculationValue = 0
        CALC_SPACE.Refresh()
        
        if self.VECTOR_COLUMN:
            self._setColumnConfig()
        
            TMColumnCalculation = CALC_SPACE.CreateCalculation(self.OBJECT, self.COLUMN_ID, self.COLUMN_CONFIG)
        else:
            TMColumnCalculation = CALC_SPACE.CalculateValue(self.OBJECT, self.COLUMN_ID)
        
        if TMColumnCalculation:
            try:
                TMColumnCalculationValue = TMColumnCalculation.Value()
            except:
                TMColumnCalculationValue = TMColumnCalculation
        
        return TMColumnCalculationValue


def get_TM_Column_Calculation(temp, context, sheet_type, obj_id, obj_type, column_id, currency, vector_column, start_Date, end_Date, *rest):
    tmColumnValue = 0
    
    if obj_id and str(obj_id).isdigit():
        if obj_type == 'Trade':
            object = acm.FTrade[obj_id]
        elif obj_type == 'Instrument':
            object = acm.FInstrument[obj_id]
    else:
        print('object_id is not numeric.')
        return tmColumnValue
    
    TMColumnCalculation = SAGEN_IT_TM_Column_Calucation(context, sheet_type, object, column_id, [currency], vector_column)
    
    try:
        TMColumnCalculation.simulateGlobalValue(start_Date, end_Date, currency)
        
        try:
            TMColumnCalculationValue = TMColumnCalculation.getTMCalucationColumn()
            
            tmColumnValue = TMColumnCalculation.formatTMColumnCalculationValue(TMColumnCalculationValue)
        except:
            return tmColumnValue
    finally:
        TMColumnCalculation.removeGlobalSimulation()
    
    return tmColumnValue


def money_flow_value(money_flow, end_date, column_id):
    """
    This method returns a column value for any money flow object
    """

    MONEY_FLOW_CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', end_date)
    MONEY_FLOW_CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calculation = MONEY_FLOW_CALC_SPACE.CreateCalculation(money_flow, column_id)
    value = calculation.Value()
    if hasattr(value, "IsKindOf") and value.IsKindOf(acm.FDenominatedValue):
        value = value.Number()

    return value


def GetValueForObj(column, object):
    """
    This method returns column values which are derived from methond
    """
    methodchain = str(column.Method()).split('.')
    value = object
    for method in methodchain:
        property = value.GetPropertyObject(method)
        value = property.Get()
    return value
