from __future__ import print_function
import acm
import FUxCore

s_userPaneVisibleKey =  acm.FSymbol('userPaneVisible')
s_contactsPaneVisibleKey =  acm.FSymbol('contactsPaneVisible')

def CopyIcon(iconName, newIconName) :
    if not acm.UX().IconFromName(newIconName) :
        icon = acm.UX().IconFromName(iconName)
        icon.Name(newIconName)
        icon.RegisterIcon()

def CreateApplicationInstance():
    CopyIcon('FUser', 'FPerson')
    CopyIcon('FUser', 'FPerson')

    return PersonEditorApplication()
    
def ReallyStartApplication(person = None):
    acm.UX().SessionManager().StartApplication('Person Editor', person)

def StartApplication(eii):
    ReallyStartApplication();

def StartApplicationFromObject(eii):
    users = eii.ExtensionObject()
    
    if users :
        for user in users :
            ReallyStartApplication(user.Person());


def LinkPersonToObject(eii) :
    usersOrContacts = eii.ExtensionObject()
    
    if usersOrContacts :
        person = acm.UX().Dialogs().SelectObjectsInsertItemsWithProviders(eii.Parameter('shell'), acm.FPerson, False)

        if person :
            for userOrContact in usersOrContacts :
                try :
                    userOrContact.Person(person);
                    userOrContact.Commit()
                except StandardError as ex:
                    print (ex)    

class PersonCommand(FUxCore.MenuItem):
    def __init__(self, parent, invokeCB, enabledCB = None, checkedCB = None, userData = None):
        self.m_parent = parent
        self.m_invokeCB = invokeCB
        self.m_enabledCB = enabledCB
        self.m_checkedCB = checkedCB
        self.m_userData = userData

    def Invoke(self, cd):
        if self.m_userData != None:
            self.m_invokeCB(self.m_userData)
        else :
            self.m_invokeCB()
    
    def Applicable(self):
        return True
        
    def Enabled(self):
        return self.m_enabledCB(self.m_userData) if self.m_enabledCB else True
    
    def Checked(self):
        return self.m_checkedCB(self.m_userData) if self.m_checkedCB else False


class PersonEditorApplication(FUxCore.LayoutApplication):
    def __init__(self):
        FUxCore.LayoutApplication.__init__(self)

        self.m_person = acm.FPerson()
        self.m_personClone = self.m_person.Clone()
        self.m_firstNameInput = None
        self.m_lastNameInput = None
        self.m_dateOfBirthInput = None
        self.m_nationalIdInput = None
        self.m_exchangeIdInput = None
        self.m_crmID = None
        self.m_userTree = None
        self.m_contactsTree = None
        self.m_layoutIsInitilized = False;
        self.m_objectsToCommit = {}
        self.m_serverUpdateEnabled = True


    def CreateLinkUserCB(self):
        return PersonCommand(self, self.LinkUser, self.DefaultEnabled)

    def CreateRemoveUserLinkCB(self):
        return PersonCommand(self, self.RemoveLinkUser, self.EnableRemoveUserLink)

    def CreateLinkContactCB(self):
        return PersonCommand(self, self.LinkContact, self.DefaultEnabled)

    def CreateRemoveContactLinkCB(self):
        return PersonCommand(self, self.RemoveLinkContact, self.EnableRemoveContactLink)

    def EnableRemoveUserLink(self, ud) :
        return self.m_userTree.GetSelectedItem() != None

    def EnableRemoveContactLink(self, ud) :
        return self.m_contactsTree.GetSelectedItem() != None

    def CreateShowUsersPaneCB(self):
        return PersonCommand(self, self.ShowPane, None, self.PaneIsVisible, self.m_userTree)

    def CreateShowContactsPaneCB(self):
        return PersonCommand(self, self.ShowPane, None, self.PaneIsVisible, self.m_contactsTree)

    def CreateEditAdditionalInfoCB(self):
        return PersonCommand(self, self.EditAdditionalInfo, self.EditAdditionalInfoEnabled)

    def EditAdditionalInfoEnabled(self, ud):
        return self.m_person != None and not self.m_person.IsInfant()

    def Link(self, domain, domainDisplayName, root, icon = None):
        ret = False
        if self.m_person :
            ret = True

            if self.m_person.IsInfant() :
                ret = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Question', 'To link the person to a ' + domainDisplayName + ' it need to be saved, do you want to save?')
                if ret == 'Button1' :
                    ret = self.CommitPerson()
                else:
                    ret = False
                

            if ret:
                objects = acm.UX().Dialogs().SelectObjectsInsertItemsWithProviders(self.Shell(), domain, True)

                if objects:
                    for object in objects :
                        try:
                            self.UpdateObjectsPersonLink(object, self.m_person)
                            self.AddLinkedObjectTreeNode(root, object, icon if icon else object.Icon())

                        except RuntimeError as ex:
                            print (ex)

        return ret


    def LinkUser(self):
        self.Link(acm.FUser, 'User', self.m_userTree.GetRootItem())

    def RemoveLink(self, tree):
        ret = False;
        userItems = tree.GetSelectedItems()
        if userItems :
            for userItem in userItems :
                object = userItem.GetData()
                if object :
                    try :
                        self.UpdateObjectsPersonLink(object, None)
                        userItem.Remove()            
                        ret = True
                    except StandardError as ex:
                        print (ex)

        return ret

    def EditAdditionalInfo(self) :
        acm.UX().Dialogs().EditAdditionalInfo(self.Shell(), self.m_person)

    def RemoveLinkUser(self):
        self.RemoveLink(self.m_userTree)

    def RemoveLinkContact(self):
        self.RemoveLink(self.m_contactsTree)

    def LinkContact(self) :
        self.Link(acm.FContact, 'Contact', self.m_contactsTree.GetRootItem(), 'FriendUser')

    def ShowPane(self, pane) :
        pane.Visible(not pane.Visible())
    
    def PaneIsVisible(self, pane) :
        return pane.Visible()

    def DefaultEnabled(self, ud) :
        return self.m_person != None

    def UserTreeCommands(self) :
        userTreeCommands = [
        ['linkToUser',             'View',  'Link to User',               'Link to a user',                                    'Ctrl+L',       'l',      self.CreateLinkUserCB, False ],
        ['removeLinkToUser',       'View',  'Remove Link',                'Remove Link to user',                               '',       '',             self.CreateRemoveUserLinkCB, False ],
        FUxCore.Separator(),
        ['showUserPane',           'View',  'Show User Pane',             'Show the linked user pane',                         'Ctrl+1',       '',       self.CreateShowUsersPaneCB, False ],
        ]

        return userTreeCommands

    def ContactsTreeCommands(self):
        contactsTreeCommands = [
        ['linkToContact',          'View',  'Link to Contact',            'Link to a contact',                                 'Ctrl+A',       'a',      self.CreateLinkContactCB, False ],
        ['removeLinkToContact',    'View',  'Remove Link',                'Remove Link to contact',                               '',       '',          self.CreateRemoveContactLinkCB, False ],
        FUxCore.Separator(),
        ['showContactPane',        'View',  'Show Contacts Pane',         'Show the linked contacts pane',                     'Ctrl+2',       '',       self.CreateShowContactsPaneCB, False ],
        ]

        return contactsTreeCommands

    def GeneralCommands(self) :
        generalCommands = [
        ['editAdditionalInfo',     'View',  'Additional Info',            'Edit Additional Info',                              '',              '',      self.CreateEditAdditionalInfoCB, False ],
        ]

        return generalCommands

    def Commands(self) :
        commands = []

        commands.extend(self.UserTreeCommands())
        commands.extend(self.ContactsTreeCommands())
        commands.extend(self.GeneralCommands())
        
        return commands

    def HandleRegisterCommands(self, builder):
        fileCommands = acm.FSet()
        
        fileCommands.Add('FileNew')
        fileCommands.Add('FileOpen')
        fileCommands.Add('FileSave')
        fileCommands.Add('FileDelete')
            
        builder.RegisterCommands(FUxCore.ConvertCommands(self.Commands()), fileCommands)
    
    def HandleStandardFileCommandInvoke(self, commandName):
        if commandName == 'FileNew':
            self.OnFileNew()
        if commandName == 'FileOpen':
            self.OnFileOpen()
        if commandName == 'FileSave':
            self.OnFileSave()
        if commandName == 'FileDelete':
            self.OnFileDelete()
            
    def HandleStandardFileCommandEnabled(self, commandName):
        ret = True
        if commandName == 'FileSave':
            ret = self.m_person != None
        if commandName == 'FileDelete':
            ret = self.m_person != None and not self.m_person.IsInfant()

        return ret

    def ValidateSaveCB(self, ud, namn, existingItem, p3):
        isValidSave = existingItem == None

        if existingItem :
            ret = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Question', 'Are you sure you want to replace the person ' + existingItem.StringKey() + '?')
            if ret == 'Button1' :
                try:
                    existingItem.Delete()
                    isValidSave = True
                except RuntimeError as ex:
                    acm.UX().Dialogs().MessageBoxInformation(self.Shell(), 'Unable delete object ' + existingItem.StringKey())
                

        return isValidSave    
       
    def DoFileNew(self):
        self.Clear()

    def OnFileNew(self):
        if self.VerifyCloseSetup('Do you want to save the current person?'):
            self.DoFileNew()

    def Clear(self) :
        self.m_person = acm.FPerson()

        self.SetPersonData(self.m_person)
        self.UpdateControls()

        self.SetContentCaption('')

    def RemovePersonLinks(self, collection) :
        if collection :
            for obj in collection :
                obj.Person(None)
                obj.Commit()

    def Delete(self) :
        if self.m_person :
            self.m_serverUpdateEnabled = False;

            try :
                self.RemovePersonLinks(self.m_person.Users())    
                self.RemovePersonLinks(self.m_person.Contacts())    
                self.m_person.Delete()
                self.Clear()
            except StandardError as ex :
                acm.UX().Dialogs().MessageBoxInformation(self.Shell(), 'Unable to delete the current Person: ' + ex.message)

            self.m_serverUpdateEnabled = True;

    def OnFileDelete(self):
        ret = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Question', 'Are you sure you want to delete the current person?')

        if ret == 'Button1' :
            self.Delete()                    

    def UpdateObjectsPersonLink(self, object, person) :
        clone = object.Clone()
        clone.Person(person)
        self.m_objectsToCommit[object] = clone

    def CommitPerson(self) :
        ret = False
        self.m_serverUpdateEnabled = False;

        if self.m_person:
            try :
                self.GetPersonData(self.m_person)
                self.m_person.Commit()
                self.m_personClone = self.m_person.Clone()

                for object, clone in self.m_objectsToCommit.iteritems() :
                    object.Apply(clone)
                    object.Commit()

                self.m_objectsToCommit = {}
                self.SetCaption()
                ret = True
            except StandardError as ex:
                acm.UX().Dialogs().MessageBoxInformation(self.Shell(), 'Unable to save the current Person: ' + ex.message)


        self.m_serverUpdateEnabled = True;
                
        return ret
       
    def OnFileSave(self):
        self.CommitPerson()
          

    def OnFileOpen(self):
        if self.VerifyCloseSetup('Do you want to save the current Person?'):
            selectedObject = acm.UX().Dialogs().SelectObject(self.Shell(), 'Select Person', 'Persons', self.Persons(), None)
            if selectedObject != None:
                self.SetPersonData(selectedObject)
    
    def Persons(self):
        return acm.FPerson.Select('').SortByProperty('Name')
    
        
    def HandleSetContents(self, contents):
        if self.VerifyCloseSetup('Do you want to save the current person?'):
            if contents != None:
                if contents.IsKindOf('FPerson'):
                    self.m_person = contents
                    self.m_personClone = self.m_person.Clone()
                    if self.m_layoutIsInitilized:
                        self.SetPersonData(self.m_person)
    
    def HandleGetContents(self):
        return self.m_person
        

    def GetCurrentObject(self) :
        return self.m_person

    def CanHandleObject(self, obj):
        ret = False

        if obj :
            ret = obj.IsKindOf('FPerson')

        return ret


    def HandleObject(self, obj):
        print ('HandleObject')
        print (obj)
        if obj.IsKindOf('FPerson'):
            self.m_person = obj
            self.SetPersonData(self.m_person)

    
    def GetApplicationIcon(self):
        return 'FUser'
    
    def UpdateControls(self):
        pass


    def ServerUpdate(self, sender, aspectSymbol, parameter):
        pass


    def InitLayout(self, creationInfo):
        builder = acm.FUxLayoutBuilder()

        builder.BeginVertBox('Invisible')
        builder.    AddInput('firstNameInput', 'First Name')
        builder.    AddInput('lastNameInput', 'Last Name')
        builder.    AddInput('dateOfBirthInput', 'Date Of Birth')
        builder.    AddInput('nationalIdInput', 'National ID')
        builder.    AddInput('exchangeIdInput', 'Exchange ID')
        builder.    AddInput('crmID', 'CRM ID')
        builder.    AddSpace(10)
        builder.    AddTree('userTree', -1, 150)
        builder.    AddSpace(10)
        builder.    AddTree('contactsTree', -1, 150)
        builder.EndBox()

        layout = creationInfo.AddPane(builder, 'mainPane')

        self.m_firstNameInput = layout.GetControl('firstNameInput')
        self.m_lastNameInput = layout.GetControl('lastNameInput')
        self.m_dateOfBirthInput = layout.GetControl('dateOfBirthInput')
        self.m_nationalIdInput = layout.GetControl('nationalIdInput')
        self.m_exchangeIdInput = layout.GetControl('exchangeIdInput')
        self.m_crmID = layout.GetControl('crmID')
        self.m_userTree = layout.GetControl('userTree')
        self.m_contactsTree = layout.GetControl('contactsTree')


        self.m_firstNameInput.MaxTextLength(140)
        self.m_lastNameInput.MaxTextLength(140)
        self.m_dateOfBirthInput.MaxTextLength(10)
        self.m_nationalIdInput.MaxTextLength(40)
        self.m_exchangeIdInput.MaxTextLength(9)
        self.m_crmID.MaxTextLength(40)

        self.m_userTree.ShowColumnHeaders(True)
        self.m_userTree.ShowHierarchyLines(False)
        self.m_userTree.ColumnLabel(0, 'Linked Users')
        self.m_userTree.AddCallback('ContextMenu', self.OnTreeContextMenu, (self.m_userTree, self.UserTreeCommands) )
        self.m_userTree.EnableMultiSelect(True)

        self.m_contactsTree.ShowColumnHeaders(True)
        self.m_contactsTree.ShowHierarchyLines(False)
        self.m_contactsTree.ColumnLabel(0, 'Linked Contacts')
        self.m_contactsTree.ColumnWidth(0, 200)
        self.m_contactsTree.AddColumn("Party", 200)
        self.m_contactsTree.AddCallback('ContextMenu', self.OnTreeContextMenu, (self.m_contactsTree, self.ContactsTreeCommands) )
        self.m_contactsTree.EnableMultiSelect(True)

        self.m_contactsTree.Visible(False)
        self.m_layoutIsInitilized = True

    def GetContextHelpID(self):
        return 1008
    
    
    def AddUser(self, child, childIcon, obj):
        child.Icon(childIcon, childIcon)
        child.Label(obj.Name(), 0)
        child.SetData(obj)

    def AddContact(self, child, childIcon, obj):
        child.Icon(childIcon, childIcon)
        child.Label(obj.Name(), 0)
        child.Label(obj.Party().Name(), 1)
        child.SetData(obj)
    
    def AddLinkedObjectTreeNode(self, root, obj, childIcon) :
        shouldAdd = True
        children = root.Children() 
        
        if children:
            for childNode in children :
                if childNode.GetData() == obj :
                    shouldAdd = False
                    break        
    
        if shouldAdd :
            child = root.AddChild()
            if obj.IsKindOf(acm.FUser):
                self.AddUser(child, childIcon, obj)
            elif obj.IsKindOf(acm.FContact):
                self.AddContact(child, childIcon, obj)

    def Populate(self, tree, collection, icon = None) :
        tree.RemoveAllItems()
        root = tree.GetRootItem() 
    
        for obj in collection :
            childIcon = icon
            if not childIcon:
                childIcon = obj.Icon()

            self.AddLinkedObjectTreeNode(root, obj, childIcon)

    def AddCustomTreeContextItemsCB(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        commandCB = ud

        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commandCB()))
       
    def OnTreeContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        treeCtrl = ud[0]
        commandCB = ud[1]

        item = treeCtrl.GetSelectedItem()

        if item :
            obj = item.GetData()
            if hasattr(obj, 'Class') :
                acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, [obj], False, self.AddCustomTreeContextItemsCB, commandCB)
            else:
                menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commandCB))


    def SetPersonData(self, person) :
        if person :
            self.m_objectsToCommit = {}

            self.m_firstNameInput.SetData(person.FirstName())
            self.m_lastNameInput.SetData(person.LastName())
            self.m_dateOfBirthInput.SetData(person.DateOfBirth())
            self.m_nationalIdInput.SetData(person.NationalId())
            self.m_exchangeIdInput.SetData(person.ExchangeId())
            self.m_crmID.SetData(person.CrmId()) 

            self.Populate(self.m_userTree, person.Users())
            self.Populate(self.m_contactsTree, person.Contacts(), 'FriendUser')

            if self.m_person :
                self.m_person.RemoveDependent(self)

            self.m_person.AddDependent(self)

            self.m_person = person
            self.m_personClone = self.m_person.Clone()
            self.AddObjectToMostRecentlyUsedList(person)
            self.SetCaption()
            
    def GetPersonData(self, person):
        if person :
            person.FirstName(self.m_firstNameInput.GetData())
            person.LastName(self.m_lastNameInput.GetData())
            person.DateOfBirth(self.m_dateOfBirthInput.GetData())
            person.NationalId(self.m_nationalIdInput.GetData())
            person.ExchangeId(self.m_exchangeIdInput.GetData())
            person.CrmId(self.m_crmID.GetData()) 


    def HandleCreate( self, creationInfo ):
        self.InitLayout(creationInfo)

        if self.m_person :
            self.SetPersonData(self.m_person)

        self.UpdateControls()

    def IsModified(self) :
        ret = len(self.m_objectsToCommit) > 0;

        if not ret and self.m_personClone :
            person = acm.FPerson()
            self.GetPersonData(person)

            ret = ret or not self.m_personClone.FirstName() == person.FirstName()
            ret = ret or not self.m_personClone.LastName() == person.LastName()
            ret = ret or not self.m_personClone.DateOfBirth() == person.DateOfBirth()
            ret = ret or not self.m_personClone.NationalId() == person.NationalId()
            ret = ret or not self.m_personClone.ExchangeId() == person.ExchangeId()
            ret = ret or not self.m_personClone.CrmId() == person.CrmId()

        return ret;

    def VerifyCloseSetup(self, text) :
        close = True

        if self.m_layoutIsInitilized and self.IsModified():
            ret = acm.UX().Dialogs().MessageBoxYesNoCancel(self.Shell(), 'Information', text)

            if ret == 'Button1' :
                self.OnFileSave()
                close = True

            if ret == 'Button2' :
                close = True

            if ret == 'Button3' :
                close = False

        if close and self.m_person :
            self.m_person.RemoveDependent(self)

        return close

    def HandleClose(self):
        return self.VerifyCloseSetup('Do you want to save before closing?')

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        if self.m_serverUpdateEnabled :
            update = True
            if self.IsModified():
                ret = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Information', 'The current person has been modified, do you want to accept the changes?')

                update = ret == 'Button1'

            if update :
                self.SetPersonData(self.m_person)


    def SetCaption(self):
        if self.m_person:
            caption = self.m_person.StringKey()
            if caption == ', ' :
                caption = ''

            self.SetContentCaption(caption)
    
    def DoChangeCreateParameters( self, createParams ):
        createParams.UseSplitter(True)
        createParams.SplitHorizontal(False)
        createParams.LimitMinSize(True)
        createParams.AdjustPanesWhenResizing(True)
        createParams.ShowMostRecentlyUsedList(True)
        
    def HandleCreateStatusBar(self, sb):
        self.m_statusBarTextPane = sb.AddTextPane(100)
        self.m_statusBarIconPane = sb.AddIconPane()
        self.m_statusBarProgressPane = sb.AddProgressPane(100)

    def HandleSaveLayout(self, contents):
        contents.AtPut(s_userPaneVisibleKey, self.m_userTree.Visible())
        contents.AtPut(s_contactsPaneVisibleKey, self.m_contactsTree.Visible())

    def HandleLoadLayout(self, contents):
        if contents :
            if contents.HasKey(s_userPaneVisibleKey) :
                self.m_userTree.Visible( contents.At(s_userPaneVisibleKey))
            if contents.HasKey(s_contactsPaneVisibleKey) :
                self.m_contactsTree.Visible( contents.At(s_contactsPaneVisibleKey))
