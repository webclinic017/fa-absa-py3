""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_fva/./etc/AAFVAPluginSettings.py"
'''-------------------------------------------------------------
    After customisation save the AAUserParamsAndSettingsTemplate
    module as AAUserParamsAndSettings",
-------------------------------------------------------------'''
import acm
import ast
import FBDPCommon
import AAParamsAndSettingsHelper
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()


#---------------Market data path functions---------
def MarketDataFilePathFVA(valuationDate):
    '''---------------------------------------
    The valuationDate parameter enables the use of historical price
    factors in valuation. Example:
    if valutionDate < acm.Time().DateToday():
        return 'C:/Adaptiv/bin/MarketDataBaseVal' + str(valuationDate) + '.dat'
    '''
    return 'C:/Adaptiv/bin/MarketData.dat'

def getCurveName(key, dict):
    curveName = ''
    if key in dict:
        curveName = dict[key]
    else:
        message = 'Get funding curve. Missing key: ' + key + ' Using key ' + key[0:3] + ' instead.'
        logger.LOG(message)
        if key[0:3] in dict:
            curveName = dict[key[0:3]]
        else:
            logger.ELOG("Error, no funding curve mapped for " + key[0:3] + "or " + key)
    
    return curveName
    
def getFundingCostInterestCurveIrInformation(key):
    fundingCostInterestCurve = FBDPCommon.valueFromFParameter('FxVAParameters', 'FundingCostInterestCurve')
    fundingCostInterestCurve = ast.literal_eval(fundingCostInterestCurve)
    curveName = getCurveName(key, fundingCostInterestCurve)
    if curveName and acm.FYieldCurve[curveName]:
        return acm.FYieldCurve[curveName].IrCurveInformation()
    return None

def getFundingBenefitInterestCurveIrInformation(key):
    fundingBenefitInterestCurve = FBDPCommon.valueFromFParameter('FxVAParameters', 'FundingBenefitInterestCurve')
    fundingBenefitInterestCurve = ast.literal_eval(fundingBenefitInterestCurve)
    curveName = getCurveName(key, fundingBenefitInterestCurve)
    if curveName and acm.FYieldCurve[curveName]:
        return acm.FYieldCurve[curveName].IrCurveInformation()
    return None

def getFundingCreditCurveIrInformation(key):
    fundingCreditCurve = FBDPCommon.valueFromFParameter('FxVAParameters', 'FundingCreditCurve')
    fundingCreditCurve = ast.literal_eval(fundingCreditCurve)
    curveName = getCurveName(key, fundingCreditCurve)
    if curveName and acm.FYieldCurve[curveName]:
        return acm.FYieldCurve[curveName].IrCurveInformation()
    return None

def getRiskFreeCurveIrInformation(key):
    riskFreeCurve = FBDPCommon.valueFromFParameter('FxVAParameters', 'RiskFreeCurve')
    riskFreeCurve = ast.literal_eval(riskFreeCurve)
    curveName = getCurveName(key, riskFreeCurve)
    if curveName and acm.FYieldCurve[curveName]:
        return acm.FYieldCurve[curveName].IrCurveInformation()
    return None
