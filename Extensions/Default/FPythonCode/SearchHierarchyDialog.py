import acm
import FUxCore
import fnmatch
import unicodedata


def Show(shell, caption, searchableItems, selectItemCB):
    customDlg = SearchHierarchyDialog(searchableItems, selectItemCB)
    customDlg.m_caption = caption

    builder = customDlg.CreateLayout()
    
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )
    


    
class SearchHierarchyDialog (FUxCore.LayoutDialog):
    def __init__(self, searchableItems, selectItemCB):
        self.m_searchButton = 0
        self.m_searchableItems = searchableItems
        self.m_selectItemCB = selectItemCB
        

    def HandleApply( self ):
        return True

    def HandleCancel(self):
        return True

    def OnInputChanged(self, ud, cd):
        self.Populate()

    def OnSearch(self, ud, cd) :
        self.Populate()

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)

        self.m_hierarchyList = layout.GetControl('hierarchyList')

        self.m_searchButton = layout.GetControl('searchButton')
        self.m_searchButton.AddCallback('Activate', self.OnSearch, None)

        self.m_searchInput = layout.GetControl('searchInput')
        self.m_searchInput.AddCallback('Activate', self.OnSearch, self)
        self.m_searchInput.SetFocus()

        self.m_hierarchyList.AddColumn('Name')
        self.m_hierarchyList.AddColumn('Path')
        self.m_hierarchyList.ShowColumnHeaders(True)
        self.m_hierarchyList.AddCallback('SelectionChanged', self.OnSearchHierarchyListChanged, self)
        self.m_hierarchyList.AddCallback('DefaultAction', self.OnSearchHierarchyDefaultAction, self)
        self.m_hierarchyList.EnableHeaderSorting(True)
    
    def Populate(self) :
        self.m_hierarchyList.RemoveAllItems()
        root = self.m_hierarchyList.GetRootItem()

        query = self.m_searchInput.GetData()
        query = query.lower()
        

        for searchItem in self.m_searchableItems :
            if not query or searchItem.MatchAll(query) :
                child = root.AddChild()
                child.Label(searchItem.DisplayName())
                child.Label(searchItem.PathAsString(), 1)

                icon = 'Tree'
                if searchItem.Node().IsLeaf() :
                    icon = 'TreeSimulate'

                child.Icon(icon, icon)
                child.SetData(searchItem)

    def OnSearchHierarchyListChanged(self, ud, cd):
        item = self.m_hierarchyList.GetSelectedItem()

        if item:
            searchItem = item.GetData()
            self.m_selectItemCB(searchItem.Node())

    def OnSearchHierarchyDefaultAction(self, ud, cd) :
        self.m_fuxDlg.CloseDialogOK()        

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox()
        b.  BeginVertBox()
        b.      BeginHorzBox()
        b.          AddInput('searchInput', 'Name')
        b.          AddButton('searchButton', 'Search')
        b.      EndBox()
        b.      AddList('hierarchyList', 12, -1, 80)
        b.      AddSpace(5)
        b.      BeginHorzBox()
        b.          AddFill()
        b.          AddButton('cancel', 'Close')
        b.      EndBox()
        b.  EndBox()
        b.EndBox()

        return b

