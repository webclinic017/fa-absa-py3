import acm
import FUxCore

def Show(shell, caption, label, warningText):
    customDlg = StartTaskDlg()
    customDlg.m_caption = caption
    customDlg.m_label = label
    customDlg.m_warningText = warningText.split("\n")
    
    builder = customDlg.CreateLayout()
    
    ret = False
    if acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg ) :
        ret = True
        
    return ret

class StartTaskDlg(FUxCore.LayoutDialog):
    def __init__(self):
        self.m_caption = None
        self.m_label = None
        self.m_warningText = None

    def HandleApply(self):
        return True

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        i = 0
        for label in self.m_warningText:
            b.  AddLabel('label%s' % str(i), label)
        b.  AddSpace(10)
        b.  BeginHorzBox()
        b.          AddFill()
        b.          AddButton('ok', 'OK')
        b.          AddButton('cancel', 'Cancel')
        b.  EndBox()    
        b.EndBox()
        return b
