import ael
def bobocfds(p,date,*rest):
    dat = ael.date(date)
    prfs = p
    a = ael.enum_from_string('TradeStatus', 'BO-BO Confirmed')
    b = ael.enum_from_string('TradeStatus', 'Simulated')
    c = ael.enum_from_string('TradeStatus', 'Void')
    d = ael.enum_from_string('TradeStatus', 'Terminated')
    dat = dat.add_days(-1)
    dt = dat.to_string(ael.DATE_ISO)
    print a, b, c, d, dt
    q = '''select
                trdnbr
           from
                trade
           where
                prfnbr = %s 
            and status not in (%d,%d,%d,%d)
            and time >= "%s"''' % (prfs.prfnbr, a, b, c, d, dt)
    val = ael.dbsql(q)
    print val
    for t in ael.dbsql(q)[0]:
        trd = ael.Trade[t[0]]
        tc = trd.clone()
        tc.status = 'BO-BO Confirmed'
        print tc.trdnbr
        tc.commit() 
    return 'Success'
