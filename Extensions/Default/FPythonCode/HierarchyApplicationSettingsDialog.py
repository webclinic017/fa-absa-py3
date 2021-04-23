from __future__ import print_function
import acm
import FUxCore
import GetShortNameDialog

from HierarchyEditorUtils import Settings
from HierarchyEditorUtils import SettingsKeys
from HierarchyEditorUtils import SettingsFromChoice
from HierarchyEditorUtils import ParameterFromName

def Show(shell, caption):
    customDlg = HierarchyApplicationSettingsDialog()
    customDlg.m_caption = caption

    builder = customDlg.CreateLayout()
    
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )
    
def ShowEditSettingsDialog(shell, caption, settings):
    customDlg = EditSettingsDialog(settings)
    customDlg.m_caption = caption

    builder = customDlg.CreateLayout()
    
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )





class EditSettingsDialog (FUxCore.LayoutDialog):
    def __init__(self, settings):
        self.m_okButton = None
        self.m_settingsList = None
        self.m_boldCheck = None
        self.m_visibleCheck = None
        self.m_colorButton = None
        self.m_currentColor = None
        self.m_settings = settings

    def HandleApply( self ):
        self.m_settings.m_bold = self.m_boldCheck.Checked()
        self.m_settings.m_visible = self.m_visibleCheck.Checked()
        self.m_settings.m_color = self.m_currentColor

        return True

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)
        self.m_okButton = layout.GetControl('ok')
        self.m_boldCheck = layout.GetControl('boldCheck')
        self.m_visibleCheck = layout.GetControl('visibleCheck')
        self.m_colorButton = layout.GetControl('color')

        self.m_colorButton.AddCallback('Activate', self.OnColorButton, None)

        self.m_boldCheck.Checked(self.m_settings.m_bold)
        self.m_visibleCheck.Checked(self.m_settings.m_visible)
        self.m_currentColor = self.m_settings.m_color

        if self.m_settings.m_color:
            self.m_colorButton.SetColor('Background', self.m_settings.m_color)

    def OnColorButton(self, ud, cd) :
        color = acm.UX().Dialogs().ColorPicker(self.m_fuxDlg.Shell(), None)
        self.m_colorButton.SetColor('Background', color)
        self.m_currentColor = color

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddCheckbox('visibleCheck', 'Visible')
        b.  AddCheckbox('boldCheck', 'Bold')
        b.  AddButton('color', 'Color')
        b.  AddSpace(10)
        b.  BeginHorzBox()
        b.      AddFill()
        b.      AddButton('ok', 'OK')
        b.      AddButton('cancel', 'Cancel')
        b.  EndBox()

        b.EndBox()
        return b

    
class HierarchyApplicationSettingsDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_applyToButton = None
        self.m_settingsList = None
        self.m_editButton = None
        self.m_parameter = None
        self.m_extensionModule = acm.GetDefaultContext().EditModule()

    def HandleApply( self ):
        return self.CommitParameters()

    def OnSettingsSelectionChanged(self, ud, cd):
        self.UpdateControls()
        
    def OnEditSettings(self, ud, cd):
        item = self.m_settingsList.GetSelectedItem()
        if item:
            settings = item.GetData()
            if ShowEditSettingsDialog(self.m_fuxDlg.Shell(), 'Edit Settings', settings) :
                self.UpdateItemFromSettings(item, settings)

    def UpdateControls(self) :
        item = self.m_settingsList.GetSelectedItem()
        self.m_editButton.Enabled(item != None) 


    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)
        self.m_applyToButton = layout.GetControl('applyTo')
        self.m_settingsList = layout.GetControl('settingsList')
        self.m_editButton = layout.GetControl('editButton')

        self.m_settingsList.ShowColumnHeaders(True)
        self.m_settingsList.AddColumn('Column Category', 200)
        self.m_settingsList.AddColumn('Visible', 100)
        self.m_settingsList.AddColumn('Bold', 100)
        self.m_settingsList.AddColumn('Color', 100)

        self.m_settingsList.AddCallback('SelectionChanged', self.OnSettingsSelectionChanged, None)
        self.m_settingsList.AddCallback('DefaultAction', self.OnEditSettings, None)
        self.m_editButton.AddCallback('Activate', self.OnEditSettings, None)
        self.m_applyToButton.AddCallback('Activate', self.OnApplyButton, None)

        self.m_parameter = ParameterFromName('HierarchyEditorSettings')

        self.Populate()

        self.UpdateControls()

    def OnApplyToEditModule(self, ud) :
        self.m_extensionModule = acm.GetDefaultContext().EditModule()
        self.m_fuxDlg.CloseDialogOK()

    def OnApplyToCustomModule(self, ud) :
        modules = acm.GetDefaultContext().Modules()

        module = acm.UX().Dialogs().SelectObject(self.m_fuxDlg.Shell(), 'Select Extension Module', 'Extension Module', modules, self.m_extensionModule)

        if module :
            self.m_extensionModule = module
            self.m_fuxDlg.CloseDialogOK()
            

    def OnApplyButton(self, ud, cd ):
        menu = acm.FUxMenu()
        menu.AddItem( self.OnApplyToEditModule, None, 'Edit Module', 'E' )
        menu.AddSeparator()
        menu.AddItem( self.OnApplyToCustomModule, None, 'Custom Module...', 'C' )

        menu.Track(self.m_applyToButton )


    def UpdateItemFromSettings(self, item, settings) :
        item.Label('True' if settings.m_visible else 'False', 1)
        item.Label('True' if settings.m_bold else 'False', 2)
        if settings.m_color :
            item.Style(3, False, settings.m_color.ColorRef(), settings.m_color.ColorRef())

        item.SetData(settings)

    def Populate(self):
        choiceList = acm.FChoiceList.Select('name="Hierarchy Column Category" and list="MASTER"')
        root = self.m_settingsList.GetRootItem()

        if choiceList :
            choiceList = choiceList[0]
            choices = choiceList.ChoicesSorted()
            if choices:
                for choice in choices :
                    child = root.AddChild()
                    child.Label(choice.Name())
                    child.Icon('AdjustJournals', 'AdjustJournals')

                    settings = SettingsFromChoice(choice, self.m_parameter)
                    self.UpdateItemFromSettings(child, settings)
                
    def ColorString(self, color):
        s = ''
        if color :
            colorRef = color.ColorRef()

            r = str(colorRef & 255)
            g = str((colorRef >> 8) & 255)
            b = str((colorRef >> 16) & 255)

            s = 'r' + r + ' ' + 'g' + g + ' ' + 'b' + b

        return s

    def CommitParameters(self) :

        parameter = acm.FParameterGUIDefinition()
        parameter.Name('HierarchyEditorSettings')

        children = self.m_settingsList.GetRootItem().Children()

        for child in children :
            settings = child.GetData()
            name = str(settings.m_choice.Name())

            parameter.AtPut(name + SettingsKeys.Visible, settings.m_visible)
            parameter.AtPut(name + SettingsKeys.Bold, settings.m_bold)

            parameter.AtPut(name + SettingsKeys.Color, self.ColorString(settings.m_color))

        text = 'FObject:' + parameter.AsString()
        acm.GetDefaultContext().EditImport('FParameterGUIDefinition', text, False, self.m_extensionModule)
        
        ret = True
        try :
            self.m_extensionModule.Commit()
        except Exception as e :
            ret = None
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), e.message)
    
        return ret

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddList('settingsList', 10, -1, 100)
        b.  BeginHorzBox()
        b.      AddFill()
        b.      AddButton('editButton', 'Edit..')
        b.  EndBox()
        b.  BeginHorzBox()
        b.      AddFill()
        b.      AddButton('applyTo', 'Save >')
        b.      AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b
