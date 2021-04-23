""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAUserParamsAndSettingsTemplate.py"
'''-------------------------------------------------------------
    After customisation save the AAUserParamsAndSettingsTemplate
    module as AAUserParamsAndSettings",
-------------------------------------------------------------'''
import acm


#----------------Calculation parameters-----------------------
# CVA Parameters
CVA_BASE_TIME_GRID                       = "0d 2d 1w 2w 1m 3m(3m)"
CVA_ANTITHETIC                           = "No"
CVA_USE_DYNAMIC_DATES                    = "Yes"
CVA_SCENARIO_TIME_GRID                   = "0d 2d 1w 2w 1m 3m(3m)"
CVA_MAX_HORIZON                          = ""
CVA_FIRST_TO_DEFAULT_ADJUSTMENT          = "None"
CVA_DEFLATE_STOCHASTICALLY               = "Yes"

# PFE Parameters
PFE_BASE_TIME_GRID                       = "0d 2d 1w 2w 1m 3m(3m)"
PFE_ANTITHETIC                           = "No"
PFE_USE_DYNAMIC_DATES                    = "Yes"
PFE_SCENARIO_TIME_GRID                   = "0d 2d 1w 2w 1m 3m(3m)"
PFE_MAX_HORIZON                          = ""
PFE_PERCENTILES                          = "[99, 95, 90]"

# CVA/PFE Parameters
BASE_CURRENCY                            = "EUR"
RANDOM_SEED                              = "1"
NO_MODEL_EVOLUTION                       = "Constant"
ADJUST_TO_EXTERNAL_MTM                   = "Yes"
EXCLUDE_PAID_TODAY                       = "No"
USE_PACE                                 = False
DEFAULT_TIMEBUCKET                       = 'CVA_1Y-3Y-Rest'

DEFAULT_SUPPORTED_STRESSSCENARIO         = ['BenchmarkShiftUp', 'BenchmarkShiftUpBucket', 'BenchmarkShiftDown', 'BenchmarkShiftDownBucket', 'CreditShiftUp', 'CreditShiftUpBucket', 'CreditShiftDown', 'CreditShiftDownBucket', 'CreditAttribution']

#----------------Adaptiv DLL path-----------------------------
ADAPTIV_PATH = "C:\\Program Files\\FIS\\Adaptiv Analytics\\"

#----------------Adaptiv Analytics Studio path-----------------
ADAPTIV_ANALYTICS_STUDIO_PATH       = r'C:\Program Files\FIS\Adaptiv Analytics\AAStudio.exe'

#----------------Adaptiv Analytics Log path-----------------
ADAPTIV_ANALYTICS_LOG_PATH       = r'C:\temp\AdaptivCVA.txt'

#---------------Market data path functions---------
def MarketDataFilePathBaseVal(valuationDate):
    '''---------------------------------------
    The valuationDate parameter enables the use of historical price
    factors in valuation. Example:
    if valutionDate < acm.Time().DateToday():
        return 'C:/Adaptiv/bin/MarketDataBaseVal' + str(valuationDate) + '.dat'
    '''
    return 'C:/Adaptiv/bin/MarketData.dat'

def MarketDataFilePathCVA(valuationDate):
    '''---------------------------------------
    The valuationDate parameter enables the use of historical price
    factors in valuation. Example:
    if valutionDate < acm.Time().DateToday():
        return 'C:/Adaptiv/bin/MarketDataCVA' + str(valuationDate) + '.dat'
    '''
    return 'C:/Adaptiv/bin/MarketData.dat'

def MarketDataFilePathPFE(valuationDate):
    '''---------------------------------------
    The valuationDate parameter enables the use of historical price
    factors in valuation. Example:
    if valutionDate < acm.Time().DateToday():
        return 'C:/Adaptiv/bin/MarketDataPFE' + str(valuationDate) + '.dat'
    '''
    return 'C:/Adaptiv/bin/MarketData.dat'

def MarketDataFilePathFVA(valuationDate):
    '''---------------------------------------
    The valuationDate parameter enables the use of historical price
    factors in valuation. Example:
    if valutionDate < acm.Time().DateToday():
        return 'C:/Adaptiv/bin/MarketDataFVA' + str(valuationDate) + '.dat'
    '''
    return 'C:/Adaptiv/bin/MarketData.dat'

def MergedMarketDataFilePathCVA(valuationDate):
    '''---------------------------------------
    The valuationDate parameter enables the use of historical price
    factors in valuation. Example:
    if valutionDate < acm.Time().DateToday():
        return 'C:/Adaptiv/bin/MergedMarketDataCVA' + str(valuationDate) + '.dat'
    '''
    return 'C:/Adaptiv/bin/MergedMarketDataCVA.dat'

def MergedMarketDataFilePathPFE(valuationDate):
    '''---------------------------------------
    The valuationDate parameter enables the use of historical price
    factors in valuation. Example:
    if valutionDate < acm.Time().DateToday():
        return 'C:/Adaptiv/bin/MergedMarketDataPFE' + str(valuationDate) + '.dat'
    '''
    return 'C:/Adaptiv/bin/MergedMarketDataPFE.dat'

def MergedMarketDataFilePathFVA(valuationDate):
    '''---------------------------------------
    The valuationDate parameter enables the use of historical price
    factors in valuation. Example:
    if valutionDate < acm.Time().DateToday():
        return 'C:/Adaptiv/bin/MergedMarketDataFVA' + str(valuationDate) + '.dat'
    '''
    return 'C:/Adaptiv/bin/MergedMarketDataFVA.dat'
    
def RiskFactorArchiveFilePathCVA(valuationDate):
    '''---------------------------------------
    The valuationDate parameter enables the use of historical price
    factors in valuation. Example:
    if valutionDate < acm.Time().DateToday():
        return 'C:/Adaptiv/bin/RiskFactorArchiveCVA' + str(valuationDate) + '.dat'
    '''
    return 'C:/Adaptiv/bin/RiskFactorArchiveCVA.dat'

def RiskFactorArchiveFilePathPFE(valuationDate):
    '''---------------------------------------
    The valuationDate parameter enables the use of historical price
    factors in valuation. Example:
    if valutionDate < acm.Time().DateToday():
        return 'C:/Adaptiv/bin/RiskFactorArchivePFE' + str(valuationDate) + '.dat'
    '''
    return 'C:/Adaptiv/bin/RiskFactorArchivePFE.dat'

def RiskFactorArchiveFilePathFVA(valuationDate):
    '''---------------------------------------
    The valuationDate parameter enables the use of historical price
    factors in valuation. Example:
    if valutionDate < acm.Time().DateToday():
        return 'C:/Adaptiv/bin/RiskFactorArchiveFVA' + str(valuationDate) + '.dat'
    '''
    return 'C:/Adaptiv/bin/RiskFactorArchiveFVA.dat'
def PFECalculationCurrency(cbInstrument):
    additionalInfo = cbInstrument.AdditionalInfo()
    if not additionalInfo:
        return cbInstrument.Currency()

    pfeCurrency = None
    try:
        pfeCurrency = additionalInfo.PFECurrency()
    except:
        pass

    pfeCurr = None
    if pfeCurrency:
        pfeCurr = acm.FCurrency[pfeCurrency]

    if pfeCurr:
        return pfeCurr

    return cbInstrument.Currency()

#---------------Price factor settings---------
def getNumberOfCurvePoints():
    return 100
    

#----------------Export to file directory------
'''
Sets the directory to use when exporting a CVA calculation
through the right-click menu in Trading Manager. If set to
None one of the following directories will be used:
The directory named by the TMPDIR/TEMP or TMP environment variable or
a platform specific location.
'''
EXPORT_TO_FILE_DIR = None
