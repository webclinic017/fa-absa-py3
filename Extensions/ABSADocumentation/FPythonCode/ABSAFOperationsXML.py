""" Compiled: NONE NONE """

import acm
import xml.dom.minidom
import hashlib
import exceptions

try:
    import FDocumentationParameters as DocParams
except ImportError:
    import FDocumentationParametersTemplate as DocParams

class InvalidTagException(exceptions.Exception):
    def init(self, args = None):
        self.args = args

class InvalidEventException(exceptions.Exception):
    def init(self, args = None):
        self.args = args

class InvalidXMLTemplate(exceptions.Exception):
    def init(self, args = None):
        self.args = args

class ABSAFOperationsXML(object):
    @staticmethod
    def HasChildLoops(node):
        if ABSAFOperationsXML.ToXml(node).find('acmLoop') != -1:
            return True
        else:
            return False

    @staticmethod
    def FindTopLoops(node):
        loops = list()

        for i in node.childNodes:
            if i.attributes and i.hasAttribute('acmLoop'):
                loops.append(i)
            elif ABSAFOperationsXML.HasChildLoops(i):
                loops.append(i)
        return loops

    @staticmethod
    def ExecuteHookOrMethod(xmlNode, fObject, attribute):
        result = None
        try:
            if xmlNode.hasAttribute('method') or xmlNode.hasAttribute('acmLoop'):
                method = acm.FMethodChain(acm.FSymbol(str(xmlNode.getAttribute(attribute))))
                if xmlNode.hasAttribute('file'):
                    newFile = __import__(str(xmlNode.getAttribute('file')))
                    return eval('newFile' + "." + str(method) +"(fObject)")
                else:
                    result = method.Call([fObject])

            elif xmlNode.hasAttribute('eval'):
                evalString = acm.FMethodChain(acm.FSymbol(str(xmlNode.getAttribute('eval'))))
                result = eval('fObject' + "." + str(evalString))
            elif not xmlNode.attributes:
                result = fObject
        except InvalidEventException, e:
            raise InvalidEventException, e
        except Exception, e:
            if fObject != None and xmlNode.hasAttribute(attribute):
                raise InvalidTagException, ", Failed to run: " + str(fObject.ClassName()) + "." + str(xmlNode.getAttribute(attribute)) + '()' + str(e)
            else:
                raise InvalidTagException, ", Failed to run: " + str(e)
        return result

    @staticmethod
    def ExecuteAcmCode(originalNode, fObject, originalXml, onlyForComparison):
        for i in originalNode.getElementsByTagName("acmCode"):
            if onlyForComparison:
                if i.hasAttribute('ignoreUpdate'):
                    if i.getAttribute('ignoreUpdate') == 'True':
                        i.parentNode.replaceChild(originalXml.createTextNode(str('')), i)
                        continue

            data = ABSAFOperationsXML.ExecuteHookOrMethod(i, fObject, 'method')

            if i.hasAttribute('dataFormat') and str(i.getAttribute('dataFormat')) == 'XML':
                x = originalXml.importNode(xml.dom.minidom.parseString(str(data)).firstChild, True)#deep copy
                i.parentNode.replaceChild(x, i)
            else:
                data = str(data)
                data = data.decode( DocParams.xmlEncoding )
                i.parentNode.replaceChild(originalXml.createTextNode(data), i)
        return originalNode

    @staticmethod
    def RemoveNodeByName(node, name):
        for i in node.getElementsByTagName(name):
            if ABSAFOperationsXML.HasChildLoops(i):
                i.parentNode.removeChild(i)

                break

    @staticmethod
    def UpdateXml(originalXml, fObject, xmlNode, onlyForComparison):
        loops = ABSAFOperationsXML.FindTopLoops(xmlNode)
        for i in loops:

            if ABSAFOperationsXML.ExecuteHookOrMethod(i, fObject, 'acmLoop'):
                result = ABSAFOperationsXML.ExecuteHookOrMethod(i, fObject, 'acmLoop')
                if result.IsKindOf(acm.FBusinessObject) or result.IsKindOf(acm.FCommonObject):
                    arrayOfFObjects = [result]
                else:
                    arrayOfFObjects = result.AsArray()

                newLineNode = i.previousSibling.cloneNode(2)
                for j in arrayOfFObjects:
                    nodeClone = i.cloneNode(10)
                    ABSAFOperationsXML.UpdateXml(originalXml, j, nodeClone, onlyForComparison)
                    newNodeClone = ABSAFOperationsXML.ExecuteAcmCode(nodeClone, j,  originalXml, onlyForComparison)

                    if newNodeClone.hasAttribute('acmLoop'):
                        newNodeClone.removeAttribute('acmLoop')
                    if newNodeClone.hasAttribute('file'):
                        newNodeClone.removeAttribute('file')

                    xmlNode.insertBefore(newNodeClone, i)
                ABSAFOperationsXML.RemoveNodeByName(xmlNode, i.nodeName)
            else:
                xmlNode.removeChild(i.nextSibling)
                xmlNode.removeChild(i)


    @staticmethod
    def CreateXMLMiniDom(template):
        return xml.dom.minidom.parseString(template)

    @staticmethod
    def GenerateXmlFromTemplate(template, confirmation):
        from FXMLAttributeFunctions import FXMLAttributeFunctions
        if template == None or template == '':
            return None
        onlyForComparison = False
        templateXML = ABSAFOperationsXML.CreateXMLMiniDom(template)
        ABSAFOperationsXML.UpdateXml(templateXML, confirmation, templateXML.lastChild, onlyForComparison)
        templateXML = ABSAFOperationsXML.ExecuteAcmCode(templateXML.lastChild, confirmation, templateXML, onlyForComparison).parentNode
        af = FXMLAttributeFunctions(templateXML)
        templateXML = af.process_attributes()
        return templateXML

    @staticmethod
    def GenerateXmlFromTemplateAsString(template, confirmation):
        newXML = ABSAFOperationsXML.GenerateXmlFromTemplate(template, confirmation)
        if newXML:
            return ABSAFOperationsXML.ToXml(newXML)
        return ''

    @staticmethod
    def GenerateMD5FromTemplate(template, confirmation):
        if template == None or template == '':
            return ''
        onlyForComparison = True
        templateXML = ABSAFOperationsXML.CreateXMLMiniDom(template)
        ABSAFOperationsXML.UpdateXml(templateXML, confirmation, templateXML.lastChild, onlyForComparison)
        templateXML = ABSAFOperationsXML.ExecuteAcmCode(templateXML.lastChild, confirmation, templateXML, onlyForComparison).parentNode

        md5Sum = hashlib.md5(ABSAFOperationsXML.ToXml(templateXML))
        return md5Sum.hexdigest()

    @staticmethod
    def GenerateMD5FromTemplateAsXMLForDebuging(template, confirmation):
        onlyForComparison = True
        templateXML = ABSAFOperationsXML.CreateXMLMiniDom(template)
        ABSAFOperationsXML.UpdateXml(templateXML, confirmation, templateXML.lastChild, onlyForComparison)
        templateXML = ABSAFOperationsXML.ExecuteAcmCode(templateXML, confirmation, templateXML, onlyForComparison)
        return templateXML

    @staticmethod
    def ToXml(XML):
        if DocParams.xmlEncoding != "ISO-8859-1":
            return XML.toxml('utf8')
        else:
            return XML.toxml('ISO-8859-1')

