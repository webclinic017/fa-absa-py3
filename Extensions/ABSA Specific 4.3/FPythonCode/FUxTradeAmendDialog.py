import acm
import FUxCore
class AmendmentReasonDialog (FUxCore.LayoutDialog):

    def __init__(self, params):
        self.m_nameEdit = 0
        self.m_fuxDlg = 0
        self.params = params

    def HandleApply(self):
        amendment_reason = self.m_amendmentReason.GetData()
        amendment_reason_detail = self.m_amendmentReasonDetail.GetData()
        return (amendment_reason, amendment_reason_detail)

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        if 'caption' in self.params:
            self.m_fuxDlg.Caption(self.params['caption'])
        self.m_amendmentReason = layout.GetControl("amendmentReason")
        self.m_amendmentReasonDetail = layout.GetControl("amendmentReasonDetail")
        
        voiding = False
        creating_backdated = False
        if 'voiding' in self.params:
            voiding = self.params['voiding']
        if 'creating_backdated' in self.params:
            creating_backdated = self.params['creating_backdated']
            
        if voiding:
            self.m_amendmentReason.Populate(self._get_choice_list_values('AmendReasonVoid'))
        elif creating_backdated:
            self.m_amendmentReason.Populate(self._get_choice_list_values('AmendReasonNewBackdate'))
        else:
            self.m_amendmentReason.Populate(self._get_choice_list_values('AmendReason'))
        if creating_backdated:
            self.m_amendmentReasonDetail.Populate(['Backdate'])
        else:
            amendment_reason_types = self._get_choice_list_values('AmendReasonType')
            if 'Backdate' in amendment_reason_types:
                amendment_reason_types.remove('Backdate')
            self.m_amendmentReasonDetail.Populate(amendment_reason_types)

    def _get_choice_list_values(self, choice_list_name):
        query = 'list = "MASTER" and name = "{0}"'.format(choice_list_name)
        parent_choicelist = acm.FChoiceList.Select01(query, None)
        choices = [choice.Name() for choice in parent_choicelist.Choices()]
        return choices

def StartDialog(eii):
    shell = eii.ExtensionObject().Shell()
    builder = CreateLayout()
    customDlg = AmendmentReasonDialog()
    result = acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg)
    return result

def ShowDialog(shell, params):
    builder = CreateLayout()
    customDlg = AmendmentReasonDialog(params)
    result = acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg)
    return result

def CreateLayout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.AddLabel('amendmentReasonLbl', "Amendment reason:")
    b.AddList('amendmentReason', numlines=10, width=80)
    b.AddLabel('amendmentReasonDetailLbl', "Amendment type:")
    b.AddList('amendmentReasonDetail', numlines=4, width=80)
    b.BeginHorzBox('None')
    b.AddFill()
    b.AddButton('ok', 'OK')
    b.AddButton('cancel', 'Cancel')
    b.EndBox()
    b.EndBox()
    return b


