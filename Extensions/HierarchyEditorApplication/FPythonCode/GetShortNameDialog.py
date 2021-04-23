import acm
import FUxCore
  

def Show(shell, caption, label, initialText, maxLength=-1, checkAlphaNum=False, names = None):
    customDlg = GetShortNameDlg()
    customDlg.m_caption = caption
    customDlg.m_label = label
    customDlg.m_initialText = initialText
    customDlg.m_maxLength = maxLength
    customDlg.m_checkAlphaNum = checkAlphaNum
    customDlg.m_names = names

    builder = customDlg.CreateLayout()
    
    text = None
    if acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg ) :
        text = customDlg.m_text
        
    return text
    


    
class GetShortNameDlg (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_okButton = 0
        self.m_edit = 0
        self.m_initialText = ''
        self.m_text = ''
        self.m_label = ''
        self.m_caption = 'Input'
        self.m_maxLength = -1
        self.m_checkAlphaNum = False
        self.m_names = None
        
    def HandleApply( self ):
        ret = True
        s = self.m_edit.GetData()

        if self.m_checkAlphaNum :
            s = s
            if not s.isalnum():
                s = [x for x in s if x.isalnum() or x == '_'] 
                s = s.lstrip('0123456789')


        if self.m_names != None:
            if s in self.m_names :
                acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'The name ' + s + ' is already used, please select another name')
                self.m_edit.SetFocus()
                self.m_edit.SetTextSelection(0, -1)


                ret = None

        self.m_text = s

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
        
        self.m_edit.AddCallback( 'Changed', self.OnEditChanged, self )

        self.m_edit.SetData(self.m_initialText)
        self.m_edit.SetTextSelection(0, -1)
        
        if self.m_maxLength != -1 :
            self.m_edit.MaxTextLength(self.m_maxLength)

        self.UpdateControls()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddInput('editCtrl', self.m_label, 50)
        b.  AddSpace(10)
        b.  BeginHorzBox()
        b.          AddFill()
        b.          AddButton('ok', 'OK')
        b.          AddButton('cancel', 'Cancel')
        b.  EndBox()    
        b.EndBox()
        return b

