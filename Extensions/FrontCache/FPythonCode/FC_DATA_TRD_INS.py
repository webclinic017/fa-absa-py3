
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_TRD_INS
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents the container for trade instrument data
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

#**********************************************************#
#Class Definition
#*********************************************************#
class FC_DATA_TRD_INS(FC_DATA_BASE.FC_DATA_BASE): 
    
  
    #**********************************************************#
    #Properties
    #*********************************************************#
    #FInstrument - get from the fTree proxy to ensure the same object is used
    @property
    def FInstrument(self):
        return self.GetFObject()
    
    
        
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, trade):
        if not trade:
            raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED)
        else:
            """if trade.Oid() in (87083353,87083354):
                worksheetName = 'FC_TRADE_INSTRUMENT_OVERRIDE'
            else:"""
            worksheetName = UTILS.Constants.fcGenericConstants.FC_TRADE_INSTRUMENT

            #Construct the base class
            FC_DATA_BASE.FC_DATA_BASE.__init__(self, worksheetName)
            
            #Set the FTreeProxy - for trade instrument this is the second row (first child) in the portfolio worksheet
            self._fTreeProxy = FC_DATA_BASE.GetTopLevelNodeTreeProxy(worksheetName, trade)
        
    #**********************************************************#
    #Methods
    #*********************************************************#
    #GetFObject override 
    def GetFObject(self):
        if self._fTreeProxy and self._fTreeProxy.Item() and self._fTreeProxy.Item().Instrument():
            return self._fTreeProxy.Item().Trade().Instrument()


