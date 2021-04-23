import ael

def ReturnRate(temp, i, *rest):
    trades = i.trades()
    list = []
    for t in trades:
        if t.status not in ('Void', 'Terminated', 'Simulated'):
            tup = (t.time, t.trdnbr, t.price)
            list.append(tup)
 
    list.sort()
    return list[0][2]


def ReturnRate_LastTrade(temp, i, *rest):
    trades = i.trades()
    list = []
    for t in trades:
        if t.status in ('BO Confirmed', 'FO Confirmed', 'BO-BO Confirmed') and t.quantity > 0:
            tup = (ael.date_from_time(t.time), t.trdnbr, t.price)
            list.append(tup)

    list.sort()
    list.reverse()
    return list[0][2]
