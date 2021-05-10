""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/saccr/./etc/SACCRDataCreator.py"
import acm
import AAUtilFunctions as Util
import AADataUtilFunctions as DataUtil
import AAComposer
import math
import AAParamsAndSettingsHelper as Params
import AAParameterFiltration as ParamsFilter
import SACCRSettings
import datetime
import AADataCreator

logger = Params.getAdaptivAnalyticsLogger()

try:
    import AAValuation
except:
    logger.ELOG("Could not import module AAValuation")

        
def SystemParameters():
    sp_string = "<System Parameters>"
    sp_string += "\n"
    sp_string += "Base_Currency="
    sp_string += Params.getBaseCurrency()
    return sp_string


def PriceFactors(cvaMarketDataStrings, customMarketDataString):
    xml = []
    xml.append("\n<Price Factors>")
    xml.append(cvaMarketDataStrings)
    if customMarketDataString:
        xml.append(customMarketDataString)
    return '\n'.join(xml)

def createDataXML(systemParameters, priceFactors, valuationDate):
    dataFileName = SACCRSettings.MarketDataFilePath(valuationDate)
    staticData = ""
    with open (dataFileName, "r") as staticMarketDataFile:
        staticData=staticMarketDataFile.readlines()
    
    
    xml = []
    xml.append('\n'.join(staticData))
    xml.append(systemParameters)
    xml.append(priceFactors)
    return ''.join(xml)
    
  
def createSACCRMarketDataXML(marketDataString, currency, customMarketDataString, valuationDate):
    systemParameters = SystemParameters()
    priceFactors = PriceFactors('\n'.join(marketDataString), '\n'.join(customMarketDataString))
    return createDataXML(systemParameters, priceFactors, valuationDate)

def date_to_xldate(date):
    date1 = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    temp = datetime.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return int(delta.days) + (int(delta.seconds) / 86400)

def xldate_to_date(xldate): 
    temp = datetime.datetime(1900, 1, 1) 
    delta = datetime.timedelta(days=xldate)
    dt = temp+delta 
    return dt.strftime('%Y-%m-%d')

def convertIrRateTypeToStr(rateType):
    if rateType == 'Continuous':
        return '0D'
    elif rateType == 'Annual Comp':
        return '1Y'
    elif rateType == 'Semi Annual':
        return '6M'
    elif rateType == 'Quarterly':
        return '3M'
    elif rateType == 'Monthly':
        return '1M'
    else:
        return None

def createSACCRRateFixingString(curves, fxDiscountCurves, deflationCurve, valuationDate):
    curve_infos = []
    irCurveInformations = AADataCreator.getIrCurveInformations(curves, fxDiscountCurves, deflationCurve)
    for irCurveInformation in irCurveInformations:
    	AADataCreator.getUnderlyingCurveInfo(irCurveInformation, curve_infos, 1)
    	AADataCreator.getConstituentCurveInfo(irCurveInformation, curve_infos)
    	
    myCurveInfoLists = list(set(curve_infos))
    price_factorL = []
    for curve in myCurveInfoLists:
        price_factor = AADataCreator.InterestRatePriceFactor(curve, valuationDate)
        price_factorL.append(price_factor)

    header = 'DATE\t'
    for curve in myCurveInfoLists:
        rateType = convertIrRateTypeToStr(curve.StorageRateType())
        rateTypeStr ='\"\t'
        if rateType:
            rateTypeStr = ',' + rateType + '\"\t'
        header += '\"InterestRate.' + curve.Name()+ rateTypeStr
        
    header += '\n'

    dateList = []
    for curve in myCurveInfoLists:
        price_factor = AADataCreator.InterestRatePriceFactor(curve, valuationDate)
        dates = price_factor.getPointDates()
        for d in dates:
            dateList.append(date_to_xldate(d))

    dates = list(set(dateList))
    dates.sort()

    content = ''
    for d in dates:
        strD = xldate_to_date(d)
        strFixing = str(d) + '\t'
        for p in price_factorL:
            strFixing = strFixing + str(p.getRate(strD)) + '\t'
        content = content + strFixing + '\n'
    
    comment = "#Two comment rows" + '\n' + '#Columns	#Rows	' + '\n'
    summery = str(len(price_factorL) + 1) + '\t' + str(len(dates)) + '\n'
    result = comment + summery + header + content
    return result
