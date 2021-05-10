import acm
from at import addInfo
from at_logging import getLogger
from PS_Functions import get_pb_fund_counterparty
from PB_Saxo_general import (
                             get_alias_from_alias_or_cp,
                             get_saxo_depo_portfolio,
                             get_saxo_cp,
                             )

CALL_ACCNT_TMPL = "%(curr)s/SAXO_%(alias)s_CallAcc"
CALL_IMARGIN_TMPL = "%(curr)s/SAXO_%(alias)s_InitMarg"

DEPO_CALL_ACCOUNT_TYPE = "CALL_ACCOUNT"
DEPO_MARGIN_ACCOUNT_TYPE = "MARGIN_ACCOUNT"
DEPO_TYPES = (
              DEPO_CALL_ACCOUNT_TYPE,
              DEPO_MARGIN_ACCOUNT_TYPE,
              )

LOGGER = getLogger(__name__)


def check_depos_existence(alias, currency, from_date):
    LOGGER.info("Checking depos...")
    for depo_type in DEPO_TYPES:
        create_deposit(alias, currency, depo_type, from_date)


def get_account_name(alias, curr, depo_type):
    alias = get_alias_from_alias_or_cp(alias)
    if depo_type == "CALL_ACCOUNT":
        name_acc = "CallAcc"
    else:
        name_acc = "InitMargin"
    return curr + '/' + "SAXO" + "_" + alias + "_" + name_acc


def get_call_account_name(alias_or_cp, curr):
    alias = get_alias_from_alias_or_cp(alias_or_cp)
    return CALL_ACCNT_TMPL % {'curr':curr, 'alias':alias}

    
def get_imargin_account_name(alias_or_cp, curr):
    alias = get_alias_from_alias_or_cp(alias_or_cp)
    return CALL_IMARGIN_TMPL % {'curr':curr, 'alias':alias}


def get_call_account(alias_or_cp, curr):
    name = get_call_account_name(alias_or_cp, curr)
    return _get_ins(name)


def get_imargin_account(alias_or_cp, curr):
    name = get_imargin_account_name(alias_or_cp, curr)
    return _get_ins(name)


def _get_ins(name):
    ins = None
    try:
        ins = acm.FInstrument[name]
        if not ins:
            raise RuntimeError("Nonexisting instrument: '%s'" % name)
        trades = _ins_trades(ins)
        if len(trades) != 2:
            raise RuntimeError("Call Account '%s' trades error. Excpected 2 trades, found %d"
                % (name, len(trades)))
    except Exception:
        ins = None
    return ins


def _get_depo_name(alias, depo_type, curr):
    if depo_type == "CALL_ACCOUNT":
        return get_call_account_name(alias, curr)
    else:
        return get_imargin_account_name(alias, curr)


def _get_depo(alias, depo_type, curr):
    name = _get_depo_name(alias, depo_type, curr)
    return _get_ins(name)


def _ins_trades(instr):
    trades = [t for t in instr.Trades() if t.Status() not in ('Simulated', 'Void', 'Terminated')]
    return trades


def create_deposit(alias, currency, depo_type, from_date):

    name = _get_depo_name(alias, depo_type, currency)
    ins = acm.FInstrument[name]
    if ins:
        trds_size = len(_ins_trades(ins))
        if trds_size == 2:
            return ins
        elif trds_size > 0:
            raise RuntimeError("Invalid number of call account '%s' trades. Expected 2, found: %d"
                % (ins.Name(), trds_size))

    # creating new deposits (4) and their trades here

    curr = acm.FCurrency[currency]
    cal = curr.Calendar()
    day_count_method = curr.Legs()[0].DayCountMethod()
    cparty = get_pb_fund_counterparty(alias)
    end_date = cal.AdjustBankingDays(from_date, 20)
    next_month = acm.Time.FirstDayOfMonth(acm.Time.DateAddDelta(from_date, 0, 1, 0))

    # can't use transaction while creating 2 trades in transaction
    # since validation rule would change one of the portfolios to Graveyard
    # acm.BeginTransaction()
    try:
        if not ins:
            
            LOGGER.info("Creating depo: '%s'", name)
            
            ins = acm.FDeposit()
            ins.Name(name)
            ins.Currency(curr)
            ins.ContractSize(1)
            ins.DateFrom(from_date)
            ins.Otc(True)
            ins.OpenEnd('Open End')
            ins.PayOffsetMethod('Business Days')
            ins.PriceFindingChlItem(
                acm.FChoiceList.Select('list = "PriceFindingGroup" and name = "Close"')[0])
            ins.SpotBankingDaysOffset(0)
            ins.ShortDividendFactor(1)
            ins.ValuationGrpChlItem(
                acm.FChoiceList.Select('list = "ValGroup" and name = "AC_GLOBAL_Funded"')[0])
            ins.QuoteType('Clean')
            ins.Quotation('Clean')
            ins.OpenEnd('Open End')
            ins.ExpiryDate(end_date)
            ins.MinimumPiece(100000000)
            ins.RoundingSpecification('Rounding_FX_2Dec')



            leg = ins.CreateLeg(False)
            # leg = acm.FLeg()
            leg.PayCalendar(cal)
            leg.ResetCalendar(cal)
            leg.Currency(curr)
            leg.Decimals(11)
            leg.FloatRateFactor(1)
            leg.FixedRate(0)
            leg.NominalFactor(1)
            leg.FixedCoupon(True)
            leg.PayLeg(False)
            leg.DayCountMethod(day_count_method)
            leg.NominalAtEnd(True)
            leg.Rounding('Normal')
            leg.RollingPeriod("1m")
            leg.EndPeriodUnit("Days")
            leg.ResetDayOffset(0)
            leg.ResetType("Weighted")
            leg.ResetPeriod("1d")
            leg.ResetDayMethod("Following")
            leg.RollingPeriodBase(next_month)
            leg.PayDayMethod("Following")
            leg.Reinvest(True)

            leg.StartDate(from_date)
            leg.EndDate(end_date)
            leg.LegType('Call Fixed Adjustable')
            leg.StrikeType("Absolute")

            ins.RegisterInStorage()
            leg.Instrument(ins)
            # leg.Commit()

            ins.Commit()


            addInfo.save(ins, "CE Bankruptcy", "YES")

        if not ins.Trades():

            LOGGER.info("Booking depo trades...")
            
            trade = acm.FTrade()
            trade.Instrument(ins)
            trade.Portfolio(get_saxo_depo_portfolio())
            trade.Currency(curr)
            trade.Quantity(1)
            trade.Counterparty(get_saxo_cp())
            trade.Acquirer(acm.FInternalDepartment['PRIME SERVICES DESK'])
            trade.ValueDay(from_date)
            trade.AcquireDay(from_date)
            trade.TradeTime(from_date)
            trade.Status("BO Confirmed")
            trade.Trader(acm.User())

            trade.RegisterInStorage()
            trade.AdditionalInfo().Funding_Instype("Call Prime Brokerage Funding")
            trade.Commit()

            acc_name = get_account_name(alias, currency, depo_type)
            addInfo.save(trade, 'Account_Name', acc_name)

            trade2 = trade.Clone()
            trade2.Counterparty(cparty)
            trade2.ValueDay(from_date)
            trade2.AcquireDay(from_date)
            trade2.TradeTime(from_date)
            trade2.Quantity(-1)
            trade2.RegisterInStorage()
            trade2.AdditionalInfo().Funding_Instype("Call Prime Brokerage Funding")
            trade2.Commit()
            addInfo.save(trade2, 'Account_Name', acc_name)
            
            LOGGER.info("\tTrades booked: %d, %d", trade.Oid(), trade2.Oid())

        # acm.CommitTransaction()
    except Exception as exc:
        # acm.AbortTransaction()
        LOGGER.exception("Instrument '%s' not created: %s", name, exc)
        raise
    
    return ins


# print create_deposit("MAP110", "GBP", "CALL_ACCOUNT", "2017-06-06").Name()
