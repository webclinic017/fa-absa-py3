""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentXMLOverrideGetter.py"
import FOperationsDocumentXMLDOM as opsxmldom

class FOperationsDocumentXMLOverrideGetter():

    def __init__(self, messageType, coreMessageTypes, overrideModule):
        self.messsageType = messageType
        self.overrideModule = overrideModule
        self.isCustomMT = self.messsageType not in coreMessageTypes

    def GetOverrideXML(self):
        try:
            overrideModule = self.LoadOverrideModule()
            if not overrideModule:
                return None

            commonBlockOverride = self.GetCommonBlockOverride(overrideModule)
            messageBlockOverride = self.GetMessageBlockOverride(overrideModule)
            overrideXML = opsxmldom.MergeXML(commonBlockOverride, messageBlockOverride)
            return opsxmldom.ToXml(overrideXML)
        except Exception as e:
            errorMsg = "Could not generate override XML for SWIFT message type {}: {}".format(self.messsageType, str(e))
            e.args = (errorMsg,)
            raise

    def LoadOverrideModule(self):
        overrideModule = None
        try:
            overrideModule = __import__(self.overrideModule)
        except ImportError as e:
            if self.isCustomMT:
                errorMsg = 'User override module %s is missing. No XML generated.' % self.overrideModule
                e.args = (errorMsg,)
                raise

        return overrideModule

    def GetCommonBlockOverride(self, overrideModule):
        commonBlockOverride = getattr(overrideModule, 'commonBlock_template', None)
        if commonBlockOverride:
            commonBlockOverride = opsxmldom.CreateXMLMiniDom(commonBlockOverride)
            opsxmldom.InsertFileAttribute(commonBlockOverride)
        return commonBlockOverride

    def GetMessageBlockOverride(self, overrideModule):
        messageBlockOverride = None
        messageBlockText = self.GetMessageBlock(overrideModule)

        if messageBlockText:
            messageBlockOverride = opsxmldom.CreateXMLMiniDom(messageBlockText)
            opsxmldom.InsertFileAttribute(messageBlockOverride)

        return messageBlockOverride

    def GetMessageBlock(self, overrideModule):
        messageBlock = None
        try:
            messageBlock = getattr(overrideModule, 'MT%s_template' % self.messsageType)
        except AttributeError as e:
            if self.isCustomMT:
                errorMsg = 'MT%s_template in user override module %s is missing. No XML generated.' % (self.messsageType, overrideModule.__name__)
                e.args = (errorMsg,)
                raise
        return messageBlock

