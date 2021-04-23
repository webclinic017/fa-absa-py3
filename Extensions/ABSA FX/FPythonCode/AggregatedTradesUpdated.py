
import ael

def getAggregateTradesUpdated(aggTrade, startDate, endDate):
    startDate = ael.date(startDate)
    endDate = ael.date(endDate)
    query = r'''
    SELECT trdnbr
    from trade
    WHERE aggregate_trdnbr in (%i) and updat_time >= '%s' and updat_time <= '%s'
    ''' %(aggTrade.Oid(), startDate.to_string('%d %B %Y'), endDate.add_delta(1, 0, 0).to_string('%d %B %Y'))
    result = ael.dbsql(query)
    return result[0]

def countAggregatedTradesUpdated(aggTrade, startDate, endDate):
    return len(getAggregateTradesUpdated(aggTrade, startDate, endDate))
