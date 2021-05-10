

import sys
import acm
import ael


from FUDMCCommon_CPP import native_import

""" Function imports """
CreateValFunc_func = acm.GetFunction("CreateCValuationFunction", 1)
GetObject_func = acm.GetFunction("getObject", 2)
AsDateTime_func = acm.GetFunction("asDateTime", 1)
MergeDictionaries_func = acm.GetFunction("mergeDictionaries", 2)
NowAsDays_func = acm.GetFunction("nowAsDays", 0)
DateTimeAsDouble_func = acm.GetFunction("dateTimeAsDouble", 1)


""" Time handling """
defaultCalendarName = "Target"
calendar = ael.Calendar[defaultCalendarName]
if not calendar:
    msg = "Calendar not found %s"%defaultCalendarName
    raise AttributeError(msg)

today = ael.date_today()
fourMonths = today.add_banking_day(calendar, 4 * 20)
eightMonths = today.add_banking_day(calendar, 8 * 20) 
twelveMonths = today.add_banking_day(calendar, 12 * 20)
sixteenMonths = today.add_banking_day(calendar, 16 * 20)
twentyMonths = today.add_banking_day(calendar, 20 * 20)
twentyfourMonths = today.add_banking_day(calendar, 24 * 20)

def NowFDateTime():
    dateTimeNow_str = acm.FDateTime()
    return dateTimeNow_str

def ExpiryFDateTime(instrument):
    expiryDateTime_str = acm.FDateTime(instrument.ExpiryDate())
    return expiryDateTime_str


""" Random generators """
randTypeSEQ = 0
randTypeSobol = 1
randTypeMersenne = 2
randTypeZiggurat = 3
randTypeSobolBroda = 4


""" Process generation """
def UdmcLogNormProcessIRTS( S, \
                        vol, \
                        timeSteps, \
                        historicalAssetPrices, \
                        cc, \
                        rf, \
                        dividends, \
                        valuationDate, \
                        isQuanto, \
                        quantoCorrelation, \
                        underlyingQuantoVol, \
                        fxVol, \
                        randGenType, \
                        seed):
    udmcLogNormProcessIRTS = acm.GetFunction("udmcLogNormProcessIRTS", 14)
    return udmcLogNormProcessIRTS(  S, vol, timeSteps, historicalAssetPrices, \
                                    cc, rf, dividends, valuationDate, isQuanto, \
                                    quantoCorrelation, underlyingQuantoVol, fxVol, \
                                    randGenType, seed)

""" Fixing dictionary """
def UDMCCreateFixingDictionary(instrument, \
                               components, \
                               componentValues, \
                               eventKeyTypes, \
                               eventTypes, \
                               adflEventDates, \
                               includeInHistorical, \
                               valuationDateTime, \
                               expiryDateTime, \
                               nTimeParts):
    CreateFixingDictionary_func = acm.GetFunction("udmcCreateFixingDictionary", 10)
    fixingDictionary = CreateFixingDictionary_func(instrument, \
                                                   components, \
                                                   componentValues, \
                                                   eventKeyTypes, \
                                                   eventTypes, \
                                                   adflEventDates, \
                                                   includeInHistorical, \
                                                   valuationDateTime, \
                                                   expiryDateTime, \
                                                   nTimeParts)
    return fixingDictionary

""" UDMC Valuation function """
def CreateValuationFunction(pelCode):
    try:
        valFunc = CreateValFunc_func(pelCode)
        return valFunc
    except Exception as e:
        msg = "Exception thrown when creating valuation function: %s"%str(e)
        raise TypeError(msg)

""" General """
def MergeDictionaries(dict1, dict2):
    return MergeDictionaries_func(dict1, dict2)

def GetPaydate_double(instrument):
    settlementDate = None
    if instrument.SettlementType() == "Physical Delivery":
        settlementDate = instrument.SettlementDate()
    else:
        underlying = instrument.Underlying()
        expiryDate = instrument.ExpiryDate()
        spotDays = instrument.SpotBankingDaysOffset()
        settlementDate = underlying.GetSpotDay(expiryDate, calendar, spotDays)
        
    if not settlementDate:
        msg = "Settlement date not found"
        raise AttributeError(msg)
    return DateTimeAsDouble_func(settlementDate)

def GetSpotDate(instrument):
    spotDays = instrument.SpotBankingDaysOffset()
    spotDay = today.add_banking_day(calendar, spotDays)
    return spotDay

def GetSpotDateAsDays(instrument):
    spotDays = instrument.SpotBankingDaysOffset()
    spotDay = today.add_banking_day(calendar, spotDays)
    nowAsDays = NowAsDays_func()
    spotAsDays = nowAsDays + today.days_between(spotDay)
    return spotAsDays

""" Payoff extensions """
def FetchPelCode(payoffName):
    context = acm.GetDefaultContext()
    payoff = context.GetExtension("FUserDefinedPayoff", "FObject", payoffName)
    if not payoff:
        msg = "Could not fetch payoff pel-code: %s"%payoffName
        raise AttributeError(msg)
    return payoff.Value()
    

""" Yield Curve Ir """
defaultYieldCurveName = "EUR-SWAP"
def DefaultYieldIr():
    yieldCurve = acm.FYieldCurve[defaultYieldCurveName]
    if not yieldCurve:
        msg = "Default yield curve not found"
        raise AttributeError(msg)
    return yieldCurve.Ir()

""" Repo Curve Ir """
defaultRepoCurveName = "EUR-SWAP"
def DefaultRepoIr():
    repoCurve = acm.FYieldCurve[defaultRepoCurveName]
    if not repoCurve:
        msg = "Default repo curve not found"
        raise AttributeError(msg)
    return repoCurve.Ir()

""" Tree Simulations """
def ShiftNode(nodeEvaluator, shiftValue, simFunc):
    unsimulatedValue = nodeEvaluator.Value()
    simulatedValue = simFunc(unsimulatedValue, shiftValue) 
    nodeEvaluator.Simulate(simulatedValue, False)

def CalcDiffValues(baseEval, shiftEval, shiftSize, shiftFunc):
    unshiftedValue = baseEval.Value()
    undValue = shiftEval.Value()
    shiftedUndValue = shiftFunc(undValue, shiftSize) 
    shiftEval.Simulate(shiftedUndValue, False)
    shiftedValue = baseEval.Value()
    shiftEval.RemoveSimulation()
    return (unshiftedValue, shiftedValue)

def RunTwoDimSimulations(instrument, baseNode_str, \
                         firstValues_arr, secondValues_arr, \
                         firstShiftNode_str, secondShiftNode_str, \
                         firstShiftFunc, secondShiftFunc):
    context = acm.GetDefaultContext()
    tag = acm.CreateEBTag()

    rootEvaluator = acm.GetCalculatedValueFromString(instrument, context, baseNode_str, tag)
    outerShiftEvals = rootEvaluator.FindAdHoc(firstShiftNode_str, acm.FObject)

    if not len(outerShiftEvals) > 0:
        msg = "Could not find shift node, '%s'"%firstShiftNode_str
        raise TypeError(msg)
    outerShiftEval = outerShiftEvals[0]
   
    innerShiftEvals = rootEvaluator.FindAdHoc(secondShiftNode_str, acm.FObject)
    if not len(innerShiftEvals) > 0:
        msg = "Could not find shift node, '%s'"%secondShiftNode_str
        raise TypeError(msg)
    innerShiftEval = innerShiftEvals[0]
    
    resultMatrix = []
    for firstSimValue in firstValues_arr:
        ShiftNode(outerShiftEval, firstSimValue, firstShiftFunc)
        for secondSimValue in secondValues_arr:
            result = CalcDiffValues(rootEvaluator, innerShiftEval, secondSimValue, secondShiftFunc)
            resultMatrix.append(result)
        outerShiftEval.RemoveSimulation()
    return resultMatrix

""" File Utilities """
def OutputMatrixToFile(matrix, rows, cols, fileName):
    outputFile = open(fileName, 'w')
    for i in range(rows):
        for j in range(cols):
            data = matrix[i*cols + j]
            outputFile.write(str(data) + '\t')
        outputFile.write('\n')
    outputFile.close() 
    

""" Plot utilities """
pyPackagesPath = r"C:\Python23\Lib\site-packages"
global matplotlib
def ImportMatplotLib():
    try:
        matplotlib = native_import("matplotlib", pyPackagesPath)
    except:
        matplotlib = None
        msg = "Could not import matplotlib"
        raise ImportError(msg)
    return matplotlib





