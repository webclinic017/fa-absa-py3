""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AADataUtilFunctions.py"
import acm
import AAUtilFunctions as Util
import AAParamsAndSettingsHelper as Params
import importlib
logger = Params.getAdaptivAnalyticsLogger()

def pointDates(curveInfo):
    dates = curveInfo.PointDates()
    if curveInfo.UnderlyingCurve():
        dates = set(dates)
        dates.update(pointDates(curveInfo.UnderlyingCurve()))
    return dates
        
def lastPointDate(curveInfo):
    lastDate = curveInfo.LastPointDate()
    if curveInfo.UnderlyingCurve():
        undLastDate = lastPointDate(curveInfo.UnderlyingCurve())
        if lastDate < undLastDate:
            lastDate = undLastDate
    return lastDate

def getPeriodVolatility(fromDate, toDate):
    yearsBetween = acm.GetFunction('yearsBetween', 4)
    return yearsBetween(fromDate, toDate, "ACT/365", None)

def isSpread(yieldCurveComponent):
    if yieldCurveComponent.IsKindOf("FSpreadCurve") or yieldCurveComponent.IsKindOf("FYCAttribute") or yieldCurveComponent.IsKindOf("FInstrumentSpread"):
        return 1
    return 0

def lastPriceDate(priceIndex):
    # return date of the most recent price in the historical price table
    curr = priceIndex.Currency()
    small_date = acm.Time().SmallDate()
    last_date = small_date
    for p in priceIndex.HistoricalPrices():
        if p.Currency() == curr and p.Day() > last_date and p.Settle() > 0:
            last_date = p.Day()
            
    if last_date == small_date:
        raise Exception('Missing prices for %s' % priceIndex.StringKey())
    else:
        return last_date

def refPriceDate(priceIndex):
    last_date = lastPriceDate(priceIndex)
    if priceIndex.ReferenceDateType() == 'First of next month':
        adjusted_date = acm.Time.DateAddDelta(last_date, 0, 1, 0)
        d = '01'
    elif priceIndex.ReferenceDateType() == 'First of current month':
        adjusted_date = last_date
        d = '01'
    else:
        return last_date
        
    ymd = adjusted_date.split('-')
    y = ymd[0]
    m = ymd[1]
    date = y + '-' + m + '-' + d
    return date
        

# ----------------------------------------

def getCounterPartyIDFromCurve(creditCurveComponent):
    if creditCurveComponent.IsKindOf("FYCAttribute"):
        issuer = creditCurveComponent.Issuer()
        if issuer == None:
            raise AssertionError("No issuer found")
        else:
            cpy_id = issuer.StringKey()
    elif creditCurveComponent.IsKindOf("FSpreadCurve"):
        cpy_id = creditCurveComponent.StringKey()
    else:
        raise AssertionError("Credit Curve Component is not a spread curve")
    return Util.createAALabel(cpy_id)

def getCounterPartyID(creditIrCurveInformation):
    if creditIrCurveInformation.IsKindOf("FShiftedIrCurveInformation"):
        origCurve = creditIrCurveInformation.OriginalCurve()
        if origCurve:
            creditIrCurveInformation = origCurve
    yc_component = creditIrCurveInformation.YieldCurveComponent()
    return getCounterPartyIDFromCurve(yc_component)
    
def getNameFromMappingLink(ml):
    return getNameFromCurve(ml)
    
def getPriceFactorName(priceFactorEntity):
    priceFactorList = []
    if priceFactorEntity.IsKindOf("FMappingLink"):
        linkObject = priceFactorEntity.Link()
        if linkObject.IsKindOf("FYieldCurveHierarchy"):
            yieldCurveHierarchy = linkObject
            while yieldCurveHierarchy:
                priceFactorList.insert(0, yieldCurveHierarchy.YieldCurveComponent())
                yieldCurveHierarchy = yieldCurveHierarchy.UnderlyingComponent()
        if linkObject.IsKindOf("FVolatilityStructureHierarchy"):
            volatilityHierarchy = linkObject
            priceFactorList.insert(0, volatilityHierarchy.VolatilityStructure())
    elif priceFactorEntity.IsKindOf("FIrCurveInformation"):
        irCurveInformation = priceFactorEntity
        while irCurveInformation:
            origCurve = irCurveInformation.OriginalCurve()
            if origCurve:
                irCurveInformation = origCurve
            priceFactorList.insert(0, irCurveInformation.YieldCurveComponent())
            irCurveInformation = irCurveInformation.UnderlyingCurve()
    elif priceFactorEntity.IsKindOf("FVolatilityInformation"):
        volatilityInformation = priceFactorEntity
        priceFactorList.insert(0, volatilityInformation.OriginalVolatility().VolatilityStructure())
    else:
        priceFactorList.append(priceFactorEntity)
    return parameterNames(priceFactorList)

def parameterNames(parameters):
    names = []
    for parameter in parameters:
        names.append(parameterName(parameter))
    return '.'.join(names)

def parameterName(parameter):
    name = ""
    if parameter.IsKindOf('FCommonObject'):
        name = parameter.OriginalOrSelf().LiveEntity().StringKey()
    else:
        name = parameter.StringKey()
    if parameter.IsKindOf('FYieldCurve') or parameter.IsKindOf('FYCAttribute') or parameter.IsKindOf('FInstrumentSpread') or parameter.IsKindOf('FVolatilityStructure'):
        return Util.createAALabel(name)
    else:
        return name

def getNameFromCurve(curveEntity):
    yieldCurveComponents = []
    if curveEntity.IsKindOf("FMappingLink"):
        yieldCurveHierarchy = curveEntity.Link()
        while yieldCurveHierarchy:
            yieldCurveComponents.insert(0, yieldCurveHierarchy.YieldCurveComponent())
            yieldCurveHierarchy = yieldCurveHierarchy.UnderlyingComponent()
    if curveEntity.IsKindOf("FIrCurveInformation"):
        irCurveInformation = curveEntity
        while irCurveInformation:
            origCurve = irCurveInformation.OriginalCurve()
            if origCurve:
                irCurveInformation = origCurve
            yieldCurveComponents.insert(0, irCurveInformation.YieldCurveComponent())
            irCurveInformation = irCurveInformation.UnderlyingCurve()
    return parameterNames(yieldCurveComponents)

def cvaBaseCurrency():
    return acm.FCurrency[Params.getBaseCurrency()]

def getMappedFXDiscountLinkFromPair(ccy_from, ccy_to):    
    return ccy_from.MappedDiscountLink(ccy_to, False, None)

# -----------------------------------------------------------

def reloadPythonCode(_eii):
    try:
        import AAIntegration
        importlib.reload(AAIntegration)
        import AAParamsAndSettingsHelper
        importlib.reload(AAParamsAndSettingsHelper)
        try:
            import AAUserParamsAndSettings
        except ImportError:
            pass
        else:
            importlib.reload(AAUserParamsAndSettings)
        import AAUserParamsAndSettingsTemplate
        importlib.reload(AAUserParamsAndSettingsTemplate)
        import AAUtilFunctions
        importlib.reload(AAUtilFunctions)     
        import AADataUtilFunctions
        importlib.reload(AADataUtilFunctions)            
        import AACashFlowCreator
        importlib.reload(AACashFlowCreator)
        import AAComposer
        importlib.reload(AAComposer)
        import AACalculationCreator
        importlib.reload(AACalculationCreator)
        import AADataCreator
        importlib.reload(AADataCreator)
        import AADealsCreator
        importlib.reload(AADealsCreator)
        import AAImport
        importlib.reload(AAImport)
        import AAMenusAndButtons
        importlib.reload(AAMenusAndButtons)
        import AANettingSetCreator
        importlib.reload(AANettingSetCreator)
        import CVAHooksTemplate
        importlib.reload(CVAHooksTemplate)
        try:
            import CVAHooks
        except ImportError:
            pass
        else:
            importlib.reload(CVAHooks)
        import CVAHooksHelper
        importlib.reload(CVAHooksHelper)
        import AACustomDealsCreator
        importlib.reload(AACustomDealsCreator)
        import AAInstrumentFiltration
        importlib.reload(AAInstrumentFiltration)
        import AACfInstrumentDeal
        importlib.reload(AACfInstrumentDeal)
        import AAFxForwardDeal
        importlib.reload(AAFxForwardDeal)
        import AAFxSwapDeal
        importlib.reload(AAFxSwapDeal)
        import AAParameterDictionary
        importlib.reload(AAParameterDictionary)
        import AACfInstrumentDealCCSwap
        importlib.reload(AACfInstrumentDealCCSwap)
        import AACfInstrumentDealSwaption
        importlib.reload(AACfInstrumentDealSwaption)
        import AACfInstrumentDealCapFloor
        importlib.reload(AACfInstrumentDealCapFloor)
        import AACfInstrumentDealCMSSwap
        importlib.reload(AACfInstrumentDealCMSSwap)
        import AAFRADeal
        importlib.reload(AAFRADeal)
        import AAFxOptionDeal
        importlib.reload(AAFxOptionDeal)
        import AACfInstrumentDealCallPutableSwap
        importlib.reload(AACfInstrumentDealCallPutableSwap)
        import AAValuation
        importlib.reload(AAValuation)
        import AAParameterFiltration
        importlib.reload (AAParameterFiltration)
        import AACommodityFutureDeal
        importlib.reload (AACommodityFutureDeal)
        import AACommodityOptionDeal
        importlib.reload(AACommodityOptionDeal)
        import AAILBondFutureDeal
        importlib.reload(AAILBondFutureDeal)
        import AAEquitySwapDeal
        importlib.reload(AAEquitySwapDeal)
        import AACreditDefaultSwapDeal
        importlib.reload(AACreditDefaultSwapDeal)
        import AAStockOptionDeal
        importlib.reload(AAStockOptionDeal)
        import AABondOptionDeal
        importlib.reload(AABondOptionDeal)
        
        logger.LOG("Reloaded Adaptiv python modules successfully")
    except Exception as e:
        logger.ELOG(str(e))
