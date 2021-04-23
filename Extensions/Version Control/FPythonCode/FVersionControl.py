from __future__ import print_function
"""-------------------------------------------------------------------------------------------------------
MODULE
    FVersionControl - Version Control Integration
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This module allows extension modules (FExtensionModules) to be version controlled by
    third party version control systems.
    
    Basically, a directory on the user's hard drive must be configured to contain exported
    extension module files that are stored in a third party version control system. This 
    module makes the hassle of checkout module from version control system, import module 
    into ARENA followed by export module to file, check in file to version control system 
    much easier and more intuitive.

    Menu extensions present users with a list of version control operations. The user
    can choose to check in, out or undo the current module. The code attempts to execute 
    the chosen operation by running the configured version control system's command line 
    commands.
    
    Checks are made of whether a user has a module checked out or in by looking at the 
    associated file's read-only properties.
    
    Additional version control operations may be added.
    
    A detailed description of the functionality and configuration is given in FCA-3585.
    
DEPENDENCIES

    Requires access to the following libraries: acm, ael, os

    Requires access to the FVersionControl Python module.

    The module should be called by the following menu extensions (FMenuExtension):
    
    [Version Control]CExtensionManagerAppFrame:Check In =
      Function=FVersionControl.VCModule
      MenuType=Application
      Operation=Check In
      ParentMenu=Tools/Module Version Control
    
    [Version Control]CExtensionManagerAppFrame:Check Out =
      Function=FVersionControl.VCModule
      MenuType=Application
      Operation=Check Out
      ParentMenu=Tools/Module Version Control
    
    [Version Control]CExtensionManagerAppFrame:Undo Check Out =
      Function=FVersionControl.VCModule
      MenuType=Application
      Operation=Undo Check Out
      ParentMenu=Tools/Module Version Control
    
    To prevent users using this version control module from modifying extension modules
    that they do not have checked out, the following code must be integrated into the existing 
    FValidation AEL hook code:
    
        import ael
        
        VCErrMsg = ""<<-Add another quote here!
        *********************************************************
        * Version Control Error:                                *
        *    Your extension module update has been cancelled.   *
        *    You do not appear to have the module checked out.  *
        *    If you do have the module checked out investigate  *
        *    why the file is reported as read-only.             *
        *                                                       *
        *    If you are not using version control and would     *
        *    like to stop getting this message, remove the      *
        *    module "Version Control" from your context using   * 
        *    the Extension Manager application.                 *
        *                                                       *
        *    See FCA3585 for full documentation.                *
        *                                                       *
        *********************************************************
        ""<<-Add another quote here!
        
        # We only want to do version control checking
        # if the current user is using version control
        # Easy way to check is to try and import 'FVersionControl'
        # which will only work if the module 'Version Control' is in 
        # the current user's context - implying that the 
        # current user must be using version control
        
        def validate_entity(e,op):
            if e.record_type == 'TextObject' \
                and e.type == 'Extension Module' \
                and op in ['Update','Delete']:
                try:
                
                    import FVersionControl
                
                    if not FVersionControl.ValidationCheck(e):
                        
                        raise Exception(VCErrMsg)
        
                except ImportError:
                
                    pass

    
MAJOR REVISIONS
2006-04-26  Russel W    Created
2006-05-08  Russel W    Improved user interface using new ActiveModule() method 
                        on CExtensionManagerAppFrame class.
2006-05-26  Russel W    Added two level of customisation: extension values and hooks.
2006-09-07  Russel W    Added support for xmr format.
2006-09-08  Russel W    Added FileName hook
-------------------------------------------------------------------------------------------------------"""
import acm
import ael
import FVersionControlHooks

# Configurable settings
# Loaded from FVersionControlHooks

# The directory where exported extension modules are kept.
VCDirectory = FVersionControlHooks.GetVCDirectory()

# The file extension of the exported extension module files.
FileExtension = FVersionControlHooks.GetFileExtension()

# The full path of the command to execute to check in an
# extension module to the third party version control system
CheckInCommandPath = FVersionControlHooks.GetCheckInCommandPath()

# A list of additional arguments to send to the check in application
CheckInArguments = FVersionControlHooks.GetCheckInArguments()

# The full path of the command to execute to check out an
# extension module from the third party version control system
CheckOutCommandPath = FVersionControlHooks.GetCheckOutCommandPath()

# A list of additional arguments to send to the check out application
CheckOutArguments = FVersionControlHooks.GetCheckOutArguments()

# The full path of the command to execute to undo the check out of
# an extension module from the third party version control system
UndoCheckOutCommandPath = FVersionControlHooks.GetUndoCheckOutCommandPath()

# A list of additional arguments to send to the undo check out application
UndoCheckOutArguments = FVersionControlHooks.GetUndoCheckOutArguments()

# A list of common arguments to be sent with all commands 
CommonAdditionalArguments = FVersionControlHooks.GetCommonAdditionalArguments()

# End - Configurable settings

class MessageBox:
    """Encapsulates the ACM msgBox function.

    Sample code:
    
    mb = MessageBox()
    mb.Show('Hello World', 'Test message.\nHello', mb.OKCancel_Buttons | mb.Information_Icon | mb.Application_Modal)
    print (mb.Response())
    print (mb.Response() == mb.OK_Clicked)
    """
    
    # Available display option constants
    
    OK_Button = 0x00000000L
    OKCancel_Buttons = 0x00000001L
    AbortRetryIgnore_Buttons = 0x00000002L
    YesNoCancel_Buttons = 0x00000003L
    YesNo_Buttons = 0x00000004L
    RetryCancel_Buttons = 0x00000005L
    
    Error_Icon = 0x00000010L
    Question_Icon = 0x00000020L
    Warning_Icon = 0x00000030L
    Information_Icon = 0x00000040L
   
    Application_Modal = 0x00000000L
    System_Modal = 0x00001000L
    Task_Modal = 0x00002000L
    
    # Clicked button constants
    
    OK_Clicked = 1
    Cancel_Clicked = 2
    Abort_Clicked = 3
    Retry_Clicked = 4
    Ignore_Clicked = 5
    Yes_Clicked = 6
    No_Clicked = 7
    Close_Clicked = 8
   
    def Show(self, title, message, options):
        self.function = acm.GetFunction('msgBox', 3)
        self.result = self.function(title, message, int(options))
        
    def Response(self):
        return self.result
    
def CheckPathStatus(file):
    """Returns supplied path's status.
    
    Returns 
        0 if not found or error
        1 if present
        2 if readable
        3 if writable and readable
    """
    
    try:
    
        import os
        
    except ImportError:
    
        ael.log('Could not import Python os library')
        return 0
    
    try:
    
        if os.access(file, os.R_OK) and os.access(file, os.W_OK):
        
            return 3
    
        elif os.access(file, os.R_OK):
        
            return 2
            
        elif os.access(file, os.F_OK):
        
            return 1
    
        else:
        
            return 0
            
    except IOError:
    
        return 0

def SpawnProcess(cmdpath, arguments):
    """Spawns syncronous new process.
    
    Spawns a new process with a call to os.spawnv().
    arguments is a list of program arguments.
    See Python docs for details.
    
    Sample code:
    
    print (SpawnProcess('c:\\windows\\notepad.exe', ['MyDoc']))
    """
    
    try:
    
        import os
    
    except ImportError:
    
        ael.log('Could not import Python os library')
        return -1 

    # os.spawnv expects the args list to begin with the 
    # command name.
    arguments.insert(0, cmdpath[cmdpath.rfind('\\') + 1:] )
    
    try:
    
        return os.spawnv(os.P_WAIT, cmdpath, arguments)
    
    except OSError:
    
        ael.log('Could not spawn process')
        return -2

def CheckInModule(name):
    """Check in an extension module."""
    
    filename = VCDirectory + name + FileExtension
    fs = CheckPathStatus(filename)
        
    # Is the file read-only?
    if fs == 2:
    
        mb = MessageBox()
        mb.Show('Version Control Error', 'The file ' + filename + ' is not checked out.' \
            + '\nIf this is incorrect investigate why the file ' + filename + ' is read-only.', \
            mb.OK_Button | mb.Error_Icon | mb.Application_Modal)
            
        return 0
    
    elif fs > 2:
    
        # Execute required commands to check in the file to
        # the configured version control system
        args = []
        args = list(CheckInArguments)
        args.extend(CommonAdditionalArguments)
        args.append('"' + filename + '"')

        if not SpawnProcess(CheckInCommandPath, args):

            mb = MessageBox()
            mb.Show('Version Control Success', 'The module ' + name + ' has successfully been checked in.', \
                mb.OK_Button | mb.Information_Icon | mb.Application_Modal)
                
            return 1
        
        else:
        
            mb = MessageBox()
            mb.Show('Version Control Error', 'The module ' + name + ' could not be checked in.' \
                + '\nUnable to automatically determine the problem.', \
                mb.OK_Button | mb.Error_Icon | mb.Application_Modal)            
            
            return 0
    
    
    # Else the file could not be found
    else:
    
        mb = MessageBox()
        mb.Show('Version Control Error', 'The file ' + filename + ' could not be found.' \
            + '\nWould you like to create this file?', \
            mb.YesNo_Buttons | mb.Question_Icon | mb.Application_Modal)
            
        if mb.Response() == mb.Yes_Clicked:
        
            # Create the file
            f = file(filename, 'w')
            
            # Export the module
            mod = acm.FExtensionModule.Select01('name = "%s"' % (name), '')
            f.write(mod.AsString())
            
            f.close()
    
            # Try again
            return CheckInModule(name)
        
        else:
        
            return 0

def CheckOutModule(name):
    """Check out an extension module."""
    
    filename = VCDirectory + name + FileExtension
    fs = CheckPathStatus(filename)
        
    # Does a writable file already exist?
    if fs == 3:
    
        mb = MessageBox()
        mb.Show('Version Control Error', 'The file ' + filename + ' is already checked out.' \
            + '\nIf this is incorrect investigate why the file ' + filename + ' is not read-only.', \
            mb.OK_Button | mb.Error_Icon | mb.Application_Modal)
            
        return 0
    
    # Does a read-only file exist?
    elif fs > 0:

        # Execute required commands to check out the file from
        # the configured version control system
    
        args = []
        args = list(CheckOutArguments)
        args.extend(CommonAdditionalArguments)
        args.append('"' + filename + '"')

        if not SpawnProcess(CheckOutCommandPath, args):

            mb = MessageBox()
            mb.Show('Version Control Success', 'The module ' + name + ' has successfully been checked out.', \
                mb.OK_Button | mb.Information_Icon | mb.Application_Modal)
                
            return 1
        
        else:
        
            mb = MessageBox()
            mb.Show('Version Control Error', 'The module ' + name + ' could not be checked out.' \
                + '\nUnable to automatically determine the problem.', \
                mb.OK_Button | mb.Error_Icon | mb.Application_Modal)            
        
            return 0
    
    # Else the file could not be found
    else:
    
        mb = MessageBox()
        mb.Show('Version Control Error', 'The file ' + filename + ' could not be found.' \
            + '\nWould you like to create this file?', \
            mb.YesNo_Buttons | mb.Question_Icon | mb.Application_Modal)
            
        if mb.Response() == mb.Yes_Clicked:
        
            # Create the file
            f = file(filename, 'w')
            
            # Export the module
            mod = acm.FExtensionModule.Select01('name = "%s"' % (name), '')
            f.write(mod.AsString())
            
            f.close()
            
            mb = MessageBox()
            mb.Show('Version Control Success', 'The module ' + name + ' has successfully been exported to ' + filename + '.'\
                + '\nFile is not yet in your version control system and may need to be added manually.', \
                mb.OK_Button | mb.Information_Icon | mb.Application_Modal)

            return 0

def UndoCheckOutModule(name):
    """Undo the check out of an extension module."""
    
    filename = VCDirectory + name + FileExtension
    fs = CheckPathStatus(filename)

    # Does a writable file exist?
    if fs == 3:

        # Execute required commands to undo the check out of the file 
        # from the configured version control system
    
        args = []
        args = list(UndoCheckOutArguments)
        args.extend(CommonAdditionalArguments)
        args.append('"' + filename + '"')
        
        if not SpawnProcess(UndoCheckOutCommandPath, args):

            mb = MessageBox()
            mb.Show('Version Control Success', 'The module ' + name + '\'s check out has successfully been undone.', \
                mb.OK_Button | mb.Information_Icon | mb.Application_Modal)
                
            return 1
        
        else:
        
            mb = MessageBox()
            mb.Show('Version Control Error', 'The module ' + name + '\'s check out could not be undone.' \
                + '\nUnable to automatically determine the problem.', \
                mb.OK_Button | mb.Error_Icon | mb.Application_Modal)            
        
            return 0
    
    # Does a read-only file exist?
    elif fs > 0:

        mb = MessageBox()
        mb.Show('Version Control Error', 'The module ' + name + ' is not checked out.' \
            + '\nIf this is incorrect investigate why the file ' + filename + ' is not read-only.', \
            mb.OK_Button | mb.Error_Icon | mb.Application_Modal)
            
        return 0
    
    # Else the file could not be found
    else:
    
        mb = MessageBox()
        mb.Show('Version Control Error', 'The file ' + filename + ' could not be found.', \
            mb.OK_Button | mb.Error_Icon | mb.Application_Modal)
        
        return 0    

def CheckVCDirectory():
    """Check if VC directory exists."""
    
    ps = CheckPathStatus(VCDirectory)
    
    if ps > 0:
        
        return 1
        
    else:
    
        mb = MessageBox()
        mb.Show('Version Control Error', 'The configured version control directory ' + VCDirectory + ' could not be found.' \
            + '\nWould you like to create this directory?', \
            mb.YesNo_Buttons | mb.Question_Icon | mb.Application_Modal)
            
        if mb.Response() == mb.Yes_Clicked:
                
            try:
            
                import os           
       
            except ImportError:
            
                ael.log('Could not import Python os library')
                return 0            
            
            try:
                
                os.makedirs(VCDirectory)
                return 1
                
            except:
            
                return 0
                
        else:
        
            return 0

def CheckVCConfig():
    """Validate the version control paths."""
    
    if CheckPathStatus(CheckInCommandPath) > 0 \
        and CheckPathStatus(CheckOutCommandPath) > 0 \
        and CheckPathStatus(UndoCheckOutCommandPath) > 0 \
        and CheckVCDirectory():
            
            return 1
            
    else:

        mb = MessageBox()
        mb.Show('Version Control Configuration Error', 'The configured paths could not be verified.' \
            + '\nCorrect the configuration settings, see FCA3585 for details.', \
            mb.OK_Button | mb.Error_Icon | mb.Application_Modal)        

        return 0

def ValidationCheck(module):
    """Validate change to a db textobject of type Extension Module.
    
    This function is called by the ael FValidation hook every
    time  db textobject of type Extension Module is modified.
    Function must be as fast as possible, although there should
    not too many calls to it. Its not as if we're intercepting price
    or trade updates.
    """
    
    # If file is present and writable it must be checked out,
    # therefore can be modified.
    
    filename = VCDirectory + module.name + FileExtension
    
    if CheckPathStatus(filename) > 2:
    
        return 1
        
    else:
    
        return 0

def cleanup_xmr_text(text):
    """Return a clean string from an xmr string."""

    cleantext = ''

    lines = text.split('\n')
    
    for line in lines:

        cleantext = cleantext + line[1:-2] + '\n'

    cleantext.replace('\\"', '"')
    cleantext.replace("\\'", "'")
    cleantext.replace('\\\\', '\\')

    return cleantext
    
def VCModule(eii):
    """Version control a module."""
           
    if CheckVCConfig():
    
        eo = eii.ExtensionObject()
        ed = eii.Definition()
    
        op = ed.At('Operation').AsString()
        module = eo.ActiveModule()
        modulename = FVersionControlHooks.GetFileName(module)

        if op == 'Check Out':
        
            if CheckOutModule(modulename):
            
                mb = MessageBox()
                mb.Show('Version Control Query', 'Would you like to import the module ' + modulename + '?', \
                    mb.YesNo_Buttons | mb.Question_Icon | mb.Application_Modal)               
            
                if mb.Response() == mb.Yes_Clicked:
                
                    filename = VCDirectory + modulename + FileExtension
                    
                    try:
                        
                        f = file(filename, 'r')                        
                        text = f.read()
                        f.close()
                        
                        if FileExtension == '.xmr':
                        
                            text = cleanup_xmr_text(text)
                            
                        newmod = acm.ImportExtensionModule(text)
                        
                        module.Apply(newmod)
                        module.Commit()
                        
                    except IOError:
                    
                        mb = MessageBox()
                        mb.Show('Version Control Error', 'Unable to open the file '+ filename + '.', \
                            mb.OK_Button | mb.Error_Icon | mb.Application_Modal)                            
                                
        elif op == 'Check In':
    
            mb = MessageBox()
            mb.Show('Version Control Query', 'Would you like to export the module ' + modulename + ' before checking it in?', \
                mb.YesNo_Buttons | mb.Question_Icon | mb.Application_Modal)               
        
            if mb.Response() == mb.Yes_Clicked:
    
                filename = VCDirectory + modulename + FileExtension
                
                try:
                    
                    f = file(filename, 'w')
                    
                    if FileExtension == '.xmr':
                    
                        f.write(module.AsStringResource())
                    
                    else:
                    
                        f.write(module.AsString())
                    
                    f.close()
                                                    
                except IOError:
                
                    mb = MessageBox()
                    mb.Show('Version Control Error', 'Unable to write the file '+ filename + '.', \
                        mb.OK_Button | mb.Error_Icon | mb.Application_Modal)                                        
        
            CheckInModule(modulename)
    
        elif op == 'Undo Check Out':
        
            UndoCheckOutModule(modulename)

        else: # Not a standard operation, need to pass the request on to FVersionControlHooks

            filename = VCDirectory + modulename + FileExtension
            FVersionControlHooks.CustomOperations(filename, op)
