"""-----------------------------------------------------------------------------
Project: Prime Brokerage Project
Department: Prime Services
Requester: Francois Henrion
Developer: Paul Jacot-Guillarmod
CR Number: 666125 (Initial Deployment)

HISTORY
================================================================================
Date       Change no     Developer          Description
--------------------------------------------------------------------------------
2011-06-07 677654        Paul J.-Guillarmod Made an update to sweep Client TPL instead of built in TPL
2011-06-17 685737        Paul J.-Guillarmod Added a functionality to sweep the difference in today's and yesterday's TPL
2011-07-05 704002        Paul J.-Guillarmod Added functionality so that deposits can be made on mirror trades
2011-09-26 782094        Herman Hoon        Split between fully funded and financed
2011-12-08 850928        Herman Hoon        Update to include the Daily Provision in the TPL
2012-06-28 ??????        Anwar Banoo        Enhanced debugging info and tactical fix for interest periods being crossed
2013-04-10 935599        Peter Fabian       Added support for sweeping Int fut fees
2013-04-26 980059        Peter Fabian       Fix of Int fut fees code
2014-03-18 1815805       Ondrej Bahounek    Sweeping bug fixed: Call Account TPL updated even when equals zero
2014-06-26 2026751       Libor Svoboda      Updated functions GetTotal, GetCurrentTotal and IsCurrentInterestPeriod
2015-07-14 2961517       Jakub Tomaga       Sweeping report added
2015-09-11 3090331       Jakub Tomaga       Portfolio independent sweeping
2016-03-17 3506685       Ondrej Bahounek    Accommodate PBA
2018-11-12 CHG1001113453 Tibor Reiss        Enable fully funded CFD for MMIBETA2
2019-03-27 FAPE-65       Tibor Reiss        Remove fully funded CFD for MMIBETA2(yes, you are reading it correctly)
2019-11-21 FAPE-147      Tibor Reiss        Propagate error
2020-11-20 FAPE-460      Marcus Ambrose     Added get_brokers_call_account and get_call_account
-----------------------------------------------------------------------------"""
import acm
from collections import defaultdict

import FCallDepositFunctions
import PS_Functions
import PS_FundingSweeper
from at_logging import getLogger


CALL_ACC_POSTING_THRESHOLD = 0.009
LOGGER = getLogger(__name__)


def get_pswap_tpl(portfolio_swap, date, instrument_type):
    """
    Return a tuple consisting of:
    * the sum of all TPL values on the provided portfolio swap
      for the provided date and the provided instrument type.
    * a dictionary indexed by instrument name
      of sums of all TPL values for the provided date
      for every instrument of the provided type
      on the provided portfolio swap.

    TPL is stored at the position (instrument) level.
    Each value is stored as:
    * fixing value on resets of type "Return", which belong to
    * cashflows whose additional info "PS_FundWarehouse" equals "TPL"
      or is undefined and are present in
    * legs of type "Total Return"
    on a portfolio swap.
    """
    tpl_sum = float()  # 0 of type float
    tpl_dict = defaultdict(float)
    total_return_legs = acm.FLeg.Select(
        'instrument = {0} and legType = "Total Return"'.format(portfolio_swap.Oid())
    )
    for leg in total_return_legs:
        instrument = leg.IndexRef()
        if instrument.InsType() != instrument_type:
            continue
        for cashflow in leg.CashFlows():
            cashflow_subtype = cashflow.AdditionalInfo().PS_FundWarehouse()
            if cashflow_subtype is not None and cashflow_subtype != "TPL":
                continue
            relevant_resets = acm.FReset.Select(
                "cashFlow = {0} "
                'and resetType = "Return" '
                'and day = "{1}"'.format(cashflow.Oid(), date)
            )
            for reset in relevant_resets:
                value = reset.FixingValue()
                tpl_sum += value
                tpl_dict[instrument.Name()] += value
    return (tpl_sum, tpl_dict)


def returnTPLCashFlow(callAccount, instrumentType, portfolioSwap, date):
    """Return the TPL cashflow for a given instrument type, for a given portfolio swap and for a given date."""
    for cashFlow in callAccount.Legs()[0].CashFlows():
        if (
            cashFlow.PayDate() == date
            and cashFlow.add_info("PS_InstrumentType") == instrumentType
            and cashFlow.add_info("PSCashType") == portfolioSwap.Name()
        ):
            return cashFlow
    return None


def IsCurrentInterestPeriod(callAccount, date):
    """Copy of code from ABSAPSSweep"""
    LOGGER.info(
        "Check if %s is in Current Interest Period for %s", date, callAccount.Name()
    )
    nextInterestDay = callAccount.NextScheduledInterestDay()
    lastInterestDay = acm.Time.DateAddDelta(nextInterestDay, 0, -1, 0)
    LOGGER.info(
        """Next Interest Day=%s
    Last Interest Day=%s""",
        nextInterestDay,
        lastInterestDay,
    )

    if (acm.Time().DateDifference(date, nextInterestDay) <= 0) and (
        acm.Time().DateDifference(date, lastInterestDay) >= 0
    ):
        LOGGER.info(
            "Default case for checking if current interest period has been met on account: %s",
            callAccount.Name(),
        )
        return True
    else:
        LOGGER.info(
            "No case met in checking if current interest period has been met on account: %s",
            callAccount.Name(),
        )
        return False


def GetTotal(portfolioSwap, callAccount, date, instrumentType):
    """Modified code from ABSAPSSweep"""
    total = 0
    leg = callAccount.Legs()[0]
    portfolioSwapName = portfolioSwap.Name()

    for cashFlow in leg.CashFlows():
        if (
            not cashFlow.StartDate()
            and not acm.Time.DateDifference(date, cashFlow.PayDate())
            and cashFlow.add_info("PSCashType") == portfolioSwapName
            and cashFlow.add_info("PS_InstrumentType") == instrumentType
        ):
            total = total + cashFlow.FixedAmount()
        elif (
            not acm.Time.DateDifference(date, cashFlow.StartDate())
            and cashFlow.add_info("PSCashType") == portfolioSwapName
            and cashFlow.add_info("PS_InstrumentType") == instrumentType
        ):
            total = total + cashFlow.FixedAmount()

    return total


def GetCurrentTotal(portfolioSwap, callAccount, date, instrumentType):
    """Modified code from ABSAPSSweep"""
    total = 0
    leg = callAccount.Legs()[0]
    portfolioSwapName = portfolioSwap.Name()

    for cashFlow in leg.CashFlows():
        if (
            not acm.Time.DateDifference(date, cashFlow.PayDate())
            and cashFlow.StartDate() == ""
            and cashFlow.add_info("PS_InstrumentType") == instrumentType
            and cashFlow.add_info("PSCashType") == portfolioSwapName
            and cashFlow.CashFlowType() == "Fixed Amount"
        ):
            total = total + round(cashFlow.FixedAmount(), 6)

    return total


def updateCallAccountTPL(
    callAccountTPL, portfolioSwap, callAccount, date, instrumentType
):
    LOGGER.info("------ Start Update CallAccount TPL ------")
    cashFlow = None
    LOGGER.info("Check interest period window")
    if IsCurrentInterestPeriod(callAccount, date):
        total = GetCurrentTotal(portfolioSwap, callAccount, date, instrumentType)
        newTotal = callAccountTPL - total
        LOGGER.info(
            """In current period process
        Current TPL Total=%s
        TPL Total Posting=%s""",
            total,
            newTotal,
        )
        if abs(newTotal) > CALL_ACC_POSTING_THRESHOLD:
            tradeList = callAccount.Trades()
            cashFlow = FCallDepositFunctions.adjust(
                callAccount,
                newTotal,
                date,
                "Prevent Settlement",
                None,
                None,
                1,
                trades=tradeList,
            )
        else:
            LOGGER.info("Skip posting of almost zero: %s", newTotal)
    else:
        total = GetTotal(portfolioSwap, callAccount, date, instrumentType)
        newTotal = callAccountTPL - total
        LOGGER.info(
            """In backdate period process
        Historical TPL Total=%s
        TPL Total Posting=%s""",
            total,
            newTotal,
        )
        if abs(newTotal) > CALL_ACC_POSTING_THRESHOLD:
            dateToday = acm.Time().DateToday()
            cashFlow = FCallDepositFunctions.backdate(
                callAccount,
                newTotal,
                date,
                dateToday,
                "Prevent Settlement",
                None,
                None,
                1,
            )
        else:
            LOGGER.info("Skip posting of almost zero: %s", newTotal)

    if cashFlow:
        PS_Functions.SetAdditionalInfo(cashFlow, "PSCashType", portfolioSwap.Name())
        PS_Functions.SetAdditionalInfo(cashFlow, "PS_InstrumentType", instrumentType)

    LOGGER.info("------ End Update CallAccount TPL ------")
    return (total, newTotal)


def TPLSweeper(portfolio_swap, start_date, end_date):
    """Sweep TPL into the call account for a given data range (inclusive)."""
    LOGGER.info(
        "------ Start process for %s, from %s to %s ------",
        portfolio_swap.Name(),
        start_date,
        end_date,
    )

    trade = PS_Functions.get_instrument_trade(portfolio_swap)
    portfolio = PS_Functions.get_pb_reporting_portfolio(trade.Counterparty())
    call_account = PS_Functions.get_pb_call_account(
        trade.Counterparty(), trade.Currency().Name()
    )
    date_today = acm.Time().DateToday()

    sweeping_class = portfolio_swap.AdditionalInfo().PB_Sweeping_Class()
    LOGGER.info(sweeping_class)

    is_fully_funded = PS_Functions.get_pb_pswap_ff_flag(portfolio_swap)
    LOGGER.info(
        "Params: Portfolio=%s, CallAccount=%s, FullyFunded=%s",
        portfolio.Name(),
        call_account.Name(),
        is_fully_funded,
    )

    if is_fully_funded:
        tpl_columns = ["Portfolio Cash End"]
        if portfolio_swap.Currency().Name() != "ZAR":
            tpl_columns = ["PBA Portfolio Cash End"]
    else:
        tpl_columns = [
            "Client TPL",
            "Daily Funding",
            "Daily Warehousing",
            "Daily Provision",
        ]

    LOGGER.info("TPL Columns=%s", tpl_columns)

    current_tpl_dict = defaultdict(lambda: defaultdict(defaultdict))
    historical_tpl_dict = defaultdict(lambda: defaultdict(defaultdict))
    call_account_tpl_dict = defaultdict(lambda: defaultdict(defaultdict))
    current_tpl_breakdown_dict = defaultdict(lambda: defaultdict(defaultdict))
    historical_tpl_breakdown_dict = defaultdict(lambda: defaultdict(defaultdict))

    if sweeping_class == "Unknown":
        LOGGER.info(
            "Skipping portfolio swap %s with sweeping class 'Unknown'",
            portfolio_swap.Name(),
        )
    else:
        query_folder = acm.FStoredASQLQuery[sweeping_class]
        query = query_folder.Query()
        query = PS_Functions.modify_asql_query(
            query, "Portfolio.Name", False, new_value=portfolio.Name()
        )
        if is_fully_funded:
            query = PS_Functions.add_ff_flag_to_query(query)
        if portfolio_swap.Currency().Name() != "ZAR":
            LOGGER.info(
                "Non ZAR pswap; searching for trades with currency: %s",
                portfolio_swap.Currency().Name(),
            )
            query = PS_Functions.add_currency_to_query(
                query, portfolio_swap.Currency().Name()
            )

        # It is necessary to use a clone,
        # because otherwise the query folder stays modified in memory.
        qf_clone = query_folder.Clone()
        qf_clone.Query(query)

        LOGGER.info("Sweeping class %s: %s trades", sweeping_class, len(query.Select()))

        instrumentTypeGrouper = acm.FAttributeGrouper("Trade.Instrument.InsType")

        calendar = acm.FCalendar["ZAR Johannesburg"]
        for date in PS_Functions.DateGenerator(start_date, end_date):
            if not calendar.IsNonBankingDay(None, None, date):
                previousBankingDay = calendar.AdjustBankingDays(date, -1)
                callAccountTPL = 0
                tplDictionary = PS_FundingSweeper.TradingManagerSweeper(
                    qf_clone, date, tpl_columns, False, instrumentTypeGrouper
                )
                LOGGER.info(
                    """Processing for date=%s
                Previous banking date=%s
                Trading manager call returned=%s""",
                    date,
                    previousBankingDay,
                    tplDictionary,
                )

                current_tpl_dict[date] = tplDictionary
                for instrumentType, tplValues in tplDictionary.items():
                    LOGGER.info(
                        """Iterating TM result=%s
                    \t%s
                    \t%s""",
                        instrumentType,
                        tpl_columns,
                        tplValues,
                    )

                    tm_breakdown = PS_FundingSweeper.TradingManagerSweeperBreakdown(
                        qf_clone,
                        date,
                        instrumentType,
                        tpl_columns,
                        False,
                        instrumentTypeGrouper,
                    )
                    current_tpl_breakdown_dict[date][instrumentType] = tm_breakdown
                    totalTPL = sum(tplValues)

                    (
                        previousBankingDayTPL,
                        previousBankingDayTPLBreakdown,
                    ) = get_pswap_tpl(
                        portfolio_swap, previousBankingDay, instrumentType
                    )

                    historical_tpl_dict[date][instrumentType] = previousBankingDayTPL
                    historical_tpl_breakdown_dict[date][
                        instrumentType
                    ] = previousBankingDayTPLBreakdown
                    # The value that gets swept to the call account will be
                    # (todays tpl) - (yesterdays tpl) + (daily funding and fees)
                    callAccountTPL = totalTPL - previousBankingDayTPL
                    LOGGER.info(
                        """Previous banking day TPL=%s
                    Total TPL for today=%s
                    Call account TPL=%s""",
                        previousBankingDayTPL,
                        totalTPL,
                        callAccountTPL,
                    )

                    (total, new_total) = updateCallAccountTPL(
                        callAccountTPL,
                        portfolio_swap,
                        call_account,
                        date,
                        instrumentType,
                    )
                    call_account_tpl_dict[date][instrumentType] = [
                        callAccountTPL,
                        total,
                        new_total,
                    ]
            else:
                LOGGER.info("Skipping %s - non banking day", date)

    LOGGER.info(
        "------ End process for %s, from %s to %s ------",
        portfolio_swap.Name(),
        start_date,
        end_date,
    )
    return (
        current_tpl_dict,
        historical_tpl_dict,
        call_account_tpl_dict,
        current_tpl_breakdown_dict,
        historical_tpl_breakdown_dict,
    )


def get_call_account(alias, currency):
    if not isinstance(currency, str):
        currency = currency.Name()

    name = "{}/{}_CallAcc".format(currency, alias)
    ins = acm.FInstrument[name]

    if not ins:
        raise RuntimeError("No deposit named {} exists".format(name))
    return ins


def get_brokers_call_account(alias, currency, broker):
    if not isinstance(currency, str):
        currency = currency.Name()

    name = "{}/{}_CallAcc_{}".format(currency, alias, broker)
    ins = acm.FInstrument["{}".format(name)]

    if not ins:
        raise RuntimeError("No deposit named {} exists".format(name))
    return ins
