""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementXML.py"

import FSwiftMessageTypeCalculator as Calculator
import FOperationsDocumentXMLTemplateGetter as TemplateGetter
import FSwiftParametersTemplate

from FOperationsDocumentXMLOverrideGetter import FOperationsDocumentXMLOverrideGetter as overrideGetter
from FOperationsDocumentXML import FOperationsDocumentXML
from FSwiftMTSecuritiesSettlement import IsSecurityCancellation

try:
    from FSettlementParameters import MTMessageToXMLMap
except ImportError:
    from FSettlementParametersTemplate import MTMessageToXMLMap

n99OverrideTypes = {199: [199, 103], 299: [299, 202]}

class FSettlementXML(object):
    def __init__(self, settlement):
        self.__messageType = Calculator.Calculate(settlement)
        self.__settlement = settlement
        self.__template = TemplateGetter.GetSwiftTemplate(self.__messageType, MTMessageToXMLMap)
        self.__isCustomTemplate = TemplateGetter.IsCustomSwiftTemplate(self.__messageType, MTMessageToXMLMap)

    def GetSettlementXMLOverride(self):
        overrideXML = None
        if self.__messageType and not self.__isCustomTemplate and not IsSecurityCancellation(self.__settlement):    #Do not apply overrides to custom templates and security cancellations
            overrideXML = self.RetrieveOverrideXML()
        return overrideXML

    def GenerateXmlFromTemplate(self):
        try:
            overrideXML = self.GetSettlementXMLOverride()
            return FOperationsDocumentXML.GenerateXmlFromTemplateAsString(self.__template, self.__settlement, overrideXML)
        except Exception as e:
            errorMsg = 'Failed to generate XML. '
            e.args = (errorMsg + str(e.args[0]),)
            raise

    def RetrieveOverrideXML(self):
        overrideModule = 'FSettlementSwiftXMLHooks'
        coreMessageTypes = dict(FSwiftParametersTemplate.USED_MT_MESSAGES_SETTLEMENT)
        xmlList = list()
        messageTypes = self.RetrieveAllMessageTypes()

        for mtType in messageTypes:
            overrideXML = overrideGetter(mtType, coreMessageTypes, overrideModule).GetOverrideXML()
            if overrideXML:
                xmlList.append(overrideXML)
        return xmlList

    def RetrieveAllMessageTypes(self):
        if self.__messageType in list(n99OverrideTypes.keys()):
            return n99OverrideTypes[self.__messageType]
        return [self.__messageType]


