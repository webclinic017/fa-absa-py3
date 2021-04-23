import acm
import FUxCore


def ReallyStartDialog(shell, paths, rowId):
    builder = CreateLayout()
    customDlg = TreeADFLViewerDlg(paths, rowId)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )

def StartDialog(eii, paths, rowId):
    shell = eii.ExtensionObject().Shell()
    ReallyStartDialog(shell, paths, rowId);

class TreeADFLViewerDlg (FUxCore.LayoutDialog):
    def __init__(self, paths, rowId):
        self.m_tree = 0
        self.m_paths = paths
        self.m_rowId = rowId
        
    def HandleApply( self ):
        return 1
    
    @FUxCore.aux_cb
    def TreeContextMenuCB(self, ud, cd):
        
        menuBuilder = cd.At('menuBuilder')
        items = cd.At('items')
        
        objects = acm.FArray()
        
        for item in items:
            objects.Add(item.GetData())
        
        acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, objects, False)
    
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(str(self.m_rowId) + ' - Potential Duplicates')
        self.m_tree = layout.GetControl('tree')
        
        self.m_tree.ShowColumnHeaders()
        self.m_tree.EnableMultiSelect()
        self.m_tree.AddColumn("Value", 100)
        self.m_tree.AddColumn("Handle", 100)
        self.m_tree.ColumnLabel(0, "Name")
        self.m_tree.AddCallback('ContextMenu', self.TreeContextMenuCB, None)
        
        treeRoot = self.m_tree.GetRootItem()
        self.BuildTree( treeRoot, self.m_paths )
        
    def BuildTree( self, root, paths ):
        if not paths:
            return
        keys = paths.keys()
        keys.sort(key=lambda x: x.Entity())
        for eval in keys:
            treeChild = root.AddChild()
            treeChild.SetData(eval)
            treeChild.Label(eval.Entity())
            treeChild.Label(eval.Value(), 1 )
            treeChild.Label(eval.Handle(), 2 )
            for local in eval.Locals():
                lChild = treeChild.AddChild()
                lChild.SetData(local)
                lChild.Label("LOCAL: " + str(local.Entity()))
                lChild.Label(local.Value(), 1 )
                lChild.Label(local.Handle(), 2 )
            self.BuildTree( treeChild, paths[eval] )
    
def CreateLayout():
    b = acm.FUxLayoutBuilder()
    b.BeginHorzBox('None')
    b.  BeginVertBox('None')
    b.          AddTree("tree", 640, 480)
    b.          BeginHorzBox('None')
    b.                  AddFill()
    b.          EndBox()
    b.  EndBox()
    b.EndBox()
    return b
    
