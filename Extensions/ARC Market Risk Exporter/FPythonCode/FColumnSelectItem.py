""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FColumnSelectItem.py"
import acm
import FUxCore

def OnAddClicked(self, cd):
    val = self.m_values.GetData()
    if val:
        self.AddItemOnSelectedList(val)
        self.RemoveItem(self.valList, self.m_values, val)


def OnValDoubleClicked(self, cd):
    val = self.m_values.GetData()
    if val:
        self.AddItemOnSelectedList(val)
        self.RemoveItem(self.valList, self.m_values, val)


def OnSelDoubleClicked(self, cd):
    val = self.m_selected.GetData()
    if val:
        self.AddItemOnValueList(val)
        self.RemoveItem(self.selectList, self.m_selected, val)

def OnRemoveClicked(self, cd):
    val = self.m_selected.GetData()
    if val:
        self.AddItemOnValueList(val)
        self.RemoveItem(self.selectList, self.m_selected, val)


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


class SelectColumnsCustomDialog(FUxCore.LayoutDialog):

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
        self.caption = 'Selected Columns'
        self.valLabel = 'All Columns'
        self.selectLabel = 'Selected Columns'
        self.valList = []
        self.selectList = []

    def AddItemOnSelectedList(self, item):
        self.selectList.append(item)
        self.selectList.sort()
        self.m_selected.Populate(self.selectList)
        self.m_selected.SetData(item)
    
    def AddItemOnValueList(self, item):
        self.valList.append(item)
        self.valList.sort()
        self.m_values.Populate(self.valList)
        self.m_values.SetData(item)

    def RemoveItem(self, objList, itemList, item):
        index = objList.index(item)
        objList.remove(item)
        itemList.RemoveItem(item)
        if objList:
            if len(objList) <= index:
                index -= 1
            newItem = objList[index]
            if newItem:
                itemList.SetData(newItem)

    def HandleApply(self):
        selectedIds = []
        for val in self.selectList:
            if val:
                selectedIds.append(val)
        resultDic = acm.FDictionary()
        resultDic.AtPut('result', selectedIds)
        return resultDic

    def ValidateAdd(self, key, value):
        return True

    def GetValFromFltid(self, valList, fltid):
        for val in valList:
            if val == fltid:
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
        self.valList = self.LoadColumns()
        self.valList.sort()
        self.m_values.Populate(self.valList)
        if self.valList:
            self.m_values.SetData(self.valList[0])

    def LoadColumns(self):
        columnList = []
        columns = acm.GetDefaultContext().GetAllExtensions('FColumnDefinition',
                None, True, True, 'sheet columns', 'portfoliosheet').Sort()
        for column in columns:
            columnList.append(column.Name().Text())
        return columnList


class SelectSingleColumnsCustomDialog(SelectColumnsCustomDialog):

    def __init__(self, params):
        self.choices = params['choices']
        self.selected = params['selected']
        self.caption = 'Selected Column'
        self.valLabel = 'All Columns'
        self.selectLabel = 'Selected Column'
        self.valList = []
        self.selectList = []

    def AddItemOnSelectedList(self, item):
        for i in self.selectList:
            self.valList.append(i)

        self.valList.sort()
        self.m_values.Populate(self.valList)
        
        self.selectList = []
        self.selectList.append(item)

        self.m_selected.Populate(self.selectList)
        self.m_selected.SetData(item)

       
class SelectRiskFactorColumnsCustomDialog(SelectSingleColumnsCustomDialog):
    SupportedColumns = ('Position Delta Per Equity Price Risk Factor',
                     'Position Delta Cash Per Equity Price Risk Factor',
                     'Position Delta Per Price Risk Factor',
                     'Position Gamma Cash Per Equity Price Risk Factor',
                     'Position Gamma Per Equity Price Risk Factor')

    def LoadColumns(self):
        return [column for column in self.SupportedColumns]
