
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_TRD_SCALAR
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents the container for trade scalar data
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#

import FC_DATA_BASE
from FC_UTILS import FC_UTILS as UTILS

class FC_DATA_TRD_SCALAR(FC_DATA_BASE.FC_DATA_BASE): 
    
    
    
    
    #**********************************************************#
    #Properties
    #*********************************************************#
    #FTrade - get from the fTree proxy to ensure the same object is used
    @property
    def FTrade(self):
        return self.GetFObject()
        
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, trade):
        if not trade:
            raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED)
        else:
            """if trade.Oid() in (87083353,87083354):
                worksheetName = 'FC_TRADE_SCALAR_OVERRIDE'
            else:"""
            worksheetName = UTILS.Constants.fcGenericConstants.FC_TRADE_SCALAR

            #Construct the base class
            FC_DATA_BASE.FC_DATA_BASE.__init__(self, worksheetName)
            
            #Set the FTreeProxy - for trade scalar this is the top row in the trade worksheet
            self._fTreeProxy = FC_DATA_BASE.GetTopLevelNodeTreeProxy(worksheetName, trade)
   
    #**********************************************************#
    #Methods
    #*********************************************************#
    #GetFObject override 
    def GetFObject(self):
        if self._fTreeProxy and self._fTreeProxy.Item() and self._fTreeProxy.Item().Trade():
            return self._fTreeProxy.Item().Trade()
