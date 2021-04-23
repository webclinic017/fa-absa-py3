import ael

dt = ael.date_today()

ael_variables = [('Date', 'Run Date', 'date', dt, dt, 0, 0)]

def ael_main(dict):

    print '**************************************'    
    print '******Starting To Copy *****'	
    print '**************************************'

    ael.poll()

    td = ael.date(dt)
    print td
    for ins in ael.Instrument:
        cp = ins.prices()
        hp = ins.historical_prices(td)
        if ins.instype not in ('BuySellback', 'Repo/Reverse', 'Deposit', 'FRN'): 
#and ins.exp_day >= ael.date_today():
            if len(cp) == 0:
                for p in hp:
                    nhp = p.new()
                    nhp.day = ael.date_today()
                    print nhp.pp()
                    nhp.commit()
            else:
                for p in cp:
                    ncp = p.clone()
                    ncp.day = ael.date_today()
                    print ncp.pp()
                    ncp.commit()
    ael.poll()
    print '**************************************'    
    print '******Finished Copy *****'	
    print '**************************************'









