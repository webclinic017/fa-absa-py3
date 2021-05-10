""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/aggr_arch/etc/FAggruleSelectItem.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import acm
import FUxCore


SEPARATOR = '  - Fltnbr: '


def OnAddClicked(self, cd):

    val = self.m_values.GetData()
    if val:
        AddItem(self.selectList, self.m_selected, val)
        RemoveItem(self.valList, self.m_values, val)


def OnValDoubleClicked(self, cd):
    val = self.m_values.GetData()
    if val:
        AddItem(self.selectList, self.m_selected, val)
        RemoveItem(self.valList, self.m_values, val)


def OnSelDoubleClicked(self, cd):
    val = self.m_selected.GetData()
    if val:
        AddItem(self.valList, self.m_values, val)
        RemoveItem(self.selectList, self.m_selected, val)


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


def OnRemoveAllClicked(self, cd):
    for val in self.selectList:
        self.valList.append(val)
    self.selectList = []
    self.m_selected.Clear()
    self.valList.sort()
    self.m_values.Populate(self.valList)
    SelectFirstItem(self.valList, self.m_values)


def SelectFirstItem(objList, itemList):
    if objList:
        firstItem = objList[0]
        itemList.SetData(firstItem)


class SelectAggrulesCustomDialog(FUxCore.LayoutDialog):

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
        self.caption = 'Selected Aggrules'
        self.valLabel = 'All Aggrules'
        self.selectLabel = 'Selected Aggrules'
        self.valList = []
        self.selectList = []

    def HandleApply(self):
        selectedIds = []
        for val in self.selectList:
            fltr = val.partition(SEPARATOR)[2]
            if fltr:
                selectedIds.append(fltr)
        resultDic = acm.FDictionary()
        resultDic.AtPut('result', selectedIds)
        return resultDic

    def ValidateAdd(self, key, value):
        return True

    def GetValFromFltid(self, valList, fltid):
        for val in valList:
            fltr = val.partition(SEPARATOR)[2]
            if fltr == str(fltid):
                return val
        return None

    def SetControlData(self):
        for fltid in self.selected:
            val = self.GetValFromFltid(self.valList, fltid)
            if val:
                self.valList.remove(val)
                self.selectList.append(val)
        self.valList.sort()
        self.selectList.sort()
        self.m_values.Populate(self.valList)
        self.m_selected.Populate(self.selectList)
        SelectFirstItem(self.valList, self.m_values)
        SelectFirstItem(self.selectList, self.m_selected)

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
        self.PopulateControls()
        self.SetControlData()

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
        b.   AddSpace(3)
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

    def PopulateControls(self):
        self.valList = self.LoadAggRules()
        self.valList.sort()
        self.m_values.Populate(self.valList)
        if self.valList:
            self.m_values.SetData(self.valList[0])

    def LoadAggRules(self):
        ruleList = []
        rules = acm.FAggregationRule.Select('')
        for rule in rules:
            no = rule.Ordernbr()
            if no < 10:
                no = '0' + str(no)
            ruleList.append(str(no) + SEPARATOR + str(rule.Fltnbr()))
        return ruleList
