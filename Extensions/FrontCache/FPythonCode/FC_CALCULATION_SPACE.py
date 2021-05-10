
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_CALCULATION_SPACE
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents a wrapper for the acm calculation spaces
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
import acm
from FC_UTILS import FC_UTILS as UTILS

class FC_CALCULATION_SPACE(): 
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, context, worksheet, clearItemThreshold):
        self._clearItemThreshold = clearItemThreshold
        self._itemCount = 0
        self._innerCalcSpace = None
        
        #check the worksheet instance
        if not worksheet:
            raise Exception(UTILS.Constants.fcExceptionConstants.VALID_INSTANCE_OF_WORKBOOK_SHEET_MUST_BE_PROVIDED)
        
        #Construct and clear the inner calcSpace
        if worksheet.IsKindOf(UTILS.Constants.fcGenericConstants.F_TRADE_SHEET):
            self._innerCalcSpace = acm.Calculations().CreateCalculationSpace(context, UTILS.Constants.fcGenericConstants.F_TRADE_SHEET)
        elif worksheet.IsKindOf(UTILS.Constants.fcGenericConstants.FPORTFOLIOSHEET):
            self._innerCalcSpace = acm.Calculations().CreateCalculationSpace(context, UTILS.Constants.fcGenericConstants.FPORTFOLIOSHEET)
        elif worksheet.IsKindOf(UTILS.Constants.fcGenericConstants.F_MONEYFLOW_SHEET):
            self._innerCalcSpace = acm.Calculations().CreateCalculationSpace(context, UTILS.Constants.fcGenericConstants.F_MONEYFLOW_SHEET)
        elif worksheet.IsKindOf(UTILS.Constants.fcGenericConstants.F_SETTLEMENT_SHEET):
            self._innerCalcSpace = acm.Calculations().CreateCalculationSpace(context, UTILS.Constants.fcGenericConstants.F_SETTLEMENT_SHEET)
        else:
            raise Exception(UTILS.Constants.fcExceptionConstants.WORKSHEETS_OF_TYPE_S_NOT_SUPPORTED % (sheetName))
        self._innerCalcSpace.Clear()
        
    #**********************************************************#
    #Properties
    #*********************************************************#
    #The ACM calculation space
    @property
    def InnerCalcSpace(self):
        return self._innerCalcSpace
        
    #Number of items inserted in the calc space
    @property
    def ItemCount(self):
        return self._itemCount

    #Get or set whether the threshold for clearing items in the calc space (-1 disables)
    @property
    def ClearItemThreshold(self):
        return self._clearItemThreshold
    
    @ClearItemThreshold.setter
    def ClearItemThreshold(self, value):
        self._clearItemThreshold = value
        
    #**********************************************************#
    #Methods
    #*********************************************************#
    #insert an fObject into the and return a top level node
    def InsertItem(self, fObject):
        #check the fObject instance
        if not fObject:
            raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FOBJECT_INSTANCE_MUST_BE_PROVIDED)
        elif not self._innerCalcSpace:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_CALC_SPACE_NOT_CREATED)
        else:
            #Clear the items in the calc space
            if self._clearItemThreshold > -1 and self._itemCount>=self._clearItemThreshold:
                self.Clear()
            
            #Now insert the item
            node =  self._innerCalcSpace.InsertItem(fObject)
            self._itemCount = self._itemCount + 1
            return node
                
    #forces the inner calc space to be cleared
    def Clear(self):
        if not self._innerCalcSpace:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_CALC_SPACE_NOT_CREATED)
        else:
            self._innerCalcSpace.Clear()
            self._itemCount = 0
            
           
    #forces the inner calc space to be refreshed
    def Refresh(self):
        if not self._innerCalcSpace:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_CALC_SPACE_NOT_CREATED)
        else:
            self._innerCalcSpace.Refresh()
    
    #apply global Trading Manager Simulation
    def SimulateGlobalValue(self, columnId, value):
        if not self._innerCalcSpace:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_CALC_SPACE_NOT_CREATED)
        else:
            self._innerCalcSpace.SimulateGlobalValue(columnId, value)
    
    #remove global Trading Manager Simulation
    def RemoveGlobalSimulation(self, columnId):
        if not self._innerCalcSpace:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_CALC_SPACE_NOT_CREATED)
        else:
            self._innerCalcSpace.RemoveGlobalSimulation(columnId)
    
    #remove Trading Manager Simulation
    def RemoveSimulation(self, fObject, columnId):
        if not self._innerCalcSpace:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_CALC_SPACE_NOT_CREATED)
        else:
            self._innerCalcSpace.RemoveSimulation(fObject, columnId)
