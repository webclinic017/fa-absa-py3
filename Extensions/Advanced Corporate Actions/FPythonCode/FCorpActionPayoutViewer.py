""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionPayoutViewer.py"
import acm
import FUxCore

def SelectFirstItem(objList, itemList):
    if objList:
        firstItem = objList[0]
        itemList.SetData(firstItem)


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


def OnDeleteClicked(self, cd):
    val = self.m_values.GetData()
    if val:
        acm.FCorporateActionPayout[val].Delete()
        RemoveItem(self.valList, self.m_values, val)


def OnValDoubleClicked(self, cd):
    val = self.m_values.GetData()
    if val:
        acm.StartRunScript(acm.FCorporateActionPayout[val], 'Modify')


class PayoutsListCustomDialog(FUxCore.LayoutDialog):

    LIST_VALUES = 'listValues'
    BTN_DELETE = 'btnDelete'

    def __init__(self, params):
        self.choices = params['choices']
        self.selected = params['selected']
        self.caption = 'Payouts List'
        self.valLabel = 'Payouts'
        self.valList = []
        self.selectList = []

    def HandleApply(self):
        resultDic = acm.FDictionary()
        resultDic.AtPut('result', self.valList)
        return resultDic

    def SetControlData(self):
        SelectFirstItem(self.valList, self.m_values)

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.caption)
        self.m_values = layout.GetControl(self.LIST_VALUES)
        self.m_values.AddCallback('DefaultAction', OnValDoubleClicked, self)
        self.m_btnDelete = layout.GetControl(self.BTN_DELETE)
        self.m_btnDelete.AddCallback('Activate', OnDeleteClicked, self)
        self.PopulateControls()
        self.SetControlData()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.   AddLabel("lblValues", self.valLabel)
        b.   AddList(self.LIST_VALUES, 10, -1, 15, -1)
        b.  EndBox()
        b. AddSpace(3)
        b. EndBox()
        b. AddSpace(5)
        b. BeginHorzBox()
        b.   AddFill()
        b.   AddButton(self.BTN_DELETE, "Delete")
        b.   AddButton('ok', 'Close')
        b. AddSpace(3)
        b. EndBox()
        b.EndBox()
        return b

    def PopulateControls(self):
        self.valList = [s for s in self.selected]
        self.valList.sort()
        self.m_values.Populate(self.valList)
        if self.valList:
            self.m_values.SetData(self.valList[0])