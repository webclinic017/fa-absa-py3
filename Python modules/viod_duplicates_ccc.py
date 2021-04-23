import acm
from collections import defaultdict
from at_time import to_datetime

duplicates = defaultdict(list)

portfolio = acm.FPhysicalPortfolio["ACS RTM - 41012"]
value_date = '2019-03-20'

query = acm.CreateFASQLQuery('FTrade', 'AND')
query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))
query.AddAttrNode('ValueDay', 'EQUAL', value_date)
trades = query.Select()


for trade in trades:
    duplicates[trade.AdditionalInfo().XtpJseRef()].append(trade)
    
count = 0
try:
    acm.BeginTransaction()
    for key in duplicates:
        if len(duplicates[key]) == 2:
            my_trades = sorted(duplicates[key], key = lambda t: t.CreateTime())
            print(to_datetime(my_trades[0].CreateTime()), to_datetime(my_trades[1].CreateTime()))
            trade = my_trades[1]
            trade.Status('Void')
            trade.Commit()
            count += 1
    print("{0} Stocks voided".format(count))
    acm.CommitTransaction()
except Exception as ex:
    acm.AbortTransaction()

portfolio = acm.FPhysicalPortfolio["41012_CFD_ZERO"]
value_date = '2019-03-15'

query = acm.CreateFASQLQuery('FTrade', 'AND')
query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))
query.AddAttrNode('ValueDay', 'EQUAL', value_date)
trades = query.Select()

count = 0
try:
    acm.BeginTransaction()
    for trade in trades:
        trade.Status('Void')
        trade.Commit()
        count += 1
    print("{0} CFDs voided".format(count))
    acm.CommitTransaction()
except Exception as ex:
    acm.AbortTransaction()


