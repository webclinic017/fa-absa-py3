""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationXML.py"

import xml.etree.ElementTree as ET
import FSwiftMessageTypeCalculator as Calculator
import FSwiftMTConfirmation

import FOperationsDocumentXMLDOM as opsxmldom

from FOperationsUtils import LogAlways
from FOperationsDocumentXML import FOperationsDocumentXML
from FOperationsDocumentXMLTemplateGetter import GetTemplate, IsCustomSwiftTemplate
from FDocumentationCompression import ZlibToXml, HexToZlib

from FOperationsDocumentXMLOverrideGetter import FOperationsDocumentXMLOverrideGetter as overrideGetter
from FOperationsDocumentXMLMD5Generator import FOperationsDocumentXMLMD5Generator as MD5Generator
import FSwiftParametersTemplate

from FConfirmationEnums import ConfirmationType

class FConfirmationXML(object):
    def __init__(self, confirmation):
        from FConfirmationParameters import MTMessageToXMLMap, templateToXMLMap, defaultXMLTemplate

        if confirmation.IsApplicableForSWIFT():
            self.__messageType = Calculator.Calculate(confirmation)
        else:
            self.__messageType = 0
        self.__confirmation = confirmation
        self.__template = GetTemplate(confirmation, self.__messageType, MTMessageToXMLMap, templateToXMLMap, defaultXMLTemplate)
        self.__isCustomTemplate = IsCustomSwiftTemplate(self.__messageType, MTMessageToXMLMap)

    def GetConfirmationXMLOverride(self):
        overrideModule = 'FConfirmationSwiftXMLHooks'
        overrideXML = None
        coreMessageTypes = dict(FSwiftParametersTemplate.USED_MT_MESSAGES_CONFIRMATION)
        if self.__confirmation.IsApplicableForSWIFT():
            if self.__messageType and not self.__isCustomTemplate:    #Do not apply overrides to custom templates
                overrideXML = overrideGetter(self.__messageType, coreMessageTypes, overrideModule).GetOverrideXML()

            if overrideXML and self.__confirmation.Type() == ConfirmationType.CANCELLATION:
                overridableCancellationTags = ['YOUR_REFERENCE', 'TYPE_OF_OPERATION']
                overrideXML = opsxmldom.FilterSwiftTemplateTags(overrideXML, overridableCancellationTags)

        overrideXMLList = list()
        if overrideXML:
            overrideXMLList.append(overrideXML)
        return overrideXMLList

    def RemoveSwiftChilds(self):
        template = self.__template
        if self.__confirmation.IsApplicableForSWIFT():
            if not self.__messageType:
                template = opsxmldom.RemoveSwiftChilds(template)
        return template

    def GenerateMD5FromTemplate(self):
        try:
            template = self.RemoveSwiftChilds()
            overrideXML = self.GetConfirmationXMLOverride()
            return MD5Generator.GenerateMD5FromTemplate(template, self.__confirmation, overrideXML)
        except Exception as e:
            errorMsg = 'Failed to generate checksum for confirmation %d. ' % (self.__confirmation.Oid())
            LogAlways(errorMsg + str(e))
            return ''

    def GenerateXmlFromTemplate(self):
        try:
            overrideXML = self.GetConfirmationXMLOverride()
            if self.__confirmation.Type() == "Cancellation" and not self.__confirmation.IsApplicableForSWIFT():
                opsDoc = self.__confirmation.ConfirmationReference().Documents()[0]
                if opsDoc.Data() != "":
                    xml = ZlibToXml(HexToZlib(opsDoc.Data()))
                    xml = FConfirmationXML.SetXMLValueForTag(xml, "TYPE", ConfirmationType.CANCELLATION)
                else:
                    xml = FOperationsDocumentXML.GenerateXmlFromTemplateAsString(self.__template, self.__confirmation, overrideXML)
            else:
                xml = FOperationsDocumentXML.GenerateXmlFromTemplateAsString(self.__template, self.__confirmation, overrideXML)
            return xml
        except Exception as e:
            errorMsg = 'Failed to generate XML. '
            e.args = (errorMsg + str(e.args[0]),)
            raise

    @staticmethod
    def SetXMLValueForTag(xmlString, tagName, value):
        root = ET.fromstring(xmlString)
        node = root.find(".//" + tagName)
        if node != None:
            node.text = value
        return ET.tostring(root, "UTF-8", "xml")
