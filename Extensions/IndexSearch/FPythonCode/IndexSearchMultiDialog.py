import acm
import FUxCore
import IndexSearchMultiPart
import IndexSearchCreator

from IndexSearchUtils import unicode_encode
from IndexSearchUtils import unicode_decode

s_colCount = 2

def V(info, key) :
    value = info.get(key, '')

    return unicode_encode(value)

class IndexSearchMultiDialog (FUxCore.LayoutDialog):
    def __init__(self, configurations, query = '', pageCount = 10):
        self.m_configurations = configurations
        self.m_indexSearchMultiParts = []
        self.m_openBtn = None
        self.m_searchInput = None
        self.m_query = query

        for index, configuration in enumerate(configurations) :
            indexSearchMultiPart = IndexSearchMultiPart.IndexSearcMultiPart(configuration, 'ctrl' + str(index), pageCount)
            self.m_indexSearchMultiParts.append(indexSearchMultiPart)            

    def HandleApply( self ):
        self.Open()
        return None

    def Caption(self) :
        return 'Index Search'

    def HandleDestroy(self):
        for indexSearchMultiPart in self.m_indexSearchMultiParts :
            indexSearchMultiPart.HandleDestroy()

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.Caption())

        self.m_openBtn = layout.GetControl('ok')
        self.m_searchInput = layout.GetControl('searchInput')
        self.m_searchInput.AddCallback( 'Changed', self.OnSearchChanged, self )
        self.m_searchInput.SetData(self.m_query)
      
        for indexSearchMultiPart in self.m_indexSearchMultiParts :
            indexSearchMultiPart.HandleCreate(layout)

            if self.m_query :
                indexSearchMultiPart.DoSearch(self.m_query, 1)

    def OnSearchChanged(self, ud, cd) :
        query = unicode_decode(self.m_searchInput.GetData())

        for indexSearchMultiPart in self.m_indexSearchMultiParts :
            indexSearchMultiPart.DoSearch(query, 1)

    def BeginHorzBoxIfNeeded(self, builder, index):
        if index % s_colCount == 0 :
            builder.BeginHorzBox()

    def EndBoxIfNeeded(self, builder, index) :
        index += 1
        if index % s_colCount == 0 :
            builder.EndBox()

    def CreateLayout(self) :
        builder = acm.FUxLayoutBuilder()

        builder.BeginVertBox()
        builder.  BeginHorzBox()
        builder.      AddInput('searchInput', '')
        builder.  EndBox()

        for index, indexSearchMultiPart in enumerate(self.m_indexSearchMultiParts) :
            self.BeginHorzBoxIfNeeded(builder, index)
            indexSearchMultiPart.BuildLayoutPart(builder)
            self.EndBoxIfNeeded(builder, index)

        if len(self.m_indexSearchMultiParts) % s_colCount != 0: #need to close the final BeginHorzBox
            builder.EndBox()

        builder.  BeginHorzBox()
        builder.      AddFill()
        builder.      AddButton('ok', 'Open')
        builder.      AddButton('cancel', 'Close')
        builder.  EndBox()
        builder.EndBox()

        return builder

class SelectIndexMultiSearchDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_okButton = None
        self.m_configurations = IndexSearchCreator.get_configurations()
        self.m_selectedConfiguration = None

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Select Index Search')

        self.m_okButton = layout.GetControl('ok')
        self.m_selectIndexControl = layout.GetControl('selectIndexControl')
        self.m_selectIndexControl.ShowCheckboxes(True)
        self.m_selectIndexControl.ShowColumnHeaders(True)

        self.m_selectIndexControl.AddColumn('Index Name', -1)
        configurationNames = []

        root = self.m_selectIndexControl.GetRootItem()

        for configuration in self.m_configurations :
            child = root.AddChild()
            child.Label(unicode_encode(configuration.Identifier()))
            child.SetData(configuration)
            child.Icon('FreezePane')


    def HandleApply( self ):
        selectedItems = self.m_selectIndexControl.GetCheckedItems()
        configurations = []

        for item in selectedItems :
            configurations.append(item.GetData())

        return configurations


    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddList('selectIndexControl', 10)
        b.  BeginHorzBox()
        b.      AddFill()
        b.      AddButton('ok', 'Open')
        b.      AddButton('cancel', 'Close')
        b.  EndBox()
        b.EndBox()

        return b

def ShowIndexSearcMultiDialog(basicApp, indexName, query, pageCount = 20) :
    selectedConfiguration = None
    configurations = IndexSearchCreator.get_configurations()
    for configuration in configurations :
        if indexName == str(configuration.Identifier()) :
            selectedConfiguration = configuration
            break
    
    if selectedConfiguration :
        indexSearchDialog = IndexSearchMultiDialog([selectedConfiguration], query, pageCount)
        builder = indexSearchDialog.CreateLayout()
        acm.UX().Dialogs().ShowCustomDialog(basicApp.Shell(), builder, indexSearchDialog)        

def ReallyStartDialog(basicApp):
    selectIndexSearchDialog = SelectIndexMultiSearchDialog()
    builder = selectIndexSearchDialog.CreateLayout()
    configurations = acm.UX().Dialogs().ShowCustomDialogModal(basicApp.Shell(), builder, selectIndexSearchDialog)

    if configurations :
        indexSearchDialog = IndexSearchMultiDialog(configurations)
        builder = indexSearchDialog.CreateLayout()
        acm.UX().Dialogs().ShowCustomDialog(basicApp.Shell(), builder, indexSearchDialog)

def ShowDialog(eii) :
    basicApp = eii.ExtensionObject()
    ReallyStartDialog(basicApp)
