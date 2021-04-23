
import acm
import sys   
import importlib

def RedirectExtensionModulePython(moduleName, extensionModulePath):
    def RedirectModuleToFile(moduleName, fileName) :
        try :
            if not moduleName in sys.modules :
                importlib.import_module(moduleName)
        except Exception as e:
            print ('Failed to import ', moduleName, e)
            pass

        if moduleName in sys.modules :
            module = sys.modules[moduleName]
            module.__file__ = fileName
                       
    extModule = acm.GetDefaultContext().GetModule(moduleName)
        
    if extModule:    
        pythonCodeCollection = extModule.GetAllExtensions('FPythonCode')

        if not extensionModulePath in sys.path:
            sys.path.append(extensionModulePath)  

        if pythonCodeCollection :
            for pythonCode in pythonCodeCollection :
                fileName = extensionModulePath + '\\' + pythonCode.Name() + '.py'            
                RedirectModuleToFile(str(pythonCode.Name()), fileName)                
