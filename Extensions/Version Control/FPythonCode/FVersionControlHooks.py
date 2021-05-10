"""-------------------------------------------------------------------------------------------------------
MODULE
    FVersionControlHooks - Version Control Integration Hooks
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This module contains all user customisable functionality for the AEF Extension
    Module Version Control integration solution.

    All the "Get.." functions in this module, other than the utility function "GetExtValueAsPyObject",
    are called from the module "FVersionControl" to obtain user-configurable settings. The default
    implementations of these functions fetches the settings from FExtensionValue extensions.
    
    Returned values can be customised in two ways:
    *   For simple customisation the values contained in the referenced FExtensionValue 
        extensions may be edited to match the desired settings. Module overrides may be
        used to use specific settings on a user or group level.
    *   For more complex customisation the Python functions contained in this module may
        be customised however desired, as long as their return parameters are unchanged.
        Again, module overrides may be used to use specific settings on a user or group level.
        FVersionControl will import the FVersionControlHooks module that is lowest in the user's 
        context.

    A detailed description of the functionality and configuration is given in FCA-3585.

DEPENDENCIES

    Requires access to the following libraries: acm, FVersionControl
    
LIMITATIONS

    Must only be called by the FVersionControl module.
   
MAJOR REVISIONS
2006-05-24  Russel W    Created
2006-09-08  Russel W    Added FileName hook
-------------------------------------------------------------------------------------------------------"""
import acm
import FVersionControl

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
        
def GetVCDirectory():
    """Return the directory where exported extension modules are kept.

    Default implementation fetches values from the 
    FExtensionValue: VCDirectory
    """
    
    return GetExtValueAsPyObject('CExtensionManagerAppFrame', 'VCDirectory')

def GetFileExtension():
    """Return file extension of the exported extension module files.

    Default implementation fetches values from the 
    FExtensionValue: FileExtension
    """
    
    return GetExtValueAsPyObject('CExtensionManagerAppFrame', 'FileExtension')

def GetFileName(module):
    """Return suggested name for the exported extension module files.

    Default implementation simply returns the current module's name.
    """
    
    return module.StringKey()

def GetCheckInCommandPath():
    """Return the full path of the command to execute to check in an
    extension module to the third party version control system.

    Default implementation fetches values from the 
    FExtensionValue: CheckInCommandPath
    """
    
    return GetExtValueAsPyObject('CExtensionManagerAppFrame', 'CheckInCommandPath')

def GetCheckOutCommandPath():
    """Return the full path of the command to execute to check out an
    extension module to the third party version control system.

    Default implementation fetches values from the 
    FExtensionValue: CheckOutCommandPath
    """
    
    return GetExtValueAsPyObject('CExtensionManagerAppFrame', 'CheckOutCommandPath')

def GetUndoCheckOutCommandPath():
    """Return the full path of the command to execute to undo the 
    check out an extension module to the third party version control 
    system.

    Default implementation fetches values from the 
    FExtensionValue: UndoCheckOutCommandPath
    """
    
    return GetExtValueAsPyObject('CExtensionManagerAppFrame', 'UndoCheckOutCommandPath')

def GetCheckInArguments():
    """Return a list of additional arguments to send to the check in application.
    
    Default implementation fetches values from the 
    FExtensionValue: CheckInArguments        
    """
    
    return GetExtValueAsPyObject('CExtensionManagerAppFrame', 'CheckInArguments')

def GetCheckOutArguments():
    """Return a list of additional arguments to send to the check out application.
    
    Default implementation fetches values from the 
    FExtensionValue: CheckOutArguments
    """
    
    return GetExtValueAsPyObject('CExtensionManagerAppFrame', 'CheckOutArguments')

def GetUndoCheckOutArguments():
    """Return a list of additional arguments to send to the undo check out application.
    
    Default implementation fetches values from the 
    FExtensionValue: UndoCheckOutArguments
    """
    
    return GetExtValueAsPyObject('CExtensionManagerAppFrame', 'UndoCheckOutArguments')

def GetCommonAdditionalArguments():
    """Return a list of common additional arguments to send to all application.
    
    Default implementation fetches values from the 
    FExtensionValue: CommonAdditionalArguments
    """
    
    return GetExtValueAsPyObject('CExtensionManagerAppFrame', 'CommonAdditionalArguments')


def CustomOperations(file, operation):
    """Handle custom version control operations.
    
    Default implementation fetches a Python dictionary from the 
    FExtensionValue: CustomOperations
    
    The dictionary specifies the actions to be performed in response
    to custom version control operations. The layout is:
    
    { \
    '<operation1>':(<function>, (tuple of function arguments), \
    '<operation2>':(<function>, (tuple of function arguments), \
    ....
    }
    
    An example extension value for ClearCase's version tree and history is:

    [Version Control]CExtensionManagerAppFrame:CustomOperations
    { \
    'History':(FVersionControl.SpawnProcess, ('C:\\Program Files\\Rational\\ClearCase\\bin\\cleartool.exe', ['lshistory', '-graphical', '"' + file + '"'])), \
    'VersionTree':(FVersionControl.SpawnProcess, ('C:\\Program Files\\Rational\\ClearCase\\bin\\cleartool.exe', ['lsvtree', '-graphical', '"' + file + '"'])) \
    }
    
    """
    
    spec = GetExtValueAsPyObject('CExtensionManagerAppFrame', 'CustomOperations', locals(), globals())
    
    func = spec[operation][0]
    args = spec[operation][1]
    func(*args)
