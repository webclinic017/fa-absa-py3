""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_fva/./etc/AAFVAIntegration.py"
import AAParamsAndSettingsHelper
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

try:
    import AAValuation
except:
    logger.ELOG("Could not import module AAValuation")
try:
    import AAFVAValuation
except:
    logger.ELOG("Could not import module FCAValuation")
import acm

def FillFVAResult(resultArray, cvaCurrency, valuationDate):
    resultDictionary = acm.FDictionary()
    resultDictionary["FVA"] = acm.DenominatedValue(resultArray[0], cvaCurrency, valuationDate)
    resultDictionary["FBA"] = acm.DenominatedValue(resultArray[1], cvaCurrency, valuationDate)
    resultDictionary["FCA"] = acm.DenominatedValue(resultArray[2], cvaCurrency, valuationDate)
    return resultDictionary

def CreateFVADictionary(baseValuesResult, cvaCurrency, valuationDate):
    baseValuesDictionary = FillFVAResult(baseValuesResult, cvaCurrency, valuationDate)
    return baseValuesDictionary
    
def EmptyFVAResult(cvaCurrency, valuationDate, cvaWithWrongWayRisk):
    emptyFVAArray = [0.0, 0.0, 0.0]
    return CreateFVADictionary(emptyFVAArray, cvaCurrency, valuationDate)

def ParseFVAResult(resultXml, cvaCurrency, valuationDate, cvaWithWrongWayRisk, cvaScenName):
    baseValuesResult = AAFVAValuation.ParseFvaResultXml(resultXml, "Base", cvaScenName)
    return CreateFVADictionary(baseValuesResult, cvaCurrency, valuationDate)
