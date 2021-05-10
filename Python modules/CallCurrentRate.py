import ael

def call_current_rate(temp,trd,*rest):
    t = ael.Trade[(int)(trd)]
    cf_end = ael.date('1970-01-01')
    cfnbr = 0
    reset_end = ael.date('1970-01-01')
    resetnbr = 0
    
    for c in t.insaddr.legs()[0].cash_flows():
        if c.end_day > cf_end:
            cf_end = c.end_day
            cfnbr = c.cfwnbr
            
    for cf in t.insaddr.legs()[0].cash_flows():
        if cf.cfwnbr == cfnbr:
            for r in cf.resets():
                if r.end_day > reset_end:
                    reset_end = r.end_day
                    resetnbr = r.resnbr
            
            for r in cf.resets():
                if r.resnbr == resetnbr:
                    return (str)(r.value)
