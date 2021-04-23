import ael
today = ael.date_today()
capend = ['1Y', '2Y', '3Y', '4Y', '5Y', '6Y', '7Y', '10Y', '15Y', '20Y']
ins = ael.Instrument['ZAR/CAP/GEN/1D/OPT/RFWD+2']
ic = ins.clone()

for k in capend:
    newsins = ael.Instrument.new('Cap')
    startdate = today
    enddate = k
    print startdate, ': ', enddate
    for l in newsins.legs():
        l.start_day = startdate
        l.end_period = k
        l.float_rate = ael.Instrument['ZAR-JIBAR-3M-OPT']
        l.regenerate()
    newsins.insid = 'ZAR/CAP/GEN/' + enddate + '/OPT/RFWD+2'
    ninsid = newsins.insid
    newsins.generic = 1
    newsins.product_chlnbr = ins.product_chlnbr
    newsins.quote_type = ins.quote_type
    try:
        newsins.commit()
    except:
        print 'Not created'
    print ninsid
