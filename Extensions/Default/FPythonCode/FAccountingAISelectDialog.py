""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingAISelectDialog.py"
import acm
import FUxCore


def OnAccountingInstructionDoubleClick(dialog, cd):
    dialog.AddAccountingInstruction()

def OnSelectedAccountingInstructionDoubleClick(dialog, cd):
    dialog.RemoveAccountingInstruction()

def OnAddButton(dialog, cd):
    dialog.AddAccountingInstruction()

def OnRemoveButton(dialog, cd):
    dialog.RemoveAccountingInstruction()

def OnRemoveAllButton(dialog, cd):
    dialog.RemoveAllAccountingInstructions()

def OnCancelButton(dialog, cd):
    dialog.m_fuxDialog.CloseDialogCancel()

def GetLayoutBuilder():
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.   AddLabel('labelAccountingInstructions', 'Accounting Instructions')
        b.   AddList('accountingInstructions', 10, -1, 30, -1)
        b.  EndBox()
        b.  BeginVertBox()
        b.   AddFill()
        b.   AddButton('addButton', 'Add')
        b.   AddButton('removeButton', 'Remove')
        b.   AddSpace(3)
        b.   AddButton('removeAllButton', 'Remove All')
        b.   AddFill()
        b.  EndBox()
        b.  AddSpace(2)
        b.  BeginVertBox()
        b.   AddLabel('labelSelectedAccountingInstructions', 'Selected Accounting Instructions')
        b.   AddList('selectedAccountingInstructions', 10, -1, 30, -1)
        b.  EndBox()
        b. AddSpace(3)
        b. EndBox()
        b. AddSpace(5)
        b. BeginHorzBox()
        b.   AddFill()
        b.   AddButton('ok', 'OK')
        b.   AddButton('cancelButton', 'Cancel')
        b. AddSpace(3)
        b. EndBox()
        b.EndBox()
        return b

class AISelectionDialog(FUxCore.LayoutDialog):

    def __init__(self):

        self.m_accountingInstructions         = None
        self.m_selectedAccountingInstructions = None
        self.m_addButton                      = None
        self.m_removeButton                   = None
        self.m_removeAllButton                = None
        self.m_fuxDialog                      = None
        self.m_cancelButton                   = None
        self.aiList = acm.FArray()
        self.aiSelectedList = acm.FArray()

    def HandleCreate(self, dialog, layout):
        self.m_fuxDialog = dialog
        self.m_fuxDialog.Caption('Select Accounting Instructions')

        self.m_accountingInstructions = layout.GetControl('accountingInstructions')
        self.m_accountingInstructions.AddCallback('DefaultAction', OnAccountingInstructionDoubleClick, self)

        self.m_selectedAccountingInstructions = layout.GetControl('selectedAccountingInstructions')
        self.m_selectedAccountingInstructions.AddCallback('DefaultAction', OnSelectedAccountingInstructionDoubleClick, self)

        self.m_addButton = layout.GetControl('addButton')
        self.m_addButton.AddCallback('Activate', OnAddButton, self)

        self.m_removeButton = layout.GetControl('removeButton')
        self.m_removeButton.AddCallback('Activate', OnRemoveButton, self)

        self.m_removeAllButton = layout.GetControl('removeAllButton')
        self.m_removeAllButton.AddCallback('Activate', OnRemoveAllButton, self)

        self.m_addButton = layout.GetControl('cancelButton')
        self.m_addButton.AddCallback('Activate', OnCancelButton, self)

        self.LoadAccountingInstructions()

    def AddAccountingInstruction(self):
        ai = self.m_accountingInstructions.GetData()
        if ai:
            self.m_accountingInstructions.RemoveItem(ai)
            self.aiList.Remove(ai)
            self.aiSelectedList.Add(ai)
            self.m_selectedAccountingInstructions.Populate(self.aiSelectedList.SortByProperty('Name', True))

    def RemoveAccountingInstruction(self):
        ai = self.m_selectedAccountingInstructions.GetData()
        if ai:
            self.m_selectedAccountingInstructions.RemoveItem(ai)
            self.aiSelectedList.Remove(ai)
            self.aiList.Add(ai)
            self.m_accountingInstructions.Populate(self.aiList.SortByProperty('Name', True))

    def RemoveAllAccountingInstructions(self):
        self.aiList.AddAll(self.aiSelectedList)
        self.m_selectedAccountingInstructions.RemoveAllItems()
        self.m_accountingInstructions.Populate(self.aiList.SortByProperty('Name', True))
        self.aiSelectedList.Clear()

    def LoadAccountingInstructions(self):
        if 0 == self.aiList.Size() and 0 == self.aiSelectedList.Size():
            accountingInstructions = acm.FAccountingInstruction.Select('')
            sortedByName = accountingInstructions.SortByProperty('Name', True)
            self.aiList.AddAll(sortedByName)
            self.m_accountingInstructions.Populate(sortedByName)
        else:
            self.m_accountingInstructions.Populate(self.aiList.SortByProperty('Name', True))
            self.m_selectedAccountingInstructions.Populate(self.aiSelectedList.SortByProperty('Name', True))

    def GetSelectedAccountingInstructions(self):
        return self.aiSelectedList

def ShowDialog(shell, aiSelectionDialog):
    layoutBuilder = GetLayoutBuilder()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, layoutBuilder, aiSelectionDialog)




