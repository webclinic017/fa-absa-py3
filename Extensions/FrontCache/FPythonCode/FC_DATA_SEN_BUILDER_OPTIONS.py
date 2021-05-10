
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_SEN_BUILDER_OPTIONS
PROJECT                 :       Front Cache
PURPOSE                 :       Describes to a sensitivity builder how to construct a sensitivity
DEPARTMENT AND DESK     :       All Departments and all Desks.
DEVELOPER               :       Gavin Wienand
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
import FC_ENUMERATIONS as ENUMERATIONS

'''----------------------------------------------------------------------------------------------------------
Class containing the Builder Option Properties
----------------------------------------------------------------------------------------------------------'''
class FC_DATA_SEN_BUILDER_OPTIONS(object):

    #Constructor
    def __init__(self):
        
        #reset the fields
        self._buildSensitivityData=True
        self._serializationType=None

    #**********************************************************#
    #Properties
    #*********************************************************#
    #BuildSensitivityData
    @property
    def BuildSensitivityData(self):
        return self._buildSensitivityData
    
    @BuildSensitivityData.setter
    def BuildSensitivityData(self, value):
        self._buildSensitivityData = value

    #SerializationType
    @property
    def SerializationType(self):
        return self._serializationType
    
    @SerializationType.setter
    def SerializationType(self, value):
        self._serializationType = value
