""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FClientInfoHorzPanel.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FClientInfoHorzPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm

from FPanel import Panel
from FIntegratedWorkbenchUtils import IsKindOf
from FEvent import EventCallback

class ClientInfoHorzPanel(Panel):

    EDIT_APPLICATION_NAME = 'Party Definition'

    NAME = 'nameCtrl'
    CONTACT = 'contactCtrl'
    CONTACT_LABEL = 'contactNameCtrl'
    SHORT_NAME = 'shortNameCtrl'
    COUNTRY = 'countryCtrl'
    TYPE = 'typeCtrl'
    TELEPHONE = 'telephoneCtrl'
    EDIT_PARTY = 'editPartyCtrl'

    def __init__(self):
        Panel.__init__(self)
        self._nameCtrl = None
        self._contactCtrl = None
        self._currentClient = None
        self._shortNameCtrl = None
        self._countryCtrl = None
        self._typeCtrl = None
        self._telephoneCtrl = None
        self._clientObserver = self._ClientObserver(self)
        self._currentParty = None
        self._editPartyCtrl = None

    def RemoveSubscriptions(self):
        Panel.RemoveSubscriptions(self)
        self._ClearClientObserverIf()

    def InitControls(self, layout):
        self._nameCtrl = layout.GetControl(self.NAME)
        self._nameCtrl.Editable(False)
        self._contactCtrl = layout.GetControl(self.CONTACT)
        self._contactCtrl.AddCallback('DefaultAction', self._ContactRowDoubleClicked, None)
        self._contactCtrl.ShowGridLines()
        self._contactCtrl.ShowColumnHeaders()
        self._contactCtrl.AddColumn('Contact Name', 200, 'Client contact name')
        self._contactCtrl.AddColumn('Telephone', 150, 'Client contact telephone')
        self._contactCtrl.AddColumn('Email address', 300, 'Client contact email address')

        self._shortNameCtrl = layout.GetControl(self.SHORT_NAME)
        self._shortNameCtrl.Editable(False)
        self._countryCtrl = layout.GetControl(self.COUNTRY)
        self._countryCtrl.Editable(False)
        self._typeCtrl = layout.GetControl(self.TYPE)
        self._typeCtrl.Editable(False)
        self._telephoneCtrl = layout.GetControl(self.TELEPHONE)
        self._telephoneCtrl.Editable(False)
        self._editPartyCtrl = layout.GetControl(self.EDIT_PARTY)
        self._editPartyCtrl.AddCallback('Activate', self._EditPartyButtonPressed, None)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', '')
        b.  BeginHorzBox('None', '')
        b.    AddInput(self.SHORT_NAME, 'Name')
        b.    AddInput(self.NAME, 'Full Name')
        b.    AddInput(self.COUNTRY, 'Country')
        b.    AddInput(self.TYPE, 'Type')
        b.    AddInput(self.TELEPHONE, 'Telephone')
        b.    AddButton(self.EDIT_PARTY, 'Edit...')
        b.  EndBox()
        b.  AddList(self.CONTACT, -1, 20, self.Settings().Width(), self.Settings().Height())
        b.EndBox()
        return b

    class _ClientObserver(object):
        """ Internal class that listens to changes to the FCounterParty
        instance currently shown by the view."""
        def __init__(self, parent):
            self._parent = parent

        def ServerUpdate(self, sender, aspect, param=None):
            if sender and IsKindOf(sender, acm.FCounterParty):
                self._parent._ShowClient(sender)

    @EventCallback
    def OnCounterpartiesSelected(self, event):
        client = event.First()
        if client:
            self._ShowClient(client)
        else:
            self._ClearClientInfo()

    def _ClearClientInfo(self):
        self._currentParty = None
        self._nameCtrl.SetData('')
        self._shortNameCtrl.SetData('')
        self._countryCtrl.SetData('')
        self._typeCtrl.SetData('')
        self._telephoneCtrl.SetData('')
        self._contactCtrl.RemoveAllItems()
        self._ClearClientObserverIf()

    def _ClearClientObserverIf(self):
        if self._currentClient:
            self._currentClient.RemoveDependent(self._clientObserver)
            self._currentClient = None

    def _ShowClient(self, client, contact=None):
        """ Show relevant client info.
        'client' is an instance of FCounterParty """
        if client and IsKindOf(client, acm.FParty):
            self._currentParty = client
            # Set the party data first
            self._nameCtrl.SetData(client.Fullname())
            self._contactCtrl.RemoveAllItems()
            self._shortNameCtrl.SetData(client.Name())
            self._countryCtrl.SetData(client.Country())
            self._typeCtrl.SetData(client.Type())
            self._telephoneCtrl.SetData(client.Telephone())

            # Then set the contact data
            contacts = client.Contacts()
            rooti = self._contactCtrl.GetRootItem()
            for c in contacts.SortByProperty('Name'):
                item = rooti.AddChild(True)
                item.Label(c.Name(), 0)
                item.Label(c.Telephone(), 1)
                item.Label(c.Email(), 2)
                item.Icon(c.Icon(), c.Icon())
                item.SetData(c)
                if contact and (contact.Name() == c.Name()):
                    item.Selected(True)

            # Make self a dependant of the client
            self._ClearClientObserverIf()
            self._currentClient = client
            self._currentClient.AddDependent(self._clientObserver)

    def _EditPartyButtonPressed(self, evt, data):
        acm.StartApplication(self.EDIT_APPLICATION_NAME, self._currentParty)

    def _ContactRowDoubleClicked(self, evt, data):
        item = self._contactCtrl.GetSelectedItem()
        if item:
            contact = item.GetData()
            acm.StartApplication(self.EDIT_APPLICATION_NAME, contact)
