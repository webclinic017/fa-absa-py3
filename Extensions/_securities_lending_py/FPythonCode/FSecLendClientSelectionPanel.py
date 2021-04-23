""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendClientSelectionPanel.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendClientSelectionPanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Client View - Panel for selecting a client.

------------------------------------------------------------------------------------------------"""
import acm
from FPanel import Panel
from FSecLendEvents import OnClientViewCounterpartySelected, OnClientViewCounterpartyChangedFromOrderCapture
from FEvent import EventCallback

class SecLendClientSelectionPanel(Panel):

    def __init__(self):
        super(SecLendClientSelectionPanel, self).__init__()
        self._treeCtrl = None
        self._search = None

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('Invisible')
        b.  AddInput('search', '')
        b.  AddSpace(2)
        b.  AddTree('treeCtrl', width=200, height=70)
        b.EndBox()
        return b

    def InitControls(self, layout):
        self.InitSearchControl(layout)
        self.InitTreeControl(layout)

    def InitSearchControl(self, layout):
        self._search = layout.GetControl('search')
        self._search.ToolTip('Enter search criteria to filter the clients')
        self._search.AddCallback('Changed', self.OnSearch, None)

    def InitTreeControl(self, layout):
        self._treeCtrl = layout.GetControl('treeCtrl')
        self._treeCtrl.AddCallback('SelectionChanged', self.OnSelectionChanged, None)
        self._treeCtrl.AddCallback('ContextMenu', self.OnTreeContextMenu, None)
        self.AddClients()

    def AddClients(self, searchCriteria=''):
        self._treeCtrl.RemoveAllItems()
        root = self._treeCtrl.GetRootItem()

        partyQry = acm.CreateFASQLQuery('FParty', 'AND')
        partyQry.AddAttrNodeBool('NotTrading', False)
        typeNode = partyQry.AddOpNode('OR')
        typeNode.AddAttrNode('Type', 'EQUAL', 'Counterparty')
        typeNode.AddAttrNode('Type', 'EQUAL', 'Client')
        if searchCriteria:
            partyQry.AddAttrNode('Name', 're_like_nocase', '*{}*'.format(searchCriteria))
                   
        for party in partyQry.Select():
            treeItem = root.AddChild()
            treeItem.Label(party.Name())
            treeItem.SetData(party)
            treeItem.Icon(party.Icon(), party.Icon())

    def GetSelectedClient(self):
        if self._treeCtrl.GetSelectedItem() and self._treeCtrl.GetSelectedItem().GetData():
            selectedItem = self._treeCtrl.GetSelectedItem().GetData()
            return selectedItem if selectedItem.IsKindOf(acm.FParty) else None

    def OnSearch(self, *args):
        self.AddClients(self._search.GetData())

    def OnSelectionChanged(self, *args):
        if self._treeCtrl.GetSelectedItem() and self._treeCtrl.GetSelectedItem().GetData():
            counterparty = self._treeCtrl.GetSelectedItem().GetData()
            self.SendEvent(OnClientViewCounterpartySelected(self, counterparty))

    def OnTreeContextMenu(self, *args):
        selectedItems = args[1].At('items')
        menuBuilder = args[1].At('menuBuilder')
        objects = [item.GetData() for item in selectedItems]
        acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, objects, False)
        
    @EventCallback
    def OnClientViewCounterpartyChangedFromOrderCapture(self, event):
        if event.Counterparty():
            self._treeCtrl.RemoveAllItems()
            root = self._treeCtrl.GetRootItem()
            treeItem = root.AddChild()
            treeItem.Label(event.CounterpartyName())
            treeItem.SetData(event.Counterparty())
            treeItem.Icon(event.Counterparty().Icon(), event.Counterparty().Icon())
        else:
            self.AddClients()