import acm
import os
import sys   

from DevUtilHelpFunctions import SaveToFile

def SaveExtensionModulePythonToFile(moduleName, extensionModulePath, overwrite = True, extModule = None):
    def RemoveFirstAndThreeLastLine(s):
        ind1 = s.find('\n')
        ind2 = len(s)
        for i in range(0, 3):
            ind2 = s.rfind('\n', 0, ind2)
            if ind2 == -1 :
                ind2 = len(s) - 1
                break
            
        return s[ind1+1:ind2]
    
    if not extModule :
        extModule = acm.GetDefaultContext().GetModule(moduleName)
        
    if extModule:    
        pythonCodeCollection = extModule.GetAllExtensions('FPythonCode')

        if pythonCodeCollection :
            if not os.path.exists(extensionModulePath):
                os.makedirs(extensionModulePath)

            if not extensionModulePath in sys.path:
                sys.path.append(extensionModulePath)  
                
            for pythonCode in pythonCodeCollection :
                source = pythonCode.AsString()
                
                source = RemoveFirstAndThreeLastLine(source)
                source = source.replace('´', '\'')
                fileName = extensionModulePath + '/' + pythonCode.Name() + '.py'
                if not os.path.isfile(fileName) or overwrite :
                    SaveToFile(fileName, source)
                
