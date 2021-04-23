import ael, acm
import time
import datetime

allTrades = []


def convert_to_datetime(date, format):
    """
        Converts a string to a datetime object
    """
    if str(type(date)) == "<type 'str'>":
        if format:
            slist = date.split('/')
            return datetime.date(int(slist[2]), int(slist[1]), int(slist[0]))   
        else:
            slist = date.split('-')
            return datetime.date(int(slist[0]), int(slist[1]), int(slist[2]))          
    return date

today = convert_to_datetime(str(ael.date_today()), '%d/%m/%Y')
print today

def IsTradeExpired(trade):
    i = trade.Instrument()
    
    if(i.InsType() == 'Option'):
        return i.IsExpired()
    
    if(i.InsType() == 'Fra'):
        return False  
    
    if not i.IsExpired():
        return today > convert_to_datetime(trade.ValueDay(), None)
    return i.IsExpired()
    
def countTrades(trades):
    num = 0
    for trd in trades:
        if not IsTradeExpired(trd):
            num = num + 1
            allTrades.append(trd.Oid())
    return num

portfolios = ['VOE', 'FUT', 'BVOE', 'FUT_Swaps', 'G7OE', 'Prop_Main', 'ABVOE4F'] 

for p in portfolios:
    port = acm.FPhysicalPortfolio[p];
    print 'starting ' + p 
    if port:
        count = countTrades(port.Trades() )
        print allTrades
        allTrades = []
        print str(count) + ' trades in ' + p
print 'done'


