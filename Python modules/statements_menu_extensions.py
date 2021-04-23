"""-----------------------------------------------------------------------------
PURPOSE              :  Client Valuation Statements Automation
                        This module implements user-side functionality 
                        (e.g. release statement, preview files, adhoc statement)
                        accessible through corresponding FMenuExtensions.
DESK                 :  PCG Collateral
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2019-02-14  CHG1001362755  Libor Svoboda       Initial Implementation (FEC)
2019-03-14  CHG1001488095  Libor Svoboda       Enable Option statements
2019-04-12  CHG1001590405  Libor Svoboda       Enable Swap, Cap & Floor, and 
                                               Structured Deal statements
2020-06-03  CHG0103217     Libor Svoboda       Add SBL client statements
2020-06-23  CHG0108121     Libor Svoboda       Enable bulk manual requests
"""
import json
import os
import time
from collections import defaultdict, OrderedDict

import acm
import FUxCore

from statements_config import STATEMENTS, get_bp_config
from statements_params import STATE_CHART, DATE_PATTERN_MONTH
from statements_util import get_last_step, can_user_force, format_date


CALENDAR = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time.DateToday()


def create_cto(cto_name):
    cto = acm.FCustomTextObject()
    cto.Name(cto_name)
    cto.SubType('Statements')
    return cto


def update_cto(cto_name, data_dict):
    cto = acm.FCustomTextObject[cto_name]
    if not cto:
        cto = create_cto(cto_name)
    text = json.dumps(data_dict)
    cto.Text(text)
    cto.Commit()


def show_message_box(shell, message, dialog_type):
    acm.UX().Dialogs().MessageBox(shell, dialog_type, message, 'OK', 
                                  None, None, 'Button1', 'Button1')


def manual_request(eii, event='', force=False):
    ops_manager = eii.ExtensionObject()
    shell = ops_manager.Shell()
    if not ops_manager.IsKindOf(acm.FBackOfficeManagerFrame):
        return
    sheet = ops_manager.ActiveSheet()
    selection = sheet.Selection()
    requested = []
    for selected_cell in selection.SelectedRowCells():
        bp = selected_cell.BusinessObject()
        if not bp.IsKindOf(acm.FBusinessProcess):
            msg = 'Row %s: Only applicable to business process objects.' % str(bp)
            show_message_box(shell, msg, 'Warning')
            continue
        if not bp.StateChart() == STATE_CHART:
            msg = ('Business process %s: Only applicable to "%s" state chart.' 
                   % (bp.Oid(), STATE_CHART.Name()))
            show_message_box(shell, msg, 'Warning')
            continue
        can_handle = bp.CanHandleEvent(event) 
        if not can_handle and not force:
            msg = ('Business process %s: Not in the right state,'
                   ' cannot handle event "%s".' % (bp.Oid(), event))
            show_message_box(shell, msg, 'Warning')
            continue
        elif not can_handle and force:
            can_force, msg = can_user_force(bp, event)
            if not can_force:
                msg = 'Business process %s: %s' % (bp.Oid(), msg)
                show_message_box(shell, msg, 'Warning')
                continue
        step_id = bp.CurrentStep().Oid()
        data_dict = {
            'step_id': str(step_id),
            'event': event,
            'user': acm.User().Name(),
            'time': str(int(time.time())),
        }
        cto_name = 'Statements_%s_%s_%s' % (data_dict['user'], data_dict['step_id'],
                                            data_dict['event'])
        try:
            update_cto(cto_name, data_dict)
        except Exception as exc:
            msg = ('Business process %s: Failed to commit "%s" event request: %s' 
                    % (bp.Oid(), event, str(exc)))
            show_message_box(shell, msg, 'Error')
        else:
            requested.append(str(bp.Oid()))
    if requested:
        msg = 'Processing user request for %s.' % ', '.join(requested)
        show_message_box(shell, msg, 'Information')


def manual_release(eii):
    manual_request(eii, 'Manual Release')


def cancel(eii):
    manual_request(eii, 'Cancel')


def resend(eii):
    manual_request(eii, 'Resend')


def reset_process(eii):
    manual_request(eii, 'Reset Process')


def request_document(eii):
    manual_request(eii, 'Request Document')


def force_pending_calculation(eii):
    manual_request(eii, 'Pending Calculation', True)


def force_pending_send(eii):
    manual_request(eii, 'Pending Send', True)


def preview_file(eii, file_param=''):
    ops_manager = eii.ExtensionObject()
    shell = ops_manager.Shell()
    if not ops_manager.IsKindOf(acm.FBackOfficeManagerFrame):
        return
    sheet = ops_manager.ActiveSheet()
    selection = sheet.Selection()
    selected_cell = selection.SelectedCell()
    bp = selected_cell.BusinessObject()
    if not bp.IsKindOf(acm.FBusinessProcess):
        msg = 'Only applicable to business process objects.'
        show_message_box(shell, msg, 'Warning')
        return
    generated_step = get_last_step(bp, 'Generated')
    if not generated_step:
        msg = 'File has not been generated yet.'
        show_message_box(shell, msg, 'Warning')
        return
    params = generated_step.DiaryEntry().Parameters()
    file_name = params[file_param] if params.HasKey(file_param) else ''
    if not file_name:
        msg = 'Preview not available, file path was not specified.'
        show_message_box(shell, msg, 'Error')
        return
    val_date = bp.AdditionalInfo().BP_ValuationDate()
    config = get_bp_config(bp)
    if not config:
        msg = 'No statements config found for BP %s.' % bp.Oid()
        show_message_box(shell, msg, 'Error')
        return
    preview_dir = config.process_class.get_preview_dir(val_date)
    file_path = os.path.join(preview_dir, file_name)
    if not os.path.exists(file_path):
        msg = 'Preview not available yet, please try again in a few minutes.'
        show_message_box(shell, msg, 'Information')
        return
    os.startfile(file_path)


def preview_pdf(eii):
    preview_file(eii, 'pdf_file')


def preview_xlsx(eii):
    preview_file(eii, 'xlsx_file')


def create_ad_hoc_statement_layout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.AddOption('party_name', 'Party name', 70)
    b.AddOption('statement_type', 'Statement type', 70)
    b.AddOption('contact', 'Contact', 70)
    b.AddInput('val_date', 'Valuation date', 70)
    b.AddSpace(20)
    b.BeginHorzBox('None')
    b.AddFill()
    b.AddButton('ok', 'Request')
    b.AddButton('cancel', 'Cancel')
    b.EndBox()
    b.EndBox()
    return b


def create_ad_hoc_statement_date_period_layout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.AddOption('party_name', 'Party name', 70)
    b.AddOption('statement_type', 'Statement type', 70)
    b.AddOption('contact', 'Contact', 70)
    b.AddOption('val_date', 'Date Period', 70)
    b.AddSpace(20)
    b.BeginHorzBox('None')
    b.AddFill()
    b.AddButton('ok', 'Request')
    b.AddButton('cancel', 'Cancel')
    b.EndBox()
    b.EndBox()
    return b


def create_ad_hoc_statement_start_end_layout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.AddOption('party_name', 'Party name', 70)
    b.AddOption('statement_type', 'Statement type', 70)
    b.AddOption('contact', 'Contact', 70)
    b.AddInput('start_date', 'Start date', 70)
    b.AddInput('end_date', 'End date', 70)
    b.AddSpace(20)
    b.BeginHorzBox('None')
    b.AddFill()
    b.AddButton('ok', 'Request')
    b.AddButton('cancel', 'Cancel')
    b.EndBox()
    b.EndBox()
    return b


def ad_hoc_statement(eii, layout_def, dialog_class):
    ext_obj = eii.ExtensionObject()
    shell = ext_obj.Shell()
    party = None
    if ext_obj.IsKindOf(acm.CPartyDefinitionFrame):
        party = ext_obj.CurrentObject()
    ad_hoc_dialog = dialog_class(party)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, layout_def, ad_hoc_dialog)

    
def ad_hoc_valuation_statement(eii):
    layout = create_ad_hoc_statement_layout()
    ad_hoc_statement(eii, layout, AdHocValuationStatement)


def ad_hoc_sbl_fee_statement(eii):
    layout = create_ad_hoc_statement_date_period_layout()
    ad_hoc_statement(eii, layout, AdHocSBLFeeStatement)


def ad_hoc_sbl_finder_fee_statement(eii):
    layout = create_ad_hoc_statement_date_period_layout()
    ad_hoc_statement(eii, layout, AdHocSBLFinderFeeStatement)


def ad_hoc_sbl_movement_statement(eii):
    layout = create_ad_hoc_statement_start_end_layout()
    ad_hoc_statement(eii, layout, AdHocSBLMovementStatement)


def ad_hoc_sbl_open_pos_coll_statement(eii):
    layout = create_ad_hoc_statement_layout()
    ad_hoc_statement(eii, layout, AdHocSBLOpenPosCollStatement)


def ad_hoc_sbl_open_pos_ops_statement(eii):
    layout = create_ad_hoc_statement_layout()
    ad_hoc_statement(eii, layout, AdHocSBLOpenPosOpsStatement)


def ad_hoc_sbl_summary_open_pos_statement(eii):
    layout = create_ad_hoc_statement_layout()
    ad_hoc_statement(eii, layout, AdHocSBLSummaryOpenPosStatement)


def ad_hoc_sbl_margin_call_statement(eii):
    layout = create_ad_hoc_statement_layout()
    ad_hoc_statement(eii, layout, AdHocSBLMarginCallStatement)


def ad_hoc_sbl_dividend_notification(eii):
    layout = create_ad_hoc_statement_layout()
    ad_hoc_statement(eii, layout, AdHocSBLDividendNotification)


class InvalidDate(Exception):
    pass


class AdHocDialog(FUxCore.LayoutDialog):
    
    event = ''
    allow_today = False
    default_date = CALENDAR.AdjustBankingDays(TODAY, -1)
    
    def __init__(self, party):
        self._party = party
        self._statement_types = defaultdict(list)
    
    @classmethod
    def is_future_date(cls, date):
        if cls.allow_today:
            return date > TODAY
        return date >= TODAY
    
    def _on_statement_type_changed(self, *args):
        self._contact.Clear()
        statement_type = str(self._statement_type.GetData())
        if not statement_type in self._statement_types:
            return
        contacts = self._statement_types[statement_type]
        self._contact.Populate(contacts)
        self._contact.SetData(contacts[0])
    
    def _on_party_changed(self, *args):
        party = self._party if self._party else self._party_name.GetData()
        self._statement_types = defaultdict(list)
        for contact in party.Contacts():
            for name, config in STATEMENTS.items():
                if config.matches(contact) and config.event == self.event:
                    self._statement_types[name].append(contact)
        self._statement_type.Clear()
        for key in self._statement_types:
            self._statement_type.AddItem(key)
            self._statement_type.SetData(key)
        self._on_statement_type_changed()
        
    def _set_defaults(self):
        if self._party:
            self._party_name.AddItem(self._party)
            self._party_name.SetData(self._party)
            self._party_name.Editable(False)
        else:
            parties = acm.FParty.Select('type in ("Client", "Counterparty")')
            self._party_name.Populate(parties)
            self._party_name.SetData(parties[0])
        self._on_party_changed()
    
    def _set_date(self, date_obj, date_string=''):
        if not date_string:
            date_string = self.default_date
        date_obj.SetData(date_string)
    
    def _get_date(self, date_obj, field_name='Date'):
        date = str(date_obj.GetData()).strip()
        try:
            non_bank_day = CALENDAR.IsNonBankingDay(None, None, date)
        except:
            msg = 'Invalid %s, please specify as YYYY-MM-DD.' % field_name
            raise InvalidDate(msg)
        if non_bank_day:
            msg = '%s is a non business day.' % field_name
            raise InvalidDate(msg)
        if self.is_future_date(date):
            msg = 'Future %s.' % field_name
            raise InvalidDate(msg)
        return date
    
    def _set_dates(self, layout):
        self._val_date = layout.GetControl('val_date')
        self._set_date(self._val_date)
    
    def HandleCreate(self, dlg, layout):
        self._dlg = dlg
        self._dlg.Caption('Adhoc %s' % self.event)
        self._shell = dlg.Shell()
        self._party_name = layout.GetControl('party_name')
        self._party_name.AddCallback('Changed', self._on_party_changed, self)
        self._statement_type = layout.GetControl('statement_type')
        self._statement_type.AddCallback('Changed', self._on_statement_type_changed, self)
        self._contact = layout.GetControl('contact')
        self._set_dates(layout)
        self._set_defaults()
    
    def HandleApply(self):
        if not self._statement_types:
            msg = ('Statements settings not found,'
                   ' please set up contact rules first.')
            show_message_box(self._shell, msg, 'Error')
            return
        try:
            val_date = self._get_date(self._val_date, 'Valuation date')
        except InvalidDate as exc:
            show_message_box(self._shell, str(exc), 'Error')
            return
        statement_type = str(self._statement_type.GetData())
        config = STATEMENTS[statement_type]
        party = self._party if self._party else self._party_name.GetData()
        contact = self._contact.GetData()
        bps = config.find_bps(contact, val_date)
        if bps:
            bp = bps[0]
            current_state = bp.CurrentStep().State().Name()
            msg = ('Business process already exists (%s, %s) for %s statement,'
                   ' %s, the specified contact and %s.' 
                   % (bp.Oid(), current_state, 
                      statement_type, party.Name(), val_date))
            show_message_box(self._shell, msg, 'Error')
            return
        data_dict = {
            'event': 'New',
            'contact_id': str(contact.Oid()),
            'val_date': val_date,
            'statement': statement_type,
            'user': acm.User().Name(),
            'time': str(int(time.time())),
        }
        cto_name = 'Statements_%s_%s_%s_%s' % (data_dict['user'], data_dict['contact_id'],
                                               data_dict['val_date'], data_dict['event'])
        try:
            update_cto(cto_name, data_dict)
        except Exception as exc:
            msg = 'Failed to commit statement request: %s' % str(exc)
            show_message_box(self._shell, msg, 'Error')
        else:
            msg = 'Statement request sent successfully.'
            show_message_box(self._shell, msg, 'Information')


class AdHocValuationStatement(AdHocDialog):
    
    event = 'Valuation Statement'


class AdHocSBLFeeStatement(AdHocDialog):
    
    event = 'SBL Fee Statement'
    periods_count = 12
    
    @classmethod
    def generate_date_periods(cls):
        fom_today = acm.Time.FirstDayOfMonth(TODAY)
        fom_dates = [acm.Time.DateAddDelta(fom_today, 0, -i, 0) 
                     for i in range(cls.periods_count)]
        dates = [CALENDAR.AdjustBankingDays(fom, -1) for fom in fom_dates]
        date_periods = OrderedDict()
        for date in dates:
            date_periods[format_date(date, DATE_PATTERN_MONTH)] = date
        return date_periods
    
    def _set_date(self, date_obj):
        self._date_periods = self.generate_date_periods()
        if not self._date_periods:
            return
        for date_period in self._date_periods:
            date_obj.AddItem(date_period)
        date_obj.SetData(list(self._date_periods.keys())[0])
    
    def _get_date(self, date_obj, _field_name):
        date_period = str(date_obj.GetData())
        if date_period in self._date_periods:
            return self._date_periods[date_period]
        raise InvalidDate('Date period not recognized')


class AdHocSBLFinderFeeStatement(AdHocSBLFeeStatement):
    
    event = 'SBL Finder Fee Statement'


class AdHocSBLMovementStatement(AdHocDialog):
    
    event = 'SBL Movement Statement'
    allow_today = True
    
    def _set_dates(self, layout):
        self._start_date = layout.GetControl('start_date')
        self._set_date(self._start_date)
        self._end_date = layout.GetControl('end_date')
        self._set_date(self._end_date, TODAY)
    
    def _get_date(self, date_obj, field_name='Date'):
        date = str(date_obj.GetData()).strip()
        try:
            date = acm.Time.FromDate(date)[:10]
        except:
            msg = 'Invalid %s, please specify as YYYY-MM-DD.' % field_name
            raise InvalidDate(msg)
        if self.is_future_date(date):
            msg = 'Future %s.' % field_name
            raise InvalidDate(msg)
        return date
    
    def HandleApply(self):
        if not self._statement_types:
            msg = ('Statements settings not found,'
                   ' please set up contact rules first.')
            show_message_box(self._shell, msg, 'Error')
            return
        try:
            start_date = self._get_date(self._start_date, 'Start date')
            end_date = self._get_date(self._end_date, 'End date')
        except InvalidDate as exc:
            show_message_box(self._shell, str(exc), 'Error')
            return
        if end_date < start_date:
            msg = 'Start Date after End Date.'
            show_message_box(self._shell, msg, 'Error')
            return
        statement_type = str(self._statement_type.GetData())
        contact = self._contact.GetData()
        data_dict = {
            'event': 'New',
            'contact_id': str(contact.Oid()),
            'val_date': end_date,
            'statement': statement_type,
            'user': acm.User().Name(),
            'time': str(int(time.time())),
            'start_date': start_date,
            'end_date': end_date,
        }
        cto_name = 'Statements_%s_%s_%s_%s' % (data_dict['user'], data_dict['contact_id'],
                                               data_dict['val_date'], data_dict['event'])
        try:
            update_cto(cto_name, data_dict)
        except Exception as exc:
            msg = 'Failed to commit statement request: %s' % str(exc)
            show_message_box(self._shell, msg, 'Error')
        else:
            msg = 'Statement request sent successfully.'
            show_message_box(self._shell, msg, 'Information')


class AdHocSBLOpenPosCollStatement(AdHocDialog):
    
    event = 'SBL Open Position Coll Statement'
    allow_today = True
    default_date = TODAY


class AdHocSBLOpenPosOpsStatement(AdHocDialog):
    
    event = 'SBL Open Position Ops Statement'
    allow_today = True
    default_date = TODAY


class AdHocSBLSummaryOpenPosStatement(AdHocDialog):
    
    event = 'SBL Summary OpenPos Statement'
    allow_today = True
    default_date = TODAY


class AdHocSBLMarginCallStatement(AdHocDialog):
    
    event = 'SBL Margin Call Statement'
    allow_today = True
    default_date = TODAY


class AdHocSBLDividendNotification(AdHocDialog):
    
    event = 'SBL Dividend Notification Statement'
    allow_today = True
    default_date = TODAY
