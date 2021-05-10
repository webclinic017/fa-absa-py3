""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAParamsAndSettingsHelper.py"
import acm
import ast

USER_MODULE_EXISTS = False
try:
    import AAUserParamsAndSettings
    USER_MODULE_EXISTS = True
except:
    pass
import AAUserParamsAndSettingsTemplate

FParameters = acm.GetDefaultContext().GetExtension(
        'FParameters', 'FObject', 'FxVAParameters'
).Value()
FParamList = []

for key in FParameters:
    if str(FParameters[key]) == '0' or str(FParameters[key]) == '1':
        value = bool(int(str(FParameters[key])))
    elif str(FParameters[key])[0] == '{':
        value = ast.literal_eval(str(FParameters[key]))
    else:
        value = str(FParameters[key])
        
    listItem = [str(key), value]
    FParamList.append(listItem)

FParameters = dict(FParamList)

#----------------Price factor settings------------------------
def getNumberOfCurvePoints():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'getNumberOfCurvePoints'):
        return AAUserParamsAndSettings.getNumberOfCurvePoints()
    else:
        return AAUserParamsAndSettingsTemplate.getNumberOfCurvePoints()


#----------------Adaptiv DLL path-----------------------------
def getAdaptivPath():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'ADAPTIV_PATH'):
        adaptivPath = AAUserParamsAndSettings.ADAPTIV_PATH
        if adaptivPath[-1] != '\\':
            index = adaptivPath.rfind('\\')
            return adaptivPath[:index+1]
        return adaptivPath
    else:
        return AAUserParamsAndSettingsTemplate.ADAPTIV_PATH

#----------------Adaptiv Analytics Studio path----------------
def getAdaptivAnalyticsStudioPath():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'ADAPTIV_ANALYTICS_STUDIO_PATH'):
        return AAUserParamsAndSettings.ADAPTIV_ANALYTICS_STUDIO_PATH
    else:
        return AAUserParamsAndSettingsTemplate.ADAPTIV_ANALYTICS_STUDIO_PATH

#----------------Adaptiv Analytics Log path----------------
def getAdaptivAnalyticsLogPath():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'ADAPTIV_ANALYTICS_LOG_PATH'):
        return AAUserParamsAndSettings.ADAPTIV_ANALYTICS_LOG_PATH
    else:
        return AAUserParamsAndSettingsTemplate.ADAPTIV_ANALYTICS_LOG_PATH

#----------------Adaptiv Analytics Logger----------------
def getAdaptivAnalyticsLogger():
    import FLogger
    import logging
    logger = FLogger.FLogger.GetLogger('AdaptivCVA')
    logger.Reinitialize(logToFileAtSpecifiedPath=getAdaptivAnalyticsLogPath())
    log_formatter = logging.Formatter( '%(asctime)s %(message)s', '%y%m%d %H%M%S' )
    for hndlr in logger.Handlers():
        hndlr.setFormatter(log_formatter)
    return logger

#----------------Market data paths----------------------------
def getFile(valulationDate, paramAttributeName):
    getter = None
    if USER_MODULE_EXISTS:
        getter = getattr(AAUserParamsAndSettings, paramAttributeName, None)

    if not getter:
        getter = getattr(AAUserParamsAndSettingsTemplate, paramAttributeName)

    return getter(valulationDate)

def getMarketDataFileBaseVal(valuationDate):
    return getFile(valuationDate, 'MarketDataFilePathBaseVal')

def getMarketDataFileCva(valuationDate, ignoreUseRealTimeMarketData):
    if ignoreUseRealTimeMarketData or useRealTimeMarketData():
        return getFile(valuationDate, 'MarketDataFilePathCVA')

    return getFile(valuationDate, 'MergedMarketDataFilePathCVA')

def getMarketDataFilePfe(valuationDate, ignoreUseRealTimeMarketData):
    if ignoreUseRealTimeMarketData or useRealTimeMarketData():
        return getFile(valuationDate, 'MarketDataFilePathPFE')

    return getFile(valuationDate, 'MergedMarketDataFilePathPFE')

def getMarketDataFileFva(valuationDate, ignoreUseRealTimeMarketData):
    if ignoreUseRealTimeMarketData or useRealTimeMarketData():
        return getFile(valuationDate, 'MarketDataFilePathFVA')

    return getFile(valuationDate, 'MergedMarketDataFilePathFVA')

def getRiskFactorArchiveFileCva(valuationDate):
    return getFile(valuationDate, 'RiskFactorArchiveFilePathCVA')

def getRiskFactorArchiveFilePfe(valuationDate):
    return getFile(valuationDate, 'RiskFactorArchiveFilePathPFE')

def getRiskFactorArchiveFileFva(valuationDate):
    return getFile(valuationDate, 'RiskFactorArchiveFilePathFVA')

#--------------Calculation Parameters-------------------------
def getCVABaseTimeGrid():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'CVA_BASE_TIME_GRID'):
        return AAUserParamsAndSettings.CVA_BASE_TIME_GRID
    else:
        return AAUserParamsAndSettingsTemplate.CVA_BASE_TIME_GRID

def getCVAAntithetic():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'CVA_ANTITHETIC'):
        return AAUserParamsAndSettings.CVA_ANTITHETIC
    else:
        return AAUserParamsAndSettingsTemplate.CVA_ANTITHETIC

def getCVAUseDynamicDates():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'CVA_USE_DYNAMIC_DATES'):
        return AAUserParamsAndSettings.CVA_USE_DYNAMIC_DATES
    else:
        return AAUserParamsAndSettingsTemplate.CVA_USE_DYNAMIC_DATES

def getCVAScenarioTimeGrid():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'CVA_SCENARIO_TIME_GRID'):
        return AAUserParamsAndSettings.CVA_SCENARIO_TIME_GRID
    else:
        return AAUserParamsAndSettingsTemplate.CVA_SCENARIO_TIME_GRID

def getCVAMaxHorizon():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'CVA_MAX_HORIZON'):
        return AAUserParamsAndSettings.CVA_MAX_HORIZON
    else:
        return AAUserParamsAndSettingsTemplate.CVA_MAX_HORIZON

def getCVAFirstToDefaultAdjustment():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'CVA_FIRST_TO_DEFAULT_ADJUSTMENT'):
        return AAUserParamsAndSettings.CVA_FIRST_TO_DEFAULT_ADJUSTMENT
    else:
        return AAUserParamsAndSettingsTemplate.CVA_FIRST_TO_DEFAULT_ADJUSTMENT

def getCVADeflateStochastically():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'CVA_DEFLATE_STOCHASTICALLY'):
        return AAUserParamsAndSettings.CVA_DEFLATE_STOCHASTICALLY
    else:
        return AAUserParamsAndSettingsTemplate.CVA_DEFLATE_STOCHASTICALLY

def getPFEBaseTimeGrid():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'PFE_BASE_TIME_GRID'):
        return AAUserParamsAndSettings.PFE_BASE_TIME_GRID
    else:
        return AAUserParamsAndSettingsTemplate.PFE_BASE_TIME_GRID

def getPFEAntithetic():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'PFE_ANTITHETIC'):
        return AAUserParamsAndSettings.PFE_ANTITHETIC
    else:
        return AAUserParamsAndSettingsTemplate.PFE_ANTITHETIC

def getPFEUseDynamicDates():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'PFE_USE_DYNAMIC_DATES'):
        return AAUserParamsAndSettings.PFE_USE_DYNAMIC_DATES
    else:
        return AAUserParamsAndSettingsTemplate.PFE_USE_DYNAMIC_DATES

def getPFEScenarioTimeGrid():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'PFE_SCENARIO_TIME_GRID'):
        return AAUserParamsAndSettings.PFE_SCENARIO_TIME_GRID
    else:
        return AAUserParamsAndSettingsTemplate.PFE_SCENARIO_TIME_GRID

def getPFEMaxHorizon():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'PFE_MAX_HORIZON'):
        return AAUserParamsAndSettings.PFE_MAX_HORIZON
    else:
        return AAUserParamsAndSettingsTemplate.PFE_MAX_HORIZON

def getPFEPercentiles():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'PFE_PERCENTILES'):
        return AAUserParamsAndSettings.PFE_PERCENTILES
    else:
        return AAUserParamsAndSettingsTemplate.PFE_PERCENTILES

def getBaseCurrency():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'BASE_CURRENCY'):
        return AAUserParamsAndSettings.BASE_CURRENCY
    else:
        return AAUserParamsAndSettingsTemplate.BASE_CURRENCY

def getRandomSeed():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'RANDOM_SEED'):
        return AAUserParamsAndSettings.RANDOM_SEED
    else:
        return AAUserParamsAndSettingsTemplate.RANDOM_SEED

def getNoModelEvolution():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'NO_MODEL_EVOLUTION'):
        return AAUserParamsAndSettings.NO_MODEL_EVOLUTION
    else:
        return AAUserParamsAndSettingsTemplate.NO_MODEL_EVOLUTION

def getAdjustToExternalMtM():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'ADJUST_TO_EXTERNAL_MTM'):
        return AAUserParamsAndSettings.ADJUST_TO_EXTERNAL_MTM
    else:
        return AAUserParamsAndSettingsTemplate.ADJUST_TO_EXTERNAL_MTM

def getExcludePaidToday():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'EXCLUDE_PAID_TODAY'):
        return AAUserParamsAndSettings.EXCLUDE_PAID_TODAY
    else:
        return AAUserParamsAndSettingsTemplate.EXCLUDE_PAID_TODAY

def getPFECalculationCurrency(cbInstrument):
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'PFECalculationCurrency'):
        return AAUserParamsAndSettings.PFECalculationCurrency(cbInstrument)
    else:
        return AAUserParamsAndSettingsTemplate.PFECalculationCurrency(cbInstrument)

#----------------Export to file dir--------------------------
def useRealTimeMarketData():
    return FParameters['RealTimeMarketData']

def useRiskFactorArchive():
    return FParameters['UseRiskFactorArchive']

def optimiseFVACalculation():
    return FParameters['OptimiseFVACalculation']

def useStressScenario():
    return FParameters['useStressScenario']

#----------------Export to file dir--------------------------
def getExportToFileDir():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'EXPORT_TO_FILE_DIR'):
        return AAUserParamsAndSettings.EXPORT_TO_FILE_DIR
    else:
        return AAUserParamsAndSettingsTemplate.EXPORT_TO_FILE_DIR
#-------------------------------------------------------------

def getUsePaceSetting():
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'USE_PACE'):
        return AAUserParamsAndSettings.USE_PACE
    else:
        return AAUserParamsAndSettingsTemplate.USE_PACE
        
def getTimeBucket():
    timeBucketStr = ""
    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'DEFAULT_TIMEBUCKET'):
        timeBucketStr = AAUserParamsAndSettings.DEFAULT_TIMEBUCKET
    else:
        timeBucketStr = AAUserParamsAndSettingsTemplate.DEFAULT_TIMEBUCKET
    
    storedTimeBucket = acm.FStoredTimeBuckets[timeBucketStr]
    if storedTimeBucket:
        return storedTimeBucket.TimeBuckets()

    return None

def getSupportedStressScenario():

    if USER_MODULE_EXISTS and hasattr(AAUserParamsAndSettings, 'DEFAULT_SUPPORTED_STRESSSCENARIO'):
        return AAUserParamsAndSettings.DEFAULT_SUPPORTED_STRESSSCENARIO
    else:
        return AAUserParamsAndSettingsTemplate.DEFAULT_SUPPORTED_STRESSSCENARIO
