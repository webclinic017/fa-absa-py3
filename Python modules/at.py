"""Arena Tools - stuff that makes Front Arena users' lives easier."""
# //depot/AbsaCapital/SMIT/Front Arena/Python Scripts/at/

import sys, datetime

import acm, ael                                     #@UnresolvedImport

import at_functools as functools                    #@UnusedImport
import at_calculation_space as calculation_space    #@UnusedImport
import at_addInfo as addInfo                        #@UnusedImport
import at_addInfoSpec as addInfoSpec                #@UnusedImport
import at_addInfoSpecEnum as addInfoSpecEnum        #@UnusedImport
import at_choice as choice                          #@UnusedImport
import at_choiceList as choiceList                  #@UnusedImport
import at_choiceListEnum as choiceListEnum          #@UnusedImport
import at_dataTypes as dataTypes                    #@UnusedImport
import at_dbsql as dbsql                            #@UnusedImport
import at_ael_variables as ael_variables            #@UnusedImport
import at_progress as progress                      #@UnusedImport

import logging

DATE_YMD_FORMAT = '%Y-%m-%d'
DATE_YMDHMS_FORMAT = '%Y-%m-%d %H:%M:%S'

# Trade processes
TP_NONE =               0       # 0
TP_FX_SPLIT_CHILD =     1 << 0  # 1
TP_FX_SPLIT_PARENT =    1 << 1  # 2
TP_MM_SPLIT_CHILD =     1 << 2  # 4
TP_MM_SPLIT_PARENT =    1 << 3  # 8
TP_SPOT_COVER_CHILD =   1 << 4  # 16
TP_SPOT_COVER_PARENT =  1 << 5  # 32
TP_SALES_COVER_CHILD =  1 << 6  # 64
TP_SALES_COVER_PARENT = 1 << 7  # 128
TP_PROLONG_CHILD =      1 << 8  # 256
TP_PROLONG_PARENT =     1 << 9  # 512

TP_PREMIUM_PARENT =     1 << 11 # 2048
TP_FX_SPOT =            1 << 12 # 4096
TP_FX_FORWARD =         1 << 13 # 8192
TP_SWAP_NEAR_LEG =      1 << 14 # 16384
TP_SWAP_FAR_LEG =       1 << 15 # 32768
TP_REVERSAL =           1 << 16 # 65536
TP_SPOT_COVER_INS_CCY = 1 << 17 # 131072
TP_HISTORIC_PRICING =   1 << 18 # 262144
TP_SCM_BACK2BACK =      1 << 19 # 524288
TP_GROUP_PARENT =       1 << 20 # 1048576
TP_PREMIUM_CHILD =      1 << 21 # 2097152
TP_INSIDE_CLS =         1 << 22 # 4194304

TP_OUTSIDE_CLS =        1 << 27 # 134217728
TP_DRAWDOWN_OFFSET =    1 << 28 # 268435456
TP_DRAWDOWN_CHILD =     1 << 29 # 536870912

# Trade statuses
TS__ENUM = 'TradeStatus'
TS_BO_CONFIRMED = 'BO Confirmed'
TS_BOBO_CONFIRMED ='BO-BO Confirmed'
TS_CONFIRMED_VOID = 'Confirmed Void'
TS_EXCHANGE = 'Exchange'
TS_FO_CONFIRMED = 'FO Confirmed'
TS_INTERNAL = 'Internal'
TS_LEGALLY_CONFIRMED = 'Legally Confirmed'
TS_RESERVED = 'Reserved'
TS_SIMULATED = 'Simulated'
TS_TERMINATED = 'Terminated'
TS_VOID = 'Void'

# Instrument types
INST__ENUM = 'InsType'
INST_BASKET_REPO_REVERSE = 'BasketRepo/Reverse'
INST_BASKET_SECLOAN = 'BasketSecurityLoan'
INST_BILL = 'Bill'
INST_BOND ='Bond'
INST_BONDINDEX = 'BondIndex'
INST_BUYSELLBACK = 'BuySellback'
INST_CALLACCOUNT = 'CallAccount'
INST_CAP = 'Cap'
INST_CASH_COLLATERAL = 'CashCollateral'
INST_CD = 'CD'
INST_CFD = 'CFD'
INST_CLN = 'CLN'
INST_COLLAR = 'Collar'
INST_COLLATERAL = 'Collateral'
INST_COMBINATION = 'Combination'
INST_COMMODITY = 'Commodity'
INST_COMMODITY_INDEX = 'Commodity Index'
INST_COMMODITY_VARIANT = 'Commodity Variant'
INST_CONVERTIBLE = 'Convertible'
INST_CREDITDEFAULT_SWAP = 'CreditDefaultSwap'
INST_CREDITINDEX = 'CreditIndex'
INST_CURR = 'Curr'
INST_CURR_SWAP = 'CurrSwap'
INST_DEPOSIT = 'Deposit'
INST_DEPOSITARY_RECEIPT = 'Depositary Receipt'
INST_DEALCURR_BOND = 'DualCurrBond'
INST_EQUITY_INDEX = 'EquityIndex'
INST_EQUITY_SWAP = 'EquitySwap'
INST_ETF = 'ETF'
INST_FLOOR = 'Floor'
INST_FRA = 'FRA'
INST_FREEDEFCF = 'FreeDefCF'
INST_FRN = 'FRN'
INST_FUND = 'Fund'
INST_FUTURE_FORWARD = 'Future/Forward'
INST_FXRATE = 'Fx Rate'
INST_FXOPTION_DATEDFWD = 'FXOptionDatedFwd'
INST_FXSWAP = 'FxSwap'
INST_INDEXLINKED_BOND = 'IndexLinkedBond'
INST_INDEXLINKED_SWAP = 'IndexLinkedSwap'
INST_LEPO = 'LEPO'
INST_MBS_ABS = 'MBS/ABS'
INST_MULTIASSET = 'MultiAsset'
INST_MULTIOPTION = 'MultiOption'
INST_NONE = 'None'
INST_OPTION = 'Option'
INST_PORTFOLIO_SWAP = 'Portfolio Swap'
INST_PRICE_INDEX = 'PriceIndex'
INST_PRICE_SWAP = 'PriceSwap'
INST_PROMIS_LOAN = 'PromisLoan'
INST_RATE_INDEX = 'RateIndex'
INST_REPO_REVERSE = 'Repo/Reverse'
INST_SECURITY_LOAN = 'SecurityLoan'
INST_STOCK = 'Stock'
INST_STOCKRIGHT = 'StockRight'
INST_SWAP = 'Swap'
INST_TOTALRETURN_SWAP = 'TotalReturnSwap'
INST_UNKNOWN = 'UnKnown'
INST_VARIANCE_SWAP = 'VarianceSwap'
INST_WARRANT = 'Warrant'
INST_ZERO = 'Zero'

def date_to_datetime(date):
    """Convert date to Python datetime object.

    :param date: Date to be converted.
    :type date: ``ael_date``, ``datetime``, ``FDateTime``, ``string`` or timestamp
    :returns: ``datetime.datetime``

    """
    # datetime
    if isinstance(date, datetime.datetime):
        return date

    # timestamp
    if isinstance(date, (int, int, float)):
        return datetime.datetime.fromtimestamp(date)

    # ael_date
    if isinstance(date, ael.ael_date):
        return datetime.datetime.fromtimestamp(date.to_time())

    # FDateTime -- all efforts to make this nicer failed.
    if type(date).__name__ == 'FDateTime':
        # '2012-09-26 02:00:00' => '2012-09-26'
        return datetime.datetime.strptime(date.Value(), DATE_YMDHMS_FORMAT)

    # string
    if isinstance(date, str):
        # Supports both local date and Ymd
        formats = [DATE_YMD_FORMAT, DATE_YMDHMS_FORMAT, '%x', '%c']
        for frmt in formats:
            try:
                return datetime.datetime.strptime(date, frmt)
            except ValueError:
                pass

        raise ValueError('Invalid format.')

    raise TypeError('Unexpected date type: ' + str(date))

def date_to_ymd_string(date):
    """Convert date to Y-m-d format.

    :param date: Date to be converted.
    :type date: ``ael_date``, ``datetime``, ``FDateTime``, ``string`` or timestamp
    :returns: ``string`` in Y-m-d format.

    """

    return date_to_datetime(date).strftime(DATE_YMD_FORMAT)

DAYCOUNT_ACT_365 = 2
"""Actual/365 daycount method."""

def days_between(date1, date2, daycount_method):
    """Return number of days between two dates using specified daycount method."""
    date1 = date_to_datetime(date1).date()
    date2 = date_to_datetime(date2).date()
    if daycount_method == DAYCOUNT_ACT_365:
        return (date2 - date1).days

    raise ValueError('Unsupported daycount method.')


def enable_console_logging(level = logging.INFO):
    """Enable logging to console."""
    sh = logging.StreamHandler()
    sh.setLevel(level)

    logger = logging.getLogger()
    logger.addHandler(sh)
    logger.setLevel(level)

def to_acm(obj, cls):
    """Convert an acm/ael object or id to its ACM representation."""
    if not cls.IsKindOf(acm.FClass):
        raise ValueError('Expected acm class in cls parameter.')

    if obj == None:
        return None

    # Int or String
    if isinstance(obj, int) or isinstance(obj, str):
        return cls[obj]

    # ACM
    if hasattr(obj, 'Class') and obj.IsKindOf(cls):
        return obj

    # AEL
    if type(obj).__name__ == 'ael_entity':
        acmobj = acm.Ael.AelToFObject(obj)
        if acmobj and acmobj.IsKindOf(cls):
            return acmobj

    raise ValueError('Invalid object type.')

def eval_ext_attr(attr_name, fobject=None):
    """Returns the value of the extension attribute for the given object."""
    context = acm.GetDefaultContext()
    evaluator = acm.GetCalculatedValue(fobject, context, attr_name)
    if evaluator:
        return evaluator.Value()
    else:
        raise AttributeError("Could not load extension attribute {0}.".format(attr_name))

