"""
------------------------------------------------------------------------------------------------------------------------
PROJECT                 :  Prime Brokerage Project
MODULE                  :  PS_TradeFees
PURPOSE                 :  Define fees for caps and floors.
DEPATMENT AND DESK      :  Prime Services
REQUESTER               :  Francois Henrion
DEVELOPER               :  Anil Parbhoo
CR NUMBER               :  850964
------------------------------------------------------------------------------------------------------------------------

HISTORY
========================================================================================================================
Date        Change no      Developer          Description
------------------------------------------------------------------------------------------------------------------------
            CR699989       Paul J.-Guillarmod Initial deployment
            CR750738       Herman Hoon        Added the ReturnTradeFee function
            CR750738       Anil Parbhoo       Change the calculation for BsB, Repo, Bond Future, Bond Option,
                                              Swaption, FRN, Currency future and Currency Option
            CR752067       Anil Parbhoo       Correct the calculation fee for currency futures and options
                                              on currency futures
            CR754294       Anil Parbhoo       Redefine fees for bond trades
            CR756719       Anil Parbhoo       Define fees for caps and floors
            CR850964       Paul J.-Guillarmod Added logic to suppress trade fee calculation
            CR850964       Anil Parbhoo       Update trade fee calculation for Cando options on FRAs and
                                              currency options
            CR889562       Paul J.-Guillarmod Expanded trade fee suppression logic. Fixed bug where close
                                              out options caused the delta calculation to fail.
            CHNG126505     Anil Parbhoo       Changed the calculation for the currency option fee based
                                              on the contract size of the instrument
2012-05-16  CHNG194115     Peter Fabian       Added function AddCFDFees for calculating fees for CFDs.
                                              Plus small refactoring
2012-05-25  CR230018       Nidheesh Sharma    Changed the vatFactor so it uses _GetVATFactor(trade) and not 1.14
2012-06-18  CR264971       Peter Fabian       SET needs to be added in the overnight batch as well, removed
                                              some functions which are not needed anymore
2012-11-30  CHNG620460     Peter Fabian       Removed the code that calculated CFD fees here, now they're
                                              calculated on the fly during sweeping
2013-02-18  CHNG809119     Peter Kutnik       Updates for Voice fees on Equities
2013-03-04  CHNG842516     Peter Fabian       Update of fees for YieldX currency derivatives to sliding scale calc
2013-04-10  CHNG935599     Peter Fabian       Added support for Int fut fees
2013-06-13  CHNG1092563    Peter Fabian       Added fees for bonds with counterparty = ABSA, use benchmark
                                              delta for bonds (instead of yield delta)
2013-06-21  CHNG0001124273 Peter Kutnik       Bond fees to be payable on trade date, not value date
2013-06-25  C1127529       Hynek Urban        Make currency derivatives fees customizable per clients
2013-02-06  C1682284       Hynek Urban        Change the default YieldX fee to 1.8 (from 1.75)
2014-12-11  CHNG0002501286 Libor Svoboda      SET fee 2015 update
2015-06-11  CHNG0002889266 Jakub Tomaga       STT payments excluded from Property Stocks
2016-10-18  CHNG0004031972 Jakub Tomaga       Sliding coef for currency derivatives updated
2019-03-07  FAPE-21        Jaco Swanepoel     Change execution fee payments to use a new additional payment
                                              fee type called 'Execution Fee'. This applies to all products
                                              except Bonds which will be converted at a later date.
2020-05-04  FAPE-288       Marian Zdrazil     BIDVEST Note trading
2020-07-23  FAPE-138       Marian Zdrazil     Change calculation of execution fees for Agris/commodity derivatives
2020-09-25  FAPE-154       Marian Zdrazil     Remove STT charges for Nil Paid trades

------------------------------------------------------------------------------------------------------------------------
"""




import acm

from at_logging import getLogger
import PS_Functions
import PS_TimeSeriesFunctions
from PS_BrokerFeesRates import get_vat_for_date


LOGGER = getLogger(__name__)

calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time.DateToday()
PREV_BUSINESS_DAY = calendar.AdjustBankingDays(TODAY, -1)

STRATE_TS_AEL = 'PS_TradeFees'
STRATE_LOWER = 'Strate_lower'
STRATE_FACTOR = 'Strate_factor'
STRATE_LOWER_LIM = 'Strate_lower_lim'
STRATE_UPPER_LIM = 'Strate_upper_lim'

MATRIX_FUNDS = [
    "MATBINK",
    "MATFI",
    "MATMULT",
    "MAP110",
    "MATFI2",
    "MATMULT2",
    "MATBINK2",
    "MAP110B",
    "MATBINK3",
    "MATFI3",
    "MATMULT3",
    "MAP110C",
    "MATFI4",
    "MATMULT4",
    "MATBINK4",
    "MAP110D",
    "MATBLUE",
    "MATBLUE2",
    "MATBLUE3",
    "MATBLUE4"
]
FAIRTREE_FUNDS = ["FAIRFIGM", "FAIRWOD"]
NOVARE_FUNDS = ["NOVFI3"]
SOUTHCHESTER_FUNDS = ["SSEPRHF"]
KADD_FUNDS = ["SAKADD"]
AAMAQUA_FUNDS = ["AAMAQUA"]

ONE_BIP = 0.0001
ONE_PERCENT = 0.01
CONTR_SIZE_CURR_FUT = 1000.0
FIVE_K_RAND_CEILING = 5000.00
# TO SET NUMBER OF DAYS IN A YEAR FOR ACT/365 DAY COUNT METHOD
DAYS_IN_YEAR = 365


def reporting_portfolios(shortname_list):
    """
        Return list of reporting portfolios for given list of shortnames.
    """
    for shortname in shortname_list:
        counterparty = PS_Functions.get_pb_fund_counterparty(shortname)
        yield PS_Functions.get_pb_reporting_portfolio(counterparty)


def is_client_trade(trade, client_funds):
    """
        Return True if trade sits under reporting compound of a fund in list.
    """
    for reporting_portfolio in reporting_portfolios(client_funds):
        if PS_Functions.is_child_portf(trade.Portfolio(), reporting_portfolio):
            return True

    shortname = PS_Functions.get_pb_fund_shortname(trade.Counterparty())
    if shortname in client_funds:
        return True

    return False


def matrix_execution_rate(trade):
    """
        Return negotiated execution rate for MATRIX.

        Execution fee calculation required greater granularity for MATRIX:
        1. FRAs with an end date less than 5 months from trade date should be 10bps
        2. FRAs with an end date greater than 5 months from trade date should be
           20 bps
        3. Swaps with an end date less than 5 years should be 20 bps
        4. Swaps with an end date of greater than 5 years should be 45 bps
        5. Bonds should be 15bps
        6. Caps / Floors / Swaptions should be 25 bps (benchmark delta of highest
           underlying delta reference if a straddle). This execution fee will be
           booked manually by FO - therefore rate 0bps
        7. Otherwise rate will be extracted from a portfolio
    """
    trade_date = _RemoveTime(trade.TradeTime())
    instrument = trade.Instrument()
    if instrument.InsType() == "FRA":
        treshold_date = acm.Time().DateAddDelta(trade_date, 0, 5, 0)
        if instrument.EndDate() <= treshold_date:
            rate = 0.1
        else:
            rate = 0.2
    elif instrument.InsType() == "Swap":
        treshold_date = acm.Time().DateAddDelta(trade_date, 5, 0, 0)
        if instrument.EndDate() <= treshold_date:
            rate = 0.20
        else:
            rate = 0.45
    elif instrument.InsType() == "Bond":
        rate = 0.15
    elif instrument.InsType() in ["Cap", "Floor"]:
        rate = 0.0
    elif instrument.InsType() == "Option" and instrument.Underlying().InsType() in ["FRA", "Swap"]:
        rate = 0.0
    else:
        rate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(
            trade.Portfolio(), trade_date)
    return rate


def fairtree_execution_rate(trade):
    """
        Return negotiated execution rate for FAIRTREE.

        Execution fee calculation required greater granularity for FAIRTREE:
        1. FRAs should be 25 bops
        2. Swaps with an end date less than 5 years should be 25 bps
        3. Swaps with an end date of greater than 5 years should be 150 bps
        4. Bonds should be 15bps
        5. Caps / Floors / Swaptions should be 25 bps (benchmark delta of highest
           underlying delta reference if a straddle). This execution fee will be
           booked manually by FO - therefore rate 0bps
        6. Otherwise rate will be extracted from a portfolio
    """
    trade_date = _RemoveTime(trade.TradeTime())
    instrument = trade.Instrument()
    if instrument.InsType() == "FRA":
        rate = 0.25
    elif instrument.InsType() == "Swap":
        treshold_date = acm.Time().DateAddDelta(trade_date, 5, 0, 0)
        if instrument.EndDate() <= treshold_date:
            rate = 0.25
        else:
            rate = 1.50
    elif instrument.InsType() == "Bond":
        rate = 0.15
    elif instrument.InsType() in ["Cap", "Floor"]:
        rate = 0.0
    elif instrument.InsType() == "Option" and instrument.Underlying().InsType() in ["FRA", "Swap"]:
        rate = 0.0
    else:
        rate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(
            trade.Portfolio(), trade_date)
    return rate


def novare_execution_rate(trade):
    """
        Return negotiated execution rate for NOVARE.

        Execution fee calculation required greater granularity for NOVARE:
        1. Swaps with an end date less than 5 years should be 25 bps
        2. Swaps with an end date of greater than 5 years should be 150 bps
    """
    trade_date = _RemoveTime(trade.TradeTime())
    instrument = trade.Instrument()
    if instrument.InsType() == "Swap":
        treshold_date = acm.Time().DateAddDelta(trade_date, 5, 0, 0)
        if instrument.EndDate() <= treshold_date:
            rate = 0.25
        else:
            rate = 1.50
    else:
        rate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(
            trade.Portfolio(), trade_date)
    return rate


def southchester_execution_rate(trade):
    """
        Return negotiated execution rate for SOUTHCHESTER.

        Execution fee calculation required greater granularity for SOUTHCHESTER:
        1. Swaps with an end date less than 5 years should be 25 bps
        2. Swaps with an end date of greater than 5 years should be 150 bps
    """
    trade_date = _RemoveTime(trade.TradeTime())
    instrument = trade.Instrument()
    if instrument.InsType() == "Swap":
        treshold_date = acm.Time().DateAddDelta(trade_date, 5, 0, 0)
        if instrument.EndDate() <= treshold_date:
            rate = 0.25
        else:
            rate = 1.50
    else:
        rate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(
            trade.Portfolio(), trade_date)
    return rate


def kadd_execution_rate(trade):
    """
        Return negotiated execution rate for KADD.

        Execution fee calculation required greater granularity for KADD:
        1. Swaps with an end date less than 5 years should be 25 bps
        2. Swaps with an end date of greater than 5 years should be 45 bps
    """
    trade_date = _RemoveTime(trade.TradeTime())
    instrument = trade.Instrument()
    if instrument.InsType() == "Swap" or instrument.InsType() == "FRA":
        treshold_date = acm.Time().DateAddDelta(trade_date, 5, 0, 0)
        if instrument.EndDate() <= treshold_date:
            rate = 0.25
        else:
            rate = 0.45
    else:
        rate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(
            trade.Portfolio(), trade_date)
    return rate


def aamaqua_execution_rate(trade):
    """
        Return negotiated execution rate for AAMAQUA .

        Execution fee calculation required greater granularity for AAMAQUA :
        1. Swaps and FRAs with an end date less than 5 years should be 25 bps
        2. Swaps and FRAs with an end date of greater than 5 years should be 55 bps
    """
    trade_date = _RemoveTime(trade.TradeTime())
    instrument = trade.Instrument()
    if instrument.InsType() in ("Swap", "FRA"):
        threshold_date = acm.Time().DateAddDelta(trade_date, 5, 0, 0)
        rate = 0.25 if instrument.EndDate() <= threshold_date else 0.55
    else:
        rate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(
            trade.Portfolio(), trade_date)
    return rate


def get_execution_rate(trade):
    """
        Return execution fee for a trade.

        It is not possible to customise execution fee rate
        per instrument type on FA UI, therefore for certain portfolios
        the customisation is done only in the codebase.
        This will be removed when it is possible to set in UI.
    """
    trade_date = _RemoveTime(trade.TradeTime())
    custom_execution_rates = (
        (MATRIX_FUNDS, matrix_execution_rate),
        (FAIRTREE_FUNDS, fairtree_execution_rate),
        (NOVARE_FUNDS, novare_execution_rate),
        (SOUTHCHESTER_FUNDS, southchester_execution_rate),
        (KADD_FUNDS, kadd_execution_rate),
        (AAMAQUA_FUNDS, aamaqua_execution_rate),
    )

    # Constant rate for CDS
    if trade.Instrument().InsType() == 'CreditDefaultSwap':
        return 0.015

    for fund, custom_execution_rate in custom_execution_rates:
        if is_client_trade(trade, fund):
            return custom_execution_rate(trade)

    return PS_TimeSeriesFunctions.GetExecutionPremiumRate(trade.Portfolio(), trade_date)


def isTakeonTrade(trade):
    takeOnFlag4 = trade.OptKey4()
    takeOnFlag3 = trade.OptKey3()

    if takeOnFlag4 and takeOnFlag4.Name() == 'PS No Fees':
        return True
    elif takeOnFlag3 and takeOnFlag3.Name() == 'PS No Fees':
        return True
    else:
        return False


def _RemoveTime(date):
    """
        Remove the time from an acm datetime and return the date.
    """
    return date.split(" ")[0]


def _add_payment(trade, amount, fee_type):
    """
        Add or update a fee payment on a trade.
    """
    if not amount:
        return

    LOGGER.debug("Adding payment to trade %s, amount %s, fee type %s", trade.Oid(), amount, fee_type)
    trade_date = _RemoveTime(trade.TradeTime())

    # KUTNIKPE tactical exception for Bond execution fees.
    if (fee_type == 'Execution Fee' and trade.Instrument().InsType() in ('Bond', 'FRN', 'IndexLinkedBond')):
        pay_day = trade_date
    else:
        pay_day = trade.ValueDay()

    party = acm.FParty['PRIME SERVICES DESK']

    for payment in trade.Payments():
        if payment.Text() == fee_type or payment.Type() == fee_type:
            payment.Amount(amount)
            payment.PayDay(pay_day)
            payment.ValidFrom(trade_date)
            payment.Commit()
            LOGGER.info("Updated %s on trade %d to %g", fee_type, trade.Oid(), amount)
            break
    else:
        payment = acm.FPayment()
        payment.Trade(trade)
        payment.Currency(acm.FInstrument['ZAR'])

        # There are specific Additional Payment types for the fee types in the list below
        if fee_type in ['INS', 'SET', 'STT', 'Brokerage Vatable', 'DWT', 'Execution Fee']:
            payment.Type(fee_type)
        else:
            payment.Type('Cash')
            payment.Text(fee_type)

        payment.Party(party)
        payment.Amount(amount)
        payment.PayDay(pay_day)
        payment.ValidFrom(trade_date)
        payment.Commit()
        LOGGER.info("Added %s on trade %d to %g", fee_type, trade.Oid(), amount)


def _add_note_payment(trade, amount, fee_type):
    """
    Add an execution fee payment on a note trade.
    """
    if not amount:
        return

    LOGGER.debug("Adding payment to note trade %s, amount %s, fee type %s", trade.Oid(), amount, fee_type)

    party = acm.FParty['PRIME SERVICES DESK']

    payment = acm.FPayment()
    payment.Trade(trade)
    payment.Currency(acm.FInstrument['ZAR'])
    payment.Type(fee_type)
    payment.Party(party)
    payment.Amount(amount)
    payment.PayDay(TODAY)
    payment.ValidFrom(TODAY)
    payment.Commit()
    LOGGER.info("Added %s on note trade %d to %g", fee_type, trade.Oid(), amount)


def _IsHedgeInternal(trade):
    """
        Check to see if the trade is hedged with a trade from an internal desk.
    """
    hedgeTrade = trade.TrxTrade()
    if hedgeTrade and hedgeTrade.Counterparty().Type() == 'Intern Dept':
        return True
    else:
        return False


def _readDefaultExtensionAttribute(obj, extensionAttribute):
    defaultContext = acm.GetDefaultContext()
    evaluator = acm.GetCalculatedValue(obj, defaultContext, extensionAttribute)
    if not evaluator:
        raise Exception('Could not load extension attribute [%s]' % extensionAttribute)
    else:
        return evaluator.Value()


def _GetVATFactor(trade):
    """
        Depending on the instrument type VAT will be calculated on fees.  The calculation is done in ADFL as its
        needed for other extension attributes.
    """
    vat_rate = get_vat_for_date(_RemoveTime(trade.TradeTime()))
    return vat_rate


def _CalculateFixedIncomeExecutionFee(trade):
    """
        Execution fee calculation for fixed income instruments.
        This is based on the Execution Rate addinfo on the trade
        portfolio and the yield delta of the trade.
        An execution fee is not added for trades
        that are hedged internally.
    """
    if trade.Status() not in ['Void', 'Simulated']:
        if trade.Instrument().InsType() not in ('Bond', 'FRN', 'IndexLinkedBond')\
                and trade.Instrument().Otc()\
                and _IsHedgeInternal(trade):
            feeFactor = 0.0
        else:
            feeFactor = 1.0

        executionRate = get_execution_rate(trade)
        vatFactor = _GetVATFactor(trade)

        if trade.Instrument().InsType() in ('Bond', 'FRN', 'IndexLinkedBond', 'CreditDefaultSwap'):
            tradeDelta = PS_Functions.TradeBenchmarkDelta(trade)
        else:
            tradeDelta = PS_Functions.TradeYieldDelta(trade)

        return -1.0 * abs(tradeDelta * vatFactor * executionRate * feeFactor)

    return 0


def _PriceDeltaCash(trade):
    calculationSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
    value = calculationSpace.CalculateValue(trade, 'Portfolio Delta Cash')
    try:
        value = value.Number()
    except Exception as exc:
        value = value

    return value


def _CalculateDerivativeExecutionFee(trade):
    """
        Execution fee calculation for derivatives.
    """
    instrument = trade.Instrument()
    instrumentType = instrument.InsType()

    tradeDate = _RemoveTime(trade.TradeTime())
    executionRate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(trade.Portfolio(), tradeDate) * ONE_PERCENT
    vatFactor = _GetVATFactor(trade)
    priceDeltaCash = _PriceDeltaCash(trade)

    if instrumentType == 'Future/Forward' and trade.Status() not in ['Void', 'Simulated']:
        return -1.0 * abs(vatFactor * executionRate * priceDeltaCash)

    elif instrumentType == 'Option' and trade.Status() not in ['Void', 'Simulated']:
        if instrument.add_info('Cando Option'):
            b = abs(vatFactor * executionRate * priceDeltaCash)
            feeList = [b, FIVE_K_RAND_CEILING]

            return -1.0 * (max(feeList))
        else:
            return -1.0 * abs(vatFactor * executionRate * priceDeltaCash)


def _GetFXRate(instrument, currencyName):
    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    fxRateCalculation = instrument.Calculation().FXRate(calcSpace, currencyName)
    try:
        fxRate = fxRateCalculation.Number()
    except Exception as exc:
        fxRate = 0.0

    return fxRate


def _GetDelta(instrument):
    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    deltaCalculation = instrument.Calculation().PriceDelta(calcSpace)
    try:
        delta = deltaCalculation.Number()
    except Exception as exc:
        delta = 0.0

    return delta


def _CalculateCurrencyFutureExecutionFee(trade):
    if not(_IsHedgeInternal(trade)) and trade.Status() not in ['Void', 'Simulated']:
        instrument = trade.Instrument()
        underlying = instrument.Underlying()
        insCurrency = instrument.Currency().Name()

        spot = _GetFXRate(underlying, insCurrency)
        vatFactor = _GetVATFactor(trade)
        nominal = trade.Quantity() * instrument.ContractSize()

        tradeDate = _RemoveTime(trade.TradeTime())
        executionRate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(trade.Portfolio(), tradeDate) / (instrument.ContractSize())

        return -1.0 * abs(nominal * vatFactor * executionRate * spot)

    return 0


def _CalculateCurrencyFutureOptionExecutionFee(trade):
    if not(_IsHedgeInternal(trade)) and trade.Status() not in ['Void', 'Simulated']:
        instrument = trade.Instrument()
        underlying = instrument.Underlying()
        undUnderlying = underlying.Underlying()
        insCurrency = instrument.Currency().Name()

        spot = _GetFXRate(undUnderlying, insCurrency)
        vatFactor = _GetVATFactor(trade)

        tradeDate = _RemoveTime(trade.TradeTime())
        executionRate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(trade.Portfolio(),
                                                                       tradeDate) / CONTR_SIZE_CURR_FUT

        feeValue = abs(vatFactor * trade.Quantity() * instrument.ContractSize() * spot * executionRate)

        if instrument.InsType() == 'Option' and instrument.add_info('Cando Option'):
            return -1.0 * max([feeValue, FIVE_K_RAND_CEILING])
        else:
            delta = _GetDelta(instrument)
            return -1.0 * abs(feeValue * delta)

    return 0


def _CalculateCurrencyOptionExecutionFee(trade):
    if not(_IsHedgeInternal(trade)) and trade.Status() not in ['Void', 'Simulated']:
        instrument = trade.Instrument()
        underlying = instrument.Underlying()
        insCurrency = instrument.Currency().Name()

        spot = _GetFXRate(underlying, insCurrency)
        vatFactor = _GetVATFactor(trade)

        tradeDate = _RemoveTime(trade.TradeTime())
        executionRate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(trade.Portfolio(), tradeDate)

        if instrument.ContractSize() == CONTR_SIZE_CURR_FUT:
            contract_size_factor = CONTR_SIZE_CURR_FUT
        else:
            contract_size_factor = 1.0

        feeValue = abs(vatFactor * trade.Quantity() * instrument.ContractSize() * spot * executionRate / contract_size_factor)

        if instrument.InsType() == 'Option' and instrument.add_info('Cando Option'):
            return -1.0 * max([feeValue, FIVE_K_RAND_CEILING])
        else:
            delta = _GetDelta(instrument)
            return -1.0 * abs(feeValue * delta)

    return 0


def _is_nil_paid(stock_name):
    # Nil Paid name should look like: ZAR/SUI (regular stock) --> ZAR/SUIN (Nil Paid)
    # 8 characters long, 4th char being back-slash, 8th letter 'N'
    if len(stock_name) == 8:
        if stock_name[7] == 'N' and stock_name[3] == '/':
            reg_stock_name = stock_name[:7]
            reg_stock = acm.FStock[reg_stock_name]
            if reg_stock is not None:
                return True
    return False


def _CalculateSTT(trade):
    """
        Securities Transfer Tax calculation for stock trades. Only charged when receiving equity, not selling it.
        STT is the only equity fee with no VAT.
    """
    nil_paid = _is_nil_paid(trade.Instrument().Name())
    if (trade.Instrument().InsType() in ['Stock'] and trade.Instrument().Name() not in
            ['ZAR/STXRAF'] and trade.Quantity() > 0 and trade.Status() not in ['Void', 'Simulated'] and not nil_paid):
        # Exclude STT paymetns from Property Stocks
        product_type = trade.Instrument().ProductTypeChlItem()
        if product_type and product_type.Name() == "Property Stock":
            return 0
        sttFactor = float(25) * ONE_BIP
        return -1.0 * abs(trade.Premium()) * sttFactor
    return 0


def _CalculateINS(trade):
    """
        Investor Protection Levy for equity trades.
    """
    if trade.Instrument().InsType() in ['Stock', 'ETF'] and trade.Status() not in ['Void', 'Simulated']:
        insFactor = float(2) * ONE_BIP * ONE_PERCENT
        vatFactor = _GetVATFactor(trade)
        return -1.0 * abs(trade.Premium()) * insFactor * vatFactor
    return 0


def _CalculateSET(trade, orderValue):
    """
        Strate Levies and Fees for equity trades.
    """
    if trade.Instrument().InsType() in ['Stock', 'ETF'] and trade.Status() not in ['Void', 'Simulated']:
        tradeDate = _RemoveTime(trade.TradeTime())
        textObj = acm.FAel[STRATE_TS_AEL]
        strateLower = _GetTSValue(STRATE_LOWER, textObj, tradeDate)
        strateFactor = _GetTSValue(STRATE_FACTOR, textObj, tradeDate)
        strateLowerLim = _GetTSValue(STRATE_LOWER_LIM, textObj, tradeDate)
        strateUpperLim = _GetTSValue(STRATE_UPPER_LIM, textObj, tradeDate)

        if orderValue < strateLowerLim:
            setFactor = strateLower
        elif orderValue <= strateUpperLim:
            setFactor = orderValue * strateFactor * ONE_BIP
        else:
            setFactor = strateUpperLim * strateFactor * ONE_BIP

        vatFactor = _GetVATFactor(trade)
        if abs(orderValue) > ONE_BIP:
            return -1.0 * abs(trade.Premium() / float(orderValue)) * setFactor * vatFactor
    return 0


def _CalculateEquityBrokerage(trade):
    """
        Brokerage for equity trades.
    """
    if trade.Instrument().InsType() in ['Stock', 'ETF'] and trade.Status() not in ['Void', 'Simulated']:
        tradeDate = _RemoveTime(trade.TradeTime())

        # Calculate brokerage at different rates based on whether the trade
        tradeType = trade.EquityTradeType()
        LOGGER.info(tradeType)
        if tradeType == 'Trade Report':
            executionRate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(trade.Portfolio(), tradeDate,
                                                                           'Non-DMA') * ONE_PERCENT
        elif tradeType == 'Voice':
            executionRate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(trade.Portfolio(), tradeDate,
                                                                           'Voice') * ONE_PERCENT
        else:
            executionRate = PS_TimeSeriesFunctions.GetExecutionPremiumRate(trade.Portfolio(),
                                                                           tradeDate) * ONE_PERCENT
        vatFactor = _GetVATFactor(trade)
        return -1.0 * abs(trade.Premium()) * executionRate * vatFactor
    return 0


def _SlidingScaleFeePerContract(scalesDict, feeAbove, qty):
    """
        Determines the fee per contract for sliding scale
        methodology given a dictionary of upper boundaries -> fees
        and quantity of the trade.
        For all quantities above the max boundary in the dictionary
        feeAbove is used as fee per contract.
    """
    found = 0
    qty = abs(qty)
    for bucketCap in sorted(scalesDict.keys()):
        if qty <= bucketCap:
            found = 1
            break
    if found:
        feePerContract = scalesDict[bucketCap]
    else:
        feePerContract = feeAbove
    return feePerContract


def _get_counterparty_for_agency_trade(trade):
    prf = trade.Portfolio()
    call_accnt = prf.AdditionalInfo().PSClientCallAcc()
    if not call_accnt or not call_accnt.Trades():
        return
    return call_accnt.Trades()[0].Counterparty()


def _CalculateYieldXCurrFutureFee(trade):
    """
        Caluclate fee for YieldX FX Future
        using 'sliding scale' methodology
    """
    cparty = _get_counterparty_for_agency_trade(trade)
    if cparty and cparty.AdditionalInfo().PS_YXFutureFeeCoef():
        ABSAFutureFeeCoef = cparty.AdditionalInfo().PS_YXFutureFeeCoef()
    else:
        ABSAFutureFeeCoef = 2.0
    futuresSlidingScale = {
        499: 1.37,
        999: 1.32,
        2999: 1.20,
        4999: 1.12,
        7499: 1.02,
        9999: 0.63,
    }
    qty = trade.Quantity()
    return -1.0 * abs(qty * _SlidingScaleFeePerContract(futuresSlidingScale, 0.38, qty) * ABSAFutureFeeCoef)


def _CalculateYieldXCurrOptionFee(trade):
    """
        Calculate fee for YieldX FX Option
        using 'sliding scale' methodology
    """
    cparty = _get_counterparty_for_agency_trade(trade)
    if cparty and cparty.AdditionalInfo().PS_YXOptionFeeCoef():
        ABSAOptionFeeCoef = cparty.AdditionalInfo().PS_YXOptionFeeCoef()
    else:
        ABSAOptionFeeCoef = 2.0
    optionsSlidingScale = {
        499: 0.69,
        999: 0.67,
        2999: 0.61,
        4999: 0.56,
        7499: 0.53,
        9999: 0.32,
    }
    qty = trade.Quantity()
    return -1.0 * abs(qty * _SlidingScaleFeePerContract(optionsSlidingScale, 0.21, qty) * ABSAOptionFeeCoef)


def _calculate_fut_opt_agris_execution_fee(trade):
    """
        Calculate execution fee for Agris/commodity futures and options
    """
    counter_party = _get_counterparty_for_agency_trade(trade)
    if counter_party and counter_party.AdditionalInfo().PS_YXFutureFeeCoef():
        future_fee_coef = counter_party.AdditionalInfo().PS_YXFutureFeeCoef()
    else:
        future_fee_coef = 2.0

    trd_add_info = trade.AdditionalInfo()
    clearing_fee = trd_add_info.PS_ClearingFee()
    exchange_fee = trd_add_info.PS_ExchangeFee()

    if clearing_fee is None:
        clearing_fee = 0.0
    if exchange_fee is None:
        exchange_fee = 0.0

    return -1.0 * abs((clearing_fee + exchange_fee) * future_fee_coef)


def _calculate_commodities_fee(trade):
    """
        Calculate execution fee on commodities and derivatives on them.
    """
    calc_space = acm.FCalculationSpace('FTradeSheet')
    safex_fee_with_vat = calc_space.CalculateValue(trade, 'SAFEX Total Fee Incl VAT')
    trade_portfolio = trade.Portfolio()
    simple_rate_factor = trade_portfolio.AdditionalInfo().PSSimpleRateFactor()
    return safex_fee_with_vat * simple_rate_factor


def _IsYieldXCurrDeriv(trade):
    """
        Try to determine whether the instrument
        is YieldX curr derivative
        (using external id/optional key on the trade
        which should be set by YieldX adapter)
    """
    if 'YIELDX' in trade.OptionalKey().upper():
        return True
    else:
        return False


def _GetTSValue(tsName, entity, date):
    """
        Return a time series value corresponding to the input 'tsName'
        and 'entity' with date equal or closest lower than the input
        'date'. If no such a time series exists, raise exception.
    """
    ts = PS_TimeSeriesFunctions.GetTimeSeries(tsName, entity)
    try:
        return [entry.TimeValue() for entry in
                sorted(ts, key=lambda point: point.Day(), reverse=True)
                if date >= entry.Day()][0]
    except TypeError:
        raise Exception("Time Series '%s' for '%s' not found."
                        % (tsName, type(entity)))
    except IndexError:
        raise Exception("Time Series '%s' for '%s' does not contain any entry before or at %s."
                        % (tsName, type(entity), date))


def add_note_fee(trade):
    """
        Calculate execution fees for BIDVEST note in PB_CE_FF_BIDGLOBLB_CR portfolio
    """
    days = acm.Time.DateDifference(TODAY, PREV_BUSINESS_DAY)
    value = -1.0 * days * trade.Quantity() * get_execution_rate(trade) * trade.Instrument().used_price() * ONE_PERCENT / DAYS_IN_YEAR
    _add_note_payment(trade, value, 'Execution Fee')


def add_trade_fees(trade, prop_factor, order_value=0):
    """
        Calculate the fees for a trade and add them as payments.
        This function is called from a scheduled script
        and run daily to add fees to new trades.

        The prop_factor variable will be used to change the sign
        of fees when adding payments onto trades in the prop tree.
        The default is to assume the fees will be for the client,
        not from Absa's point of view.
    """
    LOGGER.debug("Adding trade %s, prop-factor %s, order value %s", trade.Oid(), prop_factor, order_value)
    if isTakeonTrade(trade):
        return

    instype = trade.Instrument().InsType()
    underlying = trade.Instrument().Underlying()

    if instype in ['Stock', 'ETF']:
        ins_fee = _CalculateINS(trade)
        _add_payment(trade, prop_factor * ins_fee, 'INS')

        brokerage = _CalculateEquityBrokerage(trade)
        _add_payment(trade, prop_factor * brokerage, 'Brokerage Vatable')

        stt_fee = _CalculateSTT(trade)
        _add_payment(trade, prop_factor * stt_fee, 'STT')

        set_fee = _CalculateSET(trade, order_value)
        _add_payment(trade, prop_factor * set_fee, 'SET')

    elif instype in ['Future/Forward', 'Option']:
        underlying_instype = underlying.InsType()

        if underlying_instype == 'Commodity':
            execution_fee = _calculate_fut_opt_agris_execution_fee(trade)

        elif underlying_instype in ('Bond', 'FRN', 'IndexLinkedBond'):
            execution_fee = _CalculateFixedIncomeExecutionFee(trade)

        elif underlying_instype == 'Curr':
            if _IsYieldXCurrDeriv(trade):
                if instype == 'Future/Forward':
                    execution_fee = _CalculateYieldXCurrFutureFee(trade)
                else:  # instype == 'Option'
                    execution_fee = _CalculateYieldXCurrOptionFee(trade)
            else:
                if instype == 'Future/Forward':
                    execution_fee = _CalculateCurrencyFutureExecutionFee(trade)
                else:  # instype == 'Option'
                    execution_fee = _CalculateCurrencyOptionExecutionFee(trade)

        elif instype == 'Option':
            if underlying_instype in ('Swap', 'FRA'):
                execution_fee = _CalculateFixedIncomeExecutionFee(trade)
            elif (underlying_instype == 'Future/Forward' and underlying.
                    Underlying().InsType() == 'Curr'):
                execution_fee = _CalculateCurrencyFutureOptionExecutionFee(trade)
            elif (underlying_instype == 'Future/Forward' and underlying.
                    Underlying().InsType() == 'Commodity'):
                execution_fee = _calculate_fut_opt_agris_execution_fee(trade)
            else:
                execution_fee = _CalculateDerivativeExecutionFee(trade)
        else:
            execution_fee = _CalculateDerivativeExecutionFee(trade)

        _add_payment(trade, prop_factor * execution_fee, 'Execution Fee')

    elif instype in ['Bond',
                     'Cap',
                     'FRA',
                     'FRN',
                     'Floor',
                     'IndexLinkedBond',
                     'Swap',
                     'CurrSwap',
                     'CreditDefaultSwap']:

        execution_fee = _CalculateFixedIncomeExecutionFee(trade)
        _add_payment(trade, prop_factor * execution_fee, 'Execution Fee')

    elif instype == 'Commodity':
        commodities_fee = _calculate_commodities_fee(trade)
        _add_payment(trade, prop_factor * commodities_fee, 'Execution Fee')


def ReturnFee(tradeArray, feeType, startDate, endDate):
    """
        Return the sum of all fees of a particular type.
    """
    totalFee = 0.0
    for trade in [trd for trd in tradeArray if
                  trd.Status() not in ['Void', 'Simulated'] and (startDate < _RemoveTime(trd.TradeTime()) <= endDate)]:
        for payment in trade.Payments():
            if payment.Text() == feeType or payment.Type() == feeType:
                totalFee += payment.Amount()

    return totalFee


def ReturnTotalFee(tradeArray, startDate, endDate):
    """
        Return the sum of all fees except for STT.
    """
    totalFee = 0.0
    for trade in [trd for trd in tradeArray if
                  trd.Status() not in ['Void', 'Simulated'] and (startDate < _RemoveTime(trd.TradeTime()) <= endDate)]:
        for payment in trade.Payments():
            if payment.Type() in ['INS', 'SET', 'Brokerage Vatable', 'Execution Fee']:
                totalFee += payment.Amount()

    return totalFee


def ReturnTradeFee(trade):
    """
        Return the sum of all fees except for STT.
    """
    totalFee = 0.0
    for payment in trade.Payments():
        if payment.Type() in ['INS', 'SET', 'Brokerage Vatable', 'Execution Fee']:
            totalFee += payment.Amount()
    return totalFee


def GetInternationalExecutionFee(trade):
    """
        Return the international trade fee (International Fee).
    """
    for payment in trade.Payments():
        feeType = payment.Text()
        if feeType in ['IntlExecutionFee']:
            return acm.DenominatedValue(payment.Amount(), payment.Currency(), None)
    return acm.DenominatedValue(0, trade.Currency(), None)
