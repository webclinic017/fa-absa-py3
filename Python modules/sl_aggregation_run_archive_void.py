"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Archives voided security loan trades
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  371587
-----------------------------------------------------------------------------"""

import acm
import sl_aggregation

archiveDateKey = 'ArchiveDate'
tradeFilterKey = 'TradeFilter'

nsTime = acm.Time()
endOfLastMonth = nsTime.DateAddDelta(nsTime.FirstDayOfMonth(nsTime.DateNow()), 0, 0, -1)

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [archiveDateKey, 'Archive Date', 'date', None, endOfLastMonth, 1, 0, 'Trades expiring on or before this date will be archived.', None, 1],
    [tradeFilterKey, 'Trade Filter', 'FTradeSelection', None, None, 1, 1, 'The Trade Filter that returns trades to be considered for archiving.', None, 1],
]

def ael_main(parameters):
    archiveDate = parameters[archiveDateKey]
    tradeFilter = parameters[tradeFilterKey][0]
    trades = tradeFilter.Trades()
    print('Archiving trades from trade filter [%s] expiring on or before %s' % (tradeFilter.Name(), archiveDate.to_string()))
    print('%i trades selected for aggregation' % len(trades))
    sl_aggregation.VoidedTradeArchiver.Run(trades, sl_aggregation.ToAcmDate(archiveDate))
