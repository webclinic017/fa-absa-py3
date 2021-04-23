""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAValuation.py"
import AAImport
from xml.dom.minidom import parseString
import string
import AAParamsAndSettingsHelper
import datetime
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()
useStressScenario = AAParamsAndSettingsHelper.useStressScenario()
OLE_TIME_ZERO = datetime.datetime(1899, 12, 30, 0, 0, 0)

'''--------------------------------------------------------------------------
TODO:   The way functions are split up between AAValuation and AAIntegration 
        does not really map to the module names anymore. 
        Either merge them or split them up in a better way.
--------------------------------------------------------------------------'''

def validateCalculation(doc):
    validated = True
    errors = doc.getElementsByTagName('Errors')
    for error in errors[0].childNodes:
        if error.nodeType == error.TEXT_NODE:
            continue
        nodeStr = None
        if error.hasAttribute('Level'):
            nodeStr = 'Level'
        elif error.hasAttribute('Severity'):
            nodeStr = 'Severity'
        if nodeStr:
            if not str(error.firstChild.nodeValue)[0:14] == "Server Garbage": # TODO: The string compare check for Garbage Server is a temporary fix until the actual problem has been adressed.
                if error.getAttributeNode(nodeStr).nodeValue == "Error":
                    logger.ELOG("Adaptiv error: " + error.firstChild.nodeValue)
                    validated = False
                elif error.getAttributeNode(nodeStr).nodeValue == "Warning":
                    logger.WLOG("Adaptiv warning: " + error.firstChild.nodeValue)
    return validated

def Calculate(xml_string):
    ascii_res = AAImport.ea.Calculate(xml_string, 1)
    return ascii_res.encode('ascii', 'ignore') 

def ParseBaseValuationResultXml(res_xml):
    doc = parseString(res_xml)
    if validateCalculation(doc):
        values = doc.getElementsByTagName('CurrencyValues')
        if not values:
            return 0
        for val in values:
            if val.getAttributeNode('currency').nodeValue == "TOTAL":
                val_array = val.firstChild.nodeValue.split(',')
                pv = float(val_array[0]) 
                return pv
    else:
        raise AssertionError("Adaptiv valuation failed and only returned errors.")

def ParsePFEResultXml(res_xml, bucketStartDate, bucketEndDate):
    doc = parseString(res_xml)
    if validateCalculation(doc):
        series = doc.getElementsByTagName('Series')
        if len(series) == 1:
            foundItem = None
            for item in series[0].getElementsByTagName('SeriesItem'):
                name = item.getAttribute('Name').encode('ascii', 'ignore')
                if 'BankExposure' in name.replace(" ", ""):
                    foundItem = item
                    break
                    
            xValue = foundItem.getElementsByTagName('X')[0].firstChild.nodeValue  
            yValue = foundItem.getElementsByTagName('Y')[0].firstChild.nodeValue 
            
            dates = [(OLE_TIME_ZERO + datetime.timedelta(float(i))).date().isoformat() for i in (xValue).split(",")]
            floats = [float(i) for i in (yValue).split(",")]
            
            startIndex = len(dates)-1
            try:
                startIndex = next(x[0] for x in enumerate(dates) if x[1] > bucketStartDate)
            except StopIteration as ex:
                pass
                
            endIndex = len(dates)-1
            try:
                endIndex = next(x[0] for x in enumerate(dates) if x[1] >= bucketEndDate)
                if dates[endIndex] == bucketEndDate and endIndex != len(dates) - 1:
                    endIndex += 1
            except StopIteration as ex:
                pass
            
            resultPFEs = floats    
            resultDates = dates
            if startIndex >= endIndex:
                resultPFEs = [floats[startIndex]]
                resultDates = [dates[startIndex]]
            
            elif endIndex == len(dates)-1 :
                resultPFEs = floats[startIndex:-1]
                resultDates = dates[startIndex:-1]
            
            else:
                resultPFEs = floats[startIndex:endIndex]
                resultDates = dates[startIndex:endIndex]
            return resultPFEs, resultDates
    else:
        raise AssertionError("Adaptiv valuation failed and only returned errors.")

def getPFEResults(res_xml):
    doc = parseString(res_xml)
    validateCalculation(doc)
    series = doc.getElementsByTagName('Series')
    if len(series) == 1:
        foundItem = None
        for item in series[0].getElementsByTagName('SeriesItem'):
            name = item.getAttribute('Name').encode('ascii', 'ignore')
            if 'BankExposure' in name.replace(" ", ""):
                foundItem = item
                break
                
        xValue = foundItem.getElementsByTagName('X')[0].firstChild.nodeValue  
        yValue = foundItem.getElementsByTagName('Y')[0].firstChild.nodeValue 
        
        dates = [(OLE_TIME_ZERO + datetime.timedelta(float(i))).date().isoformat() for i in (xValue).split(",")]
        floats = [float(i) for i in (yValue).split(",")]
        
        return dates, floats

def ParsePFEResultXmlWithMultiplePercentile(res_xml):
    doc = parseString(res_xml)
    if validateCalculation(doc):
        series = doc.getElementsByTagName('Series')
        if len(series) == 1:
            results = {}
            for item in series[0].getElementsByTagName('SeriesItem'):
                name = item.getAttribute('Name').encode('ascii', 'ignore')
                if 'BankExposure' in name.replace(" ", ""):
                    percentile = filter(str.isdigit,  name)
                    yValue = item.getElementsByTagName('Y')[0].firstChild.nodeValue 
                    floats = [float(i) for i in (yValue).split(",")]
                    results[percentile] = floats
            return results
    else:
        raise AssertionError("Adaptiv valuation failed and only returned errors.")


def __findNodeItem(root, matchedKey):
    for i in root.getElementsByTagName('KEY'):
        childItem = i.getAttribute('keyvalue').encode('ascii', 'ignore').replace(" ", "")
        if matchedKey.replace(" ", "") == childItem:
            return i

def __getNodeValue(node, cvaWrongWayRiskType):
    for e in node.getElementsByTagName('KEY'):
        kValue = e.getAttribute('keyvalue').encode('ascii', 'ignore')
        if cvaWrongWayRiskType in kValue.replace(" ", ""):
            return float(e.firstChild.nodeValue)
            
def ParseCvaResultXml(res_xml, cvaWrongWayRiskType, cvaScenName):
    doc = parseString(res_xml)
    scenarioKey = 'Base'
    if cvaScenName not in ['Base']:
        scenarioKey = "Scen " + cvaScenName
    if validateCalculation(doc):
        data = doc.getElementsByTagName('DATA')
        if len(data) == 1:
            scenNode = data[0]
            if useStressScenario:
                scenNode = __findNodeItem(data[0], scenarioKey)
                if not scenNode:
                    scenNode = data[0]

            bankNode = __findNodeItem(scenNode, 'Bank')
            if not bankNode:
                raise AssertionError("ParseCvaResultXml failed to find Bank keyword.")

            cvaNode = __findNodeItem(bankNode, 'CVA')
            cva = __getNodeValue(cvaNode, cvaWrongWayRiskType)
            
            dvaNode = __findNodeItem(bankNode, 'DVA')
            dva = __getNodeValue(dvaNode, cvaWrongWayRiskType)
            
            bilateralNode = __findNodeItem(bankNode, 'Bilateral')
            bilateral = __getNodeValue(bilateralNode, cvaWrongWayRiskType)
            
            return_param = (cva, dva, bilateral)
            return return_param
    else:
        raise AssertionError("Adaptiv valuation failed and only returned errors.")
