"""Customised Adjust Deposit functionality.

This module overrides FCallDeposit from the Default extension module.


Initial implementation
======================

Department: Securities Lending, Money Market Desk
Requesters: Michele Kluever, Sabir Ballim
Developers: Rohan van der Walt, Ickin Vural, Heinrich Cronje


History
=======

????-??-?? Rohan van der Walt   CR 325147: Added functionality for FCallDepositFunctions.adjust() to work correctly when Call Account has more than one trade on it. Trades must pass isEquityCallAccount test for Securities Lending.
????-??-?? Ickin Vural          CR 466028: Added Settle type.
????-??-?? Heinrich Cronje      CR 766044: Added the functionality to cater for High Level and Low Level SSIs.
????-??-?? Peter Basista        FA Upgrade 2014.
????-??-?? Rohan van der Walt   Adapt our custom adjustDeposit functionality to work with new interface for FCallDeposit introduced during the 2014.4.8 upgrade.
2015-11-05 Bushy Ngwako         Hashed out variable to allow Lower Level to be Visible to Dealers.
2017-01-25 Vojtech Sidorin      ABITFA-4481: Refactor and update.
2017-01-26 Vojtech Sidorin      ABITFA-4661: Fix backdating logic.
2017-02-23 Mighty Mkansi/Vojtech Sidorin  ABITFA-4417: Forbid adjusting if the deposit has more than one live trade, counting mirrors as one.
2017-07-24 Vojtech Sidorin      FAU-880: Update FCallDeposit - used_account() changed behaviour.
2017-08-31 Vojtech Sidorin      PostUpgrade: Disable the option to select a specific SSI if the SettlementModification hook is disabled.
2017-09-13 Vojtech Sidorin      ABITFA-5033: Update to work with new SSI objects in Front Arena 2017.
2019-05-20 Cuen Edwards         FAOPS-474: Reversal improvements and other minor changes.
2019-09-30 Amit Kardile         CHG1002321698: Removed hardcoded residual factor 0.25 and added support for taking it from 'Residual_Factor' add info
2019-10-07 Amit Kardile         CHG1002348213: Fixed the bug in residual threshold calculation
2020-05-18 Amit Kardile         FAFO-98: Adjust Deposit function changed. Removed hardcoding.
2020-11-24 Amit Kardile         FAFO-158: Fixed the comparing to zero bug
2021-01-21 Amit Kardile         FAFO-182: Fixed the net deposit balance bug
"""

import acm
import ael
from at_logging import getLogger
from at_ux import msg_dialog
from FCallDepositFunctions import (
        formnum,
        numstr_to_float,
        get_effective_ssis,
        intEndDay,
        backdate,
        adjust,
        get_cp_cash_account_from_ssi,
        is_voided_trade,
        get_non_voided_trades,
        can_be_adjusted,
        get_settlement_accounts,
        msg_box_ok,
        get_current_balance
        )
import FUxCore
import FUxNet
import clr
from primaryDepositNotice import noticeAmount, depositNoticeAmount

WinForms = clr.System.Windows.Forms
Color = clr.System.Drawing.Color

LOGGER = getLogger(__name__)

DOUBLE_FORMATTER = acm.FDomain['double'].DefaultFormatter()
DATE_FORMATTER = acm.FDomain['date'].DefaultFormatter()
DATETIME_FORMATTER = acm.FDomain['datetime'].DefaultFormatter()

# Johann : Types that should cause settlements to go on hold.
KNOWN_AMOUNT_TERM_REINVESTMENT_SETTLE_TYPES = [
    "Term To Call: Capital and Interest",
    "Term To Call: Capital",
    "Term To Call: Interest"
]

UNKNOWN_AMOUNT_TERM_REINVESTMENT_SETTLE_TYPES = [
    "Term To Call: Interest",
    "Term To Call: Partial",
    "Term To Call: Partial Capital and Interest",
    "Term To Call: Partial Capital",
    "Term To Multiple"
]

# NOTE - there are no known amount call reinvestment settle types.

UNKNOWN_AMOUNT_CALL_REINVESTMENT_SETTLE_TYPES = [
    "Call to Term"
]

KNOWN_AMOUNT_REINVESTMENT_SETTLE_TYPES = KNOWN_AMOUNT_TERM_REINVESTMENT_SETTLE_TYPES

UNKNOWN_AMOUNT_REINVESTMENT_SETTLE_TYPES = \
    UNKNOWN_AMOUNT_CALL_REINVESTMENT_SETTLE_TYPES + \
    UNKNOWN_AMOUNT_TERM_REINVESTMENT_SETTLE_TYPES

REINVESTMENT_SETTLE_TYPES = \
    UNKNOWN_AMOUNT_REINVESTMENT_SETTLE_TYPES + \
    KNOWN_AMOUNT_REINVESTMENT_SETTLE_TYPES

HOLD_SETTLE_TYPES = REINVESTMENT_SETTLE_TYPES + ['Reversal']

settle_hooks = None
try:
    from FSettlementParameters import hooks as settle_hooks
except Exception as ex:
    msg = ("Importing FSettlementParameters.hooks failed. Cannot determine "
           "whether the functionality to select a specific SSI is enabled or "
           "disabled.")
    LOGGER.warning(msg)


class AdjustDepositDialog(FUxCore.LayoutDialog, object):
    """Adjust Deposit dialog meant to be invoked by AUX.

    A typical invocation would look like this:

        # (1) Instantiate the dialogue in the background.
        #     (The __init__ method will be called.)
        dialog = AdjustDepositDialog(shell, instrument, trade)
        # (2) Set up the layout (fields, labels, etc.).
        layout = dialog.create_layout()
        # (3) Show the dialogue to the user.
        #     (The HandleCreate method will be called just before the dialogue
        #     is shown.)
        acm.UX().Dialogs().ShowCustomDialogModal(shell, layout, dialog)
    """

    # Notes shown if there are custom Trade Account Links (TALs) present
    # on the trade.
    TAL_NOTE1 = ("Note: There are custom Trade Account Links (TALs) "
                 "defined for this trade.")
    TAL_NOTE2 = ("You can manage TALs on the trade ticket "
                 "--> tab Accounts --> Show Details.")
    # Notes shown if the custom-SSI functionality is disabled.
    CUSTOM_SSI_DISABLED_NOTE1 = ("Note: The functionality to select a specific "
                                 "settle instruction is currently disabled.")
    CUSTOM_SSI_DISABLED_NOTE2 = ("For more information please contact "
                                 "\"AbCap SM IT - Trade Management\".")


    # Settle Types to populate the drop-down lists.
    SETTLE_TYPES = [
        "Settle",
        "Internal",
        "DTI",
        "Against Paper",
        "Reversal",
        "Square Off",
        "Interest Repayment",
        "Please Phone",
        "Migration Adjustment",
        "Debit Cheque Account"
    ]

    #Johann: Extend Settle type list
    SETTLE_TYPES = SETTLE_TYPES + UNKNOWN_AMOUNT_CALL_REINVESTMENT_SETTLE_TYPES

    def __init__(self, shell, instrument, trade, reinvestment_settle_type, reinvestment_amount):
        self.shell = shell
        self.instrument = instrument
        self.trade = trade
        self.dialog = None  # To be set by HandleCreate.
        self.layout = None  # To be set by HandleCreate.
        self.reinvestment_settle_type = reinvestment_settle_type
        self.reinvestment_amount = reinvestment_amount
        self.amountControl = None
        self.reversed_cash_flow = None
        self.intDataBindingControls()

    def intDataBindingControls(self):
        self._bindings = acm.FUxDataBindings()
        formatter = acm.Get('formats/LimitValues')
        self.amountControl = self._bindings.AddBinder('amount', 'double', formatter)

    def create_layout(self):
        """Create and return the form layout.

        The form layout is returned as an instance of FUxLayoutBuilder.
        """
        # NOTE: Single quotes in labels will break the layout (even escaped).
        # Double quotes can be used without escaping.
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox("None")

        # Value Date and Amount fields.
        b.BeginVertBox("None")
        # NOTE: Naming an input field "date" causes errors.
        b.AddComboBox("value_date", "Value Date*")
        self.amountControl.BuildLayoutPart(b, "Amount*:")
        #b.AddInput("amount", "Amount*")
        b.EndBox()

        b.AddFill()

        # Settlement section.
        b.BeginVertBox("EtchedIn", "Amount Settlement")
        b.AddComboBox("settle_type", "Settlement Type*")

        b.BeginHorzBox("None")
        b.AddInput("reversed_cf_input", "Reversed Cash Flow*")
        b.AddButton("select_cash_flow_button", "...", False, True)
        b.EndBox()

        if not self.custom_ssi_enabled():
            b.AddLabel("custom_ssi_note1", self.CUSTOM_SSI_DISABLED_NOTE1)
            b.AddLabel("custom_ssi_note2", self.CUSTOM_SSI_DISABLED_NOTE2)
        b.AddCheckbox("ssi_checkbox", "Use specific settle instruction")
        b.AddComboBox("ssi", "Settlement Instruction")
        b.BeginHorzBox("None")
        b.AddLabel("fa_acc_label", "Counterparty account:")
        # NOTE: Setting the label width with a parameter doesn't seem working,
        # therefore we insert a placeholder text to reserve the space.
        b.AddLabel("fa_acc_name", "_____________(to be populated)_____________")
        b.EndBox()
        b.AddLabel("fa_acc_note1", self.TAL_NOTE1)
        b.AddLabel("fa_acc_note2", self.TAL_NOTE2)
        b.EndBox()

        b.AddFill()

        # Interest section.
        b.BeginVertBox("EtchedIn", "Interest Settlement")
        b.BeginHorzBox("None")
        b.AddLabel("cfra_acc_label", "Interest is being paid to:")
        b.AddLabel("cfra_acc_name", "_____________(to be populated)_____________")
        b.EndBox()
        b.EndBox()

        b.AddFill()

        # Footnote and buttons.
        b.AddLabel("mandatory_label", "* indicates mandatory fields")
        b.AddSeparator()
        b.BeginHorzBox("Invisible")
        b.AddFill()
        b.AddButton("adjust", "Adjust")
        b.AddButton("cancel", "Close")
        b.EndBox()

        b.EndBox()
        return b

    def HandleCreate(self, dialog, layout):
        """This method is called before the dialogue is shown to the user."""
        # Save the reference to the dialog and layout for later use.
        self.dialog = dialog
        self.layout = layout
        self.amountControl.InitLayout(self.layout)
        gc = layout.GetControl
        dialog.Caption(
                "Adjust Deposit {inst} ({trade})"
                .format(inst=self.instrument.Name(), trade=self.trade.Oid()))

        # Color the account notes red.
        red = acm.UX().Colors().Create(195, 31, 0)
        if not self.custom_ssi_enabled():
            gc("custom_ssi_note1").SetColor("Text", red)
            gc("custom_ssi_note2").SetColor("Text", red)
        gc("fa_acc_note1").SetColor("Text", red)
        gc("fa_acc_note2").SetColor("Text", red)

        # Set tooltips.
        gc("ssi").ToolTip("Standing Settlement Instruction (SSI) to be used "
                          "for settling the Amount.")

        # Register callbacks.
        #gc("amount").AddCallback("Activate", self.format_amount, None)
        # NOTE: A checkbox control appears to trigger only the Changing and
        # Activate events. The Activate event seems the most suitable one.
        gc("settle_type").AddCallback("Changed", self.on_settle_type_combobox_changed, None)

        gc("reversed_cf_input").AddCallback("Changed", self.on_reversed_cf_input_changed, None)
        gc("select_cash_flow_button").AddCallback("Activate", self.on_select_cash_flow_button_press, None)

        gc("ssi_checkbox").AddCallback("Activate", self.on_ssi_checkbox_update, None)
        gc("ssi").AddCallback("Changing", self.update_fa_acc_name, None)
        gc("adjust").AddCallback("Activate", self.adjust, None)

        # Update the state and contents of controls.
        self.populate_controls()
        self.format_amount_input()
        self.format_settle_type_combobox()
        self.format_reversed_cf_input()
        self.format_select_cash_flow_button()
        self.format_ssi_checkbox()
        self.format_ssi_combobox()
        self.update_fa_acc_name()
        self.update_cfra_acc_name()
        self.on_ssi_checkbox_update()
        self.update_settlement_notes()

    @FUxCore.aux_cb
    def on_settle_type_combobox_changed(self, *_):
        """Event handler called on settle type combobox changed."""
        self.format_reversed_cf_input()
        self.format_select_cash_flow_button()
        self.format_ssi_checkbox()

    @FUxCore.aux_cb
    def on_reversed_cf_input_changed(self, *_):
        """Event handler called on reversed cash flow input changed."""
        gc = self.layout.GetControl
        reversed_cf_input = gc("reversed_cf_input")
        try:
            reversed_cf_oid = int(reversed_cf_input.GetData())
            self.reversed_cash_flow = acm.FCashFlow[reversed_cf_oid]
        except:
            self.reversed_cash_flow = None
        if self.reversed_cash_flow:
            reversed_cf_description = "Type: {cash_flow_type}, Nominal: {nominal}, "
            reversed_cf_description += "Pay Day: {pay_date}"
            reversed_cf_description = reversed_cf_description.format(
                cash_flow_type=self.reversed_cash_flow.CashFlowType(),
                nominal=DOUBLE_FORMATTER.Format(self.reversed_cash_flow.FixedAmount()),
                pay_date=DATE_FORMATTER.Format(self.reversed_cash_flow.PayDate())
            )
            reversed_cf_input.ToolTip(reversed_cf_description)
        else:
            reversed_cf_input.ToolTip(None)

    @FUxCore.aux_cb
    def on_select_cash_flow_button_press(self, *_):
        """Event handler called on select cash flow press."""
        leg = self.instrument.MainLeg()
        select_expression = "leg = {leg_oid} and cashFlowType = 'Fixed Amount'".format(
            leg_oid=leg.Oid()
        )
        cash_flows = acm.FCashFlow.Select(select_expression).AsArray().SortByProperty('PayDate, Oid')
        dialog = SelectFixedAmountCashFlowDialog(self.trade, cash_flows, self.reversed_cash_flow)
        selected_cash_flow = acm.UX.Dialogs().ShowCustomDialogModal(self.shell,
            dialog.GetLayoutBuilder(), dialog)
        if selected_cash_flow:
            gc = self.layout.GetControl
            reversed_cf_input = gc("reversed_cf_input")
            reversed_cf_input.SetData(selected_cash_flow.Oid())

    @FUxCore.aux_cb
    def on_ssi_checkbox_update(self, *_):
        """Called when the Settlement Instruction checkbox changes."""
        self.format_ssi_combobox()
        self.update_fa_acc_name()
        self.update_settlement_notes()

    def format_amount_input(self):
        """Format the amount input based on current values."""
        gc = self.layout.GetControl
        settle_type = gc("settle_type").GetData()
        editable = settle_type not in KNOWN_AMOUNT_REINVESTMENT_SETTLE_TYPES
        self.amountControl.Editable(editable)

    def format_settle_type_combobox(self):
        """Format the amount input based on current values."""
        gc = self.layout.GetControl
        settle_type_combobox = gc("settle_type")
        editable = not self.reinvestment_settle_type
        settle_type_combobox.Editable(editable)

    def format_reversed_cf_input(self):
        """Format the reversed cash flow input based on current values."""
        gc = self.layout.GetControl
        settle_type = gc("settle_type").GetData()
        reversed_cf_input = gc("reversed_cf_input")
        visible = settle_type == "Reversal"
        reversed_cf_input.Visible(visible)

    def format_select_cash_flow_button(self):
        """Format the select cash flow button based on current values."""
        gc = self.layout.GetControl
        settle_type = gc("settle_type").GetData()
        select_cash_flow_button = gc("select_cash_flow_button")
        visible = settle_type == "Reversal"
        select_cash_flow_button.Visible(visible)

    def format_ssi_checkbox(self):
        """Format the SSI checkbox based on current values."""
        gc = self.layout.GetControl
        ssi_checkbox = gc("ssi_checkbox")
        settle_type = gc("settle_type").GetData()
        enable = self.custom_ssi_enabled() and settle_type not in HOLD_SETTLE_TYPES
        ssi_checkbox.Enabled(enable)

    def format_ssi_combobox(self):
        """Format the SSI combobox based on current values."""
        gc = self.layout.GetControl
        use_custom_ssi = gc("ssi_checkbox").Checked()
        ssi_combobox = gc("ssi")
        enable = use_custom_ssi
        ssi_combobox.Enabled(enable)

    def update_fa_acc_name(self, *_):
        """Callback: Update the displayed name of the Fixed Amount account."""
        gc = self.layout.GetControl
        display_name = "(None)"
        default_account = self.get_cp_used_account("Fixed Amount")
        used_account = None
        if gc("ssi").Enabled():
            # Get the account from a specific settle instruction.
            ssi_name = gc("ssi").GetData()
            if ssi_name:
                ssi = acm.FSettleInstruction.Select01(
                        "party={0} and name='{1}'"
                        .format(self.trade.Counterparty().Oid(), ssi_name),
                        "Account not unique."
                        )
                if ssi:
                    used_account = get_cp_cash_account_from_ssi(ssi)
        else:
            # Get the default Fixed Amount account.
            used_account = default_account
        if used_account is not None:
            if used_account is default_account:
                display_name = "{0} (default)".format(used_account.Name())
            else:
                display_name = "{0}".format(used_account.Name())
        gc("fa_acc_name").SetData(display_name)

    def update_cfra_acc_name(self, *_):
        """Callback: Update the displayed name of the interest account.

        The interest account is the one set up for the Call Fixed Rate
        Adjustable cashflow.
        """
        gc = self.layout.GetControl
        used_cfra_account = self.get_cp_used_account("Call Fixed Rate Adjustable")
        if used_cfra_account is None:
            gc("cfra_acc_name").SetData("(None)")
        else:
            gc("cfra_acc_name").SetData(used_cfra_account.Name())

    def get_cp_used_account(self, cf_type):
        """Return the default counterparty account for a given cashflow type.

        Arguments:
        cf_type -- (str) Cashflow type, e.g. "Fixed Amount"

        Returns the counterparty account (FAccount).
        """
        settlement_accounts = get_settlement_accounts(self.trade, cf_type)
        return settlement_accounts["counterparty_account"]

    def update_settlement_notes(self):
        """Show a note if the trade has custom trade account links."""
        gc = self.layout.GetControl
        if self.has_custom_tals():
            gc("fa_acc_note1").SetData(self.TAL_NOTE1)
            gc("fa_acc_note2").SetData(self.TAL_NOTE2)
        else:
            gc("fa_acc_note1").SetData("")
            gc("fa_acc_note2").SetData("")

    def has_custom_tals(self):
        """Return True if the trade has custom trade account links."""
        for tal in self.trade.AccountLinks():
            if not tal.SystemGenerated():
                return True
        return False

    def populate_controls(self):

        """Populate drop-down lists and set default values."""
        gc = self.layout.GetControl

        # Value Date.
        # NOTE: If the Populate() method is used, the SetData() method
        # cannot be used to pre-select a value. Therefore we use a for-loop.
        value_dates = (
                str(ael.date_today()),
                str(ael.date_today().add_banking_day(
                    ael.Instrument[self.trade.Currency().Oid()], -1))
                )
        for value_date in value_dates:
            gc("value_date").AddItem(value_date)
        gc("value_date").SetData(0)

        # Amount.
        if self.reinvestment_amount:
            self.amountControl.SetValue(round(self.reinvestment_amount, 2))
        else:
            self.amountControl.SetValue(0.0)

        # Settlement Types.
        settle_type_combobox = gc("settle_type")
        if self.reinvestment_settle_type:
            settle_type_combobox.SetData(self.reinvestment_settle_type)
        else:
            for settle_type in self.SETTLE_TYPES:
                settle_type_combobox.AddItem(settle_type)
                settle_type_combobox.SetData(0)

        # Settlement Instructions.
        settle_instructions = get_effective_ssis(self.trade, "Fixed Amount")
        # Pre-select the most specific SSI that references the default
        # settlement account, otherwise leave blank.
        default_ssi = None
        for ssi in settle_instructions:
            gc("ssi").AddItem(ssi.Name())
            if (default_ssi is None and self.get_cp_used_account("Fixed Amount")
                    is get_cp_cash_account_from_ssi(ssi)):
                default_ssi = gc("ssi").ItemCount() - 1
        if default_ssi is None:
            default_ssi = ""
        gc("ssi").SetData(default_ssi)

    def adjust(self, *_):
        """Adjust the deposit - called after clicking the Adjust button."""

        # Check for duplicate cash flows
        if not self.validate_duplicate_cash_flows():
            return

        # Data formatting and validation.
        if not self.format_amount():
            return
        if not self.validate_data():
            return

        # Get values from the form fields.
        gc = self.layout.GetControl
        value_date = gc("value_date").GetData()
        #amount = float(gc("amount").GetData().replace(",", ""))
        amount = self.amountControl.GetValue()
        settle_type = gc("settle_type").GetData()
        reversed_cashflow = None
        if settle_type == "Reversal":
            reversed_cf_oid = int(gc("reversed_cf_input").GetData())
            reversed_cashflow = acm.FCashFlow[reversed_cf_oid]

        use_specific_ssi = gc("ssi_checkbox").Checked()
        ssi_name = gc("ssi").GetData()
        cp_account = None
        trade = self.instrument.Trades()[0]
        portfolio = trade.Portfolio()
        secondary_capacity_balance = 0
        seconday_capacity_value = 0
        residual_threshold = 0
        account_threshold = 0
        if portfolio.AdditionalInfo().NoticePortfolio() == True:
            if  portfolio.AdditionalInfo().Residual_Capacity():
                residual_threshold = portfolio.AdditionalInfo().Residual_Capacity()

            if  portfolio.AdditionalInfo().Deposit_Threshold():
                account_threshold = portfolio.AdditionalInfo().Deposit_Threshold()

            secondary_deposit_amount =  noticeAmount(portfolio, "Secondary Deposit")
            primary_deposit_amount = noticeAmount(portfolio, "Primary Deposit")
            access_deposit_amount = noticeAmount(portfolio, "Access Withdrawal")
            notice_withdrawal = noticeAmount(portfolio, "Notice Withdrawal")
            account_secondary_deposit_amount =  depositNoticeAmount(trade.Instrument(), "Secondary Deposit")
            account_primary_deposit_amount = depositNoticeAmount(trade.Instrument(), "Primary Deposit")
            account_access_deposit_amount = depositNoticeAmount(trade.Instrument(), "Access Withdrawal")
            account_net_deposit_balance = account_secondary_deposit_amount + account_primary_deposit_amount + account_access_deposit_amount
            account_net_deposit_check = account_secondary_deposit_amount + account_primary_deposit_amount + account_access_deposit_amount
            secondary_capacity_balance = access_deposit_amount + secondary_deposit_amount
            total_prigramme_balance = primary_deposit_amount + secondary_deposit_amount
            net_deposit_post_notice = secondary_deposit_amount + primary_deposit_amount + notice_withdrawal + access_deposit_amount
            net_deposit_balance = secondary_deposit_amount + primary_deposit_amount + access_deposit_amount
            
            if portfolio.AdditionalInfo().Residual_Factor():
                residual_capacity_balance = (net_deposit_balance - primary_deposit_amount) + (portfolio.AdditionalInfo().Residual_Factor() * residual_threshold)
            else:
                residual_capacity_balance = (net_deposit_balance - primary_deposit_amount) + residual_threshold
            
            seconday_capacity_value = secondary_capacity_balance + amount
            primary_deposit_notice = net_deposit_balance + primary_deposit_amount

        if use_specific_ssi:
            ssi = acm.FSettleInstruction.Select01(
                    "party={0} and name='{1}'"
                    .format(self.trade.Counterparty().Oid(), ssi_name),
                    "Account not unique."
                    )
            if ssi:
                cp_account = get_cp_cash_account_from_ssi(ssi)
            if not cp_account:
                msg = "Please select a valid Settlement Instruction."
                msg_dialog(msg, type_="Error", shell=self.dialog.Shell())
                LOGGER.error(msg)
                return
        LOGGER.debug("Value Date: {0}".format(value_date))
        LOGGER.debug("Amount: {0}".format(amount))
        LOGGER.debug("Settlement Type: {0}".format(settle_type))
        LOGGER.debug("Use specific settlement instruction: {0}".format(use_specific_ssi))
        LOGGER.debug("Settlement Instruction: {0}".format(ssi_name))

        # Adjust or backdate (after the user confims).
        # If the Amount Value Date falls into a rolling period, the
        # interest for which has already been paid out, do backdating;
        # otherwise do plain adjusting.
        int_per_end = intEndDay(self.instrument, value_date)
        if int_per_end is not None and int_per_end < ael.date_today():
            # Backdate.
            question = (
                    "Backdating {0}.\n\n"
                    "The Value Date falls into an interest period that ends "
                    "in the past. The cashflow corresponding to the Amount "
                    "will be backdated and additional interest cashflows will "
                    "be created for all past interest periods.\n\n"
                    "Do you wish to proceed?"
                    .format(self.instrument.Name())
                    )
            clicked = msg_dialog(question, type_="Warning",
                                 shell=self.dialog.Shell(), button3="Cancel")
            if clicked == "Button1":
                backdate(self.instrument, amount, ael.date(value_date),
                         ael.date_today(), settle_type=settle_type,
                         cp_account=cp_account, shell=self.dialog.Shell(),
                         reversed_cashflow=reversed_cashflow)
        else:
            # Plain adjust.
            question = ("{0} will be adjusted.\n\n"
                        "Do you wish to proceed?"
                        .format(self.instrument.Name()))
            clicked = msg_dialog(question, type_="Question",
                                 shell=self.dialog.Shell(), button3="Cancel")
            if clicked == "Button1":
                trades = acm.FList().AddAll([self.trade])
                if portfolio.AdditionalInfo().NoticePortfolio() == True:
                    if seconday_capacity_value > 0 and not AdjustDepositDialog._is_almost_zero(secondary_capacity_balance) and settle_type != "Call to Term":
                        msg = "Secondary capacity reached, adjusting with amount of %s %0.2f on the secondary balance" %(self.instrument.Currency().Name(), -secondary_capacity_balance)
                        LOGGER.info(msg)
                        msg_box_ok(msg, type_="Information", shell=self.dialog.Shell())
                        adjust(self.instrument, -secondary_capacity_balance, ael.date(value_date),
                            settle_type = settle_type, cp_account = cp_account,
                            shell=self.dialog.Shell(), reversed_cashflow=reversed_cashflow,
                            trades=trades)
                        
                        if seconday_capacity_value + net_deposit_post_notice < residual_threshold:
                            if account_net_deposit_check + seconday_capacity_value + amount > account_threshold:
                                msg = "Cannot book into a primary deposit account, balance reached"
                                LOGGER.error(msg)
                                msg_box_ok(msg, type_="Error", shell=self.dialog.Shell())
                            else:
                                msg = "Booked %s %0.2f to a primary amount" %(self.instrument.Currency().Name(), seconday_capacity_value)
                                LOGGER.info(msg)
                                msg_box_ok(msg, type_="Information", shell=self.dialog.Shell())

                                adjust(self.instrument, seconday_capacity_value, ael.date(value_date),
                                    settle_type=settle_type, cp_account=cp_account,
                                    shell=self.dialog.Shell(), reversed_cashflow=reversed_cashflow,
                                    trades=trades)
                        else:
                            msg = "Cannot book into a primary deposit account, balance reached"
                            LOGGER.error(msg)
                            msg_box_ok(msg, type_="Error", shell=self.dialog.Shell())

                    elif abs(seconday_capacity_value) > abs(residual_threshold):
                        msg = "Secondary capacity of %0.2f cannot be greater than residual threshold which is set to %0.2f" %(seconday_capacity_value, residual_threshold)
                        LOGGER.error(msg)
                        msg_box_ok(msg, type_="Error", shell=self.dialog.Shell())

                    elif residual_capacity_balance + amount < -0.001 and settle_type != "Call to Term":
                        msg = "Residual Capacity cannot be negative, please withdraw lesser amount or create a Call Term Deposit / Notice Withdrawal"
                        LOGGER.error(msg)
                        msg_box_ok(msg, type_="Error", shell=self.dialog.Shell())
                    elif account_net_deposit_balance + amount > account_threshold and amount > 0:
                        msg = "Account residual reached"
                        LOGGER.error(msg)
                        msg_box_ok(msg, type_="Error", shell=self.dialog.Shell())
                    elif amount > 0 and settle_type == "Call to Term":
                        msg = "Notice Withdrawal to Call to Term cannot be positive"
                        LOGGER.error(msg)
                        msg_box_ok(msg, type_="Error", shell=self.dialog.Shell())
                    elif get_current_balance(self.trade) + amount > residual_threshold:
                        msg = "Maximum deposit amount allowed reached, please deposit lesser amount"
                        LOGGER.error(msg)
                        msg_box_ok(msg, type_="Error", shell=self.dialog.Shell())
                    elif  amount + net_deposit_post_notice > residual_threshold and settle_type != "Call to Term":
                        msg = "Deposit amounts cannot be greater than the maximum programme value"
                        LOGGER.error(msg)
                        msg_box_ok(msg, type_="Error", shell=self.dialog.Shell())
                    else:
                        adjust(self.instrument, amount, ael.date(value_date),
                            settle_type=settle_type, cp_account=cp_account,
                            shell=self.dialog.Shell(), reversed_cashflow=reversed_cashflow,
                            trades=trades)
                else:
                    adjust(self.instrument, amount, ael.date(value_date),
                        settle_type=settle_type, cp_account=cp_account,
                        shell=self.dialog.Shell(), reversed_cashflow=reversed_cashflow,
                        trades=trades)


    def format_amount(self, *_):
        """Format the Amount and return True on success, False otherwise."""
        amount_control = self.layout.GetControl("amount")
        try:
            amount_control.SetData(formnum(numstr_to_float(amount_control.GetData())))
            return True
        except ValueError:
            msg = "Invalid Amount. Please enter a valid nonzero amount."
            LOGGER.exception(msg)
            msg_dialog(msg, type_="Error", shell=self.dialog.Shell())
            return False

    def validate_data(self):
        """Validate the user data from the form."""
        try:
            gc = self.layout.GetControl

            # Value Date.
            value_date = gc("value_date").GetData()
            try:
                value_date = ael.date(value_date).to_string(ael.DATE_ISO)
            except TypeError:
                error_message = "Invalid Value Date. Please enter a valid date."
                raise ValueError(error_message)

            # Amount.
            try:
                amount = self.amountControl.GetValue()
            except ValueError:
                amount = None
                LOGGER.exception()
            if amount in (None, 0.):
                error_message = "Invalid Amount. Please enter a valid nonzero numeric string."
                raise ValueError(error_message)

            # Settle Type.
            settle_type_control = gc("settle_type")
            if not settle_type_control.GetData():
                raise ValueError("Missing Settlement Type.")

            # Reversal Cash Flow.
            settle_type = settle_type_control.GetData()
            if settle_type == "Reversal":
                reversed_cf_oid = gc("reversed_cf_input").GetData()
                if not reversed_cf_oid:
                    raise ValueError("A reversed cash flow must be specified.")
                reversed_cash_flow = acm.FCashFlow[reversed_cf_oid]
                if not reversed_cash_flow:
                    error_message = "Reversed cash flow {reversed_cf_oid} does not exist."
                    raise ValueError(error_message.format(
                        reversed_cf_oid=reversed_cf_oid
                    ))
                if reversed_cash_flow.Instrument() != self.instrument:
                    error_message = "Reversed cash flow {reversed_cf_oid} does not belong to "
                    error_message += "the same instrument."
                    raise ValueError(error_message.format(
                        reversed_cf_oid=reversed_cf_oid
                    ))
                if reversed_cash_flow.CashFlowType() != 'Fixed Amount':
                    error_message = "Reversed cash flow {reversed_cf_oid} is not a fixed "
                    error_message += "amount cash flow."
                    raise ValueError(error_message.format(
                        reversed_cf_oid=reversed_cf_oid
                    ))
                if value_date != reversed_cash_flow.PayDate():
                    error_message = "Value date is not equal to reversed cash flow {reversed_cf_oid} "
                    error_message += "pay date of {reversed_cf_pay_date}."
                    raise ValueError(error_message.format(
                        reversed_cf_oid=reversed_cf_oid,
                        reversed_cf_pay_date=DATE_FORMATTER.Format(reversed_cash_flow.PayDate())
                    ))
                reversed_amount = reversed_cash_flow.FixedAmount() * self.trade.Quantity()
                if not self._amounts_are_equal_and_opposite(amount, reversed_amount):
                    error_message = "Amount is not equal and opposite to reversed cash flow "
                    error_message += "{reversed_cf_oid} amount of {reversed_cf_amount}."
                    raise ValueError(error_message.format(
                        reversed_cf_oid=reversed_cf_oid,
                        reversed_cf_amount=DOUBLE_FORMATTER.Format(reversed_cash_flow.FixedAmount())
                    ))
                if self._is_cash_flow_reversed(reversed_cash_flow):
                    error_message = "Reversed cash flow {reversed_cf_oid} has already been reversed."
                    raise ValueError(error_message.format(
                        reversed_cf_oid=reversed_cf_oid
                    ))

            # Settle Instruction.
            if gc("ssi_checkbox").Checked():
                ssi_control = gc("ssi")
                if not ssi_control.ItemExists(ssi_control.GetData()):
                    error_message = "Invalid Settlement Instruction. Please select a value "
                    error_message += "from the drop-down list."
                    raise ValueError(error_message)

            return True
        except Exception as exception:
            LOGGER.error(exception, exc_info=False)
            msg_dialog(str(exception), type_="Error", shell=self.dialog.Shell())
            return False

    def validate_duplicate_cash_flows(self):
        amount = 0
        duplicates = []

        # Value Date.
        gc = self.layout.GetControl
        value_date = acm.Time.AsDate(gc("value_date").GetData())

        # Amount.
        try:
            amount = self.amountControl.GetValue()
        except ValueError:
            amount = None
            LOGGER.exception()
        if amount in (None, 0.):
            msg = "Invalid Amount. Please enter a valid nonzero numeric string."
            msg_dialog(msg, type_="Error", shell=self.dialog.Shell())
            return False

        flows = self.instrument.Legs().First().CashFlows()
        for flow in flows:
            flow_amount = flow.FixedAmount() * self.trade.Quantity()
            if amount == flow_amount and value_date == flow.PayDate():
                duplicates.append(flow)

        if duplicates:
            from GValidation_DuplicateCashFlows import DialogDuplicateCashFlows, CreateLayout
            dialog = DialogDuplicateCashFlows(duplicates)
            return acm.UX().Dialogs().ShowCustomDialogModal(self.dialog.Shell(), CreateLayout(), dialog)
        return True

    def custom_ssi_enabled(self):
        """Return True if the custom-SSI functionality should be enabled."""
        # Fallback if the import of settle_hooks failed.
        if settle_hooks is None:
            return True

        settle_hook_names = [h.GetHookName() for h in settle_hooks]
        return "SettlementModification" in settle_hook_names

    @staticmethod
    def _amounts_are_equal_and_opposite(amount1, amount2):
        """
        Determine if two amounts are equal but with the opposite
        signs.
        """
        if amount1 > 0 and amount2 > 0:
            return False
        if amount1 < 0 and amount2 < 0:
            return False
        sum_of_amounts = amount1 + amount2
        return AdjustDepositDialog._is_almost_zero(sum_of_amounts)

    @staticmethod
    def _is_almost_zero(amount, epsilon=0.009):
        """
        Determine if an amount is 'almost zero'.
        """
        almost_zero = acm.GetFunction('almostZero', 2)
        return almost_zero(abs(amount), epsilon)

    @staticmethod
    def _is_cash_flow_reversed(cash_flow):
        """Determine whether or not a cash flow has already been reversed by another cash flow."""
        select_expression = "leg = {leg_oid} and cashFlowType = 'Fixed Amount'".format(
            leg_oid=cash_flow.Leg().Oid()
        )
        fixed_amount_cash_flows = acm.FCashFlow.Select(select_expression).AsArray()
        for fixed_amount_cash_flow in fixed_amount_cash_flows:
            settle_type = fixed_amount_cash_flow.AddInfoValue('Settle_Type')
            if settle_type is None:
                continue
            if 'Reversal' not in settle_type:
                continue
            reversed_cashflow_oid = fixed_amount_cash_flow.AddInfoValue('Reversed_CF_Ref')
            if reversed_cashflow_oid is None:
                continue
            if reversed_cashflow_oid == cash_flow.Oid():
                return True
        return False


class SelectFixedAmountCashFlowDialog(FUxCore.LayoutDialog):
    """
    Dialog used to select a Fixed Amount cash flow.
    """

    def __init__(self, trade, cash_flows, selected_cash_flow):
        """
        Constructor.
        """
        self._trade = trade
        self._cash_flows = cash_flows
        self._selected_cash_flow = selected_cash_flow
        self._dialog = None
        self._layout = None
        self._cash_flow_grid = None

    @FUxCore.aux_cb
    def HandleCreate(self, dialog, layout):
        """
        AUX hook called to create the dialog.
        """
        self._dialog = dialog
        self._layout = layout
        self._dialog.Caption('Select Cash Flow')
        self._cash_flow_grid = self._create_cash_flow_grid()
        cash_flow_panel = self._layout.GetControl('cash_flow_panel').GetCustomControl()
        cash_flow_panel.Padding = WinForms.Padding(1)
        cash_flow_panel.BackColor = Color.Gray
        cash_flow_panel.Controls.Add(self._cash_flow_grid)

    @FUxCore.aux_cb
    def HandleApply(self):
        """
        AUX hook called when the user presses the OK button.

        Returns a value to allow the dialog to close, None to prevent
        it.
        """
        try:
            selected_rows = self._cash_flow_grid.SelectedRows
            if selected_rows.Count > 1:
                raise RuntimeError('Expecting zero or one selected cash flow.')
            elif selected_rows.Count < 1:
                raise ValueError('A cash flow must be selected.')
            selected_row = selected_rows[0]
            cash_flow_oid = selected_row.Cells[0].Value
            self._selected_cash_flow = acm.FCashFlow[cash_flow_oid]
            return self._selected_cash_flow
        except Exception as exception:
            msg_dialog(str(exception), type_="Error", shell=self._dialog.Shell())

    @FUxCore.aux_cb
    def HandleCancel(self):
        """
        AUX hook called when the user cancels or closes the dialog.

        Returns a value to allow the dialog to close, None to prevent
        it.
        """
        return True

    def GetLayoutBuilder(self):
        """
        Gets a layout builder for the dialog.
        """
        layout_builder = acm.FUxLayoutBuilder()
        layout_builder.BeginVertBox('None')
        FUxNet.AddWinFormsControlToBuilder(layout_builder, 'cash_flow_panel', 'System.Windows.Forms.Panel',
            'System.Windows.Forms', 600, 300)
        layout_builder.BeginHorzBox('None')
        layout_builder.AddButton('ok', 'OK')
        layout_builder.AddButton('cancel', 'Cancel')
        layout_builder.EndBox()
        layout_builder.EndBox()
        return layout_builder

    def _create_cash_flow_grid(self):
        """
        Create the cash flow grid control.
        """
        cash_flow_grid = WinForms.DataGridView()
        cash_flow_grid.ColumnHeadersHeightSizeMode = WinForms.DataGridViewColumnHeadersHeightSizeMode.DisableResizing
        cash_flow_grid.AllowUserToAddRows = False
        cash_flow_grid.AllowUserToDeleteRows = False
        cash_flow_grid.AllowUserToResizeRows = False
        cash_flow_grid.ReadOnly = True
        cash_flow_grid.SelectionMode = WinForms.DataGridViewSelectionMode.FullRowSelect
        cash_flow_grid.MultiSelect = False
        cash_flow_grid.Dock = WinForms.DockStyle.Fill
        cash_flow_grid.AutoSizeRowsMode = WinForms.DataGridViewAutoSizeRowsMode.DisplayedCellsExceptHeaders
        cash_flow_grid.ColumnHeadersBorderStyle = WinForms.DataGridViewHeaderBorderStyle.Single
        cash_flow_grid.CellBorderStyle = WinForms.DataGridViewCellBorderStyle.Single
        cash_flow_grid.RowHeadersBorderStyle = WinForms.DataGridViewHeaderBorderStyle.Single
        cash_flow_grid.GridColor = Color.WhiteSmoke
        cash_flow_grid.BackgroundColor = Color.White
        cash_flow_grid.RowHeadersVisible = False
        cash_flow_grid.BorderStyle = WinForms.BorderStyle.None
        self._create_cash_flow_grid_columns(cash_flow_grid)
        self._create_cash_flow_grid_rows(cash_flow_grid)
        self._set_cash_flow_grid_row_selection(cash_flow_grid)
        return cash_flow_grid

    def _create_cash_flow_grid_columns(self, cash_flow_grid):
        """
        Create the cash flow grid columns.
        """
        cash_flow_grid.ColumnCount = 7
        cash_flow_grid.Columns[0].Name = 'Number'
        cash_flow_grid.Columns[0].Width = 60
        cash_flow_grid.Columns[0].DefaultCellStyle.Alignment = WinForms.DataGridViewContentAlignment.MiddleRight
        cash_flow_grid.Columns[1].Name = 'Type'
        cash_flow_grid.Columns[1].Width = 80
        cash_flow_grid.Columns[2].Name = 'Curr'
        cash_flow_grid.Columns[2].Width = 40
        cash_flow_grid.Columns[3].Name = 'Nominal'
        cash_flow_grid.Columns[3].DefaultCellStyle.Alignment = WinForms.DataGridViewContentAlignment.MiddleRight
        cash_flow_grid.Columns[3].Width = 100
        cash_flow_grid.Columns[4].Name = 'Pay Day'
        cash_flow_grid.Columns[4].Width = 75
        cash_flow_grid.Columns[5].Name = 'Create Time'
        cash_flow_grid.Columns[5].Width = 120
        cash_flow_grid.Columns[6].Name = 'Create User'
        cash_flow_grid.Columns[6].Width = 80

    def _create_cash_flow_grid_rows(self, cash_flow_grid):
        """
        Create the cash flow grid rows.
        """
        for cash_flow in self._cash_flows:
            cash_flow_amount = cash_flow.FixedAmount() * self._trade.Quantity()
            cash_flow_grid.Rows.Add([
                cash_flow.Oid(),
                cash_flow.CashFlowType(),
                cash_flow.Leg().Currency().Name(),
                DOUBLE_FORMATTER.Format(cash_flow_amount),
                DATE_FORMATTER.Format(cash_flow.PayDate()),
                DATETIME_FORMATTER.Format(acm.Time.DateTimeFromTime(cash_flow.CreateTime())),
                cash_flow.CreateUser().Name()
            ])

    def _set_cash_flow_grid_row_selection(self, cash_flow_grid):
        """
        Sets the row selection of the cash flow grid.
        """
        selected_index = -1
        if self._selected_cash_flow:
            # Select index of currently selected cash flow if present.
            selected_index = self._get_grid_row_index_of_cash_flow(cash_flow_grid,
                self._selected_cash_flow)
        if selected_index == -1:
            # Fallback on selecting index of last cash flow.
            selected_index = cash_flow_grid.Rows.Count - 1
        # Set the selection if valid.
        if selected_index > -1:
            selected_row = cash_flow_grid.Rows[selected_index]
            cash_flow_grid.FirstDisplayedScrollingRowIndex = selected_row.Index
            cash_flow_grid.Refresh()
            cash_flow_grid.CurrentCell = selected_row.Cells[1]
            selected_row.Selected = True

    def _get_grid_row_index_of_cash_flow(self, cash_flow_grid, cash_flow):
        """
        Gets the row index of a cash flow in the cash flow grid.

        If the cash flow is present then the index is returned.  If the
        cash flow is not present, -1 is returned.
        """
        for row in cash_flow_grid.Rows:
            cash_flow_oid = row.Cells[0].Value
            if cash_flow_oid == cash_flow.Oid():
                return row.Index
        return -1


class CallDepositMenuItem(FUxCore.MenuItem, object):
    """Setup for the Adjust Deposit menu item."""

    def __init__(self, ext_object, trade):
        self.ext_object = ext_object
        self.my_trade = trade


    @property
    def _tm_row(self):
        """Return the current Trading Manager row."""
        row = None
        try:
            row = self.ext_object.ActiveSheet().Selection().SelectedCell().RowObject()
        except AttributeError:
            pass
        return row

    @property
    def instrument(self):
        """Return the instrument that should be adjusted."""
        if self.my_trade is not None:
            return self.my_trade.Instrument()
        instrument = None
        if self.ext_object.IsKindOf("CInsDefAppFrame"):
            # In the instrument/trade definition form.
            try:
                instrument = self.ext_object.OriginalInstrument()
            except AttributeError:
                pass
        elif self.ext_object.IsKindOf("FUiTrdMgrFrame"):
            # In the trading manager.
            try:
                instrument = self._tm_row.Instrument()
            except AttributeError:
                try:
                    instrument = self._tm_row.SingleInstrument()
                except AttributeError:
                    pass
        return instrument

    @property
    def trade(self):
        """Return the trade that should be adjusted."""

        if self.my_trade is not None:
            return self.my_trade

        trade = None
        if self.ext_object.IsKindOf("CInsDefAppFrame"):
            # In the instrument/trade definition form.
            try:
                trade = self.ext_object.OriginalTrade()
            except AttributeError:
                pass
        elif self.ext_object.IsKindOf("FUiTrdMgrFrame"):
            # In the trading manager.
            try:
                trade = self._tm_row.Trade()
            except AttributeError:
                try:
                    trade = get_non_voided_trades(self.instrument)[0]
                except (AttributeError, IndexError):
                    pass
        return trade

    def Applicable(self):
        """Return True if the menu item should be shown, False otherwise."""
        return self.instrument is not None and self.instrument.IsCallAccount()

    def Enabled(self):
        """
        Return True if the menu item should be enabled, i.e. clickable;
        return False if the menu item should be disabled, i.e. 'grayed'.
        """
        return (self.Applicable() and
                self.trade is not None and
                not is_voided_trade(self.trade))

    def Invoke(self, eii):
        """This method is called by FA to show the GUI dialogue."""
        settlementInstruct =""
        newAmount = 0.0
        if isinstance(eii, list):
            settlementInstruct = eii[2]
            newAmount = eii[3]
            trade = eii[1]
            eii= eii[0]
        else:
            trade = None

        ext_object = eii.ExtensionObject()
        shell = ext_object.Shell()

        if (self.Applicable() and self.Enabled() and
                can_be_adjusted(self.instrument)):
            dialog = AdjustDepositDialog(shell, self.instrument, self.trade, settlementInstruct, newAmount)
            layout = dialog.create_layout()
            acm.UX().Dialogs().ShowCustomDialogModal(shell, layout, dialog)
        else:
            instrument_name = "None"
            try:
                instrument_name = self.instrument.Name()
            except AttributeError:
                pass
            msg = ("Cannot adjust the deposit '{0}'. It must be a call "
                   "account with exactly one non-voided trade. (Mirror trades "
                   "are counted as one.)".format(instrument_name))
            msg_dialog(msg, type_="Error", shell=shell)


def create_call_deposit_menu_item(ext_object):
    """Return an object representing the Call Deposit menu item.

    This function is meant to be referenced from an FMenuExtension.
    """

    if isinstance(ext_object, list):
        #settlementInstruct = ext_object[2]
        #newAmount = ext_object[3]
        trade = ext_object[1]
        ext_object= ext_object[0]

    else:
        trade = None

    return CallDepositMenuItem(ext_object, trade)
