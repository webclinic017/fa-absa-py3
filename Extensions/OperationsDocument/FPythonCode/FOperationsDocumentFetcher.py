""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/scripts/FOperationsDocumentFetcher.py"
"""----------------------------------------------------------------------------
MODULE
    FOperationsDocumentFetcher - used from Prime when retrieving Adaptiv document

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

DEPENDENCY

NOTE

----------------------------------------------------------------------------"""
import FOperationsDocumentService as DocumentMod
import FOperationsUtils as UtilsMod
from tempfile import gettempdir
import os as osMod

def __GetDocumentFormatFromDocumentType(docType):
    docFormat = DocumentMod.DocumentFormat.INVALID
    if docType == 'pdf':
        docFormat = DocumentMod.DocumentFormat.PDF
    elif docType == 'rtf':
        docFormat = DocumentMod.DocumentFormat.RTF
    elif docType == 'txt':
        docFormat = DocumentMod.DocumentFormat.ASCII
    return docFormat

def __GenerateFilepath(document, extension):
    filename = '%d.%s' % (document.GetDocumentId(), extension)
    return osMod.path.join(gettempdir(), filename)

def __SaveDocumentToDisc(document, extension):
    filePath = __GenerateFilepath(document, extension)
    fileMode = ''
    docFile = None
    if document.GetDataType() == DocumentMod.DataType.TEXT:
        fileMode = 'w'
    elif document.GetDataType() == DocumentMod.DataType.BINARY:
        fileMode = 'wb'
    else:
        raise Exception('Could not save document: The file mode is not supported.')

    try:
        docFile = open(filePath, fileMode)
    except IOError as e:
        UtilsMod.LogAlways('Could not open document %d. File already in use? %s' % (document.GetDocumentId(), e))
    if docFile:
        docFile.write(document.GetData())
        docFile.close()
    return filePath

ael_variables = [('document_id', 'Document id', 'int', [], '0', 0),
                 ('document_type', 'Document type (pdf/rtf/txt)', 'string', ["pdf", "rtf", "txt"], 'pdf', 0)]

def ael_main(dictionary):
    ''' ael_main and ael_variables are used for diaplaying a preview of the
    document from the Operations Manager Application. Do not log about path of the
    document because it is not relevant when calling this module from settlement
    or confirmation sheet.'''

    docId = int(dictionary['document_id'])
    docType = dictionary['document_type']
    try:
        import FDocumentationParameters as Params

        docService = DocumentMod.CreateDocumentService(Params)
        docPath = ''
        if docService.IsConnected():
            document = docService.GetDocument(docId, __GetDocumentFormatFromDocumentType(docType))
            docPath = __SaveDocumentToDisc(document, docType)
            #UtilsMod.Log(True, 'Document is saved here: %s' %docPath)
        else:
            UtilsMod.LogAlways('Could not fetch document: No connection to document service.')
        return docPath
    except DocumentMod.DocumentServiceException as e:
        UtilsMod.LogAlways('Could not do fetch document %d: %s' % (docId, e))
