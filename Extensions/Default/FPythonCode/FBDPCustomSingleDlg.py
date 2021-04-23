""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPCustomSingleDlg.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE

    FBDPCustomSingleDlg.py - Module with customized dialog

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FUxCore
import FBDPCommon

# GUI callbacks
def OnAddClicked(self, cd):
    if self.allow_multiple_values or len(self.selectList) < 1:
        val = self.m_values.GetData()
        if val:
            val = self.GetDisplayNameFromObjectCb(obj=val)
            AddItem(self.selectList, self.m_selected, val, self)
            RemoveItem(self.valList, self.m_values, val, self)

    return

def OnAddAllClicked(self, cd):
    assert self.allow_multiple_values, 'Multiple values not allowed'
    for val in self.valList[:]:
        AddItem(self.selectList, self.m_selected, val, self)
        RemoveItem(self.valList, self.m_values, val, self)

    self.m_values.Clear()
    return

def OnValDoubleClicked(self, cd):
    return OnAddClicked(self, cd)

def OnSelDoubleClicked(self, cd):
    val = self.m_selected.GetData()
    if val:
        val = self.GetDisplayNameFromObjectCb(obj=val)
        AddItem(self.valList, self.m_values, val, self)
        RemoveItem(self.selectList, self.m_selected, val, self)

    return

def OnRemoveClicked(self, cd):
    val = self.m_selected.GetData()
    if val:
        val = self.GetDisplayNameFromObjectCb(obj=val)
        AddItem(self.valList, self.m_values, val, self)
        RemoveItem(self.selectList, self.m_selected, val, self)

    return

def OnRemoveAllClicked(self, cd):
    for val in self.selectList:
        self.valList.append(val)

    self.selectList = []
    self.m_selected.Clear()
    self.SortChoices(self.valList)
    self.m_values.Populate(self.valList)
    SelectFirstItem(self.valList, self.m_values, self)
    return

def AddItem(displayList, objList, displayItem, self):
    displayList.append(displayItem)
    self.SortChoices(displayList)
    items = self.GetObjectsFromNames(names=displayList)
    item = self.getObjectFromName(name=displayItem)
    objList.Populate(items)
    objList.SetData(item)
    return

def RemoveItem(displayList, objList, displayItem, self):
    displayIndex = displayList.index(displayItem)
    displayList.remove(displayItem)
    item = self.getObjectFromName(name=displayItem)
    objList.RemoveItem(item)
    if displayList:
        if len(displayList) <= displayIndex:
            displayIndex -= 1

        newDisplayItem = displayList[displayIndex]
        newItem = self.getObjectFromName(name=newDisplayItem)
        objList.SetData(newItem)

    return

def SelectFirstItem(displayList, objList, self):
    if displayList:
        firstItem = displayList[0]
        if self:
            firstItem = self.getObjectFromName(name=firstItem)

        objList.SetData(firstItem)

    return

class SelectItemCustomDialog(FUxCore.LayoutDialog):
    LIST_VALUES = 'listValues'
    LIST_SELECTED = 'listSelected'
    BTN_ADD = 'btnAdd'
    BTN_REMOVE = 'btnRemove'
    BTN_ADD_ALL = 'btnAddAll'
    BTN_REMOVE_ALL = 'btnRemoveAll'

    def __init__(
        self, shell, params, selectionName,
        getObjectChoicesCb, multiple_values=True,
        customSortedObjectsCb=None, getDisplayNameFromObjectCb=None
    ):
        #self.choices = params['choices']
        #Contains output names
        self.selected = params['selected']
        self.caption = 'Selected %s' % selectionName
        self.valLabel = 'All %s' % selectionName
        self.selectLabel = 'Selected %s' % selectionName
        #Contains display names
        self.valList = []
        #Contains display names
        self.selectList = []
        #Contains actual entities
        self.objectToNameMap = {}

        #Returns of list of possible selection choices
        self.getObjChoicesCb = getObjectChoicesCb or (lambda: [])

        """
        Define custom sorted function for non-trivial sorting requirements
        """
        #Returns a sorted list - defaults to alphanumeric sorting
        self.sortedCb = customSortedObjectsCb or self.DefaultSorted

        """
        The following should be used when the displayed form
        differs from the output
        """
        #Returns the form that is displayed on the selection dialog
        self.displayNameFromObjectCb = getDisplayNameFromObjectCb or \
            (lambda obj: obj)
        self.allow_multiple_values = bool(multiple_values)
        self.shell = shell

    def Create(self):
        dialog = acm.UX().Dialogs().ShowCustomDialogModal(
            self.shell, self.CreateLayout(), self
        )
        return dialog

    def GetObjectChoices(self):
        objs = self.getObjChoicesCb()
        objs = self.sortedCb(objs)
        names = []
        for obj in objs:
            name = self.GetDisplayNameFromObjectCb(obj=obj)
            self.objectToNameMap[name] = obj
            names.append(name)

        return names

    def DefaultSorted(self, objs):
        inf = float('inf')
        str_type = type('')

        def key(obj):
            if isinstance(obj, str_type):
                pfx = int(obj.partition(' ')[0]) if \
                    obj and obj[0].isdigit() else inf
                return (pfx, obj.lower())

            return obj

        return sorted(objs, key=key)

    def SortChoices(self, names):
        if not names:
            return

        items = self.GetObjectsFromNames(names=names)
        items = self.sortedCb(items)
        del names[:]
        s_names = [self.GetDisplayNameFromObjectCb(item) for item in items]
        names.extend(s_names)
        return

    def getObjectFromName(self, name):
        return self.objectToNameMap[name]

    def GetObjectsFromNames(self, names):
        return [self.getObjectFromName(name=name) for name in names]

    def GetDisplayNameFromObjectCb(self, obj):
        return self.displayNameFromObjectCb(obj)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.   AddLabel("lblValues", self.valLabel)
        b.   AddList(self.LIST_VALUES, 10, -1, 21, -1)
        b.  EndBox()
        b.  BeginVertBox()
        b.   AddFill()
        b.   AddButton(self.BTN_ADD, "Add")
        b.   AddButton(self.BTN_REMOVE, "Remove")
        if self.allow_multiple_values:
            b.   AddSpace(3)
            b.   AddButton(self.BTN_ADD_ALL, "Add All")
            b.   AddButton(self.BTN_REMOVE_ALL, "Remove All")

        b.   AddFill()
        b.  EndBox()
        b.  AddSpace(2)
        b.  BeginVertBox()
        b.   AddLabel("lblSelect", self.selectLabel)
        b.   AddList(self.LIST_SELECTED, 10, -1, 24, -1)
        b.  EndBox()
        b. AddSpace(3)
        b. EndBox()
        b. AddSpace(5)
        b. BeginHorzBox()
        b.   AddFill()
        b.   AddButton('ok', 'OK')
        b.   AddButton('cancel', 'Cancel')
        b. AddSpace(3)
        b. EndBox()
        b.EndBox()
        return b

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.caption)
        self.m_values = layout.GetControl(self.LIST_VALUES)
        self.m_values.AddCallback('DefaultAction', OnValDoubleClicked, self)
        self.m_selected = layout.GetControl(self.LIST_SELECTED)
        self.m_selected.AddCallback('DefaultAction', OnSelDoubleClicked, self)
        self.m_btnAdd = layout.GetControl(self.BTN_ADD)
        self.m_btnAdd.AddCallback('Activate', OnAddClicked, self)
        self.m_btnRemove = layout.GetControl(self.BTN_REMOVE)
        self.m_btnRemove.AddCallback('Activate', OnRemoveClicked, self)
        if self.allow_multiple_values:
            self.m_btnAddAll = layout.GetControl(self.BTN_ADD_ALL)
            self.m_btnAddAll.AddCallback('Activate', OnAddAllClicked, self)
            self.m_btnRemoveAll = layout.GetControl(self.BTN_REMOVE_ALL)
            self.m_btnRemoveAll.AddCallback(
                'Activate', OnRemoveAllClicked, self)

        self.PopulateControls()
        self.SetControlData()

    def PopulateControls(self):
        self.valList = self.GetObjectChoices()
        self.selectList = [v for v in list(self.selected) if v in self.valList]
        self.valList = [v for v in self.valList if v not in self.selectList]
        self.SortChoices(self.valList)
        items = self.GetObjectsFromNames(names=self.valList)
        self.m_values.Populate(items)
        items = self.GetObjectsFromNames(names=self.selectList)
        self.m_selected.Populate(items)
        if len(self.valList):
            item = self.getObjectFromName(name=self.valList[0])
            self.m_values.SetData(item)

    def SetControlData(self):
        for selection in self.selected:
            if selection and selection in self.valList:
                self.valList.remove(selection)
                self.selectList.append(selection)

        self.SortChoices(self.valList)
        self.SortChoices(self.selectList)
        items = self.GetObjectsFromNames(names=self.valList)
        self.m_values.Populate(items)
        items = self.GetObjectsFromNames(names=self.selectList)
        self.m_selected.Populate(items)
        SelectFirstItem(self.valList, self.m_values, self)
        SelectFirstItem(self.selectList, self.m_selected, self)

    def HandleApply(self):
        items = self.GetObjectsFromNames(names=self.selectList)
        resultDic = acm.FDictionary()
        resultDic.AtPut('result', items)
        return resultDic

    def ValidateAdd(self, key, value):
        return True

class SelectArchivedInstrumentPackagesCustomDialog(SelectItemCustomDialog):
    def __init__(
        self, shell, params, multiple_values=True, name_to_oid_dict=None
    ):
        self._name_to_oid_map = name_to_oid_dict
        if self._name_to_oid_map is not None:
            self._name_to_oid_map.clear()
        SelectItemCustomDialog.__init__(
            self,
            shell=shell,
            params=params,
            multiple_values=multiple_values,
            selectionName='Instrument Packages',
            getObjectChoicesCb=self.GetChoicesCb
        )

    def GetChoicesCb(self):
        query = (
            'SELECT ip.name, ip.seqnbr FROM instrument_package as ip '
            'WHERE ip.archive_status = 1'
        )
        selections = FBDPCommon.FBDPQuerySelection(
            name='Instrument Packages',
            query_expr=query,
            num_results_per_row=2
        ).Run()
        _selections = []
        for name, oid in selections:
            name = str(name)
            _selections.append(name)
            if self._name_to_oid_map is not None:
                self._name_to_oid_map[name] = int(oid)

        return _selections
