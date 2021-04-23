""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/AppWorkspaceTools/etc/FAppWorkspaceDesignerPanels.py"
""" Compiled: 2018-06-07 17:06:19 """

#__src_file__ = "extensions/AppWorkspaceTools/etc/FAppWorkspaceDesignerPanels.py"
import acm
import FUxCore
import FAppWorkspaceDesignerControls
import Contracts_AppConfig_Messages_AppWorkspace as AppWorkspace
import Contracts_EditObject_Messages_EditObjectCreate as EditObjectCreate
        
class WorkspaceTabPanel(FUxCore.LayoutPanel):
    __name__ = 'workspaceTab'

    def __init__(self, parent):
        self.parent = parent
        self.nodeData = None
        self._controls = []
        self._bindings = acm.FUxDataBindings()
        self._bindings.AddDependent(self)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        
        self._bindings.AddBinderAndBuildLayoutPart(b, 'viewName', 'Stored View Template:', acm.GetDomain('FHgcStoredViewTemplate'), None, acm.FHgcStoredViewTemplate.Select('user = None'))
        
        b.  AddInput('name', 'Workspace Name:')
        b.  AddInput('caption', 'Caption:')
        b.  AddPopuplist('editableObjectTarget', 'Editor Window Mode:')
        b.  AddInput('marketUniqueIds', 'Enable Markets:')
        b.  BeginVertBox('EtchedIn', 'Index Search')
        b.    AddCheckbox('indexSearchEnabled', 'Enable Index Search')
        b.    AddInput('indexSearchEnvironmentName', 'Calculation Environment')
        b.    BeginVertBox('EtchedIn', 'Action')
        b.      AddPopuplist('indexSearchOpenWithExtensionType', 'Extension Type:', -1, -1, 'Default')
        b.      AddPopuplist('indexSearchOpenWithDefinitionName', 'Definition:', -1, -1, 'Default')
        b.    EndBox()
        b.    AddButton('indexSearchDialogSettings', 'Dialog Settings...')
        b.  EndBox()
        
        b.  BeginHorzBox('None')
        b.    AddInput('iconName', 'Icon:')
        b.    AddButton('icons', 'Select...')
        b.  EndBox()
        
        b.  AddInput('activeTab', 'Active Tab:')
        b.  AddInput('size', 'Size:')
        b.  AddInput('throttlingDelay', 'Throttling Delay:')
        
        b.  AddInput('_label', 'Label:')
        b.  AddInput('whitelist', 'Whitelist:')
        b.  AddInput('blacklist', 'Blacklist:')
        b.  AddInput('parentViewNames', 'Parent View Names:')
        b.  AddInput('columnIndex', 'Column Index:')
        b.  AddInput('height', 'Height:')
        b.  AddInput('columnWidths', 'Column Widths:')
        b.  AddInput('partSizes', 'Relative Part Sizes:')
        
        b.  AddPopuplist('extensionType', 'Extension Type:', -1, -1, 'Default')
        
        b.  AddCheckbox('lazyLoad', 'Lazy Load')
        b.  AddCheckbox('enableExcelRtd', 'Enable Excel Real-Time Copy')
        b.  AddCheckbox('showCheckboxColumn', 'Show Checkbox Column')
        b.  AddCheckbox('showActionMenu', 'Show Action Menu')
        b.  AddCheckbox('isUtilityView', 'Utility View')
        b.  AddCheckbox('selectionControlled', 'Selection Controlled')
        b.  AddButton('dialogSettings', 'Dialog Settings...')
        b.  AddCheckbox('collapsed', 'Collapsed')
        b.  AddCheckbox('stacked', 'Stacked')
        
        b.  BeginVertBox('EtchedIn', 'Open With')
        b.    AddPopuplist('openWithExtensionType', 'Extension Type:', -1, -1, 'Default')
        b.    AddPopuplist('openWithDefinitionName', 'Definition:', -1, -1, 'Default')
        b.  EndBox()
        
        b.  BeginHorzBox('EtchedIn', 'Action Menu Items')
        b.    AddList('actionItems', 6, 6, 60)
        b.    BeginVertBox('None')
        b.      AddButton('addActionItem', 'Add')
        b.      AddButton('removeActionItem', 'Remove')
        b.      AddButton('setDefaultActionItem', 'Set Default')
        b.    EndBox()
        b.  EndBox()
        
        b.  BeginHorzBox('EtchedIn', 'Quick Open', 'quickOpen')
        b.    AddCheckbox('instrument', 'Instrument')
        b.    AddCheckbox('trade', 'Trade')
        b.    AddCheckbox('insPackage', 'Instrument Package')
        b.    AddCheckbox('dealPackage', 'Deal Package')
        b.  EndBox()
        b.EndBox()
        return b
    
    def HideAllControls(self):
        # TODO To avoid flicker, don't hide the controls that 
        # will immediately be shown again. This is too corse-grained. 
        self.name.Visible(False)
        self._icons.Visible(False)
        self._quickOpen.Visible(False)
        self._dialogSettings.Visible(False)
        self._indexSearchDialogSettings.Visible(False)
        for control in self._controls:
            control.Hide()

    def SetupWorkspaceControls(self):
        self.HideAllControls()
        self.name.Visible(True)
        self.PopulateNameField()
        self._editableObjectTarget.Show('settings', 'contents')
        self._marketUniqueIds.Show('settings', 'contents')
        self._indexSearchEnabled.Show('settings.indexSearchSettings', 'contents')
        self._indexSearchEnvironmentName.Show('settings.indexSearchSettings', 'contents')
        self._indexSearchOpenWithExtensionType.Show('settings.indexSearchSettings', 'contents')
        self.PopulateExtensions({
            'ctrl': self._indexSearchOpenWithExtensionType,
            'cascadeCtrl': self._indexSearchOpenWithDefinitionName
        })
        self._indexSearchOpenWithDefinitionName.Show('settings.indexSearchSettings', 'contents')
        self._indexSearchDialogSettings.Visible(True)
        
    def SetupWorkbenchTabControls(self):
        self.HideAllControls()
        self._caption.Show()
        self._iconName.Show()
        self._icons.Visible(True)
        
    def SetupDashboardTabControls(self):
        self.HideAllControls()
        self._caption.Show(None, 'tabContent')
        self._iconName.Show(None, 'tabContent')
        self._columnWidths.Show(None, 'userSettings')
        self._icons.Visible(True)
        
    def SetupDockSectionControls(self):
        self.HideAllControls()
        self._activeTab.Show(None, 'settings')
        self._collapsed.Show(None, 'settings')
        self._stacked.Show(None, 'contents')
        self._partSizes.Show(None, 'settings')
        self._size.Show(None, 'settings')

    def SetupMainViewControls(self):
        self.HideAllControls()
        self._viewName.Show()
        self._throttlingDelay.Show()
        self._caption.Show()
        self._lazyLoad.Show()
        self._enableExcelRtd.Show()
        self._showCheckboxColumn.Show()
        self._showActionMenu.Show()
        self._actionItemsListCtrl.Show()
        
    def SetupDockSectionPartControls(self):
        self.HideAllControls()
        self._viewName.Show('view')
        self._throttlingDelay.Show('view')
        self._caption.Show('view')
        self._actionItemsListCtrl.Show('view')
        self._lazyLoad.Show('view')
        self._enableExcelRtd.Show('view')
        self._showCheckboxColumn.Show('view')
        self._showActionMenu.Show('view')
        self._isUtilityView.Show()
    
    def SetupToolbarControls(self):
        self.HideAllControls()
        self._quickOpen.Visible(True)
        self._instrument.Show()
        self._trade.Show()
        self._insPackage.Show()
        self._dealPackage.Show()
        
    def SetupButtonControls(self, isDockPartNode):
        self.HideAllControls()
        self._label.Show()
        self._icons.Visible(True)
        self._iconName.Show()
        self._extensionType.Show()
        self._whitelist.Show()
        self._blacklist.Show()
        if not isDockPartNode:
            # Dock parts and toolbars have buttons, 
            # but dock part buttons should always be selection controlled.
            self._selectionControlled.Show()    
        self._dialogSettings.Visible(True)
        self._openWithExtensionType.Show()
        self.PopulateExtensions({
            'ctrl': self._openWithExtensionType,
            'cascadeCtrl': self._openWithDefinitionName
        })
        self._openWithDefinitionName.Show()
        
    def SetupDashboardPartControls(self):
        self.HideAllControls() 
        self._viewName.Show('view', 'part')
        self._throttlingDelay.Show('view', 'part')
        self._caption.Show('view', 'part')
        self._actionItemsListCtrl.Show('view', 'part')
        self._lazyLoad.Show('view', 'part')
        self._enableExcelRtd.Show('view', 'part')
        self._showCheckboxColumn.Show('view', 'part')
        self._showActionMenu.Show('view', 'part')
        self._parentViewNames.Show(None, 'part')
        self._collapsed.Show(None, 'settings')
        self._height.Show(None, 'settings')
        self._columnIndex.Show(None, 'settings')
        
    def SetupControls(self):
        def StrControl(name, toolTip, items=[], fieldName=None):
            ctrl = FAppWorkspaceDesignerControls.StrControl(self, name, toolTip, items, fieldName)
            self._controls.append(ctrl)
            return ctrl
        def IntControl(name, toolTip, items=[], fieldName=None):
            ctrl = FAppWorkspaceDesignerControls.IntControl(self, name, toolTip, items, fieldName)
            self._controls.append(ctrl)
            return ctrl
        def BoolControl(name, toolTip, items=[], fieldName=None):
            ctrl = FAppWorkspaceDesignerControls.BoolControl(self, name, toolTip, items, fieldName)
            self._controls.append(ctrl)
            return ctrl
        def RepeatedControl(name, toolTip, items=[], fieldName=None):
            ctrl = FAppWorkspaceDesignerControls.RepeatedControl(self, name, toolTip, items, fieldName)
            self._controls.append(ctrl)
            return ctrl
        def RepeatedDoubleControl(name, toolTip, items=[], fieldName=None):
            ctrl = FAppWorkspaceDesignerControls.RepeatedDoubleControl(self, name, toolTip, items, fieldName)
            self._controls.append(ctrl)
            return ctrl
        def ActionItemsListControl():
            ctrl = FAppWorkspaceDesignerControls.ActionItemsListControl(self)
            self._controls.append(ctrl)
            return ctrl
        def HabitatParametersControl(name, toolTip, fieldName):
            ctrl = FAppWorkspaceDesignerControls.HabitatParametersControl(self, name, toolTip, fieldName=fieldName)
            self._controls.append(ctrl)
            return ctrl
            
        self._caption = StrControl('caption', 'The caption.')
        self._iconName = StrControl('iconName', 'Icon to use. Supports overlaying multiple icons.')
        
        self._activeTab = IntControl('activeTab', 'The active tab, if this section is tabbed.')
        
        self._collapsed = BoolControl('collapsed', 'If checked, this section will be initially collapsed.')
        
        self._stacked = BoolControl('stacked', 'If checked, section parts will be stacked next to each other. Otherwise the section parts will be shown in tabs (if there are more than one).')
        
        self._partSizes = RepeatedDoubleControl('partSizes', 'A comma-separated list of relative part sizes that are used the section parts are shown stacked rather than tabbed.')
        
        self._size = IntControl('size', 'Height or width of this section, depending on its location.')
        
        self._viewName = StrControl('viewName', 'The name of the stored view template to be displayed. Stored view templates are created in the Business Intelligence Workbench application.')
        
        self._lazyLoad = BoolControl('lazyLoad', 'Lazy load conserves resources by only loading the content that is currently viewed. Recommended for large portfolios, queries etc. Turning it off allows local search.')
        self._enableExcelRtd = BoolControl('enableExcelRtd', 'Enables copying grid cells as Excel Real-Time formulas that allows pasting ticking numbers into Excel. Requires the Arena Excel RTD plugin to be installed.')
        self._throttlingDelay = IntControl('throttlingDelay', 'Controls the rate of updates in this view. At least this number of milliseconds will pass between updates. A higher number will make numbers tick less frequently.')
        self._showActionMenu = BoolControl('showActionMenu', 'Shows the action menu.')
        self._showCheckboxColumn = BoolControl('showCheckboxColumn', 'Shows the checkbox column.')
        self._isUtilityView = BoolControl('isUtilityView', 'A utility view has no content of its own but rather shows the currently selected rows in the main view inserted.')
        
        self._label = StrControl('_label', 'If a label is specified, the enumerated items will be shown in a menu button with the specified icon and label. If there is no label the items will be laid out as individual buttons in the toolbar.')
        
        extensionTypes = ['FCustomInstrumentDefinition', 'FDealPackageDefinition', 'FEditableObjectDefinition']
                    
        self._extensionType = StrControl('extensionType', 'Editor extension type.', extensionTypes)
        
        self._whitelist = RepeatedControl('whitelist', 'Only enumerated items in this list will be used. Whitelist is applied before blacklist.')
        
        self._blacklist = RepeatedControl('blacklist', 'All enumerated items, except the ones in this list, will be used. Whitelist is applied before blacklist.')
        
        self._selectionControlled = BoolControl('selectionControlled', 'If checked, the buttons in this group will only be allowed if there is an active selection in the sheet. The selected items will be passed as arguments to the editor definition. Useful for performing bulk actions.')
        
        self._openWithExtensionType = StrControl('openWithExtensionType', 'Open with extension type.', extensionTypes)
        self._openWithDefinitionName = StrControl('openWithDefinitionName', 'Open with definition name.')
        self._openWithExtensionType.control.AddCallback('Changed', self.OnOpenWithExtensionTypeChanged, {
            'ctrl': self._openWithExtensionType, 
            'cascadeCtrl': self._openWithDefinitionName
        })
        
        self._parentViewNames = RepeatedControl('parentViewNames', 'A comma-separated list of view names in this tab for which content changes will change the contents of this view. It acts as a utility viewer of more than one view at a time.')
        
        self._columnIndex = IntControl('columnIndex', 'What dashboard column to put this part in. The first column has index 0.')
        self._height = IntControl('height', '')
        
        self._columnWidths = RepeatedDoubleControl('columnWidths', 'A comma-separated list of column widths expressed as a share of 1.0 (e.g 0.5, 0.5 for two evenly-sized columns). For more information, please refer to FCA 4875.')
        
        self._quickOpen = self.layout.GetControl('quickOpen')
        self._instrument = BoolControl('instrument', 'Show Quick Open Instrument field')
        self._trade = BoolControl('trade', 'Show Quick Open Trade field')
        self._insPackage = BoolControl('insPackage', 'Show Quick Open Instrument Package field')
        self._dealPackage = BoolControl('dealPackage', 'Show Quick Open Deal Package field')
        
        items = {'Application Window': AppWorkspace.WorkspaceSettings.CT_APPLICATION_WINDOW,
                 'Browser Window': AppWorkspace.WorkspaceSettings.CT_BROWSER_WINDOW}
        self._editableObjectTarget = StrControl('editableObjectTarget', 'Controls how editor (deal capture) windows are opened: application windows are confined within the same browser window as the main application, while browser window mode means that editors are opened in their own browser window.', items)
        
        self._marketUniqueIds = RepeatedControl('marketUniqueIds', 'Names of market places to allow the user to connect to.')
        
        self._indexSearchEnabled = BoolControl('indexSearchEnabled', 'Enable index search against the "Instrument" index.', fieldName='enabled')
        self._indexSearchEnvironmentName = HabitatParametersControl('indexSearchEnvironmentName', 'Name of calculation environment where the index search tasks are run. Leave empty to use default calculation environment. It is highly recommended to use a shared calculation environment for index search.', fieldName='habitatParameters')
        self._indexSearchOpenWithExtensionType = StrControl('indexSearchOpenWithExtensionType', 'Open search hits with extension type.', extensionTypes, fieldName='openWithExtensionType')
        self._indexSearchOpenWithDefinitionName = StrControl('indexSearchOpenWithDefinitionName', 'Open search hits with definition name.', fieldName='openWithDefinitionName')
        self._indexSearchOpenWithExtensionType.control.AddCallback('Changed', self.OnOpenWithExtensionTypeChanged, {
            'ctrl': self._indexSearchOpenWithExtensionType, 
            'cascadeCtrl': self._indexSearchOpenWithDefinitionName
        })
        self._indexSearchDialogSettings = self.layout.GetControl('indexSearchDialogSettings')
        self._indexSearchDialogSettings.AddCallback('Activate', self.OnEditDialogSettings, 'contents.settings.indexSearchSettings.dialogSettings')
        
        self.name = self.layout.GetControl('name')
        self.name.AddCallback('Changed', self.OnWorkspaceNameChanged, None)
        
        self.layout.GetControl('iconName').Editable(False)
        self._icons = self.layout.GetControl('icons')
        self._icons.AddCallback('Activate', self.OnSelectIcon, None)

        self._dialogSettings = self.layout.GetControl('dialogSettings')
        self._dialogSettings.AddCallback('Activate', self.OnEditDialogSettings, 'dialogSettings')

        self._actionItemsListCtrl = ActionItemsListControl()

    def GetName(self):
        return self.name.GetData()
        
    def OnWorkspaceNameChanged(self, *args):
        self.parent.SetWorkspaceName(self.GetName())
        self.OnControlChanged()
        
    def PopulateNameField(self):
        self.name.SetData(self.nodeData.Label())

    def OnSelectIcon(self, *args):
        currentIcon = self._iconName.GetData()
        newIconName = acm.UX().Dialogs().SelectIcon(self.parent.Shell(), currentIcon)
        if newIconName:
            self._iconName.SetData(newIconName)
        else:
            self._iconName.Clear()

    def OnEditDialogSettings(self, *args):
        path = args[0]
        nodeData = self.nodeData
        elems = path.split('.')
        elems.reverse()
        while len(elems):
            el = elems.pop()
            nodeData = getattr(nodeData, el)
        dialogSettings = nodeData        
        customDlg = DialogSettingsDialog(self.parent.Shell(), dialogSettings)
        return acm.UX().Dialogs().ShowCustomDialogModal(self.parent.Shell(), customDlg.CreateLayout(), customDlg)

    def OnOpenWithExtensionTypeChanged(self, *args):
        ctrls = args[0]
        ctrls['cascadeCtrl'].control.Clear()
        ctrls['cascadeCtrl'].DoOnChanged()        
        self.PopulateExtensions(ctrls)

    def PopulateExtensions(self, ctrls):
        ext = acm.GetClass(ctrls['ctrl'].control.GetData())
        if ext:    
            items = [x.Value().At('DisplayName') for x in acm.GetDefaultContext().GetAllExtensions(ext)]
            ctrls['cascadeCtrl'].control.Populate(items)

    def HandleCreate( self, layout ):
        self.layout = layout
        self._bindings.AddLayout(layout)
        self.SetupControls()
        self.HideAllControls()
    
    def OnControlChanged(self, *args):
        self.parent.treePanel.UpdateSelectedNode()
#------------------------------------------------------------------------------
class SelectActionItemsDialog(FUxCore.LayoutDialog):

    EXTENSION_TYPES = ['FDealPackageDefinition', 'FCustomInstrumentDefinition', 'FEditableObjectDefinition']    

    def __init__(self, shell, spec = None):
        self.m_shell = shell
        self.m_delegate = DialogSettingsDelegate(shell, spec.dialogSettings)
        self.m_spec = spec
        if not self.m_spec.extensionType:
            self.m_spec.extensionType = self.EXTENSION_TYPES[0]

    def HandleApply(self):
        self.m_spec.extensionType = self.m_extensionType.GetData().decode('latin-1')
        self.m_spec.definitionName = self.m_definitionName.GetData().decode('latin-1')
        self.m_spec.label = self.m_label.GetData().decode('latin-1')
        self.m_spec.icon = self.m_icon.GetData().decode('latin-1')
        
        if not self.m_delegate.HandleApply():
            self.m_spec.ClearField('dialogSettings')
        return True
 
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Action Item Specification')
        self.m_label = layout.GetControl('dialogLabel')
        self.m_extensionType = layout.GetControl('extensionType')
        self.m_extensionType.AddCallback('Changed', self.OnExtensionTypeChanged, None)
        self.m_definitionName = layout.GetControl('definitionName')
        self.m_definitionName.AddCallback('Changed', self.OnDefinitionNameChanged, None)
        self.m_icon = layout.GetControl('dsMenuIcon')
        self.m_icon.Editable(False)
        self.m_selectMenuIcon = layout.GetControl('dsSelectMenuIcon')
        self.m_selectMenuIcon.AddCallback('Activate', self.OnSelectIcon, self.m_icon)
        self.PopulateControls()
        self.SetControlData()
        self.m_delegate.HandleCreate(layout)

    def GetCurrentDefinitionValule(self):
        et = self.m_extensionType.GetData()
        dn = self.m_definitionName.GetData()
        ext = acm.GetDefaultContext().GetExtension(et, acm.FObject, dn)
        if ext:
            return ext.Value()

    def OnSelectIcon(self, ctrl, x):
        currentIcon = ctrl.GetData()
        newIconName = acm.UX().Dialogs().SelectIcon(self.m_shell, currentIcon)
        if newIconName:
            ctrl.SetData(newIconName)
        else:
            ctrl.Clear()

    def OnExtensionTypeChanged(self, *args):
        ext = acm.GetClass(self.m_extensionType.GetData())
        if ext:    
            items = [x.Value().At('DisplayName') for x in acm.GetDefaultContext().GetAllExtensions(ext)]
            self.m_definitionName.Populate(items)
        self.OnDefinitionNameChanged()

    def OnDefinitionNameChanged(self, *args):
        dfn = self.GetCurrentDefinitionValule()
        if dfn:
            label = dfn.DisplayName() if hasattr(dfn, 'DisplayName') else dfn.Caption().AsString() if dfn.Caption() else None
            if label:
                self.m_label.SetData(label)
            else:
                self.m_label.Clear()
            icon = dfn.Icon()
            if icon:
                self.m_icon.SetData(icon)
            else:
                self.m_icon.Clear()
        else:
            self.m_label.Clear()
            self.m_icon.Clear()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. AddPopuplist('extensionType', 'Extension Type', 28)
        b. AddPopuplist('definitionName', 'Definition')
        b. AddInput('dialogLabel', 'Label')
        b.  BeginHorzBox('None')
        b.    AddInput('dsMenuIcon', 'Icon:')
        b.    AddButton('dsSelectMenuIcon', 'Select...')
        b.  EndBox()
        self.m_delegate.CreateLayout(b, 'EtchedIn', 'Dialog Settings')
        b. BeginHorzBox()
        b.   AddFill()
        b.   AddButton('ok', 'OK')
        b.   AddButton('cancel', 'Cancel')
        b. EndBox()
        b.EndBox()
        return b
    
    def PopulateControls(self):
        self.m_extensionType.Populate(self.EXTENSION_TYPES)        
        
    def SetControlData(self):
        self.m_extensionType.SetData(self.m_spec.extensionType.encode('latin-1'))
        self.OnExtensionTypeChanged()
        self.m_definitionName.SetData(self.m_spec.definitionName.encode('latin-1'))
        self.m_label.SetData(self.m_spec.label.encode('latin-1'))
        self.m_icon.SetData(self.m_spec.icon.encode('latin-1'))
#------------------------------------------------------------------------------
class DialogSettingsDialog(FUxCore.LayoutDialog):

    def __init__(self, shell, ds):
        self.delegate = DialogSettingsDelegate(shell, ds)

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Dialog Settings')
        self.delegate.HandleCreate(layout)

    def HandleApply(self):
        return self.delegate.HandleApply()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        self.delegate.CreateLayout(b)
        b. BeginHorzBox()
        b.   AddFill()
        b.   AddButton('ok', 'OK')
        b.   AddButton('cancel', 'Cancel')
        b. EndBox()
        b.EndBox()
        return b
#------------------------------------------------------------------------------
class DialogSettingsDelegate:

    APPLY_MODE_ITEMS = {
        'Save':         EditObjectCreate.DialogSettings.AM_SAVE, 
        'Save New':     EditObjectCreate.DialogSettings.AM_SAVE_NEW, 
        'Close':        EditObjectCreate.DialogSettings.AM_CLOSE, 
        'No Buttons':   EditObjectCreate.DialogSettings.AM_NONE 
    }

    def __init__(self, shell, ds):
        self.shell = shell
        self.ds = ds

    def CreateLayout(self, b, borderType = 'None', label = ''):
        b. BeginVertBox(borderType, label)
        b.  AddPopuplist('dsApplyMode', 'Apply Mode')  
        b.  AddInput('dsCaption', 'Caption')
        b.  AddInput('dsApplyLabel', 'Apply Label')
        b.  BeginHorzBox('None')
        b.    AddInput('dsApplyIcon', 'Apply Icon:')
        b.    AddButton('dsSelectApplyIcon', 'Select...')
        b.  EndBox()
        b.  AddInput('dsCancelLabel', 'Cancel Label')
        b.  BeginHorzBox('None')
        b.    AddInput('dsCancelIcon', 'Cancel Icon:')
        b.    AddButton('dsSelectCancelIcon', 'Select...')
        b.  EndBox()
        b.  AddCheckbox('dsShowSlimDetailed', 'Show Slim/Detailed')
        b. EndBox()

    def HandleCreate(self, layout):
        self.m_caption = layout.GetControl('dsCaption')
        self.m_applyMode = layout.GetControl('dsApplyMode')
        self.m_applyMode.ToolTip('Controls what button combination should be shown in the toolbar. ' + 
                                 'Save and Save New are cancellable and run the corresponding save hooks, ' + 
                                 'Close simply dismantles the deal (package). Leave this setting blank to use the standard toolbar layout.')

        self.m_applyLabel = layout.GetControl('dsApplyLabel')
        self.m_applyIcon = layout.GetControl('dsApplyIcon')
        self.m_applyIcon.Editable(False)
        self.m_selectApplyIcon = layout.GetControl('dsSelectApplyIcon')
        self.m_selectApplyIcon.AddCallback('Activate', self.OnSelectIcon, self.m_applyIcon)
        self.m_cancelLabel = layout.GetControl('dsCancelLabel')
        self.m_cancelIcon = layout.GetControl('dsCancelIcon')
        self.m_cancelIcon.Editable(False)
        self.m_selectCancelIcon = layout.GetControl('dsSelectCancelIcon')
        self.m_selectCancelIcon.AddCallback('Activate', self.OnSelectIcon, self.m_cancelIcon)
        self.m_showSlimDetailed = layout.GetControl('dsShowSlimDetailed')
        self.PopulateControls()
        self.SetControlData()

    def OnSelectIcon(self, ctrl, x):
        currentIcon = ctrl.GetData()
        newIconName = acm.UX().Dialogs().SelectIcon(self.shell, currentIcon)
        if newIconName:
            ctrl.SetData(newIconName)
        else:
            ctrl.Clear()

    def PopulateControls(self):
        self.m_applyMode.Populate(self.APPLY_MODE_ITEMS.keys())
        
    def SetControlData(self):
        ds = self.ds
        if ds.HasField('applyMode'):
            am = next(k for k, v in self.APPLY_MODE_ITEMS.items() if v == ds.applyMode)
            self.m_applyMode.SetData(am)
            self.m_caption.SetData(ds.caption.encode('latin-1'))
            self.m_applyLabel.SetData(ds.applyLabel.encode('latin-1'))
            self.m_applyIcon.SetData(ds.applyIcon.encode('latin-1'))
            self.m_cancelLabel.SetData(ds.cancelLabel.encode('latin-1'))
            self.m_cancelIcon.SetData(ds.cancelIcon.encode('latin-1'))
            self.m_showSlimDetailed.Checked(ds.showSlimDetailed)

    def HandleApply(self):
        am = self.APPLY_MODE_ITEMS.get(self.m_applyMode.GetData())
        if am:
            ds = self.ds
            ds.applyMode = am
            ds.caption = self.m_caption.GetData().decode('latin-1')
            ds.applyLabel = self.m_applyLabel.GetData().decode('latin-1')
            ds.applyIcon = self.m_applyIcon.GetData().decode('latin-1')
            ds.cancelLabel = self.m_cancelLabel.GetData().decode('latin-1')
            ds.cancelIcon = self.m_cancelIcon.GetData().decode('latin-1')
            ds.showSlimDetailed = self.m_showSlimDetailed.Checked()
            return True
        else:
            return False
