
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_CALCULATION_SEN_TEST
PROJECT                 :       Front Cache
PURPOSE                 :       This module must only be used for testing the FC_CALCULATION_SENSITIVITY 
                                Module
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Gavin Wienand
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#Core
import FReportAPI
import FReportAPIBase
import acm

#Custom
from FC_CALCULATION_SENSITIVITY import FC_CALCULATION_SENSITIVITY as sensCalculation
import FC_SERIALIZATION
from FC_UTILS import FC_UTILS as UTILS
UTILS.Initialize('FC_AD_HOC_REQUEST_GENERATOR')

fObject       = acm.FPhysicalPortfolio['SL_LEIPS']
reportBase    = FReportAPI.FWorksheetReportApiParameters(includeRawData=True, expiredPositions=True)
reportBuilder = FReportAPIBase.FReportBuilder(reportBase)

calculationResults = sensCalculation(reportBuilder, fObject).returnObjectSensitivity()

print FC_SERIALIZATION.CustomDictToXMLString(calculationResults, fObject.ClassName())
print FC_SERIALIZATION.CustomDictToProtobuf(calculationResults)
