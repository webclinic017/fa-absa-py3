"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Reverses the aggregation performed on trades
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  371587
-----------------------------------------------------------------------------"""

import acm
import sl_aggregation

tradeFilterKey = 'TradeFilter'

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [tradeFilterKey, 'Trade Filter', 'FTradeSelection', None, None, 1, 1, 'The Trade Filter that returns trades to be considered for archiving.', None, 1]
]

def ael_main(parameters):
    tradeFilter = parameters[tradeFilterKey][0]
    trades = tradeFilter.Trades()
    print('De-Aggregating trades from trade filter [%s]' % tradeFilter.Name())
    print('%i trades selected for de-aggregation' % len(trades))
    sl_aggregation.DeAggregator.Run(trades)
