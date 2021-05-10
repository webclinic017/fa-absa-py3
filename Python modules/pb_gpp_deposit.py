import acm
import at_addInfo
from at_logging import getLogger

from PS_Functions import get_pb_fund_counterparty

from pb_gpp_general import (
                            get_alias_from_alias_or_cp,
                            get_depo_portf,
                            get_gpp_cp,
                            )

LOGGER = getLogger(__name__)

CALL_ACCNT_TMPL = "%(curr)s/GPP_%(alias)s_CallAcc"
CALL_IMARGIN_TMPL = "%(curr)s/GPP_%(alias)s_InitMarg"

DEPO_CALL_ACCOUNT_TYPE = "CALL_ACCOUNT"
DEPO_MARGIN_ACCOUNT_TYPE = "MARGIN_ACCOUNT"
DEPO_TYPES = (
              DEPO_CALL_ACCOUNT_TYPE,
              DEPO_MARGIN_ACCOUNT_TYPE,
              )


def check_depos_existence(alias, currency, from_date):
    LOGGER.info("Checking depos...")
    for depo_type in DEPO_TYPES:
        ins = create_deposit(alias, currency, depo_type, from_date)
        LOGGER.info("Existing depo: %s (trades: %s)" % (ins.Name(), ins.Trades()))


def _get_account_name(alias, curr, depo_type):
    alias = get_alias_from_alias_or_cp(alias)
    if depo_type == DEPO_CALL_ACCOUNT_TYPE:
        name_acc = "CallAcc"
    else:
        name_acc = "InitMargin"
    return "{0}/{1}_{2}_{3}".format(curr, "GPP", alias, name_acc)


def get_call_account(alias_or_cp, curr):
    if isinstance(curr, str):
        return _get_depo(alias_or_cp, DEPO_CALL_ACCOUNT_TYPE, curr)
    return _get_depo(alias_or_cp, DEPO_CALL_ACCOUNT_TYPE, curr.Name())


def get_imargin_account(alias_or_cp, curr):
    if isinstance(curr, str):
        return _get_depo(alias_or_cp, DEPO_MARGIN_ACCOUNT_TYPE, curr)
    return _get_depo(alias_or_cp, DEPO_MARGIN_ACCOUNT_TYPE, curr.Name())


def _get_depo_name(alias, depo_type, curr):
    alias = get_alias_from_alias_or_cp(alias)
    if depo_type == DEPO_CALL_ACCOUNT_TYPE:
        name = CALL_ACCNT_TMPL % {'curr':curr, 'alias':alias}
    else:
        name = CALL_IMARGIN_TMPL % {'curr':curr, 'alias':alias}
    return name


def _get_depo(alias, depo_type, curr):
    name = _get_depo_name(alias, depo_type, curr)
    ins = acm.FInstrument[name]
    if not ins:
        raise RuntimeError("Nonexisting depo '%s'" % name)
    
    trades = [t for t in ins.Trades() if t.Status() not in ('Simulated', 'Terminated', 'Void')]
    if len(trades) != 2:
        raise RuntimeError("Invalid depo '%s' trade. Expected 2 valid trades, found %d"
            % (name, len(trades)))
    
    return ins


def create_deposit(alias, currency, depo_type, from_date):
    name = _get_depo_name(alias, depo_type, currency)
    ins = acm.FInstrument[name]
    if ins:
        return ins

    curr = acm.FCurrency[currency]
    cal = curr.Calendar()
    day_count_method = curr.Legs()[0].DayCountMethod()
    cparty = get_pb_fund_counterparty(alias)
    end_date = cal.AdjustBankingDays(from_date, 20)
    next_month = acm.Time.FirstDayOfMonth(acm.Time.DateAddDelta(from_date, 0, 1, 0))

    # can't use transaction while creating 2 trades in transaction
    # since validation rule would change one of the portfolios to Graveyard
    try:
        if not ins:
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

            ins.Commit()

            at_addInfo.save(ins, "CE Bankruptcy", "YES")

        if ins.Trades() and len([t for t in ins.Trades() 
            if t.Status() not in ('Simulated', 'Void', 'Terminated')]) != 2:
            
            raise RuntimeError("Invalid number of call account 's' trades. Expected 2, got: %d" \
                % (ins.Name(), len(ins.Trades())))
                
        if not ins.Trades():

            trade = acm.FTrade()
            trade.Instrument(ins)
            trade.Portfolio(get_depo_portf())
            trade.Currency(curr)
            trade.Quantity(1)
            trade.Counterparty(get_gpp_cp())
            trade.Acquirer(acm.FInternalDepartment['PRIME SERVICES DESK'])
            trade.ValueDay(from_date)
            trade.AcquireDay(from_date)
            trade.TradeTime(from_date)
            trade.Status("BO Confirmed")
            trade.Trader(acm.User())

            trade.RegisterInStorage()
            trade.AdditionalInfo().Funding_Instype("Call Prime Brokerage Funding")
            trade.Commit()

            acc_name = _get_account_name(alias, currency, depo_type)
            at_addInfo.save(trade, 'Account_Name', acc_name)

            trade2 = trade.Clone()
            trade2.Counterparty(cparty)
            trade2.ValueDay(from_date)
            trade2.AcquireDay(from_date)
            trade2.TradeTime(from_date)
            trade2.Quantity(-1)
            trade2.RegisterInStorage()
            trade2.AdditionalInfo().Funding_Instype("Call Prime Brokerage Funding")
            trade2.Commit()
            at_addInfo.save(trade2, 'Account_Name', acc_name)

    except Exception as exc:
        exc_msg = "ERROR: Depo instrument '%s' not created: %s" % (name, str(exc))
        LOGGER.error(exc_msg)
        raise

    LOGGER.info("Depo instrument '%s' created (trades: [%d, %d])",
        ins.Name(), trade.Oid(), trade2.Oid())
    return ins

