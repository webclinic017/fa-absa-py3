"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FConfirmationXML

DESCRIPTION
    This module is used to extend the behaviour of the core FConfirmationXML
    module.

    The following customisations have been done:

    - Addition of soft fix for AR 722957: Cancellation confirmation different from
      original. SPR 403306 Fixed in 2017.3.  This override MUST BE REMOVED once upgrade
      to latest version > 2017.3 is done.
    - Addition of GenerateFreeFormCancellationXml to generate the XML for a cancellation
      confirmation by: looking for a cancellation XML hook specified for an event and
      calling it if found; falling back on default/core behaviour should a cancellation
      XML hook not be found.
    - Addition of GetFreeFormCancellationXmlHook to find any cancellation XML hook
      specified for an event.
    - Addition of DefaultGenerateFreeFormCancellationXml to extract default/core
      behaviour for generating free-form cancellation confirmation XML out into a
      separate method.
    - Modification of GenerateXmlFromTemplate to replace default/core behaviour with a
      call to GenerateFreeFormCancellationXml.
    - Modification of import of FConfirmationParameters to be consistent with
      FConfirmationEngine and allow for optional confirmation parameters.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-10-25      FAOPS-226       Cuen Edwards            Letitia Carboni         Initial Implementation with soft fix for AR 722957
                                                                                migrated from organisation extension module.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

""" Compiled: 2017-07-12 14:02:12 """

# __src_file__ = "extensions/confirmation/etc/FConfirmationXML.py"

import xml.etree.ElementTree as ET
import FSwiftMessageTypeCalculator as Calculator
import FOperationsDocumentXMLDOM as opsxmldom

from FOperationsUtils import LogAlways
from FOperationsDocumentXML import FOperationsDocumentXML
from FOperationsDocumentXMLTemplateGetter import GetTemplate, IsCustomSwiftTemplate
from FDocumentationCompression import ZlibToXml, HexToZlib

from FOperationsDocumentXMLOverrideGetter import FOperationsDocumentXMLOverrideGetter as overrideGetter
from FOperationsDocumentXMLMD5Generator import FOperationsDocumentXMLMD5Generator as MD5Generator
import FSwiftParametersTemplate

try:
    import FConfirmationParameters as ConfirmationParameters
except ImportError as error:
    import FConfirmationParametersTemplate as ConfirmationParameters
    LogAlways("Failed to import FConfirmationParameters, " + str(error))

from FConfirmationEnums import ConfirmationType


class FConfirmationXML(object):
    def __init__(self, confirmation):
        self.__messageType = Calculator.Calculate(confirmation)
        self.__confirmation = confirmation
        self.__template = GetTemplate(confirmation, self.__messageType, ConfirmationParameters.MTMessageToXMLMap,
            ConfirmationParameters.templateToXMLMap, ConfirmationParameters.defaultXMLTemplate)
        self.__isCustomTemplate = IsCustomSwiftTemplate(self.__messageType, ConfirmationParameters.MTMessageToXMLMap)

    def GetConfirmationXMLOverride(self):
        overrideModule = 'FConfirmationSwiftXMLHooks'
        overrideXML = None
        coreMessageTypes = dict(FSwiftParametersTemplate.USED_MT_MESSAGES_CONFIRMATION)
        if self.__confirmation.IsApplicableForSWIFT():
            # #######################################################################################
            # Added condition to not include overrides for Cancellation messages.
            # AR  722957 : Cancellation confirmation different from original
            # SPR 403306 Fixed in 2017.3
            # ---------------------------------------------------------------------------------------
            # Old code:
            #if self.__messageType and not self.__isCustomTemplate:    #Do not apply overrides to custom templates
            # ---------------------------------------------------------------------------------------
            # new code with condition:
            if self.__messageType and not self.__isCustomTemplate and self.__confirmation.Type() != ConfirmationType.CANCELLATION:    #Do not apply overrides to custom templates
            # #######################################################################################
                overrideXML = overrideGetter(self.__messageType, coreMessageTypes, overrideModule).GetOverrideXML()
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
                xml = FConfirmationXML.GenerateFreeFormCancellationXml(self.__template, self.__confirmation,
                    overrideXML)
            else:
                xml = FOperationsDocumentXML.GenerateXmlFromTemplateAsString(self.__template, self.__confirmation,
                    overrideXML)
            return xml
        except Exception as e:
            errorMsg = 'Failed to generate XML. '
            e.args = (errorMsg + str(e.args[0]),)
            raise

    @staticmethod
    def GenerateFreeFormCancellationXml(cancellationTemplate, cancellationConfirmation, overrideXML):
        """
        Generate the XML for a cancellation confirmation.
        """
        cancellationXMLHook = FConfirmationXML.GetFreeFormCancellationXmlHook(cancellationConfirmation
            .EventChlItem().Name())
        if cancellationXMLHook is not None:
            return cancellationXMLHook.GenerateCancellationXML(cancellationTemplate, cancellationConfirmation,
                overrideXML)
        return FConfirmationXML.DefaultGenerateFreeFormCancellationXml(cancellationTemplate,
            cancellationConfirmation, overrideXML)

    @staticmethod
    def GetFreeFormCancellationXmlHook(eventName):
        """
        Get any free-form cancellation XML hook specified for an event.

        If no hook is found, None is returned.
        """
        if not hasattr(ConfirmationParameters, 'eventToFreeFormCancellationXMLHookMap'):
            return None
        eventToCancellationXMLHookMap = dict(ConfirmationParameters.eventToFreeFormCancellationXMLHookMap)
        return eventToCancellationXMLHookMap.get(eventName)

    @staticmethod
    def DefaultGenerateFreeFormCancellationXml(cancellationTemplate, cancellationConfirmation,
            overrideXML):
        """
        Default/Core behaviour for generating free-form cancellation
        confirmation XML.
        """
        opsDoc = cancellationConfirmation.ConfirmationReference().Documents()[0]
        if opsDoc.Data() != "":
            xml = ZlibToXml(HexToZlib(opsDoc.Data()))
            xml = FConfirmationXML.SetXMLValueForTag(xml, "TYPE", ConfirmationType.CANCELLATION)
        else:
            xml = FOperationsDocumentXML.GenerateXmlFromTemplateAsString(cancellationTemplate, cancellationConfirmation,
                overrideXML)
        return xml

    @staticmethod
    def SetXMLValueForTag(xmlString, tagName, value):
        root = ET.fromstring(xmlString)
        node = root.find(".//" + tagName)
        if node != None:
            node.text = value
        return ET.tostring(root, "UTF-8", "xml")
