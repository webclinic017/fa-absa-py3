import ael, FSQL_functions

def test(temp,seqnbr,*rest):
    s = ael.Settlement[seqnbr]
    t = s.trdnbr
    i = t.insaddr
    cf = s.cfwnbr
    date = FSQL_functions.LastBusinessDay(temp, ael.date_today().add_days(-2))
    if s.type in ('Call Fixed Rate Adjustable', 'Fixed Rate Adjustable') and s.status == 'Exception' and s.value_day == ael.date_today():
        if cf.type in ('Call Fixed Rate Adjustable', 'Fixed Rate Adjustable'):
            if date > cf.start_day and date <= cf.end_day:
                set = s.clone()
                set.status = 'Authorised'
                set.commit()
                return 1
    return 0
