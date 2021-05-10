
"""-----------------------------------------------------------------------
MODULE
    FStartRunScript - Starts the scripts FExportPythonCode and 
    FImportPythonCode
    
DESCRIPTION
    Invoked from the Menu extensions.
    
    Karl Fock 2006
    
-----------------------------------------------------------------------"""

import acm
  
def StartExportScript(eii):                
    #module, context        
    acm.RunModuleWithParameters("FExportPythonCode", acm.GetDefaultContext())    

def StartImportScript(eii):                    
    acm.RunModuleWithParameters("FImportPythonCode", acm.GetDefaultContext())    
