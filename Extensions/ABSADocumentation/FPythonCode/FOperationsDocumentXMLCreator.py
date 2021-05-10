""" Compiled: 2018-12-05 17:44:23 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentXMLCreator.py"

import acm

from FConfirmationDocXMLSpecifier import ConfirmationDocumentXMLSpecifier
from FConfirmationSwiftXMLSpecifier import ConfirmationSwiftXMLSpecifier


#---------------------------------------------------------------------------
def __XmlToFile(xmlStr, path, fileName):

    filepath = path + fileName
    
    try:
        xmlFile = open(filepath, 'w')
        
        with xmlFile:
            xmlFile.write(xmlStr)
            acm.Log('Wrote file {}'.format(filepath))
        
    except IOError as e:
        
        acm.Log("Could not write XML message to file {}, Error: {}".format(filepath, e))

#---------------------------------------------------------------------------
def SaveXml(xmlStr, path, fileName):

    assert fileName, "No filename for the xml given"
    assert xmlStr, "No xml data to save"
    if len(path):
        __XmlToFile(xmlStr, path, fileName)

#---------------------------------------------------------------------------
def ToXml(xmlSpecifier):

    xmlStr = ''

    if (isinstance(xmlSpecifier, ConfirmationDocumentXMLSpecifier) or
        isinstance(xmlSpecifier, ConfirmationSwiftXMLSpecifier)):

        from FConfirmationXML import FConfirmationXML
        aelConfirmation = xmlSpecifier.GetObject('Confirmation')
        
        if aelConfirmation:
            
            confirmation = acm.FConfirmation[aelConfirmation.seqnbr]
            xmlStr = FConfirmationXML(confirmation).GenerateXmlFromTemplate()
    else:
        
        from FSettlementXML import FSettlementXML
        aelSettlement = xmlSpecifier.GetObject('Settlement')
        
        if aelSettlement:
            
            settlement = acm.FSettlement[aelSettlement.seqnbr]
            xmlStr = FSettlementXML(settlement).GenerateXmlFromTemplate()

    return xmlStr
