""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/saccr/./etc/SACCRIntegration.py"
import AAParamsAndSettingsHelper
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()
import xml.etree.ElementTree as xmlElementTree
import datetime
import SACCRSettings
import os

try:
    import SACCRValuation
except:
    logger.ELOG("Could not import module SACCRValuation")
import acm

def AssembleXML(instName, dealsXML, marketDataXML, rateFixingStr, currency, valuationDate):
    currencyName = currency.Name()
    date = datetime.datetime.strptime(valuationDate, '%Y-%m-%d').strftime(
            '%d%b%Y')
    
    dealDirName = SACCRSettings.SACCRDealOutFilePath() + date
    if not os.path.exists(dealDirName):
        os.makedirs(dealDirName)
    dataDirName = SACCRSettings.SACCRMarketDataOutFilePath() + date
    if not os.path.exists(dataDirName):
        os.makedirs(dataDirName)
    arfDirName = SACCRSettings.RateFixingFilePath() + date
    if not os.path.exists(arfDirName):
        os.makedirs(arfDirName)
        
    dealFileName = dealDirName + '/deal_' + instName +'.AAP'
    dataFileName = dataDirName + '/marketData_' + instName +'.DAT'
    arfFileName = arfDirName + '/ratefixings_' + instName +'.ARF'

    with open(dealFileName, "w") as dealFile:
        dealFile.write(dealsXML)
        dealFile.close()

    with open(dataFileName, "w") as marketDataFile:
        marketDataFile.write(marketDataXML)
        marketDataFile.close()

    with open(arfFileName, "w") as arfFile:
        arfFile.write(rateFixingStr)
        arfFile.close()
        
    request = xmlElementTree.Element('Analysis')
    calculation = xmlElementTree.SubElement(
        request, 'Calculation',
        name='SACCR',
        sink='artiQ'
    )
    xmlElementTree.SubElement(
        calculation, 'Property',
        name='Rate Fixings', value=arfFileName
    )
    xmlElementTree.SubElement(
        calculation, 'Property',
        name='Reporting Currency', value=currencyName
    )
    xmlElementTree.SubElement(
        calculation, 'Property',
        name='Deals',
        value=dealFileName
    )
    xmlElementTree.SubElement(
        calculation, 'Property', 
        name='Base Date',
        value=date
    )
    xmlElementTree.SubElement(
        calculation, 'Property',
        name='Destination Cube', value='Default'
    )
    xmlElementTree.SubElement(
        calculation, 'Property',
        name='Destination Catalog', 
        value='SACCR'
    )
    xmlElementTree.SubElement(
        calculation, 'Property',
        name='Market Data', 
        value=dataFileName
    )
    
    requestXml = xmlElementTree.tostring(request)
    return requestXml
       
def Calculate(instName, dealsXML, marketDataXML, ratefixingStr, currency, valuationDate):
    xml = AssembleXML(instName, dealsXML, marketDataXML, ratefixingStr, currency, valuationDate)
    res_xml = SACCRValuation.Calculate(xml)
    return res_xml
