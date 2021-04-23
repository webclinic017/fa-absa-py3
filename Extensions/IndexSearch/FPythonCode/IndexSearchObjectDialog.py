from __future__ import print_function
import acm
import FUxCore
import IndexSearchDialog
import IndexSearchCreator

from IndexSearchUtils import unicode_encode
from IndexSearchUtils import unicode_decode



def V(info, key) :
    value = info.get(key, '')

    return unicode_encode(value)

class IndexSearchObjectDialog (IndexSearchDialog.IndexSearchDialog):
    def __init__(self, configuration, query = ''):
        self.m_columnKeys = configuration.IndexAttributes()
        self.m_indexName = configuration.Identifier()

        IndexSearchDialog.IndexSearchDialog.__init__(self, query)

    def PopulateColumns(self):
        self.m_list.AddColumn('Terms matched', 100)

        for key in self.m_columnKeys :
            self.m_list.AddColumn(key, 100)

    def IndexName(self) :
        return self.m_indexName

    def Caption(self) :
        return str(self.m_indexName) +' Index Search'

    def ObjectFromInfo(self, info) :
        obj = None
        try:
            m  = info['moniker']
            obj = acm.Hgc().ResolveMoniker(m.SerializeToString(), 'any')
        except Exception as e :
            print (e)

        return obj

    def Open(self) :
        item = self.m_list.GetSelectedItem()
        if item :
            info = item.GetData()
            if info :
                obj = self.ObjectFromInfo(info)
                if obj :
                    applicationName = acm.UX().SessionManager().GetDefaultApplicationForDocument(obj.Class())
                    acm.UX().SessionManager().StartApplication(applicationName, obj)


    def BuildContextMenu(self, menuBuilder):
        item = self.m_list.GetSelectedItem()
        if item :
            info = item.GetData()
            obj = self.ObjectFromInfo(info)
            if obj :
                acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, [obj], False, None, None)


    def GetSafeIcon(self, info) :
        icon = None
        try :
            icon = info['icon']
        except:
            pass

        if not icon :
            icon = 'OpenFolder'

        return str(icon)

    def AddListItem(self, root, info, select) :
        child = root.AddChild()
        child.Label(unicode_encode(info['terms']), 0)
        for index, key in enumerate(self.m_columnKeys) :
            child.Label(unicode_encode(info[unicode_decode(key)]), index + 1)

        child.Icon(self.GetSafeIcon(info))
        child.SetData(info)
        child.Select(select)

class SelectIndexSearchDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_okButton = None
        self.m_configurations = IndexSearchCreator.get_configurations()
        self.m_selectedConfiguration = None

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Select Index Search')

        self.m_okButton = layout.GetControl('ok')
        self.m_selectIndexControl = layout.GetControl('selectIndexControl')

        configurationNames = []

        for configuration in self.m_configurations :
            configurationNames.append(str(configuration.Identifier()))            

        configurationNames.sort()
        
        firstName = None
        for name in configurationNames :
            self.m_selectIndexControl.AddItem(name)
            if not firstName :
                firstName = name

        self.m_selectIndexControl.SetData(firstName)

        

    def HandleApply( self ):
        selectedName = str(self.m_selectIndexControl.GetData())
        for configuration in self.m_configurations :
            if selectedName == str(configuration.Identifier()) :
                self.m_selectedConfiguration = configuration
                break

        return self.m_selectedConfiguration


    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddOption('selectIndexControl', 'Select Index')
        b.  BeginHorzBox()
        b.      AddFill()
        b.      AddButton('ok', 'Open')
        b.      AddButton('cancel', 'Close')
        b.  EndBox()
        b.EndBox()

        return b


def ShowIndexSearchDialog(basicApp, indexName, query) :
    selectedConfiguration = None
    configurations = IndexSearchCreator.get_configurations()
    for configuration in configurations :
        if indexName == str(configuration.Identifier()) :
            selectedConfiguration = configuration
            break
    
    if selectedConfiguration :
        indexSearchDialog = IndexSearchObjectDialog(selectedConfiguration, query)
        builder = indexSearchDialog.CreateLayout()
        acm.UX().Dialogs().ShowCustomDialog(basicApp.Shell(), builder, indexSearchDialog)        


def ReallyStartDialog(basicApp):
    selectIndexSearchDialog = SelectIndexSearchDialog()
    builder = selectIndexSearchDialog.CreateLayout()
    configuration = acm.UX().Dialogs().ShowCustomDialogModal(basicApp.Shell(), builder, selectIndexSearchDialog)

    if configuration :
        indexSearchDialog = IndexSearchObjectDialog(configuration)
        builder = indexSearchDialog.CreateLayout()
        acm.UX().Dialogs().ShowCustomDialog(basicApp.Shell(), builder, indexSearchDialog)

def ShowDialog(eii) :
    basicApp = eii.ExtensionObject()
    ReallyStartDialog(basicApp)
