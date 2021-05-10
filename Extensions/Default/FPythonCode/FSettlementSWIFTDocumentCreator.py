""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementSWIFTDocumentCreator.py"
import FOperationsDocumentService as DocumentMod
import FSwiftMessageTypeExtractor as ExtractorMod
import FSettlementSwiftXMLSpecifier
from tempfile import gettempdir
import FOperationsDocumentXMLCreator as XmlCreator
import ael
import acm
import FOperationsUtils as UtilsMod
from FOperationsExceptions import WrapperException
from FSwiftExceptions import SwiftWriterAPIException


ael_variables = [('settlement_oid', 'Settlement Oid', 'int', [], '0', 0)]

def ael_main(dictionary):
    ''' This function is called from FSettlement.cpp (CreateSWIFTDocuments)
    when doing preview of the document from the settlement sheet.'''

    settlement_oid = int(dictionary['settlement_oid'])
    createdDocuments = acm.FArray()

    import FDocumentationParameters as Params
    try:
        docService = DocumentMod.CreateDocumentService(Params)

        rec = ael.Settlement[int(settlement_oid)]
        if not rec:
            UtilsMod.LogVerbose('Could not find Settlement (seqnbr=%s), no document will be fetched' % (str(settlement_oid)))
        else:
            xmlSpecifier = FSettlementSwiftXMLSpecifier.SettlementSwiftXMLSpecifier("", rec)
            if docService.IsConnected():
                mtExtractor = ExtractorMod.FSwiftMessageTypeExtractor(docService)
                xml2 = XmlCreator.ToXml(xmlSpecifier)
                docIds = docService.CreateDocument(xml2)
                xmlDirectory = gettempdir()
                if xmlDirectory[-1] !=  "\\":
                    xmlDirectory = xmlDirectory + "\\"

                xmldata = docService.GetXML(xml2)
                XmlCreator.SaveXml(xmldata, xmlDirectory, xmlSpecifier.GetUniqueFilename())

                for docId in docIds:
                    pair = acm.FPair()
                    pair.First(docId)
                    pair.Second(mtExtractor.Extract(docId))
                    createdDocuments.Add(pair)

            else:
                UtilsMod.LogVerbose('Could not create document: No connection to document service.')
    except (WrapperException, SwiftWriterAPIException) as e:
        UtilsMod.LogAlways('Could not do create document for settlement {}: {}'.format(settlement_oid, e))
        createdDocuments.Clear()
    return createdDocuments

