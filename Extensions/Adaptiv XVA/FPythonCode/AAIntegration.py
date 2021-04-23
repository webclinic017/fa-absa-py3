""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAIntegration.py"
import AAParamsAndSettingsHelper
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

try:
    import AAValuation
except:
    logger.ELOG("Could not import module AAValuation")
import acm

def AssembleXML(dealsXML, calculationXML, marketDataXML, stressXML):
    xml = []
    if dealsXML and calculationXML and marketDataXML:
        xml.append("<Calc>")
        xml.append(calculationXML)
        xml.append(dealsXML)
        xml.append(marketDataXML)
        xml.append(stressXML)
        xml.append("</Calc>")
    result = ''.join(xml)
    return result

def AACalculate(dealsXML, calculationXML, marketDataXML, stressXML):
    xml = AssembleXML(dealsXML, calculationXML, marketDataXML, stressXML)
    res_xml = AAValuation.Calculate(xml)
    return res_xml

def FillCVAResult(resultArray, cvaCurrency, valuationDate):
    resultDictionary = acm.FDictionary()
    cvaEnumeration = acm.FEnumeration["enum(CVACalculationType)"]
    resultDictionary[cvaEnumeration.Enumerator(1)] = acm.DenominatedValue(resultArray[0], cvaCurrency, valuationDate)
    resultDictionary[cvaEnumeration.Enumerator(2)] = acm.DenominatedValue(resultArray[1], cvaCurrency, valuationDate)
    resultDictionary[cvaEnumeration.Enumerator(3)] = acm.DenominatedValue(resultArray[2], cvaCurrency, valuationDate)
    return resultDictionary

def CreateResultDictionary(baseValuesResult, totalValuesResult, adjustmentValuesResult, cvaCurrency, valuationDate):
    baseValuesDictionary = FillCVAResult(baseValuesResult, cvaCurrency, valuationDate)
    resultDictionary = None
    if totalValuesResult and adjustmentValuesResult:
        resultDictionary = acm.FDictionary()
        resultDictionary["Base"] = baseValuesDictionary

        totalValuesDictionary = FillCVAResult(totalValuesResult, cvaCurrency, valuationDate)
        resultDictionary["Total"] = totalValuesDictionary

        adjustmentValuesDictionary = FillCVAResult(adjustmentValuesResult, cvaCurrency, valuationDate)
        resultDictionary["Adjustment"] = adjustmentValuesDictionary
    else:
        resultDictionary = baseValuesDictionary
    return resultDictionary

def EmptyCVAResult(cvaCurrency, valuationDate, cvaWithWrongWayRisk):
    emptyCVAArray = [0.0, 0.0, 0.0]
    if cvaWithWrongWayRisk:
        return CreateResultDictionary(emptyCVAArray, emptyCVAArray, emptyCVAArray, cvaCurrency, valuationDate)
    else:
        return CreateResultDictionary(emptyCVAArray, None, None, cvaCurrency, valuationDate)

def ParseCVAResult(resultXml, cvaCurrency, valuationDate, cvaWithWrongWayRisk, cvaScenName):
    baseValuesResult = AAValuation.ParseCvaResultXml(resultXml, "Base", cvaScenName)
    totalValuesResult = None
    adjustmentValuesResult = None
    if cvaWithWrongWayRisk:
        totalValuesResult = AAValuation.ParseCvaResultXml(resultXml, "Total", cvaScenName)
        adjustmentValuesResult = AAValuation.ParseCvaResultXml(resultXml, "Adjustment", cvaScenName)
    return CreateResultDictionary(baseValuesResult, totalValuesResult, adjustmentValuesResult, cvaCurrency, valuationDate)

def ParseBaseValuationResult(resultXml, cvaCurrency, valuationDate):
    resDict = acm.FDictionary()
    result = AAValuation.ParseBaseValuationResultXml(resultXml)
    resDict["Base Valuation"] = acm.DenominatedValue(result, cvaCurrency, valuationDate)
    return resDict

def ParsePFEResult(resultXml, cvaCurrency, valuationDate, bucketStartDate, bucketEndDate):
    resDict = acm.FDictionary()
    resultPFEs, resultDates = AAValuation.ParsePFEResultXml(resultXml, bucketStartDate, bucketEndDate)
    resultL = []
    for pfeValue, date in zip(resultPFEs, resultDates):
        resultL.append(acm.DenominatedValue(pfeValue, cvaCurrency, date))
    resDict["PFE"] = resultL
    return resDict

def ParseMaxPFEResultWithMultiplePercentiles(resultXml, cvaCurrency, valuationDate):
    resDict = acm.FDictionary()
    results = AAValuation.ParsePFEResultXmlWithMultiplePercentile(resultXml)
    maxPFE = []
    sortedKeys = sorted(list(results.keys()), reverse=True)
    for key in sortedKeys:
        maxPFE.append(max(results[key]))
    resDict["PFE"] = acm.DenominatedValue(maxPFE, cvaCurrency, valuationDate)
    return resDict
