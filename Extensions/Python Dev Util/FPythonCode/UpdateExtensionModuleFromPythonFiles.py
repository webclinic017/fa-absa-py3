import acm
import os
import sys   
import inspect
import linecache

from DevUtilHelpFunctions import SaveToFile

def UpdateExtensionModulePythonCodeFromPythonFiles(path, extensionModuleName, extensionModuleFileName, extensionModuleFilePath) :
        
    linecache.clearcache()
    extModule = acm.GetDefaultContext().GetModule(extensionModuleName)
    
    if extModule == None:
        extModule = acm.FExtensionModule[extensionModuleName]
      
    if extModule == None :    
        extModule = acm.FExtensionModule()
        extModule.Name(extensionModuleName)

    for file in os.listdir(path):
        if file.endswith('.py'):
            pythonModuleName = file[:len(file) - 3]
            
            if pythonModuleName in sys.modules :
                sysModule = sys.modules[pythonModuleName]

                src = 'FObject:' + pythonModuleName + '\n'
                src = src + inspect.getsource(sysModule)

                acm.GetDefaultContext().EditImport(acm.FPythonCode, src, False, extModule)
    
    if not extModule.IsBuiltIn():
        try:
            extModule.Commit()
        except RuntimeError as e:
            raise Exception('Failed to commit Extension Module: ' + extensionModuleName + '. Error: ' + e.message)
    
    if extensionModuleFilePath:
        if not os.path.exists(extensionModuleFilePath):
            os.makedirs(extensionModuleFilePath)

        fileNameAndPath = extensionModuleFilePath + extensionModuleFileName

        fileSuffix = extensionModuleFileName[-3:]
        fileContent = None
        if fileSuffix == 'txt':
            fileContents = extModule.AsString()
        elif fileSuffix == 'xmr':
            fileContents = extModule.AsStringResource()
        else:
            raise Exception('Unknown file type')
        
        SaveToFile(fileNameAndPath, fileContents)
