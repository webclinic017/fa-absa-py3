'''
MODULE
    CashFlow_Recon: To extract all money flows and/or the Valend of trades for the Liquidity and capital funding team.
HISTORY
==============================================================================
2015-08-04 TEMS-849 Andrei Conicov Have added counterparty CSA related columns 
------------------------------------------------------------------------------
'''

import acm
import ael
from at_time import acm_date, to_datetime
from traceback import print_exc
import datetime

# FAST_MODE skips all long calculations, so you will get wrong
#  results, but sooner.
FAST_MODE = False

# LOG_LEVEL 1 displays slow calculations
# LOG_LEVEL 2 displays every record ID as it is calculated
LOG_LEVEL = 1

# Number of minutes to run. 0 means run until finished
MAX_RUNTIME = 0

CALC_SPACE_MONEY = "MONEY_SPACE"
CALC_SPACE_TRADE = "TRADE_SPACE"
CALC_SPACE_START = "START_SPACE"
CALC_SPACE_END = "END_SPACE"


def _log(message):
    print("%s %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))


def _trdfilterList():
    """
    Returns the list of available trade filters
    """
    tradeFilterList = []
    tfs = acm.FTradeSelection.SqlSelect('name', 'name like Liquidity_%')
    for t in tfs:
        tradeFilterList.append(t.ColumnValues()[0])

    return tradeFilterList


INCEPTION = ael.date('1970-01-01')
TODAY = ael.date_today()
PREVBUSDAY = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)
TWODAYSAGO = TODAY.add_days(-2)
YESTERDAY = TODAY.add_days(-1)

EndDateList = {'Now': TODAY.to_string(ael.DATE_ISO),
               'TwoDaysAgo': TWODAYSAGO.to_string(ael.DATE_ISO),
               'PrevBusDay': PREVBUSDAY.to_string(ael.DATE_ISO),
               'Yesterday': YESTERDAY.to_string(ael.DATE_ISO),
               'Custom Date': TODAY.to_string(ael.DATE_ISO)}

InstType = {'CFD': 'INS_CFD',
            'SWAP': 'INS_SWAP',
            'CAP': 'INS_CAP',
            'TOTALRETURNSWAP': 'INS_TOTAL_RETURN_SWAP',
            'CURRSWAP': 'INS_CURR_SWAP',
            'CREDITDEFAULTSWAP': 'INS_CREDIT_DEFAULT_SWAP',
            'FUTURE/FORWARD': 'INS_FUTURE',
            'CURR': 'INS_CURR',
            'OPTION': 'INS_OPTION',
            'PRICESWAP': 'INS_PRICE_SWAP',
            'FLOOR': 'INS_FLOOR',
            'FRA': 'INS_FRA',
            'COMBINATION': 'INS_COMBINATION',
            'INDEXLINKEDSWAP': 'INS_INDEX_LINKED_SWAP',
            'VARIANCESWAP': 'INS_VARIANCE_SWAP'}


def _safe_value(value):
    if value is None:
        return 0
    elif hasattr(value, "Number"):
        return value.Number()

    return value


# def _get_formated_value(value, default='', title=None):
#     result = default
#     if hasattr(value, "Number"):
#         result = value.Number()
#     elif value == None:
#         result = 0
#     elif value != None:
#         result = value
#     else:
#         print "{0}: {1}".format(title, value)
#
#     return result

# def _trade_value(trade, endDate, columnId):
#     '''This method returns a value for any money flow object'''
#     calcSpace = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
#
#     try:
#         calcSpace.SimulateValue(trade, 'Portfolio Profit Loss End Date', 'Custom Date')
#         calcSpace.SimulateValue(trade, 'Portfolio Profit Loss End Date Custom', endDate)
#
#         calc = calcSpace.CalculateValue(trade, columnId)
#     finally:
#         calcSpace.Clear()
#         calcSpace.RemoveSimulation(trade, 'Portfolio Profit Loss End Date')
#         calcSpace.RemoveSimulation(trade, 'Portfolio Profit Loss End Date Custom')
#
#     return calc


def _get_value(value):
    if hasattr(value, "IsKindOf") and value.IsKindOf(acm.FDenominatedValue):
        result = value.Number()
    else:
        result = value
    return result


def _fx_rate(fromCurrency, toCurrency, date):
    """Obtains FX rate for a certain date.

    Parameters:
    fromCurrency -- str, eg. USD
    toCurrency -- str, egk. ZAR
    date -- str, eg. 2012-10-10
    """

    if (fromCurrency, toCurrency, date) not in _fx_rate._ccy_cache.keys():
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        fromCurr = acm.FCurrency[fromCurrency]
        toCurr = acm.FCurrency[toCurrency]
        _fx_rate._ccy_cache[(fromCurrency, toCurrency, date)] = fromCurr.Calculation().FXRate(
            calcSpace, toCurr, date).Number()

    return _fx_rate._ccy_cache[(fromCurrency, toCurrency, date)]


class CalcSpaceSet:
    def __init__(self):
        self.spaces = {}

    def add_space(self, space_name, calc_space):
        self.spaces[space_name] = calc_space

    def add_filter(self, space_name, trade_filter):
        self.spaces[space_name].InsertItem(trade_filter)
        self.spaces[space_name].Refresh()

    def add_trade(self, space_name, trade):
        self.spaces[space_name].Clear()
        self.spaces[space_name].InsertItem(trade)
        self.spaces[space_name].Refresh()

    def first_child(self, space_name):
        return self.spaces[space_name].RowTreeIterator().FirstChild()

    def get_val(self, space_name, node, column, description=""):
        try:
            if FAST_MODE:
                return 0.0

            start = datetime.datetime.now()
            result = self.spaces[space_name].CalculateValue(node, column, None, False)
            end = datetime.datetime.now()
            duration = (end - start).total_seconds()
            if LOG_LEVEL and duration > 1.0:
                if description:
                    _log("  Calc '%s' took %.1f seconds (%s)" % (column, duration, description))
                else:
                    _log("    Calc '%s' took %.1f seconds" % (column, duration))

            return result
        except Exception as x:
            print_exc()
            raise Exception("Exception calculating value '%s': %s" % (column, str(x)))

    def get_safe_val(self, space_name, node, column, description=""):
        cs_result = self.get_val(space_name, node, column, description)
        return _safe_value(cs_result)

    def get_zar_val(self, space_name, node, column, fx_rate, description=""):
        amount = self.get_safe_val(space_name, node, column, description)
        return str("%.2f" % (amount * fx_rate))

    def close_all(self):
        for calc_space in self.spaces.values():
            calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
            calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
            calc_space.Clear()


def _cashflow_row(trade, css, node, fromRepDate, toRepDate, expDate, cfCurr, fxRate, cfNumber):
    description = "Trade: %i, Cashflow: %s" % (trade.Oid(), str(cfNumber))
    if LOG_LEVEL > 1:
        _log("ROW %s" % description)

    if trade.Instrument().InsType().upper() not in InstType:
        raise Exception("Unexpected instype '%s', trade %i".format(trade.Instrument().InsType(), trade.Oid()))

    amountPV = css.get_safe_val(CALC_SPACE_MONEY, node, 'Portfolio Present Value', description)
    zarAmountPV = css.get_zar_val(CALC_SPACE_MONEY, node, 'Portfolio Present Value', fxRate, description)
    Amount = css.get_safe_val(CALC_SPACE_MONEY, node, 'Cash Analysis Projected', description)
    zarAmount = css.get_zar_val(CALC_SPACE_MONEY, node, 'Cash Analysis Projected', fxRate, description)

    cfNominal = css.get_val(CALC_SPACE_MONEY, node, 'Cash Analysis Event Face Value', description)
    ZAR_CF_Nominal = css.get_zar_val(CALC_SPACE_MONEY, node, 'Cash Analysis Event Face Value', fxRate, description)

    Nominal = css.get_val(CALC_SPACE_MONEY, node, 'Cash Analysis Trade Nominal', description)
    zarNominal = css.get_zar_val(CALC_SPACE_MONEY, node, 'Cash Analysis Trade Nominal', fxRate, description)

    buySell = css.get_val(CALC_SPACE_MONEY, node, 'Cash Analysis Event BuySell', description)
    connectTrd = trade.ConnectedTrdnbr()
    contrctTrd = trade.ContractTrdnbr()
    if trade.FxSwapFarLeg():
        farTrd = trade.FxSwapFarLeg().StringKey()
    else:
        farTrd = trade.StringKey()

    if trade.Instrument().InsType() == 'Option':
        optionType = str(trade.Instrument().ExerciseType())
        optionValueDate = str(trade.ValueDay())
        insDec = acm.FInstrumentLogicDecorator(trade.Instrument(), None)
        optionDeliveryDate = str(insDec.DeliveryDate())
        optionSettleType = str(trade.Instrument().SettlementType())
        if trade.Instrument().IsPutOption():
            isCallorPut = 'Put'
        else:
            isCallorPut = 'Call'
    else:
        optionType = ''
        optionValueDate = ''
        optionDeliveryDate = ''
        optionSettleType = ''
        isCallorPut = ''

    csa = trade.Counterparty().AdditionalInfo().CSA()
    csa_collateral_curr = trade.Counterparty().AdditionalInfo().CSA_Collateral_Curr()
    csa_name = trade.Counterparty().AdditionalInfo().CSA_Name()
    csa_type = trade.Counterparty().AdditionalInfo().CSA_Type()

    csa = str(csa) if csa else ''
    csa_collateral_curr = str(csa_collateral_curr) if csa_collateral_curr else ''
    csa_name = str(csa_name) if csa_name else ''
    csa_type = str(csa_type) if csa_type else ''

    return '\t'.join([
        str(fromRepDate),
        str(toRepDate),
        trade.StringKey(),
        trade.Status(),
        trade.Counterparty().StringKey(),
        expDate,
        node.Type(),
        str(node.PayDate()),
        str(node.StartDate()),
        str(node.EndDate()),
        str(Amount),
        str(amountPV),
        str(buySell),
        trade.Currency().StringKey(),
        cfCurr,
        trade.Instrument().StringKey(),
        InstType[trade.Instrument().InsType().upper()],
        '',
        str(Nominal),
        str(cfNominal),
        trade.Portfolio().StringKey(),
        trade.Acquirer().StringKey(),
        trade.Counterparty().Type(),
        str(cfNumber),
        str(zarAmount),
        str(zarAmountPV),
        str(zarNominal),
        str(ZAR_CF_Nominal),
        str(connectTrd),
        str(contrctTrd),
        str(farTrd),
        str(trade.Counterparty().AdditionalInfo().BarCap_SMS_CP_SDSID()),
        str(trade.Counterparty().AdditionalInfo().BarCap_Eagle_SDSID()),
        str(trade.Counterparty().AdditionalInfo().BarCap_SMS_LE_SDSID()),
        str(trade.Instrument().MtmFromFeed()),
        optionType,
        optionValueDate,
        optionDeliveryDate,
        optionSettleType,
        isCallorPut,
        csa,
        csa_collateral_curr,
        csa_name,
        csa_type
    ])


def _trade_row(trade, css, node, fromRepDate, toRepDate, expDate, trdCurr, fxRate, cfNumber):
    description = "Trade: %i" % trade.Oid()
    if LOG_LEVEL > 1:
        _log("ROW %s" % description)

    if trade.Instrument().InsType().upper() not in InstType:
        raise Exception(
            "Unexpected instype '{0}', trade {1}".format(trade.Instrument().InsType().upper(), trade.Oid()))

    amountPV = css.get_safe_val(CALC_SPACE_START, trade, 'Total Val End', description)
    zarAmountPV = css.get_zar_val(CALC_SPACE_START, trade, 'Total Val End', fxRate, description)

    Amount = amountPV
    zarAmount = zarAmountPV

    payDate = fromRepDate
    endDate = expDate
    startDate = expDate

    nominal = css.get_val(CALC_SPACE_TRADE, trade, 'Trade Nominal', description)
    zarNominal = css.get_safe_val(CALC_SPACE_TRADE, trade, 'ZARNominal', description)

    cfNominal = 0
    zarCFNominal = 0
    connectTrd = trade.ConnectedTrdnbr()
    contrctTrd = trade.ContractTrdnbr()
    if trade.FxSwapFarLeg():
        farTrd = trade.FxSwapFarLeg().StringKey()
    else:
        farTrd = trade.StringKey()

    if trade.Instrument().InsType() == 'Option':
        optionType = str(trade.Instrument().ExerciseType())
        optionValueDate = str(trade.ValueDay())
        insDec = acm.FInstrumentLogicDecorator(trade.Instrument(), None)
        optionDeliveryDate = str(insDec.DeliveryDate())
        optionSettleType = str(trade.Instrument().SettlementType())
        if trade.Instrument().IsPutOption():
            isCallorPut = 'Put'
        else:
            isCallorPut = 'Call'
    else:
        optionType = ''
        optionValueDate = ''
        optionDeliveryDate = ''
        optionSettleType = ''
        isCallorPut = ''

    csa = trade.Counterparty().AdditionalInfo().CSA()
    csa_collateral_curr = trade.Counterparty().AdditionalInfo().CSA_Collateral_Curr()
    csa_name = trade.Counterparty().AdditionalInfo().CSA_Name()
    csa_type = trade.Counterparty().AdditionalInfo().CSA_Type()

    csa = str(csa) if csa else ''
    csa_collateral_curr = str(csa_collateral_curr) if csa_collateral_curr else ''
    csa_name = str(csa_name) if csa_name else ''
    csa_type = str(csa_type) if csa_type else ''

    buySell = css.get_val(CALC_SPACE_START, trade, 'Bought or Sold')
    return '\t'.join([
        str(fromRepDate),
        str(toRepDate),
        trade.StringKey(),
        trade.Status(),
        trade.Counterparty().StringKey(),
        expDate,
        'Val End',
        payDate,
        startDate,
        endDate,
        str(Amount),
        str(amountPV),
        str(buySell),
        trade.Currency().StringKey(),
        trdCurr,
        trade.Instrument().StringKey(),
        InstType[trade.Instrument().InsType().upper()],
        '',
        str(nominal),
        str(cfNominal),
        trade.Portfolio().StringKey(),
        trade.Acquirer().StringKey(),
        trade.Counterparty().Type(),
        '0',
        str(zarAmount),
        str(zarAmountPV),
        str(zarNominal),
        str(zarCFNominal),
        str(connectTrd),
        str(contrctTrd),
        str(farTrd),
        str(trade.Counterparty().AdditionalInfo().BarCap_SMS_CP_SDSID()),
        str(trade.Counterparty().AdditionalInfo().BarCap_Eagle_SDSID()),
        str(trade.Counterparty().AdditionalInfo().BarCap_SMS_LE_SDSID()),
        str(trade.Instrument().MtmFromFeed()),
        optionType,
        optionValueDate,
        optionDeliveryDate,
        optionSettleType,
        isCallorPut,
        csa,
        csa_collateral_curr,
        csa_name,
        csa_type
    ])


def _do_money_flow_row(css, trade, fromRepDate, toRepDate, rows, fout):
    dt = str(fromRepDate)

    expDateTemp = trade.Instrument().ExpiryDate()
    if expDateTemp == '':
        expDate = ''
    else:
        expDate = acm_date(to_datetime(expDateTemp))

    trdCurr = trade.Currency().StringKey()
    tf_rate = _fx_rate(trdCurr, 'ZAR', dt)

    rows += 1
    line = _trade_row(trade, css, trade, fromRepDate, toRepDate, expDate, trdCurr, tf_rate, 0)
    fout.write("{0}\n".format(line))

    css.add_trade(CALC_SPACE_MONEY, trade)
    node = css.first_child(CALC_SPACE_MONEY).FirstChild()
    while node:
        c = node.Tree().Item().MoneyFlow()

        cfCurr = c.Currency().StringKey()

        pay_date = c.PayDate()
        fxRate = _fx_rate(cfCurr, 'ZAR', dt)

        if c.Class().StringKey() == 'FPaymentMoneyFlow':
            cfNumber = c.Payment().Oid()
        elif c.Class().StringKey() == 'FCashFlowMoneyFlow':
            cfNumber = c.CashFlow().Oid()
        else:
            cfNumber = 0

        if pay_date > fromRepDate:
            rows += 1
            try:
                line = _cashflow_row(trade, css, c, fromRepDate, toRepDate, expDate, cfCurr,
                                     fxRate, cfNumber)
                fout.write("{0}\n".format(line))
            except Exception as e:
                print_exc()
                print("Exception calculating money flow row for trade %i: %s" % (trade.Oid(), str(e)))

        node = node.NextSibling()

    return rows


def _iterate_money_flows(css, fromRepDate, toRepDate, fout):
    print("Iterating MoneyFlow rows ...")

    rows = 0
    next_row_report = 1000
    start = datetime.datetime.now()

    node = css.first_child(CALC_SPACE_TRADE).FirstChild()
    while node:
        try:
            trade = acm.FTrade[node.Tree().Item().StringKey()]

            rows = _do_money_flow_row(css, trade, fromRepDate, toRepDate, rows, fout)
            if rows > next_row_report:
                _log("%i rows..." % rows)
                next_row_report = rows + 1000

        except Exception as e:
            print_exc()
            print("Exception calculating trade %i: %s" % (trade.Oid(), str(e)))

        node = node.NextSibling()
        if MAX_RUNTIME and (datetime.datetime.now() - start).seconds > MAX_RUNTIME * 60:
            _log("MAX_RUNTIME exceeded!")
            node = None

    _log("TOTAL ROWS: %i" % rows)


def _iterate_trades(css, fromRepDate, toRepDate, fout):
    print("Iterating Trade rows ...")

    node = css.first_child(CALC_SPACE_TRADE).FirstChild()
    while node:
        trade = acm.FTrade[node.Tree().Item().StringKey()]

        expDateTemp = trade.Instrument().ExpiryDate()

        if expDateTemp == '':
            expDate = ''
        else:
            expDate = acm_date(to_datetime(expDateTemp))

        trdCurr = trade.Currency().StringKey()
        dt = str(fromRepDate)
        fxRate = _fx_rate(trdCurr, 'ZAR', dt)
        cfNumber = 0
        try:
            line = _trade_row(trade, css, trade, fromRepDate, toRepDate, expDate, trdCurr,
                              fxRate, cfNumber)
            fout.write("{0}\n".format(line))

        except Exception as e:
            print_exc()
            print("Exception calculating trade %: %s" % (trade.Oid(), str(e)))

        node = node.NextSibling()


'''-----------------------------------------------------------------------------------------------------------'''
ael_variables = \
    [
        ['tradeFilter', 'TradeFilter', 'string', _trdfilterList()],
        ['path', 'Path', 'string', None, '/services/frontnt/Task/', 0],
        ['fileName', 'File Name', 'string', None, 'Output.txt', 0],
        ['endDate', 'End Date', 'string', EndDateList.keys(), 'Now', 0, 0, '', None, 1],
        ['endDateCustom', 'End Date Custom', 'string', None, TODAY.to_string(ael.DATE_ISO), 0, 0, '', None, 1],
    ]
'''-----------------------------------------------------------------------------------------------------------'''


def ael_main(ael_dict):
    tf = acm.FTradeSelection[ael_dict['tradeFilter']]
    if not tf:
        print("Error, Could not find the specified trade filter '{0}'".format(ael_dict['tradeFilter']))
        return

    filePath = ael_dict['path'] + ael_dict['fileName']

    _fx_rate._ccy_cache = {}

    heading = ['fromRepDate', 'toRepDate', 'Trdnbr', 'TrdStatus', 'Counterparty', 'InsExpiry', 'CFType',
               'PayDate', 'StartDate', 'EndDate', 'Amount', 'Amount_PV', 'BS', 'TrdCurrency', 'CF_Currency',
               'InstrumentName', 'Instype', 'Product_Code', 'Nominal', 'CF_Nominal', 'Portfolio', 'Acquirer',
               'CptyType', 'Cfwnbr', 'ZAR_Amount', 'ZAR_Amount_PV', 'ZAR_Nominal', 'ZAR_CFNominal', 'Connected_Trd',
               'Contract_Trd', 'FarlegTrade', 'SMS_CP_SDSID', 'Eagle_SDSID', 'SMS_LE_SDSID', 'MTM_From_Feed',
               'Option_Type', 'Option_Value_Date', 'Option_Delivery_Date', 'Option_Settle_Type', 'IsCallorPut',
               'CSA', 'CSA Collateral Curr', 'CSA Name', 'CSA Type']

    heading = '\t'.join(heading)

    if ael_dict['endDate'] == 'Custom Date':
        fromRepDate = ael_dict['endDateCustom']
    else:
        fromRepDate = str(EndDateList[ael_dict['endDate']])

    tempDate = ael.date(fromRepDate)
    tempDate = tempDate.add_years(50)
    toRepDate = tempDate.to_string(ael.DATE_ISO)

    css = CalcSpaceSet()
    csc = acm.FCalculationSpaceCollection()
    money_space = csc.GetSpace("FMoneyFlowSheet", "Standard")
    money_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    money_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', toRepDate)
    css.add_space(CALC_SPACE_MONEY, money_space)

    trade_space = csc.GetSpace("FTradeSheet", "Standard")
    trade_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    trade_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', toRepDate)
    css.add_space(CALC_SPACE_TRADE, trade_space)

    start_space = csc.GetSpace("FTradeSheet", "Standard")
    start_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    start_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', fromRepDate)
    css.add_space(CALC_SPACE_START, start_space)

    start = datetime.datetime.now()
    print("Started: %s" % start.strftime("%Y-%m-%d %H:%M:%S"))
    with open(filePath, 'w') as fout:
        fout.writelines(heading + "\n")
        trd = tf.Trades()[0]
        if trd.Instrument().IsCashFlowInstrument() or trd.Instrument().InsType() == 'Combination':
            css.add_filter(CALC_SPACE_MONEY, tf)
            css.add_filter(CALC_SPACE_TRADE, tf)
            css.add_filter(CALC_SPACE_START, tf)
            _iterate_money_flows(css, fromRepDate, toRepDate, fout)
        else:
            css.add_filter(CALC_SPACE_TRADE, tf)
            _iterate_trades(css, fromRepDate, toRepDate, fout)

    css.close_all()
    end = datetime.datetime.now()

    print("End: %s" % end.strftime("%Y-%m-%d %H:%M:%S"))
    print("Duration: %.1f minutes" % ((end - start).seconds / 60.0))

    print('Wrote secondary output to: ', filePath)
    print('completed successfully')
