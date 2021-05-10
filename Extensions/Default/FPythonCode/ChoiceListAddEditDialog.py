import acm
import FUxCore
  

def Show(shell, caption, choiceList, names = None):
    customDlg = ChoiceListAddEditDialog()
    customDlg.m_caption = caption
    customDlg.m_choiceList = choiceList
    customDlg.m_originalName = choiceList.Name()
    customDlg.m_names = names

    builder = customDlg.CreateLayout()
    
    ret = None
    if acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg ) :
        ret = customDlg.m_choiceList

    return ret
    
class ChoiceListAddEditDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_okButton = None
        self.m_nameInput = None
        self.m_descriptionInput = None
        self.m_choiceList = ''
        self.m_caption = ''
        self.m_names = None
        self.m_originalName = ''
        self.m_maxLength = 39 #max length of name and description
        
    def HandleApply( self ):
        ret = True
        name = self.m_nameInput.GetData()
        description = self.m_descriptionInput.GetData()


        if self.m_names != None:
            if name in self.m_names and name != self.m_choiceList.Name():
                acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'The name ' + name + ' is already used, please select another name')
                self.m_nameInput.SetFocus()
                self.m_nameInput.SetTextSelection(0, -1)


                ret = None

        if ret :
            self.m_choiceList.Name(name)
            self.m_choiceList.Description(description)

        return ret

    def OnEditChanged(self, ud, cd):
        self.UpdateControls()
        
    def UpdateControls(self) :
        self.m_okButton.Enabled(len(self.m_nameInput.GetData()) > 0)
    
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)
        self.m_okButton = layout.GetControl('ok')

        self.m_nameInput = layout.GetControl('nameInput')
        self.m_descriptionInput = layout.GetControl('descriptionInput')
        
        self.m_nameInput.AddCallback( 'Changed', self.OnEditChanged, self )

        self.m_nameInput.SetData(self.m_choiceList.Name())
        self.m_nameInput.SetTextSelection(0, -1)
        self.m_nameInput.MaxTextLength(self.m_maxLength)
        

        self.m_descriptionInput.SetData(self.m_choiceList.Description())
        self.m_descriptionInput.MaxTextLength(self.m_maxLength)

        self.UpdateControls()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddInput('nameInput', 'Name', 50)
        b.  AddInput('descriptionInput', 'Description', 50)
        b.  AddSpace(10)
        b.  BeginHorzBox()
        b.          AddFill()
        b.          AddButton('ok', 'OK')
        b.          AddButton('cancel', 'Cancel')
        b.  EndBox()    
        b.EndBox()
        return b


