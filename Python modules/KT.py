import ael

ccys = [['USD', 'ZAR', 100], ['XAU', 'USD', 1]]
t1 = ael.date_today().add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)
t0 = t1.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)

for ccy in ccys:
    i = ael.Instrument[ccy[0]]
    p = ael.Price.select('insaddr = %s' % i.insaddr)
    for px in p:
        if px.day == t0 and px.ptynbr.ptyid == 'SPOT' and px.curr == ael.Instrument[ccy[1]]:
            t0p = px.settle
        elif px.day == t1 and px.ptynbr.ptyid == 'SPOT' and px.curr == ael.Instrument[ccy[1]]:
            t1p = px.settle
    if t1 == ael.date_today():
        t1p = i.used_price(ael.date_today(), ccy[1], 'SPOT')
    print t1.to_string('%d-%b'), i.insid, t0p, t1p, t1p - t0p, (t1p - t0p) * ccy[2]
