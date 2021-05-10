""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FBDPInstSelectionDialog.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE

    FSelExpiredInsDlg.py - Custom dialog for select instruments that have run
            the expiration script against it.

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import acm
import ael
import string


import FBDPCommon
import FBDPInstSelection


import FUxCore


class FBDPInstSelectionDialog(FUxCore.LayoutDialog):

    LIST_VALUES = 'listValues'
    LIST_SELECTED = 'listSelected'
    BTN_ADD = 'btnAdd'
    BTN_REMOVE = 'btnRemove'
    BTN_REMOVE_ALL = 'btnRemoveAll'

    CAPTION = 'Select Instruments'
    VAL_ITEMS_LABEL = 'All Instruments'
    SEL_ITEMS_LABEL = 'Selected Instruments'

    def __init__(self, params):
        self.choices = params['choices']
        self.selected = params['selected']
        self.scriptName = params['Script Name']

        self.valList = []
        self.selList = []

    def HandleApply(self):
        selectedIns = []
        for val in self.selList:
            ins = FBDPCommon.ael_to_acm(ael.Instrument[val])
            if not ins:
                continue
            selectedIns.append(ins)
        resultDic = acm.FDictionary()
        resultDic.AtPut('result', selectedIns)
        return resultDic

    def ValidateAdd(self, key, value):
        return True

    def __setControlData(self):
        self.valList.sort()
        self.m_values.Populate(self.valList)
        self.__selectFirstItem(self.valList, self.m_values)
        self.selList.sort()
        self.m_selected.Populate(self.selList)
        self.__selectFirstItem(self.selList, self.m_selected)

    def __populateInstSeletion(self):
        self.m_instQuery.Clear()
        for s in FBDPInstSelection.GetInstSelections():
            self.m_instQuery.AddItem(s.Name())

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.CAPTION)
        self.m_values = layout.GetControl(self.LIST_VALUES)
        self.m_values.AddCallback('DefaultAction',
                self.onValDoubleClicked.__func__, self)
        self.m_selected = layout.GetControl(self.LIST_SELECTED)
        self.m_selected.AddCallback('DefaultAction',
                self.onSelDoubleClicked.__func__, self)
        self.m_btnAdd = layout.GetControl(self.BTN_ADD)
        self.m_btnAdd.AddCallback('Activate',
                self.onAddClicked.__func__, self)
        self.m_btnRemove = layout.GetControl(self.BTN_REMOVE)
        self.m_btnRemove.AddCallback('Activate',
                self.onRemoveClicked.__func__, self)
        self.m_btnRemoveAll = layout.GetControl(self.BTN_REMOVE_ALL)
        self.m_btnRemoveAll.AddCallback('Activate',
                self.onRemoveAllClicked.__func__, self)

        self.m_instQuery = layout.GetControl("instQuery")
        self.m_btnGo = layout.GetControl("go")
        self.m_btnGo.AddCallback('Activate',
                self.onGoClicked.__func__, self)

        self.__populateInstSeletion()
        self.__setControlData()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.   BeginHorzBox()
        b.    AddOption("instQuery", "Instrument Query")
        b.    AddButton("go", "Go")
        b.   EndBox()
        b.   AddLabel("lblValues", self.VAL_ITEMS_LABEL)
        b.   AddList(self.LIST_VALUES, 10, -1, 55, -1)
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
        b.   AddLabel("lblSelect", self.SEL_ITEMS_LABEL)
        b.   AddList(self.LIST_SELECTED, 10, -1, 58, -1)
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

    def __selectFirstItem(self, objList, itemList):
        if objList:
            firstItem = objList[0]
            itemList.SetData(firstItem)

    def __addItem(self, objList, itemList, item):
        objList.append(item)
        objList.sort()
        itemList.Populate(objList)
        itemList.SetData(item)

    def __removeItem(self, objList, itemList, item):
        index = objList.index(item)
        objList.remove(item)
        itemList.RemoveItem(item)
        if objList:
            if len(objList) <= index:
                index -= 1
            newItem = objList[index]
            if newItem:
                itemList.SetData(newItem)

    def onAddClicked(self, cd):
        val = self.m_values.GetData()
        if val:
            self.__addItem(self.selList, self.m_selected, val)
            self.__removeItem(self.valList, self.m_values, val)

    def onValDoubleClicked(self, cd):
        val = self.m_values.GetData()
        if val:
            self.__addItem(self.selList, self.m_selected, val)
            self.__removeItem(self.valList, self.m_values, val)

    def onSelDoubleClicked(self, cd):
        val = self.m_selected.GetData()
        if val:
            self.__addItem(self.valList, self.m_values, val)
            self.__removeItem(self.selList, self.m_selected, val)

    def onRemoveClicked(self, cd):
        val = self.m_selected.GetData()
        if val:
            self.__addItem(self.valList, self.m_values, val)
            self.__removeItem(self.selList, self.m_selected, val)

    def onRemoveAllClicked(self, cd):
        for val in self.selList:
            self.valList.append(val)
        self.selList = []
        self.m_selected.Clear()
        self.valList.sort()
        self.m_values.Populate(self.valList)
        self.__selectFirstItem(self.valList, self.m_values)

    def onGoClicked(self, cd):
        val = self.m_instQuery.GetData()
        instSelection = FBDPInstSelection.GetInstSelections()
        if not instSelection:
            return

        for s in instSelection:
            if s.Name() == val:
                self.LoadQuery(s)
                return

    def LoadQuery(self, s):
        self.valList = s.Run()
        self.valList.sort()
        self.m_values.Populate(self.valList)
        self.__selectFirstItem(self.valList, self.m_values)
