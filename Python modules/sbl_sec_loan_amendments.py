"""-----------------------------------------------------------------------------
PURPOSE              :  SBL onto FA
                        This module provides functionality to amend sec loan
                        and/or recalculate Loan and Finder fees.
                        It is used by the "Amend Loan" and "Recalc Fees" menu
                        extensions accessible from the sec loan trade ticket.
DESK                 :  SBL PTS
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-06-03  CHG0102113     Libor Svoboda       Initial Implementation
"""
from collections import defaultdict

import acm
import ael
import FUxCore
from at_logging import getLogger
from sbl_monthly_fee_payments import (calculate_loan_fee_values,
                                      calculate_finder_fee_values,
                                      book_payments,
                                      apply_minimum_fee,
                                      sl_party_and_payment_factor,
                                      regenerate_cashflows,
                                      select_trades,
                                      regenerate_instruments,
                                      book_minimum_fee,
                                      MIN_FEE_TYPE,
                                      FIRST_OF_THIS_MONTH,
                                      LAST_OF_PREVIOUS_MONTH,
                                      FIRST_OF_PREVIOUS_MONTH)


LOGGER = getLogger(__name__)
CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()
CALENDAR = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time.DateToday()
VALID_FROM = FIRST_OF_THIS_MONTH
BASE_QUERY_NAME = 'SBL_Monthly_Fee'
PAY_DAY = TODAY
PARAMS = {
    'ux_shell': None,
    'billable_parties': None,
}

def create_layout_amend():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox()
    b.  BeginHorzBox('EtchedIn', 'Price')
    b.    AddInput('current_price', 'Current')
    b.    AddInput('new_price', 'New')
    b.  EndBox()
    b.  BeginHorzBox('EtchedIn', 'Quantity')
    b.    AddInput('current_quantity', 'Current')
    b.    AddInput('new_quantity', 'New')
    b.  EndBox()
    b.  BeginHorzBox('EtchedIn', 'Start Date')
    b.    AddInput('current_start_date', 'Current')
    b.    AddInput('new_start_date', 'New')
    b.  EndBox()
    b.  BeginHorzBox('EtchedIn', 'End Date')
    b.    AddInput('current_end_date', 'Current')
    b.    AddInput('new_end_date', 'New')
    b.  EndBox()
    b.  BeginHorzBox('EtchedIn', 'Rate')
    b.    AddInput('current_rate', 'Current')
    b.    AddInput('new_rate', 'New')
    b.  EndBox()
    b.  BeginHorzBox('EtchedIn', 'SL_CFD')
    b.    AddCheckbox('current_sl_cfd', 'Current')
    b.    AddCheckbox('new_sl_cfd', 'New')
    b.  EndBox()
    b.  BeginHorzBox('EtchedIn', 'Minimum Fee')
    b.    AddInput('current_min_fee', 'Current')
    b.    AddInput('new_min_fee', 'New')
    b.  EndBox()
    b.  AddFill()
    b.  AddSpace(10)
    b.  BeginHorzBox()
    b.    AddCheckbox('recalculate_fees', 'Recalculate current fees')
    b.  EndBox()
    b.  AddFill()
    b.  AddSpace(10)
    b.  BeginHorzBox()
    b.    AddFill()
    b.    AddButton('ok', 'Update')
    b.    AddButton('cancel', 'Cancel')
    b.  EndBox()
    b.EndBox()
    return b

    
def create_layout_fee_recalc():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox()
    b.  AddLabel('recalc_label', 'Recalculate fees for the current period?')
    b.  AddFill()
    b.  AddSpace(10)
    b.  BeginHorzBox()
    b.    AddFill()
    b.    AddButton('ok', 'Yes')
    b.    AddButton('cancel', 'Cancel')
    b.  EndBox()
    b.EndBox()
    return b


def create_layout_fee_recalc_per_party():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox()
    b.  AddOption('party_name', 'Party name', 70)
    b.  AddOption('payment_type', 'Payment type', 70)
    b.  AddInput('start_date', 'Billing period start')
    b.  AddInput('end_date', 'Billing period end')
    b.  AddInput('base_query', 'Base trade query')
    b.  AddFill()
    b.  AddSpace(10)
    b.  BeginHorzBox()
    b.    AddFill()
    b.    AddButton('ok', 'Recalculate')
    b.    AddButton('cancel', 'Cancel')
    b.  EndBox()
    b.EndBox()
    return b


def show_custom_dialog(message, dialog_type, shell):
    """Show a custom dialog."""
    acm.UX().Dialogs().MessageBox(shell, dialog_type, message, 'OK', 
                                  None, None, 'Button1', 'Button1')


def find_payments(trade, payment_type, valid_from='', include_min_fee=False):
    query = 'trade=%s and type="%s"' % (trade.Oid(), payment_type)
    if valid_from:
        period_start = acm.Time.FirstDayOfMonth(valid_from)
        period_end = acm.Time.DateAddDelta(period_start, 0, 0, 
                                           acm.Time.DaysInMonth(valid_from)-1)
        query += ' and validFrom>="%s" and validFrom<="%s"' % (period_start, period_end)
    if include_min_fee:
        query += ' and text="Minimum Fee"'
    payments = acm.FPayment.Select(query)
    payments_dict = defaultdict(list)
    for payment in payments:
        payments_dict[payment.Party()].append(payment)
    return payments_dict


def update_min_fee_payment(trade, payment_type='Loan Fee'):
    payments = find_payments(trade, MIN_FEE_TYPE, include_min_fee=True)
    if not payments:
        msg = 'No minimum %s payments found for the current period.' % MIN_FEE_TYPE
        show_custom_dialog(msg, 'Information', PARAMS['ux_shell'])
        LOGGER.info(msg)
        return
    for counterparty in payments:
        cp_flag = counterparty.AdditionalInfo().SL_CptyType()
        get_cp, _ = sl_party_and_payment_factor(cp_flag)
        trade_cp = get_cp(trade)
        if counterparty != trade_cp:
            LOGGER.warning('Trade counterparty "%s" does not match the payment party "%s".'
                           % (trade_cp.Name(), counterparty.Name()))
            continue
        first_of_this_month = acm.Time.FirstDayOfMonth(TODAY)
        end_date = acm.Time.DateAddDelta(first_of_this_month, 0, 0, -1)
        apply_minimum_fee(trade, payment_type, VALID_FROM, PAY_DAY, end_date, cp_flag)


def update_loan_fee_payment(trade, payment_type='Loan Fee'):
    payments = find_payments(trade, payment_type, VALID_FROM)
    if not payments:
        msg = 'No %s payments found for the current period.' % payment_type
        show_custom_dialog(msg, 'Information', PARAMS['ux_shell'])
        LOGGER.info(msg)
        return
    for counterparty in payments:
        cp_flag = counterparty.AdditionalInfo().SL_CptyType()
        get_cp, _ = sl_party_and_payment_factor(cp_flag)
        trade_cp = get_cp(trade)
        if counterparty != trade_cp:
            LOGGER.warning('Trade counterparty "%s" does not match the payment party "%s".'
                           % (trade_cp.Name(), counterparty.Name()))
            continue
        LOGGER.info('Updating %s for party "%s"' % (payment_type, counterparty.Name()))
        first_of_this_month = acm.Time.FirstDayOfMonth(TODAY)
        end_date = acm.Time.DateAddDelta(first_of_this_month, 0, 0, -1)
        start_date = acm.Time.FirstDayOfMonth(end_date)
        payment_vals = calculate_loan_fee_values([trade], start_date, end_date)
        book_payments(payment_vals, VALID_FROM, PAY_DAY, payment_type, cp_flag)


def update_finder_fee_payment(trade, payment_type='Finder Fee'):
    payments = find_payments(trade, payment_type, VALID_FROM)
    if not payments:
        msg = 'No %s payments found for the current period.' % payment_type
        show_custom_dialog(msg, 'Information', PARAMS['ux_shell'])
        LOGGER.info(msg)
        return
    for counterparty in payments:
        get_cp, _ = sl_party_and_payment_factor('Finder')
        finder = get_cp(trade)
        if counterparty != finder:
            LOGGER.warning('Trade finder "%s" does not match the payment party "%s".'
                           % (finder.Name(), counterparty.Name()))
            continue
        LOGGER.info('Updating %s for party "%s"' % (payment_type, counterparty.Name()))
        first_of_this_month = acm.Time.FirstDayOfMonth(TODAY)
        end_date = acm.Time.DateAddDelta(first_of_this_month, 0, 0, -1)
        start_date = acm.Time.FirstDayOfMonth(end_date)
        payment_vals = calculate_finder_fee_values([trade], start_date, end_date)
        book_payments(payment_vals, VALID_FROM, PAY_DAY, payment_type, 'Finder')


def start_dialog_amend(eii):
    """Callback from menu extension to start the main dialog."""
    shell = eii.ExtensionObject().Shell()
    trade = eii.ExtensionObject().OriginalTrade()
    if not trade:
        show_custom_dialog('Invalid trade.', 'Error', shell)
        return
    builder = create_layout_amend()
    dialog = SecLoanAmendDialog(trade, eii.ExtensionObject())
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dialog)


def start_dialog_fee_recalc(eii):
    """Callback from menu extension to start the main dialog."""
    shell = eii.ExtensionObject().Shell()
    trade = eii.ExtensionObject().OriginalTrade()
    if not trade:
        show_custom_dialog('Invalid trade.', 'Error', shell)
        return
    builder = create_layout_fee_recalc()
    dialog = SecLoanFeeRecalc(trade)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dialog)


def start_dialog_fee_recalc_per_party(eii):
    """Callback from menu extension to start the main dialog."""
    shell = eii.ExtensionObject().Shell()
    builder = create_layout_fee_recalc_per_party()
    dialog = SecLoanFeeRecalcPerParty()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dialog)


def get_billable_parties():
    if PARAMS['billable_parties']:
        return PARAMS['billable_parties']
    query = acm.CreateFASQLQuery('FParty', 'AND')
    query.AddAttrNode('AdditionalInfo.SL_Billing', 'EQUAL', True)
    PARAMS['billable_parties'] = query.Select()
    return PARAMS['billable_parties']


class StringInput(object):
    
    def __init__(self, layout, current_name, new_name):
        self._current_control = layout.GetControl(current_name)
        self._current_control.Editable(False)
        self._new_control = layout.GetControl(new_name)
        self._new_control.AddCallback('LooseFocus', self._on_loose_focus, None)
    
    @property
    def current(self):
        return self._current_control.GetData()
    
    @current.setter
    def current(self, value):
        self._current_control.SetData(value)
    
    @property
    def new(self):
        return self._new_control.GetData()
    
    @new.setter
    def new(self, value):
        self._new_control.SetData(value)
    
    def _on_loose_focus(self, *args):
        pass
    
    def updated(self):
        return self.current != self.new


class DateInput(StringInput):
    
    def _on_loose_focus(self, *args):
        try:
            self.new = acm.Time.FromDate(self.new)[:10]
        except:
            show_custom_dialog('Invalid input.', 'Error', PARAMS['ux_shell'])
            self.new = self.current


class FloatInput(StringInput):
    
    @property
    def current(self):
        return float(self._current_control.GetData())
    
    @current.setter
    def current(self, value):
        self._current_control.SetData(value)
    
    @property
    def new(self):
        return float(self._new_control.GetData())
    
    @new.setter
    def new(self, value):
        self._new_control.SetData(value)
    
    def _on_loose_focus(self, *args):
        try:
            _ = self.new
        except:
            show_custom_dialog('Invalid input.', 'Error', PARAMS['ux_shell'])
            self.new = self.current


class CheckboxInput(StringInput):
    
    @property
    def current(self):
        return self._current_control.Checked()
    
    @current.setter
    def current(self, value):
        self._current_control.Checked(value)
    
    @property
    def new(self):
        return self._new_control.Checked()
    
    @new.setter
    def new(self, value):
        self._new_control.Checked(value)


class SecLoanAmendDialog(FUxCore.LayoutDialog):
    
    def __init__(self, trade, ins_frame):
        self._trade = trade
        self._ins_frame = ins_frame
        self._inputs = {}
    
    @staticmethod
    def recalculate_fees(trade):
        try:
            update_loan_fee_payment(trade)
            update_min_fee_payment(trade)
            update_finder_fee_payment(trade)
        except Exception as exc:
            msg = 'Fee update failed: %s' % str(exc)
            show_custom_dialog(msg, 'Error', PARAMS['ux_shell'])
            LOGGER.exception(msg)
        else:
            LOGGER.info('Fee update successful.')
    
    def _reset_inputs(self):
        ins = self._trade.Instrument()
        price = round(self._trade.AllInPrice(), 9)
        quantity = round(self._trade.Quantity() * ins.RefValue(), 9)
        start_date = ins.StartDate()
        end_date = ins.EndDate()
        rate = ins.Legs()[0].FixedRate()
        sl_cfd = bool(ins.AdditionalInfo().SL_CFD())
        min_fee = (ins.AdditionalInfo().SL_Minimum_Fee() 
                   if ins.AdditionalInfo().SL_Minimum_Fee() else 0.0)
        
        self._inputs['price'].current = price
        self._inputs['price'].new = price
        self._inputs['quantity'].current = quantity
        self._inputs['quantity'].new = quantity
        self._inputs['start_date'].current = start_date
        self._inputs['start_date'].new = start_date
        self._inputs['end_date'].current = end_date
        self._inputs['end_date'].new = end_date
        self._inputs['rate'].current = rate
        self._inputs['rate'].new = rate
        self._inputs['sl_cfd'].current = sl_cfd
        self._inputs['sl_cfd'].new = sl_cfd
        self._inputs['min_fee'].current = min_fee
        self._inputs['min_fee'].new = min_fee
    
    def HandleCreate(self, dlg, layout):
        self._fux_dlg = dlg
        PARAMS['ux_shell'] = dlg.Shell()
        self._fux_dlg.Caption('Security Loan Amendments')
        
        self._recalculate_fees = layout.GetControl('recalculate_fees')
        self._recalculate_fees.Checked(True)
        
        self._inputs['price'] = FloatInput(layout, 'current_price', 'new_price')
        self._inputs['quantity'] = FloatInput(layout, 'current_quantity', 'new_quantity')
        self._inputs['start_date'] = DateInput(layout, 'current_start_date', 'new_start_date')
        self._inputs['end_date'] = DateInput(layout, 'current_end_date', 'new_end_date')
        self._inputs['rate'] = FloatInput(layout, 'current_rate', 'new_rate')
        self._inputs['sl_cfd'] = CheckboxInput(layout, 'current_sl_cfd', 'new_sl_cfd')
        self._inputs['min_fee'] = FloatInput(layout, 'current_min_fee', 'new_min_fee')
        self._reset_inputs()
    
    def HandleApply(self):
        ins = self._trade.Instrument()
        trade_image = self._trade.StorageImage()
        ins_image = ins.StorageImage()
        if self._inputs['price'].updated() or self._inputs['quantity'].updated():
            contract_size = ins.ContractSize()
            quotation_factor = ins.Quotation().QuotationFactor()
            price = self._inputs['price'].new
            quantity = self._inputs['quantity'].new
            trade_quantity = price * quotation_factor * quantity / contract_size
            ref_val = contract_size / (price * quotation_factor)
            underlying = ins.Underlying()
            ref_price = price
            if underlying.InsType() in ('Bond', 'IndexLinkedBond'):
                ref_price = underlying.Calculation().PriceConvert(
                    CALC_SPACE, price, 'Pct of Nominal', underlying.Quotation(), 
                    self._inputs['start_date'].new)
            trade_image.Quantity(trade_quantity)
            ins_image.RefValue(ref_val)
            ins_image.RefPrice(ref_price)
        if self._inputs['start_date'].updated():
            leg = ins_image.Legs()[0]
            leg.StartDate(self._inputs['start_date'].new)
        if self._inputs['end_date'].updated():
            leg = ins_image.Legs()[0]
            leg.EndDate(self._inputs['end_date'].new)
        if self._inputs['rate'].updated():
            leg = ins_image.Legs()[0]
            leg.FixedRate(self._inputs['rate'].new)
        if self._inputs['sl_cfd'].updated():
            ins_image.AdditionalInfo().SL_CFD(self._inputs['sl_cfd'].new)
        if self._inputs['min_fee'].updated():
            ins_image.AdditionalInfo().SL_Minimum_Fee(self._inputs['min_fee'].new)
        
        if not trade_image.IsModified() and not ins_image.IsModified():
            show_custom_dialog('No updates requested.', 'Information', PARAMS['ux_shell'])
            return
        
        acm.BeginTransaction()
        try:
            ins_image.Commit()
            trade_image.Commit()
            acm.CommitTransaction()
        except Exception as exc:
            acm.AbortTransaction()
            msg = 'Amendment failed: %s' % str(exc)
            show_custom_dialog(msg, 'Error', PARAMS['ux_shell'])
            LOGGER.exception(msg)
            return
        LOGGER.info('Amendment successful.')
        # Sec Loan ticket wouldn't refresh properly without this
        self._ins_frame.SetContents(self._trade)
        self._reset_inputs()
        
        try:
            regenerate_cashflows(ins)
        except Exception as exc:
            msg = 'Regenerate failed: %s' % str(exc)
            show_custom_dialog(msg, 'Error', PARAMS['ux_shell'])
            LOGGER.exception(msg)
            return
        LOGGER.info('Loan regenerated.')
        
        if self._recalculate_fees.Checked():
            self.recalculate_fees(self._trade)
        show_custom_dialog('Done.', 'Information', PARAMS['ux_shell'])


class SecLoanFeeRecalc(FUxCore.LayoutDialog):
    
    def __init__(self, trade):
        self._trade = trade
    
    def HandleCreate(self, dlg, layout):
        self._fux_dlg = dlg
        PARAMS['ux_shell'] = dlg.Shell()
        self._fux_dlg.Caption('Recalculate Fees')
    
    def HandleApply(self):
        ins = self._trade.Instrument()
        try:
            regenerate_cashflows(ins)
        except Exception as exc:
            msg = 'Regenerate failed: %s' % str(exc)
            show_custom_dialog(msg, 'Error', PARAMS['ux_shell'])
            LOGGER.exception(msg)
            return
        LOGGER.info('Loan regenerated.')
        
        SecLoanAmendDialog.recalculate_fees(self._trade)
        show_custom_dialog('Done.', 'Information', PARAMS['ux_shell'])
        return True


class SecLoanFeeRecalcPerParty(FUxCore.LayoutDialog):
    
    payment_types = (
        'Loan Fee',
        'Finder Fee',
    )
    base_query_name = BASE_QUERY_NAME
    
    def _on_party_changed(self, *args):
        party_name = str(self._party_name.GetData().Name())
        if 'FINDER' in party_name.upper():
            self._payment_type.SetData('Finder Fee')
        else:
            self._payment_type.SetData('Loan Fee')
    
    def _set_defaults(self):
        for payment_type in self.payment_types:
            self._payment_type.AddItem(payment_type)
        self._payment_type.SetData(self.payment_types[0])
        parties = get_billable_parties()
        self._party_name.Populate(parties)
        self._party_name.SetData(parties[0])
        self._start_date.SetData(FIRST_OF_PREVIOUS_MONTH)
        self._end_date.SetData(LAST_OF_PREVIOUS_MONTH)
        self._base_query.SetData(self.base_query_name)
    
    def HandleCreate(self, dlg, layout):
        self._fux_dlg = dlg
        PARAMS['ux_shell'] = dlg.Shell()
        self._fux_dlg.Caption('Recalculate Fees for Counterparty')
        self._party_name = layout.GetControl('party_name')
        self._party_name.AddCallback('Changed', self._on_party_changed, self)
        self._payment_type = layout.GetControl('payment_type')
        self._start_date = layout.GetControl('start_date')
        self._start_date.Editable(False)
        self._end_date = layout.GetControl('end_date')
        self._end_date.Editable(False)
        self._base_query = layout.GetControl('base_query')
        self._base_query.Editable(False)
        self._base_query.Visible(False)
        self._set_defaults()
    
    def HandleApply(self):
        payment_type = str(self._payment_type.GetData())
        query = acm.FStoredASQLQuery[str(self._base_query.GetData())].Query()
        party = self._party_name.GetData()
        start_date = str(self._start_date.GetData())
        end_date = str(self._end_date.GetData())
        LOGGER.info('Booking %s for date range %s - %s.' 
                    % (payment_type, start_date, end_date))
        if payment_type == 'Finder Fee':
            flag = 'Finder'
            trades = select_trades(query, start_date, end_date, finders=[party])
        elif party.AdditionalInfo().SL_CptyType() == 'Lender':
            flag = 'Lender'
            trades = select_trades(query, start_date, end_date, lenders=[party])
        elif party.AdditionalInfo().SL_CptyType() == 'Borrower':
            flag = 'Borrower'
            trades = select_trades(query, start_date, end_date, borrowers=[party])
        else:
            msg = 'SL_CptyType not specified for party %s.' % party.Name()
            show_custom_dialog(msg, 'Error', PARAMS['ux_shell'])
            LOGGER.error(msg)
            return
        LOGGER.info('Selected %s trades.' % len(trades))
        regenerate_instruments(trades)
        if payment_type == 'Finder Fee':
            payment_vals = calculate_finder_fee_values(trades, start_date, end_date)
            book_payments(payment_vals, FIRST_OF_THIS_MONTH, TODAY, payment_type, flag)
        else:
            payment_vals = calculate_loan_fee_values(trades, start_date, end_date)
            book_payments(payment_vals, FIRST_OF_THIS_MONTH, TODAY, payment_type, flag)
            book_minimum_fee(trades, payment_type, FIRST_OF_THIS_MONTH, TODAY, end_date, flag)
        show_custom_dialog('Done.', 'Information', PARAMS['ux_shell'])
        LOGGER.info('Done.')
