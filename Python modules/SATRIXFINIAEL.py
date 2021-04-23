import ael

def ChangeSATRIXAttribs():

    trades = ael.TradeFilter['SATRIX FINI'].trades()
    print(len(trades))
    clentry = ael.Instrument['ZAR/STK/STX4/28OCT05/C/1059.25/OTC'].product_chlnbr
    for t in trades:
        ins = t.insaddr
    print(ins.quote_type)
    ic = ins.clone()
    ic.product_chlnbr = clentry
    ic.quote_type = 'Per Contract'
    ic.commit()
    ael.poll()
    tc = t.clone()
    tc.price = 0
    tc.premium = 0
    tc.commit()
    

ChangeSATRIXAttribs()
