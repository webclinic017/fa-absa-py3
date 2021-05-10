'''
===================================================================================================
PURPOSE: This module provides the Templeate Editor functionality.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''

import acm
import FUxCore
import FLogger

import HedgeTemplate
import HedgeConstants
import HedgeValidation

userAccess = HedgeValidation.UserAccess(acm.User())
logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE)


def CreateApplicationInstance():
    return HedgeTemplateEditorApplication()


def ReallyStartApplication(shell, count):
    acm.UX().SessionManager().StartApplication(HedgeConstants.STR_HEDGE_TEMPLATE, None)


def StartApplication(eii):
    shell = eii.ExtensionObject().Shell()
    ReallyStartApplication(shell, 0)


class HedgeTemplateEditorCommandItem(FUxCore.MenuItem):
    def __init_(self):
        pass

    def Invoke(self, cd):
        logger.LOG(cd.Definition().GetName().Text())

    def Applicable(self):
        return True

    def Enabled(self):
        return True

    def Checked(self):
        return False


class HedgeTemplateEditorApplication(FUxCore.LayoutApplication):
    def __init__(self):
        FUxCore.LayoutApplication.__init__(self)
        self.m_template = HedgeTemplate.HedgeTemplate()

    def CreateCommandCB(self):
        return HedgeTemplateEditorCommandItem()

    def HandleRegisterCommands(self, builder):
        # No specific custom commands used - See FUxCore.ConvertCommands
        # itemName,     parent,  path,        tooltiptext, accelerator, mnemonic, callback, default
        commands = [['openSuite', 'View', 'Test Suite', 'Open Suite 1', '', '',
                     self.CreateCommandCB, False]]

        # To be able to use the standard File commands(Open,Save,Save As etc) create an FSet and add
        #       the enumerator values corresponding to the commands desired. Look at the
        #       FUxStandardFileCommands enum for a list of available commands.
        fileCommands = acm.FSet()
        fileCommands.Add('FileNew')
        fileCommands.Add('FileOpen')
        fileCommands.Add('FileSave')
        fileCommands.Add('FileSaveAs')
        fileCommands.Add('FileDelete')
        fileCommands.Add('FileRevert')
        fileCommands.Add('FileExit')

        builder.RegisterCommands(FUxCore.ConvertCommands(commands), fileCommands)

    def HandleStandardFileCommandInvoke(self, commandName):
        if commandName == 'FileNew':
            self.on_file_new()
        if commandName == 'FileOpen':
            self.on_file_open()
        if commandName == 'FileSave':
            self.on_file_save()
        if commandName == 'FileSaveAs':
            self.on_file_save_as()
        if commandName == 'FileDelete':
            self.on_file_delete()
        if commandName == 'FileRevert':
            self.on_file_revert()

    def HandleStandardFileCommandEnabled(self, commandName):
        if commandName == 'FileSave':
            return True  # False
        else:
            return True

    def on_file_new(self):
        self.InitialiseNewTemplate()
        self.UpdateGUI()

    def on_file_open(self):
        selectedObject = acm.UX().Dialogs().SelectObject(self.Shell(),
                                                         'Select Hedge Template',
                                                         'Hedge Templates',
                                                         HedgeTemplate.get_templates(),
                                                         None)
        if selectedObject is not None:
            self.HandleObject(selectedObject)

    def on_file_save(self):
        name = self.m_inputTemplateName.GetData()
        if not name:
            logger.WLOG('No valid name given for template')
            return
        self.m_template.set_id(name)
        self.m_template.SetName(name)
        self.m_template.set_status(self.m_optionTemplateStatus.GetData())
        testsettings = HedgeTemplate.get_test_settings(self)
        self.m_template.set_test_settings(testsettings)
        self.m_template.save()
        self.SetCaption()

    def on_validate_CB(self, shell, obj, arg3, arg4):
        ''' Function to validate name when using "Save As" '''
        if obj in HedgeTemplate.get_templates():
            acm.UX().Dialogs().MessageBoxInformation(shell,
                                                     'A Hedge Template with this'
                                                     ' name already exists.')
            return False
        return True

    def on_file_save_as(self):
        name = acm.UX().Dialogs().SaveObjectAs(self.Shell(),
                                               'Save Hedge Template',
                                               'Hedge Templates',
                                               HedgeTemplate.get_templates(),
                                               None,
                                               self.on_validate_CB,
                                               None)
        if not name:
            logger.WLOG('No valid name given for template')
            return

        self.m_template.set_id(name)
        self.m_template.SetName(name)
        self.m_template.set_status(self.m_optionTemplateStatus.GetData())
        testsettings = HedgeTemplate.get_test_settings(self)
        self.m_template.set_test_settings(testsettings)
        self.m_template.save()
        self.SetCaption()
        self.UpdateGUI()

    def on_file_delete(self):
        self.m_template.delete()
        self.InitialiseNewTemplate()
        self.UpdateGUI()

    def on_file_revert(self):
        if self.m_template.get_id():
            self.HandleObject(self.m_template.get_id())

    def HandleDefaultAction(self, shell, cd):
        pass

    def HandleSetContents(self, contents):
        """Override this method to be able to load application
        specific data. This method is called when opening a workspace.
        """
        pass

    def HandleGetContents(self):
        return self.m_currentObject

    def CanHandleObject(self, obj):
        """Can this application handle the object obj in any way?
        When an object is drag & dopped into the application this method
        is called in order for the system to decide which mouse cursor to show.
        """
        # Should return true if object is FCustomTextObject
        # Calls "HandleObject", which shoudl also be implemented better to deal with FObjects
        return False

    def HandleObject(self, obj):
        # Called when new object is loaded through File > Open
        self.m_template.set_id(obj)
        self.m_template.read()
        HedgeTemplate.set_test_settings(self, self.m_template.get_test_settings())
        self.m_inputTemplateName.SetData(self.m_template.get_id())
        self.m_optionTemplateStatus.SetData(self.m_template.get_status())
        self.UpdateGUI()

    def GetApplicationIcon(self):
        # Find an icon that would resemble somehow "Hedge Accounting Template"
        # Create own icon?
        return 'Options'

    def HandleCreate(self, creationInfo):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('EtchedIn', '')
        b.  BeginHorzBox('None', None)
        b.    AddInput('inputTemplateName', 'Template Name')
        b.  EndBox()
        b.  AddOption('optionTemplateStatus', 'Status')
        HedgeTemplate.CreateLayout(b)
        b.EndBox()

        self.m_myPane = creationInfo.AddPane(b, 'myPane')
        HedgeTemplate.HandleCreate(self, creationInfo, self.m_myPane)

        # Set Controls
        self.m_inputTemplateName = self.m_myPane.GetControl('inputTemplateName')
        self.m_optionTemplateStatus = self.m_myPane.GetControl('optionTemplateStatus')

        # populate
        for status in HedgeTemplate.get_statusses():  # Do not use populate()
            self.m_optionTemplateStatus.AddItem(status)

        self.m_inputTemplateName.Editable(True)
        self.InitialiseNewTemplate()
        self.UpdateGUI()

    def InitialiseNewTemplate(self):
        self.m_template.new()
        HedgeTemplate.set_test_settings_default(self)
        self.m_inputTemplateName.Clear()
        self.m_optionTemplateStatus.SetData('New')

    def UpdateGUI(self):
        testsettings = HedgeTemplate.get_test_settings(self)
        self.m_template.set_test_settings(testsettings)
        HedgeTemplate.on_hedgetemplate_testsetting_change(self, True)
        self.SetCaption()
        self.m_inputTemplateName.SetData(self.m_template.get_id())
        self.m_optionTemplateStatus.SetData(self.m_template.get_status())

    def SetCaption(self):
        if self.m_template:
            self.SetContentCaption(self.m_template.get_id())
        else:
            self.SetContentCaption(None)

    def DoChangeCreateParameters(self, createParams):
        # Essentially use default settings
        createParams.UseSplitter(True)
        createParams.SplitHorizontal(False)
        createParams.LimitMinSize(True)
        createParams.AutoShrink(True)
        createParams.AdjustPanesWhenResizing(True)

    def HandleCreateStatusBar(self, sb):
        # we dont use status bar in our app
        pass


class CreateObject(FUxCore.MenuItem):
    def __init__(self, extObj):
        self.m_extObj = extObj

    def Invoke(self, eii):
        if userAccess.is_hedge_user():
            StartApplication(eii)
        else:
            return None

    def Applicable(self):
        return userAccess.is_hedge_user()

    def Enabled(self):
        return userAccess.is_hedge_user()

    def Checked(self):
        return False


def DisplayCheck(extObj):
    return CreateObject(extObj)
