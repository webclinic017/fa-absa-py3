import acm, ael, time, csv


"""-----------------------------------------------------------------------------
Date:                   2011-05-31
Purpose:                Generates reset risk per date per index
Department and Desk:    IRD Desk
Requester:              Hendrik jv Rensburg
Developer:              Dirk Straus / Hendrik jv Rensburg
CR Number:              685904

-------------------------------------------------------------------------------"""

today = ael.date_today()
stoday = today.to_string('%Y-%m-%d')

ael_variables = [ 
                ('Portfolio', 'Portfolio: ', 'FPhysicalPortfolio', None, 'GK_SWAPS', 0, 1, 'Name of Portfolio'),
                 ('TrdFilter', 'Trade Filter: ', 'FTradeSelection', None, None, 0, 1, 'Name of Trade Filter'),                                    
                 ('MaxResetTerm', 'Max Reset Start Tenor: ', 'string', None, '50y', 1),
                 ('Outpath', 'Output Path: ', 'string', None, 'C:\\\\temp\\\\', 1),
                 ('Outfile', 'Output File: ', 'string', None, 'ResetRisk_' + stoday  + '.xls', 1),
                 ('TradeLevel', 'Trade Level: ', 'string', ['Yes', 'No'], 'No', 1)
                 ] 


# ================= CONSTANTS
debug = 0

gcs = acm.Calculations().CreateStandardCalculationsSpaceCollection()


filt_status = ['Void', 'Simulated']
filt_cf_type = ['Float Rate', 'Floorlet', 'Caplet']

GroupChain = []
GroupChain.append(acm.Risk().GetGrouperFromName('Default'))
grouper = acm.FChainedGrouper(GroupChain) 

bigdate = ael.BIG_DATE
smalldate = ael.SMALL_DATE
zar = ael.Instrument['ZAR']

bms_dat = {}
bms_dat['ZAR'] = ['ZAR-JIBAR-3M', 'ZAR/FRA/JI/|S|X|E|', 'ZAR/FRA/JI/PRE_MPC', 'ZAR/FRA/JI/POST_MPC', 'ZAR-SWAP']
bms_dat['USD'] = ['USD-LIBOR-3M', 'USD/FRA/LI/|S|X|E|', '', '', 'USD-SWAP']

context = acm.GetDefaultContext()
sheet_type = 'FPortfolioSheet'
column_id = 'Portfolio Forward Delta Yield Bucket'

global SE_rts
SE_rts = {}
#==============



#===================================================================================================================
def write_file(name, data, access='wb'):
    name =name.replace(' ', '')
    f = open(name, access)
    c = csv.writer(f, dialect = 'excel-tab')
    c.writerows(data)    
    f.close()


#===================================================================================================================
def lin_interp(xy, val):
    if val <= xy[0][0]:
        return xy[0][1], xy[0][2]
    for k in range(1, len(xy)):
        if xy[k][0] > val: 
            n = xy[k-1][0].days_between(xy[k][0]) * 1.0
            n1 = xy[k-1][0].days_between(val) * 1.0
            n2 = n - n1        
            interp = n1/n * xy[k][1] + n2/n * xy[k-1][1]
            return interp, xy[k][2]
            
    return xy[ len(xy)-1 ][1], xy[ len(xy)-1 ][2]

#===================================================================================================================
def get_next_mpc(ccy):
    ret = None
    lst = []
    
    ts_name = 'MO_MPC' + '_' +  ccy    
    tsspec = acm.FTimeSeriesSpec[ts_name]    
    ts = tsspec.TimeSeries()
    
    for t in ts:
        lst.append(ael.date(t.Day()))
            
    lst.sort()
    
    for dt in lst:        
        if dt > today:
            ret = dt
            break
                
    if not ret:
        msg =('ERROR: DATA PROBLEM, script will fail. The time series (%s) needs to have a date in the future.'
        'Please ask MO to complete it.' % ts_name)
        print msg
        raise ValueError(msg)

    return ret    

#===================================================================================================================    
def get_SE_yc(ccy):
    print 'Geting rates for ccy : ' + ccy
    ret = []
    done_mpc = 0
    
    if not bms_dat.has_key(ccy):
        return []
        
    bms = bms_dat[ccy]
    
    ael_ccy = ael.Instrument[ccy]
    
    next_mpc = get_next_mpc(ccy)
    
    insid_prempc = bms[2]
    ins_prempc = ael.Instrument[insid_prempc]
    
    insid_postmpc = bms[3]
    ins_postmpc = ael.Instrument[insid_postmpc]
    
    insid_fra = bms[1]
    
    # add first point
    insid = bms[0]
    ins = ael.Instrument[insid]
    rt = ins.used_price()
    dt = today
    
    prev_rt = rt
    
    ret.append( (dt, rt, insid) )
    
    for k in range(1, 10):    
        insid = insid_fra.replace('|S|', str(k)).replace('|E|', str(k+3) )
        ins = ael.Instrument[insid]
        rt = ins.used_price()
        dt = today.add_months(k).adjust_to_banking_day(ael_ccy)
        ret.append( (dt, rt, insid) )        
            
        if dt > next_mpc and not done_mpc:
            # add pre-mpc point
            dt = next_mpc
            insid = 'PRE-MPC'
            
            if ins_prempc:
                prert = ins_prempc.used_price()
            else:
                prert = prev_rt
            
            ret.append( (dt, prert, insid) )
            

            # add post_mpc point
            dt = next_mpc.add_days(1)
            insid = 'POST-MPC'
            
            if ins_postmpc:
                postrt = ins_postmpc.used_price()
            else:
                postrt = rt
            
            ret.append( (dt, postrt, insid) ) 
            
            done_mpc = 1
            
        prev_rt = rt
    
    ret.sort()
    
    return ret

#===================================================================================================================        
def get_adj_fwd_rate(yc_fwd, ccy, dt1, dt2):
    global SE_rts    
    
    if not SE_rts.has_key(ccy) and ccy in bms_dat.keys():
        SE_rts[ccy] = get_SE_yc(ccy)
    
    fwd_rt = yc_fwd.Rate(dt1, dt2, 'Simple', 'Act/365', 'Spot Rate', None, 0)

    if SE_rts.has_key(ccy) and dt1 <= today.add_period('9m'):                
        syc_base = bms_dat[ccy][4]
        yc_base = acm.FYieldCurve[syc_base]
        yc_base_calc = yc_base.IrCurveInformation()
        
        fwd_sys = yc_base_calc.Rate(dt1, dt1.add_period('3m'), 'Simple', 'Act/365', 'Spot Rate', None, 0)
        
        fwd_mkt, bucket = lin_interp(SE_rts[ccy], dt1)
        fwd_mkt =  fwd_mkt / 100.0
        
        adj = fwd_mkt - fwd_sys
    else:
        adj = 0.0    
        bucket = ''
    
    return fwd_rt, adj, fwd_rt + adj, bucket

#===================================================================================================================        
# =========================================================================
def GenStrFromList(delim, *list):
    s = ''
    k = 0
    cnt = len(list)
    
    for o in list:
        k += 1
        if k < cnt:
            s = s + str(o) + delim
        else:
            s = s + str(o) + '\n'
    
    return s


# =========================================================================
def RecurseTree(nd, ret):
    nd.Expand(1, 100)
    sType = str(nd.Item().ClassName())    
    cnt = nd.NumberOfChildren()
    
    if debug:
        print nd.StringKey(), sType, cnt
    
    if cnt == 0:                # lowest level
        ret.append(nd)
    else:
        nd_iter = nd.Iterator().FirstChild()            
        
        while nd_iter:        
            nd_child = nd_iter.Tree()       
            RecurseTree(nd_child, ret) 
            nd_iter = nd_iter.NextSibling()

# =========================================================================
def GetInsLst(ins, ret):
    if not ins:
        return
        
    instype = ins.InsType()
    
    if instype in ['Option']:
        und = ins.Underlying()
        GetInsLst(und, ret)
    elif instype in ['Combination']:
        cboinscol = ins.Instruments()
        
        for cboins in cboinscol:
            GetInsLst(cboins, ret)
            
    else:
        ret.append(ins)
        
        
# =========================================================================

def GetResets(trds, max_reset):
    cnt = len(trds)
    n = 0

    dat = {}
    excl_cf = []

    for trd in trds:
        n += 1
        
        if n % 100 == 0:
            print n, '/', cnt
        
        if trd.Status() not in filt_status:
            trdnbr = trd.Oid()          
            parent_ins = trd.Instrument()
            
            inslst = []
            
            GetInsLst(parent_ins,  inslst)
            
            for ins in inslst:                
                for leg in ins.Legs():                
                    float_ref = leg.FloatRateReference()
                    
                    if float_ref:
                        rsts = leg.Resets()
                        float_ref_id = float_ref.Name()
                    else:
                        rsts = []
                        
                    for rst in rsts:                        
                        start = ael.date( rst.Day() )
                        end = ael.date( rst.EndDate() )
                        rst_type = rst.ResetType()
                        cf = rst.CashFlow()
                        cf_c = cf.Calculation()     
                        try:
                            nom = cf_c.Nominal(gcs, trd).Number()
                        except:
                            nom = 0.0
                        
                        cf_type = cf.CashFlowType()
                        
                        if cf_type not in filt_cf_type and cf_type not in excl_cf:
                            excl_cf.append(cf_type)
                        
                        if start > today and start <= max_reset and cf_type in filt_cf_type:
                            if not dat.has_key(trdnbr):
                                dat[trdnbr] = {}
                                
                            if not dat[trdnbr].has_key(float_ref_id):
                                dat[trdnbr][float_ref_id] = []
                            
                            if (start, end) not in dat[trdnbr][float_ref_id]:
                                dat[trdnbr][float_ref_id].append( (start, end, nom) )
                            
    print excl_cf
    
    return dat

# =========================================================================    

def ael_main(data):    

    # Process parameters
    #--------------------------------------------------------
    print '=' * 50
    keys = data.keys()
    keys.sort()
    
    for k in keys:
        print k, data[k]
    print '=' * 50
    
    print '\n' * 3
    
    p_port = data['Portfolio']
    p_trdfilt = data['TrdFilter']
    p_max_rst_term = data['MaxResetTerm']
    p_outpath = data['Outpath']
    p_outfile = data['Outfile']
    p_trd_level = data['TradeLevel']
    
    trds = []
    
    tm = time.clock()

    cs = acm.Calculations().CreateCalculationSpace( context, sheet_type )
    
    for p in p_port:
        trds.extend(p.Trades())

    for p in p_trdfilt:
        trds.extend(p.Trades())

    max_reset = today.add_period(p_max_rst_term)
    
    if p_trd_level =='Yes':
        trdlvl = 1
    else:
        trdlvl = 0

    sOutPath = p_outpath
    sOutFile = p_outfile
    #--------------------------------------------------------

    

    dat = GetResets(trds, max_reset)

    trds = dat.keys()
    trdcnt = len(trds)
    nn = 0

    fin = {}

    for trdnbr in trds:
        if debug:
            print '\n', '=' * 20
            print trdnbr
        
        nn += 1
        if nn % 100 == 0:
            print nn, '/', trdcnt
            
        trd = acm.FTrade[trdnbr]  
        ins = trd.Instrument()
        und = ins.Underlying()
        
        instype = ins.InsType()
        insid = ins.Name()
        
        if und:
            instype += ' >> ' + und.InsType()    
        
        fltrefs = dat[trdnbr].keys()
        multi_flt = 0
        
        if len(fltrefs) > 1:
            multi_flt = 1
            if debug:
                print '\n', '=' * 15, trdnbr, fltrefs
        
        nd = cs.InsertItem( trd )
        nd.ApplyGrouper(grouper) 
        cs.Refresh()
        
        if not multi_flt:
            nds = [nd]
        else:
            nds = []    
            RecurseTree(nd, nds)            
        
        for nd in nds:
            nd_type = str(nd.Item().ClassName())    
            
            if nd_type in ['FLegAndTrades']:            
                leg = nd.Item().Leg()
                fltrefobj = leg.FloatRateReference()            
                
                if fltrefobj:
                    fltref = fltrefobj.Name()                
                else:
                    yc = None
            else:  
                fltref = fltrefs[0]
                fltrefobj = acm.FInstrument[fltref]                        
            
            if fltref:    
                yc = fltrefobj.Calculation().MappedDiscountCurve(gcs)
                fltrefccy = fltrefobj.Currency().Name()
                
                dts = dat[trdnbr][fltref]
                dts.sort()
                
                dt_map = {}
                sdt = ''
                
                for dt in dts:
                    if dt[0] <= max_reset:
                        start = dt[0].to_string('%Y-%m-%d')
                        end = dt[1].to_string('%Y-%m-%d')
                        nom = dt[2]
                        df = yc.Discount(today, dt[0])
                        fwd_rt, adj, adj_fwd_rt, bucket = get_adj_fwd_rate(yc, fltrefccy, dt[0], dt[1])
                        
                        dt_map[start] = [start, nom, df, fwd_rt, adj, adj_fwd_rt, bucket]
                        
                        if "'" + start + "'" not in sdt:
                            sdt += "'" + start + "' "
                
                sdt += "'Rest'"
                
                if debug:
                    print '\nBuckets\n', '=' * 20, '\n', len(sdt.split(' ')), sdt
                    
                    dt_map_keys = dt_map.keys()
                    dt_map_keys.sort()
                    
                    for dt_map_end in dt_map_keys:
                        print dt_map[dt_map_end], '\t', dt_map_end
                    
                time_buckets = acm.Time.CreateTimeBuckets( 0, sdt, None, None, 0, True, True, True, True, False )
                column_config = acm.Sheet.Column().ConfigurationFromTimeBuckets(time_buckets )
                
                calc = cs.CreateCalculation( nd, column_id, column_config )
                
                vals = calc.Value()    
                
                dts = sdt.split(' ')                        
                
                cnt = len(vals)            
                
                if cnt <> len(dts):
                    print trdnbr, '- Bucket count and Val count differ :', cnt, len(dts)

                if debug:
                    print '\nVals', '=' * 20
                    
                for n in range(0, cnt):
                    enddt = dts[n].lstrip("'").rstrip("'")                
                    
                    if enddt <> 'Rest':
                        stdt = dt_map[enddt][0]
                        nom = dt_map[enddt][1] 
                        df = dt_map[enddt][2] 
                        fwd_rt = dt_map[enddt][3] 
                        adj = dt_map[enddt][4] 
                        adj_fwd_rt = dt_map[enddt][5] 
                        bucket = dt_map[enddt][6] 
                        
                        app = [ [stdt, '', 1.0] ]
                    else:
                        stdt = enddt
                        nom = 0.0    
                        df = fwd_rt = adj = adj_fwd_rt = 0.0                
                        
                        app = [ [stdt, '', 1.0] ]
                    
                    if debug:
                        print n, '\t', enddt, '\t', enddt
                    
                    val = vals[n].Number()                                
                    
                    for a in app:                                        
                        stdt = a[0]
                            
                        per = a[1]
                        fact = a[2]
                        
                        if trdlvl:
                            key = (fltref, trdnbr, stdt)
                        else:
                            key = (fltref, 'Total', stdt)
                        
                        if stdt == 'Rest' and val <> 0 and max_reset == bigdate:
                            print '-=' * 15, trdnbr, instype, '%.0f' % val, cnt            
                        
                        if fin.has_key(key):
                            fin[key][0] += val * fact
                            fin[key][1] += nom * fact                        
                        else:
                            fin[key] = [val * fact, nom * fact, df, fwd_rt, adj, adj_fwd_rt, bucket]

    keys = fin.keys()
    keys.sort()

    outdat = []

    hdr = ['RepDate', 'Index', 'Trade', 'ResetDate', 'PV01', 'Nominal', 'df', 'fwd', 'adj', 'adj_fwd', 'prov', 'bucket']
    outdat.append(hdr)

    for k in keys:
        idx = k[0]
        trd = k[1]
        dt = k[2]
        pv01 = fin[k][0]
        nom = fin[k][1]
        df = fin[k][2]
        fwd_rt = fin[k][3]
        adj = fin[k][4]
        adj_fwd_rt = fin[k][5]
        prov = adj * pv01 * 100 * 100
        bucket = fin[k][6]
        
        sln = [today, idx, trd, dt, pv01, nom, df, fwd_rt, adj, adj_fwd_rt, prov, bucket]
        outdat.append(sln)
        
    write_file(sOutPath + sOutFile, outdat)

    cs.Clear()
    acm.Memory().GcWorldStoppedCollect()

    print '%.0f' % (time.clock() - tm), 'sec'
    print 'Wrote secondary output to:::', sOutPath + sOutFile
