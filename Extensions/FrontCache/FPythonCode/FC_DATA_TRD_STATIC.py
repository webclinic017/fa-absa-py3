
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_TRD_STATIC
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents the container for trade static data
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

class FC_DATA_TRD_STATIC(FC_DATA_BASE.FC_DATA_BASE): 
    
        
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
        worksheetName = UTILS.Constants.fcGenericConstants.FC_TRADE_STATIC
        if not trade:
            raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED)
        else:
            """if trade.Oid() in (87083353,87083354):
                worksheetName = 'FC_TRADE_STATIC_OVERRIDE'
            else:"""
            worksheetName = UTILS.Constants.fcGenericConstants.FC_TRADE_STATIC
            #Construct the base class
            FC_DATA_BASE.FC_DATA_BASE.__init__(self, worksheetName)
            
            #Set the FTreeProxy - for trade static this is the top row in the trade worksheet
            self._fTreeProxy = FC_DATA_BASE.GetTopLevelNodeTreeProxy(worksheetName, trade)
            
    #**********************************************************#
    #Methods
    #*********************************************************#
    #GetFObject override 
    def GetFObject(self):
        if self._fTreeProxy and self._fTreeProxy.Item() and self._fTreeProxy.Item().Trade():
            return self._fTreeProxy.Item().Trade()
        

#Test
'''
import FC_ENUMERATIONS
t = acm.FTrade[18543398]
tradeStatic = FC_DATA_TRD_STATIC(t)
tradeStatic.Calculate()
tradeStatic.SerializeCalculationResults(FC_ENUMERATIONS.SerializationType.XML)
print tradeStatic.SerializedCalculationResults

'''
