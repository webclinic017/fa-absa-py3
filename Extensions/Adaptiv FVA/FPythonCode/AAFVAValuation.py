""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_fva/./etc/AAFVAValuation.py"
import AAImport
from xml.dom.minidom import parseString
import string
import AAValuation
import AAParamsAndSettingsHelper
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()
useStressScenario = AAParamsAndSettingsHelper.useStressScenario()

'''--------------------------------------------------------------------------
TODO:   The way functions are split up between AAValuation and AAIntegration 
        does not really map to the module names anymore. 
        Either merge them or split them up in a better way.
--------------------------------------------------------------------------'''
def __findNodeItem(root, matchedKey):
    for i in root.getElementsByTagName('KEY'):
        childItem = i.getAttribute('keyvalue').encode('ascii', 'ignore').replace(" ", "")
        if matchedKey.replace(" ", "") == childItem:
            return i
          
def ParseFvaResultXml(res_xml, cvaWrongWayRiskType, cvaScenName):
    doc = parseString(res_xml)
    scenarioKey = 'Base'
    if cvaScenName not in ['Base']:
        scenarioKey = "Scen" + cvaScenName
    AAValuation.validateCalculation(doc)
    data = doc.getElementsByTagName('DATA')
    if len(data) == 1:
        scenNode = data[0]
        if useStressScenario:
            scenNode = __findNodeItem(data[0], scenarioKey)
            if not scenNode:
                scenNode = data[0]

        bankNode = __findNodeItem(scenNode, 'Bank')
        if not bankNode:
            raise AssertionError("ParseFvaResultXml failed to find Bank keyword.")

        fvaNode = __findNodeItem(bankNode, 'FVA')
        fva = float(fvaNode.firstChild.nodeValue)
        
        fbaNode = __findNodeItem(bankNode, 'FBA')
        fba = float(fbaNode.firstChild.nodeValue)
        
        fcaNode = __findNodeItem(bankNode, 'FCA')
        fca = float(fcaNode.firstChild.nodeValue)
        
        return_param = (fva, fba, fca)
        return return_param

    raise AssertionError("Adaptiv valuation failed and only returned errors.")
