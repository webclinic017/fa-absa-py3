
"""-----------------------------------------------------------------------
MODULE
    FExtensionValues - Function for getting the extension values.
        
DESCRIPTION
    The extension values are used for setting defaults for 
    import and export directories etc.
    
    Karl Fock 2006
    
-----------------------------------------------------------------------"""

import acm
   
def GetExtValueAsPyObject(class_, extension, globals = globals(), locals = locals()):
    """Fetch an FExtensionValue's value from the default context and return as a Python object.

        The string stored on the extension value is passed through the Python eval function
    `   to return a Python object.
    
    """    
    ext = acm.GetDefaultContext().GetExtension('FExtensionValue', class_, extension)
    
    if ext:
        return eval(ext.Value(), globals, locals)        
    else:
        return None    
    
    
"""
Extension Values:

ExportDirectory         Directory where exported python code files are kept.
BackupDirectory         Directory where backed up python code files are kept.
DBBackupDirectory       Directory where overwritten db modules are kept. I.e AEL Modules.
ImportDirectory         Directory from where to import exported python code files.
DefaultModule           Default module to export.
"""
    
def GetExtensionValue(ext_value_name):
    return GetExtValueAsPyObject('CExtensionManagerAppFrame', ext_value_name)


"""--------------------------------------------------------------------"""
#set extension value

def TrimContent(oldContent, moduleName, extensionName):    
    """ Add "[module_name]CExtensionManagerAppFrame:extension_name" and "¤" to module. """   
    content = "[" + moduleName + "]" + "CExtensionManagerAppFrame:" + extensionName + "\n"
    oldContent = '\'' + oldContent + '\''
    oldContent = oldContent.replace('\\','\\\\');
    content += oldContent
    content += "\n¤"    
    return content


def SetExtensionValue(extensionValueName, newValue):    
    moduleName = acm.GetDefaultContext().EditModule().Name()  #Save extensions in the edit module (user module)
    context = acm.FExtensionContext()                
    context.AddModule(moduleName)        
    extensionModule = acm.FExtensionModule[moduleName]   
    
    content = TrimContent(newValue, moduleName, extensionValueName)
    context.EditImport("FExtensionValue", content) 
    
    extensionModule.Commit()
