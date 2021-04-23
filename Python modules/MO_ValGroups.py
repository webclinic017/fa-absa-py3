'''
Script is used to check whether all trades in selected trade filter and /or portfolio is mapped to the correct ValGroup given
the CSA data for the selected counterparty. The script can also be used to bulk update trades to use correct ValGroup.

Date            CR              Developer               Change
==========      =========       ======================  ========================================================
2012-04-25      CHNG0000147579  Jaysen Naicker          Minor changes by Dirk Strauss
2012-08-03      CHNG0000349530  Willie van der Bank     Minor changes by Dirk Strauss
'''

#*******************************************************************************************************
import acm, time, ael

#-------------------------------------------------------------------------        
def get_instypes():
    s = 'Stock,StockRight,Future/Forward,Option,Warrant,LEPO,Bond,FRN,PromisLoan,Zero,Bill,CD,Deposit,FRA,Swap,CurrSwap,Cap,Floor,Collar,Curr,EquityIndex,BondIndex,RateIndex,Convertible,MultiOption,MultiAsset,Combination,FreeDefCF,FxSwap,Collateral,SecurityLoan,Repo/Reverse,BuySellback,PriceIndex,IndexLinkedBond,TotalReturnSwap,CreditDefaultSwap,EquitySwap,Commodity,DualCurrBond,MBS/ABS,UnKnown,CLN,CallAccount,CashCollateral,BasketRepo/Reverse,CreditIndex,IndexLinkedSwap,BasketSecurityLoan,CFD,VarianceSwap,Fund,Depositary Receipt,FXOptionDatedFwd,Portfolio Swap,ETF,Fx Rate,PriceSwap,Commodity Index,Commodity Variant'
    
    lst = s.split(',')    
    
    return lst

#-------------------------------------------------------------------------            
ael_variables = [ 
                ('Portfolio', 'Portfolio: ', 'FPhysicalPortfolio', None, None, 0, 1, 'Name of Portfolio'),
                 ('TrdFilter', 'Trade Filter: ', 'FTradeSelection', None, 'IRD_SWAPS_ALL_BMDELTA', 0, 1, 'Name of Trade Filter'),                                    
                 ('InsTypes', 'Instrument Types: ', 'string', get_instypes(), 'Swap,FRA,CurrSwap,IndexLinkedSwap', 1, 1, 'enum(InsType)'),
                 ('live_only', 'Only Live Deals: ', 'string', ['Yes', 'No'], 'Yes', 1),
                 ('excl_terminated', 'Exclude Terminated Deals: ', 'string', ['Yes', 'No'], 'Yes', 1),
                 ('calc_impact', 'Calc PnL Impact: ', 'string', ['Yes', 'No'], 'No', 1),
                 ('update_vg', 'Update ValGroup: ', 'string', ['Yes', 'No'], 'No', 1)
                 ] 

#-------------------------------------------------------------------------        
today = ael.date_today()

context = acm.GetDefaultContext()

cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
cs_ps = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')

global gvgs
gvgs = {}

t = '\t'

gvg_mask = {}
gvg_mask['DEFAULT'] = 'AC_OIS_<CCY>'
gvg_mask['CurrSwap'] = 'AC_OIS_<CCY>_XCCY'

#-------------------------------------------------------------------------        
def GetFxRates():
    date = acm.Time.DateToday()
    fccys = acm.FCurrency.Select('')
    ccys = {}
    curr = acm.FCurrency['ZAR']
    currBase = acm.FCurrency['USD']    
    inf = 1e10000
    for fccy in fccys:
        s = fccy.Name()
        if len(s) > 0:
            if fccy == currBase:
                fx_ccyusd = 1.0
            else:
                fx_ccyusd = fccy.Calculation().FXRate(cs, currBase, date).Number()

            if currBase == curr:
                fx_zarusd = 1
            else:
                fx_zarusd = currBase.Calculation().FXRate(cs, curr, date).Number()

            fx = fx_ccyusd * fx_zarusd

            if fx <> inf and fx <> -inf:
                ccys[s] = fx    
        
    return ccys

#-------------------------------------------------------------------------        
def get_vg_for_name(svg):
    global gvgs
    
    if len(gvgs) == 0:
        cls = acm.FChoiceList.Select('')
        
        for cl in cls:
            if cl.List() == 'ValGroup':
                gvgs[cl.Name()] = cl
                
    return gvgs.get(svg, None)                

#-------------------------------------------------------------------------        
def get_csa_valgroup_for_party(trd):
    ins = trd.Instrument()
    instype = ins.InsType()
    
    vg_mask = gvg_mask['DEFAULT']
    
    if gvg_mask.has_key(instype):    
        vg_mask = gvg_mask[instype]
        
    ret = ins.ValuationGrpChlItem()
    
    is_ois = 0
    if ret:
        if ret.Name()[0:6] == 'AC_OIS':
            is_ois = 1
        
    pty = trd.Counterparty()    
    
    if not pty:
        print '*' * 20, trd.Oid()
        
    csa = pty.add_info('CSA')
    csa_ccy = pty.add_info('CSA Collateral Curr')
    csa_switch_date = pty.add_info('CSA Switch Date')
    if csa_switch_date:
        csa_switch_date = ael.date_from_string(csa_switch_date)
        if csa_switch_date <= ael.date_from_string(acm.Time().AsDate(trd.TradeTime())):
            csa_ccy = pty.add_info('CSA CollateralCurr2')
        
    csa_type = pty.add_info('CSA Type')
    
    if csa and csa_type in ['Gold', 'Strong']:
        svg = vg_mask.replace('<CCY>', csa_ccy)
        vg = get_vg_for_name(svg)
        
        if vg:
            ret = vg
        else:
            print '*' * 20
            print 'Trade : ', trd.Oid()
            print 'Party : ', pty.Name()
            print 'CSA : ', csa
            print 'CSA Ccy : ', csa_ccy
            print 'CSA Type : ', csa_type
            print 'ValGroup not found : ', '-' + svg + '-'
            print '*' * 20

    elif is_ois:
        # currently on OIS ValGroup but shouldn't be
        ret = None
        
    
    return ret

#-------------------------------------------------------------------------        
def ael_main(data):  
    print time.ctime()

    p_port = data['Portfolio']
    p_trdfilt = data['TrdFilter']
    p_instypes = data['InsTypes']
    p_calc_impact = [0, 1][data['calc_impact'] == 'Yes']
    p_update_vg = [0, 1][data['update_vg'] == 'Yes']
    p_live_only = [0, 1][data['live_only'] == 'Yes']
    p_excl_terminated = [0, 1][data['excl_terminated'] == 'Yes']    
    
    inslst = []
    
    print '*****  Parameters *********'
    
    for p in p_port:
        print 'Portfolio : ', p.Name()
        inslst.extend(p.Instruments())

    for p in p_trdfilt:
        print 'TradeFilter : ', p.Name()
        inslst.extend(p.Instruments())
    
    print 'InsTypes : ', p_instypes
    print 'Live deals only : ', p_live_only
    print 'Exclude Terminated : ', p_excl_terminated
    print 'Calc Impact : ', p_calc_impact
    print 'Commit changes : ', p_update_vg
    print '*****************************\n'
    
    excl_instypes = ['Void', 'Simulated']
    
    if p_excl_terminated:
        excl_instypes.append('Terminated')
    
    print p_excl_terminated, excl_instypes
    
    fxrts = GetFxRates()

    dat = {}
    ins_to_updat = {}
    
    for ins in inslst:
        insid = ins.Name()
        instype = ins.InsType()               
        
        mat = ael.date('1970-01-01')
        
        if p_live_only:
            mat = ins.maturity_date()
            
            if mat <> '':
                mat = ael.date(mat)
            else:
                mat = ael.date('1970-01-01')
                
            is_mat = mat <= today
        else:
            is_mat = 0
        
            
        if instype in p_instypes and not is_mat:
            trds = ins.Trades()     #tf.TradesIn(ins)                
            
            for trd in trds:
                if trd.Status() not in excl_instypes:  
                    instmp_lst = [ins]
                    
                    # process all Combination children as well
                    if instype in ['Combination']:
                        instmp_lst.extend( ins.Instruments() )
                        
                    for instmp in instmp_lst:
                        if instmp.InsType() in p_instypes:
                            mapped_vg = instmp.ValuationGrpChlItem()
                            vg = get_csa_valgroup_for_party(trd)
                            
                            if vg:
                                svg = vg.Name()                
                                vg_ok = 1
                            else:
                                svg = '????????'
                                vg_ok = 0

                            key = (instmp.Name(), mapped_vg.Name(), vg_ok )            
                            
                            if not dat.has_key(key):                    
                                dat[key] = {}         
                                
                            if not dat[key].has_key(svg):
                                dat[key][svg] = []                    
                                
                            dat[key][svg].append(trd)
                                

        

    to_be_updated = {}
    probs = {}
    probs_vg = {}

    for key in dat.keys():    
        insid = key[0]
        svg = key[1]
        vg_ok = key[2]        
        
        if vg_ok and len( dat[key].keys() ) == 1:
            snew_vg = dat[key].keys()[0]
            
            if svg <> snew_vg:
                to_be_updated[insid] = [svg, snew_vg, dat[key][snew_vg]]            
        elif vg_ok:
            probs[key] = dat[key]        
        else:
            probs_vg[key] = dat[key]        
            
                

    #-----------------------------------------------------------------------------------
    print '=' * 10, t, '=' * 10, t, '=' * 10, t, '=' * 10, t, '=' * 10
    print 'To be updated'
    print '=' * 10, t, '=' * 10, t, '=' * 10, t, '=' * 10, t, '=' * 10
    print '\n'

    totpnl = 0.0

    cnt = len( to_be_updated.keys() )
    k = 0
    
    for insid in to_be_updated.keys():
        k += 1
        ins = to_be_updated[insid][2][0].Instrument()
        
        svg = to_be_updated[insid][0]
        svg_new = to_be_updated[insid][1]
        
        vg_new = get_vg_for_name(svg_new)
        
        trds = to_be_updated[insid][2]
        
        pvs = {}
        
        if p_calc_impact or p_update_vg:
            # get base pvs
            if p_calc_impact:
                for trd in trds:
                    trdnbr = trd.Oid()                

                    if svg <> svg_new:
                        pv = cs_ps.CalculateValue(trd, 'Portfolio Value End')
                    else:
                        pv = 0.0
                        
                    fx = fxrts[pv.Unit().Text()]
                    pv = pv.Number() * fx                    
                    pvs[trdnbr] = [pv, 0.0]
            
            if svg <> svg_new:
                ins.ValuationGrpChlItem(vg_new)        
            
            # get simu pvs
            if p_calc_impact and svg <> svg_new:
                for trd in trds:
                    trdnbr = trd.Oid()        

                    if svg <> svg_new:
                        pv = cs_ps.CalculateValue(trd, 'Portfolio Value End')
                    else:
                        pv = 0.0

                    fx = fxrts[pv.Unit().Text()]
                    pv = pv.Number() * fx                    
                    pvs[trdnbr][1] = pv
            
            if svg <> svg_new:
                if p_update_vg:                  
                    ins.Commit()
                else:                
                    ins.Unsimulate()    
        
        n = 0
        for trd in trds:
            n += 1
            if n == 1:
                pre = str(k) + ' | ' + str(cnt) + t + insid + t
            else:
                pre = t * 2
                
            trdnbr = trd.Oid()
            
            pnl = 0.0
            if p_calc_impact:
                pnl = pvs[trdnbr][1] - pvs[trdnbr][0]
                totpnl += pnl
                
            print pre, trdnbr, t, svg, t, ' --> ', t, svg_new, t, trd.Portfolio().Name(), t, trd.Counterparty().Name(), t, pnl
            
    print '\nTotal PnL impact : %.2f' % totpnl    
    print '\n' * 3
            
    #-----------------------------------------------------------------------------------        

    print '=' * 10, t, '=' * 10, t, '=' * 10, t, '=' * 10, t, '=' * 10
    print 'Problems - ValGroup Unknown'
    print '=' * 10, t, '=' * 10, t, '=' * 10, t, '=' * 10, t, '=' * 10
    print '\n'
                
    for key in probs_vg.keys():
        insid = key[0]
        svg = key[1]        
        
        print insid        
        print '-' * 20
        
        for svg_new in probs_vg[key].keys():
            trds = probs_vg[key][svg_new]
            
            for trd in trds:
                trdnbr_ext = ''
                
                mirror = trd.GetMirrorTrade()
                if mirror:
                    trdnbr_ext = mirror.Name()
                
                if trd.OptionalKey()[0:2] == 'MW':
                    trdnbr_ext += trd.OptionalKey()[0:2]
                
                print trd.Oid(), t, trdnbr_ext, t, svg, t, ' --> ', t, svg_new, t, trd.Portfolio().Name(), t, trd.Counterparty().Name()
            
        print '-' * 20        
        print '\n'    
        

    #-----------------------------------------------------------------------------------        

    print '=' * 10, t, '=' * 10, t, '=' * 10, t, '=' * 10, t, '=' * 10
    print 'Problems - not 1-to-1 instr v trade'
    print '=' * 10, t, '=' * 10, t, '=' * 10, t, '=' * 10, t, '=' * 10
    print '\n'
                
    for key in probs.keys():
        insid = key[0]
        svg = key[1]        
        
        print insid        
        print '-' * 20
        
        for svg_new in probs[key].keys():
            trds = probs[key][svg_new]
            
            for trd in trds:
                trdnbr_ext = ''
                
                mirror = trd.GetMirrorTrade()
                if mirror:
                    trdnbr_ext = mirror.Name()
                
                if trd.OptionalKey()[0:2] == 'MW':
                    trdnbr_ext += trd.OptionalKey()[0:2]
                
                print trd.Oid(), t, trdnbr_ext, t, svg, t, ' --> ', t, svg_new, t, trd.Portfolio().Name(), t, trd.Counterparty().Name()
            
        print '-' * 20        
        print '\n'    

    print time.ctime()
#*******************************************************************************************************
