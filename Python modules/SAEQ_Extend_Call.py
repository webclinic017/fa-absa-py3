import ael
ins_list=['EQ_BARCAP_CFD_Fict_L', 'EQ_BARCAP_CFD_Fict_D']#, 'EQ_BARCAP_CFD_Funding_L','EQ_BARCAP_CFD_Funding_D']
for i in ins_list:
    ins = ael.Instrument[i]
    for l in ins.legs():
        maxdate = l.start_day
        for c in l.cash_flows():
            if c.pay_day > maxdate and c.type == 'Call Float Rate':
                maxdate = c.pay_day
    print maxdate
    while maxdate < ael.date_today():
        try:
            ins.extend_open_end()
            maxdate = maxdate.add_banking_day(ael.Instrument['ZAR'], 1)
            
        except:
            print 'Prob'
            
        ael.poll()

