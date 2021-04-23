import ael
ins = ael.Instrument.select('instype = "%s"' %('Option'))
for i in ins:
    if i.und_instype == 'Curr' and i.exp_day == ael.date_today():
        print(i.insid, i.exp_day)
        for p in i.historical_prices():
            if p.day == i.exp_day:
                pc = p.clone()
                pc.settle = 0.0
                pc.commit()
                
