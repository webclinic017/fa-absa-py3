""" Compiled: 2017-03-16 11:22:18 """

#__src_file__ = "extensions/operations_document/etc/FDocumentationMain.py"

"""------------------------------------------------------------------------------------------
MODULE
    FDocumentationMain - Module that is executed by the documentation ATS.

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

DEPENDENCY

NOTE
AMBA must be configured to send all confirmation/settlement fields.

HISTORY
==============================================================================================
Date           CR number        Developer       Description
----------------------------------------------------------------------------------------------
02/12/2016     CHNG0004142324   Mighty Mkansi   Implementation of singleton functionality for
                                                ATS OPS start ups.
2017                            Willie vd Bank  Updated for 2017 upgrade
--------------------------------------------------------------------------------------------"""
import time
import acm
import singleton
import os
import ast

try:
    import FOperationsATSRoutines
    import FOperationsUtils as Utils
    import FOperationsDocumentService
    from FOperationsDocumentXSLTransformer import XSLTransformer, XSLTransformerException
    import FSwiftParametersMetaDataCheck as MetaDataCheck
    import FOperationsDocumentProcess
    from FOperationsExceptions import ParameterModuleException
except Exception, error:
    print "Failed to import , " + str(error)

try:
    import FDocumentationParameters as Params
except ImportError:
    import FDocumentationParametersTemplate as Params

dbTables = ['CONFIRMATION', 'SETTLEMENT', 'ACKNOWLEDGEMENT']

user_name = acm.UserName()
machineName = os.environ['COMPUTERNAME']
text_name = 'ATS_SINGLETON_%s'%user_name
singleton_instance = acm.FCustomTextObject[str(text_name)]
if singleton_instance:
    singleton_dict = ast.literal_eval(singleton_instance.Text())

process_id = os.getpid()

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

        except FOperationsDocumentService.DocumentServiceException, dse:
            Utils.LogAlways('Could not connect properly to Document Service: %s' % dse)
            raise SystemExit
        except XSLTransformerException, xte:
            Utils.LogAlways('ATS start-up failed: %s' % xte)
            raise SystemExit
        except ParameterModuleException, parametersModuleError:
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
    if singleton_instance is None:        
        aTSRoutines.Start(acm.TaskParameters().At('taskParameters'))
        singleton.lock_singleton()
    else:         
        print 'cannot start the ats for user %s on server %s, service already started by server %s with user %s'%(user_name, machineName, singleton_dict['machine'], singleton_dict['user'] )
        raise SystemExit


def work():
    if not singleton_instance:       
        aTSRoutines.Work()

def stop(): 

    # The ATS which created the singleton object can't read the object from the same process ID
    # We will unlock the singleton from this instance, we will need to chck the 
    # machine/ server name and process ID to unlock the singleton
    
    if not singleton_instance:       
        try:
            print 'removing singleton %s'%text_name
            singleton.unlock_singleton()
        except Exception as e:
            print 'Singleton instance does not exist', e
        
        aTSRoutines.Stop()
    
    elif  machineName == singleton_dict['machine']:
        if user_name == singleton_dict['user']: 
         
            print 'removing singleton %s'%text_name
            singleton.unlock_singleton()
            aTSRoutines.Stop()
        else:
            aTSRoutines.Stop()
    else: 
        aTSRoutines.Stop()
        
    
def status():
    return aTSRoutines.Status()
