
import acm
import FSettlementParameters as params

trade = acm.FTrade[33612374]
count = 1
queries = [params.tradeFilterQueries, params.preventSettlementCreationQueries]
unique = set()

msg = '{0}:\nThese will generate settlements when all conditions are: {1}'
for query in queries:
    if count == 1:
        print msg.format('tradeFilterQueries', True)
    else:
        print msg.format('preventSettlementCreationQueries', False)
    print '=='*40
    count +=1
    for q in query:
        result = acm.FStoredASQLQuery[q].Query().IsSatisfiedBy(trade)
        print 'Query Name: {0} >>> condition: {1}'.format(q, result)
        unique.add(result)
    print 'Final Result: {0}'.format(unique)
    unique = set()
print ''
