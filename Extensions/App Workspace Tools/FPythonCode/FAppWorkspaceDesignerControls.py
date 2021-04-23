""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/AppWorkspaceTools/etc/FAppWorkspaceDesignerControls.py"
""" Compiled: 2018-06-07 17:06:19 """

#__src_file__ = "extensions/AppWorkspaceTools/etc/FAppWorkspaceDesignerControls.py"
import Contracts_AppConfig_Messages_AppWorkspace as AppWorkspace

class ControlBase():
    def __init__(self, panel, name, toolTip, items=[], fieldName=None):
        self.panel = panel
        self.controlName = name
        self.fieldName = fieldName if fieldName else self.controlName
        self.toolTip = toolTip
        self.items = items
        self.objectPath = None
        self.dictKey = None
        self.SetupControl()
        
    def GetNodeData(self):
        nodeData = self.panel.nodeData
        if self.dictKey:            
            nodeData = getattr(nodeData, self.dictKey)
        if self.objectPath:
            elems = self.objectPath.split('.')
            elems.reverse()
            while len(elems):
                el = elems.pop()
                nodeData = getattr(nodeData, el)
        return nodeData
        
    def GetCtrlData(self):
        nodeData = self.GetNodeData()
        return getattr(nodeData, self.fieldName.replace('_', ''))
            
    def PopulateControl(self):
        if self.items:
            keys = self.items.keys() if isinstance(self.items, dict) else self.items
            self.control.Populate(keys)
        
    def SetupControl(self):
        self.control = self.panel.layout.GetControl(self.controlName)
        self.control.AddCallback('Changed', self.OnChanged, None)
        if self.toolTip:
            self.control.ToolTip(self.toolTip)
        
    def Show(self, path = None, dictKey = None):
        self.objectPath = path
        self.dictKey = dictKey
        self.PopulateControl()
        self.control.Visible(True)
    
    def Hide(self):
        self.control.Visible(False)
        
    def GetData(self):
        return self.control.GetData()
        
    def SetData(self, value):
        self.control.SetData(value)

    def Clear(self):    
        self.control.Clear()
    
    def OnChanged(self, *args):
        self.DoOnChanged()
        self.panel.OnControlChanged()
    
    def DoOnChanged(self):
        raise NotImplementedError('DoOnChanged')

class IntControl(ControlBase):
    def DoOnChanged(self):
        data = self.GetNodeData()
        setattr(data, self.fieldName, int(self.control.GetData()))
    
    def PopulateControl(self):
        ControlBase.PopulateControl(self)
        ctrlData = self.GetCtrlData()
        self.control.SetData(ctrlData)

class BoolControl(ControlBase):
    def DoOnChanged(self):
        data = self.GetNodeData()
        setattr(data, self.fieldName, self.control.Checked())
    
    def SetupControl(self):
        ControlBase.SetupControl(self)
        self.control.AddCallback('Activate', self.OnChanged, None)
    
    def PopulateControl(self):
        ControlBase.PopulateControl(self)
        ctrlData = self.GetCtrlData()
        self.control.Checked(ctrlData)

class StrControl(ControlBase):
    def DoOnChanged(self):
        data = self.GetNodeData()
        ctrlData = self.control.GetData()
        if self.items and isinstance(self.items, dict):
            ctrlData = self.items[ctrlData]
        setattr(data, self.fieldName.replace('_', ''), ctrlData)
    
    def PopulateControl(self):
        ControlBase.PopulateControl(self)
        ctrlData = self.GetCtrlData()
        if self.items and isinstance(self.items, dict):
            for k in self.items:
                if self.items[k] == ctrlData:
                    ctrlData = k
                    break
                
        self.control.SetData(ctrlData.encode('utf-8'))

class HabitatParametersControl(ControlBase):
    def DoOnChanged(self):
        import Contracts_Tk_Messages_TkEnumerations as TkEnum
        nodeData = self.GetNodeData()
        data = getattr(nodeData, self.fieldName)
        data.Clear()
        ctrlData = self.control.GetData()
        if ctrlData:
            data.environmentName = ctrlData.encode('utf-8')
            data.type = TkEnum.htNamedEnvironment
        else:
            data.type = TkEnum.htDefault
    
    def PopulateControl(self):
        import Contracts_Tk_Messages_TkEnumerations as TkEnum
        ctrlData = self.GetCtrlData()
        if ctrlData.type == TkEnum.htNamedEnvironment:
            s = ctrlData.environmentName or ''
            self.control.SetData(s.encode('utf-8'))
        else:
            self.control.SetData('')

class RepeatedControl(ControlBase):
    def DoOnChanged(self):
        data = self.GetNodeData()
        container = getattr(data, self.fieldName)
        container.__delslice__(0, len(container))
        
        inputs = filter(
            lambda x: len(x) > 0, 
            map(
                lambda x: x.strip(), 
                self.control.GetData().split(',')
            ))
        for input in inputs:
            container.append(self.StrToValue(input))
    
    def PopulateControl(self):
        ControlBase.PopulateControl(self)
        ctrlData = self.GetCtrlData()
        if len(ctrlData) != 0:
            self.control.SetData(', '.join([self.ValueToStr(x) for x in ctrlData]).encode('utf-8'))
        else:
            self.control.Clear()
    
    def StrToValue(self, s):
        return s
    
    def ValueToStr(self, v):
        return str(v)

class RepeatedDoubleControl(RepeatedControl):
    def StrToValue(self, value):
        try:
            return float(value)
        except ValueError:
            return 0

class ActionItemsListControl(ControlBase):

    def __init__(self, panel):
        ControlBase.__init__(self, panel, '', '', None)    

    def SetupControl(self):
        l = self.panel.layout
        self._actionItemsList = l.GetControl('actionItems')
        self._actionItemsList.ShowColumnHeaders(True)
        self._actionItemsList.AddColumn('Definition', 120)
        self._actionItemsList.AddColumn('Label', 120)
        self._actionItemsList.AddColumn('Is Default', 60)
        self._actionItemsList.AddCallback('SelectionChanged', self.OnActionItemSelectionChanged, None)
        self._actionItemsList.AddCallback('DefaultAction', self.OnEditActionItem, None)

        self._addActionItemBtn = l.GetControl('addActionItem')
        self._addActionItemBtn.AddCallback('Activate', self.OnAddActionItem, None)
        
        self._removeActionItemBtn = l.GetControl('removeActionItem')
        self._removeActionItemBtn.AddCallback('Activate', self.OnRemoveActionItem, None)
        self._removeActionItemBtn.Enabled(False)
        
        self._setDefaultActionItemBtn = l.GetControl('setDefaultActionItem')
        self._setDefaultActionItemBtn.AddCallback('Activate', self.OnSetDefaultActionItem, None)
        self._setDefaultActionItemBtn.Enabled(False)        

    def Hide(self):
        self._actionItemsList.Visible(False)
        self._addActionItemBtn.Visible(False)
        self._removeActionItemBtn.Visible(False)
        self._setDefaultActionItemBtn.Visible(False)

    def Show(self, path = None, dictKey = None):
        self.objectPath = path
        self.dictKey = dictKey
        self.PopulateControl()
        self._actionItemsList.Visible(True)
        self._addActionItemBtn.Visible(True)
        self._removeActionItemBtn.Visible(True)
        self._setDefaultActionItemBtn.Visible(True)

    def PopulateControl(self):
        self._actionItemsList.RemoveAllItems()        
        for spec in self.GetNodeData().actionMenuItems:
            self.AddActionItemRow(spec)                        

    def AddActionItemRow(self, spec):        
        rootItem = self._actionItemsList.GetRootItem()
        newRow = rootItem.AddChild(True)
        newRow.SetData(spec)
        self.UpdateActionListRow(newRow)

    def OnActionItemSelectionChanged(self, *args):
        count = len(self._actionItemsList.GetSelectedItems())
        self._setDefaultActionItemBtn.Enabled(count == 1)
        self._removeActionItemBtn.Enabled(count >= 1)
        
    def OnAddActionItem(self, *args):
        spec = AppWorkspace.ActionItemSpecification()
        if self.EditInDialog(spec):
            self.GetNodeData().actionMenuItems.extend([spec])
            self.AddActionItemRow(spec)

    def OnEditActionItem(self, *args):
        row = self._actionItemsList.GetSelectedItem()
        self.EditInDialog(row.GetData())
        self.UpdateActionListRow(row)

    def EditInDialog(self, spec):
        import FAppWorkspaceDesignerPanels, acm
        shell = self.panel.parent.Shell()
        customDlg = FAppWorkspaceDesignerPanels.SelectActionItemsDialog(shell, spec)
        return acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg)                    

    def UpdateActionListRow(self, row):
        spec = row.GetData()
        row.Icon(spec.icon.encode('latin-1', 'ignore'))
        row.Label(spec.definitionName.encode('latin-1', 'ignore'), 0)
        row.Label(spec.label.encode('latin-1', 'ignore'), 1)
        row.Label('Yes' if spec.isDefault else '', 2)

    def OnRemoveActionItem(self, *args):
        for item in self._actionItemsList.GetSelectedItems():
            self.GetNodeData().actionMenuItems.remove(item.GetData())
        self._actionItemsList.RemoveAllSelectedItems(False)
        
    def OnSetDefaultActionItem(self, *args):
        items = self._actionItemsList.GetSelectedItems()
        if len(items) == 1:
            selected = items[0].GetData()
            for child in self._actionItemsList.GetRootItem().Children():
                spec = child.GetData() 
                if spec == selected:
                    spec.isDefault = not spec.isDefault
                else:
                    spec.isDefault = False            
                self.UpdateActionListRow(child)


