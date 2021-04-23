"""
    ConfirmationDiaryDialog
    
    Fix for Confirmation Diary viewer for AR 749833
"""
import acm
import FUxCore

def get_Conf_Diary_Text(conf):
    # Remove the DateTime tags and return the txt
    dt = ''
    dict = {
        '<DateTime><Date><Year>' : '',
        '</Year><Month>' : '-',
        '</Month><Day>' : '-',
        '</Day></Date><Time><Hour>' : ' ',
        '</Hour><Min>' : ':',
        '</Min><Sec>' : ':',
        '</Sec><MSec>' : ':',
        '</MSec></Time></DateTime>' : ' UTC'
        }

    if conf.Diary():
        dt = conf.Diary().Text()
        for entry in list(dict.keys()):
            dt = dt.replace(entry, dict[entry]) 
    return dt

class ConfirmationDiaryDlg(FUxCore.LayoutDialog):

    def __init__(self, params):
        self.m_fuxDlg = 0
        self.m_oldDiaryText = 0
        self.m_newDiaryText = 0
        self.m_confirmation_list = params["confirmation_list"]

    def HandleApply( self ):
        return self.m_newDiaryText.GetData()

    def HandleCancel(self):
        return True

    def PopulateData(self):
        if len(self.m_confirmation_list) == 1:
            confo = self.m_confirmation_list[0]
            self.m_oldDiaryText.SetData(get_Conf_Diary_Text(confo) if confo and confo.Diary() else '')
            
    def UpdateControls(self):
        self.m_oldDiaryText.Editable(False)

    def HandleCreate( self, dlg, layout ):
        self.m_fuxDlg = dlg
        caption = 'Fill in diary'
        if len(self.m_confirmation_list) == 1:
            caption = caption + ' - Confirmation %s' %(self.m_confirmation_list[0].Oid())
        self.m_fuxDlg.Caption(caption)
        self.m_oldDiaryText = layout.GetControl("oldDiaryText")
        self.m_newDiaryText = layout.GetControl("newDiaryText")
        self.PopulateData()
        self.UpdateControls()
        self.m_newDiaryText.SetFocus()

def CreateLayout():
    b = acm.FUxLayoutBuilder()
    b.  BeginVertBox('None')
    b.    AddText("oldDiaryText", 300, 150, 1000, 1000)
    b.    AddText("newDiaryText", 300, 100, 1000, 1000)
    b.    BeginHorzBox()
    b.      AddFill()
    b.      AddButton('cancel', '&&Cancel')
    b.      AddButton('ok', '&&Save')
    b.    EndBox()
    b.  EndBox()
    return b
        
def StartDialog(eii):
    params = {}
    confo_list = []
    selection = eii.ExtensionObject().ActiveSheet().Selection()
    cells = selection.SelectedCells()
    if len(cells) > 0:
        for cell in cells:
            confo = cell.RowObject().Confirmation()
            if confo and confo not in confo_list:
                confo_list.append(confo)
    
    params["confirmation_list"] = confo_list
            
    shell = eii.ExtensionObject().Shell()
    builder = CreateLayout()
    custom_dlg = ConfirmationDiaryDlg(params)
    diary_entry = acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, custom_dlg)

    if diary_entry:
        for confo in confo_list:
            confo.AddDiaryNote(diary_entry)
