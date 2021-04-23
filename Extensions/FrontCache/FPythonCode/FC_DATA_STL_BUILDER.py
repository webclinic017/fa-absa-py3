'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_STL_BUILDER
PROJECT                 :       Front Cache
PURPOSE                 :       Settlement data builder for creating settlement objects
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Andy + Aaron
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#
from datetime import datetime
import FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
from FC_DATA_STL import FC_DATA_STL as fcDataSettlement
from FC_DATA_STL_DATA import FC_DATA_STL_DATA as fcDataSettlementData
#*********************************************************#
#Class Definition
#*********************************************************#
class FC_DATA_STL_BUILDER():
    #Fields
    _innerSettlement = None
    
    #Constructor
    def __init__(self, settlementNumber):
        self._innerSettlement = fcDataSettlement(settlementNumber)
    
    #Methods
    #Create the trade static data
    def CreateData(self):
        if not self._innerSettlement:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_STL_CONTAINER_DNE)
        else:
            self._innerSettlement.Data = fcDataSettlementData(self._innerSettlement.FSettlement)
            
        return self
        
    #Calls calculate on the inner trade container and return the container
    def CalculateAndBuild(self):
        if not self._innerSettlement:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_STL_CONTAINER_DNE)
        else:
            startTime = datetime.now()
            self._innerSettlement.Calculate()
            endTime = datetime.now()
            self._innerSettlement.SettlementBuildTime = FC_UTILS.getLapsedTimeInSeconds(startTime, endTime)
            return self._innerSettlement
        
        
        
 
