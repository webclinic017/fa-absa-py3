""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOFileFormatHook.py"
"""--------------------------------------------------------------------------
MODULE
    FWSOFileFormatHook

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

def ParseXMLReconciliationDocument(fp):
    """Function for parsing reconciliation documents in XML format."""
    from xml.etree import cElementTree as ElementTree
    def CreateItemDictFromXmlNode(node):
        itemDict = dict()
        for child in node:
            key = '' if not child.tag else child.tag.strip()
            value = '' if not child.text else child.text.strip()
            itemDict[key] = value
        return itemDict
    xmlString = fp.read()
    root = ElementTree.fromstring(xmlString)
    for itemNode in root:
        if itemNode.get('id') in (root.tag,):
            continue
        itemDict = CreateItemDictFromXmlNode(itemNode)
        if not itemDict:
            continue
        yield dict((key, value) for key, value in list(itemDict.items()))
