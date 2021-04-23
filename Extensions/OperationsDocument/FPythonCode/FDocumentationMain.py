""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/FDocumentationMain.py"

"""----------------------------------------------------------------------------
MODULE
    FDocumentationMain - Module that is executed by the documentation ATS.

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

DEPENDENCY

NOTE
AMBA must be configured to send all confirmation/settlement fields.

----------------------------------------------------------------------------"""
import time
import acm
try:
    import FOperationsATSRoutines
    import FOperationsUtils as Utils
    import FOperationsDocumentService
    from FOperationsDocumentXSLTransformer import XSLTransformer, XSLTransformerException
    import FSwiftParametersMetaDataCheck as MetaDataCheck
    import FOperationsDocumentProcess
    from FOperationsExceptions import ParameterModuleException
except Exception as error:
    print("Failed to import , " + str(error))

import FDocumentationParameters as Params

dbTables = ['CONFIRMATION', 'SETTLEMENT', 'ACKNOWLEDGEMENT']


class FOperationsDocumentEngine(FOperationsATSRoutines.FOperationsATSEngine):

    def __init__(self, name, dbTables, paramsModule, paramsModuleTemplateName):
        self.__confirmationDocumentXSLTransformer = None
        self.__docService = None
        FOperationsATSRoutines.FOperationsATSEngine.__init__(self, name, dbTables, paramsModule, paramsModuleTemplateName)

    def Start(self):
        try:
            MetaDataCheck.run()
            self.InitXSLTransformers()
            self.__docService = FOperationsDocumentService.CreateDocumentService(self.GetParamsModule())
            Utils.LogAlways('Checking connection to Document Service...')
            if (0 == len(self.GetParamsModule().xmlDirectory)):
                logMessage = 'XML file directory is not configured. XML files will not be saved.'
                Utils.LogAlways(logMessage)
            if self.__docService.IsConnected():
                Utils.LogAlways('Connected to Document Service.')
            else:
                Utils.LogAlways('Not connected to Document Service.')

        except FOperationsDocumentService.DocumentServiceException as dse:
            Utils.LogAlways('Could not connect properly to Document Service: %s' % dse)
            raise SystemExit
        except XSLTransformerException as xte:
            Utils.LogAlways('ATS start-up failed: %s' % xte)
            raise SystemExit
        except ParameterModuleException as parametersModuleError:
            Utils.LogAlways('ATS start-up failed: %s' % parametersModuleError)
            raise SystemExit

    def Work(self, msg, obj):
        if obj:
            FOperationsDocumentProcess.DefaultProcessing(obj, self.__confirmationDocumentXSLTransformer, self.__docService)
        else:
            FOperationsDocumentProcess.AckNakProcessing(msg)

    def InitXSLTransformers(self):
        ''' Create XSLTransformer instances. '''
        paramsModule = self.GetParamsModule()
        extension = paramsModule.xslTemplateExtensionForConfirmationDocuments
        directory = paramsModule.xsltDirectoryForConfirmationDocuments
        filenameExtension = paramsModule.xsltFilenameExtensionForConfirmationDocuments
        if extension != '':
            Utils.LogAlways('XSLT for confirmation documents enabled.')
            self.__confirmationDocumentXSLTransformer = XSLTransformer(extension, directory, filenameExtension)
        else:
            Utils.LogAlways('XSLT for confirmation documents disabled.')
            self.__confirmationDocumentXSLTransformer = None

    def Stop(self):
        statusMessage = 'Stop called at %s' % (time.ctime())
        Utils.LogAlways(statusMessage)
        return

    def Status(self):
        return "Documentation ATS status"


    def IsCreateObjectFromAMBAMessage(self, msg):
        '''If the amba message includes ACKNOWLEDGMENT then simulation should not be done.'''
        return msg.mbf_find_object('ACKNOWLEDGMENT') == None

docEngine = FOperationsDocumentEngine('Documentation', dbTables, Params, 'FDocumentationParametersTemplate')
aTSRoutines = FOperationsATSRoutines.FOperationsATSRoutines(docEngine)

#ATS entry points
def start():
    aTSRoutines.Start(acm.TaskParameters().At('taskParameters'))

def work():
    aTSRoutines.Work()

def stop():
    aTSRoutines.Stop()

def status():
    return aTSRoutines.Status()

