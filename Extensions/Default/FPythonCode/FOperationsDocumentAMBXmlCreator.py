""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentAMBXmlCreator.py"
from FOperationsDocumentXML import FOperationsDocumentXML
from FOperationsDocumentEnums import DocumentFormat


class TagDataHandler:
    def __init__(self, function, args):
        self.__function = function
        self.__args = args

    def GetFunction(self):
        return self.__function

    def GetArguments(self):
        argString = '<?xml version="1.0" encoding="UTF-8"?><ARGUMENTS>\n'
        for argName, argValue in self.__args:
            argString += '  <%s>%s</%s>\n' % (argName, argValue, argName)
        argString += '</ARGUMENTS>'
        return argString

    def GetCreateDocumentArguments(self):
        '''Diffent xml then usual, note CDATA!
            <Request><FUNCTION>CreateDocument</FUNCTION>
               <ARGUMENTS>
               <xmlData><![CDATA[<?xml version="1.0" encoding="UTF-8"?>
               <MESSAGE><SWIFT/></MESSAGE>]]></xmlData>
               </ARGUMENTS>
        </Request>'''

        argString = '<?xml version="1.0" encoding="UTF-8"?>\n<ARGUMENTS>\n'
        for argName, argValue in self.__args:
            argString += '  <%s>\n    <![CDATA[%s]]>\n  </%s>\n' % (argName, argValue, argName)
        argString += '</ARGUMENTS>'
        return argString

class AMBXmlCreator:

    baseXml = '''\
<Request>
    <FUNCTION><acmCode eval = 'GetFunction()'/></FUNCTION>
    <acmCode eval = 'GetArguments()' dataFormat='XML'/>
</Request>
'''
    createDocumentXml = '''\
<Request>
    <FUNCTION><acmCode eval = 'GetFunction()'/></FUNCTION>
    <acmCode eval = 'GetCreateDocumentArguments()' dataFormat='XML'/>
</Request>
'''
    def __init__(self):
        pass

    def GetDocumentXML(self, documentId, documentFormat):
        if documentFormat == DocumentFormat.PDF:
            return self.__GetDocumentAsPDF(documentId)
        elif documentFormat == DocumentFormat.ASCII:
            return self.__GetDocumentAsASCII(documentId)
        elif documentFormat == DocumentFormat.RTF:
            return self.__GetDocumentAsRTF(documentId)
        else:
            return ''

    def __GetDocumentAsPDF(self, documentId):
        return FOperationsDocumentXML.GenerateXmlFromTemplateAsString(AMBXmlCreator.baseXml,
                                                              TagDataHandler('GetDocumentAsPDF',
                                                                             [('DocumentID', documentId)]))

    def __GetDocumentAsASCII(self, documentId):
        return FOperationsDocumentXML.GenerateXmlFromTemplateAsString(AMBXmlCreator.baseXml,
                                                              TagDataHandler('GetDocumentAsASCII',
                                                                             [('DocumentID', documentId)]))
    def __GetDocumentAsRTF(self, documentId):
        return FOperationsDocumentXML.GenerateXmlFromTemplateAsString(AMBXmlCreator.baseXml,
                                                              TagDataHandler('GetDocumentAsRTF',
                                                                             [('DocumentID', documentId)]))

    def SendDocumentByRouterXML(self, documentId, routerName):
        tagDataHandler = TagDataHandler('SendDocumentByRouterName', [('DocumentID', documentId), ('RouterName', routerName)])
        return FOperationsDocumentXML.GenerateXmlFromTemplateAsString(AMBXmlCreator.baseXml, tagDataHandler)

    def GetDocumentInfoXML(self, documentId):
        return FOperationsDocumentXML.GenerateXmlFromTemplateAsString(AMBXmlCreator.baseXml,
                                                              TagDataHandler('ReturnDocumentAttributesByDocId',
                                                                             [('documentId', documentId)]))
    def IsConnectedXML(self):
        return FOperationsDocumentXML.GenerateXmlFromTemplateAsString(AMBXmlCreator.baseXml,
                                                              TagDataHandler('GetConnectionStatus', []))

    def CreateDocumentXML(self, xmlData):
        return FOperationsDocumentXML.GenerateXmlFromTemplateAsString(AMBXmlCreator.createDocumentXml,
                                                              TagDataHandler('CreateDocument',
                                                              [('xmlData', xmlData)]))

    def ReturnDocumentProcessingLogXML(self, documentId):
        return FOperationsDocumentXML.GenerateXmlFromTemplateAsString(AMBXmlCreator.baseXml,
                                                              TagDataHandler('ReturnDocumentProcessingLogXML',
                                                                             [('resultId', documentId)]))