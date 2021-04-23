import ael
today = ael.date_today()
swapend = ['1Y', '2Y', '3Y', '4Y', '5Y', '10Y', '20Y', '25Y']
optend = ['3M', '6M', '1Y', '2Y']
ins = ael.Instrument['ZAR/IRS/GEN/1D/OPT']
opt = ael.Instrument['ZAR/IRS/REC/0D/1Y/OPT']
ic = ins.clone()


for k in swapend:
    newsins = ael.Instrument.new('Swap')
    startdate = today
    enddate = k
    print startdate, ': ', enddate
    for l in newsins.legs():
        l.start_day = startdate
        l.end_period = k
        if l.type == 'Float':
            l.float_rate = ael.Instrument['ZAR-JIBAR-3M-OPT']
        l.regenerate()
    newsins.insid = 'ZAR/IRS/GEN/' + enddate + '/OPT'
    ninsid = newsins.insid
    newsins.generic = 1
    newsins.product_chlnbr = ins.product_chlnbr
    newsins.quote_type = ins.quote_type
    try:
        newsins.commit()
    except:
        print 'Not created'
    print ninsid


#Receiver
    for i in optend:
        newoptins = ael.Instrument.new('Option')
        newoptinspay = ael.Instrument.new('Option')
        und = ael.Instrument[ninsid]
        newoptins.und_insaddr = und
        newoptins.und_instype = 'Swap'
        newoptins.exp_period = i 
        ed = i + '/' + k
        newoptins.insid = 'ZAR/IRS/REC/' + ed + '/OPT'
        print newoptins.insid
        newoptins.generic = 1
        newoptins.product_chlnbr = opt.product_chlnbr
        newoptins.notice_period = opt.notice_period
        newoptins.strike_type = opt.strike_type
        newoptins.settlement = opt.settlement
        newoptins.contr_size = opt.contr_size
        newoptins.quote_type = 'Pct of Nominal'
        newoptins.spot_banking_days_offset = opt.spot_banking_days_offset
        newoptins.price_finding_chlnbr = opt.price_finding_chlnbr 
        newoptins.pay_day_offset = opt.pay_day_offset
        newoptins.call_option = 0
        try:
            newoptins.commit()
        except:
            print 'Not created'
#Payer
        newoptinspay.und_insaddr = und
        newoptinspay.und_instype = 'Swap'
        newoptinspay.exp_period = i
        ed = i + '/' + k
        newoptinspay.insid = 'ZAR/IRS/PAY/' + ed + '/OPT'
        print newoptinspay.insid
        newoptinspay.generic = 1
        newoptinspay.product_chlnbr = opt.product_chlnbr
        newoptinspay.notice_period = opt.notice_period
        newoptinspay.strike_type = opt.strike_type
        newoptinspay.settlement = opt.settlement
        newoptinspay.contr_size = opt.contr_size
        newoptinspay.quote_type = 'Pct of Nominal'
        newoptinspay.spot_banking_days_offset = opt.spot_banking_days_offset
        newoptinspay.price_finding_chlnbr = opt.price_finding_chlnbr 
        newoptinspay.pay_day_offset = opt.pay_day_offset
        newoptinspay.call_option = 1
        try:
            newoptinspay.commit()
        except:
            print 'Not created'
