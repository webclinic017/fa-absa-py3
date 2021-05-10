""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FInstrumentNavigationPanel.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FInstrumentNavigationPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm
import FEvent

from FSalesTradingLogging import logger
from FNavigationPanel import NavigationPanel
from FIntegratedWorkbenchUtils import IsKindOf, RemoveDuplicates, UniqueSizedList
from FBookmarks import FBookmarks
from FEvent import EventCallback


class InstrumentNavigationPanel(NavigationPanel):

    def __init__(self):
        NavigationPanel.__init__(self)
        self._rootPageGroupName = self.Settings().RootPageGroupName()

    def BuildTree(self):
        struct = [self.Node(self._BookmarkedLabel(), self._bookmarks.Get(), True, self._Bookmarks()),
                  self.Node(self._RecentLabel(), [], True, self._MRUList()),
                  self._PageGroupNodes()]
        self.UpdateNodes(struct)

    def Items(self, event, selection):
        selectedItems = NavigationPanel.Items(self, event, selection)
        items = acm.FArray()
        if FEvent.OnInstrumentsSelected in event.__bases__:
            for item in selectedItems:
                if IsKindOf(item, acm.FPageGroup):
                    items.AddAll(item.InstrumentsRecursively())
                elif isinstance(item, FBookmarks):
                    items.AddAll(item.GetBookmarksAsList())
                elif isinstance(item, UniqueSizedList):
                    items.AddAll(item.Items())
                else:
                    items.Add(item)
        return sorted(RemoveDuplicates(items))
        
    def MultiSelectEnabled(self):
        return True

    # ---- Event handling ----

    @EventCallback
    def OnTrade(self, event):
        instr = event.Trade().Instrument()
        self._MRUList().AddUnique(instr)

        mruSel = self._MRUInstrumentsQuery(self._MRUList().Items()).Select()
        struct = [self.Node(self._RecentLabel(), mruSel, True, self._MRUList())]
        self.UpdateNodes(struct)

    @EventCallback
    def OnBookmark(self, event):
        logger.debug("InstrumentNavigationPanel.OnBookmark()")
        struct = [self.Node(self._BookmarkedLabel(), self._Bookmarks().Get(), True, self._Bookmarks())]
        self.UpdateNodes(struct)

    def _MRUInstrumentsQuery(self, mruList=None):
        if not mruList:
            return None
        query = acm.CreateFASQLQuery('FInstrument', 'OR')
        for conv in mruList:
            query.AddOpNode('OR')
            query.AddAttrNode('Oid', 'EQUAL', conv.Oid())
        return query

    def _PageGroupNodes(self, pageGroup=None):
        if not pageGroup:
            rootPageGroup = acm.FPageGroup[self._rootPageGroupName]
            if rootPageGroup:
                allInstrumentsRoot = self._PageGroupNodes(rootPageGroup)
                return self.Node(self._AllLabel(), allInstrumentsRoot, True, rootPageGroup)
            else:
                logger.error("InstrumentNavigationPanel._PageGroupNodes()"
                             " Invalid root name: %s" % self._rootPageGroupName)
                return None
        else:
            nodeList = []
            for sg in pageGroup.SubGroups().SortByProperty('Name'):
                nodeCaption = sg.Name() + ' [' + str(len(sg.InstrumentsRecursively())) + ']'
                nodeList.append(self.Node(nodeCaption,
                                          subNodes=self._PageGroupNodes(sg),
                                          isExpanded=False,
                                          data=sg,
                                          iconName=self._FolderIcon(sg)))
            instruments = acm.FArray()
            instruments.AddAll([leaf.Instrument() for leaf in pageGroup.Leafs()])
            for instrument in instruments.SortByProperty('Name'):
                nodeList.append(self.Node(instrument.Name(),
                                          isExpanded=False,
                                          data=instrument,
                                          iconName=instrument.Icon()))
            return nodeList