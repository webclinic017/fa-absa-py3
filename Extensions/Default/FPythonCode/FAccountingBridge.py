""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/subledgermigration/FAccountingBridge.py"
import FAccounting
import acm
import ael

DENOMFUNC = acm.GetFunction('denominatedvalue', 4)
NANFUNC = acm.GetFunction('notANumber', 0)

def TradeFunction(fTrade, valuationDate, functionName):
    FAccounting.init()

    trade = ael.Trade[fTrade.Oid()]
    run_day = ael.date(valuationDate)

    return FAccountingFunctionWrapper(functionName, trade, run_day, None, None, None, None)

def LegFunction(legAndTrades, valuationDate, functionName):
    FAccounting.init()

    trades = legAndTrades.Trades()
    assert(trades.Size() == 1)
    trade = ael.Trade[trades.At(0).Oid()]
    legnbr = legAndTrades.Leg().Oid()
    run_day = ael.date(valuationDate)

    return FAccountingFunctionWrapper(functionName, trade, run_day, legnbr, None, None, None)

def MoneyFlowFunction(moneyFlow, valuationDate, functionName):
    FAccounting.init()

    trade = ael.Trade[moneyFlow.Trade().Oid()]

    cfwnbr = None
    divnbr = None
    pmtnbr = None
    sourceObject = moneyFlow.SourceObject()
    if sourceObject.IsKindOf(acm.FCashFlow):
        cfwnbr = sourceObject.Oid()
    elif sourceObject.IsKindOf(acm.FDividend):
        divnbr = sourceObject.Oid()
    elif sourceObject.IsKindOf(acm.FPayment):
        pmtnbr = sourceObject.Oid()

    run_day = ael.date(valuationDate)

    return FAccountingFunctionWrapper(functionName, trade, run_day, None, cfwnbr, divnbr, pmtnbr)

def FAccountingFunctionWrapper(functionName, trade, run_day, legnbr, cfwnbr, divnbr, pmtnbr):
    fAccountingFunction = getattr(FAccounting, functionName)
    valueCurrencyVector = fAccountingFunction(trade, run_day, cfwnbr, legnbr, None, 1, divnbr, pmtnbr)

    dVOrNumber = None
    valueTypeName = type(valueCurrencyVector).__name__
    if valueTypeName == 'list' and len(valueCurrencyVector) == 2:
        dVOrNumber = CreateDenominatedValue(valueCurrencyVector)
    elif valueTypeName == 'int' or valueTypeName == 'float':
        dVOrNumber = valueCurrencyVector
    else:
        dVOrNumber = DENOMFUNC(NANFUNC(), None, None, None)

    return dVOrNumber

def CreateDenominatedValue(valueCurrencyVector):
    dV = None

    assert(len(valueCurrencyVector) == 2)

    number = valueCurrencyVector[0]
    currencyID = valueCurrencyVector[1]
    dV = DENOMFUNC(number, currencyID, None, None)

    return dV
