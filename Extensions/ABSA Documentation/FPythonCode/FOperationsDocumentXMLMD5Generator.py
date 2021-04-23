"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FOperationsDocumentXMLMD5Generator

DESCRIPTION
    This module is used to extend the behaviour of the core FOperationsDocumentXMLMD5Generator
    module.

    The following customisations have been done:

    - Overrode FOperationsDocumentXMLMD5Generator.ProcessOther method (inherited from 
      customised FOperationsDocumentXML) to remove any elements that should be excluded when 
      generating the MD5 checksum.      
    - Addition of method FOperationsDocumentXMLMD5Generator.RemoveElementsWithIgnoreUpdate
      to perform the actual removal of elements to be excluded.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-08-28      FAOPS-218       Cuen Edwards            Kgomotso Gumbo          Added support for the ignoreUpdate attribute on non-
                                                                                acmCode and acmLoop elements.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

""" Compiled: 2017-07-12 14:02:20 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentXMLMD5Generator.py"
import hashlib
from FOperationsDocumentXML import FOperationsDocumentXML
import FOperationsDocumentXMLDOM as opsxmldom
import inspect

class FOperationsDocumentXMLMD5Generator(FOperationsDocumentXML):

    def __init__(self):
        super(FOperationsDocumentXMLMD5Generator, self).__init__()

    def ProcessAcmCode(self, originalXml, originalNode, fObject, sourceRecord):
        for acmCodeNode in originalNode.getElementsByTagName("acmCode"):
            if self.ExcludeTagFromMD5(acmCodeNode, fObject, sourceRecord):
                #remove node
                OneUpParent, TwoUpParent  = opsxmldom.GetAncestors(acmCodeNode)
                if TwoUpParent:
                    TwoUpParent.removeChild(OneUpParent.previousSibling)
                    TwoUpParent.removeChild(OneUpParent)

        return super(FOperationsDocumentXMLMD5Generator, self).ProcessAcmCode(originalXml, originalNode, fObject, sourceRecord)

    def ProcessAcmLoop(self, originalXml, xmlNode, fObject, sourceRecord):
        loops = opsxmldom.FindTopLoops(xmlNode)
        for acmLoopNode in loops:
            if self.ExcludeTagFromMD5(acmLoopNode, fObject, sourceRecord):
                #remove node
                OneUpParent, dummyTwoUpParent  = opsxmldom.GetAncestors(acmLoopNode)
                if OneUpParent:
                    OneUpParent.removeChild(acmLoopNode.previousSibling)
                    OneUpParent.removeChild(acmLoopNode)
        super(FOperationsDocumentXMLMD5Generator, self).ProcessAcmLoop(originalXml, xmlNode, fObject, sourceRecord)

    def ProcessOther(self, templateXML):
        self.RemoveElementsWithIgnoreUpdate(templateXML)
        super(FOperationsDocumentXMLMD5Generator, self).ProcessOther(templateXML)

    def RemoveElementsWithIgnoreUpdate(self, parentNode):
        for node in parentNode.childNodes:
            if node.nodeType != opsxmldom.ATTRIBUTE_TYPE_NODE:
                continue
            if self.ExcludeTagFromMD5(node, None, None):
                parentNode.removeChild(node)
            else:
                self.RemoveElementsWithIgnoreUpdate(node)

    @classmethod
    def GenerateMD5FromTemplate(cls, template, sourceRecord, overrideXML = None):
        if template == None or template == '':
            return ''
        templateXML = cls.GenerateXmlFromTemplateAsString(template, sourceRecord, overrideXML)
        md5Sum = hashlib.md5(templateXML)
        return md5Sum.hexdigest()

    def ExcludeTagFromMD5(self, xmlNode, fObject, sourceRecord):
        includeTag = False
        pyModule = None
        fileAttribute = 'file'
        ignoreUpdateFunctionAttribute = 'ignoreUpdateFunction'
        ignoreUpdateFunctionValue = None
        if xmlNode.hasAttribute('ignoreUpdate'):
            if xmlNode.getAttribute('ignoreUpdate') == 'True':
                return True

        if xmlNode.hasAttribute(fileAttribute):
            pyModule = str(xmlNode.getAttribute(fileAttribute))
        if xmlNode.hasAttribute(ignoreUpdateFunctionAttribute):
            ignoreUpdateFunctionValue = str(xmlNode.getAttribute(ignoreUpdateFunctionAttribute))
            if not pyModule:
                pyModule = opsxmldom.FindFileAttribute(xmlNode)
            if not pyModule:
                errorMsg = "File attribute missing for function %s." % ignoreUpdateFunctionValue
                raise LookupError(errorMsg)
        if ignoreUpdateFunctionValue and pyModule:
            newFile = __import__(pyModule)
            try:
                params = [(), (fObject,), (fObject, sourceRecord)]
                expectedParams = len(inspect.getargspec(eval('newFile' + "." + ignoreUpdateFunctionValue))[0])
                if expectedParams < len(params):
                    return getattr(newFile, ignoreUpdateFunctionValue)(*(params[expectedParams]))
                else:
                    errorMsg = "%s.%s should take maximum 2 arguments. Found %d." % (pyModule, ignoreUpdateFunctionValue, expectedParams)
                    raise TypeError(errorMsg)

            except (NameError, AttributeError) as e:
                errorMsg = "%s.%s, %s" % (pyModule, ignoreUpdateFunctionValue, e.message)
                e.message = errorMsg
                raise
        return includeTag
