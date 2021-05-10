
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_SEN_CALC
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents the container for sensitivity calculated data
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Gavin Wienand
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#

from FC_CALCULATION_SENSITIVITY import FC_CALCULATION_SENSITIVITY as sensCalculation
from FC_UTILS import FC_UTILS as UTILS
import FC_DATA_BASE
import FReportAPI
import FReportAPIBase

class FC_DATA_SEN_CALC(FC_DATA_BASE.FC_DATA_BASE):
    def __init__(self, object, sensType=UTILS.Constants.fcGenericConstants.PORTFOLIO):
        self._fObject = object
        self._reportParamBase = FReportAPI.FWorksheetReportApiParameters(includeRawData=True)
        self._reportBuilder = FReportAPIBase.FReportBuilder(self._reportParamBase)
        self._sensType = sensType

    @property
    def FObject(self):
        return self._fObject

    @property
    def FReportBuilder(self):
        return self._reportBuilder

    def Calculate(self):
        fObject       = self.FObject
        reportBuilder = self.FReportBuilder
        if (fObject):
            self._calculationResults = sensCalculation(reportBuilder, fObject, self._sensType).returnObjectSensitivity()
