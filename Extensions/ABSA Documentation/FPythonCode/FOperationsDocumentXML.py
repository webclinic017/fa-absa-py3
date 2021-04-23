"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FOperationsDocumentXML

DESCRIPTION
    This module is used to extend the behaviour of the core FOperationsDocumentXML
    module.

    The following customisations have been done:

    - Addition of the FOperationsDocumentXML.ProcessOther method to perform removal of 
      ignoreUpdate attributes from non-acmCode and acmLoop elements.
    - Integration of OperationsDocumentXML.ProcessOther at the end of OperationsDocumentXML.
      GenerateXml (after all core behaviour has run so as not to interfere with existing 
      behaviour).

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

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentXML.py"
import acm
import inspect
import FOperationsDocumentXMLDOM as opsxmldom
from FSwiftUtils import SwiftTrans
TEXT_NODE = 3

try:
    import FDocumentationParameters as DocParams
except ImportError:
    import FDocumentationParametersTemplate as DocParams

class FOperationsDocumentXML(object):

    def __init__(self):
        opsxmldom.SetXMLEncoding(DocParams.xmlEncoding)

    def ExecuteAcmCode(self, xmlNode, fObject, sourceRecord):
        if not filter(xmlNode.hasAttribute, ['method', 'function', 'acmLoop', 'eval']):
            return fObject

        if xmlNode.hasAttribute('eval'):
            evalString = acm.FMethodChain(acm.FSymbol(str(xmlNode.getAttribute('eval'))))
            return eval('fObject' + "." + str(evalString))
        else:
            pyModule = None
            attribute = None

            if xmlNode.hasAttribute('file'):
                pyModule = str(xmlNode.getAttribute('file'))

            if xmlNode.hasAttribute('method'):
                attribute = 'method'
            elif xmlNode.hasAttribute('acmLoop'):
                attribute = 'acmLoop'
            elif xmlNode.hasAttribute('function'):
                attribute = 'function'
                if not pyModule:
                    pyModule = opsxmldom.FindFileAttribute(xmlNode)
                if not pyModule:
                    raise LookupError("File attribute missing for function " + str(xmlNode.getAttribute(attribute)))


            functionOrMethod = acm.FMethodChain(acm.FSymbol(str(xmlNode.getAttribute(attribute))))
            if attribute == 'method':
                return functionOrMethod.Call([fObject])

            if attribute == 'acmLoop' and not pyModule:
                return functionOrMethod.Call([fObject])

            if pyModule:
                params = [(), (fObject,), (fObject, sourceRecord)]
                newFile = __import__(pyModule)
                try:
                    expectedParams = len(inspect.getargspec(eval('newFile' + "." + str(functionOrMethod)))[0])
                    if expectedParams < len(params):
                        return getattr(newFile, str(functionOrMethod))(*(params[expectedParams]))
                    else:
                        errorMsg = "%s.%s should take maximum 2 arguments. Found %d." % (pyModule, str(functionOrMethod), expectedParams)
                        raise TypeError(errorMsg)
                except (NameError, AttributeError) as e:
                    errorMsg = "%s.%s, " % (pyModule, str(functionOrMethod))
                    e.args = (errorMsg + str(e.args[0]),)
                    raise

    def ProcessAcmCode(self, originalXml, originalNode, fObject, sourceRecord):
        for i in originalNode.getElementsByTagName("acmCode"):

            data = self.ExecuteAcmCode(i, fObject, sourceRecord)

            if data == None:
                OneUpParent, TwoUpParent  = opsxmldom.GetAncestors(i)
                if TwoUpParent and TwoUpParent.tagName == 'SWIFT':
                    TwoUpParent.removeChild(OneUpParent.previousSibling)
                    TwoUpParent.removeChild(OneUpParent)
                    continue

            if i.hasAttribute('dataFormat') and str(i.getAttribute('dataFormat')) == 'XML':

                if "xml version" not in data:
                    data = '<?xml version="1.0" encoding="' + DocParams.defaultCodePage + '"?>' + data

                x = originalXml.importNode(opsxmldom.CreateXMLMiniDom(str(data)).firstChild, True)#deep copy
                i.parentNode.replaceChild(x, i)
            else:
                data = str(data)
                data = data.decode( DocParams.defaultCodePage )
                i.parentNode.replaceChild(originalXml.createTextNode(data), i)

        self.ProcessAcmCodeAttributes(originalNode, fObject, sourceRecord)

        return originalNode

    def ProcessAcmCodeAttributes(self, node, fObject, sourceRecord):
        if node.attributes:
            for aItem in node.attributes.items():
                if "acmCode" in str(aItem[1]):
                    nodeXML = opsxmldom.CreateXMLMiniDom("<" + aItem[1] +">")
                    data = self.ExecuteAcmCode(nodeXML.lastChild, fObject, sourceRecord)
                    node.setAttribute(aItem[0], str(data))

    def ProcessAcmLoop(self, originalXml, xmlNode, fObject, sourceRecord):
        loops = opsxmldom.FindTopLoops(xmlNode)
        for i in loops:
            result = self.ExecuteAcmCode(i, fObject, sourceRecord)
            if result:
                if result.IsKindOf(acm.FBusinessObject) or result.IsKindOf(acm.FCommonObject):
                    arrayOfFObjects = [result]
                else:
                    arrayOfFObjects = result.AsArray()

                for j in arrayOfFObjects:
                    nodeClone = i.cloneNode(10)
                    self.ProcessAcmLoop(originalXml, nodeClone, j, sourceRecord)
                    newNodeClone = self.ProcessAcmCode(originalXml, nodeClone, j, sourceRecord)

                    if newNodeClone.hasAttribute('acmLoop'):
                        newNodeClone.removeAttribute('acmLoop')
                    if newNodeClone.hasAttribute('file'):
                        newNodeClone.removeAttribute('file')
                    if newNodeClone.hasAttribute('ignoreUpdateFunction'):
                        newNodeClone.removeAttribute('ignoreUpdateFunction')

                    xmlNode.insertBefore(newNodeClone, i)
                opsxmldom.RemoveNodeByName(xmlNode, i.nodeName)
            else:
                xmlNode.removeChild(i.nextSibling)
                xmlNode.removeChild(i)

    def ProcessAcmTemplate(self, templateXML, fObject, sourceRecord):
        acmTemplateNodes = templateXML.getElementsByTagName('acmTemplate')
        while acmTemplateNodes:
            for acmTemplateNode in acmTemplateNodes:
                data = self.ExecuteAcmCode(acmTemplateNode, fObject, sourceRecord)
                self.InsertAcmTemplate(data, acmTemplateNode)
            acmTemplateNodes = templateXML.getElementsByTagName('acmTemplate')

    def InsertAcmTemplate(self, data, acmTemplateNode):
        if data:
            if '</SWIFT>' not in data:
                data = '<SWIFT>' + str(data) + '</SWIFT>'

            subTemplate = opsxmldom.CreateXMLMiniDom(data)
            opsxmldom.InsertFileAttribute(subTemplate)

            swiftTag = subTemplate.getElementsByTagName('SWIFT')[0]
            childNodes = opsxmldom.RemoveTrailingTextNodes(swiftTag.childNodes)

            for child in childNodes:
                nodeToBeInserted = subTemplate.importNode(child, True)
                acmTemplateNode.parentNode.insertBefore(nodeToBeInserted, acmTemplateNode)
        else:
            acmTemplateNode.parentNode.removeChild(acmTemplateNode.previousSibling)

        acmTemplateNode.parentNode.removeChild(acmTemplateNode)

    def ProcessAcmInit(self, templateXML, fObject, sourceRecord):
        acmInitNodes = templateXML.getElementsByTagName('acmInit')
        for acmInitNode in acmInitNodes:
            self.ExecuteAcmCode(acmInitNode, fObject, sourceRecord)
            acmInitNode.parentNode.removeChild(acmInitNode.previousSibling)
            acmInitNode.parentNode.removeChild(acmInitNode)

    def ApplyXMLOverride(self, templateXML, overrideXML):
        if overrideXML and len(overrideXML):
            for xml in overrideXML:
                overrideXMLCode = opsxmldom.CreateXMLMiniDom(xml)
                self.ProcessAcmDelete(templateXML, overrideXMLCode)
                templateXML = opsxmldom.MergeXML(templateXML, overrideXMLCode)
        return templateXML

    def ProcessAcmDelete(self, templateXML, overrideXML):
        NodesToDelete = overrideXML.getElementsByTagName('acmDelete')
        for aNodeToDelete in NodesToDelete:
            if aNodeToDelete.hasAttribute('tagName'):
                tagName = aNodeToDelete.getAttribute('tagName')
                opsxmldom.DeleteNodes(templateXML, tagName)
                opsxmldom.DeleteNodes(overrideXML, tagName)

                aNodeToDelete.parentNode.removeChild(aNodeToDelete.previousSibling)
                aNodeToDelete.parentNode.removeChild(aNodeToDelete)

    def ProcessNonSwiftChars(self, templateXML):
        swiftTag = templateXML.getElementsByTagName('SWIFT')
        if not swiftTag:
            return

        swiftTrans = SwiftTrans()

        swiftTag = swiftTag[0]
        childNodes = opsxmldom.RemoveTrailingTextNodes(swiftTag.childNodes)

        for node in childNodes:
            if node.nodeType == TEXT_NODE:
                continue
            if node.hasChildNodes():
                data = node.firstChild.data
                data = swiftTrans.Compute(data)
                node.replaceChild(templateXML.createTextNode(data), node.firstChild)

    def ProcessOther(self, templateXML):
        opsxmldom.RemoveIgnoreUpdateAttributeFromNodes(templateXML)

    def GenerateXml(self, template, sourceRecord, overrideXML = None):
        templateXML = opsxmldom.CreateXMLMiniDom(template)
        self.ProcessAcmTemplate(templateXML, sourceRecord, sourceRecord)
        self.ProcessAcmInit(templateXML, sourceRecord, sourceRecord)

        templateXML = self.ApplyXMLOverride(templateXML, overrideXML)
        self.ProcessAcmLoop(templateXML, templateXML.lastChild, sourceRecord, sourceRecord)

        templateXML = self.ProcessAcmCode(templateXML, templateXML.lastChild, sourceRecord, sourceRecord).parentNode
        self.ProcessNonSwiftChars(templateXML)

        opsxmldom.RemoveFileAttributes(templateXML)
        
        self.ProcessOther(templateXML)
        return templateXML

    @classmethod
    def GenerateXmlFromTemplate(cls, template, sourceRecord, overrideXML = None):
        if template == None or template == '':
            return None
        templateXML = cls().GenerateXml(template, sourceRecord, overrideXML)
        return templateXML

    @classmethod
    def GenerateXmlFromTemplateAsString(cls, template, sourceRecord, overrideXML = None):
        newXML = cls.GenerateXmlFromTemplate(template, sourceRecord, overrideXML)
        if newXML:
            return opsxmldom.ToXml(newXML)
        return ''
