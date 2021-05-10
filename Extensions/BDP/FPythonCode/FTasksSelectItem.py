""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/pace_runner/etc/FTasksSelectItem.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import acm
import FUxCore


def OnAddClicked(self, cd):

    val = self.m_values.GetData()
    if val:
        AddItem(self.selectList, self.m_selected, val)
        RemoveItem(self.valList, self.m_values, val)
        self.m_modulelist.Enabled(False)


def OnValDoubleClicked(self, cd):
    val = self.m_values.GetData()
    if val:
        AddItem(self.selectList, self.m_selected, val)
        RemoveItem(self.valList, self.m_values, val)
        self.m_modulelist.Enabled(False)


def OnSelDoubleClicked(self, cd):
    val = self.m_selected.GetData()
    if val:
        AddItem(self.valList, self.m_values, val)
        RemoveItem(self.selectList, self.m_selected, val)
    if not self.selectList:
        self.m_modulelist.Enabled(True)


def AddItem(objList, itemList, item):
    objList.append(item)
    objList.sort()
    itemList.Populate(objList)
    itemList.SetData(item)


def RemoveItem(objList, itemList, item):
    index = objList.index(item)
    objList.remove(item)
    itemList.RemoveItem(item)
    if objList:
        if len(objList) <= index:
            index -= 1
        newItem = objList[index]
        if newItem:
            itemList.SetData(newItem)


def OnRemoveClicked(self, cd):
    val = self.m_selected.GetData()
    if val:
        AddItem(self.valList, self.m_values, val)
        RemoveItem(self.selectList, self.m_selected, val)
    if not self.selectList:
        self.m_modulelist.Enabled(True)


def OnRemoveAllClicked(self, cd):
    for val in self.selectList:
        self.valList.append(val)
    self.selectList = []
    self.m_selected.Clear()
    self.valList.sort()
    self.m_values.Populate(self.valList)
    SelectFirstItem(self.valList, self.m_values)
    self.m_modulelist.Enabled(True)


def SelectFirstItem(objList, itemList):
    if objList:
        firstItem = objList[0]
        itemList.SetData(firstItem)


def OnListChanged(self, cd):
    val = self.m_modulelist.GetData()
    self.LoadTasks(val)

    
class SelectTasksCustomDialog(FUxCore.LayoutDialog):

    DICT_KEYS = 'dictKeys'
    DICT_VALUES = 'dictValues'
    DICT_PAIRS = 'dictPairs'
    LIST_VALUES = 'listValues'
    LIST_SELECTED = 'listSelected'
    BTN_ADD = 'btnAdd'
    BTN_REMOVE = 'btnRemove'
    BTN_REMOVE_ALL = 'btnRemoveAll'

    def __init__(self, params):
        self.choices = params['choices']
        self.selected = params['selected']
        self.caption = 'Selected Tasks'
        self.valLabel = 'All Tasks'
        self.selectLabel = 'Selected Tasks'
        self.valList = []
        self.selectList = []
        self.supportedModules = params.At("supportedModules", [])
        
    def HandleApply(self):
        resultDic = acm.FDictionary()
        resultDic.AtPut('result', self.selectList)
        return resultDic
        
    def ValidateAdd(self, key, value):
        return True

    def SetControlData(self):
        for t in self.selected:
            if t:
                self.valList.remove(t)
                self.selectList.append(t)
        self.valList.sort()
        self.selectList.sort()
        self.m_values.Populate(self.valList)
        self.m_selected.Populate(self.selectList)
        SelectFirstItem(self.valList, self.m_values)
        SelectFirstItem(self.selectList, self.m_selected)
        if self.selectList:
            self.m_modulelist.Enabled(False)

    def __selectFirstItem(self, objList, itemList):
        if objList:
            firstItem = objList[0]
            itemList.SetData(firstItem)

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
        self.m_btnRemoveAll = layout.GetControl(self.BTN_REMOVE_ALL)
        self.m_btnRemoveAll.AddCallback('Activate', OnRemoveAllClicked, self)
        self.m_modulelist = layout.GetControl("modulelist")
        self.m_modulelist.AddCallback('Changed', OnListChanged, self)
        
        self.PopulateControls()
        self.SetControlData()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.    AddOption("modulelist", "Script Module")
        b.   AddLabel("lblValues", self.valLabel)
        b.   AddList(self.LIST_VALUES, 20, -1, 41, -1)
        b.  EndBox()
        b.  BeginVertBox()
        b.   AddFill()
        b.   AddButton(self.BTN_ADD, "Add")
        b.   AddButton(self.BTN_REMOVE, "Remove")
        b.   AddSpace(3)
        b.   AddButton(self.BTN_REMOVE_ALL, "Remove All")
        b.   AddFill()
        b.  EndBox()
        b.  AddSpace(2)
        b.  BeginVertBox()
        b.   AddLabel("lblSelect", self.selectLabel)
        b.   AddList(self.LIST_SELECTED, 20, -1, 44, -1)
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

    def PopulateControls(self):
        
        supportedModules = ["FAggregation",
                            "FFxAggregation",
                            "FPLSweep",
                            "FCashAggregation",
                            "FFxSpotRolloverMMFunding",
                            "FFxSpotRolloverSwapFunding"]
        if self.supportedModules:
            supportedModules = self.supportedModules

        savedSupported = supportedModules[0]
        for supported in supportedModules:
            self.m_modulelist.AddItem(supported)
            if (self.selected and
                acm.FAelTask[self.selected[0]].ModuleName() == supported):
                savedSupported = supported

        self.m_modulelist.SetData(savedSupported)
        self.LoadTasks(savedSupported)
        
    def LoadTasks(self, moduleName):
        self.valList = []
        tasks = acm.FAelTask.Select('moduleName = {}'.format(moduleName))
        for t in tasks:
            self.valList.append(t.Name())

        self.m_values.Populate(self.valList)
        self.__selectFirstItem(self.valList, self.m_values)
