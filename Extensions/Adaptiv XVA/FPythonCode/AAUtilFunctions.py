""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAUtilFunctions.py"
from __future__ import print_function
import acm
import os
import AAParamsAndSettingsHelper
import tempfile

def flattenMTM(mtm):
    if mtm:
        if mtm.IsKindOf("FDenominatedValue"):
            return mtm.Number()
        
        if mtm.IsKindOf("FArray"):
            return flattenMTM(mtm.At(0))
        
        if mtm.IsKindOf("FException"):
            return 0.0
    return 0.0

def getMtMValue(mtm):
    if isinstance(mtm, float):
        if mtm != 0.0:
            return mtm
    
    return "&lt;undefined&gt;"

def getLag(fixingMethod):
    if fixingMethod == "CPI -3Months":
        return 3
    elif fixingMethod == "CPI -3Months NoInterpol":
        return 3
    elif fixingMethod == "CPI -2Months NoInterpol":
        return 2
    elif fixingMethod == "CPI -8Months NoInterpol":
        return 8
    elif fixingMethod == "CPI -4Months":
        return 4
    else:
        raise Exception("Fixing method %s is not supported in AA" % fixingMethod)

def getReferenceNameFromFixingMethod(fixingMethod):
    if fixingMethod == "CPI -3Months":
        return "IndexReferenceInterpolated3M"
    elif fixingMethod == "CPI -3Months NoInterpol":
        return "IndexReference3M"
    elif fixingMethod == "CPI -2Months NoInterpol":
        return "IndexReference2M"
    elif fixingMethod == "CPI -8Months NoInterpol":
        return "IndexReference8M"
    elif fixingMethod == "CPI -4Months":
        return "IndexReferenceInterpolated4M"
    else:
        raise Exception("Fixing method %s is not supported in AA" % fixingMethod)

def getBuySellFlag(isPayLeg):
    if isPayLeg:
        return "Sell"
    else:
        return "Buy"

def getCallOrPutType(isCallOption):
    if isCallOption:
        return "Call"
    else:
        return "Put"

def getPayerReceiverFlag(isReceiverSwap):
    if isReceiverSwap:
        return "Receiver"
    else:
        return "Payer"
        
def getSettlementTypeFlag(settlementType):
    if settlementType == "Cash":
        return "Cash"
    if settlementType == "Physical Delivery":
        return "Physical"
    raise Exception("Unknown settlement type: %s" % settlementType)
        
# Converts PRIME's leg type enumerated type to Adaptiv Analytics' property key
def getLegType(primeLegType):
    if "Float" in primeLegType :
        return "Floating"
    if "Fixed" in primeLegType:
        return "Fixed"
    # There might be more supported leg types
    raise Exception("Unknown leg type: %s" % primeLegType)    

# Returns Adaptiv Analytics' value for "Principal Exchange" property
def getPrincipalExchangeStr(leg):
    principalExchangeStr = "None"   
    if leg.NominalAtStart() and (not leg.NominalAtEnd()):
        principalExchangeStr = "Start"
    if (not leg.NominalAtStart()) and leg.NominalAtEnd():
        principalExchangeStr = "Maturity"
    if leg.NominalAtStart() and leg.NominalAtEnd():
        principalExchangeStr = "Start_Maturity"
    return principalExchangeStr

def monthAbbreviation (month):
    if month == "01":
        return "Jan"
    elif month == "02":
        return "Feb"
    elif month == "03":
        return "Mar"
    elif month == "04":
        return "Apr"
    elif month == "05":
        return "May"
    elif month == "06":
        return "Jun"
    elif month == "07":
        return "Jul"
    elif month == "08":
        return "Aug"
    elif month == "09":
        return "Sep"
    elif month == "10":
        return "Oct"
    elif month == "11":
        return "Nov"
    elif month == "12":
        return "Dec"
    else:
        raise AssertionError("Invalid month format")

def createDateString(date):
    ymd = date.split('-')
    assert(len(ymd) == 3), "Invalid date format"  
    return ymd[2] + monthAbbreviation(ymd[1]) + ymd[0]

def createDateStringFromDateTime(dateTime):
    # Format: "YYY-MM-DD hh:mm:ss"
    return createDateString(dateTime.split(' ')[0])
    
def createDatePeriodString(datePeriod):
    return datePeriod.upper()

def createDayCountString(dayCount):
    if dayCount == "Act/360":
        return "ACT_360"
    elif dayCount == "Act/365":
        return "ACT_365"
    elif dayCount == "Act/ActAFB":
        return "ACT_ACT_AFB"
    elif dayCount == "30/360":
        return "_30_360"
    elif dayCount == "30E/360":
        return "_30E_360"
    elif dayCount == "Act/ActISMA":
        return "ACT_ACT_ICMA"
    elif dayCount == "Bus/252":
        return "BUS_252"
    else:
        raise AssertionError("Invalid day count method")

def createBasisPointString(value):
    return str(value * 10000.0) + " bp"
    
def createPercentageString(value):
    return str(value * 100.0) + "%"

def createBoolString(inBool):
    if inBool:
        return "Yes"
    else:
        return "No"

def createStringFromTuple(inTuple):
    string = ""
    for item in inTuple:
        if string != "":
            string += ","
        if type(item) is str:
            string += item
        elif type(item) is int or type(item) is float:
            string += str(item)               
    return string

def createAALabel(name):
    # Characters not supported by Adaptiv Analytics
    for bad_char in ".,/~":
        name = name.replace(bad_char, '')
    # XML special characters
    for bad_char in "<>&":
        name = name.replace(bad_char, '')
    return name

def createReference(obj):
    if isinstance(obj, basestring):
        return createAALabel(obj)
    elif obj.IsKindOf('FStaticLegInformation'):
        return createAALabel(obj.InstrumentId())
    elif obj.IsKindOf('FInstrument'):
        return createAALabel(obj.Name())
    return createAALabel(str(obj))
    
def createValidWinFileName(filename):
    validSpecialChars = ['^', '&', '@', '{', '}', '[', ']', '$', '=', '!', '-', '#', '(', ')', '%', '.', '+', '~', '_', ' ']
    return "".join(c for c in filename if c.isalnum() or c in validSpecialChars).rstrip()

def flattenToStringforListElement(list):
    newList = []
    for e in list:
        if isinstance(e, str):
            newList.append(e)
        else:
            newList.append('\n'.join(e))
    
    return newList

def listToString(list):
    return "\n".join(list)

def getMaxValue(valList):
    values = [v.Value() for v in valList]
    if not values:
        return None
        
    maxV = max(values)
    if not maxV.IsKindOf("FDenominatedValue"):
        return None
        
    # Override the datetime to current valuation date to prevent discounting.
    return acm.DenominatedValue(maxV.Value(), maxV.Unit(), acm.Time.DateToday())

def getPFEAajFilePath():
    aajFilePath = AAParamsAndSettingsHelper.getExportToFileDir()
    if not aajFilePath:
        aajFilePath = tempfile.gettempdir()

    if not aajFilePath:
        print('No ExportToFileDir provided.')
        return None    

    if not os.path.exists(aajFilePath):
        print('The given export path "%s" does not ' \
            'exist.' %(aajFilePath))
        return None

    if not os.path.isdir(aajFilePath):
        print('The given export path "%s" is not ' \
            'a directory.' %(aajFilePath))
        return None

    if not os.access(aajFilePath, os.W_OK):
        print('The given export path "%s" is not ' \
            'writable.' %(aajFilePath))
        return None

    absExportPath = os.path.abspath(aajFilePath)
    appendix = 'PFE_%s' %(acm.Time().DateToday())
    absExportPath = os.path.join(absExportPath, appendix)
    if not os.path.exists(absExportPath):
       os.makedirs(absExportPath)
    return absExportPath

def exportIPFEJobFiles(beforePFEXml, afterPFEXml, rowObjectID, doPrintJobFile):
    if doPrintJobFile:
        if not beforePFEXml and not afterPFEXml:
            return
            
        AAJFilePath = getPFEAajFilePath()
        if not AAJFilePath:
            return 'Failed to export AAJ files.' 
        PATH = "%s\\%s_beforeIPFE.aaj" %(AAJFilePath, rowObjectID)
        job_string = "<Job>" + beforePFEXml + "</Job>"
        fout = open(PATH, 'w')
        fout.write(job_string)
        fout.close()
        print("Wrote job file to: ", PATH)
        
        PATH = "%s\\%s_afterIPFE.aaj" %(AAJFilePath, rowObjectID)
        job_string = "<Job>" + afterPFEXml + "</Job>"
        fout = open(PATH, 'w')
        fout.write(job_string)
        fout.close()
        
        print("Wrote job file to: ", PATH)
        return "AAJ Files Saved."
    return ""

def IsSupportedTimeBuckets(timeBuckets):
    if not timeBuckets:
        return 0

    supportedTimeBuckets = AAParamsAndSettingsHelper.getTimeBucket()
    if len(timeBuckets) != len(supportedTimeBuckets):
        return 0

    for tb1, tb2 in zip(supportedTimeBuckets, timeBuckets):
        if tb1 != tb2:
            return 0
    return 1 
    
def GetBucketScenNames(name):
    timeBuckets = AAParamsAndSettingsHelper.getTimeBucket()
    scenName = [name + tb.Name() for tb in timeBuckets]
    return scenName

def GetRiskValueBenchmarkCurves(benchmarkCurv, cvaCurvStr):
    curvStr = cvaCurvStr
    if type(cvaCurvStr)is not str:
        curvStr = " ".join(str(x) for x in cvaCurvStr)
        
    curvItems = curvStr.split(",")
    cvaIntCurves = []
    for item in curvItems:
        i = item.find("InterestRate.")
        if i == -1:
            continue
        c = item[i+13:]
        cvaIntCurves.append(c)
    
    irCurves = []
    for b in benchmarkCurv:
        bCurve = b.Name()
        if bCurve not in cvaIntCurves:
            continue
        irCurves.append(b)
    return irCurves

def GetRiskFactorScenName(riskfactors):
    return riskfactors[0].Identifier().Text()

def IsSupportedStressRiskType(riskFactorTypeName):
    defaultSupportedScenario = AAParamsAndSettingsHelper.getSupportedStressScenario()
    if riskFactorTypeName in ['Par CDS Rate'] and 'CreditAttribution' in defaultSupportedScenario:
        return 1
    return 0

def IsSupportedScenario(scenName):
    defaultSupportedScenario = AAParamsAndSettingsHelper.getSupportedStressScenario()
    if scenName in defaultSupportedScenario:
        return 1
    return 0
