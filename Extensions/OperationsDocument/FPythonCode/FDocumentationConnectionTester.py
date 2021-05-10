""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/FDocumentationConnectionTester.py"
#
# FDocumentationConnectionTester - tool for testing connection to the Documentation module
#
#
# Copy this file into some own Python module and comment out parts of the code
# that are numbered with #TEST1, #TEST2, etc
# Run tests in module via Reload (Ctrl+R)

import ael
import FOperationsUtils as Utils

import FOperationsDocumentService
import FSettlementSwiftXMLSpecifier
import FOperationsDocumentXMLCreator as XmlCreator
from tempfile import gettempdir
import FDocumentationParameters as Params

__docService = None

Utils.InitFromParameters(Params)

try:
    Utils.LogAlways('Testing Adaptiv Connection (%s)' % __file__)
    __docService = FOperationsDocumentService.CreateDocumentService(Params)
    Utils.LogAlways('Checking connection to Document Service...')
    # TEST#1
    if __docService.IsConnected():
        Utils.LogAlways('Connected to Document Service.')
    else:
        Utils.LogAlways('Not connected to Document Service.')
    # TEST#2
    '''
    # change seqnbr to match settlement that has column Document equal to 202 or so
    seqnbr = 8062
    xmlSpecifier = FSettlementSwiftXMLSpecifier.SettlementSwiftXMLSpecifier("", ael.Settlement[seqnbr])
    xmlDirectory = gettempdir()
    if xmlDirectory[-1] !=  "\\":
        xmlDirectory = xmlDirectory + "\\"
    xml2 = XmlCreator.ToXml(xmlSpecifier)
    print __docService.CreateDocument(xml2)
    XmlCreator.SaveXml(__docService.GetXML(xml2), xmlDirectory, xmlSpecifier.GetUniqueFilename())
    '''
    # TEST#3
    # note that even better test is to execute FOperationsDocumentFetcher for pdf/txt/rtf
    #__docService.GetDocument(4711, 1) # rtf
    #__docService.GetDocument(4711, 2) # pdf
    #__docService.GetDocument(4711, 3) # ascii

    # TEST#4
    #__docService.GetDocumentInfo(4711)

    # TEST#5
    #__docService.SendDocumentByRouterName(4711, "Network")
    Utils.LogAlways('Test done')

except FOperationsDocumentService.DocumentServiceException as dse:
    Utils.LogAlways('Could not connect to Document service: %s' % dse)
    raise SystemExit
