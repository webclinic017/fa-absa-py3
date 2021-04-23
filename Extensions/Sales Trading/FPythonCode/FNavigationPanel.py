""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FNavigationPanel.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FNavigationPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm
import FIntegratedWorkbenchUtils as utils

from FSalesTradingLogging import logger
from FPanel import Panel
from FBookmarks import FBookmarks
from FEvent import EventCallback
from FIcon import Icon


class NavigationPanel(Panel):

    def __init__(self):
        Panel.__init__(self)
        self._tree = None
        self._topNodes = dict()
        self._topNodeIconName = self.Settings().TopNodeIcon()
        self._mruList = utils.UniqueSizedList(int(self.Settings().MRUDepth()))
        self._bookmarks = FBookmarks(self.Settings().BookmarkKey())

        if self.Settings().OutgoingEvents():
            self._outgoingEvents = utils.GetAttributesInModule(
                self.Settings().OutgoingEvents())
        else:
            self._outgoingEvents = []
        if self.Settings().IncomingEvents():
            self._incomingEvents = utils.GetAttributesInModule(self.Settings().IncomingEvents())
        else:
            self._incomingEvents = []

    def HandleSelectionChanged(self):
        # pylint: disable-msg=W0110
        selItems = self.SelectedObjects()
        if selItems:
            self._SendChangeEvent(filter(lambda item: item and not item.IsDeleted(), selItems))

    def _HandleSearchActivated(self, text):
        allItems = self.ItemsWithData(self._tree.GetRootItem())
        matchingItems = [item for item in allItems
                         if self._ItemMatchesSearchString(item, text)]
        if matchingItems:
            try:
                index = matchingItems.index(self._tree.GetSelectedItem())
                index = index+1 if index < len(matchingItems)-1 else 0
            except ValueError:
                index = 0
            item = matchingItems[index]
            self.CollapseAllAbove(self._tree.GetSelectedItem())
            self._tree.DeselectAllItems()
            item.Select()

    def CollapseAllAbove(self, item):
        item.Collapse()
        if item.Parent():
            item = self.CollapseAllAbove(item.Parent())

    def _ItemMatchesSearchString(self, item, searchString):
        itemName = str(item.GetData().Name()).lower()
        return searchString in itemName

    def Tree(self):
        return self._tree

    def Root(self):
        return self._tree.GetRootItem()

    def SelectedItems(self):
        """ Get the selected tree item. """
        return self._tree.GetSelectedItems()

    def SelectedObjects(self):
        """ Get the objects contained in the selected tree item. """
        def _GetItemData(item):
            if item:
                return item.GetData().Data() if item.GetData() else None
                
        items = self.SelectedItems()
        if items:
            return map(_GetItemData, items)
    
    def SelectedObject(self):
        selectedObjects = self.SelectedObjects()
        if selectedObjects:
            return selectedObjects[0]
        else:
            return None

    def Item(self, data, parent=None):
        """ Get the item that contains given data object. """
        if not parent:
            parent = self.Root()
        for ch in parent.Children():
            if (ch.GetData() != None) and (ch.GetData().Data() == data):
                return ch
            elif ch.ChildrenCount() > 0:
                item = self.Item(data, ch)
                if item:
                    return item
        return None

    def TopNode(self, name):
        """ Return a named top level node. """
        return self._topNodes[name]

    def TopNodeIconName(self, topNodeIconName=None):
        if not topNodeIconName:
            return self._topNodeIconName
        else:
            self._topNodeIconName = topNodeIconName

    def UpdateNodes(self, nodeStruct):
        self._AddNodes(nodeStruct, None)
        self.Tree().ForceRedraw()

    def Items(self, event, selection):
        """ Override in child classes. """
        return selection

    def ItemsWithData(self, treeItem):
        items = [treeItem] if treeItem.GetData() else []
        for child in treeItem.Children():
            items.extend(self.ItemsWithData(child))
        return items

    class Node(object):
        """ Representation of a Node in the tree. """
        def __init__(self, name, subNodes=[], isExpanded=False, data=None, iconName=None):
            # pylint: disable-msg=W0102
            self._name = name
            self._subNodes = subNodes
            self._isExpanded = isExpanded
            self._data = data
            self._iconName = iconName

        def Name(self):
            return self._name

        def SubNodes(self):
            return self._subNodes

        def IsExpanded(self):
            return self._isExpanded

        def Data(self):
            return self._data

        def IconName(self, iconName=None):
            if iconName != None:
                self._iconName = iconName
            else:
                return self._iconName

    def _BookmarkedLabel(self):
        return self.Settings().BookmarkedLabel()

    def _RecentLabel(self):
        return self.Settings().RecentLabel()

    def _AllLabel(self):
        return self.Settings().AllLabel()

    def _MRUList(self):
        return self._mruList

    def _Bookmarks(self):
        return self._bookmarks

    def _SendChangeEvent(self, selection):
        if not self._outgoingEvents:
            logger.error("NavigationPanel._SendChangeEvent() Unknown event class: %s" % (self.Settings().OutgoingEvents()))
            return
        for outgoingEvent in self._outgoingEvents:
            try:
                assert outgoingEvent, 'Unknown event class'
                items = self.Items(outgoingEvent, selection)
                evt = outgoingEvent(self, items)
                self.SendEvent(evt)
            except Exception as stderr:
                logger.error("NavigationPanel._SendChangeEvent() Exception while sending event of type %s: %s" % (outgoingEvent, stderr))
                logger.debug(stderr, exc_info=True)

    def _AddNodes(self, nodeStruct, parentNode):
        if not isinstance(nodeStruct, list):
            logger.error("NavigationPanel._AddNodes() Expected list")
            return

        for node in nodeStruct:
            treeNode = None
            if not isinstance(node, self.Node):
                logger.error("NavigationPanel._AddNodes() Expected list of Node, not list of %s" %(type(node),))
                return

            if parentNode is None:
                if node.Name() in self._topNodes:
                    logger.debug("NavigationPanel._AddNodes() top node '%s' already created, removing children" % node.Name())
                    treeNode = self._topNodes[node.Name()]
                    for cl in treeNode.Children():
                        cl.Remove()
                else:
                    node.IconName(node.IconName() or self.TopNodeIconName())
                    treeNode = self._CreateChild(node)
                    self._topNodes[node.Name()] = treeNode
                    logger.debug("NavigationPanel._AddNodes() creating top node '%s'" % node.Name())
            else:
                treeNode = self._CreateChild(node, parentNode)
            if (type(node.SubNodes()) is list) and (len(node.SubNodes()) > 0) and (type(node.SubNodes()[0]) is self.Node):
                # Nested nodes
                self._AddNodes(node.SubNodes(), treeNode)
            else:
                # List of FObjects
                for obj in node.SubNodes():
                    self._CreateChild(self.Node(obj.Name(),
                                                subNodes=None,
                                                isExpanded=False,
                                                data=obj,
                                                iconName=self._FolderIcon(obj)),
                                      treeNode)
            if node.IsExpanded():
                treeNode.Expand()

    def _CreateChild(self, node, parent=None):
        """ Create a node with given parent, if the parent is None,
        " assume it is the root node. """
        sItem = None
        if not parent:
            sItem = self.Root().AddChild()
        else:
            sItem = parent.AddChild()
        sItem.Label(node.Name())
        sItem.SetData(node)
        icon = node.IconName()
        if icon:
            sItem.Icon(icon, icon)
        return sItem

    def _PopulateTree(self):
        """ Rebuild the tree model. """
        self._topNodes = dict()
        self._tree.RemoveAllItems()
        self.BuildTree()

    def _HandleSelectFirst(self, _dummy):
        self.HandleSelectionChanged()

    def InitControls(self, layout):
        self._tree = layout.GetControl('structTree')
        self._tree.ColumnLabel(0, '')
        self._tree.ColumnWidth(0, self.Settings().Width())
        self._PopulateTree()
        self._EnableMultiSelect()
        self.Shell().CallAsynch(self._HandleSelectFirst, None)

    def _EnableMultiSelect(self):
        self._tree.EnableMultiSelect( self.MultiSelectEnabled() )

    def InitSubscriptions(self):
        Panel.InitSubscriptions(self)
        self._tree.AddCallback('SelectionChanged',
            self.__SelectionChanged, None)
        self._tree.AddCallback('DefaultAction',
            self.__DefaultAction, None)

    def MultiSelectEnabled(self):
        """ Override in child classes. """
        return False

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', '')
        b.  AddTree('structTree', self.Settings().Width(), -1, -1, -1)
        b.EndBox()
        return b

    @EventCallback
    def OnSearchActivated(self, event):
        if event.Class() in self._incomingEvents:
            self._HandleSearchActivated(event.SearchString().lower())

    def __SelectionChanged(self, cd=None, data=None):
        if data:
            self.HandleSelectionChanged()

    def __DefaultAction(self, cd=None, data=None):
        selected = self.SelectedObject()
        if hasattr(selected, 'Class'):
            appName = acm.GetDefaultApplication(selected.Class())
            if appName:
                acm.StartApplication(appName, selected)

    def BuildTree(self):
        """ Delegate the building of the tree to child classes. """
        pass

    @staticmethod
    def _FolderIcon(folder):
        return Icon(folder.StringKey()).GetIcon() or folder.Icon()
