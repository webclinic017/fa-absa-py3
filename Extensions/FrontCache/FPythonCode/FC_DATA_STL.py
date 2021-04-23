'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_STL
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents a Settlement data container
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Andy + Aaron
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#
import acm
import FC_UTILS
import FC_SERIALIZATION
from FC_UTILS import FC_UTILS as UTILS
from xml.etree.ElementTree import Element, tostring
from FC_DATA_ABSTRACT import FC_DATA_ABSTRACT as DATA_ABSTRACT
 
class FC_DATA_STL(DATA_ABSTRACT):
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, settlementNumber):
        #find the settlement
        settlement = acm.FSettlement[settlementNumber]
        if not settlement:
            raise Exception(UTILS.Constants.fcExceptionConstants.STL_NOT_FOUND % str(settlementNumber))
        else:
            self._fSettlement = settlement
            
        #reset all the inner data containers
        self._data = None
        self._serializationType = None
        self._serializedData = None
        
        #performanceCounters
        self._settlementBuildTime = 0
        
    #**********************************************************#
    #Properties
    #*********************************************************#
    #FSettlement
    @property
    def FSettlement(self):
        return self._fSettlement
    
    #Data
    @property
    def Data(self):
        return self._data
    
    @Data.setter
    def Data(self, value):
        self._data = value
    
    @property
    def DataCount(self):
        if self.Data:
            return 1
        else:
            return 0
            
            
    
    #SerializationType
    @property
    def SerializationType(self):
        return self._serializationType
    
    @SerializationType.setter
    def SerializationType(self, value):
        self._serializationType = value
    
        
    #SerializedData
    @property
    def SerializedData(self):
        return self._serializedData
    
    #SettlementBuildTime
    @property
    def SettlementBuildTime(self):
        return self._settlementBuildTime
    
    @SettlementBuildTime.setter
    def SettlementBuildTime(self, value):
        self._settlementBuildTime = value
        
        
    #**********************************************************#
    #Methods
    #*********************************************************#
    def Calculate(self):
        self.calcStatic()                        
          
    def Serialize(self):
        self._serializedData = FC_SERIALIZATION.SerializeSettlement(self.SerializationType, self)
        
    
    def GetInfoAsXml(self):
        rootElement  = Element(UTILS.Constants.fcGenericConstants.SETTLEMENT_INFO)
        FC_UTILS.AddXmlChildElement(rootElement, UTILS.Constants.fcGenericConstants.SETTLEMENT_BUILD_TIME, str(self.SettlementBuildTime))
        FC_UTILS.AddXmlChildElement(rootElement, UTILS.Constants.fcGenericConstants.STATIC_COUNT, str(self.DataCount))
        return tostring(rootElement)
        
    def GetErrorsAsXml(self):
        rootElement  = Element(UTILS.Constants.fcGenericConstants.SETTLEMENT_ERRORS)
        return tostring(rootElement)
    def calcStatic(self):
        #Calc static
        if self.Data:
            try:
                self.Data.Calculate()
                #Special step to add the settlement domain to the calculation results
                self.Data.CalculationResults[UTILS.Constants.fcGenericConstants.TRADE_DOMAIN] = FC_UTILS.FC_UTILS.FrontArenaInstanceName
            except Exception, e:
                raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_CALC_STATIC_ATTR_S %(str(self._fSettlement.Oid()), str(e)))
    
