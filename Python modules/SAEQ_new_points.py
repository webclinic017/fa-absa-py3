import ael, acm
#print dir(acm)
#val = acm.GetCalculatedValueFromString()
ins = ael.Instrument['ZAR/EQ/ALSI/2W/P/-15.00']
und = 'ZAR/ALSI'
#print ins.pp()
maturities = ['2011-12-15', '2009-06-18', '2010-06-17']
strikes = [-90.00, -80.00, -70.00, -60.00, -50.00, -30.00, -25.00, -20.00, -15.00, -12.50, -10.00, -7.50, -5.00, -2.50, 0.00, 2.50, 5.00, 7.50, 10.00, 12.50, 15.00, 20.00, 25.00, 30.00, 50.00, 60.00, 70.00, 80.00, 90.00, 100.00]
 
def creat_instr(maturities, strikes, und, cs):
    uins = ael.Instrument[und]
    vg = ael.ChoiceList.read('entry = "EQ_ALSI_Opt_Blk" and list = "ValGroup"')
    list = []
    for s in strikes:
        for m in maturities:
            print m, s
            opt = ael.Instrument.new('Option')
            opt.und_insaddr = uins
            opt.exp_day = ael.date(m)
            opt.exp_time = 0
            opt.generic = 0
            opt.otc = 0
            opt.spot_banking_days_offset = 0
            opt.product_chlnbr = vg
            opt.contr_size = cs
            opt.strike_price = s
            opt.strike_type = 'Rel Frw Pct'
            opt.exercise_type = 'American'
            opt.pay_day_offset = 0
            if opt.exp_day.to_ymd()[1] == 6:
                v= 'JUN'
            elif opt.exp_day.to_ymd()[1] == 12:
                v = 'DEC'
            ep = (str)(opt.exp_day.to_ymd()[0])
            print ep[2:4]
            if round(s) == s:
                s = (int)(s)                
            if s > 0:
                t = '+' + (str)(s)
            else:
                t = (str)(s)
            opt.insid = 'ZAR/FUT/ALSI/RFP/' + v + ep[2:4] + '/' + t + '%'
            print opt.insid
            pos = (opt.insid).find('#')
            print opt.insid
            if pos < 0:
                try:
                    opt.commit()
                    list.append(opt.insid)
                except:
                    print 'Dup'
            else:
                list.append(opt.insid[0:(pos-1)])
                print 'Already exists'
    print list
    return list
 
def creat_new_vol(voname):
    vl = ael.Volatility[voname]
    if vl:
        return voname
    else:
        nvol = ael.Volatility.new()
        #print nvol.pp()
        #oldvol = ael.Volatility['SAEQ_Skew']
        #print 'Old'
        #for op in oldvol.points():
        #    print op.pp()
        nvol.vol_name = voname
        nvol.vol_type = 'Benchmark'
        nvol.framework = 'Black & Scholes'
        nvol.bond_vol_type = 'Price'
        nvol.strike_type = 'Rel Frw Pct'
        nvol.curr = ael.Instrument['ZAR']
        nvol.vol_value_type = 'Relative'
        nvol.interpolation_method = 'Hermite'
        nvol.risk_type = 'Equity Vol'
        try:
            nvol.commit()
        except:
            print 'Not comitted'
        return voname
    
def add_vol_points_v(inslist, volname, vol):
    v = ael.Volatility[volname].clone()
    cpoints = []
    p = v.points()
    for i in p:
        cpoints.append(i.insaddr.insid)
    #print dir(v)
    for l in inslist:
        print 'Ins: ', l, vol
        vins = ael.Instrument[l]
        print 'Instrumetns obj', vins
        if l not in cpoints:
            vp = ael.VolPoint.new(v)
            vp.insaddr = vins
            vp.volatility = (float)(vol)
            vp.commit()
        else:
            print 'Point exists'
        #print vp.pp()
    v.commit()
def add_vol_points(inslist, volname):
    v = ael.Volatility[volname].clone()
    cpoints = []
    p = v.points()
    for i in p:
        cpoints.append(i.insaddr.insid)
    #print dir(v)
    for l in inslist:
        print 'Ins: ', l
        vins = ael.Instrument[l]
        print 'Instrumetns obj', vins
        if l not in cpoints:
            vp = ael.VolPoint.new(v)
            vp.insaddr = vins
            vp.commit()
        else:
            print 'Point exists'
        #print vp.pp()
    v.commit()
 
def get_unds():
    list = []
    s = ael.Instrument.select('instype = "Stock"')
    for i in s:
        list.append(i.insid)
    ei = ael.Instrument.select('instype = "EquityIndex"')
    for i in ei:
        list.append(i.insid)
    return list
    
#ael_variables = [('underlying','Underlying Instrument','string',get_unds(),'ZAR/ALSID_FF'),
#                ('vn','VolatilityName','string',None,None),
#                ('cons','Contract Size','float',None,1.0),
#                ('vols','Volatility','float',None,1.0),
#                ('utype','UnderlyingType','string',['SSFT','INDEX'],'SSFT')]
 
 
creat_instr(maturities, strikes, und, 10) 
 
#def ael_main(ael_dict):
#    und = ael_dict["underlying"]
#    vn = ael_dict["vn"]
#    consize = ael_dict["cons"]
#    print und,vn
#    vol = ael_dict["vols"]
#    type = ael_dict["utype"]
#    
#    if type == 'SSFT':
#        #und = 'ZAR/ALSID_FF'
#        maturities = ['15d','30d','60d','90d','180d','270d','365d','550d','730d','1095d']
#        strikes = [-90.00,-80.00,-65.00,-50.00,-40.00,-30.00,-20.00,-10.00,-5.00,-2.50,0.00,3.00,5.00,10.00,20.00,30.00,40.00,50.00,80.00,150.00,400.00,900.00]
#    else:
#        maturities = ['1w','2w','1m','2m','3m','4m','6m','9m','12m','15m','18m','21m','24m','36m','48m','84m','96m','108m','120m']
#        strikes = [-90.00,-80.00,-70.00,-60.00,-50.00,-30.00,-25.00,-20.00,-15.00,-12.50,-10.00,-7.50,-5.00,-2.50,0.00,2.50,5.00,7.50,10.00,12.50,15.00,20.00,25.00,30.00,50.00,60.00,70.00,80.00,90.00,100.00]
#    l = creat_instr(maturities,strikes,und,consize)
#    print 'l = ',l
#    von = creat_new_vol(vn)
#    print 'vn',von
#    print 'voor volpoints'
#    if vol == 1.0:
#        add_vol_points(l,von)
#    else:
#        add_vol_points_v(l,von,vol)
#    print 'vols'

 
