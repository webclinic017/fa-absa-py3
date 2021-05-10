'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_STL_DATA
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents the container for settlement static data
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Andy + Aaron
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#
from FC_UTILS import FC_UTILS as UTILS
import FC_DATA_BASE
class FC_DATA_STL_DATA(FC_DATA_BASE.FC_DATA_BASE):
    
        
    #**********************************************************#
    #Properties
    #*********************************************************#
    #FSettlement - get from the fTree proxy to ensure the same object is used
    @property
    def FSettlement(self):
        return self.GetFObject()
        
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, settlement):
        worksheetName = UTILS.Constants.fcGenericConstants.FC_SETTLEMENT_DATA
        if not settlement:
            raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FSTL_INSTANCE_MUST_BE_PROVIDED)
        else:
            #Construct the base class
            FC_DATA_BASE.FC_DATA_BASE.__init__(self, worksheetName)
            
            #Set the FTreeProxy - for settlement static this is the top row in the settlement worksheet
            self._fTreeProxy = FC_DATA_BASE.GetTopLevelNodeTreeProxy(worksheetName, settlement)            
    #**********************************************************#
    #Methods
    #*********************************************************#
    #GetFObject override 
    def GetFObject(self):
        if self._fTreeProxy and self._fTreeProxy.Item() and self._fTreeProxy.Item().Settlement():
            return self._fTreeProxy.Item().Settlement()
        
#Test
'''
import FC_ENUMERATIONS
t = acm.FSettlement[18543398]
tradeStatic = FC_DATA_TRD_STATIC(t)
tradeStatic.Calculate()
tradeStatic.SerializeCalculationResults(FC_ENUMERATIONS.SerializationType.XML)
print tradeStatic.SerializedCalculationResults

'''
