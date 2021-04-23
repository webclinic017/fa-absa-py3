"""-----------------------------------------------------------------------------
PURPOSE              :  Custom GUI for amendment reason and type selection.
                        This is triggered from FValidation_cal.
REQUESTER, DEPATMENT :  Nhlanhleni Mchunu, PCG
PROJECT              :  Fix the Front - CAL
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2018-11-13  CHG1001100033  Libor Svoboda       Initial Implementation
"""
import acm
import FUxCore
from cal_config import AMEND_REASONS, AMEND_REASONS_BACKDATE, AMEND_TYPE_BACKDATE


class AmendReasonDialog(FUxCore.LayoutDialog):
    
    caption = ''
    
    def __init__(self):
        self._reason_selection = []
        self._type_selection = []
    
    @classmethod
    def populate_list_control(cls, lc, values):
        lc.RemoveAllItems()
        lc_root = lc.GetRootItem()
        for value in values:
            child = lc_root.AddChild()
            child.SetData(value)
            child.Label(value)
    
    @classmethod
    def select(cls, lc, index=0):
        lc_root = lc.GetRootItem()
        for child_index, child in enumerate(lc_root.Children()):
            if child_index == index:
                child.Select(True)
            else:
                child.Select(False)
    
    def _set_callbacks(self):
        return
    
    def HandleCreate(self, dlg, layout):
        self._fux_dlg = dlg
        self._fux_dlg.Caption(self.caption)
        self._ok_btn = layout.GetControl('ok')
        self._ok_btn.Enabled(False)
        
        self._amend_reason = layout.GetControl('amend_reason')
        self._amend_reason.EnableMultiSelect(False)
        self.populate_list_control(self._amend_reason, self._reason_selection)
        
        self._amend_type = layout.GetControl('amend_type')
        self._amend_type.EnableMultiSelect(False)
        self.populate_list_control(self._amend_type, self._type_selection)
        self._set_callbacks()
    
    def HandleApply(self):
        selected_reason = str(self._amend_reason.GetSelectedItem().GetData())
        selected_type = str(self._amend_type.GetSelectedItem().GetData())
        return {'amend_reason': selected_reason, 
                'amend_type': selected_type}


class AmendReasonDialogStandard(AmendReasonDialog):
    
    caption = 'Please select Amendment reason'
    
    def __init__(self):
        self._reason_selection = list(AMEND_REASONS.keys())
        self._type_selection = []
    
    def _set_callbacks(self):
        self._amend_reason.AddCallback('SelectionChanged', 
                                       self._on_selection_changed_reason, self)
        self._amend_type.AddCallback('SelectionChanged', 
                                     self._on_selection_changed_type, self)
        self.select(self._amend_reason)
    
    def _on_selection_changed_reason(self, _arg1, _arg2):
        selected_item = self._amend_reason.GetSelectedItem()
        if not selected_item:
            self._ok_btn.Enabled(False)
            return
        selected_reason = str(selected_item.GetData())
        type_selection = AMEND_REASONS[selected_reason]
        self.populate_list_control(self._amend_type, type_selection)
        self.select(self._amend_type)
        self._ok_btn.Enabled(True)

    def _on_selection_changed_type(self, _arg1, _arg2):
        selected_item = self._amend_type.GetSelectedItem()
        if not selected_item:
            self.select(self._amend_type)


class AmendReasonDialogBackdate(AmendReasonDialog):
    
    caption = 'Please select Amendment reason and type (Backdate)'
    
    def __init__(self):
        self._reason_selection = AMEND_REASONS_BACKDATE
        self._type_selection = AMEND_TYPE_BACKDATE
    
    def _on_selection_changed(self, _arg1, _arg2):
        selected_reason = self._amend_reason.GetSelectedItem()
        selected_type = self._amend_type.GetSelectedItem()
        if selected_reason and selected_type:
            self._ok_btn.Enabled(True)
        else:
            self._ok_btn.Enabled(False)
    
    def _set_callbacks(self):
        self._amend_reason.AddCallback('SelectionChanged', 
                                       self._on_selection_changed, self)
        self._amend_type.AddCallback('SelectionChanged', 
                                     self._on_selection_changed, self)


def create_layout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.  AddLabel('amend_reason_label', 'Amendment reason')
    b.  AddList('amend_reason', numlines=10, width=80)
    b.  AddLabel('amend_type_label', 'Amendment type')
    b.  AddList('amend_type', numlines=4, width=80)
    b.  BeginHorzBox('None')
    b.    AddFill()
    b.    AddButton('ok', 'OK')
    b.    AddButton('cancel', 'Cancel')
    b.  EndBox()
    b.EndBox()
    return b


def start_dialog(shell, backdate=False):
    builder = create_layout()
    if backdate:
        amend_dialog = AmendReasonDialogBackdate()
    else:
        amend_dialog = AmendReasonDialogStandard()
    result = acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, amend_dialog)
    return result

