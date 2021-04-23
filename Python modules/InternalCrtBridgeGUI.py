"""----------------------------------------------------------------------------------------------------------
MODULE                  :       InternalCrtBridgeGUI
PURPOSE                 :       Automate trade process for Non-CSA trades
DEPARTMENT AND DESK     :       Trading Structured Trading & CRT 3
REQUESTER               :       Declercq Wentzel
DEVELOPER               :       Nada Jasikova
CR NUMBER               :       2493464
-------------------------------------------------------------------------------------------------------------

"""
from __future__ import print_function

import acm
import FUxCore
import InternalCrtBridge
import at_time


class CreateInternalCrtBridgeDialog(FUxCore.LayoutDialog):
    """The GUI-managing class."""

    def __init__(self, trade):
        """Init with an acm.FTrade instance."""
        self.FEE_TYPES = ['CVA',
                          'FVA',
                          'RWA',
                          'Termination_fee',
                          'Cash',
                          'Premium']
        self.TRADE_STATES = ['Simulated', 'FO Confirmed', 'FO Sales']
        self.DEFAULT_TRADE_STATE = 'Simulated'

        # prepare the layout
        self.CreateLayout()

        # setup the data
        self.client_facing_trade = trade


    def HandleApply(self):
        '''Runs when "ok" is clicked

        return None => dialog stays open
        return anything else => dialog closes'''

        # Get validated input.
        try:
            (acquirer, portfolio, trade_status, val_group, pay_date,
                    internal_fees) = self._get_input()
        except ValidationError, e:
            print(e)
            return None

        # Save the trades.
        try:
            print('Creating a new pair of internal CRT bridge trades')
            trade = InternalCrtBridge.create_fee_trades(self.client_facing_trade,
                                                   acquirer, portfolio,
                                                   trade_status, val_group)
            InternalCrtBridge.commit_entities(trade)
            mirror_trade = trade.GetMirrorTrade()
            message = 'The following trades were saved: {0}, {1}'
            print(message.format(trade.Oid(), trade.GetMirrorTrade().Oid()))
        except Exception, exc:
            print('Did not manage to save the new trades: {0}'.format(exc))
            return None

        # Save the payments.
        try:
            print('Creating internal fee payments on new trades')
            payments = InternalCrtBridge.create_fee_payments(trade, pay_date,
                                                        internal_fees)
            mirror_payments = InternalCrtBridge.create_mirror_payments(mirror_trade,
                                                                  payments)
            all_payments = payments + mirror_payments
            InternalCrtBridge.commit_entities(*all_payments)
            payment_ids = ', '.join([str(payment.Oid()) for payment in all_payments])
            print('The following payments were saved: {0}'.format(payment_ids))
        except Exception, exc:
            print('Did not manage to save the new payments: {0}'.format(exc))
            return None

        return True

    def _get_input(self):
        """
        Get user input from the form.

        ValidationError is raised in case of invalid input.

        """
        portfolio = self.fux_portfolio_list.GetData()
        acquirer = self.fux_acquirer_list.GetData()
        trade_status = self.fux_trade_status_list.GetData()
        val_group = self.fux_val_group_list.GetData()
        pay_date_str = self.fux_pay_day.GetData()
        mandatory_values = {'Acquirer': acquirer,
                            'Portfolio': portfolio,
                            'Trade status': trade_status,
                            'Pay date': pay_date_str}
        for name, value in mandatory_values.iteritems():
            if not value:
                raise ValidationError('{0} is not set'.format(name))

        try:
            pay_date = at_time.date_from_string(pay_date_str)
        except ValueError:
            raise ValidationError("Pay date is not valid")

        internal_fees = {}
        for fee_type in self.FEE_TYPES:
            internal_fees[fee_type] = self._get_int_fee_values(fee_type)

        return acquirer, portfolio, trade_status, val_group, pay_date, internal_fees

    def HandleCreate(self, dlg, layout):
        '''Runs when the GUI is being created.'''

        self.fux_dialog = dlg
        self.fux_dialog.Caption('Create Internal CRT Bridge')
        self.fux_acquirer_list = layout.GetControl('acquirer_list')
        self.fux_portfolio_list = layout.GetControl('additional_prf_list')
        self.fux_trade_status_list = layout.GetControl('trade_status_list')
        self.fux_val_group_list = layout.GetControl('val_group_list')
        self.fux_pay_day = layout.GetControl('pay_day')
        tooltip = ('These are amounts that the acquirer will be receiving. '
                   'Thus a negative amount indicates a pay away '
                   'by the acquirer.')
        for fee_type in self.FEE_TYPES:
            input_control = layout.GetControl('internal_fees_{0}'
                                              .format(fee_type))
            input_control.ToolTip(tooltip)
            setattr(self, 'fux_internal_fees_{0}'.format(fee_type),
                    input_control)
            setattr(self, 'fux_currency_{0}'.format(fee_type),
                    layout.GetControl('currency_{0}'.format(fee_type)))

        acquirers = acm.FParty.Select('')
        self.fux_acquirer_list.Populate(acquirers)

        portfolios = acm.FPhysicalPortfolio.Select('')
        self.fux_portfolio_list.Populate(portfolios)

        self.fux_trade_status_list.Populate(self.TRADE_STATES)
        default_trade_state = self.client_facing_trade.Status()
        if default_trade_state not in self.TRADE_STATES:
            default_trade_state = self.DEFAULT_TRADE_STATE
        self.fux_trade_status_list.SetData(default_trade_state)

        val_groups = acm.FChoiceList.Select('list="ValGroup"')
        self.fux_val_group_list.Populate(val_groups)
        
        pay_day_str = self.client_facing_trade.TradeTime()
        self.fux_pay_day.SetData(acm.Time.DateFromTime(pay_day_str))

        default_currency = acm.FCurrency['ZAR']

        for fee_type in self.FEE_TYPES:
            self._populate_currency_list(fee_type, default_currency)

    def CreateLayout(self):
        """Creates the layout of the GUI dialog."""

        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b. AddOption('acquirer_list', 'Acquirer', 30, 30)
        b. AddOption('additional_prf_list',
                     'Additional portfolio', 30, 30)
        b. AddOption('trade_status_list', 'Trade status', 30, 30)
        b. AddOption('val_group_list', 'Val group', 30, 30)
        b. AddSpace(10)
        
        b. BeginVertBox('EtchedIn', label='Internal fees')
        b. AddInput('pay_day', 'Pay day')
        for fee_type in self.FEE_TYPES:
            b.  BeginHorzBox('None')
            b.   AddInput('internal_fees_{0}'.format(fee_type),
                          '{0}:'.format(fee_type))
            b.   AddOption('currency_{0}'.format(fee_type), None, 10, 10)
            b.  EndBox()
        b. EndBox()
        b.AddSpace(10)

        b. BeginHorzBox('None')
        b.  AddFill()
        b.  AddButton('ok', 'Create trades')
        b.  AddButton('cancel', 'Cancel')
        b. EndBox()
        b.EndBox()

        self.layout = b

    def _get_int_fee_values(self, fee_type):
        fee_amount_input = getattr(self,
                                   'fux_internal_fees_{0}'.format(fee_type))
        fee_amount = 0
        if fee_amount_input.GetData():
            fee_amount_str = fee_amount_input.GetData()
            try:
                fee_amount = float(fee_amount_str)
            except ValueError:
                message = '{0} is not a valid fee value for {1}.'
                raise ValidationError(message.format(fee_amount_str, fee_type))
        fee_currency_input = getattr(self, 'fux_currency_{0}'.format(fee_type))
        currency = fee_currency_input.GetData()
        return [fee_amount, currency]

    def _populate_currency_list(self, fee_type, default_currency):
        fee_currency_list = getattr(self, 'fux_currency_{0}'.format(fee_type))
        currencies = acm.FCurrency.Select('')
        fee_currency_list.Populate(currencies)
        fee_currency_list.SetData(default_currency)


def startDialog_cb(eii, *rest):
    """Starts the dialog for comment adding."""
    trade = eii.ExtensionObject().CurrentObject()
    if _confirm_action(trade):
        shell = eii.ExtensionObject().Shell()
        customDlg = CreateInternalCrtBridgeDialog(trade)
        acm.UX().Dialogs().ShowCustomDialogModal(shell,
                                                 customDlg.layout,
                                                 customDlg)


def _confirm_action(trade):
    """Checks for already existing bridge trades
    and displays a warning if there are any"""

    # Check if the trade is existing
    dialog_func = acm.GetFunction('msgBox', 3)
    # or trade.Status() in ('Simulated', 'Void')
    if not trade:
        message = 'Trade needs to be saved first.'
        dialog_func('Warning', message, 0)
        return False

    bridge_trades = InternalCrtBridge.get_existing_bridge_trades(trade)

    if bridge_trades:
        message = 'There already are existing internal CRT bridge trades:\n'
        for br_trade in bridge_trades:
            message += ' - {0}\n'.format(br_trade.Oid())
        message += 'To add more trades anyway, click OK.'
        buttonSelected = dialog_func('Warning', message, 1)

        return buttonSelected == 1

    return True


class ValidationError(Exception):
    """
    Exception class for raising user errors e.g. invalid arguments and other
    preconditions for running the script.
    """
