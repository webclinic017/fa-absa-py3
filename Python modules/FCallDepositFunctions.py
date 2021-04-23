"""Utility functions for Call Deposits.


History (old)
=============

Description             : In the function backdate, added a check in to see if the Call Account
                          is already rolled. If rolled, just process the transaction. If not,
                          roll the Call Account.
Department and Desk     : PCG MM
Requester               : Venessa Kennel
Developer               : Heinrich Cronje
CR Number               : 251297

Description             : Added functionality in adjust() if Trades > 1, and isEquityCallAccount.
                          For Securities Lending, there are mirror trades on Call Accounts,
                          because old code doesn't allow more than one trade on call account,
                          adjust deposit did not work from trading manager.
Department and Desk     : Securities Lending
Requester               : Michele Kluever
Developer               : Rohan van der Walt
CR Number               : 325147

Description             : Updated adjust function to allow prime brokerage call accounts to have mirror trades on them
Department and Desk     : Prime Services
Requester               : Francois Henrion
Developer               : Paul Jacot-Guillarmod
CR Number               : 704002

Description             : Amended the Trade Account Link functions to accomodate High Level and Low Level SSI loading.
Department and Desk     : Money Market
Requester               : Money Market Front Office
Developer               : Heinrich Cronje
CR Number               : 766044

Description             : ABITFA-4290 - Need to prevent booking of a deposit onto a call loan and vice versa.
Department and Desk     : Money Market
Requester               : Money Market Front Office (Marilize Knoetze)
Developer               : Mighty Mkansi
CR Number               : 4219306


History
=======

2017-01-13 Vojtech Sidorin/Peter Basista  ABITFA-4481: Update, refactor, and improve coding style.
2017-02-23 Mighty Mkansi/Vojtech Sidorin  ABITFA-4417: Forbid adjusting if the deposit has more than one live trade, counting mirrors as one.
2017-03-24 Vojtech Sidorin                ABITFA-4661: Fix backdating logic.
2017-06-16 Vojtech Sidorin                ABITFA-4943: Fix interest calculation when backdating.
2017-07-20 Vojtech Sidorin                FAU-880: Update FCallDeposit - used_account() changed behaviour.
2017-09-19 Vojtech Sidorin                ABITFA-5033: Update to work with new SSI objects in Front Arena 2017.
2019-02-07 Cuen Edwards                   FAOPS-397: Improved number parsing to support non-breaking spaces.
2019-03-12 Stuart Wilson                  FAOPS-413: Made Committing of fixed amount cashflow transactional
2019-04-18 Cuen Edwards                   FAOPS-425: Removal of direct updates to settlements.
2019-05-20 Cuen Edwards                   FAOPS-474: Reversal improvements.
2020-05-13 Amit Kardile                   FAFO-98: Adjust Deposit function changed. Removed hardcoding.
"""

import locale
import re

import acm
import ael
import time
import at_addInfo
import CallCurrentRate
import FOperationsUtils as Utils

from ArenaFunctionBridge import cashflow_projected_cf # for 4.3 upgrade
from at_logging import getLogger
from at_ux import msg_box, msg_dialog
from SAGEN_Set_Additional_Info_new import setAddInfoEntity

from primaryDepositNotice import noticeAmount

CALC_SPACE = acm.Calculations().CreateCalculationSpace(
                acm.GetDefaultContext(), "FPortfolioSheet")

LOGGER = getLogger(__name__)


def msg_box_ok(msg, type_="Information", shell=None):
    """Show either a modal or modeless message box with an OK button.

    If a shell is provided, then the message box will be modal,
    otherwise it will be modeless.

    Positional arguments:
    msg (str) -- message to show

    Keyword arguments:
    type_ (enum(FUxMessageBoxType)) -- type of the message box
    shell (FUxShell) -- shell of the parent frame
    """
    if shell is not None:
        return msg_dialog(msg, type_, shell)
    else:
        return msg_box(msg, title=type_)


def formnum(number):
    """
    Format the number into a fixed point notation rounded to two decimal
    places with thousands separators.

    Returns a string with the formatted number.
    """
    locale.setlocale(locale.LC_ALL, "")
    return locale.format("%.2f", number, grouping=True)


def numstr_to_float(numstr):
    """Convert a numeric string to a float.

    The numeric string can contain commas to separate thousands and
    can end with a single character denoting the multiplication factor.

    Arguments:
    numstr (string) -- numeric string to convert to a float

    >>> numstr_to_float("1.25k")
    1250.0
    >>> numstr_to_float("2.5K")
    2500.0
    >>> numstr_to_float("6.3e2G")
    630000000000.0

    """
    # Multiplication factors (use lower-case chars).
    factors = {
            "k": 1e3,   # kilo
            "t": 1e3,   # thousand
            "m": 1e6,   # mega
            "g": 1e9,   # giga
            "b": 1e9,   # billion
    }

    if not numstr:
        raise ValueError("Cannot convert an empty string to a float.")

    float_ = None
    # Remove thousands separators.
    str_ = re.sub(r'(?u)[\s,]', '', numstr)
    try:
        float_ = float(str_)
    except ValueError:
        if len(str_) > 1:
            factor = str_[-1].lower()
            decimal = float(str_[:-1])
            if factor in factors:
                float_ = decimal*factors[factor]
    if float_ is not None:
        return float_
    else:
        raise ValueError("Cannot convert the numeric string to a float.")


def NumberFormatting(index, aelvars):
    """AEL variables hook: Format a numeric string."""
    numstr = aelvars[index]
    if not numstr:
        # Do nothing for an empty numeric string.
        return
    try:
        float_ = numstr_to_float(numstr)
    except ValueError:
        msg = ("Cannot convert the string to a number. Please enter a valid "
               "numeric string.")
        LOGGER.exception(msg)
        return
    aelvars[index] = formnum(float_)
    return aelvars


def is_almost_zero(amount, epsilon=0.009):
    """
    Determine if an amount is 'almost zero'.
    """
    almost_zero = acm.GetFunction('almostZero', 2)
    return almost_zero(abs(amount), epsilon)


def amendTradeAccountLink(ins, FA, CFRA, FRA):
    """Update the trade account links on the first trade of the instrument."""

    genericProcessed = False
    try:
        t = ins.Trades()[0]
    except IndexError:
        LOGGER.exception("The instrument has no trades.")
        return
    if t.Acquirer().Oid() == 2247:      #Funding Desk
        party = t.Counterparty().Name()
        ssiList = [FA, CFRA, FRA]
        for s in ssiList:
            ssi = get_ACM_SSI(party, s)
            if (not ssi):     #Not a Valid SSI entered
                return

            lowLevelSSI = True
            if (ssi.InstrumentType() == 'None') and (ssi.CashSettleCashFlowType() == 'None'):
                lowLevelSSI = False

            tradeAccountLinkQuery = acm.CreateFASQLQuery(acm.FTradeAccountLink, 'AND')
            tradeAccountLinkQuery.AddAttrNode('SettleInstruction.Name', 'EQUAL', s)
            tradeAccountLinkQuery.AddAttrNode('Trade.Oid', 'EQUAL', t.Oid())
            tradeAccountLinkQuery.AddAttrNode('PartyType', 'EQUAL', Utils.GetEnum('PartyType', 'Counterparty'))
            tal = tradeAccountLinkQuery.Select()

            if tal:
                continue

            if not genericProcessed or lowLevelSSI:
                set_Override_SSI = False
                for tal in t.AccountLinks():
                    if tal.SystemGenerated() == 0:
                        if (tal.SettleInstruction().CashSettleCashFlowType() == ssi.CashSettleCashFlowType() and tal.SettleInstruction().InstrumentType() == ssi.InstrumentType()):
                            if ssi.DefaultInstruction():
                                tal.Delete()
                                ael.poll()
                                if not lowLevelSSI:
                                    genericProcessed = True
                            else:
                                tal.SettleInstruction(ssi)
                                try:
                                    tal.Commit()
                                except Exception:
                                    LOGGER.exception("Could not amend Trade Account Link to reference SSI %s:", ssi.Name())
                                if not lowLevelSSI:
                                    genericProcessed = True
                                set_Override_SSI = True

                if (not set_Override_SSI):
                    tradeAccountLink = acm.FTradeAccountLink()
                    tradeAccountLink.Trade(t)
                    tradeAccountLink.SettleInstruction(ssi)
                    tradeAccountLink.SystemGenerated(0)
                    tradeAccountLink.PartyType('Counterparty')
                    try:
                        tradeAccountLink.Commit()
                        ael.poll()
                        if not lowLevelSSI:
                            genericProcessed = True
                    except Exception:
                        msg = ("Could not add Trade Account Link to reference "
                               "SSI {0}.".format(ssi.Name()))
                        LOGGER.exception(msg)

def get_ACM_SSI(party_name, ssi_name):
    """
    Return the first settlement instruction (FSettleInstruction)
    for the provided settlement instruction name (ssi_name)
    and the provided party name (party_name).
    """
    ssiQuery = acm.CreateFASQLQuery(acm.FSettleInstruction, 'AND')
    ssiQuery.AddAttrNode('Party.Name', 'EQUAL', party_name)
    ssiQuery.AddAttrNode('Name', 'EQUAL', ssi_name)
    ssi = ssiQuery.Select()

    if ssi:
        return ssi[0]
    return None


def is_call_loan(call_balance, trade):
    if trade.Quantity() < 0:
        return True
    elif trade.AdditionalInfo().Funding_Instype() in ('Call Loan Coll DTI',
                                                      'Call Loan Coll NonDTI',
                                                      'Call Loan DTI',
                                                      'Call Loan NonDTI',
                                                      'Call Access Loan',
                                                      'Call Bond Loan'):
        if call_balance <= 0:
            return True
    return False


def is_voided_trade(trade):
    """Return True if the trade is voided."""
    return trade.Status() in ("Void", "Confirmed Void")


def get_non_voided_trades(instrument):
    """Return all non-voided trades for the instrument."""
    return [t for t in instrument.Trades() if not is_voided_trade(t)]


def get_first_trade(instrument):
    if not instrument.IsKindOf("FDeposit"):
        return None
    first_trade = None
    non_voided_trades = get_non_voided_trades(instrument)
    if non_voided_trades:
        first_trade = non_voided_trades[0]
    return first_trade


def get_current_balance(trade):
    balance = CALC_SPACE.CalculateValue(trade, "Deposit balance").Number()
    return balance


def can_be_adjusted(instrument):
    """Return True if the instrument is a call account and can be adjusted."""

    # The instrument must be a call account.
    if not instrument.IsCallAccount():
        return False

    # It must have exactly one non-voided trade, counting mirrors as one.
    non_voided_trades = get_non_voided_trades(instrument)
    if len(non_voided_trades) == 1:
        return True
    elif len(non_voided_trades) == 2:
        # Allow if the two trades are mirrors.
        if non_voided_trades[0].GetMirrorTrade() is non_voided_trades[1]:
            return True
    return False


def turning_loan_into_deposit(instrument, amount):
    """
    Return True if the amount would turn a call loan into a deposit;
    return False otherwise.
    """
    first_trade = get_first_trade(instrument)
    if first_trade is not None:
        call_balance = get_current_balance(first_trade)
        new_balance = call_balance + amount
        if is_call_loan(call_balance, first_trade) and new_balance > 0:
            return True
    return False


def balance_is_ceded(instrument, amount):
    first_trade = get_first_trade(instrument)
    if first_trade is not None and first_trade.AdditionalInfo().MM_Account_Ceded() is not None:
        if first_trade.AdditionalInfo().MM_Account_Ceded() == True:
            call_balance = get_current_balance(first_trade)
            new_balance = call_balance + amount
            ceded_amount = first_trade.AdditionalInfo().MM_Ceded_Amount()
            if ceded_amount > new_balance:
                return True
    return False


def create_fixed_amount_cashflow(deposit, amount, date, settle_type=None, cp_account=None, bank=None,
        reversed_cashflow=None, flag=0, shell=None):
    try:
        status = None

        if deposit.Trades()[0].Quantity() > 0:
            sign = 1
        elif deposit.Trades()[0].Quantity() < 0:
            sign = -1
        fixed_amount = amount * sign
        acm.BeginTransaction()
        cf = acm.FCashFlow()
        cf.CashFlowType('Fixed Amount')
        cf.FixedAmount(fixed_amount)
        cf.NominalFactor(1)
        cf.PayDate(date)
        cf.Leg(deposit.Legs().First())

        if cp_account:
            cf.AddInfoValue("CP_Account_Ref", cp_account.Oid())
        if bank:
            cf.AddInfoValue("Bank", bank)

        if settle_type:
            if settle_type == 'Prevent Settlement':
                cf.AddInfoValue("Prvnt_CF_Settlement", "Yes")

            elif settle_type == 'Please Phone':
                status = "{0}: {1}".format(settle_type, cf.CreateUser().FullName())
            else:
                status = settle_type
            cf.AddInfoValue("Settle_Type", status)
            if settle_type == 'Reversal' and reversed_cashflow:
                cf.AddInfoValue("Reversed_CF_Ref", reversed_cashflow.Oid())

        trade = deposit.Trades()[0]
        portfolio = trade.Portfolio()

        if portfolio.AdditionalInfo().NoticePortfolio() == True:
            secondary_deposit_amount = noticeAmount(portfolio, "Secondary Deposit")
            access_deposit_amount = noticeAmount(portfolio, "Access Withdrawal")
            secondary_capacity_balance = access_deposit_amount + secondary_deposit_amount
            if amount > 0:
                if is_almost_zero(secondary_capacity_balance):
                    cf.AddInfoValue("Deposit_Notice_Type", "Primary Deposit")
                else:
                    cf.AddInfoValue("Deposit_Notice_Type", "Secondary Deposit")
            elif amount < 0:
                if settle_type == "Call to Term":
                    cf.AddInfoValue("Deposit_Notice_Type", "Notice Withdrawal")
                else:
                    cf.AddInfoValue("Deposit_Notice_Type", "Access Withdrawal")

        cf.Commit()
        acm.CommitTransaction()

        ael.poll()
        if not flag:
            msg = "The deposit was successfully adjusted. (MSG3)"
            msg_box_ok(msg, shell=shell)

            if settle_type == "Call to Term":  # Open a new term deposit if Call To Term is selected as settle type.
                openNewTermDeposit(deposit, settle_type, amount)

        return cf

    except Exception as ex:
        acm.AbortTransaction()
        msg = "Cannot adjust the deposit. (MSG1)\n {ex}".format(ex=ex)
        LOGGER.error(msg)
        if not flag:
            msg_box_ok(msg, type_="Error", shell=shell)


def exceed_deposit_minimum_value(deposit, amount):

    first_trade = get_first_trade(deposit)
    if first_trade is not None:
        call_balance = get_current_balance(first_trade)

        if not is_call_loan(call_balance, first_trade):

            new_balance = call_balance + amount
            min_value = deposit.MinimumPiece()
            if new_balance < min_value:
                return True
    return False

def adjust(deposit, amount, date, settle_type=None, cp_account=None, bank=None,
           flag=0, shell=None, reversed_cashflow=None, **extra):
    """Adjust the deposit by generating a new cash flow.

    This function calls the built-int method FInstrument.AdjustDeposit.

    The back-dating counterpart to this function is the backdate function.

    Arguments:
    deposit (FDeposit) -- Deposit instrument to adjust.
    amount (float) -- Nominal amount of the cash flow.
    date (ael_date|acm date) -- Pay Day of the cash flow.
    settle_type (string) -- Type of settlement.
    cp_account (FAccount) -- Counterparty account for the settlement.
    bank (string) -- Counterparty's bank.
    flag (?) -- ?
    shell (FUxShell) -- shell of the parent frame; if set, the message boxes
        will be modal
    reversed_cashflow -- A cashflow being reversed by the adjust.
    **extra (?) -- ?
    """

    cf = None
    # ABITFA-4290: Prevent turning a loan into a deposit.
    if turning_loan_into_deposit(deposit, amount):
        msg = ("Cannot adjust the loan. The amount would change the balance "
               "to a positive value and turn the loan into a deposit. (MSG12)")
        LOGGER.error(msg)
        msg_box_ok(msg, type_="Error", shell=shell)
        return

    if exceed_deposit_minimum_value(deposit, amount):
        msg = ("Cannot adjust the deposit. The amount would breach minimum balance of {balance} (MSG12)"
               .format(balance=deposit.MinimumPiece()))
        LOGGER.error(msg)
        msg_box_ok(msg, type_="Error", shell=shell)
        return

    if balance_is_ceded(deposit, amount):
        msg = ("Cannot adjust the deposit. The amount would change the balance below the ceded value (MSG14)")
        LOGGER.error(msg)
        msg_box_ok(msg, type_="Error", shell=shell)
        return

    if not deposit.Legs():
        msg = "Cannot adjust the deposit. It has no legs. (MSG2)"
        LOGGER.error(msg)
        msg_box_ok(msg, type_="Error", shell=shell)
        return

    if can_be_adjusted(deposit):

        cf = create_fixed_amount_cashflow(deposit, amount, date, settle_type, cp_account, bank, reversed_cashflow,
            flag, shell)

    else:
        trd = extra['trades'].AsList()[0]
        if trd.add_info('Funding Instype') == 'Call Prime Brokerage Funding':
            if trd.Quantity() == 1.0:
                amount = -amount
            if not deposit.AdjustDeposit(amount, date,
                                         -1.0):  # AdjustDeposit function does not work for Quantity (3rd arg) 1.0
                msg = "Cannot adjust the deposit. (MSG4)"
                LOGGER.error(msg)
                if not flag:
                    msg_box_ok(msg, type_="Error", shell=shell)
            ael.poll()
            cnum = 1
            if not deposit.Legs():
                msg = "Cannot adjust the deposit. It has no legs. (MSG5)"
                LOGGER.error(msg)
                msg_box_ok(msg, type_="Error", shell=shell)
                return
            for x in deposit.Legs()[0].CashFlows():
                if x.Oid() > cnum and x.CashFlowType() == 'Fixed Amount':
                    cnum = x.Oid()
            cf = acm.FCashFlow[cnum]
            if settle_type == 'Prevent Settlement':
                at_addInfo.save(cf, "Prvnt_CF_Settlement", "Yes")

        elif isEquityCallAccount(deposit):
            if trd.Quantity() == 1.0:
                amount = -amount
            if not deposit.AdjustDeposit(amount, date,
                                         -1.0):  # AdjustDeposit function does not work for Quantity (3rd arg) 1.0
                msg = "Cannot adjust the deposit. (MSG6)"
                LOGGER.error(msg)
                if not flag:
                    msg_box_ok(msg, type_="Error", shell=shell)
        else:
            msg = ("Cannot adjust the deposit. It has more than one live "
                   "trade. (Mirror trades are counted as one.) (MSG7)")
            LOGGER.error(msg)
            if not flag:
                msg_box_ok(msg, type_="Error", shell=shell)

    return cf


def intEndDay(ins, date):
    """
    Examine all the legs of the provided instrument.
    Then examine all the cashflows on each of those legs.
    Look for cashflows of type "Call Fixed Rate Adjustable".
    If such a cashflow is found, check its start date and end date.
    If the provided date is between those two dates,
    get the currently examined cashflow's end date and immediately stop.
   If no such cashflow is found, then return None.
    """

    date = ael.date(date)
    for l in ins.Legs():
        for c in l.CashFlows():
            if c.CashFlowType() == 'Call Fixed Rate Adjustable':
                if date >= ael.date(c.StartDate()) and date < ael.date(c.EndDate()):
                    return ael.date(c.EndDate())


def last_interest_start_date(instrument):
    """Return the start date of the last interest cashflow."""
    start_date = "1970-01-01"
    for leg in instrument.Legs():
        for cashflow in leg.CashFlows():
            if cashflow.CashFlowType() == "Call Fixed Rate Adjustable":
                start_date = max(start_date, cashflow.StartDate())
    return start_date


def backdate(ins, amount, date, payday=None, settle_type=None, cp_account=None,
             bank=None, flag=0, shell=None, reversed_cashflow=None):
    """Adjust the deposit by generating a back-dated cash flow.

    This function is the back-dating counterpart to the adjust function.
    """

    # Use today's date for Pay Date by default.
    if payday is None:
        payday = acm.Time.DateToday()

    # ABITFA-4290: Prevent turning a loan into a deposit.
    if turning_loan_into_deposit(ins, amount):
        msg = ("Cannot adjust the loan. The amount would change the balance "
               "to a positive value and turn the loan into a deposit. (MSG12)")
        LOGGER.error(msg)
        msg_box_ok(msg, type_="Error", shell=shell)
        return

    orgdate = date
    cflist = acm.FArray()
    leg = ins.Legs()[0]
    cf = ""

    if not can_be_adjusted(ins):
        msg = ("Cannot adjust the deposit '{0}'. It must have exactly one live "
               "trade. (Mirror trades are counted as one.) (MSG13)"
               .format(ins.Name()))
        LOGGER.error(msg)
        msg_box_ok(msg, type_="Error", shell=shell)
        return

    # Rerate.
    if ael.date_today() == ael.date_today().first_day_of_month():
        inst = ael.Instrument[ins.Oid()]
        if inst.exp_day == ael.date_today():
            inst.re_rate(ael.date_today(), (float)(CallCurrentRate.call_current_rate(ins, ins.Trades()[0].Oid())))
            if not flag:
                LOGGER.info("Rerate was successful. (MSG8)")

    # Fixed Amount (the amount being deposited/withdrawn).
    cfamount = leg.CreateCashFlow()
    cfamount.FixedAmount = amount*ins.Trades()[0].Quantity()
    cfamount.NominalFactor = 1
    cfamount.StartDate = orgdate
    # NOTE: The core Front Arena logic considers the Pay Date the Value Date
    # for interest calculation. Therefore, if backdating, i.e. the actual fixed
    # amount Value Date is before the current interest period start date, we
    # should set the Pay Date to the interest period start date.  Otherwise the
    # days between the the interest period start date and the Pay Date wouldn't
    # be included in the interest calculation.
    # (See ABITFA-4943 for more details.)
    cfamount.PayDate = last_interest_start_date(ins)
    cfamount.CashFlowType = "Fixed Amount"
    cfamount.Commit()
    cf_fixed = cfamount
    ael.poll()

    #CFD Sweeping, Settlement should not be created
    if settle_type == 'Prevent Settlement':
        LOGGER.info(cfamount)
        at_addInfo.save(cfamount, "Prvnt_CF_Settlement", "Yes")

    if not flag:
        LOGGER.info("Fixed Amount was successful. (MSG10)")

        cashf = ael.CashFlow[cfamount.Oid()]
        if settle_type:
            if settle_type == "Please Phone":
                status = "Backdate: {0}: {1}".format(settle_type, cfamount.CreateUser().FullName())
            else:
                status = "Backdate: {0}".format(settle_type)

            setAddInfoEntity(cashf, 'Settle_Type', status)
            if settle_type == 'Reversal' and reversed_cashflow:
                at_addInfo.save(cfamount, "Reversed_CF_Ref", reversed_cashflow.Oid())

        if cp_account:
            at_addInfo.save(cfamount, "CP_Account_Ref", cp_account.Oid())
        if bank:
            setAddInfoEntity(cashf, 'Bank', bank)
    # / Fixed Amount.

    # Fixed Rate Adjustable (interest on the backdated amount for
    # already-settled periods).
    cfinterest = None
    int_per_end = intEndDay(ins, date)
    while int_per_end is not None and int_per_end < ael.date_today():
        reset = ins.CurrentReset(ael.date(date))
        cf = reset.CashFlow()
        cfinterest = leg.CreateCashFlow()
        cfinterest.Apply(cf)
        cfinterest.StartDate = date
        cfinterest.GenerateResets(0, 0)
        if not leg.Reinvest():
            cfinterest.PayDate = payday
        cfinterest.EndDate = int_per_end
        #date=date.add_months(1).first_day_of_month()
        date = int_per_end
        cfinterest.CashFlowType = "Fixed Rate Adjustable"
        cfinterest.NominalFactor = -amount*ins.Trades()[0].Quantity()
        cfinterest.Commit()
        int_per_end = intEndDay(ins, date)

        if not flag:
            if settle_type:
                if settle_type == "Please Phone":
                    status = "Backdate: {0}: {1}".format(settle_type, cfinterest.CreateUser().FullName())
                else:
                    status = "Backdate: {0}".format(settle_type)
                setAddInfoEntity(ael.CashFlow[cfinterest.Oid()], 'Settle_Type', status)
            if bank:
                setAddInfoEntity(ael.CashFlow[cfinterest.Oid()], 'Bank', bank)

        for r in cfinterest.Resets():
            reset = ins.CurrentReset(r.StartDate())
            rate = reset.FixingValue()
            rc = r.Clone()
            rc.FixingValue = rate
            r.Apply(rc)
            r.Commit()
        if leg.Reinvest():
            cflist.Add((cf.StartDate(), -cashflow_projected_cf(cfinterest.Oid()), -cashflow_projected_cf(cf.Oid()), cf))

        #CFD Sweeping, Settlement should not be created
        if settle_type == "Prevent Settlement":
            at_addInfo.save(cfinterest, "Prvnt_CF_Settlement", "Yes")

    if not flag:
        LOGGER.info("Fixed Rate Adjustable was successful. (MSG9)")

    ael.poll()

    # Interest Reinvestment.
    if leg.Reinvest():
        cflist.Sort()
        LOGGER.info(cflist)
        for cfdata in cflist:
            print cfdata[1], cfdata[2], cashflow_projected_cf(cfdata[3].Oid()), cfdata[3].StartDate(), cfdata[3].EndDate()
            reinvest = leg.CreateCashFlow()
            reinvest.CashFlowType = "Interest Reinvestment"
            reinvest.FixedAmount = cfdata[1]-cfdata[2]-cashflow_projected_cf(cfdata[3].Oid())
            reinvest.PayDate = cfdata[3].EndDate()
            reinvest.NominalFactor = 1
            reinvest.Commit()
            ael.poll()

    if not flag:
       msg = "Backdate Adjust deposit was successful. (MSG11)"
       LOGGER.info(msg)
       msg_box_ok(msg, shell=shell)

    return cf_fixed


def isEquityCallAccountTrade(t):
    """
    Return True if the trade is considered an equity call account.

    The function tests that
        (1) the acquirer and counterparty are in a static list, and
        (2) the acquirer and counterparty are not the same, and
        (3) the portfolio is Call_SBL* or SBL*.
    """
    if t.add_info('Funding Instype') == 'Call Prime Brokerage Funding':
        return True

    list_ = ['EQ Derivatives Desk', 'SECURITY LENDINGS DESK']
    comp = [t.Counterparty().Name(), t.Acquirer().Name()]
    for j in comp:
        if j in list_:
            list_.remove(j)
    if len(list_) == 0:
        pat = r'(Call_){0,1}SBL.*'
        if re.match(pat, t.Portfolio().Name()):
            return True
    else:
        return False


def isEquityCallAccount(ins):
    """
    Return True if the instrument is considered an equity call account,
    False otherwise.
    """
    return all([isEquityCallAccountTrade(x) for x in ins.Trades()])


def get_effective_rule(ssi):
    """Return the effective SSI Rule, or None if none exists.

    Arguments:
    ssi (FSettleInstruction) -- Settle Instruction to test.
    """
    effective_rule = None
    for rule in ssi.Rules():
        if rule.EffectiveFrom() > acm.Time.DateNow():
            continue
        if rule.EffectiveTo() and rule.EffectiveTo() < acm.Time.DateNow():
            continue
        effective_rule = rule
        break
    return effective_rule


def get_effective_ssis(trade, cftype=None):
    """Return a list of effective Settle Instructions (SSIs).

    The returned list of SSIs is ordered by the number of criteria matching
    the trade and cashflow type (the count of statements in the corresponding
    FASQLQuery) in descending order; the most specific SSIs appear first in
    the list.

    Arguments:
    trade (FTrade) -- Trade for which the settlement is to be done.
    cftype (str)   -- Type of the cashflow that is to be settled; e.g.
                      "Fixed Amount" or "Call Fixed Rate Adjustable".
    """
    acquirer = trade.Acquirer()
    counterparty = trade.Counterparty()
    currency = trade.Currency()

    # Create a simulated settlement to get the matching SSIs.
    tmp_settlement = acm.FSettlement()
    tmp_settlement.Trade(trade)
    tmp_settlement.Acquirer(acquirer)
    tmp_settlement.Counterparty(counterparty)
    tmp_settlement.Currency(currency)
    tmp_settlement.Type(cftype)

    if counterparty is None:
        return []
    ssis = []
    for ssi in counterparty.SettleInstructions():
        # Get SSI query either from the Query() or QueryFilter() method.
        if ssi.Query():
            ssi_query = ssi.Query().Query()
        elif ssi.QueryFilter():
            ssi_query = ssi.QueryFilter()
        else:
            continue
        if (ssi_query.IsSatisfiedBy(tmp_settlement)
                and get_effective_rule(ssi) is not None):
            ssis.append((ssi, ssi_query.StatementCount()))

    return [i[0] for i in sorted(ssis, key=lambda x: x[1], reverse=True)]


def get_cp_cash_account_from_ssi(ssi):
    """Return the CP Cash Account from the Settle Instruction.

    Arguments:
    ssi (FSettleInstruction) -- Settle Instruction to get the CP account from.

    Returns FAccount, or None if no CP Cash Account is set.
    """
    cp_cash_account = None
    effective_rule = get_effective_rule(ssi)
    if effective_rule is not None:
        cp_cash_account = effective_rule.CashAccount()
    return cp_cash_account


def get_settlement_accounts(trade, cashflow_type):
    """Return the default settlement accounts.

    Arguments:
    trade (FTrade) -- Trade that is the subject of this settlement.
    cashflow_type (str) -- Type of the cashflow; e.g. "Fixed Amount".
    """

    # Create a simulated settlement to get the accounts.
    # This settlement won't be saved, only kept in memory.
    tmp_settlement = acm.FSettlement()
    tmp_settlement.Trade(trade)
    tmp_settlement.Acquirer(trade.Acquirer())
    tmp_settlement.Counterparty(trade.Counterparty())
    tmp_settlement.Currency(trade.Currency())
    tmp_settlement.Type(cashflow_type)

    # Call the core logic to set the accounts.
    acm.Operations.AccountAllocator().SetSettlementAccountInfo(tmp_settlement)

    # Extract and return the account info from the simulated settlement.
    counterparty_account = None
    if tmp_settlement.Counterparty() is not None:
        cp_acc_query = "name='{name}' and party='{party}'".format(
                       name=tmp_settlement.CounterpartyAccName(),
                       party=tmp_settlement.Counterparty().Oid())
        matching_cp_accounts = acm.FAccount.Select(cp_acc_query)
        if len(matching_cp_accounts) > 1:
            print("Warning - FCallDepositFunctions.get_settlement_accounts: "
                  "Duplicate accounts with the name '{0}' on the Party '{1}'."
                  .format(tmp_settlement.CounterpartyAccName(),
                          tmp_settlement.Counterparty().Name()))
        if matching_cp_accounts:
            counterparty_account = matching_cp_accounts[0]

    acquirer_account = None
    if tmp_settlement.Acquirer() is not None:
        acq_acc_query = "name='{name}' and party='{party}'".format(
                        name=tmp_settlement.AcquirerAccName(),
                        party=tmp_settlement.Acquirer().Oid())
        matching_acq_accounts = acm.FAccount.Select(acq_acc_query)
        if len(matching_acq_accounts) > 1:
            print("Warning - FCallDepositFunctions.get_settlement_accounts: "
                  "Duplicate accounts with the name '{0}' on the Party '{1}'."
                  .format(tmp_settlement.AcquirerAccName(),
                          tmp_settlement.Acquirer().Name()))
        if matching_acq_accounts:
            acquirer_account = matching_acq_accounts[0]

    return {"counterparty_account": counterparty_account,
            "acquirer_account": acquirer_account}


def update_add_info(entity,field_name,value,*rest):
    flag = 0
    for a in entity.additional_infos():
        if a.addinf_specnbr.field_name == field_name:
            flag = a.valnbr
    if flag:
        a = ael.AdditionalInfo[flag].clone()
        a.value = value
        a.commit()
    else:
        aspec = ael.AdditionalInfoSpec[field_name]
        tc = entity.clone()
        an = ael.AdditionalInfo.new(tc)
        an.value = value
        an.addinf_specnbr = aspec
        an.commit()


#Johann : Create new deposit
def openNewTermDeposit(deposit, settle_type, amount):


    #Check if any trades exist on the Call Account, the latest trade will be used to populate some info on the new term trade.
    if deposit.Trades():
        originalTrade = deposit.Trades()[-1]
        #Create a new deposit instrument
        #originalTrade.AdditionalInfo().Trade_Instruct(settle_type)
        #originalTrade.Commit()


        originalTrade.AdditionalInfo().Trade_Instruct(settle_type)
        originalTrade.Commit()
        newDepIns = acm.DealCapturing.CreateNewInstrument('Deposit')

        #Set information on the new term trade
        firstLeg = newDepIns.Legs()[0]
        sourceFirstLeg = deposit.Legs()[0]
        sourceEndDate = sourceFirstLeg.EndDate()
        firstLeg.StartDate(sourceEndDate)
        newDepIns.ContractSize(abs(amount))

        # Suggest new name for Instrument
        # newDepIns.Name(newDepIns.SuggestName())

        # Display after instrument updates
        #acm.StartApplication('Bond', newDepIns)

        # Create a new Trade
        newTrade = acm.DealCapturing.CreateNewTrade(newDepIns)

        # Set Front Office information on new trade
        # We are creating a deposit trade therefore the quantity should be -1
        quantity = -1
        newTrade.Quantity(quantity)
        newTrade.Counterparty(originalTrade.Counterparty())
        newTrade.Acquirer(originalTrade.Acquirer())

        # Set Back Office information on new trade
        newTrade.ContractTrade(originalTrade)
        newTrade.ConnectedTrade(originalTrade.Oid())

        # Set Additional Info
        newTrade.AdditionalInfo().Trade_Instruct(settle_type)

        x = acm.StartApplication('Deposit/Loan', newTrade)
        x.EditTrade().Quantity(quantity)
