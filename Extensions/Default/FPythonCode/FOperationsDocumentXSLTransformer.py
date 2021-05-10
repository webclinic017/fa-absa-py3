""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentXSLTransformer.py"
import acm
import FOperationsUtils as Utils
from FOperationsExceptions import WrapperException

class XSLTransformerException(WrapperException):
    def __init__(self, message, innerException = None):
        super(XSLTransformerException, self).__init__(message, innerException)

class XSLTransformer(object):

    def __init__(self, xslTemplateExtensionName, outputDirectory, outputFilenameExtension):
        Utils.LogAlways('Initializing XSLT...')
        Utils.LogAlways('Name of XSLTemplate extension: %s.' % xslTemplateExtensionName)
        self.__outputDirectory = outputDirectory
        self.__outputFilenameExtension = outputFilenameExtension
        if (self.__outputDirectory != ''):
            Utils.LogAlways('Output of XSLT will be written to directory %s and have filename extension %s' % (self.__outputDirectory, outputFilenameExtension))
        else:
            Utils.LogAlways('Output of XSLT will NOT be written to file.')
        context = acm.GetDefaultContext()
        xslExtension = context.GetExtension("FXSLTemplate", "FObject", xslTemplateExtensionName)
        if (xslExtension == None):
            raise XSLTransformerException('Could not find XSLTemplate extension named %s' % xslTemplateExtensionName)
        xsl = xslExtension.Value()
        self.__xslTransformer = acm.FXSLTTransform(xsl)
        Utils.LogAlways('XSLT initialized.')

    def Transform(self, xml, xmlSpecifier):
        output = self.__Transform(xml)
        Utils.LogVerbose('XML transformed using XSLT.')
        if (self.__outputDirectory != ''):
            filePath = self.__GenerateFilePath(xmlSpecifier)
            XSLTransformer.__WriteToFile(output, filePath)
        return output

    def __Transform(self, xml):
        output = ''
        try:
            output = self.__xslTransformer.Transform(xml)
        except Exception as e:
            raise XSLTransformerException('Failed to transform XML: ', e)
        return output

    def __GenerateFilePath(self, xmlSpecifier):
        filename = xmlSpecifier.GetUniqueFilename('_xslt', self.__outputFilenameExtension)
        filePath = self.__outputDirectory + filename
        return filePath

    @staticmethod
    def __WriteToFile(output, filePath):
        try:
            f = open(filePath, 'w')
            f.write(output)
            f.close()
            Utils.LogVerbose('Wrote the transformed XML to file %s.' % filePath)
        except Exception as e:
            msg = 'Failed to write transformed XML to file ' + filePath + '. Error: ' + str(e)
            raise XSLTransformerException(msg)

