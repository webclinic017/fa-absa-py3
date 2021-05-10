import ael

def ratechange(temp,insid,date,value,*rest):
    d = ael.date(date)  #start day
    ins = ael.Instrument[insid]
    for cf in ins.cash_flows():
        for reset in cf.resets():
            if reset.end_day == d:
                prev = reset.value
                if value != prev:
                    return (str)(prev)
                    break
    return 'No'
