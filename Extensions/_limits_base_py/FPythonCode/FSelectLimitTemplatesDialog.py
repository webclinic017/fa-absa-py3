""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FSelectLimitTemplatesDialog.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSelectLimitTemplatesDialog

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils
import FUxCore
from collections import defaultdict

logger = FAssetManagementUtils.logger
EXTENSION_GROUP = 'limits'
EXTENSION_GROUP_ITEM = 'templates'


class SelectLimitTemplatesDialog(FUxCore.LayoutDialog):

    def __init__(self, selected):
        self.m_available = None
        self.m_selected = None
        self.m_selected_ext = selected
        self.m_fuxDlg = None
        self.m_add = None
        self.m_remove = None
        
    def HandleApply(self):
        selection = []
        for val in self.m_selected.GetRootItem().Children():
            valStr = str(val.GetData())
            if valStr:
                selection.append(valStr)
        resultDic = acm.FDictionary()
        resultDic.AtPut('result', selection)
        return resultDic
    
    @staticmethod
    def GetLimitTemplates():
        limitTemplates = defaultdict(list)
        extensions = acm.GetDefaultContext().GetAllExtensions('FParameters', 'FObject',
                True, True, EXTENSION_GROUP, EXTENSION_GROUP_ITEM, False)
        for ext in extensions:
            try:
                limitTemplates[ext.Module()].append(ext.Name())
            except ValueError as e:
                logger.ELOG( 'Failed to load limit template "%s": %s' % (ext.Name(), str(e)) )
        return limitTemplates
    
    def _AddPreviouslySelected(self):
        rootItem = self.m_selected.GetRootItem()
        for selected in self.m_selected_ext:
            child = rootItem.AddChild()
            selectedSymbol = acm.FSymbol(selected)
            child.Label(selectedSymbol)
            child.Icon(None)
            child.SetData(selectedSymbol)
        
    def _TemplateIcon(self, template):
        if self.m_selected.ItemExists(template):
            return 'Check'
        else:
            return 'MarketPlaces'
    
    def _SetTemplateIcon(self, item):
        item.Icon(self._TemplateIcon(item.GetData()), self._TemplateIcon(item.GetData()))
    
    def _InitCtrls(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Limit Templates')
        self.m_available = layout.GetControl('available')
        self.m_available.Label('Available:')
        self.m_selected = layout.GetControl('selected')
        self.m_selected.Label('Selected:')
        self.m_add = layout.GetControl('addButton')
        self.m_remove = layout.GetControl('removeButton')
        self.m_available.EnableMultiSelect()
        self.m_selected.ShowGridLines()
        self.m_selected.EnableMultiSelect()
        self.m_available.AddCallback("SelectionChanged", self.AvailableSelectionChanged, self)
        self.m_available.AddCallback("DefaultAction", self.AddItems, self)
        self.m_selected.AddCallback("DefaultAction", self.RemoveSelected, self)
        self.m_add.AddCallback("Activate", self.AddItems, self)
        self.m_remove.AddCallback("Activate", self.RemoveSelected, self)
    
    def _PopulateTree(self):
        rootItem = self.m_available.GetRootItem()
        limitTemplates = self.GetLimitTemplates()
        for module in list(limitTemplates.keys()):
            modChild = rootItem.AddChild()
            modChild.Label(module.Name())
            modChild.Icon(module.Icon(), module.Icon())
            modChild.SetData(module)
            for limitTemplate in sorted(limitTemplates[module]):
                tempChild = modChild.AddChild()
                tempChild.Label(limitTemplate)
                tempChild.SetData(limitTemplate)
                self._SetTemplateIcon(tempChild)
    
    def HandleCreate( self, dlg, layout):
        self._InitCtrls( dlg, layout)
        self._AddPreviouslySelected()
        self._PopulateTree()
   
    def AvailableSelectionChanged(self, *_args):
        self.m_selected.SelectAllItems(False)
        selectedItems = [item.GetData() for item in self.m_available.GetSelectedItems()]
        for item in self.m_selected.GetRootItem().Children():
            if item.GetData() in selectedItems:
                item.Select()
   
    def UpdateIcons(self):
        for module in self.m_available.GetRootItem().Children():
            for item in module.Children():
                self._SetTemplateIcon(item)
                    
    def RemoveSelected(self, *_args):
        self.m_selected.RemoveAllSelectedItems(False)
        self.UpdateIcons()
        
    def _AddItem(self, rootItem, item):
        name = item.GetData()
        if not self.m_selected.ItemExists(name):
            child = rootItem.AddChild()
            child.Label(name)
            child.Icon(None)
            child.SetData(name)
            self._SetTemplateIcon(item)
    
    def AddItems(self, *_args):
        selectedItems = self.m_available.GetSelectedItems()
        rootItem = self.m_selected.GetRootItem()
        for item in selectedItems:
            if item.Children():
                for childItem in item.Children():
                    self._AddItem(rootItem, childItem)
            else:
                self._AddItem(rootItem, item)
                
    @staticmethod
    def CreateLayout():
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('None')
        b.  BeginVertBox('None', 'Available')
        b.      AddTree("available", 300, 20)
        b.  EndBox()
        b.  BeginVertBox('None', 'Available:')
        b.      AddFill()
        b.      AddButton("addButton", "Add")
        b.      AddButton("removeButton", "Remove")
        b.      AddSeparator()
        b.  EndBox()
        b.  BeginVertBox('None')
        b.      AddList("selected", 20, -1, 50)
        b.      BeginHorzBox('None')
        b.          AddFill()
        b.          AddButton("ok", "OK")
        b.          AddButton("cancel", "Cancel")
        b.      EndBox()
        b.  EndBox()
        b.EndBox()
        return b
