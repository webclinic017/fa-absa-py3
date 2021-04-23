
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_SEN_BUILDER
PROJECT                 :       Front Cache
PURPOSE                 :       Sensitivity data builder for creating sensitivity objects
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Gavin Wienand
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#
from datetime import datetime
import FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
from FC_DATA_SEN import FC_DATA_SEN as fcDataSensitivitiy
from FC_DATA_SEN_CALC import FC_DATA_SEN_CALC as fcDataSensitivityCalculation
#*********************************************************#
#Class Definition
#*********************************************************#
class FC_DATA_SEN_BUILDER():
    #Fields
    _innerObject = None
    
    #Constructor
    def __init__(self, objectNumber, sensType, portfolioName=None, portfolioNumber=None):
        self._innerObject = fcDataSensitivitiy(objectNumber, sensType, portfolioName, portfolioNumber)
        self._sensType = sensType

    #Methods
    #Create the Portfolio Sheet data   
    def CreateSensitivityCalc(self):
        if not self._innerObject:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_TRADE_DNE)
        else:
            self._innerObject.SensitivityWorkbook = fcDataSensitivityCalculation(self._innerObject, self._sensType)
        return self

    #Calls calculate on the inner trade container and return the container
    def CalculateAndBuild(self):
        if not self._innerObject:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_STL_CONTAINER_DNE)
        else:
            startTime = datetime.now()
            self._innerObject.Calculate()
            endTime = datetime.now()
            self._innerObject.ObjectBuildTime = FC_UTILS.getLapsedTimeInSeconds(startTime, endTime)
            return self._innerObject
