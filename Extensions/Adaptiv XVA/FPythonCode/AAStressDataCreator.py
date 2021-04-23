""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAStressDataCreator.py"
import AADataCreator 
import AADataUtilFunctions as DataUtil
import AAUtilFunctions
import AAParamsAndSettingsHelper

def createStressDataXML(stressDataDic):

    supportedScenario = AAParamsAndSettingsHelper.getSupportedStressScenario()
    stressXML = "<StressTest CompareToUnshifted= \"True\"><Scenarios>"
    for d in stressDataDic:

        if str(d) not in supportedScenario:
            continue

        data = stressDataDic[d]
        if str(d) in ['CreditAttribution']:
            stressXML +=data
        elif isinstance(data, str):
            scenHeaderStr = "<Scenario ID= \"Scen %s\"> <![CDATA[ " %(d)
            stressXML += scenHeaderStr + data +"]]> </Scenario>"
        else:
            # Array type for bucket columns.
            scenNames = AAUtilFunctions.GetBucketScenNames(str(d))
            for name, e in zip(scenNames, data):
                scenHeaderStr = "<Scenario ID= \"Scen %s\"> <![CDATA[ " %(name)
                stressXML += scenHeaderStr + e +"]]> </Scenario>"
        
    footer = "</Scenarios></StressTest> <ResultsViewer ViewTypes=\"Attributes\"> Object=MultiStressResultsViewer, Scenario_To_Graph=Base,Factor_Group_To_Graph=TOTAL,Show=CVA,Quantiles_to_show=, What_If_View=Portfolio </ResultsViewer>"
    stressXML += footer
    return stressXML
    
    
def createBenchmarkInterestRateShiftupStr(benchmarkCurv, cvaCurvStr):
    curvItems = cvaCurvStr.split(",")
    cvaIntCurves = []
    for item in curvItems:
        i = item.find("InterestRate.")
        if i == -1:
            continue
        c = item[i+13:]
        cvaIntCurves.append(c)
    
    shiftupStr = ""
    for b in benchmarkCurv:
        bCurve = b.Name()
        if bCurve not in cvaIntCurves:
            continue
        shiftupStr += "\r\nInterestRate WHERE ID = \"%s\",Curve+0.0001\r\n" %(bCurve)
    if shiftupStr:
        shiftupStr = "<Price Factors>" + shiftupStr
    
    return shiftupStr

def createBenchmarkInterestRateShiftdownStr(benchmarkCurv, cvaCurvStr):
    curvItems = cvaCurvStr.split(",")
    cvaIntCurves = []
    for item in curvItems:
        i = item.find("InterestRate.")
        if i == -1:
            continue
        c = item[i+13:]
        cvaIntCurves.append(c)
    
    shiftdnStr = ""
    for b in benchmarkCurv:
        bCurve = b.Name()
        if bCurve not in cvaIntCurves:
            continue
        shiftdnStr += "\r\nInterestRate WHERE ID = \"%s\",Curve+-0.0001\r\n" %(bCurve)
    if shiftdnStr:
        shiftdnStr = "<Price Factors>" + shiftdnStr
    
    return shiftdnStr

def createShiftedSurvivalCurveString(curve, valuationDate):
    if not curve:
        return ""
    price_factor = AADataCreator.SurvivalProbPriceFactor(curve, valuationDate)
    idString = DataUtil.getCounterPartyID(curve)
    ycPointsList = price_factor.createYCPointsList()
    
    shiftdnStr = "<Price Factors>" + "\r\nSurvivalProb WHERE ID = \"%s\",Curve=%s\r\n" %(idString, str(ycPointsList))
    
    return shiftdnStr

def createShiftedInterestCurveString(instrument, instCurves, curves, convenienceCurves, valuationDate):
    if not curves:
        return ""
    
    shiftdnStr = "<Price Factors>"
    for c in curves:
        irCurve = c.IrCurveInformation()
        price_factor = AADataCreator.InterestRatePriceFactor(irCurve, valuationDate)
        idString = c.Name()
        ycPointsList = price_factor.createYCPointsList()
    
        shiftdnStr +=  "\r\nInterestRate WHERE ID = \"%s\",Curve=%s\r\n" %(idString, str(ycPointsList))
        
    shiftedBenchMarkCurves = []
    convenienceCurveNames = [ c.Name() for c in convenienceCurves]
    for c in curves:
        name = c.Name()
        if name in convenienceCurveNames:
            shiftedBenchMarkCurves.append(c)
    shiftdnStr += createShiftedConvenienceCurveString(instrument, instCurves, shiftedBenchMarkCurves, valuationDate)
    return shiftdnStr

def createShiftedConvenienceCurveString(instruments, instCurves, shiftedBenchMarkCurves, valuationDate):

    if len(instruments) != len(instCurves):
        raise AssertionError("The number of the shifted curves and instrumens are not the same.")
        
    shiftdnStr = ""
    processedCurves = []
    for s in shiftedBenchMarkCurves:
        for inst, c in zip(instruments, instCurves):
            curveName = s.Name()
            if curveName == c.Name() and curveName not in processedCurves:
                irCurve = s.IrCurveInformation()
                price_factor = AADataCreator.ConvenienceYieldPriceFactor(inst, irCurve, valuationDate)
                idString = DataUtil.parameterName(inst)
                ycPointsList = price_factor.createYCPointsList()
                shiftdnStr +=  "\r\nConvenienceYield WHERE ID = \"%s\",Curve=%s\r\n" %(idString, str(ycPointsList))
                processedCurves.append(curveName)
        
    return shiftdnStr
    
def createShiftedCreditRiskFactorCurveString(riskFactors, curveStrs):
    if len(riskFactors) != len(curveStrs):
        raise AssertionError("The number of the riskFactors is not the same as the needed shifted curve strings.")
        
    stressXML = ''
    for r, cStr in zip(riskFactors, curveStrs):
        scName = r.Identifier().Text()
        newScName = scName.replace(", Counterparty = ", " - ")
        scenHeaderStr = "<Scenario ID= \"Scen %s\"> <![CDATA[ " %(newScName)
        stressXML += scenHeaderStr + cStr +"]]> </Scenario>"
    return stressXML
