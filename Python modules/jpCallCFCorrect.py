import ael

def update_leg(ins, dat):
    flag = 0
    print ins.insid
    if ins.insid.find('CFD'):
        flag = 1
    for l in ins.legs():
        lc = l.clone()
        lc.type = 'Call Float'
        lc.curr = ael.Instrument['ZAR']
        lc.nominal_factor = 1        
        lc.float_rate = ael.Instrument['ZAR-ABSA-TOP20-CALL']
        lc.spread = 0.15
        lc.start_day = dat
        lc.end_day = dat.add_banking_day(ael.Instrument['ZAR'], 1)        
        lc.rolling_period = '1d'        
        lc.rolling_base_day = dat
        lc.pay_day_method = 'Following'
        lc.pay_calnbr = ael.Calendar['ZAR Johannesburg']
        lc.reset_type = 'Weighted'
        lc.reset_period = '1d'
        lc.reset_day_method = 'Following'
        lc.reset_calnbr = ael.Calendar['ZAR Johannesburg']
        #lc.nominal_at_end = 
        lc.float_rate_factor = 1
        lc.strike_type = 'Absolute'
        for c in lc.cash_flows():
        
            if c.type != 'Fixed Amount':
                c.delete()
                
        lc.reinvest = 1
        lc.regenerate()
        lc.commit()
    
    return 'Success'
    
trades = ael.TradeFilter['jpCall_All_Trades EQ'].trades()

for t in trades:

    ins = t.insaddr
    update_leg(ins, ael.date('2008-09-26'))

