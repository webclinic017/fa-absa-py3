""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeRenameModule.py"
from __future__ import print_function
"""
FSettlementUpgradeRenameModule
"""
import acm

class FaelData:
    
    def __init__(self, fael, oldModuleName):
        self.__fael = fael
        self.__oldModuleName = oldModuleName
    def GetFael(self):
        return self.__fael
    def GetOldModuleName(self):
        return self.__oldModuleName

class ModuleRenamer:
    
    def __init__(self, oldModuleNames):
        self.__oldModuleNames = oldModuleNames
        self.__fAelDataList = list()
        for oldModuleName in self.__oldModuleNames:
            fael = acm.FAel[oldModuleName]
            if fael:
                fael.Name('unused_' + oldModuleName)
                self.__fAelDataList.append(FaelData(fael, oldModuleName))
    
    def __CommitFaelModule(self, fAelData):
        fAel = fAelData.GetFael()
        oldModuleName = fAelData.GetOldModuleName()
        try:
            fAel.Commit()
            print('Renamed module %s to %s' % (oldModuleName, fAel.Name()))
        except Exception as error:
            print('Could not rename module %s. Cause: %s' % (oldModuleName, error))
    
    def RenameOldModules(self):
        for fAelData in self.__fAelDataList:
            self.__CommitFaelModule(fAelData)
            

class ExtensionContainer:
    
    def __init__(self, module, oldExtensionNames):
        self.__module = module
        self.__oldExtensionNames = oldExtensionNames
        self.__extensions = module.GetAllExtensions('FPythonCode')
        
    def GetExtensions(self):
        return self.__extensions
    
    def GetModule(self):
        return self.__module
    
    def GetOldExtensionNames(self):
        return self.__oldExtensionNames

class ContextHandler:
    
    def __init__(self, extensionContainer, context):
        self.__extensionContainer = extensionContainer
        self.__context = context
        self.__newModule = acm.FExtensionModule()
        self.__newModule.Name('unused_' + str(self.__extensionContainer.GetModule().Name()))
    
    def MoveExtensions(self):
        for extension in self.__extensionContainer.GetExtensions():
            if str(extension.Name()) in self.__extensionContainer.GetOldExtensionNames():
                try:
                    self.__newModule.AddExtension(extension)
                    self.__newModule.Commit()
                    try:
                        self.__context.AddModule(self.__newModule)
                        self.__context.Commit()
                        try:
                            self.__extensionContainer.GetModule().RemoveExtension(extension)
                            self.__extensionContainer.GetModule().Commit()
                        except Exception as error:
                            print('Could not commit module %s. Cause: %s' % (self.__extensionContainer.GetModule().Name(), error))
                            print('Extension %s not removed from module.' % str(extension.Name()))
                    except Exception as error:
                        print('Could not commit context. Cause: %s' % error)
                        print('Module %s not added to context.' % str(self.__newModule.Name()))
                except Exception as error:
                    print('Could not commit new module. Cause: %s' % error)

class ExtensionRelocator:
    def __init__(self, oldExtensionNames, newContextName):
        self.__oldExtensionNames = oldExtensionNames
        self.__newContextName = newContextName
        self.__standardContext = acm.GetStandardContext()
        self.__modules = self.__GetStandardContextModules()
    
    def __GetStandardContextModules(self):
        modules = list()
        for module in self.__standardContext.Modules():
            if not module.IsBuiltIn():
                modules.append(module)
        return modules
    
    def MoveOldExtensions(self):
        context = acm.FExtensionContext()
        context.Name(self.__newContextName)
        for module in self.__modules:
            extensionContainer = ExtensionContainer(module, self.__oldExtensionNames)
            contextHandler = ContextHandler(extensionContainer, context)
            contextHandler.MoveExtensions()
