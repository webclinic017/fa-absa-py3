"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FOperationsDocumentXMLDOM

DESCRIPTION
    This module is used to extend the behaviour of the core FOperationsDocumentXMLDOM
    module.

    The following customisations have been done:

    - Addition of the RemoveIgnoreUpdateAttributeFromNodes function.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-08-28      FAOPS-218       Cuen Edwards            Kgomotso Gumbo          Added function to remove ignoreUpdate attributes from 
                                                                                nodes.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

""" Compiled: 2017-07-12 14:02:20 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentXMLDOM.py"
from xml.dom import minidom

ATTRIBUTE_TYPE_NODE = 1
TEXT_NODE = 3
BLANK = ''
XML_ENCODING = None

def CreateXMLMiniDom(templateXML):
    return minidom.parseString(templateXML)

def FindTopLoops(node):
    loops = list()
    for i in node.childNodes:
        if i.attributes and i.hasAttribute('acmLoop'):
            loops.append(i)
        elif HasChildLoops(i):
            loops.append(i)
    return loops

def HasChildLoops(node):
    if ToXml(node).find('acmLoop') != -1:
        return True
    else:
        return False

def DeleteNodes(templateXML, tagName):
    nodesToDelete = list()
    templateXMLSwiftTag = templateXML.getElementsByTagName('SWIFT')[0]
    for aNodeToDelete in GetNodesToDelete(templateXMLSwiftTag, tagName, nodesToDelete):
        aNodeToDelete.parentNode.removeChild(aNodeToDelete.previousSibling)
        aNodeToDelete.parentNode.removeChild(aNodeToDelete)

def GetNodesToDelete(parentNode, tagName, nodesToDelete):
    for aNode in parentNode.childNodes:
        if aNode.nodeType == parentNode.ELEMENT_NODE and \
        (tagName == "*" or aNode.tagName.startswith(tagName)):
            nodesToDelete.append(aNode)
        GetNodesToDelete(aNode, tagName, nodesToDelete)
    return nodesToDelete

def MergeXML(templateXML, overrideXML):

    if templateXML and overrideXML:
        templateXMLSwiftTag = templateXML.getElementsByTagName('SWIFT')[0]
        overrideXMLSwiftTag = overrideXML.getElementsByTagName('SWIFT')[0]

        childNodes = [child for child in overrideXMLSwiftTag.childNodes if child.nodeType != TEXT_NODE]
        for aChildNode in childNodes:
            nodeToBeInserted = None
            nodeToOverride = None

            nodeToBeInserted = overrideXML.importNode(aChildNode, True)
            if aChildNode.nodeName != 'acmDelete':
                nodeToOverride = templateXML.getElementsByTagName(nodeToBeInserted.nodeName)

            if nodeToOverride:
                nodeToOverride = nodeToOverride[0]
                templateXMLSwiftTag.replaceChild(nodeToBeInserted, nodeToOverride)
            else:
                templateXMLSwiftTag.insertBefore(templateXML.createTextNode(str('\n        ')), templateXMLSwiftTag.lastChild)
                templateXMLSwiftTag.insertBefore(nodeToBeInserted, templateXMLSwiftTag.lastChild)
        return templateXML

    elif templateXML:
        return templateXML
    elif overrideXML:
        return overrideXML
    else:
        return None

def InsertFileAttribute(templateXML):
    swiftTag = templateXML.getElementsByTagName('SWIFT')[0]
    if swiftTag.hasAttribute('file'):
        fileName = swiftTag.attributes['file']
    else:
        fileName = BLANK

    for child in swiftTag.childNodes:
        if fileName and not child.nodeType == TEXT_NODE and not child.hasAttribute('file'):
            child.attributes['file'] = fileName

def RemoveFileAttributes(templateXML):
    topNodeName = templateXML.lastChild.tagName
    if topNodeName == 'MESSAGE':
        if templateXML.lastChild.hasAttribute('file'):
            templateXML.lastChild.removeAttribute('file')
    RemoveFileAttributeFromNodes(templateXML.lastChild)

def RemoveFileAttributeFromNodes(parentNode):
    for node in parentNode.childNodes:
        if node.nodeType == ATTRIBUTE_TYPE_NODE:
            if node.hasAttribute('file'):
                node.removeAttribute('file')
        RemoveFileAttributeFromNodes(node)

def RemoveIgnoreUpdateAttributeFromNodes(parentNode):
    for node in parentNode.childNodes:
        if node.nodeType == ATTRIBUTE_TYPE_NODE:
            if node.hasAttribute('ignoreUpdate'):
                node.removeAttribute('ignoreUpdate')
        RemoveIgnoreUpdateAttributeFromNodes(node)

def GetAncestors(node):
    if node.parentNode:
        if node.parentNode.parentNode:
            return node.parentNode, node.parentNode.parentNode
        return node.parentNode, None
    return None, None

def RemoveNodeByName(node, name):
    for i in node.getElementsByTagName(name):
        if HasChildLoops(i):
            i.parentNode.removeChild(i)
            break

def FindFileAttribute(node):

    while node.tagName != 'MESSAGE':
        if node.hasAttribute('file'):
            return str(node.getAttribute('file'))
        node = node.parentNode
    else:
        if node.hasAttribute('file'):
            return str(node.getAttribute('file'))

def RemoveTrailingTextNodes(listOfNodes):

    if not listOfNodes:
        return listOfNodes

    firstNode = listOfNodes[0]
    if firstNode.nodeType == TEXT_NODE:
        listOfNodes = listOfNodes[1:]

    if not listOfNodes:
        return listOfNodes

    lastNode = listOfNodes[-1]
    if lastNode.nodeType == TEXT_NODE:
        listOfNodes = listOfNodes[:-1]

    return listOfNodes

def RemoveSwiftChilds(template):
    templateXML = minidom.parseString(template)
    swiftTag = templateXML.getElementsByTagName('SWIFT')[0]
    childNodes = swiftTag.childNodes[:]
    for child in childNodes:
        swiftTag.removeChild(child)
    return templateXML.toxml()

def SetXMLEncoding(encoding):
    global XML_ENCODING
    XML_ENCODING = encoding

def ToXml(template):
    if template:
        return template.toxml(XML_ENCODING)
    else:
        return None


