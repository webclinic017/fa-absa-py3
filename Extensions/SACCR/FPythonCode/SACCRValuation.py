""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/saccr/./etc/SACCRValuation.py"
import AAImport
from xml.dom.minidom import parseString
import string
import AAParamsAndSettingsHelper
import datetime
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()
OLE_TIME_ZERO = datetime.datetime(1899, 12, 30, 0, 0, 0)

'''--------------------------------------------------------------------------
TODO:   The way functions are split up between AAValuation and AAIntegration 
        does not really map to the module names anymore. 
        Either merge them or split them up in a better way.
--------------------------------------------------------------------------'''

def validateCalculation(doc):
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
                elif error.getAttributeNode(nodeStr).nodeValue == "Warning":
                    logger.WLOG("Adaptiv warning: " + error.firstChild.nodeValue)

def Calculate(xml_string):
    ascii_res = AAImport.ea.Calculate(xml_string, 1)
    return ascii_res.encode('ascii', 'ignore')