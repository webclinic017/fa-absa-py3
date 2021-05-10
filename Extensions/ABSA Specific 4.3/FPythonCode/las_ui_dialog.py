"""-----------------------------------------------------------------------------
PURPOSE              :  Legal Agreement Service (LAS) integration
DEVELOPER            :  Libor Svoboda
REQUESTER            :  Victor Mofokeng (CRT desk)
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-11-26  CHG0140652     Libor Svoboda       Initial implementation
"""
import acm
import FUxCore
from las_util import (get_last_step, get_process_for_trade, 
                      AGREEMENTS, STATE_CHART)


def create_legal_data_layout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.  AddInput('trade_input', 'Trade', 70)
    b.  BeginHorzBox('EtchedIn', 'ISDA Agreement')
    b.    AddInput('ISDA_current', 'Current', 70)
    b.    AddOption('ISDA', 'New', 70)
    b.  EndBox()
    b.  BeginHorzBox('EtchedIn', 'IM Agreement')
    b.    AddInput('IM_current', 'Current', 70)
    b.    AddOption('IM', 'New', 70)
    b.  EndBox()
    b.  BeginHorzBox('EtchedIn', 'CSA Agreement')
    b.    AddInput('CSA_current', 'Current', 70)
    b.    AddOption('CSA', 'New', 70)
    b.  EndBox()
    b.  BeginHorzBox('EtchedIn', 'Discount Index')
    b.    AddInput('Discount_Index_current', 'Current', 70)
    b.    AddOption('Discount_Index', 'New', 70)
    b.  EndBox()
    b.  AddSpace(20)
    b.  BeginHorzBox('None')
    b.    AddFill()
    b.    AddButton('ok', 'Update')
    b.    AddButton('cancel', 'Cancel')
    b.  EndBox()
    b.EndBox()
    return b


def show_message_box(shell, message, dialog_type):
    acm.UX().Dialogs().MessageBox(shell, dialog_type, message, 'OK', 
                                  None, None, 'Button1', 'Button1')


class LegalDataDialog(FUxCore.LayoutDialog):
    
    valid_steps = (
        'Complete',
        'Val Group Update Failed',
    )
    
    def __init__(self, trade, process):
        self._trade = trade
        self._params = self.get_params(process)
    
    @classmethod
    def get_params(cls, process):
        if process.CurrentStep().State().Name() not in cls.valid_steps:
            return None
        data_step = get_last_step(process, 'Data Received')
        if not data_step:
            return None
        return data_step.DiaryEntry().Parameters()
    
    def _populate_options(self, control, param_name, isda_control=None):
        control.Clear()
        if not self._params:
            return
        options = ['']
        if not isda_control:
            options.extend(list(self._params['options'].Keys()))
        elif str(isda_control.GetData()):
            options.extend(list(self._params['options'][str(isda_control.GetData())][param_name]))
        options = sorted(list(set(options)))
        for option in options:
            control.AddItem(option)
        control.SetData('')
    
    def _populate_indices(self, control, csa_control):
        control.Clear()
        if not self._params:
            return
        indices = ['']
        if str(csa_control.GetData()) and str(csa_control.GetData()) in self._params['indices']:
            indices.extend(list(self._params['indices'][str(csa_control.GetData())]))
        indices = sorted(list(set(indices)))
        for index in indices:
            control.AddItem(index)
        control.SetData('')
    
    def _populate_current(self, control, param_name):
        control.Clear()
        trade_add_infos = self._trade.AdditionalInfo()
        add_info = getattr(trade_add_infos, AGREEMENTS[param_name])()
        current_value = add_info if add_info else ''
        control.SetData(current_value)
    
    def _on_isda_changed(self, *args):
        self._populate_options(self._im, 'IM', self._isda)
        self._populate_options(self._csa, 'CSA', self._isda)
        self._populate_indices(self._discount_index, self._csa)
    
    def _on_csa_changed(self, *args):
        self._populate_indices(self._discount_index, self._csa)
    
    def _update_add_info(self, trade, control, param_name):
        add_info_name = AGREEMENTS[param_name]
        new_value = str(control.GetData())
        current_value = getattr(self._trade.AdditionalInfo(), add_info_name)()
        if new_value:
            setattr(trade.AdditionalInfo(), add_info_name, new_value)
        elif current_value:
            for add_info in trade.AddInfos()[:]:
                if add_info.AddInf().Name() == add_info_name:
                    trade.AddInfos().Remove(add_info)
    
    def HandleCreate(self, dlg, layout):
        self._dlg = dlg
        self._dlg.Caption('Legal Data')
        self._shell = dlg.Shell()
        self._trade_input = layout.GetControl('trade_input')
        self._trade_input.SetData(str(self._trade.Oid()))
        self._trade_input.Editable(False)
        
        self._isda = layout.GetControl('ISDA')
        self._populate_options(self._isda, 'ISDA')
        self._isda_current = layout.GetControl('ISDA_current')
        self._isda_current.Editable(False)
        self._populate_current(self._isda_current, 'ISDA')
        
        self._im = layout.GetControl('IM')
        self._populate_options(self._im, 'IM', self._isda)
        self._im_current = layout.GetControl('IM_current')
        self._im_current.Editable(False)
        self._populate_current(self._im_current, 'IM')
        
        self._csa = layout.GetControl('CSA')
        self._populate_options(self._csa, 'CSA', self._isda)
        self._csa_current = layout.GetControl('CSA_current')
        self._csa_current.Editable(False)
        self._populate_current(self._csa_current, 'CSA')
        
        self._discount_index = layout.GetControl('Discount_Index')
        self._populate_indices(self._discount_index, self._csa)
        self._discount_index_current = layout.GetControl('Discount_Index_current')
        self._discount_index_current.Editable(False)
        self._populate_current(self._discount_index_current, 'Discount_Index')
        
        self._isda.AddCallback('Changed', self._on_isda_changed, self)
        self._csa.AddCallback('Changed', self._on_csa_changed, self)
    
    def HandleApply(self):
        image = self._trade.StorageImage()
        self._update_add_info(image, self._isda, 'ISDA')
        self._update_add_info(image, self._im, 'IM')
        self._update_add_info(image, self._csa, 'CSA')
        self._update_add_info(image, self._discount_index, 'Discount_Index')
        try:
            image.Commit()
        except Exception as exc:
            msg = 'Failed to update: %s' % str(exc)
            show_message_box(self._shell, msg, 'Error')
            return
        self._populate_current(self._isda_current, 'ISDA')
        self._populate_current(self._im_current, 'IM')
        self._populate_current(self._csa_current, 'CSA')
        self._populate_current(self._discount_index_current, 'Discount_Index')
        show_message_box(self._shell, 'Trade updated', 'Information')


def populate_legal_data(eii):
    ext_object = eii.ExtensionObject()
    shell = ext_object.Shell()
    if ext_object.IsKindOf(acm.FBackOfficeManagerFrame):
        selected_cell = ext_object.ActiveSheet().Selection().SelectedCell()
        process = selected_cell.BusinessObject()
        if not process.IsKindOf(acm.FBusinessProcess):
            msg = 'Only applicable to business process objects.'
            show_message_box(shell, msg, 'Warning')
            return
        if process.StateChart() != STATE_CHART:
            msg = 'Only applicable to "%s" state chart.' % STATE_CHART.Name()
            show_message_box(shell, msg, 'Warning')
            return
        trade = process.Subject()
    elif (ext_object.IsKindOf(acm.FUiTrdMgrFrame) 
            or ext_object.IsKindOf(acm.CInsDefAppFrame)):
        source = (ext_object if ext_object.IsKindOf(acm.CInsDefAppFrame)
                  else ext_object.ActiveSheet().Selection().SelectedCell().BusinessObject())
        trade = source.OriginalTrade()
        process = get_process_for_trade(trade)
        if not process:
            msg = 'Business process not found for "%s" state chart.' % STATE_CHART.Name()
            show_message_box(shell, msg, 'Warning')
            return
    else:
        msg = 'Invalid App Frame "%s".' % type(ext_object)
        show_message_box(shell, msg, 'Warning')
        return
    layout = create_legal_data_layout()
    dialog = LegalDataDialog(trade, process)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, layout, dialog)
