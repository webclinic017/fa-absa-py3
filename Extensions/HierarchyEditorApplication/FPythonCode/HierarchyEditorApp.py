from __future__ import print_function
import acm
import FUxCore
import GetShortNameDialog
import CreateHierarchyTypeDialog
import CreateNewHierarchyDialog
import OpenHierarchyDialog
import HierarchyEditorUtils
import SearchHierarchyDialog
import CreateSearchableItemsProgressDialog
import HierarchyApplicationSettingsDialog 

from HierarchyEditorUtils import Settings
from HierarchyEditorUtils import SettingsFromChoice
from HierarchyEditorUtils import ParameterFromName

def CreateApplicationInstance():
    HierarchyEditorUtils.CopyIcon('Tree', 'FHierarchy')
    HierarchyEditorUtils.CopyIcon('Tree', 'FHierarchyType')
    HierarchyEditorUtils.CopyIcon('FreezePane', 'FHierarchyColumnSpecification')

    return HierarchyEditorApplication()
    
def ReallyStartApplication(shell, count):
    acm.UX().SessionManager().StartApplication('Hierarchy Editor', None)

def StartApplication(eii):
    shell = eii.ExtensionObject().Shell()
    ReallyStartApplication(shell, 0);

class RestrictionKeys :
    NoRestrictions = 'None'
    GroupLevelOnly = 'Group Level Only'
    LeafLevelOnly = 'Leaf Level Only'

class DragDropKeys :
    DragObject = acm.FSymbol('DragObjectKey')
    RightDrag = acm.FSymbol('RightDragKey')

class RightDropDataKeys :
    DropObject = acm.FSymbol('DropObjectKey')
    DropType = acm.FSymbol('DropTypeKey')
    DropItem = acm.FSymbol('DropItem')
    DropAction = acm.FSymbol('DropAction')

class RightDropTypes :
    Child = 'Child'
    PreviousSibling = 'PreviousSibling'
    NextSibling = 'NextSibling'

class DropAction :
    Move = 'Move'
    Copy = 'Copy'



class HierarchyDataValue :
    def __init__(self) :
        self.m_hierarchyNode = None

class NodeChildren :
    def __init__(self) :
        self.m_children = []
        self.m_sorted = False

    def AddChildren(self, child) :
        self.m_children.append(child)
        self.m_sorted = False

    def SortedChildren(self) :
        if not self.m_sorted :
            self.Sort()
            
        return self.m_children

    def Sort(self) :
        if self.m_children :
            sortedChildren = []
            childCount = len(self.m_children)
            currPrev = None

            while len(sortedChildren) < childCount:
                found = False

                for child in self.m_children :
                    if child.PreviousSibling() == currPrev :
                        sortedChildren.append(child)
                        self.m_children.remove(child)
                        currPrev = child
                        found = True
                        break

                if not found :
                    print ('Incorrect hierarchy, unable to resolve children')
                    break
                
            if not self.m_children :
                self.m_children = sortedChildren


class HierarchyNode :
    def __init__(self) :
        self.m_displayName = ''
        self.m_parent = None
        self.m_children = []
        self.m_dataValues = []

    def Parent(self, parent) :
        self.m_parent = parent

    def Parent(self) :
        return self.m_parent

    def Children(self) :
        return self.m_children

class MoveDirection :
    Up      = 1
    Down    = 2
    Left    = 3
    Right   = 4


class SearchItem :
    def __init__(self, node, searchString, index, path, displayName) :
        self.m_node = node
        self.m_searchString = searchString
        self.m_index = index
        self.m_path = path
        self.m_displayName = displayName

    def Match(self, query) :
        return query in self.m_searchString

    def MatchAll(self, query) :
        ret = True
        query = query.split(' ')
        for q in query :
            if not self.Match(q) :
                ret = False
                break


        return ret

    def DisplayName(self) :
        return self.m_displayName 
    def Node(self) :
        return self.m_node

    def Index(self) :
        return self.m_index

    def Path(self) :
        return self.m_path

    def PathAsString(self):
        return '/'.join(self.m_path)

class HierarchyNodeCommand(FUxCore.MenuItem):
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


class HierarchyEditorApplication(FUxCore.LayoutApplication):
    def __init__(self):
        FUxCore.LayoutApplication.__init__(self)

        self.m_imageHierarchy = None
        self.m_imageHierarchyTree = None
        self.m_originalHierarchy = None
        self.m_hierarchies = None
        self.m_searchInput = None
        
        self.m_listPane = None
        self.m_binders = None
        self.m_treeCtrl = None
        self.m_columnIndexByColumnDef = {}
        self.m_columnDefByBinder = {}
        self.m_topNode = None
        self.m_hierarchyPersistenDomains = None


        self.m_controlPaneVisible = False
        self.m_lastAspectSymbol = None
        self.m_showWarningOnQueue = False
        self.m_pendingInPlaceEditing = False
        self.m_currentValidValue = None

        self.m_treeItemByHierarchyNode = {}

        self.m_searchableItems = []
        self.m_searchableItemByNode = {}

        self.m_doIncrementalSearch = False
        self.m_doIncrementalSearchOffset = 0

        self.m_searchableItemsNeedsRefresh = True

        self.m_settingsByColumnIndex = {}

        self.m_whiteColor = acm.UX().Colors().Create(255, 255, 255).ColorRef()
        self.m_blackColor = acm.UX().Colors().Create(0, 0, 0).ColorRef()

    def SearchStringFromNode(self, node) :
        searchStrings = self.SearchStringsFromNode(node)
        searchString = ' '.join([s.lower() for s in searchStrings])

        return searchString

    def SearchStringsFromNode(self, node) :
        searchStrings = []
        searchStrings.append(node.DisplayName().lower())

        for dataValue in node.HierarchyDataValues() :
            try :
                value = self.FormatValue(dataValue.HierarchyColumnSpecification().DataDomain(), dataValue.DataValueVA())
                if hasattr(value, 'Name') :
                    value = str(value.Name())
                else:
                    value = str(value)

                searchStrings.append(value)
            except Exception as e:
                print(e)

        return searchStrings

    def DoSearch(self, node, startIndex, query) :
        foundNode = None
        breakAt = startIndex - 1
        if startIndex >= len(self.m_searchableItems) :
            startIndex = 0

        while startIndex != breakAt:
            searchItem = self.m_searchableItems[startIndex]
            if searchItem.Match(query) :
                foundNode = searchItem.Node()
                break

            startIndex += 1
            if startIndex >= len(self.m_searchableItems) :
                startIndex = 0


        if foundNode != node :
            if foundNode :
                self.SelectTreeItemFromNode(foundNode)
            else:
                self.m_treeCtrl.DeselectAllItems()


    def SelectTreeItemFromNode(self, foundNode, clearSelection = True) :
        if clearSelection :
            self.m_treeCtrl.DeselectAllItems()

        path = []
        node = foundNode
        while node :
            path.append(node)
            node = self.m_imageHierarchyTree.Parent(node)

        path.reverse()
        
        item = None
        for node in path :
            item = self.m_treeItemByHierarchyNode[node]
            if node != foundNode and not item.IsExpanded():
                item.Expand()
                   
        if item :
            item.Select()

    def HandleOnIdle(self):
        if self.m_doIncrementalSearch :
            self.m_doIncrementalSearch = False
            if self.CreateSearchableNodesIfNeeded() :
                query = self.m_searchInput.GetData()
                if query :
                    item = self.m_treeCtrl.GetSelectedItem()
                    index = 0

                    if item :
                        if len(self.m_treeCtrl.GetSelectedItems()) == 0 : # weird case but can happen
                            self.m_treeCtrl.GetFirstItem().Select()
                            if self.m_doIncrementalSearchOffset == 0 :
                                self.m_treeCtrl.DeselectAllItems()
                                item.Select()
                            else :
                                item = self.m_treeCtrl.GetFirstItem()

                        node = item.GetData()
                        searchItem = self.m_searchableItemByNode[node]
                        index = searchItem.Index() + self.m_doIncrementalSearchOffset

                    query = query.lower()
                    self.DoSearch(node, index, query)


    def OnSearchInputChanged(self, offset, cd) :
        self.m_doIncrementalSearchOffset = offset
        self.m_doIncrementalSearch = True

    def UpdateSearchItemsSearchString(self, searchItem) :
        rootNode = searchItem.Node()
        displayName = rootNode.DisplayName()
        searchStrings = self.SearchStringsFromNode(rootNode)
        if rootNode.IsLeaf() :
            displayName = searchStrings[1] if len(searchStrings) > 1 else ''

        searchString = ' '.join([s.lower() for s in searchStrings])

        searchItem.m_displayName = displayName
        searchItem.m_searchString = searchString

    def CreateSearchableNodes(self, rootNode, path) :
        if rootNode :
            searchItem = SearchItem(rootNode, '', len(self.m_searchableItems), path, '')

            self.m_searchableItems.append(searchItem)
            self.m_searchableItemByNode[rootNode] = searchItem

            children = self.ChildrenOrdered(rootNode)

            if children :
                for child in children :
                    newPath = list(path)
                    newPath.append(child.DisplayName())
                    self.CreateSearchableNodes(child, newPath)

    def CreateSearchableNodesIfNeeded(self) :
        if self.m_searchableItemsNeedsRefresh :
            self.m_searchableItemByNode = {}
            self.m_searchableItems = []
            rootNode = self.GetCurrentRootNode()
            
            if rootNode :
                path = [rootNode.DisplayName()]
                self.CreateSearchableNodes(rootNode, path)
                if CreateSearchableItemsProgressDialog.Show(self.Shell(), 'Updating hierarchy search index', self.m_searchableItems, self.UpdateSearchItemsSearchString) :
                    self.m_searchableItemsNeedsRefresh = False
        
        return not self.m_searchableItemsNeedsRefresh

    def UpdateSearchItem(self, node):
        searchItem = self.m_searchableItemByNode.get(node)

        if searchItem :
            searchItem.m_searchString = self.SearchStringFromNode(node)
        else :            
            self.m_searchableItemsNeedsRefresh = True

    def GetValidHierachyDataValue(self, value, columnSpecification, uniqueValues = None, currentValue = None) :
        hierarchyDataValue = acm.FHierarchyDataValue()
        hierarchyDataValue.HierarchyColumnSpecification = columnSpecification
        
        if not uniqueValues :
            uniqueValues = self.GetUniqueValuesByColumnSpecIfApplicable(columnSpecification)
        
        if currentValue and uniqueValues and currentValue in uniqueValues:
            uniqueValues.remove(currentValue)

        if value != None:
            hierarchyDataValue.DataValueVA(value)

        dataValue = hierarchyDataValue.DataValue()

        if dataValue in uniqueValues :
            hierarchyDataValue = None

        return hierarchyDataValue, dataValue
    

    def CreateHierarchyDataValue(self, node, columnSpecification, value, uniqueValues, showWarning):
        hierarchyDataValue, dataValue = self.GetValidHierachyDataValue(value, columnSpecification, uniqueValues)

        if not hierarchyDataValue :
            self.ShowUniqueColumnWarningAsync(dataValue, showWarning)
        elif hierarchyDataValue.DataValue() not in [None, '']:
            hierarchyDataValue.HierarchyNode = node
            hierarchyDataValue.RegisterInStorage()

    def SetTreeItemData(self, treeItem, hierarchyNode) :
        treeItem.SetData(hierarchyNode)
        self.m_treeItemByHierarchyNode[hierarchyNode] = treeItem

    def RemoveNodeFromTreeItem(self, item) :
        parent = item.Parent()
        node = item.GetData()

        self.m_treeItemByHierarchyNode.pop(node)
            
        parentNode = self.m_imageHierarchyTree.Parent(node)
        self.m_imageHierarchyTree.Remove(node)

            
        if parent and parentNode:
            if self.m_imageHierarchyTree.Children(parentNode) == None :
                parent.ChildrenCount(0)

    def AddHierarchyNode(self, nodeLabel, parentNode, hierarchyTree, child, isLeaf) :
        hierarchyNode = hierarchyTree.Add(nodeLabel, parentNode)
        hierarchyNode.IsLeaf(isLeaf)
        hierarchyNode.RegisterInStorage()
        

        if child:
            if self.ChildrenOrdered(hierarchyNode):
                child.ChildrenCount(1)
            
            self.SetTreeItemData(child, hierarchyNode)

        return hierarchyNode


    def AddHierarchyNodeToTree(self, hierarchyNode, treeNode) :
        self.SetTreeItemData(treeNode, hierarchyNode)
        label = hierarchyNode.DisplayName() if not hierarchyNode.IsLeaf() else ''
        treeNode.Label(label)

        if self.ChildrenOrdered(hierarchyNode):
            treeNode.ChildrenCount(1)

    def OnAddNodeFromColumnEnabledCB(self, exclude) :
        ok = self.OnAddNodeEnabledCB()

        if ok :
            for enumValue, domains in self.m_hierarchyPersistenDomains.iteritems() :
                if exclude != enumValue :
                    ok = len(domains) > 0
                
                    if ok :
                        break
    
        return ok

    def GetNodeChildrenNames(self, hierarchyNode, exclude = []) :
        childrenNames = set()

        if self.m_imageHierarchyTree and hierarchyNode :
            children = self.m_imageHierarchyTree.Children(hierarchyNode)
            if children :
                for child in children:
                    displayName = child.DisplayName()
                    if not displayName in exclude :
                        childrenNames.add(displayName)

        return childrenNames

    def GetUniqueValuesByColumnSpecIfApplicable(self, columnSpecification) :
        values = set()
        if columnSpecification.UniqueValues() :
            for node in self.m_imageHierarchy.HierarchyNodes():
                for dataValue in node.HierarchyDataValues():
                    if dataValue.HierarchyColumnSpecification() == columnSpecification :
                        values.add(dataValue.DataValue())
                        break

        return values

    def ColumnSpecificationFromObj(self, obj) :
        hierarchyType = self.m_imageHierarchy.HierarchyType()

        for columnSpecification in hierarchyType.SortedHierarchyColumnSpecifications() :
            if obj.Domain().IsSubtype(columnSpecification.DataDomain()) :
                return columnSpecification

        return None

    def OnAddNodeFromColumnCB(self, exclude) :
        hierarchyPersistenDomains = [] 

        for enumValue, domains in self.m_hierarchyPersistenDomains.iteritems() :
            if exclude != enumValue :
                hierarchyPersistenDomains.extend(domains)

        if hierarchyPersistenDomains :
            try:
                objects = acm.UX().Dialogs().SelectObjectsInsertItemsWithProviders(self.Shell(), hierarchyPersistenDomains, True)
                asLeaves = exclude == RestrictionKeys.GroupLevelOnly
                if objects :
                    parentItem = self.m_treeCtrl.GetSelectedItem()
                    parentNode = parentItem.GetData()

                    if parentNode.IsLeaf() :
                        parentNode = self.m_imageHierarchyTree.Parent(parentNode)
                        parentItem = parentItem.Parent()
                    
                    if self.ChildrenOrdered(parentNode) :
                        parentItem.Expand()            

                    uniqueValues = None
                    columnSpecification = None
                    self.m_searchableItemsNeedsRefresh = True
                    for obj in objects :
                        child = None
                        
                        if not columnSpecification :
                            columnSpecification = self.ColumnSpecificationFromObj(obj)

                        if not uniqueValues :
                            uniqueValues = self.GetUniqueValuesByColumnSpecIfApplicable(columnSpecification)

                        hierarchyDataValue, dataValue = self.GetValidHierachyDataValue(obj, columnSpecification, uniqueValues)
                        
                        if hierarchyDataValue :
                            if parentItem.ChildrenCount() > 0 :
                                child = parentItem.AddChild()

                            label = ''
                            if hasattr(obj, 'Name') and not asLeaves :
                                label = obj.Name()

                            hierarchyNode = self.AddHierarchyNode(label, parentNode, self.m_imageHierarchyTree, child, asLeaves)

                            if child :
                                self.AddHierarchyNodeToTree(hierarchyNode, child)
                            else:
                                parentItem.ChildrenCount(1)
                                #First child, expand so we trigger initial expand
                                parentItem.Expand()
                                child = parentItem.FirstChild()

                            hierarchyDataValue.HierarchyNode = hierarchyNode
                            hierarchyDataValue.RegisterInStorage()

                        else :
                            print ('Unable to add value ' + dataValue + ' since it already exist in a unique values column')
        

            except:
                acm.UX().Dialogs().MessageBoxInformation(self.Shell(), 'Unable to insert objects')


    def OnAddNodeCB(self, isLeaf) :

        if self.m_topNode:

            parentItem = self.m_treeCtrl.GetSelectedItem()
            hierarchy = self.m_imageHierarchy

            if not parentItem: 
                parentItem = self.m_topNode

            parentNode = parentItem.GetData()

            if parentNode.IsLeaf() :
                parentNode = self.m_imageHierarchyTree.Parent(parentNode)
                parentItem = parentItem.Parent()

            nodeLabel = ''
            childrenNames = self.GetNodeChildrenNames(parentNode)

            if not isLeaf :
                nodeLabel = GetShortNameDialog.Show(self.Shell(), 'Add Hierarchy Node', '', 'Label', -1, False, childrenNames)

            if nodeLabel != None:
                if parentItem.ChildrenCount() :
                    parentItem.Expand()
                
                    child = parentItem.AddChild()

                    hierarchyNode = self.AddHierarchyNode(nodeLabel, parentNode, self.m_imageHierarchyTree, child, isLeaf)

                    self.AddHierarchyNodeToTree(hierarchyNode, child)
                    child.EnsureVisible()
                else:
                    self.AddHierarchyNode(nodeLabel, parentNode, self.m_imageHierarchyTree, None, isLeaf)
                    parentItem.ChildrenCount(1)
                    parentItem.Expand()
                    

                self.m_searchableItemsNeedsRefresh = True
                self.m_treeCtrl.ForceRedraw()


    def OnAddNodeEnabledCB(self, notUsed = None) :
        ok = self.m_imageHierarchy != None

        if ok :
            item = self.m_treeCtrl.GetSelectedItem()

            if item:
                node = item.GetData()
                ok = not node.IsLeaf()



        return ok

    def OnEditNodeCB(self) :
        item = self.m_treeCtrl.GetSelectedItem()

        if item:
            node = item.GetData()

            if not node.IsLeaf() :
                parentNode = self.m_imageHierarchyTree.Parent(node)
                childrenNames = self.GetNodeChildrenNames(parentNode, [node.DisplayName()])
                nodeLabel = node.DisplayName() 
                nodeLabel = GetShortNameDialog.Show(self.Shell(), 'Edit Hierarchy Node', '', nodeLabel, -1, False, childrenNames)
            
                if nodeLabel :
                    node.DisplayName(nodeLabel)
                    item.Label(nodeLabel)

    def OnEditNodeEnabledCB(self, ud) :
        editable = self.OnAddNodeEnabledCB()

        if editable :
            item = self.m_treeCtrl.GetSelectedItem()

            if item:
                node = item.GetData()
                editable = not node.IsLeaf()

        return editable

    def ParentIsInItems(self, item, items) :
        parent = item.Parent()

        while parent :
            if parent in items :
                return True
            
            parent = parent.Parent()

        return False

    def ItemsHasChildren(self, items) :
        for item in items :
            if item.ChildrenCount() > 0 :
                return True

        return False

    def WarnAboutRemovingItems(self, items) :
        ret = False

        if items :
            msg = 'Are you sure you want to remove the selected ' 
            msg += 'node' if len(items) == 1 else 'nodes'
            msg += '?' if not self.ItemsHasChildren(items) else ' and all its children?' if len(items) == 1 else ' and all their children?'

            if acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Question', msg) == 'Button1' :
                ret = True

        return ret

    def RemoveItems(self, items) :
        itemsToRemove = []

        for item in items:
            self.RemoveNodeFromTreeItem(item)
            self.m_searchableItemsNeedsRefresh = True

            if not self.ParentIsInItems(item, items) :
                itemsToRemove.append(item)

        for item in itemsToRemove :
            item.Remove()

    def OnRemoveNodeCB(self) :
        items = self.m_treeCtrl.GetSelectedItems()

        if self.WarnAboutRemovingItems(items):
            self.RemoveItems(items)

    def OnRemoveNodeEnabledCB(self, ud) :
        return self.m_treeCtrl.GetSelectedItems().Size() > 0

    def GetLastChild(self, parent, excludeItem = None) :
        child = parent.FirstChild()

        if child :
            nextChild = child.Sibling(True)

            while nextChild != None :
                child = nextChild 
                nextChild = child.Sibling(True)

        if excludeItem and excludeItem == child :
            child = child.Sibling(False)       

        return child

    def MoveTreeItem(self, oldItem, newParent, newSibling = None) :
        node = oldItem.GetData()

        if newParent.ChildrenCount() == 0 :
            newParent.ChildrenCount(1)
            newParent.Expand()

        newItem = None
        if newSibling :
            newItem = self.m_treeCtrl.InsertItemAfter(newSibling)
        else:
            newItem = newParent.AddChild(False)

        self.AddHierarchyNodeToTree(node, newItem)
        newItem.Select()
        if oldItem.IsExpanded() :
            newItem.Expand()

        oldItem.Remove()


    def OnMoveItem(self, item, direction) :
        if item :
            node = item.GetData()

            if direction == MoveDirection.Down or direction == MoveDirection.Up :
                down = direction == MoveDirection.Down

                sibling = item.Sibling(down)

                if sibling:
                    siblingNode = sibling.GetData()

                    if down :
                        self.m_imageHierarchyTree.Swap(node, siblingNode)
                    else:
                        self.m_imageHierarchyTree.Swap(siblingNode, node)

                    self.m_treeCtrl.Swap(item, sibling)

            elif direction == MoveDirection.Right :
                newParent = item.Sibling(False)
                if newParent :
                    newSibling = self.GetLastChild(newParent)
                    self.MoveTreeItem(item, newParent, newSibling)
                    self.m_imageHierarchyTree.Move(node, newParent.GetData(), newSibling.GetData() if newSibling else None)
 
            elif direction == MoveDirection.Left :
                parent = item.Parent()
                if parent :
                    newParent = parent.Parent()
                    if newParent :
                        newSibling = self.GetLastChild(newParent)
                        self.MoveTreeItem(item, newParent, newSibling)
                        self.m_imageHierarchyTree.Move(node, newParent.GetData(), newSibling.GetData() if newSibling else None)


    def OnMove(self, direction):
        items = self.m_treeCtrl.GetSelectedItems()

        if direction == MoveDirection.Down :
            items = reversed(items)
    
        for item in items :
            self.OnMoveItem(item, direction)

    def CanItemMove(self, item, direction) :
        enabled = False

        if item :
            if direction == MoveDirection.Down or direction == MoveDirection.Up :
                enabled = item.Sibling(direction == MoveDirection.Down) != None
            elif direction == MoveDirection.Right :
                enabled = item.Sibling(False) != None
            elif direction == MoveDirection.Left :
                newSibling = item.Parent()
                if newSibling :
                    enabled = newSibling.Parent() != None

        return enabled

    def VerifyMovableItem(self, item, items) :
        parent = item.Parent()

        if parent :
            if parent in items :
                return False

            return self.VerifyMovableItem(parent, items)

        return True

    def CanMove(self, direction) :
        enabled = False
        items = self.m_treeCtrl.GetSelectedItems()

        for item in items :
            enabled = self.VerifyMovableItem(item, items)
            enabled = enabled and self.CanItemMove(item, direction)
            if not enabled :
                break

        return enabled

    def OnCreateHierarchyTypeEnabledCB(self, ud) :
        return True

    def OnCreateHierarchyTypeCB(self) :
        CreateHierarchyTypeDialog.Show(self.Shell(), 'Manage Hierarchy Types')

    def CreateHierarchyAddNodeCB(self):
        return HierarchyNodeCommand(self, self.OnAddNodeCB, self.OnAddNodeEnabledCB, None, False)

    def CreateHierarchyAddLeafCB(self):
        return HierarchyNodeCommand(self, self.OnAddNodeCB, self.OnAddNodeEnabledCB, None, True)

    def CreateHierarchyAddNodeFromColumnCB(self):
        return HierarchyNodeCommand(self, self.OnAddNodeFromColumnCB, self.OnAddNodeFromColumnEnabledCB, None, RestrictionKeys.LeafLevelOnly)

    def CreateHierarchyAddNodeFromColumnAsLeavesCB(self):
        return HierarchyNodeCommand(self, self.OnAddNodeFromColumnCB, self.OnAddNodeFromColumnEnabledCB, None, RestrictionKeys.GroupLevelOnly)
    
    def CreateHierarchyRemoveNodeCB(self):
        return HierarchyNodeCommand(self, self.OnRemoveNodeCB, self.OnRemoveNodeEnabledCB)    
    
    def CreateHierarchyEditNodeCB(self):
        return HierarchyNodeCommand(self, self.OnEditNodeCB, self.OnEditNodeEnabledCB)    
    
    def CreateHierarchyMoveNodeUpCB(self):
        return HierarchyNodeCommand(self, self.OnMove, self.CanMove, None, MoveDirection.Up)

    def CreateHierarchyMoveNodeDownCB(self):
        return HierarchyNodeCommand(self, self.OnMove, self.CanMove, None, MoveDirection.Down)

    def CreateHierarchySearchIncremental(self):
        return HierarchyNodeCommand(self, self.OnSearchIncremental, None, self.OnSearchIncrementalChecked)

    def CreateHierarchySearchAll(self):
        return HierarchyNodeCommand(self, self.OnSearchAll)

    def CreateHierarchyExpandCB(self) :
        return HierarchyNodeCommand(self, self.OnExpand, self.ExpandCollapseEnabled, None, False)

    def CreateHierarchyExpandAllCB(self) :
        return HierarchyNodeCommand(self, self.OnExpand, self.ExpandCollapseEnabled, None, True)

    def CreateHierarchyCollapseCB(self) :
        return HierarchyNodeCommand(self, self.OnCollapse, self.ExpandCollapseEnabled, None, False)

    def CreateHierarchyCollapseAllCB(self) :
        return HierarchyNodeCommand(self, self.OnCollapse, self.ExpandCollapseEnabled, None, True)

    def CreateHierarchyMoveNodeLeftCB(self):
        return HierarchyNodeCommand(self, self.OnMove, self.CanMove, None, MoveDirection.Left)

    def CreateHierarchyMoveNodeRightCB(self):
        return HierarchyNodeCommand(self, self.OnMove, self.CanMove, None, MoveDirection.Right)

    def CreateHierarchyTypeCB(self):
        return HierarchyNodeCommand(self, self.OnCreateHierarchyTypeCB, self.OnCreateHierarchyTypeEnabledCB)

    def CreateShowControlPaneCB(self):
        return HierarchyNodeCommand(self, self.OnShowHideControlPaneCB, self.OnShowHideControlPaneEnabledCB, self.OnShowHideControlPaneCheckedCB)

    def CreateSettingsPaneCB(self):
        return HierarchyNodeCommand(self, self.OnSettingsCB, None, None)

    def OnSettingsCB(self) :
        HierarchyApplicationSettingsDialog.Show(self.Shell(), 'Hierarchy Application Settings')

    def EnsureSelectedItemVisibleAsync(self, ud):
        item = self.m_treeCtrl.GetSelectedItem()

        if item:
            item.EnsureVisible()

    def ExpandCollapseRecursively(self, item, expand) :
        item.Expand() if expand else item.Collapse()

        for child in item.Children() :
            self.ExpandCollapseRecursively(child, expand)

    def ExpandCollapse(self, expand, subNodes) :
        for item in self.m_treeCtrl.GetSelectedItems() : 
            if subNodes :
                self.ExpandCollapseRecursively(item, expand)
            else:
                item.Expand() if expand else item.Collapse()

    def OnExpand(self, subNodes):
        self.ExpandCollapse(True, subNodes)

    def OnCollapse(self, subNodes):
        self.ExpandCollapse(False, subNodes)
    
    def ExpandCollapseEnabled(self, ud):
        ret = False
        item = self.m_treeCtrl.GetSelectedItem()
        
        if item:
            ret = self.m_imageHierarchyTree.Children(item.GetData()) != None

        return ret

    def OnSearchIncrementalChecked(self, ud) :
        return self.m_searchInput.Visible()

    def OnSearchIncremental(self) :
        show = not self.m_searchInput.Visible()
        self.m_searchInput.Visible(show)
        
        if show:
            self.m_searchInput.SetFocus()
            self.m_searchInput.SetTextSelection(0, -1)

    def OnSearchAll(self) :
        self.m_searchInput.Visible(False)
        self.m_treeCtrl.SetFocus()
        if self.CreateSearchableNodesIfNeeded() :
            SearchHierarchyDialog.Show(self.Shell(), 'Search Hierarchy', self.m_searchableItems, self.SelectTreeItemFromNode)

    def ShowControlPane(self, show) :
        self.m_controlPaneVisible = show

        for binder in self.m_columnDefByBinder.keys() :
            binder.Visible(self.m_controlPaneVisible)

        for button in self.m_clearButtons :
            button.Visible(show)

        self.Shell().CallAsynch(self.EnsureSelectedItemVisibleAsync, None)
   


     
    def OnShowHideControlPaneCB(self) :
        self.ShowControlPane(not self.m_controlPaneVisible)

    def OnShowHideControlPaneEnabledCB(self, ud):
        return self.m_imageHierarchy != None

    def OnShowHideControlPaneCheckedCB(self, ud):
        return self.m_controlPaneVisible 

    def Commands(self) :
        commands =[
        ['addNode',                'View',  'Add/Node',                  'Add a new hierarchy node',                                    'Ctrl+H',       'n',      self.CreateHierarchyAddNodeCB, False ],
        ['addLeaf',                'View',  'Add/Leaf',                  'Add a new hierarchy leaf',                                    'Ctrl+L',       'l',      self.CreateHierarchyAddLeafCB, False ],
        ['FUxMenuItemSeparator',   'View',  'Add/',  '', '', '', None, False ],
        ['addNodesFromColumns',    'View',  'Add/From Columns',          'Add node(s) using the column with the applicable domain',             '',     '',       self.CreateHierarchyAddNodeFromColumnCB, False ],
        ['addNodesFromColumnsAsLeaves', 'View',  'Add/From Columns as Leaves', 'Add node(s) as leaves using the column with the applicable domain',   '',     '',       self.CreateHierarchyAddNodeFromColumnAsLeavesCB, False ],
        FUxCore.Separator(),
        ['editNode',               'View',  'Edit Node',                 'Edit the selected hierarchy node',                            'Ctrl+E',       'E',      self.CreateHierarchyEditNodeCB, False ],
        FUxCore.Separator(),
        ['removeNode',             'View',  'Remove Node',               'Remove the selected hierarchy node',                          'Ctrl+Shift+H', 'o',      self.CreateHierarchyRemoveNodeCB, False ],
        FUxCore.Separator(),
        ['moveNodeUp',             'View',  'Move/Up',                   'Move the selected hierarchy node up',                         'Ctrl+U',       'U',      self.CreateHierarchyMoveNodeUpCB, False ],
        ['moveNodeDown',           'View',  'Move/Down',                 'Move the selected hierarchy node down',                       'Ctrl+D',       'D',      self.CreateHierarchyMoveNodeDownCB, False ],
        ['moveNodeLeft',           'View',  'Move/Left',                 'Move the selected hierarchy node left',                       'Ctrl+T',       'f',      self.CreateHierarchyMoveNodeLeftCB, False ],
        ['moveNodeRight',          'View',  'Move/Right',                'Move the selected hierarchy node right',                      'Ctrl+R',       'R',      self.CreateHierarchyMoveNodeRightCB, False ],
        FUxCore.Separator(),
        ['findIncremental',         'View',  'Find/Incremental',          'Search the hierarchy incrementally',                         'Ctrl+I',       'I',      self.CreateHierarchySearchIncremental, False ],
        ['findAll',                 'View',  'Find/All',                  'Search all nodes',                                           'Ctrl+F',       '',      self.CreateHierarchySearchAll, False ],
        FUxCore.Separator(),
        ['expandNode',              'View',  'Expand/Selected Node(s)',   'Expand the selected node',                                   'Ctrl+Shift+Add', '',      self.CreateHierarchyExpandCB, False ], #for multiselected expand, just 'Add' is taken by the tree
        ['expandAllSubNodes',       'View',  'Expand/All Subnodes',       'Expand all subnodes',                                        'Ctrl+Add',      '',      self.CreateHierarchyExpandAllCB, False ],
        ['collapseNode',            'View',  'Collapse/Selected Node(s)', 'Collapse the selected node',                                 'Ctrl+Shift+Subtract', '',      self.CreateHierarchyCollapseCB, False ],
        ['collapseAllSubNodes',     'View',  'Collapse/All Subnodes',     'Collapse all subnodes',                                      'Ctrl+Subtract', '',      self.CreateHierarchyCollapseAllCB, False ],
        FUxCore.Separator(),
        ['editHierarchyType',       'View',  'Manage Hiearchy Types',     'Edit or Create a Hierarchy Type',                             'Ctrl+M',       'T',      self.CreateHierarchyTypeCB, False ],
        FUxCore.Separator(),
        ['showEditControls',        'View',  'Show Edit Controls',        'Show or hides the edit control pane',                         'Ctrl+W',       '',       self.CreateShowControlPaneCB, False ],
        FUxCore.Separator(),
        ['settings',                'View',  'Settings',                   'Settings ',                                                  'Ctrl+B',            '',        self.CreateSettingsPaneCB, False ],
        ]

        return commands
            
    def HandleRegisterCommands(self, builder):
        fileCommands = acm.FSet()
        
        fileCommands.Add('FileNew')
        fileCommands.Add('FileOpen')
        fileCommands.Add('FileSave')
        fileCommands.Add('FileSaveAs')
        fileCommands.Add('FileDelete')
            
        builder.RegisterCommands(FUxCore.ConvertCommands(self.Commands()), fileCommands)
    
    def HandleStandardFileCommandInvoke(self, commandName):
        if commandName == 'FileNew':
            self.OnFileNew()
        if commandName == 'FileOpen':
            self.OnFileOpen()
        if commandName == 'FileSaveAs':
            self.OnFileSaveAs()
        if commandName == 'FileSave':
            self.OnFileSave()
        if commandName == 'FileDelete':
            self.OnFileDelete()
            
    def HandleStandardFileCommandEnabled(self, commandName):
        ret = True
        if commandName == 'FileSaveAs':
            ret = self.m_imageHierarchy != None
        if commandName == 'FileSave':
            ret = self.HasChanged()
        if commandName == 'FileDelete':
            ret = self.m_originalHierarchy != None

        return ret

    def ValidateSaveCB(self, ud, namn, existingItem, p3):
        isValidSave = existingItem == None

        if existingItem :
            ret = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Question', 'Are you sure you want to replace the hierarchy ' + existingItem.StringKey() + '?')
            if ret == 'Button1' :
                isValidSave = HierarchyEditorUtils.DeleteObject(existingItem, self.Shell())

        return isValidSave    
       
    def DoFileNew(self):
        hierarchy = CreateNewHierarchyDialog.Show(self.Shell(), 'Create new Hierarchy', 'New Hierarchy')

        if hierarchy:
            self.PopulateObject(hierarchy)

            self.m_topNode = self.m_treeCtrl.GetRootItem().AddChild()
            hierarchyNode = self.AddHierarchyNode(hierarchy.Name(), None, self.m_imageHierarchyTree, self.m_topNode, False)
            self.AddHierarchyNodeToTree(hierarchyNode, self.m_topNode)
            self.UpdateBinderVisibility(hierarchyNode)


    def OnFileNew(self):
        if self.VerifyCloseSetup('Do you want to save the current hierarchy?'):
            self.DoFileNew()


    def Clear(self) :
        self.m_imageHierarchy = None
        self.m_originalHierarchy = None
        self.m_treeCtrl = None
        self.m_columnIndexByColumnDef = {}
        self.m_settingsByColumnIndex = {}
        self.m_columnDefByBinder = {}
        self.m_clearButtons = []
        self.m_topNode = None
        self.m_hierarchyPersistenDomains = None
        self.m_treeItemByHierarchyNode = {}
        self.m_currentValidValue = None

        self.InitLayout()
        self.UpdateControls()

        self.SetCaption()

    def OnFileDelete(self):
        ret = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Question', 'Are you sure you want to delete the current hierarchy?')

        if ret == 'Button1' :
            if self.m_originalHierarchy :
                if HierarchyEditorUtils.DeleteObject(self.m_originalHierarchy, self.Shell()) :
                    self.Clear()

    def CommitHierarchy(self) :
        if self.m_imageHierarchy:
            if HierarchyEditorUtils.CommitObject(self.m_imageHierarchy, self.Shell()) :
                self.m_imageHierarchy = self.m_originalHierarchy.StorageImage()
                self.m_imageHierarchyTree = acm.FHierarchyTree()
                self.m_imageHierarchyTree.Hierarchy(self.m_imageHierarchy)
                self.UpdateImageHierarchy()
                self.AddObjectToMostRecentlyUsedList(self.m_originalHierarchy)

                self.SetCaption()

    def GetImageHierarchyNode(self, uniqueId, nodesByUniqueId) :
        return nodesByUniqueId.get(uniqueId)
    
    def UpdateTreeNodesRecursive(self, treeItem, nodesByUniqueId) :
        hierarchyNode = treeItem.GetData()
        if hierarchyNode :
            newHierarchyNode = self.GetImageHierarchyNode(hierarchyNode.UniqueId(), nodesByUniqueId)
            self.SetTreeItemData(treeItem, newHierarchyNode)

        children = treeItem.Children() 

        for child in children :
            self.UpdateTreeNodesRecursive(child, nodesByUniqueId)

    def  UpdateImageHierarchy(self) :

        nodesByUniqueId = {}
        self.m_treeItemByHierarchyNode = {}
        hierarchyNodes = self.m_imageHierarchy.HierarchyNodes()

        for hierarchyNode in  hierarchyNodes :
            nodesByUniqueId[hierarchyNode.UniqueId()] = hierarchyNode
    
        self.UpdateTreeNodesRecursive(self.m_treeCtrl.GetRootItem(), nodesByUniqueId)
       
    def OnFileSave(self):
        self.CommitHierarchy()
          
    def OnFileSaveAs(self):
        name  = acm.UX().Dialogs().SaveObjectAs(self.Shell(), 'Save Hierarchy As...', 'Hierarchies',  self.AllHierarchies(), None, self.ValidateSaveCB, None) 

        if name != None:
            newHierarchy = self.m_imageHierarchyTree.Duplicate()
            newHierarchy.Name(name)
            if HierarchyEditorUtils.CommitObject(newHierarchy, self.Shell()) :
                self.PopulateObject(newHierarchy)

    def OnFileOpen(self):
        if self.VerifyCloseSetup('Do you want to save the current hierarchy?'):
            selectedObject = OpenHierarchyDialog.Show(self.Shell(), 'Open Hierarchy', True)
            #selectedObject = acm.UX().Dialogs().SelectObject(self.Shell(), 'Select Hierarchy', 'Hierarchies', self.AllHierarchies(), None)
            if selectedObject != None:
                self.PopulateObject(selectedObject)
    
    def AllHierarchies(self):
        if self.m_hierarchies == None:
            self.m_hierarchies = acm.FHierarchy.Select('').SortByProperty('Name')

        return self.m_hierarchies
    
    def HandleBuildContextMenu(self, builder, cd):
        #Look at HandleRegisterCommands for more information about the command list
        commands =[
        ['addHierarchys', '', 'Add Risk Factor Collection', '', '', '', self.CreateCommandCB, False ],
        ['editHierarchys', '', 'Edit Risk Factor Collection', '', '', '', self.CreateCommandCB, True ],
        ]
        
        builder.RegisterCommands(FUxCore.ConvertCommands(commands))
        
    def HandleDefaultAction(self, shell, cd):
        pass
        
    def HandleSetContents(self, contents):
        if self.VerifyCloseSetup('Do you want to save the current hierarchy?'):
            hierarchy = self.GetHierarchyFromContents(contents)
            if hierarchy :
                self.HandleObject(hierarchy)
                if self.m_treeCtrl:
                    self.PopulateObject(self.m_imageHierarchy, False)
                
    
    def HandleGetContents(self):
        return self.m_originalHierarchy.Name()
        

    def GetCurrentObject(self) :
        return self.m_originalHierarchy
    
    def GetHierarchyFromContents(self, obj):
        hierarchy = None
        if obj :
            if type(obj) == type(''):
                hierarchy = acm.FHierarchy[obj]
            elif hasattr(obj, 'IsKindOf') and obj.IsKindOf('FHierarchy') :
                hierarchy = obj
    
        return hierarchy

    def CanHandleObject(self, obj):
        ret = False

        if obj :
            if type(obj) == type(''):
                ret = True
            elif hasattr(obj, 'IsKindOf') and obj.IsKindOf('FHierarchy') :
                ret = True

        return ret

    def StringFromDataValue(self, value):
        valueAsString = ''
        if hasattr(value, "StringKey") :
            valueAsString = value.StringKey()
        else:
            valueAsString = str(value)

        return valueAsString

    def ChildrenOrdered(self, node) :
        return self.m_imageHierarchyTree.Children(node)

    def OnTreeInitialExpand(self, ud, cd) :
        item = cd.At(acm.FSymbol('Item'))
        node = item.GetData()
        self.PopulateNodes(self.ChildrenOrdered(node), item)

    def PopulateNodes(self, nodes, root):
        if nodes :
            #only one level should be added since the tree builds on expantion
            for node in nodes :
                child = root.AddChild()
                self.AddHierarchyNodeToTree(node, child) 

    def PopulateColumns(self, hierarchy):
        parameter = ParameterFromName('HierarchyEditorSettings')

        self.m_columnIndexByColumnDef = {}
        self.m_settingsByColumnIndex = {}
        self.m_hierarchyPersistenDomains = {}

        self.m_hierarchyPersistenDomains[RestrictionKeys.NoRestrictions] = []
        self.m_hierarchyPersistenDomains[RestrictionKeys.LeafLevelOnly] = []
        self.m_hierarchyPersistenDomains[RestrictionKeys.GroupLevelOnly] = []

        self.m_treeCtrl.ColumnWidth(0, 200)
        hierarchyType = hierarchy.HierarchyType()
        columnSpecifications = hierarchyType.SortedHierarchyColumnSpecifications()

        index = 1
        for columnSpecification in columnSpecifications :
            choice = columnSpecification.ColumnCategory()
            visible = True
            if choice :
                settings = SettingsFromChoice(choice, parameter)
                if settings :
                    if settings.m_visible:
                        self.m_settingsByColumnIndex[index] = settings

                visible = settings.m_visible
                    
            if visible :
                self.m_treeCtrl.AddColumn(columnSpecification.Name(), 100)
                self.m_columnIndexByColumnDef[columnSpecification] = index


                if columnSpecification.DataDomain().Class().IncludesBehavior('FPersistentClass'):
                    restriction = columnSpecification.Restriction()
                    self.m_hierarchyPersistenDomains[restriction].append(columnSpecification.DataDomain())

                index += 1

    def GetCurrentRootNode(self) :
        rootNode = None

        if self.m_imageHierarchyTree:
            rootNode = self.m_imageHierarchyTree.RootNode()

        return rootNode

    def PopulateHierarchy(self):
        self.m_treeCtrl.RemoveAllItems()
        self.m_treeItemByHierarchyNode = {}
        self.m_searchableItemByNode = {}
        self.m_searchableItems = []

        currentHierarchy = self.m_imageHierarchy

        if currentHierarchy :
            self.PopulateColumns(currentHierarchy)
            rootNode = self.GetCurrentRootNode()

            if rootNode :
                self.m_topNode = self.m_treeCtrl.GetRootItem().AddChild()
                self.AddHierarchyNodeToTree(rootNode, self.m_topNode)
                self.UpdateBinderVisibility(rootNode)
                self.UpdateBinderValues(self.m_topNode)

    def PopulateObject(self, obj, handleObject = True):
        if handleObject :
            self.HandleObject(obj)

        self.InitLayout()
        self.PopulateHierarchy()
        self.ShowControlPane(self.m_controlPaneVisible)
        self.AddObjectToMostRecentlyUsedList(self.m_originalHierarchy)

        self.SetCaption()
        self.UpdateControls()
        self.m_searchableItemsNeedsRefresh = True

    def HandleObject(self, obj):
        if obj.IsKindOf('FHierarchy'):
            self.m_originalHierarchy = obj
            if obj.IsInfant() :
                self.m_originalHierarchy.RegisterInStorage()
                self.m_imageHierarchy = self.m_originalHierarchy
            else:
                self.m_imageHierarchy = obj.StorageImage()

            self.m_imageHierarchyTree = acm.FHierarchyTree()
            self.m_imageHierarchyTree.Hierarchy(self.m_imageHierarchy)

    
    def GetApplicationIcon(self):
        return 'Tree'
    
    def UpdateControls(self):
        pass

    def UpdateBinderVisibility(self, hierarchyNode) :
        isLeaf = hierarchyNode.IsLeaf()

        for binder, columnDef in self.m_columnDefByBinder.iteritems() :
            visible = True
            if columnDef.Restriction() == RestrictionKeys.LeafLevelOnly :
                visible = isLeaf
            elif columnDef.Restriction() == RestrictionKeys.GroupLevelOnly :
                visible = not isLeaf

            binder.Enabled(visible)

    def UpdateBinderValues(self, item) :
        if item and self.m_imageHierarchy:
            hierarchyNode = item.GetData()
            valuesByName = {}

            dataValues = hierarchyNode.HierarchyDataValues()

            for value in dataValues:
                columnSpecification = value.HierarchyColumnSpecification()
                valuesByName[acm.FSymbol(self.CtrlNameFromOId(columnSpecification.Oid()))] = value.DataValueVA()

            self.UpdateBinderVisibility(hierarchyNode)
            self.m_binders.SetValuesByName(valuesByName, False)
            item.EnsureVisible()
     
    def OnTreeDisplayInfo(self, ud, cd) :
        displayInfo = cd.At(acm.FSymbol('DisplayInfo'))
        treeItem = displayInfo.Item()
        hierarchyNode = treeItem.GetData()

        try :
            if displayInfo.Type() == 'Icon' :
                displayInfo.Value('TreeSimulate' if hierarchyNode.IsLeaf() else 'Tree')
            elif displayInfo.Type() == 'Label':
                if displayInfo.SubItem() == 0 :
                    displayInfo.Value(hierarchyNode.DisplayName())
                else :
                    for dataValue in hierarchyNode.HierarchyDataValues() :
                        index = self.m_columnIndexByColumnDef.get(dataValue.HierarchyColumnSpecification(), -1)
                        if index == displayInfo.SubItem() :
                            value = self.FormatValue(dataValue.HierarchyColumnSpecification().DataDomain(), dataValue.DataValueVA())
                            displayInfo.Value(value)

                    settings = self.m_settingsByColumnIndex.get(displayInfo.SubItem(), None)

                    if settings:
                        bg = settings.m_color.ColorRef() if settings.m_color else self.m_whiteColor
                        fg = self.m_blackColor

                        treeItem.Style(displayInfo.SubItem(), settings.m_bold, fg, bg)
        except Exception as e:
            print (e)

    def OnTreeCtrlChanged(self, ud, cd) :
        item = self.m_treeCtrl.GetSelectedItem()
        self.UpdateBinderValues(item)

    def CtrlNameFromOId(self, oid, postfix = '') :
        return 'Ctrl' + str(oid) + postfix

    def ShowUniqueColumnWarning(self, ud) :
        acm.UX().Dialogs().MessageBoxInformation(self.Shell(), 'Unable to set the chosen value since it already exist in a unique only column')
        self.m_showWarningOnQueue = False

    def ShowUniqueColumnWarningAsync(self, dataValue, showDialog) :
        if not self.m_showWarningOnQueue :
            
            if showDialog:
                self.m_showWarningOnQueue  = True
                self.Shell().CallAsynch(self.ShowUniqueColumnWarning, dataValue)
            
            raise ValueError(dataValue + ' already exist in a unique values column')

    def StartInPlaceEditing(self, args):
        treeItem = args[0]
        subItem = args[1]
        
        treeItem.EditLabel(subItem, True)
        self.m_pendingInPlaceEditing = False

    def StartInPlaceEditingAsync(self, treeItem, subItem) :
        if not self.m_pendingInPlaceEditing :
            self.m_pendingInPlaceEditing = True
            self.Shell().CallAsynch(self.StartInPlaceEditing, [treeItem, subItem])

    def VerifyAspectSymbol(self, aspectSymbol) :
        ret = False
    
        if aspectSymbol == 'ControlValueChanged' :
            ret = True
        elif aspectSymbol == 'ControlModifyFinished' and self.m_lastAspectSymbol == 'ControlModifyStarted' :
            ret = True

        self.m_lastAspectSymbol = aspectSymbol

        return ret
        
    def SetHierarchyNodeValue(self, hierarchyNode, columnSpecification, newValue, showWarning, oldValue):
        dataValues = hierarchyNode.HierarchyDataValues()
        found = False
        if dataValues:
            for value in dataValues:
                nodeColumnSpecification = value.HierarchyColumnSpecification()
                if nodeColumnSpecification == columnSpecification :
                    oldValue.append(value.DataValue())
                    hierarchyDataValue, dataValue = self.GetValidHierachyDataValue(newValue, columnSpecification, None, value.DataValue())

                    if hierarchyDataValue:
                        if newValue not in [None, '']:
                            value.DataValueVA(newValue)
                        else:
                            value.Unsimulate()
                    else:
                        self.ShowUniqueColumnWarningAsync(dataValue, showWarning)

                    found = True
                    break


        if not found:
            self.CreateHierarchyDataValue(hierarchyNode, columnSpecification, newValue, None, showWarning)

        self.UpdateSearchItem(hierarchyNode)

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        item = self.m_treeCtrl.GetSelectedItem()

        if item and parameter and self.VerifyAspectSymbol(str(aspectSymbol)):
            hierarchyNode = item.GetData()
            binderValue = parameter.GetValue()
            columnSpecification = self.m_columnDefByBinder[parameter]

            try :
                oldValue = []
                self.SetHierarchyNodeValue(hierarchyNode, columnSpecification, binderValue, True, oldValue)
                self.m_treeCtrl.ForceRedraw()
            except ValueError as e:
                print (e)

    def AddCustomTreeContextItemsCB(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(self.Commands()))

    def GetItemsFromColumnDefinition(self, columnDef, value) :
        domain = columnDef.DataDomain()
        values = None
        acmValues = None

        if domain.Class().IncludesBehavior(acm.FEnumeration) :
             acmValues = domain.Enumerators()
        #if domain.Class().IncludesBehavior(acm.FPersistentClass) and value:
        #    acmValues = domain.Select('name=')

        if acmValues :
            values = []
            uniqueValues = self.GetUniqueValuesByColumnSpecIfApplicable(columnDef)
            for value in acmValues:
                if not value in uniqueValues:
                    values.append(value)

        return values

    def OnInPlaceEditingBegin(self, ud, cd):
        info = cd.At('InPlaceEditingInfo')
        info.DynamicSize(False)
        info.ReturnMovesDown(True)
        hierarchyNode = info.Item().GetData()

        if info.SubItem() == 0 :
            if hierarchyNode.IsLeaf() :
                info.Cancel(True)
        else:
            for columnDef, index in self.m_columnIndexByColumnDef.iteritems() :
                if info.SubItem() == index or info.SubItem() == 0:
                    if columnDef.Restriction() == RestrictionKeys.LeafLevelOnly and not hierarchyNode.IsLeaf() :
                        info.Cancel(True)
                    elif columnDef.Restriction() == RestrictionKeys.GroupLevelOnly and hierarchyNode.IsLeaf() :
                        info.Cancel(True)
                    elif self.m_currentValidValue != None :
                        info.SetValue(self.m_currentValidValue)

                    info.SetItems(self.GetItemsFromColumnDefinition(columnDef, info.GetValue()))

                    break

        self.m_currentValidValue = None

    def ConvertAndUpdateValueThroughBinder(self, currentColumnDef, value):
        for binder, columnDef in self.m_columnDefByBinder.iteritems() :
            if currentColumnDef == columnDef :
                binder.SetValue(value, False)
                value = binder.GetValue()

        return value

    def FormatterFromDomain(self, domain ):
        formatter = domain.DefaultFormatter()

        if domain.StringKey() == 'double':
            formatter = acm.Get('formats/FullPrecision')
        
        return formatter

    def ParseValue(self, domain, value) :
        if value :
            formatter = self.FormatterFromDomain(domain)
        
            if formatter:
                parsedValue = formatter.Parse(value, domain)
                if parsedValue != None :
                    if domain.StringKey() == 'double' and not parsedValue:
                        value = '0'
                    else :
                        value = parsedValue
                else :
                    raise(Exception(value + ' is not a valid ' + domain.Name()))

        return value

    def FormatValue(self, domain, value) :
        formatter = self.FormatterFromDomain(domain)
        
        if formatter:
            value = formatter.Format(value)
        elif value and domain.Class().IncludesBehavior(acm.FPersistent):
            attr = domain.UniqueNameAttribute()
            query = 'name=' + value

            if attr :
                query = attr.StringKey() + '=' + value

            obj = domain.Select01(query, None)

            if not obj :
                raise(Exception('No ' + domain.Name() + ' with the name ' + value + ' exist'))        

        return value

    def OnInPlaceEditingEnd(self, ud, cd):
        info = cd.At('InPlaceEditingInfo')
        hierarchyNode = info.Item().GetData()
        self.m_currentValidValue = None

        if info.SubItem() == 0 :
            value =  info.GetValue()   

            if value and hierarchyNode.IsLeaf() :
                print ('Unable to set value: ' + info.GetValue() + '. Message: Leaves are not allowed to have labels')
                value = ''
                info.SetValue('')


            hierarchyNode.DisplayName(value)

        else:
            for columnDef, index in self.m_columnIndexByColumnDef.iteritems() :
                if info.SubItem() == index :
                    value =  str(info.GetValue())
                    if not value:
                        value = None

                    if value and columnDef.Restriction() == RestrictionKeys.LeafLevelOnly and not hierarchyNode.IsLeaf():
                        print ('Unable to set value: ' + info.GetValue() + '. Message: Node parents cannot have a value on a column with the Leaf Level Only restriction')
                        value = ''
                        info.SetValue('')
                    elif value and columnDef.Restriction() == RestrictionKeys.GroupLevelOnly and hierarchyNode.IsLeaf():
                        print ('Unable to set value: ' + info.GetValue() + '. Message: Node parents cannot have a value on a column with the Group Level Only restriction')
                        value = ''
                        info.SetValue('')
                        

                    oldValue = []

                    try:
                        nodeValue = self.ParseValue(columnDef.DataDomain(), value)
                        self.SetHierarchyNodeValue(hierarchyNode, columnDef, nodeValue, False, oldValue)
                        
                        if value != None:
                            value = self.FormatValue(columnDef.DataDomain(), value)

                            info.SetValue(value)

                        self.UpdateBinderValues(info.Item())

                    except Exception as e:
                        print ('Unable to set value: ' + info.GetValue() + '. Message: ' + e.message)
                        
                        info.Cancel(True)
                        self.m_currentValidValue = info.GetValue()
                        self.StartInPlaceEditingAsync(info.Item(), info.SubItem())



    def OnTreeContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        item = self.m_treeCtrl.GetSelectedItem()
        if item :
            obj = item.GetData()
            if hasattr(obj, 'Class') :
                acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, [obj], False, self.AddCustomTreeContextItemsCB, None)
            else:
                menuBuilder.RegisterCommands(FUxCore.ConvertCommands(self.Commands()))


    def InitLayout(self, creationInfo = None):
        self.m_columnDefByBinder = {}
        self.m_clearButtons = []
        builder = acm.FUxLayoutBuilder()

        if self.m_binders :
            self.m_binders.RemoveDependent(self)


        self.m_binders = acm.FUxDataBindings()
        self.m_binders.AddDependent(self)
        builder.BeginHorzBox()
        builder.BeginVertBox()
        builder.    AddInput('searchInput', 'Incremental search')
        builder.    AddTree('hierarchyTree', 800, 200)

        buttonNameAndBinders = []
    
        if self.m_imageHierarchy :
            builder.    BeginVertBox()
            hierarchyType = self.m_imageHierarchy.HierarchyType()

            for cd in hierarchyType.HierarchyColumnSpecifications() :
                formatter = self.FormatterFromDomain(cd.DataDomain())
                builder.BeginHorzBox()
                binder = self.m_binders.AddBinderAndBuildLayoutPart(builder, self.CtrlNameFromOId(cd.Oid()), cd.Name(), cd.DataDomain(), formatter, None, True, None, True)
                if str(cd.DataDomain()) == 'bool':
                    builder.AddFill()

                buttonName = self.CtrlNameFromOId(cd.Oid(), 'Button')
                builder.AddButton(buttonName, '', False, True)
                builder.EndBox()

                self.m_columnDefByBinder[binder] = cd
                buttonNameAndBinders.append((buttonName, binder, cd.Name()))

            builder.    EndBox()
        builder.EndBox()
        builder.EndBox()
        if creationInfo:
            self.m_listPane = creationInfo.AddPane(builder, 'listPane')
        else:
            self.m_listPane.SetLayout(builder, 'listPane')

        self.m_searchInput = self.m_listPane.GetControl('searchInput')        
        self.m_searchInput.AddCallback('Changed', self.OnSearchInputChanged, 0 )
        self.m_searchInput.AddCallback('Activate', self.OnSearchInputChanged, 1 )
        self.m_searchInput.Visible(False)

        self.m_treeCtrl = self.m_listPane.GetControl('hierarchyTree')
        self.m_treeCtrl.ColumnLabel(0, 'Hierarchy')
        self.m_treeCtrl.ShowColumnHeaders(True)
        self.m_treeCtrl.EnableMultiSelect(True)
        self.m_treeCtrl.AddCallback('SelectionChanged', self.OnTreeCtrlChanged, self)
        self.m_treeCtrl.AddCallback('GetDisplayInfo', self.OnTreeDisplayInfo, self)
        self.m_treeCtrl.AddCallback('InitialExpand', self.OnTreeInitialExpand, self)
        self.m_treeCtrl.AddCallback('ContextMenu', self.OnTreeContextMenu, None )
        self.m_treeCtrl.AddCallback('InPlaceEditingBegin', self.OnInPlaceEditingBegin, None )
        self.m_treeCtrl.AddCallback('InPlaceEditingEnd', self.OnInPlaceEditingEnd, None )

        self.m_treeCtrl.AddCallback('DragSourceBegin', self.OnDragSourceBegin, None )
        self.m_treeCtrl.AddCallback('DropTargetCanHandle', self.OnDropTargetCanHandle, None )
        self.m_treeCtrl.AddCallback('DropTargetHandle', self.OnDropTargetHandle, None )

        self.m_binders.AddLayout(self.m_listPane)

        for buttonName, binder, controlName in buttonNameAndBinders :
            buttonControl = self.m_listPane.GetControl(buttonName)
            buttonControl.SetIcon('Clear', False)
            buttonControl.ToolTip('Clears the ' + controlName + ' value')
            buttonControl.AddCallback('Activate', self.OnClearButton, binder)
            self.m_clearButtons.append(buttonControl)

    def OnClearButton(self, binder, cd) :
        binder.SetValue(None)

    def GetContextHelpID(self):
        return 1036

    def HandleCreate( self, creationInfo ):
        self.EnableOnIdleCallback(True)
        
        self.InitLayout(creationInfo)
        if self.m_imageHierarchy :
            self.PopulateObject(self.m_imageHierarchy, False)
        self.UpdateControls()

    def VerifyCloseSetup(self, text) :
        if self.HasChanged():
            ret = acm.UX().Dialogs().MessageBoxYesNoCancel(self.Shell(), 'Information', text)

            if ret == 'Button1' :
                self.OnFileSave()
                return True

            if ret == 'Button2' :
                return True

            if ret == 'Button3' :
                return False

        return True

    def HandleClose(self):
        return self.VerifyCloseSetup('Do you want to save before closing?')

    def SetCaption(self):
        if self.m_imageHierarchy:
            self.SetContentCaption(self.m_imageHierarchy.StringKey())
    
    def DoChangeCreateParameters( self, createParams ):
        createParams.UseSplitter(True)
        createParams.SplitHorizontal(False)
        createParams.LimitMinSize(True)
        createParams.AutoShrink(False)
        createParams.AdjustPanesWhenResizing(True)
        createParams.ShowMostRecentlyUsedList(True)
        
    def HandleCreateStatusBar(self, sb):
        self.m_statusBarTextPane = sb.AddTextPane(100)
        self.m_statusBarIconPane = sb.AddIconPane()
        self.m_statusBarProgressPane = sb.AddProgressPane(100)

    def HasChanged(self) :
        return self.m_imageHierarchy != None and (self.m_imageHierarchy.IsModified() or self.m_imageHierarchy.IsInfant())

    def CreateDragDropObject(self, hierarchyNode, rightDrag) :
        dragObject = acm.FDictionary()

        dragObject.AtPut(DragDropKeys.DragObject, hierarchyNode)
        dragObject.AtPut(DragDropKeys.RightDrag, rightDrag)

        return dragObject

    def OnDragSourceBegin(self, ud, cd) :
        selectedItems = self.m_treeCtrl.GetSelectedItems()
        if len(selectedItems) == 1 :
            item = self.m_treeCtrl.GetSelectedItem()
            hierarchyNode = item.GetData()
            beginDragInfo = cd.At(acm.FSymbol('DragSourceBegin'))
            beginDragInfo.SetObject(self.CreateDragDropObject(hierarchyNode, beginDragInfo.IsRightDrag()))

    def IsHierarchyNodeParent(self, potentialParent, child):
        isParent = False

        parent = self.m_imageHierarchyTree.Parent(child)

        while parent != None :
            if parent == potentialParent:
                isParent = True 
                break

            parent = self.m_imageHierarchyTree.Parent(parent)

        return isParent

    def ValidDrop(self, hierarchyNode, treeItem, rightDrag = False) :
        ret = True
        dropHierarchyNode = treeItem.GetData() if treeItem else None


        ret = ret and hierarchyNode != None
        ret = ret and dropHierarchyNode != None
        ret = ret and hierarchyNode.Hierarchy() == self.m_imageHierarchy
        ret = ret and hierarchyNode != dropHierarchyNode
        ret = ret and not self.IsHierarchyNodeParent(hierarchyNode, dropHierarchyNode)

        if not rightDrag :
            ret = ret and not dropHierarchyNode.IsLeaf()

        return ret

    def OnDropTargetCanHandle(self, ud, cd) :
        canHandleDropInfo = cd.At(acm.FSymbol('DropTargetCanHandle'))

        dragObject = canHandleDropInfo.GetObject()
        if dragObject and dragObject.Class() == acm.FDictionary :
            rightDrag = dragObject.At(DragDropKeys.RightDrag)

            if self.ValidDrop(dragObject.At(DragDropKeys.DragObject), canHandleDropInfo.Item(), rightDrag) :
                canHandleDropInfo.CanHandle(True)
                canHandleDropInfo.DropEffect('CopyOrMove')

    def RightDropMenuCallback(self, menuData) :
        dropObject = menuData.At(RightDropDataKeys.DropObject)
        dropItem = menuData.At(RightDropDataKeys.DropItem)
        dropType = menuData.At(RightDropDataKeys.DropType)
        dropAction = menuData.At(RightDropDataKeys.DropAction)
        dropSibling = None

        if dropType == RightDropTypes.Child :
            item = self.m_treeItemByHierarchyNode[dropObject]
            dropSibling = self.GetLastChild(dropItem, item)
        elif dropType == RightDropTypes.PreviousSibling :
            dropSibling = dropItem.Sibling(False)
            dropItem = dropItem.Parent()
        elif dropType == RightDropTypes.NextSibling :
            dropSibling = dropItem
            dropItem = dropItem.Parent()


        if dropAction == DropAction.Move:
            self.MoveHierarchyNode(dropObject, dropItem, dropSibling)  
        else:
             self.CopyHierarchyNode(dropObject, dropItem, dropSibling)
        

    def CreateRightDropMenuData(self, dropObject, dropItem, dropType, dropAction) :
        menuData = acm.FDictionary()

        menuData.AtPut(RightDropDataKeys.DropObject, dropObject)
        menuData.AtPut(RightDropDataKeys.DropItem, dropItem)
        menuData.AtPut(RightDropDataKeys.DropType, dropType)
        menuData.AtPut(RightDropDataKeys.DropAction, dropAction)

        return menuData

    def CreateRightSubMenu(self, subMenu, dropObject, dropItem, dropAction) :
        subMenu.AddItem(self.RightDropMenuCallback, self.CreateRightDropMenuData(dropObject, dropItem, RightDropTypes.Child, dropAction), 'Child', ' ', dropItem and self.ValidDrop(dropObject, dropItem), False)
        subMenu.AddSeparator()
        subMenu.AddItem(self.RightDropMenuCallback, self.CreateRightDropMenuData(dropObject, dropItem, RightDropTypes.PreviousSibling, dropAction), 'Above', ' ', dropItem and self.ValidDrop(dropObject, dropItem.Parent()), False)
        subMenu.AddItem(self.RightDropMenuCallback, self.CreateRightDropMenuData(dropObject, dropItem, RightDropTypes.NextSibling, dropAction), 'Below', ' ',  dropItem and self.ValidDrop(dropObject, dropItem.Parent()), False)


    def OnDropTargetHandle(self, ud, cd) :
        dropInfo = cd.At(acm.FSymbol('DropTargetHandle'))
        dragObject = dropInfo.GetObject()

        if dragObject and dragObject.Class() == acm.FDictionary :
            obj = dragObject.At(DragDropKeys.DragObject)
            rightDrag = dragObject.At(DragDropKeys.RightDrag)
            if self.ValidDrop(obj, dropInfo.Item(), rightDrag) :
            
                if rightDrag:
                    menu = acm.FUxMenu()
                    self.CreateRightSubMenu(menu.AddSubMenu('Move'), obj, dropInfo.Item(), DropAction.Move)
                    self.CreateRightSubMenu(menu.AddSubMenu('Copy'), obj, dropInfo.Item(), DropAction.Copy)
                    menu.Track(self.m_treeCtrl, dropInfo.X(), dropInfo.Y())

                else :
                    parentItem = dropInfo.Item()
                    if dropInfo.IsCopy() :
                        self.CopyHierarchyNode(obj, parentItem, self.GetLastChild(parentItem))
                    else :
                        item = self.m_treeItemByHierarchyNode[obj]
                        newSibling = self.GetLastChild(parentItem, item)

                        self.MoveHierarchyNode(obj, parentItem, newSibling)


    def CopyHierarchyNode(self, hierarchyNode, parentItem, newSibling = None) :
        copiedHierarchyNode = self.m_imageHierarchyTree.Copy(hierarchyNode, parentItem.GetData(), newSibling.GetData() if newSibling else None)

        if parentItem.ChildrenCount() :
            #be sure it is expanded before adding
            parentItem.Expand()
            child = None

            if newSibling :
                child = self.m_treeCtrl.InsertItemAfter(newSibling)
            else: 
                child = parentItem.AddChild(False)

            self.AddHierarchyNodeToTree(copiedHierarchyNode, child)

            children = self.m_imageHierarchyTree.Children(copiedHierarchyNode)

            if children and not children.IsEmpty() :
                child.ChildrenCount(1)
        else :
            parentItem.ChildrenCount(1)
            #initial expand will populate
            parentItem.Expand()
        

    def MoveHierarchyNode(self, hierarchyNode, parentItem, newSibling = None) :
        item = self.m_treeItemByHierarchyNode[hierarchyNode]

        newSiblingNode = newSibling.GetData() if newSibling else None
        self.MoveTreeItem(item, parentItem, newSibling)
        self.m_imageHierarchyTree.Move(hierarchyNode, parentItem.GetData(), newSiblingNode)
