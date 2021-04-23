import ael, time, pickle, dirk_utils

debug = 1

def bm_filters():
    flts = ('IRD_LTFX_ALL', 'IRD_SWAPS_ALL', 'IRD_PRIME', 'IRD_MAN_SWAP', 'IRD_MAN_SWAP_2', 'IRD_CPI', 'IRD_SWAP_PROP')
    
    for f in flts:
        tf = ael.TradeFilter[f + '_BMDELTA']
        if tf <> None:
            print tf.fltid
            tf.delete()
    
    tpl_term = [('Or', '', 'Status', 'equal to', 'Terminated', '')]
    
    for f in flts:
        nq = []
        tf = ael.TradeFilter[f]
        print f
        print len(tf.trades())
        q = tf.get_query()
        for tpl in q:
            if tpl in tpl_term:
                pass
            else:
                nq.append(tpl)            
    
        tpl = ('And', '', 'Instrument.Expiry day', 'greater equal', '1d', '')
        nq.append(tpl)
        
        tf = tf.new()
        tf.fltid = tf.fltid + '_BMDELTA'
        tf.set_query(nq)
        tf.commit()
        print len(tf.trades())
        print ''



def update_cpi_nacs():
    print ''
    cpiOff = ael.YieldCurve['ZAR-REAL-NACS']
    cpiSwap = ael.YieldCurve['ZAR-SWAP']
    cpiTest= ael.YieldCurve['ZAR-CPI-NACS']
    mkt = ael.Party['SPOT']
    
    bMarkPoints = []
    
    cpiTestPts= cpiTest.points()
    cpiTestBmks = cpiTest.benchmarks()
    
    for y in cpiTestBmks: 
        inst = y.instrument
        datePeriod = y.instrument.maturity_date()
        tpl = (datePeriod, inst)
        bMarkPoints.append(tpl)
        
    bMarkPoints.sort()
    step = ael.date_today()
    EndPeriod = bMarkPoints[len(bMarkPoints)-1][0]
    today = ael.date_today()
    
    for bMP in bMarkPoints:
        mat = bMP[0]
        days = today.days_between(mat) 
        tf = 182.5 / days
        
        df1 = cpiOff.yc_rate(today, mat, None, 'Act/365', 'Discount')
        df2 = cpiSwap.yc_rate(today, mat, None, 'Act/365', 'Discount')
        
        cpiPrice = (((df1/df2) ** tf) - 1) * 2
        cpiPrice = cpiPrice * 100            
        
        print today, mat, days, tf,  cpiPrice, bMP[1].insid, df1, df2
        
    
        updInst1 = bMP[1]        

        if len(updInst1.prices()) > 0:
            for p in updInst1.prices():
                if p.ptynbr == mkt:
                    priEntity = ael.Price[p.prinbr]
                    
    
            if priEntity.bid <> cpiPrice or priEntity.ask <> cpiPrice:
                priEntityC = priEntity.clone()
                priEntityC.last = cpiPrice
                priEntityC.settle = cpiPrice
                priEntityC.day = ael.date_today()
                priEntityC.commit()
                
        else:
            pn = ael.Price.new()
            #assert(pn.bits == 2)
            pn.last = cpiPrice
            #assert(pn.bits == 18)
            pn.settle = cpiPrice
            pn.insaddr = updInst1
            pn.day = ael.date_today()
            pn.ptynbr = mkt
            pn.curr = updInst1.curr
            pn.commit()














def get_fx_rates(curr):
    curr_base = ael.Instrument[curr]
    all_c = ael.Instrument.select("instype = 'Curr'")
    dt = ael.date_today()
    
    d = {}
    
    for c in all_c:
        d[c.insid] = curr_base.used_price(dt, c.insid)
    
    return d
    

def trade_lvl_bm():
    # parameters
    stf = 'SAIRD_IRP_CPIOnly'    
    sycs = ['ZAR-SWAP', 'ZAR-CPI']    
    sfile = 'c:\\temp\\test.xls'
    
    f=open(sfile, 'w')
    
    t0 = time.time()
    
    tf = ael.TradeFilter[stf]    
    
    if debug == 2:
        print 'original curve'
        print yc.pp()
        print ''
    
    # create dictionary
    d = {}
    
    # add headers
    d['trade'] = []
    d['trade'].append('InsType')
    d['trade'].append('Curr')
    d['trade'].append('PV')
    
    # add header row for curve name
    d['curve'] = []
    d['curve'].append('')
    d['curve'].append('')
    d['curve'].append('')    
    
    bms = []
    
    for syc in sycs:
        yc = ael.YieldCurve[syc].clone()
        
        for bm in yc.benchmarks():
            ins = bm.instrument
            mat = dirk_utils.bm_maturity(ins)
            tpl = (syc, mat, ins)
            bms.append(tpl)
    
    bms.sort()
    
    for bm in bms:
        ins = bm[2]
        d['trade'].append(ins.insid)
        d['curve'].append(bm[0])
        
    for trd in tf.trades():    
        pv0 = trd.present_value()
        d[trd.trdnbr] = []
        d[trd.trdnbr].append(trd.insaddr.instype)
        d[trd.trdnbr].append(trd.insaddr.curr.insid)
        d[trd.trdnbr].append(pv0)    
    
    for bm in bms:
        ins = bm[2]
        prc = ins.prices()            
        yc = ael.YieldCurve[bm[0]].clone()
        
        print 'bumping bm - ', ins.insid

        for p in prc:
            #print p.day, p.ptynbr.ptyid, p.settle
            if p.ptynbr.ptyid == 'SPOT':
                if debug == 2:
                    print 'found price'
                    print p.pp()
                    print ''
                    
                pc = p.clone()
                pc.settle = p.settle + 0.01
                pc.last = p.last + 0.01
                pc.bid = p.bid + 0.01
                pc.ask = p.ask + 0.01
                pc.apply()   
                
                if debug == 2:
                    print 'cloned point'
                    print pc.pp()
                    print ''
                    
        yc.calculate()
        yc.simulate()    
        
        if debug == 2:
            print 'modified curve'
            print yc.pp()
            print ''
            
        for trd in tf.trades():    
            pv0 = d[trd.trdnbr][2]
            pv1 = trd.present_value()
            pv01 = pv1 - pv0
            d[trd.trdnbr].append(pv01)
    
            if debug == 1:
                print trd.trdnbr, pv0, pv1, pv01            
        
        if debug == 1:
            print ''
        
        pc.revert_apply()
        yc.calculate()
        yc.simulate()
    
    # write curve headers
    ls = d['curve']
    s = ''    
    for l in ls:        
        s = s + '\t' + str(l)
    
    s = s + '\n'
    f.write(s)

    # write trade headers    
    ls = d['trade']
    s = 'trade'    
    for l in ls:        
        s = s + '\t' + str(l)
    
    s = s + '\n'
    f.write(s)
    
    keys = d.keys()
    
    for key in keys:
        if key <> 'trade' and key <> 'curve':
            ls = d[key]
            s = str(key)
            k = 0
            for l in ls:        
                s = s + '\t' + str(l)
            
            s = s + '\n'
            f.write(s)
    
    f.close()
            
    print 'Done', '%.0f' % (time.time() - t0) + 'sec'
    
    
def mod_filter():
    s = '642562,642582,688543,642504,642575,920876,688541,642585,642524,641734,642584,642554,642565,920872,940185,642507,642542,642537,642395,642422,920883,920874,920873,920884,920878,920887,920882,920889,920888,920877,642570,920890,738132,738131,642519,800885,642535,642476,642544,642541,642506,642543,642545,642536,557316,557940,688556,556791,557648,926783,736062,559420,556825,641731,559421,557496,557581,923239,943249,556805,556747,556832,556760,556761,933667,933194,924013,931935,926315,934258,933032,934179,934811,926839,557323,932126,739714,738349,678050,803337,556828,556771,556815,556765,556798,556788,556817,556830,902409,901421,951016,951103,952131,926212,901623,951289,902089,1031812,977131,982438,977191,923227,943210,982448,903380,903356,982452,982454,933097,903907,924086,931928,926285,917147,933021,927876,928710,926832,903120,933228,982440,982450,982462,982460,982436,998010,1033268,982458,903145,1033262,903812,896984'
    trds = s.split(',')
    trds.sort()
    
    tf = ael.TradeFilter['Dirk_tmp'].clone()
    q = []
    
    k = 0
    for trd in trds:
        k = k + 1
        if k == 1:
            q.append(('', '', 'Trade number', 'equal to', trd, ''))
        else:
            q.append(('Or', '', 'Trade number', 'equal to', trd, ''))
    
    tf.set_query(q)
    tf.commit()

    


