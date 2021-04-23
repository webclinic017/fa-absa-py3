import acm
import FUxCore
  

def Show(shell, caption, initialText, maxLength=-1, checkAlphaNum=False, names = None):
    customDlg = CreateNewHierarchyDialog()
    customDlg.m_caption = caption
    customDlg.m_initialText = initialText
    customDlg.m_maxLength = maxLength
    customDlg.m_checkAlphaNum = checkAlphaNum
    customDlg.m_names = names

    builder = customDlg.CreateLayout()
    
    hierarchy = None
    if acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg ) :
        hierarchy = customDlg.m_hierarchy
        
    return hierarchy
    


    
class CreateNewHierarchyDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_okButton = 0
        self.m_edit = 0
        self.m_initialText = ''
        self.m_caption = 'Input'
        self.m_maxLength = -1
        self.m_checkAlphaNum = False
        self.m_names = None
        self.m_comboCtrl = None
        
    def HandleApply( self ):
        ret = True
        s = self.m_edit.GetData()
        typeName = self.m_comboCtrl.GetData()
        hierarchyType = acm.FHierarchyType[typeName]

        if self.m_checkAlphaNum :
            s = s
            if not s.isalnum():
                s = [x for x in s if x.isalnum() or x == '_'] 
                s = s.lstrip('0123456789')


        if self.m_names != None:
            if s in self.m_names :
                acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'The name ' + s + ' is already used, please select another name')
                self.m_edit.SetTextSelection(0, -1)
                ret = None

        if ret :
            self.m_hierarchy = acm.FHierarchy()
            self.m_hierarchy.Name(s)
            self.m_hierarchy.HierarchyType(hierarchyType)

        return ret

    def OnEditChanged(self, ud, cd):
        self.UpdateControls()
        
    def UpdateControls(self) :
        self.m_okButton.Enabled(len(self.m_edit.GetData()) > 0)
    
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)
        self.m_okButton = layout.GetControl('ok')
        self.m_edit = layout.GetControl('editCtrl')
        self.m_comboCtrl = layout.GetControl('comboBoxCtrl')


        self.m_edit.AddCallback( 'Changed', self.OnEditChanged, self )

        types = acm.FHierarchyType.Select('')
        types = types.SortByProperty('StringKey')
        firstType = None
        for type in types :
            self.m_comboCtrl.AddItem(type.Name())

            if not firstType :
                firstType = type

        if firstType :
            self.m_comboCtrl.SetData(firstType)

        self.m_edit.SetData(self.m_initialText)
        self.m_edit.SetTextSelection(0, -1)
        
        if self.m_maxLength != -1 :
            self.m_edit.MaxTextLength(self.m_maxLength)

        self.UpdateControls()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddOption('comboBoxCtrl', 'Type')
        b.  AddInput('editCtrl', 'Name')
        b.  AddSpace(10)
        b.  BeginHorzBox()
        b.          AddFill()
        b.          AddButton('ok', 'OK')
        b.          AddButton('cancel', 'Cancel')
        b.  EndBox()    
        b.EndBox()
        return b

