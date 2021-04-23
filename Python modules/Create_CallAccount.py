import ael, SAGEN_Set_Additional_Info_new
def getcl():
    cl = ael.ChoiceList.select()
    for f in cl:
        if f.list == 'Funding Instype' and f.entry == 'CALL_EQ_Funding':
            return f
def create_ins(id, dat):
    ins= ael.Instrument.new('Deposit')
    ins.insid = id
    ins.curr = ael.Instrument['ZAR']
    ins.quote_type = 'Yield'
    ins.otc = 1
    #ins.product_chlnbr = ael.Choicelist.select()
    ins.contr_size=1
    ins.open_end = 'Open End'
    ins.pay_offset_method = 'Business Days'
    ins.date_from = dat
    if id.find('_L') > 0:
        ins.minimum_piece = 10000000000
    ins.commit()
    return ael.Instrument[id]
    
def update_leg(ins, dat):
    print ins.insid
    for l in ins.legs():
        lc = l.clone()
        lc.type = 'Call Float'
        lc.curr = ael.Instrument['ZAR']
        lc.nominal_factor = 1
        lc.float_rate = ael.Instrument['ZAR-ABSA-TOP20-CALL']
        lc.start_day = dat
        lc.end_day = dat.add_banking_day(ael.Instrument['ZAR'], 1)
        lc.rolling_period = '1m'
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
            c.delete()
        lc.reinvest = 1
        lc.regenerate()
        lc.commit()
        
def create_trade(ins, qty, p, dat):
    t = ael.Trade.new(ins)
    if ael.Portfolio[p.prfid + '_F']:
        t.prfnbr = ael.Portfolio[p.prfid + '_F']
    else:
        print 'Portfolio ' + p.prfid + '_F ' + 'does not exist'
    t.insaddr = ins
    t.acquire_day = dat
    t.acquirer_ptynbr = ael.Party['EQ Derivatives Desk']
    t.curr = ael.Instrument['ZAR']
    t.value_day = dat
    t.time = dat.to_time()
    t.quantity = qty
    t.price = 100
    t.status = 'FO Confirmed'
    t.counterparty_ptynbr = ael.Party['EQ Derivatives Desk']
    t.trader_usrnbr = ael.user()
    t.type = 'Normal'
    #SAGEN_Set_Additional_Info_new.setAddInfoEntity(t,'Funding Instype',getcl())
    ais = ael.AdditionalInfoSpec['Funding Instype']
    ai = ael.AdditionalInfo.new(t)
    ai.addinf_specnbr = ais
    ai.value = getcl().entry
    try:
        ai.commit()
        t.commit()
    except:
        print 'Could not commit the Call Trade'
    
        
def creat_call(p, dat):
    Lid = 'EQ_' + p.prfid + '_Funding_L'
    Did = 'EQ_' + p.prfid + '_Funding_D'
    l = ael.Instrument[Lid]
    d = ael.Instrument[Did]
    if p.prfid.find('_CFD') > 0:
        FLid = 'EQ_' + p.prfid + '_Fict_L'
        FDid = 'EQ_' + p.prfid + '_Fict_D'
        fl = ael.Instrument[FLid]
        fd = ael.Instrument[FDid]
        
        if fl:
            print 'Loan exists', fl.insid, fl.instype
        else:
            print 'Loan'
            loan = create_ins(FLid, dat)
            update_leg(loan, dat)
            create_trade(loan, -1, p, dat)
            print loan.insid
        if fd:
            print 'Depo exists', fd.insid, fd.instype
        else:
            print 'Depo'
            depo = create_ins(FDid, dat)
            update_leg(depo, dat)
            create_trade(depo, 1, p, dat)
            print depo.insid
    
    if l:
        print 'Loan exists', l.insid, l.instype
    else:
        print 'Loan'
        loan = create_ins(Lid, dat)
        update_leg(loan, dat)
        create_trade(loan, -1, p, dat)
        print loan.insid
    if d:
        print 'Depo exists', d.insid, d.instype
        return 1
    else:
        print 'Depo'
        depo = create_ins(Did, dat)
        update_leg(depo, dat)
        create_trade(depo, 1, p, dat)
        print depo.insid
    
#getcl()
creat_call(ael.Portfolio['HJTEST_CFD_ZERO'], ael.date('2008-08-01'))

