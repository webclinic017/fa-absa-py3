from __future__ import print_function

"""FUxCore - Base classes for user written UX GUIs

    See AEF Base (FCA 3724) Gui Customisation section for details.
     
(c) Copyright 2011 by Sungard FRONT ARENA. All rights reserved.
   
"""
import acm
import traceback
from functools import wraps

def aux_cb(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        try:
            return f(*args, **kwds)
        except Exception:
            traceback.print_exc()
    return wrapper

class LayoutBase:
    """Abstract base class for all user UX GUIs"""
    
    def HandleDestroy( self):
        """Called when the GUI is about to be destroyed"""
        pass
        
class LayoutApplication(LayoutBase):
    """Base class for user written standalone applications"""
    
    def __init__(self):
        self.m_application = None
    
    def Init(self, uxLayoutCreateContext, application):
        self.m_application = application
        self.HandleCreate(uxLayoutCreateContext)
        
    def SetContentCaption(self, caption):
        """Sets the content caption on the application frame
        """
        if self.m_application:
            self.m_application.SetContentCaption(caption)
            
    def Frame(self):
        """Returns the application's frame window object
        """
        frame = None
        if self.m_application:
            frame = self.m_application.Frame()
            
        return frame
        
    def Shell(self):
        """Returns the application's FUxShell
        """
        shell = None
        if self.m_application:
            shell = self.m_application.Frame().Shell()
            
        return shell
        
    def EnableOnIdleCallback(self, enable):
        """Call this method to enable or disable the calls to HandleOnIdle
        """
        if self.m_application:
            self.m_application.EnableOnIdleCallback(enable)
            
    def AddObjectToMostRecentlyUsedList(self, obj):
        """Call this method to add an object to the recent files list
        """
        if self.m_application:
            self.m_application.AddObjectToMostRecentlyUsedList(obj)
    
    def RebuildCommands(self):
        """Call this method to force a state refresh of the commands
        """
        if self.m_application:
            self.m_application.RebuildCommands()
            
    def ShowPane(self, paneName, show):
        """Call this method to show/hide a pane 
        """
        if self.m_application:
            self.m_application.ShowPane(paneName, show)

    def IsPaneVisible(self, paneName):
        """Call this method to tell if a pane is visible or not
        """
        paneIsVisible = False
        if self.m_application:
            paneIsVisible = self.m_application.IsPaneVisible(paneName)

        return paneIsVisible
    
    def HandleOnIdle(self):
        """Override to do periodical work when ever the application is idle.
        """
        pass
    
    def HandleCreate(self, uxLayoutCreateContext):
        """Construct the entire GUI using uxLayoutCreateContext
        
        See AEF Examples module and FUX_Application for example
        
          
        """
        raise NotImplementedError
    
    def DoChangeCreateParameters(self, uxCreateParameters):
        """Override to be able to modify standard application parameters,
        such as splitters,resizing behaviour etc. This method is called before HandleCreate.
        """
        pass
        
    def DoOverrideApplicationDefaultSize(self):
        """Override to be able to modify the initial size of the application.
        Should return two integer values: width and height.
        Please note that the size will never be smaller than
        the size needed for the controls to fit the application.
        Please note that the AutoShrink must be set to False in the call
        to DoChangeCreateParameters for this to work, otherwise the application
        will be shrunk back directly after resizing it.
        """
        pass
        
    def HandleCreateStatusBar(self, uxStatusBar):
        """Override to create a status bar in the application.
        Use the uxStatusBar to add different types of panes to the
        status bar. Each pane should be populated in HandleCreate.
        """
        pass
        
    def HandleGetContents(self ):
        """Override this method to be able to save application
        specific data. This method is called when saving a workspace.
        """
        return None
        
    def HandleSetContents(self, contents ):
        """Override this method to be able to load application
        specific data. This method is called when opening a workspace.
        """
        pass
        
    def GetCurrentObject(self):
        """Override this method in order to provide the object that is
        being used in the application. For instance, dragging the top left
        corner of an application will call this method to be able to drag & drop
        the current object to another application.
        """
        
        return None
        
    def CanHandleObject(self, obj):
        """Can this application handle the object obj in any way?
        When an object is drag & dopped into the application this method
        is called in order for the system to decide which mouse cursor to show.
        """
        return False
        
    def HandleObject(self, obj):
        """Handle the object obj in an application specific way.
        When an object is drag & dropped into the application this mehod
        is called to make it possible for the application to react on the
        object.
        """
        pass
        
    def HandleRegisterCommands(self, builder):
        """Override this method to be able to create commands, such as application menus.
        The builder object is a FUxCommandBuilder that is used for registering commands
        """
        pass
        
    def HandleStandardFileCommandInvoke(self, commandName):
        """Override this method to be able to react to the user pressing the file menu
        commands, such as Open,Save etc.
        commandName is the name of the command being invoked.
        """
        pass
        
    def HandleStandardFileCommandEnabled(self, commandName):
        """Override this method to be able to set the state of the file commands in the
        such as Open,Save etc.
        commandName is the name of the command to which the states should be applied.
        The method should return True if the command should be enabled and 
        False if it should be disabled
        """
        return True
        
    def HandleClose(self):
        """Override this method to react on the user closing the application
        return True to let the application close.
        """
        return True
    
    def GetApplicationIcon(self):
        """Override this method to provide the icon the application should use.
        Return the name of the icon. Check the FUxBuiltInIcons enum in the AEF Browser for
        a list of icon names
        """
        return "Application"
        
    def HandleCanStoreLayout(self):
        """Override this method to enable/disable layout saving. A small icon will appear in the right corner 
        of your application if this method return True.
        """
        return True
        
    def GetStoredLayoutIdentifier(self):
        '''Overide this method you want to be able to store different layout for different incarnations of your 
        application
        '''
        return ''
        
    def GetContextHelpID(self):
        ''' Override this function to specify a specific help section for the application '''
        return 0

    def HandleSaveLayout(self, contents):
        ''' Override this function to handle the save layout callback '''
        pass

    def HandleLoadLayout(self, contents):
        ''' Override this function to handle the load layout callback '''
        pass    

    def HandleViewTypes(self, viewType):
        ''' Override this function to handle the view types. Use the method AddSubType on the viewType parameter '''
        pass

    def HandleActiveView(self):
        ''' Override this function to return the active view, one that has been added in HandleViewTypes'''
        return None    
        
        
        
        

        
def ConvertCommands(commands):
        """Helper function that converts a static collection of
        command definitions to a format that the FUxCommandBuilder recognize
        """
        
        #Each command contains:
        #The name of the item
        #A parent(such as View,Tools etc). File is not allowed and is handled by registering as described below.
        #The path of the item ending with the item label.
        #A tooltip text, use empty string for no tooltip.
        #The accelerator for the item, use empty string for no accelerator.
        #The mnemonic for the command, use emptu string for no mnemonic.
        #A callback method that creates a FUxCore.MenuItem that is used for invoking the command and for controlling it's appearance.
        #A boolean that specifies if the command should be the default command(only applicable for context menus).
        #All parameters must be supplied when calling ConvertCommands
        #itemName,parent,path,tooltiptext,accelerator,mnemonic,callback,default
        
        convertedCommands = acm.FArray()
        for command in commands:
            
            if len(command) < 8:
                print ("Missing parameters in command")
            
            else:
                convertedCommand = acm.FUxCommandDefinition()
                
                convertedCommand.SetName(command[0])
                convertedCommand.SetParent(command[1])
                convertedCommand.SetCommandPath(command[2])
                convertedCommand.SetTooltip(command[3])
                convertedCommand.SetAccelerator(command[4])
                convertedCommand.SetMnemonic(command[5])
                convertedCommand.SetCreationFunction(command[6])
                convertedCommand.SetDefault(command[7])
                
                convertedCommands.Add(convertedCommand)
        
        return convertedCommands

class LayoutDialog(LayoutBase):
    """Base class for user written standalone dialogs"""
    
    def HandleApply(self):
        """Called when the user selects the default action (ok button)
        
        Return True to allow the GUI to close, False to prevent it
        """
        return True

    def HandleCreate(self, uxLayoutDialog, layout):
        """Construct the entire GUI using uxLayoutDialog and layout objects
        
        See AEF Examples module and AEF Base for examples and details
        
          uxLayoutDialog    An FUxLayoutDialog instance
          layout            An FUxLayout instance
        """
        raise NotImplementedError
        
    def GetFClass(self):
    
        return acm.FUxLayoutDialog
    
    def HandleCancel(self):
        '''Called when the user cancels or closes the dialog with the red cross
        return True to let the dialog close'''
        
        return True

class LayoutTabbedDialog(LayoutBase):
    """Base class for user written standalone dialogs"""
    
    def HandleApply(self):
        """Called when the user selects the default action (ok button)
        
        Return True to allow the GUI to close, False to prevent it
        """
        return True

    def HandleCreate(self, uxLayoutDialog, layout):
        """Construct the entire GUI using uxLayoutDialog and layout objects
        
        See AEF Examples module and AEF Base for examples and details
        
          uxLayoutDialog    An FUxLayoutDialog instance
          layout            An FUxLayout instance
        """
        raise NotImplementedError
        
    def GetFClass(self):
    
        return acm.FUxLayoutTabbedDialog
    
    def HandleCancel(self):
        '''Called when the user cancels or closes the dialog with the red cross
        return True to let the dialog close'''
        
        return True
    
class LayoutPanel(LayoutBase):
    """Base class for dockable GUI panels"""
    
    def Init( self, uxLayoutPanel):
        """Called by UX framework to set reference to m_uxLayoutPanel .
        Should call HandleCreate.
        """
        self.m_uxLayoutPanel = uxLayoutPanel
        self.HandleCreate()

    def GetContents(self):
        """Called by UX framework when saving a workspace to obtain the LayoutPanels contents.
        """
        return None
        
    def InitialContents(self):
        """Retrieve, if any, the initial contents of the LayoutPanel when restoring a workspace 
        """
        return self.m_uxLayoutPanel.InitialContents()
        
    def HandleCreate(self):        
        """Construct the entire GUI using self.uxLayoutPanel"""
        raise NotImplementedError

        
    def Shell(self):
        """Return the FUxShell reference to this instance.
        
        See Shell method on FUxLayoutBuilder for details
        """
        return self.m_uxLayoutPanel.Shell()
        
    def SetLayout(self, builder):
        """See SetLayout method on FUxLayoutBuilder for details"""
        return self.m_uxLayoutPanel.SetLayout(builder)
        
    def Owner(self):
        """Return the application hosting the panel
        
            See Owner method on FUxLayoutBuilder for details
        """
        return self.m_uxLayoutPanel.Owner()
        
    def SetCaption(self, caption) :
        '''Set the caption, if applicable, of the current container
        '''
        
        self.m_uxLayoutPanel.SetCaption(caption)
        
    def EnableOnIdleCallback(self, enable):
        """Call this method to enable or disable the calls to HandleOnIdle
        """
        if self.m_uxLayoutPanel:
            self.m_uxLayoutPanel.EnableOnIdleCallback(enable)
    
    def HandleOnIdle(self):
        """Override to do periodical work when ever the application is idle.
        """
        pass            
            

class MenuItem:
    """Base class for implementation of menu extension behaviour"""
    
    def Invoke(self, eii):
        """Invoke code when menu item has been pressed"""
        raise NotImplementedError
        
    def Applicable(self):
        """Is this menu item applicable for this extension object?
           Return True if applicable otherwise return False. If not applicable
           the menu item will not be shown."""
        
        return True
    
    def Enabled(self):
        """Should the menu item be enabled for this extension object?
           Return True if it should be enabled otherwise return False"""
           
        return True
    
    def Checked(self):
        """Should the menu item be checked for this extension object?
           Return True if it should be checked otherwise return False"""
           
        return False
        
def Separator():
    return ['FUxMenuItemSeparator', '',  '', '', '', '', None, False ]
        
class SubMenu:
    """Base class for implementation of menu extension behaviour"""
    
    def Invoke(self, eii):
        """Return the FUxMenu that will be shown in this submenu"""
        raise NotImplementedError
        
    def Applicable(self):
        """Is this menu item applicable for this extension object?
           Return True if applicable otherwise return False. If not applicable
           the menu item will not be shown."""
        
        return True
    
    def Enabled(self):
        """Should the menu item be enabled for this extension object?
           Return True if it should be enabled otherwise return False"""
           
        return True
    
class HostedLayoutApplicationBase(LayoutBase):
    """Base class for user written standalone applications"""
    
    def __init__(self):
        self.m_application = None
    
    def Init(self, uxLayoutCreateContext, application):
        self.m_application = application
        self.HandleCreate(uxLayoutCreateContext)
            
    def Shell(self):
        """Returns the application's FUxShell
        """
        shell = None
        if self.m_application:
            shell = self.m_application.Shell()
            
        return shell

    def EnableOnIdleCallback(self, enable):
        """Call this method to enable or disable the calls to HandleOnIdle
        """
        if self.m_application:
            self.m_application.EnableOnIdleCallback(enable)

    def ShowPane(self, paneName, show):
        """Call this method to show/hide a pane 
        """
        if self.m_application:
            self.m_application.ShowPane(paneName, show)

    def IsPaneVisible(self, paneName):
        """Call this method to tell if a pane is visible or not
        """
        paneIsVisible = False
        if self.m_application:
            paneIsVisible = self.m_application.IsPaneVisible(paneName)

        return paneIsVisible
    
    def HandleOnIdle(self):
        """Override to do periodical work when ever the application is idle.
        """
        pass
    
    def HandleCreate(self, uxLayoutCreateContext):
        """Construct the entire GUI using uxLayoutCreateContext
        
        """
        raise NotImplementedError

    def HandleHasChanged(self) :
        return True

    def GetContextHelpID(self):
        ''' Override this function to specify a specific help section for the application '''
        return 0

    def HandleViewTypes(self, viewType):
        ''' Override this function to handle the view types. Use the method AddSubType on the viewType parameter '''
        return None

    def HandleActiveView(self):
        ''' Override this function to return the active view, one that has been added in HandleViewTypes'''
        return None    


class HostedLayoutApplication(HostedLayoutApplicationBase):
    def __init__(self):
        HostedLayoutApplicationBase.__init__(self)

    def HandleClose(self):
        """Override this method to react on the user closing the application
        return True to let the application close.
        """
        return True
    
    def HandleCommitChanges(self) :
        """Called by the framework when save is called from the host application. 
        """
        return True             
        
class HostedObjectLayoutApplication(HostedLayoutApplicationBase):
    def __init__(self):
        HostedLayoutApplicationBase.__init__(self)
        
    def HandleObject(self, obj):
        """Handle the object obj of the type specified by the HostObjectType attribute 
        in FCustomApplicationDefinition.
        
        """
        pass
        
    def HandleApplyChanges(self) :
        """Called by the framework when save is called from the host application. Note that the
        framework does the commit on the current object so it should NOT be done by the 
        HostedObjectLayoutApplication
        """
        return True        

    def HandlePostApplyChanges(self, obj):
        """Called by the framework after HandleApplyChanges (if HandleApplyChanges returned True).
        
        """
        return True
