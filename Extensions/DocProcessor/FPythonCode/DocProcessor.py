from __future__ import print_function
import acm
import sys
import os
import string
import types
import glob
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders






CC_CHECK_IN = "ci"
CC_CHECK_OUT = "co"
CC_UN_CHECK_OUT = "uncheckout"
CC_UPDATE = "update"

DOCSTRING = "FDocString"
DEFINITION_MODULE = "AEFBase"
XMR_FILE_SUFFIX = ".xmr"

TRANSIENT_TYPE_DUPLICATED = "DUPLICATED"
TRANSIENT_TYPE_STORABLE = "STORABLE"

CONTENT_TYPE_EXTENSION = "EXTENSION"
CONTENT_TYPE_DEFINITION = "DEFINITION"

AEF = acm.FSymbol("aef")
PRIVATE = acm.FSymbol("private")
PUBLIC = acm.FSymbol("public")
WORKING_ON = acm.FSymbol("working on")


class ModuleContent(object):
    'An entity class that represents an content which can be an extension or a definition,\
    and includes a couple of attributes describing the content'
    def __init__(self, content, moduleName, transientType, contentType):
        self.content = content
        self.moduleName = moduleName     
        self.transientType = transientType
        self.contentType = contentType

    def getContentName(self):
        'returns the content name'
        return self.content.DocKey()

    def getContent(self):
        'returns the content itself'
        return self.content

    def getModuleName(self):
        'returns the user module that the content was found'
        return self.moduleName

    def getContentType(self):
        'returns the content type which can be either extension or definition'
        return self.contentType

    def isWorkingOn(self):
        if self.getContentType() == CONTENT_TYPE_EXTENSION and self.getContent().Definition() != None:
            if self.getContent().Definition().IsMember(AEF, WORKING_ON): 
                return True
            else:
                return False 
        else:
            if self.getContentType() == CONTENT_TYPE_DEFINITION and self.getContent() != None and self.getContent().IsMember(AEF, WORKING_ON):
                return True
                
            return False
            
    def __getMemberShip(self):
        if self.getContentType() == CONTENT_TYPE_EXTENSION and self.getContent().Definition() != None:
            if self.getContent().Definition().IsMember(AEF, PRIVATE): 
                return PRIVATE.AsString()
            else:
                return PUBLIC.AsString()
        else:
            return None
            
                
    def __str__(self):
        'the string representation of the object'        
        str =  "******************* CONTENT  ********************\n\n"        
        str += "content = "+self.content.AsString()+"\n"
        str += "module name = " +self.moduleName +"\n"
        str += "transient type = " + self.TransientType +"\n"
        str += "content type = " + self.contentType +"\n"        
        membership = self.__getMemberShip()    
        if membership != None:
            str += "membership = " + membership +"\n"
        if self.isWorkingOn():
            str +="currently being working on."+"\n"
        str += "*************************************************"
        return str
        

    def __getTransientType(self):
        'returns the transient type of the content which canbe duplicated or storable'
        return self.transientType

    def __setTransientType(self, transientType):
        'sets the transient type of the content which canbe duplicated or storable'    
        self.transientType = transientType
    
    TransientType = property(__getTransientType, __setTransientType)



class ModuleWrapper(object):
    'an entity class that represents the xmr module which stores the extensions'    
    def __init__(self, module, fileName):
        self.module = module
        self.fileName = fileName
        self.contents = {}

    def __getOrCreateStorageList(self, content):        
        'creates an entry and store an empty list in the dictionary if there are no matching the contents DocKey (name),\
        otherwise return the list stored in the entry'
        contentList = None                
        if not self.contents.__contains__(content.DocKey()):
            contentList = []
            self.contents[content.DocKey()] = contentList
        else:
            contentList = self.contents[content.DocKey()]                
        return contentList

    def addValue(self, content, moduleName, contentType):        
        'adds an content to the module, if there are other contents with the DocKey (name), the set them both to duplicated'
        storable = True        
        contentList = self.__getOrCreateStorageList(content)        
        for moduleContent in contentList:            
            if moduleContent.getModuleName() != moduleName:
                moduleContent.TransientType = TRANSIENT_TYPE_DUPLICATED
                storable = False
                break
            elif moduleContent.getModuleName() == moduleName and type(moduleContent.getContent()) == type(content):
                print ("**** WARNING  Trying to add an extension or definition from same module serveral time ****")
                print (moduleContent.getContent().DocKey(), type(moduleContent.getContent()), content.DocKey().AsString(), type(content))

        if storable == False:
            contentList.append(ModuleContent(content, moduleName, TRANSIENT_TYPE_DUPLICATED, contentType))
        else:
            contentList.append(ModuleContent(content, moduleName, TRANSIENT_TYPE_STORABLE, contentType))    
        
    def getContents(self,transientType=None,contentName=None):        
        'returns the contents of this object as a list, the parameters are optional, if None given the wildcard are used.'
        tCollection = []        
        if transientType == None and contentName == None:                    
            tCollection.extend(list(flatten(self.contents.values())))                        
            return tCollection
                    
        if contentName == None:
            for content in list(flatten(self.contents.values())):
                if content.TransientType == transientType:
                    tCollection.append(content)            
        
        else:
            if isinstance(contentName, str):
                contentName = acm.FSymbol(contentName)
            if self.contents.__contains__(contentName):            
                contentList = self.contents[contentName]                        
                for content in contentList:
                    if content.TransientType == transientType or transientType == None:
                        tCollection.append(content)

        return tCollection
            

    def getModuleName(self):
        'returns the xmr module name'
        return self.module.Name()
        
    def getFileName(self):
        'returns the file that xmr module should store and load from.'
        return self.fileName

    def getStorableContents(self):
        'an wrapped method to only return storable contents'
        return self.getContents(TRANSIENT_TYPE_STORABLE)


    def __setDefinitionMembership(self, definition):    
        for d in self.module.Definitions():
            if definition.StringKey() == d.StringKey():
                if definition.IsMember(AEF, PRIVATE) and d.IsMember(AEF, PUBLIC) or definition.IsMember(AEF, PUBLIC) and d.IsMember(AEF, PRIVATE):                    
                    if definition.IsMember(AEF, PRIVATE):                        
                        self.module.RemoveMember(d, DOCSTRING, AEF.AsString(), PUBLIC.AsString())
                        self.module.AddMember(definition, DOCSTRING, AEF.AsString(), PRIVATE.AsString())
                    else:
                        self.module.RemoveMember(d, DOCSTRING, AEF.AsString(), PRIVATE.AsString())
                        self.module.AddMember(definition, DOCSTRING, AEF.AsString(), PUBLIC.AsString())                    
                break
    
    def saveToModule(self):        
        for moduleContent in self.getStorableContents():
            if moduleContent.getContentType() == CONTENT_TYPE_EXTENSION and not moduleContent.isWorkingOn():
                self.module.AddExtension(moduleContent.getContent())
            elif moduleContent.getContentType() == CONTENT_TYPE_DEFINITION and not moduleContent.isWorkingOn():                                
                self.__setDefinitionMembership(moduleContent.getContent())
                self.module.AddDefinition(moduleContent.getContent())                

    def AsStringResource(self):
        return self.module.AsStringResource()

    def __str__(self):
        str =  "-------------------- MODULE  --------------------"+"\n"
        str += "Docmodule = "+self.module.Name()+"\n"
        str += "Docmodule file name = "+self.fileName+"\n"    
        for contentList in self.contents.values():
            for moduleContent in contentList:
                str += moduleContent.__str__()+"\n"
        
        str += "-------------------------------------------------"
        return str

    def getModule(self):
        return self.module
    
class ModuleContainer(object):
    
    def __init__(self,moduleFileNames = None):
        self.moduleDictionary = {}
        self.removedExtensions = {}
        self.movedExtension = {}
        if moduleFileNames != None:
            self.importXmrModules(moduleFileNames)
                        
    def importXmrModules(self, modulesFNames):                
        module = None
        self.moduleDictionary.clear()                
        for moduleFileName in modulesFNames:                                
            print ("moduleFileName =>", moduleFileName)
            module = acm.ImportXmr(moduleFileName)                        
            self.moduleDictionary[acm.FSymbol(module.Name())] = ModuleWrapper(module, moduleFileName)
    

    def __getOrCreateRemovedStorageList(self, extensionName):        
        contentList = None                
        if not self.removedExtensions.__contains__(extensionName):
            contentList = []
            self.removedExtensions[extensionName] = contentList
        else:
            contentList = self.removedExtensions[extensionName]                
        return contentList
        
    def addDocToModules(self, userModules):
        for module in userModules:
            for extension in module.GetAllExtensions(DOCSTRING):            
                if self.moduleDictionary.__contains__(extension.DocModule()):
                    self.__cleanOldExtensionResidence(extension)
                    self.moduleDictionary[extension.DocModule()].addValue(extension, module.Name(), CONTENT_TYPE_EXTENSION)                
                    """groups and group items"""
                    if extension.Definition() != None:                                        
                        self.moduleDictionary[acm.FSymbol(DEFINITION_MODULE)].addValue(extension.Definition(), module.Name(), CONTENT_TYPE_DEFINITION)
                else :                                
                    print ("**** WARNING  EXTENSION  =<"+extension.DocKey().AsString()+">"+" IN MODULE =<" +module.Name()+">" +"DOES NOT HAVE A DOCMODULE!!!****")
                    contentList = self.__getOrCreateRemovedStorageList(extension.DocKey())
                    contentList.append(module.Name())
                    
    
        for moduleWrapper in self.moduleDictionary.values():
            moduleWrapper.saveToModule()
            
    def getModuleWrappers(self):
        return self.moduleDictionary.values()
        
    
    def getContents(self,transientType=None,contentName=None):
        clist = []
        mlist = None
        for moduleWrapper in self.getModuleWrappers():
            mlist = moduleWrapper.getContents(transientType, contentName)
            if len(mlist) > 0:
                clist.extend(mlist)
        return clist
            
                
    def getRemovedExtensions(self):
        return self.removedExtensions

    def getMovedExtensions(self):
        return self.movedExtension
        
                  
    def __cleanOldExtensionResidence(self, extension):        
        extensionName = None        
        moduleWrapper = None
        innerDic = None            
        if not self.movedExtension.__contains__(extension.DocKey()):                    
            for key in self.moduleDictionary.keys():
                if key != acm.FSymbol(DEFINITION_MODULE) and key != extension.DocModule():
                    moduleWrapper = self.moduleDictionary[key]
                    if ContainsExtension(moduleWrapper.getModule(), extension):                                        
                        innerDic = {}
                        innerDic[moduleWrapper.getModule().Name()] = extension.DocModule()
                        self.movedExtension[extension.DocKey()] = innerDic                                            
                        extensionName = extension.DocKey().AsString()                        
                        print ("**** WARNING  EXTENSION  =<"+extensionName+">"+" IN MODULE =<" +str(moduleWrapper.getModule().Name())+">" +"HAS BEEN MOVED TO MODULE =<" +str(extension.DocModule())+">!!!****")
                        moduleWrapper.getModule().RemoveExtension(extension)
                        moduleWrapper.getModule().Commit()
                        break                                
            
                        
"""***** UTILITIES FUNCTIONS *****"""
def flatten(nested):
    try:
        for sublist in nested:
            for element in flatten(sublist):
                yield element
    except TypeError:
        yield nested

            
def ContainsExtension(module, extension):
    for ext in module.GetAllExtensions(extension.Class().Name()):
        if ext.Value().StringKey() == extension.StringKey():
            return True
    
    return False
    

def dump(moduleContainer):
    print ("************************************* DUMPING THE CONTENTS OF THE COLLECTED DATA *************************************")
    for moduleWrapper in moduleContainer.getModuleWrappers():
        print (moduleWrapper)

    message =  "____________  ALL REMOVED EXTENSIONS  ___________"+"\n\n"
    for key in moduleContainer.getRemovedExtensions().keys():
        contentList = moduleContainer.getRemovedExtensions()[key]
        message += key.AsString() + "  FROM MODULE(S) :"
        for removedModuleName in contentList:        
            message += removedModuleName+","
        message += "\n"
    
    message += "_________________________________________________" +"\n\n"   
    print (message)
    
    message = "____________  ALL MOVED EXTENSIONS  _____________"+"\n\n"
    for key in moduleContainer.getMovedExtensions().keys():
        moduleAdressDic = moduleContainer.getMovedExtensions()[key]
        message += key.AsString() + "  HAS MOVED FROM :"
        for oldModuleName in moduleAdressDic.keys():        
            message += oldModuleName+" TO " + moduleAdressDic[oldModuleName].AsString()
        message += "\n"
        
    message += "_________________________________________________" +"\n\n"   
                
    print (message)
    
        
def ListAllDocModules():    
    l = []
    cls = acm.FClass.InstancesKindOf()
    for c in cls:
        if c.BaseDomain() == c:
            m = c.DocModule()
            if len(m) == 0:
                print (c.Name())
            if not l.__contains__(m.AsString()+XMR_FILE_SUFFIX):                
                l.append(m.AsString()+XMR_FILE_SUFFIX)                
    
    l.append(DEFINITION_MODULE+XMR_FILE_SUFFIX)
    return l
    
    
def send_mail(send_from, send_to, subject, text, files=[], server="eu-sto-app04.internal.sungard.corp"):    
    assert (type(send_to)==list or type(send_to) == tuple)
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    
    msg.attach( MIMEText(text) )
    
    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file, "rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
    
    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

def CreateEmptyXmr(*modules):    
 
    for module in modules:            
        file = None
        dummyData = "\"#\","+"\n"\
                "\"# Extension module generated by gen_aelimportfile.py\","+"\n"\
                "\"# ClearCase view: build_primefamily_main_windows_release\","+"\n"\
                "\"# Timestamp: 070221 1139\","+"\n"\
                "\"# ***** DO NOT EDIT! *****\","+"\n"\
                "\"#\","+"\n"\
                '\"name        \\"'+module+ '\\"\",\n'
        filePath = os.getcwd()+'\\'+module+".xmr"            
        print (filePath)
        file = open(filePath, "w")
        
        file.write(dummyData)
        
"""***** MAIN FUNCTIONS*****"""

def __accessModulesInCC(modulenames, accessflag):        
    for moduleName in modulenames:                        
        if accessflag == CC_CHECK_IN:
            os.system('cleartool ci -c "NO SPR" ' + moduleName)
        elif accessflag == CC_CHECK_OUT:            
            os.system('cleartool co -nc '+ moduleName)
        elif accessflag == CC_UPDATE:            
            os.system('cleartool update '+ moduleName)
        elif accessflag == CC_UN_CHECK_OUT:
            os.system('cleartool uncheckout -rm ' + moduleName)        
    return modulenames



            
def __getAllUserModules():
    modulesList = []
    for user in acm.FUser.Select(''):        
        extensionModule = acm.FExtensionModule[user.Name()]
        if extensionModule != None:        
            modulesList.append(extensionModule)        
    return modulesList


def __saveModulesToFile(modulesWithContents):
    file = None
    successfulsavings = []
    for moduleWrapper in modulesWithContents:        
        try:
            file = open(moduleWrapper.getFileName(), "w")
            file.write(moduleWrapper.AsStringResource())
            successfulsavings.append(moduleWrapper.getFileName())
        except IOError as msg:
            print ("Error writing to file : "+ moduleWrapper.getFileName())
        finally:
            file.close()
    return successfulsavings


def __postProcess(moduleContainer, mailingList, alwaysSendMail):    
    __calculateStatisticsAndSendMail(moduleContainer, mailingList, alwaysSendMail)        
        

def contentTypeExplanation():
    exp = "content type can be of two kinds, EXTENSION or DEFINITION\n\n"
    exp +="EXTENSION is an normal FExtension object containing a FDocString object that describes a class or a method.\n\n"
    exp +="DEFINITION is an FExtensionDefinition object on a FExtension object that contains information about the group and group item categorization.\n"
    return exp


def transientTypeExplanation():
    exp = "transient type can be of two kinds, STORABLE or DUPLICATED\n\n"
    exp +="STORABLE defines a FExtension object or a FExtensionDefinition that will be stored in the xmr module,\n"
    exp +="only non conflicting objects are able to be stored, which means there are only one documentation describing the object in the whole system.\n\n"
    exp +="DUPLICATED defines a FExtension object or a FExtensionDefinition objet that will not be stored in the xmr module,\n"
    exp +="when there exist serveral documenation describing the same class or method the docstring object containing the description will be tagget as DUPLICATED,\n"
    exp +="the same goes with definitions.\n"
    return exp
    
    

                                    
def __calculateStatisticsAndSendMail(moduleContainer, maillist, alwaysConfirmwithMail):    
    duplications  = moduleContainer.getContents(TRANSIENT_TYPE_DUPLICATED)
    stored = moduleContainer.getContents(TRANSIENT_TYPE_STORABLE)    
    removedDic = moduleContainer.getRemovedExtensions()
    movedDic = moduleContainer.getMovedExtensions()        
    dupcounter = 0
    duplicationstatistics = {}
    message = ""
    subject = "DOCPROCESSOR RESULT"
    
    
    
    message +="_______________ INTERNAL TYPE EXPLANATIONS  _______________\n\n"
    message +=contentTypeExplanation()
    message +="\n"    
    message +="***********************************************************"+"\n"
    message +="\n"    
    message +=transientTypeExplanation()
    message +="___________________________________________________________"+"\n"
    
    if len(stored) > 0:
        message += "_________  ALL STORED DOCUMENTATIONS  ___________"+"\n"        
        for content in stored:                    
            message += content.__str__()+"\n"                        
                                
        message +="__________________________________________________"+"\n\n"
        message += "________  STORED DOCUMENTATION STATISTICS  ______"+"\n\n"
        message += "TOTAL STORED = "+ str(len(stored)) +"\n\n"
        
    if len(duplications) > 0:    
        message += "_______________  ALL DUPLICATIONS  _______________"+"\n"                
        for content in duplications:                    
            message += content.__str__()+"\n"            
            if duplicationstatistics.__contains__(content.getContentName()):
                dupcounter = duplicationstatistics[content.getContentName()]
                dupcounter += 1
                duplicationstatistics[content.getContentName()] = dupcounter
            else:                
                dupcounter = 1
            duplicationstatistics[content.getContentName()] = dupcounter                        
            
                                
        message +="__________________________________________________"+"\n"
        
        message += "____________  DUPLICATION STATISTICS  ___________"+"\n\n"
        message += "TOTAL DUPLICATIONS = "+ str(len(duplications)) +"\n\n"
        for key in duplicationstatistics.keys():
            message +=  key.AsString() +" = "+ str(duplicationstatistics[key]) +"\n"
        
        message += "_________________________________________________"+"\n\n"    
    
    if len(removedDic) > 0:
        message += "__________  ALL DOCUMENTATIONS WITH NO DOCMODULES  _________"+"\n\n"
        for key in removedDic.keys():
            contentList = removedDic[key]
            message += key.AsString() + "  FROM MODULE(S) :"
            for removedModuleName in contentList:        
                message += removedModuleName+","
            message += "\n"
        
        message += "_________________________________________________" +"\n\n"   
            
        
        message += "_  DOCUMENTATIONS WITH NO DOCMODULE STATISTICS  _"+"\n\n"
        message += 'TOTAL "HOMELESS" EXTENSION = '+ str(len(removedDic.keys())) +"\n\n"
        
        message += "_________________________________________________" +"\n\n"   
    
    if len(movedDic) > 0 :    
        message += "_________   ALL MOVED DOCUMENTATIONS  ___________"+"\n\n"
        for key in movedDic.keys():
            moduleAdressDic = movedDic[key]
            message += key.AsString() + "  HAS MOVED FROM :"
            for oldModuleName in moduleAdressDic.keys():        
                message += oldModuleName+" TO " + moduleAdressDic[oldModuleName].AsString()
            message += "\n"
        
        message += "_________________________________________________" +"\n\n"   
        
        message += "_______  MOVED DOCUMENTATIONS STATISTICS  _______"+"\n\n"
        message += "TOTAL MOVED DOCUMENTATION = "+ str(len(movedDic.keys())) +"\n\n"
        message += "_________________________________________________" +"\n\n"   
    
    
    allcount = len(duplications) + len(removedDic) + len(movedDic) + len(stored)
    if allcount > 0:
        send_mail("gary.niemen@sungard.com", maillist, subject, message)
    elif allcount == 0 and (alwaysConfirmwithMail == True or alwaysConfirmwithMail == 'True'):
        send_mail("gary.niemen@sungard.com", maillist, "Docscanner result", __NothingNewText())

def __NothingNewText():
    message = "Server = "+acm.ADSAddress()+"\n"
    message += "NO NEW OR REDUNDANT DOCUMENTATION FOUND"+"\n"
    return message

def __cleanDocModules(storedModuleWrappers, userModules):    
    extensionName = None    
    for module in userModules:        
        for moduleWrapper in storedModuleWrappers:            
            if moduleWrapper.getModuleName() != DEFINITION_MODULE:                    
                for moduleContent in moduleWrapper.getContents(TRANSIENT_TYPE_STORABLE, None):                    
                    if moduleContent.getModuleName() == module.Name():                        
                        extensionName = moduleContent.getContent().Value().StringKey()
                        if not moduleContent.isWorkingOn():                        
                            module.RemoveExtension(moduleContent.getContent())                            
        module.Commit()        



def __addAbsolutePath(moduleNameList, path):
    newList = []
    for moduleName in moduleNameList:
        moduleName = path+"\\"+moduleName
        newList.append(moduleName)
    return newList

def __getStoredAndNonStoredModules(moduleContainer):        
    stored = []
    nonstored = []
    docStoredCount = 0
    docNonStoreCount = 0
    for moduleWrapper in moduleContainer.getModuleWrappers():
        if len(moduleWrapper.getStorableContents()) > 0:
            stored.append(moduleWrapper)            
        else:
            nonstored.append(moduleWrapper)
            
    
    print (str(len(stored)) + " docmodule will be stored.")
    print (str(len(nonstored)) + " docmodule will not be stored.")
    return stored, nonstored
    
def __getFileNames(moduleWrappers):
    fileNames = []
    for moduleWrapper in moduleWrappers:
        fileNames.append(moduleWrapper.getFileName())
    return fileNames
    
def process(maillist=["yijin.zhou@sungard.com"],alwaysConfirmwithMail=False,verboseOutput=False,xmrlocation=None):    
    moduleNames = ListAllDocModules()    
    if xmrlocation != None:
        os.chdir(xmrlocation)
        print ("change directory to ", xmrlocation)
    print ("CURRDIR = ", os.getcwd())
    moduleNames = __addAbsolutePath(moduleNames, xmrlocation)    
    __accessModulesInCC(moduleNames, CC_UPDATE)    
    __accessModulesInCC(moduleNames, CC_CHECK_OUT)    
    moduleContainer = ModuleContainer(moduleNames)         
    modules = __getAllUserModules()    
    moduleContainer.addDocToModules(modules)        
    stored, nonstored = __getStoredAndNonStoredModules(moduleContainer)
    
    storedFileNames = __getFileNames(stored)
    nonstoredFilesNames = __getFileNames(nonstored)
    
    if len(storedFileNames) == len(moduleNames) and len(nonstored) == 0:
        __saveModulesToFile(stored)
        __accessModulesInCC(storedFileNames, CC_CHECK_IN)
    elif len(storedFileNames) == 0 and len(nonstoredFilesNames) == len(moduleNames):
        __accessModulesInCC(nonstoredFilesNames, CC_UN_CHECK_OUT)
    elif len(storedFileNames) < len(moduleNames) and len(storedFileNames) > 0  and len(nonstoredFilesNames) < len(moduleNames) and len(nonstoredFilesNames) > 0:
        __saveModulesToFile(stored)
        __accessModulesInCC(storedFileNames, CC_CHECK_IN)
        __accessModulesInCC(nonstoredFilesNames, CC_UN_CHECK_OUT)
        
    if verboseOutput == True or verboseOutput == 'True':        
        dump(moduleContainer)
    __postProcess(moduleContainer, maillist, alwaysConfirmwithMail)
    if len(stored) > 0 :        
        __cleanDocModules(stored, modules)        
