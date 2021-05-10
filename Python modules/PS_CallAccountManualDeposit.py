"""
=================================================================================================================================
MODULE                  :       PS_CallAccountManualDeposit
PURPOSE                 :       Script to Adjust PRIME SERVICES Call Accounts.
=================================================================================================================================

HISTORY
=================================================================================================================================
Date            Change no       Developer              Requester         Description
=================================================================================================================================
2012-08-08      396485          Heinrich Cronje        Ross Wood         Added Prevent Settlement to settle_type dropdown.
                                                                         Added Commitment of Addinfo Settle_Type.
2014-07-31      1652702         Ondrej Bahounek        Ruth Forssman     Added Deposit Descriptor for addinfo PS_Descriptor.
2016-05-12      3653091         Libor Svoboda          Eveshnee Naidoo   Enabled Inter Fund Cash Transfer, refactored.
2021-01-19      FAPE-497        Marcus Ambrose         Eveshnee Naidoo   Added exposure interest
=================================================================================================================================
"""
import acm
import at_addInfo
import FCallDepositFunctions
from PS_CallAccountSweeperFunctions import IsCurrentInterestPeriod
from at_ael_variables import AelVariableHandler


call_account = None
try:
    call_account = original_call_account
except:
    pass


class FundingInstypeError(Exception):
    pass


def get_instrument_types():
    ins_types = acm.FEnumeration["enum(InsType)"].EnumeratorStringsSkipFirst()
    ins_types = list(ins_types)
    return sorted(ins_types)


def get_deposit_types():
    deposit_types = [
        "Margin Deposit",
        "SBL Deposit",
        "Sundry Deposit",
        "Manual TPL Deposit",
        "Fee Rebate",
        "Inter Fund Cash Transfer",
        "Exposure Interest",
    ]
    return sorted(deposit_types)


def get_settlement_types():
    settlement_types = [
        "Settle",
        "Internal",
        "DTI",
        "Against Paper",
        "Reversal",
        "Square Off",
        "Interest Repayment",
        "Please Phone",
        "Migration Adjustment",
        "Debit Cheque Account",
        "Prevent Settlement",
    ]
    return sorted(settlement_types)


def get_linked_trades(orig_trade):
    linked_trades = []
    contract_trdnbr = orig_trade.ContractTrdnbr()
    instruments = [orig_trade.Instrument()]
    trades = acm.FTrade.Select("contractTrdnbr=%d" % contract_trdnbr)
    for trade in trades:
        if trade.Instrument() not in instruments:
            instruments.append(trade.Instrument())
            linked_trades.append(trade)
    return linked_trades


def get_target_trades(call_acc_name):
    target_trades = []
    if not call_acc_name:
        return target_trades
    try:
        trades = acm.FInstrument[call_acc_name].Trades()
    except:
        trades = []
    if trades and trades[0].ContractTrdnbr():
        target_trades = get_linked_trades(trades[0])
    return target_trades


def deposit_type_hook(ael_input):
    is_manual_tpl = ael_input.value == "Manual TPL Deposit"
    is_inter_fund = ael_input.value == "Inter Fund Cash Transfer"
    call_acc = None
    target_trades = []
    for var in ael_variables:
        if var.name in ["pswap", "ins_type"]:
            var.enabled = is_manual_tpl
            var.mandatory = is_manual_tpl
        if var.name == "call_acc":
            call_acc = var.value
        if var.name == "settle_type" and is_manual_tpl:
            var.value = "Prevent Settlement"

    if is_inter_fund:
        target_trades = get_target_trades(call_acc)

    for var in ael_variables:
        if var.name == "target_call_acc":
            var.enabled = is_inter_fund
            if target_trades:
                var.value = target_trades[0].Instrument()
            else:
                var.value = None


def settle_type_hook(ael_input):
    for var in ael_variables:
        if var.name == "deposit_type" and var.value == "Manual TPL Deposit":
            ael_input.value = "Prevent Settlement"


def amount_hook(ael_input):
    value = FCallDepositFunctions.NumberFormatting(0, [ael_input.value])
    if value:
        ael_input.value = value[0]


def call_acc_hook(ael_input):
    if ael_input.default:
        ael_input.enabled = False
        ael_input.value = ael_input.default
        ael_input.default = None
    else:
        ael_input.enabled = True

    if not ael_input.value:
        ael_input.enabled = True


def target_trade_hook(ael_input):
    target_trades = []
    for var in ael_variables:
        if var.name == "call_acc":
            target_trades = get_target_trades(var.value)

    if ael_input.value and acm.FTrade[ael_input.value] not in target_trades:
        ael_input.collection = target_trades
        if target_trades:
            ael_input.value = target_trades[0]

    for var in ael_variables:
        if var.name == "target_call_acc":
            if ael_input.value:
                try:
                    var.value = acm.FTrade[ael_input.value].Instrument()
                except:
                    var.value = ael_input.value.Instrument()
            else:
                var.value = None


ael_variables = AelVariableHandler()
ael_variables.add(
    "call_acc",
    label="Call Account",
    cls="FInstrument",
    mandatory=True,
    default=call_account,
    enabled=True,
    hook=call_acc_hook,
)
ael_variables.add(
    "deposit_date",
    label="Date",
    cls="date",
    default=acm.Time.DateNow(),
    alt="Deposit date.",
)
ael_variables.add(
    "deposit_amount",
    label="Amount",
    cls="string",
    default="0",
    alt="Deposit amount.",
    hook=amount_hook,
)
ael_variables.add(
    "settle_type",
    label="Settlement Type",
    cls="string",
    collection=get_settlement_types(),
    default="Settle",
    alt="Settlement type.",
    hook=settle_type_hook,
)
ael_variables.add(
    "deposit_type",
    label="Deposit Type",
    cls="string",
    collection=get_deposit_types(),
    default="Margin Deposit",
    alt="Type of Deposit.",
    hook=deposit_type_hook,
)
ael_variables.add(
    "pswap",
    label="Portfolio Swap",
    cls="FInstrument",
    alt="Portfolio swap that TPL deposit relates to.",
    mandatory=False,
)
ael_variables.add(
    "ins_type",
    label="Instrument Type",
    cls="string",
    collection=get_instrument_types(),
    alt="Instrument type that TPL deposit relates to.",
    mandatory=False,
)
ael_variables.add(
    "target_call_acc",
    label="Target Call Account",
    cls="FInstrument",
    mandatory=False,
    enabled=False,
)
ael_variables.add(
    "deposit_desc",
    label="Deposit Descriptor",
    cls="string",
    alt="Deposit descriptor flag.",
    mandatory=False,
)


def get_instrument(eii):
    if eii.ExtensionObject().IsKindOf(acm.FUiTrdMgrFrame):
        return (
            eii.ExtensionObject()
            .ActiveSheet()
            .Selection()
            .SelectedCell()
            .RowObject()
            .Instrument()
        )
    else:
        return eii.ExtensionObject().OriginalInstrument()


def make_manual_deposit(eii):
    # Menu call defined in FMenuExtension
    instrument = get_instrument(eii)
    global original_call_account
    original_call_account = instrument
    acm.RunModuleWithParametersAndData(
        "PS_CallAccountManualDeposit", "Standard", instrument
    )
    original_call_account = None


def create_inter_fund_cf(call_acc, amount, start_day, pay_day):
    leg = call_acc.Legs()[0]
    cf = leg.CreateCashFlow()
    cf.FixedAmount = amount
    cf.NominalFactor = 1
    cf.StartDate = start_day
    cf.PayDate = pay_day
    cf.CashFlowType = "Fixed Amount"
    cf.Commit()
    return cf


def create_cf(call_acc, amount, date, settle_type, deposit_type=""):
    date_today = acm.Time().DateToday()
    if deposit_type == "Inter Fund Cash Transfer":
        cash_flow = create_inter_fund_cf(call_acc, amount, date, date_today)
        return cash_flow

    if IsCurrentInterestPeriod(call_acc, date):
        trades = call_acc.Trades()
        cash_flow = FCallDepositFunctions.adjust(
            call_acc, amount, date, settle_type, None, None, 1, trades=trades
        )
    else:
        cash_flow = FCallDepositFunctions.backdate(
            call_acc, amount, date, date_today, settle_type, None, None, 1
        )
    return cash_flow


def set_add_infos(cash_flows, ael_dict):
    deposit_type = ael_dict["deposit_type"]
    settle_type = ael_dict["settle_type"]
    desc = ael_dict["deposit_desc"]
    ins_type = ael_dict["ins_type"]
    pswap = ael_dict["pswap"]
    for cf in cash_flows:
        if not cf:
            continue
        at_addInfo.save(cf, "PS_DepositType", deposit_type)
        at_addInfo.save(cf, "Settle_Type", settle_type)

        if deposit_type == "Manual TPL Deposit":
            at_addInfo.save(cf, "PSCashType", pswap.Name())
            at_addInfo.save(cf, "PS_InstrumentType", ins_type)

        if desc:
            at_addInfo.save(cf, "PS_Descriptor", desc)


def ael_main(ael_dict):
    call_account = ael_dict["call_acc"]
    date = ael_dict["deposit_date"]
    amount = float(ael_dict["deposit_amount"].replace(",", ""))
    deposit_type = ael_dict["deposit_type"]
    settle_type = ael_dict["settle_type"]
    msg_box = acm.GetFunction("msgBox", 3)
    if deposit_type == "Manual TPL Deposit" and not (
        ael_dict["ins_type"] and ael_dict["pswap"]
    ):
        msg_box("Warning", "Please specify Portfolio Swap and Instrument Type.", 0)
        return

    trades = call_account.Trades()
    if (
        not trades
        or trades[0].add_info("Funding Instype") != "Call Prime Brokerage Funding"
    ):
        raise FundingInstypeError(
            "Cannot use this functionality. Funding Instype"
            ' must be "Call Prime Brokerage Funding"'
        )

    if deposit_type == "Inter Fund Cash Transfer":
        target_call_account = ael_dict["target_call_acc"]
        if not target_call_account:
            msg_box("Warning", "Target Call Account missing.", 0)
            return
        acm.BeginTransaction()
        try:
            cf1 = create_cf(call_account, amount, date, settle_type, deposit_type)
            cf2 = create_cf(
                target_call_account, -amount, date, settle_type, deposit_type
            )
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            raise
        cash_flows = [cf1, cf2]
    else:
        cf = create_cf(call_account, amount, date, settle_type)
        cash_flows = [cf]

    set_add_infos(cash_flows, ael_dict)


def ael_main_ex(ael_dict, additional_data):
    instrument = additional_data.At("customData")
    ael_dict["call_acc"] = instrument
    ael_main(ael_dict)
