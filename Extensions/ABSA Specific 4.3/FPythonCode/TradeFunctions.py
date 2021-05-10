"""-----------------------------------------------------------------------------
PURPOSE                 :  Extension of standard FTrade methods
                            Added: TradeMonth
DEPATMENT AND DESK      :  Fixed Income
REQUESTER               :  Lerato Kekana
DEVELOPER               :  Rohan vd Walt
CR NUMBER               :  634562

HISTORY
=============================================================================
Date       Change no Developer              Description
-----------------------------------------------------------------------------
UNKNOWN    UNKNOWN   UNKNOWN                tradeProductFunction
2011-04-07           Rohan vd Walt          Added TradeMonth method to allow grouping in Trading Manager by TradeMonth
2014-07-02           Andrei Conicov         Have added the getExecutionDate function
2014-09-01           Andrei Conicov         Have added the getEconomicAmendments and getEconomicAmendmentsLoginTime
2014-10-21           Andrei Conicov         Have changed the imported module 
2015-02-18           Pavel Saparov          Added `getTradeDecorator` function which is used in ADFL
2017-11-09           Libor Svoboda          Added total_quantity_so_far for totalQuantitySoFar FCustomFunction.
                                            Removed tradeProductFunction.
-----------------------------------------------------------------------------"""
import acm, ael
import at_time
from ATSEconTradeAmend import get_economic_amendments, get_economic_amendments_login_time


def TradeMonth(self):
    nst = acm.Time()
    YMD = nst.DateToYMD(self.TradeTime())
    return str(YMD[0]) + '-' + str(YMD[1]).zfill(2)

def getExecutionDate(trade):
    """Returns the trade execution date without the time"""
    return at_time.datetime_from_string(trade.ExecutionTime()).strftime('%Y-%m-%d')

def getEconomicAmendments(trade):
    """Return the economic amendments"""
    return get_economic_amendments(trade.Oid())

def getEconomicAmendmentsLoginTime(trade):
    return get_economic_amendments_login_time(trade.Oid())     

def get_is_settled(self):
    """ Returns 'settled' if the instrument/trade is settled
        Repo/Reverse || SecurityLoan  - start date
        Bond || FRN - value date
    """
    is_settled = False
    if self.Instrument().InsType() in ['Repo/Reverse', 'SecurityLoan']:
        is_settled = self.Instrument().StartDate() < acm.Time.DateToday()
    elif self.Instrument().InsType() in ['Bond', 'FRN']:
        is_settled = self.ValueDay() < acm.Time.DateToday()
    if is_settled:
        return 'settled'
    else:
        return 'not settled'

def getTradeDecorator(trade):
    return acm.FTradeLogicDecorator(trade, None)


def total_quantity_so_far(trade, trades):
    trades = list(trades)
    trades.sort(key=lambda tr: (tr.TradeTime(), tr.Oid()))
    index = trades.index(trade)
    total = sum([tr.Quantity() for tr in trades[:index+1]])
    return total
