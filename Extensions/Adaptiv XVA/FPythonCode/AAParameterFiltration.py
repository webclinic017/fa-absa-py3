""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAParameterFiltration.py"
import acm
import AAParamsAndSettingsHelper
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

def isValidExpiryDateMethod(volatility):
    if volatility.CapFloorVolatilityType() == "Par": 
        return volatility.ExpiryDateMethod() == "Expiry-Tenor"
    else:
        return True
      
def isValidEquitySurface(volatility):
    if volatility.IsKindOf("FVolatilityInformation"):
        if volatility.StrikeType() == "Absolute":
            return True
        else:
            logger.WLOG("Volatility structure %s must have strike type Absolute to be a valid Equity Price Volatility price factor" % (volatility.Name()))
    return False

def isValidCommoditySurface(volatility):
    if volatility.IsKindOf("FVolatilityInformation"):
        if volatility.StrikeType() == "Absolute":
            return True
        else:
            logger.WLOG("Volatility structure %s must have strike type Absolute to be a valid Commodity Price Volatility price factor" % (volatility.Name()))
    return False
    
def isValidFxSurface(volatility):
    if volatility.IsKindOf("FVolatilityInformation"):
        if volatility.StructureType() == "Malz":
            return True
        elif volatility.StrikeType() == "Absolute":
            return True
        else:
            logger.WLOG("Volatility structure %s is not a valid FX Volatility" % (volatility.Name()))
    return False
    
def isValidInterestRateVolatilitySurface(volatility):
    if volatility.IsKindOf("FVolatilityInformation"):
        if volatility.CapFloorVolatilityType() == 'Par' or volatility.CapFloorVolatilityType() == 'Forward':
            if volatility.StrikeType() == "Absolute":
                if isValidExpiryDateMethod(volatility):
                    return True
                else:
                    logger.WLOG("Incorrect expiry date method for %s. 'Expiry-Tenor' is the only supported Expiry Date Method for Cap/Floor volatilities" % (volatility.Name()))
            else:
                logger.WLOG("Volatility structure %s must have strike type Absolute to be a valid Interest Rate Volatility price factor" % (volatility.Name()))
        else:
            if volatility.StrikeType() == "Rel Frw":
                return True
            else:
                logger.WLOG("Volatility structure %s must have strike type Rel Frw to be a valid Interest Yield Volatility price factor" % (volatility.Name()))
    return False
