'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_STL_BUILDER_OPTIONS
PROJECT                 :       Front Cache
PURPOSE                 :       Describes to a settlement builder how to construct a settlement
DEPARTMENT AND DESK     :       All Departments and all Desks.
DEVELOPER               :       Andy + Aaron
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
import FC_ENUMERATIONS as ENUMERATIONS

'''----------------------------------------------------------------------------------------------------------
Class containing the Builder Option Properties
----------------------------------------------------------------------------------------------------------'''
class FC_DATA_STL_BUILDER_OPTIONS(object):

    #Constructor
    def __init__(self):
        
        #reset the fields
        self._buildSettlementData=True
        self._buildControlMeasures = False
        self._serializationType=None
        
    #**********************************************************#
    #Properties
    #*********************************************************#
    #BuildSettlementData
    @property
    def BuildSettlementData(self):
        return self._buildSettlementData
    
    @BuildSettlementData.setter
    def BuildSettlementData(self, value):
        self._buildSettlementData = value
        
    #SerializationType
    @property
    def SerializationType(self):
        return self._serializationType
    
    @SerializationType.setter
    def SerializationType(self, value):
        self._serializationType = value

    #BuildControlMeasures
    @property
    def BuildControlMeasures(self):
        return self._buildControlMeasures
    
    @BuildControlMeasures.setter
    def BuildControlMeasures(self, value):
        self._buildControlMeasures = value        
