
'''#####################################################################################################
#
#  DESCRIPTION
#  -----------
#  This module can be used to simplify development of Python code.
#       1. CreatePythonFiles
#               - Files (.py) are exported from a named Extension Module
#               - Use this only to create the files, not incrementally when modifying the code
#       2. Redirect
#               - Redirect Prime to use of the created .py files
#               - Use this for every update
#       3. ReloadModules        
#               - Reload all necessary modules
#               - Use this for every update
#       4. UpdateExtensionModuleFromPythonFiles
#               - Update the Extension Module with the changes made in the .py files
#               - Use this once incremental changes are finalized
#
#  EXAMPLE 1 - Working with Extension Modules
#  ------------------------------------------
#       from PythonDevUtil import PythonDevUtil 
#
#       pyFilePath = r'D:\Projects\TEMP'
#
#       extensionModules = ['Extension Module 1', 'Extension Module 2']
#
#       pyDev = PythonDevUtil(extensionModules, pyFilePath)
#
#       pyDev.CreatePythonFiles()
#       pyDev.Redirect()
#       pyDev.ReloadModules()
#       pyDev.UpdateExtensionModuleFromPythonFiles()
#
#
#
#  EXAMPLE 2 - Working with Extension Modules stored on disc (xmr or txt)
#  ----------------------------------------------------------------------
#       from PythonDevUtil import PythonDevUtil 
#       
#       pyFilePath = r'D:\Projects\TEMP'
#       viewPath = r'D:\Projects\MAIN\base\TM_FObject'
#       
#       extensionModules = [('Deal Package Examples', 'DealPackageExamplesModule.xmr'),
#                           ('Deal Package', 'DealPackageModule.xmr')]
#       
#       pyDev = PythonDevUtil(extensionModules, pyFilePath, viewPath, [__name__])
#       
#       pyDev.CreatePythonFiles()
#       pyDev.Redirect()
#       pyDev.ReloadModules()
#       pyDev.UpdateExtensionModuleFromPythonFiles()
#
#####################################################################################################'''
from CreatePythonFilesOnDisk import SaveExtensionModulePythonToFile
from RedirectExtensionModuleToPythonFile import RedirectExtensionModulePython
from UpdateExtensionModuleFromPythonFiles import *
from ReloadDependentModules import ReloadLoadedModulesFromExtensionModule
from DevUtilHelpFunctions import FindFilePath
try:
    basestring
except NameError: #Python3
    basestring = str
    
class PythonDevUtil(object):
    def __init__(self, extensionModuleInfos, pyFilePath, viewPath = None, excludeInReload = []):
        self._extensionModuleTuples = self.__ExtensionModuleTuplesFromInput(extensionModuleInfos)
        self._pyFilePath = self.__PyFilePathFromInput(pyFilePath)
        self._viewPath = self.__ViewPathFromInput(viewPath)
        self._excludeInReload = excludeInReload
        
    def __ExtensionModuleTuplesFromInput(self, extensionModuleInfos):
        extensionModuleTuples = []
        if isinstance(extensionModuleInfos, list):
            for info in extensionModuleInfos:
                if isinstance(info, tuple):
                    extensionModuleTuples.append(info)
                elif isinstance(info, basestring):
                    extensionModuleTuples.append((info, None))
        elif isinstance(extensionModuleInfos, basestring):
            extensionModuleTuples.append((extensionModuleInfos, None))
        else:
            raise Exception('Extension modules should be as string or as list of strings')
        return extensionModuleTuples
    
    def __PyFilePathFromInput(self, pyFilePath):
        if pyFilePath:
            pyFilePath = pyFilePath[:-1] if pyFilePath.endswith('\\') else pyFilePath        
        return pyFilePath
        
    def __ViewPathFromInput(self, viewPath):
        if viewPath:
            viewPath = viewPath[:-1] if viewPath.endswith('\\') else viewPath
        return viewPath
        
    def __GetPyFilePath(self):
        return self._pyFilePath
        
    def __GetViewPath(self):
        return self._viewPath
    
    def __GetExtensionModuleTuples(self):
        return self._extensionModuleTuples
        
    def __GetExtensionModules(self):
        return [extModules[0] for extModules in self.__GetExtensionModuleTuples()]
  
    def __GetExtensionModulePath(self, moduleName):
        return self.__GetPyFilePath() + '\\'  + moduleName
    
    def CreatePythonFiles(self):
        for moduleName in self.__GetExtensionModules():
            SaveExtensionModulePythonToFile(moduleName, self.__GetExtensionModulePath(moduleName))
            
    def Redirect(self):
        for moduleName in self.__GetExtensionModules():
            RedirectExtensionModulePython(moduleName, self.__GetExtensionModulePath(moduleName))

    def ReloadModules(self, printReloadedModules = False):
        ReloadLoadedModulesFromExtensionModule(self.__GetExtensionModules(), printReloadedModules, self._excludeInReload)

    def UpdateExtensionModuleFromPythonFiles(self):
        for extModTuple in self.__GetExtensionModuleTuples():
            extensionModuleName = extModTuple[0]
            extensionModuleFileName = extModTuple[1]
            pyFilePath = self.__GetExtensionModulePath(extensionModuleName)
            extensionModuleFilePath = FindFilePath(self.__GetViewPath(), extensionModuleFileName)
            
            UpdateExtensionModulePythonCodeFromPythonFiles(pyFilePath, extensionModuleName, extensionModuleFileName, extensionModuleFilePath)
