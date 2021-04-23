from __future__ import print_function

import acm
import FUxCore
import ChoiceListAddEditDialog

def StartApplication(eii) :
    acm.UX().SessionManager().StartApplication('Choice List Editor', None)

class ChoiceListCommand(FUxCore.MenuItem):
    def __init__(self, parent, invokeCB, enabledCB = None, applicableCB = None, userData = None):
        self.m_parent = parent
        self.m_invokeCB = invokeCB
        self.m_enabledCB = enabledCB
        self.m_applicableCB = applicableCB
        self.m_userData = userData

    def Invoke(self, cd):
        if self.m_userData != None:
            self.m_invokeCB(self.m_userData)
        else :
            self.m_invokeCB()
    
    def Checked(self):
        return False
        
    def Enabled(self):
        return self.m_enabledCB(self.m_userData) if self.m_enabledCB else True
    
    def Applicable(self):
        return self.m_applicableCB(self.m_userData) if self.m_applicableCB else True

class CaseInsensitiveSet(set):
    def add(self, item):
         try:
             set.add(self, item.lower())
         except Exception:                # not a string
             set.add(self, item)

    def remove(self, item):
         try:
             set.remove(self, item.lower())
         except Exception:                # not a string
             set.remove(self, item)

    def __contains__(self, item):
        try:
            return set.__contains__(self, item.lower())
        except Exception:
            return set.__contains__(self, item)

class MoveDirection :
    Up = 'Up'
    Down = 'Down'

class ChoiceListType :
    Parent = 'Parent'
    Child = 'Child'

class ChangedType:
    Added = 'Added'
    Removed = 'Removed'
    Updated = 'Updated'

class ControlType:
    Add = 'Add'
    Update = 'Update'
    Remove = 'Remove'
    Extra = 'Extra'
    Name = 'Name'
    Description = 'Description'

class ChoiceItem:
    def __init__(self, choice, updateItemCB, deleteChoiceItemCB, choiceListType, item = None) :
        self.m_choice = choice
        self.m_matchString = ''
        self.m_item = item
        self.m_updateItemCB = updateItemCB
        self.m_deleteChoiceItemCB = deleteChoiceItemCB
        self.m_choiceListType = choiceListType
        self.UpdateMatchString()
        choice.AddDependent(self)

    def UpdateMatchString(self) :
        s = self.m_choice.Name() + ' ' + self.m_choice.Description()
        self.m_matchString = s.lower()

    def Choice(self) :
        return self.m_choice

    def SetChoice(self, choice) :
        self.CleanUp()
        self.m_choice = choice

    def SetItem(self, item) :
        self.m_item = item
    
    def Item(self) :
        return self.m_item

    def ChoiceListType(self) :
        return self.m_choiceListType

    def Match(self, filter) :
        ret = True
    
        if filter :
            filter = filter.split(' ')
            for f in filter :
                if not f in self.m_matchString :
                    ret = False
                    break
        return ret

    def CleanUp(self) :
        if self.m_choice :
            self.m_choice.RemoveDependent(self)


    def UpdateAsync(self, ud) :
        self.UpdateMatchString()
        if self.m_updateItemCB and self.m_item:
            self.m_updateItemCB(self.m_item, self.Choice(), self, self.ChoiceListType())

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        aspectSymbol = str(aspectSymbol)
        if aspectSymbol == 'update':
            acm.AsynchronousCall(self.UpdateAsync, [None])

class ChoiceListApplication(FUxCore.HostedObjectLayoutApplication):
    def __init__(self):
        FUxCore.HostedObjectLayoutApplication.__init__(self)

        self.m_choiceListControls = {}

        self.m_filterParents = None

        self.m_controls = {}
        self.m_controls[ChoiceListType.Parent] = {}
        self.m_controls[ChoiceListType.Child] = {}

        self.m_sortChildren = None
        self.m_moveUp = None
        self.m_moveDown = None

        self.m_changedChoiceLists = {}

        self.m_changedChoiceLists[ChangedType.Added] = set()
        self.m_changedChoiceLists[ChangedType.Removed] = set()
        self.m_changedChoiceLists[ChangedType.Updated] = set() 

        self.m_names = {}

        self.m_names[ChoiceListType.Parent] = CaseInsensitiveSet()
        self.m_names[ChoiceListType.Child] = CaseInsensitiveSet()

        self.m_choiceItems = {}

        self.m_showControls = {}

        self.m_choiceItems[ChoiceListType.Parent] = []
        self.m_choiceItems[ChoiceListType.Child] = []

        self.m_controlsVisible = {}

        self.m_controlsVisible[ChoiceListType.Parent] = False
        self.m_controlsVisible[ChoiceListType.Child] = False

        self.m_serverUpdateEnabled = True
        self.m_allChoices = None
        self.m_linkWidth = 90
        self.m_extraSpace = 7
        self.m_populating = False

        self.m_modifedChoiceListChildren = {}

        self.m_initialContents = None

        self.m_icon = {}
        self.m_icon[ChoiceListType.Parent] = 'AdjustJournals+OpenOverlay'
        self.m_icon[ChoiceListType.Child] = 'AdjustJournals'

    def GetContextHelpID(self):
        return 46008

    def HandleCreate( self, creationInfo ):
        builder = acm.FUxLayoutBuilder()

        builder.BeginHorzBox()
        builder.    BeginVertBox('Invisible', 'Choice List')
        builder.        AddTree('choiceListParents', 200)
        builder.        AddInput('filterParents', '')
        builder.        AddSpace(self.m_extraSpace)
        builder.        BeginVertBox()
        builder.            AddInput('nameParent', 'Name')
        builder.            AddInput('descriptionParent', 'Description')
        builder.            BeginHorzBox()
        builder.                AddHyperLink('showControlsParent', self.m_linkWidth, self.m_linkWidth)
        builder.                AddFill()
        builder.                AddButton('addParent', 'Add...')
        builder.                AddButton('updateParent', 'Edit...')
        builder.                AddButton('removeParent', 'Remove')
        builder.                AddButton('extraParent', '>', False, True)
        builder.            EndBox()
        builder.        EndBox()
        builder.    EndBox()
        builder.    BeginVertBox('Invisible', 'Choices')
        builder.        AddTree('choiceListChildren', 200)
        builder.        BeginHorzBox()
        builder.            AddFill()
        builder.            AddButton('moveUp', 'Up')
        builder.            AddButton('moveDown', 'Down')
        builder.            AddButton('sortChild', '>', False, True)
        builder.        EndBox()
        builder.        AddSpace(self.m_extraSpace)
        builder.        BeginVertBox()
        builder.            AddInput('nameChild', 'Name')
        builder.            AddInput('descriptionChild', 'Description')
        builder.            BeginHorzBox()
        builder.                AddHyperLink('showControlsChild', self.m_linkWidth, self.m_linkWidth)
        builder.                AddFill()
        builder.                AddButton('addChild', 'Add...')
        builder.                AddButton('updateChild', 'Edit...')
        builder.                AddButton('removeChild', 'Remove')
        builder.                AddButton('extraChild', '>', False, True)
        builder.            EndBox()
        builder.        EndBox()
        builder.    EndBox()
        builder.EndBox()

        layout = creationInfo.AddPane(builder, 'choiceListPane')

        self.m_allChoices = acm.FChoiceList.Select('')
        self.m_allChoices.AddDependent(self)

        self.m_choiceListControls[ChoiceListType.Parent] = layout.GetControl('choiceListParents')
        self.m_choiceListControls[ChoiceListType.Child] = layout.GetControl('choiceListChildren')

        self.m_filterParents = layout.GetControl('filterParents')
        self.m_showControls[ChoiceListType.Parent] = layout.GetControl('showControlsParent')
        self.m_controls[ChoiceListType.Parent][ControlType.Add] = layout.GetControl('addParent')
        self.m_controls[ChoiceListType.Parent][ControlType.Update] = layout.GetControl('updateParent')
        self.m_controls[ChoiceListType.Parent][ControlType.Remove] = layout.GetControl('removeParent')
        self.m_controls[ChoiceListType.Parent][ControlType.Extra] = layout.GetControl('extraParent')
        self.m_controls[ChoiceListType.Parent][ControlType.Name] = layout.GetControl('nameParent')
        self.m_controls[ChoiceListType.Parent][ControlType.Description] = layout.GetControl('descriptionParent')

        self.m_sortChildren = layout.GetControl('sortChild')
        self.m_moveUp = layout.GetControl('moveUp')
        self.m_moveDown = layout.GetControl('moveDown')

        self.m_showControls[ChoiceListType.Child] = layout.GetControl('showControlsChild')
        self.m_controls[ChoiceListType.Child][ControlType.Add] = layout.GetControl('addChild')
        self.m_controls[ChoiceListType.Child][ControlType.Update] = layout.GetControl('updateChild')
        self.m_controls[ChoiceListType.Child][ControlType.Remove] = layout.GetControl('removeChild')
        self.m_controls[ChoiceListType.Child][ControlType.Extra] = layout.GetControl('extraChild')
        self.m_controls[ChoiceListType.Child][ControlType.Name] = layout.GetControl('nameChild')
        self.m_controls[ChoiceListType.Child][ControlType.Description] = layout.GetControl('descriptionChild')

        self.m_choiceListControls[ChoiceListType.Parent].ShowColumnHeaders(True)
        self.m_choiceListControls[ChoiceListType.Parent].ColumnLabel(0, 'Name')
        self.m_choiceListControls[ChoiceListType.Parent].ColumnWidth(0, 200)
        self.m_choiceListControls[ChoiceListType.Parent].AddColumn('Description', 200)
        self.m_choiceListControls[ChoiceListType.Parent].AddColumn('Enum Name', 200)
        self.m_choiceListControls[ChoiceListType.Parent].ColumnWidth(0, 250)
        self.m_choiceListControls[ChoiceListType.Parent].ShowHierarchyLines(False)
        #self.m_choiceListControls[ChoiceListType.Parent].EnableHeaderSorting(True)

        self.m_choiceListControls[ChoiceListType.Child].ShowColumnHeaders(True)
        self.m_choiceListControls[ChoiceListType.Child].ColumnLabel(0, 'Name')
        self.m_choiceListControls[ChoiceListType.Child].ColumnWidth(0, 200)
        self.m_choiceListControls[ChoiceListType.Child].AddColumn('Description', 200)
        self.m_choiceListControls[ChoiceListType.Child].ColumnWidth(0, 250)
        self.m_choiceListControls[ChoiceListType.Child].EnableMultiSelect(True)
        self.m_choiceListControls[ChoiceListType.Child].ShowHierarchyLines(False)

        self.m_filterParents.AddCallback('Changed', self.OnFilterParents, None)

        self.m_sortChildren.AddCallback('Activate', self.OnSortChildren, None)
        self.m_moveUp.AddCallback('Activate', self.OnMove, MoveDirection.Up)
        self.m_moveDown.AddCallback('Activate', self.OnMove, MoveDirection.Down)

        for choiceListType in self.m_choiceListControls.keys() :
            self.m_choiceListControls[choiceListType].AddCallback('ContextMenu', self.OnListContextMenu, choiceListType )
            self.m_choiceListControls[choiceListType].AddCallback('SelectionChanged', self.OnChoiceListSelectionChanged, choiceListType )
            self.m_choiceListControls[choiceListType].AddCallback('DefaultAction', self.OnUpdate, choiceListType)

            self.m_showControls[choiceListType].AddCallback('Activate', self.ShowControls, choiceListType)
            self.m_showControls[choiceListType].SetData('Show input fields')
            self.m_controls[choiceListType][ControlType.Add].AddCallback('Activate', self.OnAdd, choiceListType)
            self.m_controls[choiceListType][ControlType.Update].AddCallback('Activate', self.OnUpdate, choiceListType)
            self.m_controls[choiceListType][ControlType.Remove].AddCallback('Activate', self.OnRemove, choiceListType)
            self.m_controls[choiceListType][ControlType.Extra].AddCallback('Activate', self.OnExtra, choiceListType)
            self.m_controls[choiceListType][ControlType.Name].AddCallback('Changed', self.OnNameChanged, choiceListType)

        for controls in self.m_controls.values() :
            for controlType, control in controls.iteritems() :
                if controlType == ControlType.Name or controlType == ControlType.Description:
                    control.Visible(False)

        self.CreateChoiceItems()
        self.PopulateParents(True, self.m_initialContents)
        self.UpdateControls()
        
        

    def ShowControls(self, choiceListType, cd) :
        visible = not self.m_controlsVisible[choiceListType]
        for controlType, control in self.m_controls[choiceListType].iteritems() :
            if controlType == ControlType.Name or controlType == ControlType.Description:
                control.Visible(visible)

            if controlType == ControlType.Update :
                control.Label('Update' if visible else 'Edit...')

            if controlType == ControlType.Add :
                control.Label('Add' if visible else 'Add...')

        self.m_controlsVisible[choiceListType] = visible
        self.m_showControls[choiceListType].SetData('Hide input fields' if visible else 'Show input fields')

        self.UpdateControls()

    def AddUpdateEnabled(self, choiceListType) :
        selectedItem = self.m_choiceListControls[choiceListType].GetSelectedItem()
        selectedItems = self.m_choiceListControls[choiceListType].GetSelectedItems()
        oldName = selectedItem.GetData().Choice().Name() if selectedItem else ''
        newName = self.m_controls[choiceListType][ControlType.Name].GetData()

        addEnabled = len(newName) and not newName in self.m_names[choiceListType] or not self.m_controlsVisible[choiceListType]
        if choiceListType == ChoiceListType.Child :
            addEnabled = addEnabled and self.m_choiceListControls[ChoiceListType.Parent].GetSelectedItem() != None

        updateEnabled = selectedItem != None and len(selectedItems) == 1 and len(newName) and (not newName in self.m_names[choiceListType] or newName == oldName)

        return addEnabled, updateEnabled

    def UpdateControls(self) :
        for choiceListType in self.m_choiceListControls.keys() :
            addEnabled, updateEnabled = self.AddUpdateEnabled(choiceListType)              

            self.m_controls[choiceListType][ControlType.Add].Enabled(addEnabled)
            self.m_controls[choiceListType][ControlType.Update].Enabled(updateEnabled)
            self.m_controls[choiceListType][ControlType.Extra].Enabled(updateEnabled)

    
        selectedChildItem = self.m_choiceListControls[ChoiceListType.Child].GetSelectedItem()
        selectedParentItem = self.m_choiceListControls[ChoiceListType.Parent].GetSelectedItem()
        selectedChildItems = self.m_choiceListControls[ChoiceListType.Child].GetSelectedItems()

        self.m_controls[ChoiceListType.Parent][ControlType.Remove].Enabled(selectedParentItem != None)

        self.m_sortChildren.Enabled(self.m_choiceItems[ChoiceListType.Child] != None and len(self.m_choiceItems[ChoiceListType.Child]) > 0)
        self.m_moveUp.Enabled(selectedChildItem != None and selectedChildItem.Sibling(False) != None)
        self.m_moveDown.Enabled(selectedChildItem != None and selectedChildItem.Sibling(True) != None)

        self.m_controls[ChoiceListType.Child][ControlType.Remove].Enabled(selectedChildItem != None)
        self.m_controls[ChoiceListType.Child][ControlType.Name].Enabled(selectedParentItem != None)
        self.m_controls[ChoiceListType.Child][ControlType.Description].Enabled(selectedParentItem != None)
        

    def OnFilterParents(self, ud, cd):
        self.FilterParents()
        #if not self.m_populating :
        #    self.Shell().CallAsynch(self.PopulateAsync, {'ChoiceListType' : ChoiceListType.Parent, 'Select':True})
        #    self.m_populating = True

    def OnAdd(self, choiceListType, cd = None):
        choice = acm.FChoiceList()
        names = self.m_names[choiceListType]
        choiceItemParent = None
        if choiceListType == ChoiceListType.Parent :
            choice.List('MASTER')
        else:
            item = self.m_choiceListControls[ChoiceListType.Parent].GetSelectedItem()
            choiceItemParent = item.GetData()
            choice.List(choiceItemParent.Choice().Name())
        
            
        if choice:
            if self.m_controlsVisible[choiceListType]:
                choice.Name(self.m_controls[choiceListType][ControlType.Name].GetData())            
                choice.Description(self.m_controls[choiceListType][ControlType.Description].GetData())
            else :
                choice = ChoiceListAddEditDialog.Show(self.Shell(),  'Add Choice List' if choiceListType == ChoiceListType.Parent else 'Add Choice', choice, self.m_names[choiceListType]) 
            
            if choice :
                item = None
                self.m_changedChoiceLists[ChangedType.Added].add(choice)
                choiceItem = ChoiceItem(choice, self.UpdateListItemFromChoiceList, self.DeleteChoiceItem, choiceListType)
                self.m_choiceItems[choiceListType].append(choiceItem)
                names.add(choice.Name())

                if choiceListType == ChoiceListType.Child:
                    self.m_choiceListControls[ChoiceListType.Child].DeselectAllItems()
                    item = self.m_choiceListControls[ChoiceListType.Child].GetRootItem().AddChild()
                    choiceItem.SetItem(item)
                    self.UpdateListItemFromChoiceList(item, choice, choiceItem, choiceListType)
                    self.UpdateChoiceListChildSortOrder()
                else:
                    self.m_choiceItems[choiceListType].sort(key=lambda x : x.Choice().Name())
                    self.PopulateParents()
                    item = choiceItem.Item()
                    
                if item :
                    item.Select()
                    item.EnsureVisible()


    def DeleteChoiceItem(self, choiceItem):
        if self.m_serverUpdateEnabled :
            self.m_choiceItems[choiceItem.ChoiceListType()].remove(choiceItem)
            choiceItem.CleanUp()
            for type, changedChoices in self.m_changedChoiceLists.iteritems() :
                if choiceItem.Choice() in changedChoices :
                    changedChoices.remove(choiceItem.Choice())

            if choiceItem.Item() :
                choiceItem.Item().Remove()
                choiceItem.SetItem(None)

    def OnUpdate(self, choiceListType, cd = None):
        names = self.m_names[choiceListType]
        item = self.m_choiceListControls[choiceListType].GetSelectedItem()

        if item:
            choiceItem = item.GetData()
            originalChoice = choiceItem.Choice()
            choice = originalChoice if originalChoice.IsInfant() else originalChoice.Clone()
            choiceItem.SetChoice(choice)
            oldName = choice.Name()

            if self.m_controlsVisible[choiceListType]:
                choice.Name(self.m_controls[choiceListType][ControlType.Name].GetData())            
                choice.Description(self.m_controls[choiceListType][ControlType.Description].GetData())
            else :
                choice = ChoiceListAddEditDialog.Show(self.Shell(),  'Edit Choice List' if choiceListType == ChoiceListType.Parent else 'Edit Choice', choice, self.m_names[choiceListType]) 

            if choice :
                names.remove(oldName)
                self.UpdateListItemFromChoiceList(item, choice, choiceItem, choiceListType)
                names.add(choice.Name())
                if not originalChoice.IsInfant() : #it's an added choice, no need to add to updated list
                    self.m_changedChoiceLists[ChangedType.Updated].add(choice)

                if choiceListType == ChoiceListType.Parent :
                    choices = self.GetChoices(choiceItem)
                    for childChoice in choices :
                        cloneChildChoice = childChoice if childChoice.IsInfant() else childChoice.Clone()
                        cloneChildChoice.List(choice.Name)
                        if not choice.IsInfant() : #it's an added choice, no need to add to updated list
                            self.m_changedChoiceLists[ChangedType.Updated].add(cloneChildChoice)

                self.UpdateControls()
                    
    def OnRemove(self, choiceListType, cd = None):
        list = self.m_choiceListControls[choiceListType]
        items = list.GetSelectedItems()

        if items :
            count = len(items)
            postMessage = 'choice list?' 
            if choiceListType == ChoiceListType.Child:
                postMessage = 'choices?' if count > 1 else 'choice?'

            message = 'Are you sure you want to remove the selected ' + postMessage
            ret = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Question', message, 'Delete choice list')
            itemsToRemove = []
            if ret == 'Button1':
                for item in items :
                    choiceItem = item.GetData()
                    choice = choiceItem.Choice()

                    if choice in self.m_changedChoiceLists[ChangedType.Updated] :
                        self.m_changedChoiceLists[ChangedType.Updated].remove(choice) # if updated we need to remove it from that list
                    if choice in self.m_changedChoiceLists[ChangedType.Added] :
                        self.m_changedChoiceLists[ChangedType.Added].remove(choice)
                    else:
                        if choice.Original() :
                            choice = choice.Original()

                        self.m_changedChoiceLists[ChangedType.Removed].add(choice)
   
                    self.m_choiceItems[choiceListType].remove(choiceItem)

                    choiceItem.CleanUp()
                    choiceItem.SetItem(None)

                    if choice.Name() in self.m_names[choiceListType] :
                        self.m_names[choiceListType].remove(choice.Name())

                    itemsToRemove.append(item)
                    if choiceListType == ChoiceListType.Parent :
                        for childChoiceItems in self.m_choiceItems[ChoiceListType.Child] :
                            childChoiceItems.CleanUp()
                            childChoiceItems.SetItem(None)
                        self.m_choiceItems[ChoiceListType.Child] = []

                        choices = self.GetChoices(choiceItem)
                        for childChoice in choices :
                            if childChoice in self.m_changedChoiceLists[ChangedType.Updated] :
                                self.m_changedChoiceLists[ChangedType.Updated].remove(childChoice) # if updated we need to remove it from that list
                            if childChoice in self.m_changedChoiceLists[ChangedType.Added] :
                                self.m_changedChoiceLists[ChangedType.Added].remove(childChoice)
                            else:
                                if childChoice.Original() :
                                    childChoice = childChoice.Original()
                                self.m_changedChoiceLists[ChangedType.Removed].add(childChoice)
                            

                for item in itemsToRemove :
                    item.Remove()

                if choiceListType == ChoiceListType.Child :
                    self.UpdateChoiceListChildSortOrder()

    def OnProtection(self, choiceListType) :
        item = self.m_choiceListControls[choiceListType].GetSelectedItem()
        if item :
            choiceItem = item.GetData()
            choiceClone = choiceItem.Choice().Clone()

            if acm.UX().Dialogs().Protection(self.Shell(), choiceClone) :
                self.m_changedChoiceLists[ChangedType.Updated].add(choiceClone)
                choiceItem.SetChoice(choiceClone)

    def OnAddInfo(self, choiceListType) :
        item = self.m_choiceListControls[choiceListType].GetSelectedItem()
        if item :
            choiceItem = item.GetData()
            choice= choiceItem.Choice()

            acm.UX().Dialogs().EditAdditionalInfo(self.Shell(), choice)

    def OnExtra(self, choiceListType, cd):
        menu = acm.FUxMenu()

        protectionIsImplementd = hasattr(acm.UX().Dialogs(), 'Protection')

        menu.AddItem( self.OnProtection, choiceListType, "Protection...", 'P', protectionIsImplementd )

        hasChoiceListSpec =  len(acm.FAdditionalInfoSpec.Select('recType = ChoiceList')) > 0
        menu.AddItem( self.OnAddInfo, choiceListType, "Add Info...", 'I', hasChoiceListSpec )

        menu.Track(self.m_controls[choiceListType][ControlType.Extra])


    def OnSort(self, direction):
        parentChoiceItem = self.m_choiceListControls[ChoiceListType.Parent].GetSelectedItem().GetData()
        children = self.m_choiceListControls[ChoiceListType.Child].GetRootItem().Children()
        choices = []

        for child in children :
            choices.append(child.GetData().Choice())

        choices.sort(key=lambda x : x.Name(), reverse=direction == MoveDirection.Down)
        self.m_modifedChoiceListChildren[parentChoiceItem] = choices
        self.PopulateChildren(parentChoiceItem, True)
        self.UpdateChoiceListChildSortOrder()
        self.UpdateControls()

    def OnSortChildren(self, ud, cd):
        menu = acm.FUxMenu()

        menu.AddItem( self.OnSort, MoveDirection.Up, "Sort Ascending", 'A')
        menu.AddItem( self.OnSort, MoveDirection.Down, "Sort Descending", 'D')

        menu.Track(self.m_sortChildren)


    def OnNameChanged(self, choiceListType, cd):
        self.UpdateControls()

    def OnMove(self, moveDirection, cd):
        currentItem = self.m_choiceListControls[ChoiceListType.Child].GetSelectedItem()
        choiceItem = currentItem.GetData()
        choice = choiceItem.Choice()

        newSibling = currentItem.Sibling(moveDirection == MoveDirection.Down)
        if newSibling:
            if moveDirection == MoveDirection.Up :
                newSibling = newSibling.Sibling(False)
            
            newItem = None
            if newSibling :
                newItem = self.m_choiceListControls[ChoiceListType.Child].InsertItemAfter(newSibling)
            else :
                newItem = self.m_choiceListControls[ChoiceListType.Child].GetRootItem().AddChild(False)

            self.UpdateListItemFromChoiceList(newItem, choice, choiceItem, ChoiceListType.Child)

            currentItem.Remove()
            self.m_choiceListControls[ChoiceListType.Child].DeselectAllItems()
            newItem.Select()

        self.UpdateChoiceListChildSortOrder()

    def UpdateChoiceListChildSortOrder(self) :
        choiceItemParent = self.m_choiceListControls[ChoiceListType.Parent].GetSelectedItem().GetData()

        children = self.m_choiceListControls[ChoiceListType.Child].GetRootItem().Children()
        choices = []    
        for index, child in enumerate(children) :
            choiceItem = child.GetData()
            choice = choiceItem.Choice()
            if not choice.IsClone() and not choice.IsInfant():
                choice = choice.Clone()
                choiceItem.SetChoice(choice)

            choice.SortOrder(index)
            self.m_changedChoiceLists[ChangedType.Updated].add(choice)
            choices.append(choice)

        self.m_modifedChoiceListChildren[choiceItemParent] = choices

    def OnChoiceListSelectionChanged(self, choiceListType, cd):
        item = self.m_choiceListControls[choiceListType].GetSelectedItem() 
        choice = None
        choiceItem = None

        if item :
            choiceItem = item.GetData()
            choice = choiceItem.Choice()

            self.m_controls[choiceListType][ControlType.Name].SetData(choice.Name())
            self.m_controls[choiceListType][ControlType.Description].SetData(choice.Description())
        else:
            self.m_controls[choiceListType][ControlType.Name].SetData('')
            self.m_controls[choiceListType][ControlType.Description].SetData('')

        if choiceListType == ChoiceListType.Parent :
            self.PopulateChildren(choiceItem, True)


        self.UpdateControls()

    
    def GetRootChoice(self) :
        rootChoices = acm.FChoiceList.Select('name="MASTER" and list="MASTER"')
        rootChoice = None
        if rootChoices :
            rootChoice = rootChoices.At(0)

        return rootChoice

    def CreateChoiceItems(self) :
        self.m_names[ChoiceListType.Parent] = CaseInsensitiveSet()
        rootChoice = self.GetRootChoice()
        if rootChoice :    
            choices = rootChoice.Choices()
            parentChoiceItems = []
            if choices :
                choices = choices.SortByProperty('Name')
                for choice in choices :
                    parentChoiceItems.append(ChoiceItem(choice, self.UpdateListItemFromChoiceList, self.DeleteChoiceItem, ChoiceListType.Parent))
                    self.m_names[ChoiceListType.Parent].add(choice.Name())

                self.m_choiceItems[ChoiceListType.Parent] = parentChoiceItems

    def GetValueWithDefault(self, dict, key, defaultValue):
        value = dict.At(key)

        if value == None:
            value = defaultValue

        return value

    def PopulateAsync(self, params) :   
        choiceListType = self.GetValueWithDefault(params, 'ChoiceListType', ChoiceListType.Parent)
        select = self.GetValueWithDefault(params, 'Select', False)

        if choiceListType == ChoiceListType.Parent:
            self.PopulateParents(select)
        else :
            item = self.m_choiceListControls[ChoiceListType.Parent].GetSelectedItem() 
    
            if item :
                parentChoiceItem = item.GetData()
                self.PopulateChildren(parentChoiceItem, select)

        self.m_populating = False

    def FilterParents(self) :
        children = self.m_choiceListControls[ChoiceListType.Parent].GetRootItem().Children()
        filter = self.m_filterParents.GetData()
        filter = filter.lower() if filter else ''
        selectedChoiceItem = None
        for child in children :
            choiceItem = child.GetData()
            visible = choiceItem.Match(filter)
            child.Visible(visible)

            if not selectedChoiceItem and visible :
                child.Select()
                selectedChoiceItem = choiceItem

        self.PopulateChildren(selectedChoiceItem, True)        
        self.UpdateControls()

    def PopulateParents(self, select = False, initialContents = None) :
        rootChoice = self.GetRootChoice()

        if rootChoice:
            self.m_choiceListControls[ChoiceListType.Parent].RemoveAllItems()
            filter = self.m_filterParents.GetData()
            filter = filter.lower() if filter else ''

            rootNode = self.m_choiceListControls[ChoiceListType.Parent].GetRootItem()
            addedAtLeastOne = False
            for choiceItem in self.m_choiceItems[ChoiceListType.Parent] :
                choiceItem.SetItem(None)
                choice = choiceItem.Choice()
                name = choice.Name()
                if choiceItem.Match(filter):
                    if choice != rootChoice :
                        child = rootNode.AddChild()
                        choiceItem.SetItem(child)
                        child.Label(name, 0)
                        child.Label(choice.Description(), 1)
                        child.Label(choice.EnumName(), 2)

                        child.SetData(choiceItem)
                        child.Icon(self.m_icon[ChoiceListType.Parent], self.m_icon[ChoiceListType.Parent])

                        addedAtLeastOne = True
                        if initialContents == choice :
                            child.Select()
                            initialContents = None
                            select = False

                        if select : 
                            child.Select()
                            select = False

            if not addedAtLeastOne :
                self.PopulateChildren(None)                    

    def UpdateListItemFromChoiceList(self, child, choice, choiceItem, choiceListType) :
        child.Label(choice.Name(), 0)
        child.Label(choice.Description(), 1)

        choiceItem.SetChoice(choice)
        child.SetData(choiceItem)
        child.Icon(self.m_icon[choiceListType], self.m_icon[choiceListType])

    def GetChoices(self, parentChoiceItem) :
        parentChoice = parentChoiceItem.Choice()

        choices = self.m_modifedChoiceListChildren.get(parentChoiceItem, None)
        if choices == None:
            choices = parentChoice.ChoicesSorted()

        return choices

    def PopulateChildren(self, parentChoiceItem, select = False) :
        self.m_choiceListControls[ChoiceListType.Child].RemoveAllItems()
        self.m_names[ChoiceListType.Child] = CaseInsensitiveSet()
        childrenChoiceItems = []
        self.m_controls[ChoiceListType.Child][ControlType.Name].SetData('')
        self.m_controls[ChoiceListType.Child][ControlType.Description].SetData('')


        if parentChoiceItem :
            parentChoice = parentChoiceItem.Choice()
            root = self.m_choiceListControls[ChoiceListType.Child].GetRootItem()

            choices = self.GetChoices(parentChoiceItem)

            for choiceItem in self.m_choiceItems[ChoiceListType.Child]:
                choiceItem.CleanUp()

            if choices :
                for choice in choices :
                    self.m_names[ChoiceListType.Child].add(choice.Name())
                    if choice != parentChoice :
                        child = root.AddChild()
                        choiceItem = ChoiceItem(choice, self.UpdateListItemFromChoiceList, self.DeleteChoiceItem, ChoiceListType.Child, child)
                        childrenChoiceItems.append(choiceItem)
                        self.UpdateListItemFromChoiceList(child, choice, choiceItem, ChoiceListType.Child)         
                        if select : 
                            child.Select()
                            select = False
   

        self.m_choiceItems[ChoiceListType.Child] = childrenChoiceItems

            

    def OnAddCB(self, choiceListType) :
        self.OnAdd(choiceListType)

    def OnAddEnabledCB(self, choiceListType) :
        addEnabled, updateEnabled = self.AddUpdateEnabled(choiceListType)
        return addEnabled

    def OnAddApplicable(self, choiceListType):
        return self.m_controls[choiceListType][ControlType.Add].Visible()

    def OnUpdateCB(self, choiceListType) :
        self.OnUpdate(choiceListType)

    def OnUpdateApplicable(self, choiceListType):
        return self.m_controls[choiceListType][ControlType.Add].Visible()

    def OnUpdateEnabledCB(self, choiceListType) :
        addEnabled, updateEnabled = self.AddUpdateEnabled(choiceListType)

        return updateEnabled


    def OnRemoveCB(self, choiceListType) :
        self.OnRemove(choiceListType)

    def OnRemoveEnabledCB(self, choiceListType) :
        return self.m_choiceListControls[choiceListType].GetSelectedItem() != None

    def AddCommand(self, name, path, description, shortcut, mnemonic, invokeCB, enabledCB, applicableCB, userData) :
        command = []

        command.append(name)
        command.append('View')
        command.append(path)
        command.append(description)
        command.append(shortcut)
        command.append(mnemonic)
        command.append(lambda a0 = self, a1 = invokeCB, a2 = enabledCB, a3 = applicableCB, a4 = userData : ChoiceListCommand(a0, a1, a2, a3, a4))
        command.append(False)

        return command

    def Commands(self, choiceListType) :
        commands = []

        commands.append(self.AddCommand('addChoiceList', 'Add', 'Add a new choice list', 'Ctrl+D', 'A', self.OnAddCB, self.OnAddEnabledCB, self.OnAddApplicable, choiceListType))
        commands.append(self.AddCommand('updateChoiceList', 'Update', 'Update the selected choice list', 'Ctrl+E', 'E', self.OnUpdateCB, self.OnUpdateEnabledCB, self.OnUpdateApplicable, choiceListType))
        commands.append(FUxCore.Separator())
        commands.append(self.AddCommand('RemoveChoiceList', 'Remove', 'Remove the selected choice list', 'Ctrl+R', 'R',  self.OnRemoveCB, self.OnRemoveEnabledCB, None, choiceListType))


        return commands

    def AddCustomListContextItemsCB(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(self.Commands(ud)))

    def OnListContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        item = cd.At('items')
        choice = None
        if item :
            item = item[0]
            choiceItem = item.GetData()
            choice = choiceItem.Choice()

        acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, [choice], False, self.AddCustomListContextItemsCB, ud)


    def HandleObject(self, contents):
        self.m_initialContents = contents

    def CleanUp(self) :
        self.m_allChoices.RemoveDependent(self)
        for choiceItems in self.m_choiceItems.values() :
            for choiceItem in choiceItems :
                choiceItem.CleanUp()        

    def HandleClose(self):
        if self.HandleHasChanged() :
            text = 'There are unsaved changed, do you want to save these changes?'
            ret = acm.UX().Dialogs().MessageBoxYesNoCancel(self.Shell(), 'Information', text)

            if ret == 'Button1' :
                self.CleanUp()
                return self.HandleCommitChanges()

            if ret == 'Button2' :
                self.CleanUp()
                return True

            if ret == 'Button3' :
                return False


        self.CleanUp()
        return True

    
    def HandleCommitChanges(self):
        ret = True
        try :
            self.m_serverUpdateEnabled = False

            changedChoices = self.m_changedChoiceLists[ChangedType.Removed]
            for choice in changedChoices :
                choice.Delete()
            
            changedChoices = self.m_changedChoiceLists[ChangedType.Added]
            for choice in changedChoices :
                choice.Commit()

            changedChoices = self.m_changedChoiceLists[ChangedType.Updated]
            for choice in changedChoices :
                original = choice.Original()
                if original :
                    if not original.IsDeleted() :
                        original.Apply(choice)
                        original.Commit()
                else :
                    choice.Commit()

        except Exception as e:
            acm.UX().Dialogs().MessageBoxInformation(self.Shell(), e.message, 'Choice List')
            ret = False

        if ret :
            self.m_changedChoiceLists[ChangedType.Added] = set()
            self.m_changedChoiceLists[ChangedType.Removed] = set()
            self.m_changedChoiceLists[ChangedType.Updated] = set()       

            self.m_modifedChoiceListChildren = {}

        self.m_serverUpdateEnabled = True

        return True

    def HandleHasChanged(self):
        hasChanged = False
        
        hasChanged = hasChanged or len(self.m_changedChoiceLists[ChangedType.Added]) > 0
        hasChanged = hasChanged or len(self.m_changedChoiceLists[ChangedType.Updated]) > 0
        hasChanged = hasChanged or len(self.m_changedChoiceLists[ChangedType.Removed]) > 0

        return hasChanged

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        if self.m_serverUpdateEnabled :
            aspectSymbol = str(aspectSymbol)
            choiceListType = ChoiceListType.Parent if parameter.List() == 'MASTER' else ChoiceListType.Child
            if aspectSymbol == 'insert':
                if choiceListType == ChoiceListType.Parent :
                    self.m_choiceItems[choiceListType].append(ChoiceItem(parameter, self.UpdateListItemFromChoiceList, self.DeleteChoiceItem, choiceListType))
                    self.m_choiceItems[choiceListType].sort(key=lambda x : x.Choice().Name())

                if not self.m_populating :
                    self.Shell().CallAsynch(self.PopulateAsync, {'ChoiceListType' : choiceListType})
            elif aspectSymbol == 'remove' :
                for choiceItem in self.m_choiceItems[choiceListType] :
                    if choiceItem.Choice() == parameter :
                        self.Shell().CallAsynch(self.DeleteChoiceItem, choiceItem)
                        break
    
        
def CreateApplicationInstance():
    return ChoiceListApplication()
