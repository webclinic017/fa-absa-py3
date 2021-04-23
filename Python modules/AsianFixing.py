import SAEQ_Third_Thursday, ael


print 'Instrument id', 'Expiry Date', 'Close out', 'forward price'
ins = ael.Instrument.select('instype= "Future/Forward"')
for i in ins:
    if i.und_instype == "EquityIndex":
        j = 1
        while (i.exp_day >= ael.date(SAEQ_Third_Thursday.points("", ael.date_today(), j, j))):
            closeout = ael.date(SAEQ_Third_Thursday.points("", ael.date_today(), j, j))
            print i.insid, i.exp_day,  closeout, i.forward_price(closeout, 'ZAR', 0, 'ZAR-SWAP')
            j = j + 1



    
