import ael
log = 1
log2 = 1
def calc_margin(p, date, perc, first):
    trds = p.trades()
    valstart = 0
    valend = 0
    listend = []
    liststart = []
    for t in trds:
        if t.status not in ['Void', 'Simulate']:
            if ael.date_from_time(t.time) <= date:
                val = ()
                if log: print 'E', t.quantity, t.insaddr.mtm_price(date)/100, t.insaddr.insid, date, (abs(t.quantity) * t.insaddr.mtm_price(date)/100)
                val = t.insaddr.insid, t.quantity, t.insaddr.mtm_price(date)/100
                listend.append(val)
                valend = valend + (abs(t.quantity) * t.insaddr.mtm_price(date)/100)
            if ael.date_from_time(t.time) < date:     
                val = t.insaddr.insid, t.quantity, t.insaddr.mtm_price(date.add_days(-1))/100
                if log: print 'S', t.quantity, t.insaddr.mtm_price(date.add_days(-1))/100, t.insaddr.insid, date.add_days(-1), (abs(t.quantity) * t.insaddr.mtm_price(date.add_days(-1))/100)
                valstart = valstart + (abs(t.quantity) * t.insaddr.mtm_price(date.add_days(-1))/100)
    if log2: print listend
    if log2: print 'VE ', valend, 'VS ', valstart, (valend - valstart) * perc, perc
    if first:
        return valend * perc
    else:       
        return (valend - valstart) * perc
print calc_margin(ael.Portfolio['47274_CFD'], ael.date('2007-06-08'), 0.15, 0)

