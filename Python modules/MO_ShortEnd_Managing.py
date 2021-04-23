#Developer			:Dirk Strauss/Martin van der Walt
#Purpose				:Displays provision on a reset/resetbucket level. Also displays a resetrisk table
#Deparment and Desk	:Middle Office
#Requester			:Front Office
#CR Number			:
#Query				:MO_ShortEndCurve_Managing
#Date				:2010-03-29

import acm, ael, sys

class CalcSpace(object):

    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
#===========================================================Main================================================================================

def Main(data_lst):

    InputData = data_lst[0][0] 
    FilterData = data_lst[0][1] 
    PortfolioData = data_lst[0][2] 
    ReportType = data_lst[0][3] 
    outpath = data_lst[0][4]
    Currency = data_lst[0][5]
    FwdCurve = data_lst[0][6] 
    

    print 'Starting'

    if FwdCurve not in ['ZAR-SWAP', 'USD-SWAP'] and ReportType in ('Prov_per_Reset', 'Prov_per_ResetBucket'):
        print 'Error'
        return 'Provision report not available for curve, run risk report'    
    
    #=======================================================Variables=============================================================================

    if len(PortfolioData ) > 0 and len(FilterData) > 0:
        print 'Error'
        return 'Please enter only one Data field'
        
    if len(PortfolioData) == 0 and len(FilterData) == 0:
        print 'Error'
        return 'Please enter Data field'


    if InputData == 'Portfolio':
        Name = PortfolioData
    else:
        Name = FilterData

    dt = ael.date_today()
    dt_str = dt.to_string()
    dte = dt.add_months(9)

    
    reset_dict = {}
    reset_day_dict = {}
    floatref_dict = {}
    rstb = {}
    
    trds_final1 = []
    trds_final2 = []
    
    mkt = {}
    mkt_dte = {}
    mkt_rt = {}
    mpc_list = {}
    
    data = {}
    
    TotalProv = 0  
    
    trds_comb = []
    trds = []
    
    fwd_rt = 0
    se_rt = 0
    provision = 0

    #===================================================Opening Files=========================================================
    try:
        if ReportType in ('Prov_per_Reset', 'Reset_Risk'):
            data_file1 = open(outpath + 'Data_file' + '_' + InputData + '_' + Name + '_' + ReportType + '_' + Currency + '_' + FwdCurve + '_perReset.xls', 'w')
        else:
            data_file1 = open(outpath + 'Data_file' + '_' + InputData + '_' + Name + '_' + ReportType + '_' + Currency + '_' + FwdCurve + '_perResetBucket.xls', 'w')
        s = GenStrFromList('\t', 'ReportType', ReportType) 
        data_file1.write(s)
        s = GenStrFromList('\t', 'InputData', InputData) 
        data_file1.write(s)
        s = GenStrFromList('\t', 'Input Data Name', Name) 
        data_file1.write(s)
        s = GenStrFromList('\t', 'Currency', Currency) 
        data_file1.write(s)
        s = GenStrFromList('\t', 'Yield-Curve', FwdCurve) 
        data_file1.write(s)
        if ReportType == 'Prov_per_Reset':
            s = GenStrFromList('\t', 'Trade', 'Instrument', 'Rolling Period Count', 'Rolling Period Unit', 'ResetType', 'Reset Day', 'Reset Start', 'Reset End', 'Float Ref', 'Nominal 1m', 'Nominal 3m', 'Nominal 6m', 'Nominal 9m', 'Nominal 12m', 'Currency', 'Reset Period', 'Forward Curve', 'Forward Rate', 'Mkt Rate', 'ZAR Provision')
        elif ReportType == 'Reset_Risk':
            s = GenStrFromList('\t', 'Trade', 'Instrument', 'Rolling Period Count', 'Rolling Period Unit', 'ResetType', 'Reset Day', 'Reset Start', 'Reset End', 'Float Ref', 'Nominal 1m', 'Nominal 3m', 'Nominal 6m', 'Nominal 9m', 'Nominal 12m', 'Currency', 'Reset Period')
        elif ReportType == 'Prov_per_ResetBucket':
            s = GenStrFromList('\t', 'StartDate', 'EndDate', 'Nominal', 'Fwd Rate', 'SE rate', 'Provision')
        data_file1.write(s)        
        
        if ReportType in ('Prov_per_Reset', 'Reset_Risk'):
            data_file2 = open(outpath + 'Data_file' + '_' + InputData + '_' + Name + '_' + ReportType + '_' + Currency + '_' + FwdCurve + '_perResetDay.xls', 'w')
            s = GenStrFromList('\t', 'ReportType', ReportType) 
            data_file2.write(s)
            s = GenStrFromList('\t', 'InputData', InputData) 
            data_file2.write(s)
            s = GenStrFromList('\t', 'Input Data Name', Name) 
            data_file2.write(s)
            s = GenStrFromList('\t', 'Currency', Currency) 
            data_file2.write(s)
            s = GenStrFromList('\t', 'Yield-Curve', FwdCurve) 
            data_file2.write(s)
            if ReportType in ('Prov_per_Reset'):
                s = GenStrFromList('\t', 'ResetDay', 'Nominal 1m', 'Nominal 3m', 'Nominal 6m', 'Nominal 9m', 'Nominal 12m', 'ZAR Provision')
            elif ReportType == 'Reset_Risk':
                s = GenStrFromList('\t', 'ResetDay', 'Nominal 1m', 'Nominal 3m', 'Nominal 6m', 'Nominal 9m', 'Nominal 12m')
            data_file2.write(s)
    except:
        return "Error, Input Fields Incorrect"


    #======================================================Filter Trade Population============================================
    
    #======================================================Get initial set of trades============================
    
    if InputData == 'Filter':
        trds =  acm.FTradeSelection[Name].Trades()
        for t in trds:            
            ins = t.Instrument()
            
            if ReportType == 'Prov_per_ResetBucket' and ins.InsType() in ('Swap', 'FRA'):
                if ael.date_from_string(ins.ExpiryDateOnly()) > dt: 
                    trds_final1.append(t)
            elif ReportType in ('Prov_per_Reset', 'Reset_Risk'):
                if ins.InsType() not in ('Combination', 'Curr', 'IndexLinkedSwap', 'FRN'):                
                    if ael.date_from_string(ins.ExpiryDateOnly()) > dt: 
                        trds_final1.append(t)
                elif ins.InsType()=='Curr':
                    if ael.date_from_string(t.ValueDay()) > dt:                
                        trds_final1.append(t)
                elif ins.InsType() not in ('IndexLinkedSwap', 'FRN'):
                    comb_ins = ins.Instruments()
                    for i_c in comb_ins:
                        trds_comb = i_c.Trades()
                        if len(trds_comb) >=1:
                            t = trds_comb[0]
                            trds_final1.append(t)
                        else:
                            pass      
                
    elif InputData == 'Portfolio':
        trds = acm.FPhysicalPortfolio[Name].Trades()
        for t in trds:             
            ins = t.Instrument()
            if ReportType == 'Prov_per_ResetBucket' and ins.InsType() in ('Swap', 'FRA'):
                if ael.date_from_string(ins.ExpiryDateOnly()) > dt:
                    if t.Status() in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed', 'Terminated']:
                        trds_final1.append(t)
            elif ReportType in ('Prov_per_Reset', 'Reset_Risk'):
                if ins.InsType() not in ('Combination', 'Curr', 'IndexLinkedSwap', 'FRN'):
                    if ael.date_from_string(ins.ExpiryDateOnly()) > dt: 
                        if t.Status() in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed', 'Terminated'):
                            trds_final1.append(t)
                elif ins.InsType()=='Curr':
                    if ael.date_from_string(t.ValueDate()) > dt:                
                        if t.Status() in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed', 'Terminated'):
                            trds_final1.append(t)
                elif ins.InsType() not in ('IndexLinkedSwap', 'FRN'):
                    comb_ins = ins.Instruments()
                    for i_c in comb_ins:
                        trds_comb = i_c.Trades()
                        if len(trds_comb) >= 1:                    
                            t = trds_comb[0]
                            trds_final1.append(t)
                        else:
                            pass            
    else:
        print 'Select one Input Type'
                             
    if ReportType == 'Reset_Risk':
        trds_final2 = trds_final1
    else:        
        for t in trds_final1:
            if FindBasisTrades(t) < 2:
                trds_final2.append(t)
 
    if len(trds_final2) == 0:
        print "No Trades in Selection , try again"
        return
    
    #=======================================================For Provision Reports============================================================
    
    if ReportType in ('Prov_per_Reset', 'Prov_per_ResetBucket'):    
    

        #=======================================================Get Next MPC Date=================================================
    
        timeseries = 'MO_MPC' + '_' +  Currency
        mpc_list[Currency] = PickUpMPC(timeseries)    
        data[Currency] = SE_Curve(dt_str, ael.date(get_next_mpc(dt, mpc_list[Currency])), Currency)
        mkt[Currency] = data[Currency][0]
        mkt_dte[Currency] = data[Currency][1]
        mkt_rt[Currency] = data[Currency][2]    
               
        #================================================Create main reset dictionary and write data per reset==================== 
        for t in trds_final2:
            ins = t.Instrument()            
            for l in ins.Legs():                
                if l.Currency().Name() == Currency:
                    if l.LegType() == 'Float':                    

                        #M.KLIMKE fwd_curve = l.MappedForwardLink().Link().YieldCurveComponent().Name()
                        if 'FYCAttribute' in str(l.MappedForwardLink().Link().YieldCurveComponent().Class()):
                            fwd_curve = l.MappedForwardLink().Link().YieldCurveComponent().Curve().Name()
                            crv = l.MappedForwardLink().Link().YieldCurveComponent().Curve()                               
                        else:
                            fwd_curve = l.MappedForwardLink().Link().YieldCurveComponent().Name()
                            crv = l.MappedForwardLink().Link().YieldCurveComponent()
                        if fwd_curve in ('ZAR-SWAP-SPREAD-1m', 'ZAR-SWAP-SPREAD-6m', 'ZAR-SWAP-SPREAD-12m'):
                            fwd_curve = 'ZAR-SWAP'
                            crv = acm.FBenchmarkCurve['ZAR-SWAP']                            
                        dc = l.DayCountMethod()    
                        if fwd_curve == FwdCurve:
                            for cf in l.CashFlows():
                                for r in cf.Resets():
                                    if r <> None and l.FloatRateReference() <> None:
                                        if r.ResetType() in ('Single', 'Compound', 'Weighted'):                        
                                            if ael.date(r.Day()) >= dt and ael.date(r.Day()) <= dte:
                                                fwd_rt = crv.IrCurveInformation().Rate(ael.date(r.Day()), ael.date(r.Day()).add_months(3), 'Quarterly', l.DayCountMethod(), 'Forward Rate', None, 0)                                                
                                                se_rt = lin_interp(mkt_dte[l.Currency().Name()], mkt_rt[l.Currency().Name()], ael.date(r.Day())) / 100                            
                                                reset_period = ael.date(r.StartDate()).years_between(ael.date(r.EndDate()))
                                                sign = DetermineSign(l.PayLeg())
                                                nominal = cf.Calculation().Nominal(CalcSpace.calcSpace, t).Number()
                                                provision = nominal / 1000000 * reset_period * 96 * (se_rt - fwd_rt) * 10000 * get_fx_rate(l.Currency().Name())                                                                                                                                       
                                                
                                                if  ReportType == 'Prov_per_Reset':
                                                    reset_lst = [r.Day(), r.StartDate(), r.EndDate(), l.FloatRateReference().Name(), nominal, l.Currency().Name(), reset_period, fwd_curve, fwd_rt, se_rt, provision]                                            
                                                    reset_dict[r.Oid(), t.Oid()]= reset_lst                     
                                                    if reset_dict[r.Oid(), t.Oid()][0] in reset_day_dict.keys():
                                                        pass
                                                    else:
                                                        reset_day_dict[reset_dict[r.Oid(), t.Oid()][0]] = {'1m' : 0 , '3m' : 0, '6m' : 0 ,'9m' : 0 , '12m' : 0 , 'Provision' : 0}                                                
                                                    s = GenStrFromList('\t', t.Oid(), ins.InsType(), l.RollingPeriodCount(), l.RollingPeriodUnit(), r.ResetType(), r.Day(), r.StartDate(), r.EndDate(), l.FloatRateReference().Name(),  CalculateBucket('1m', reset_period, nominal), CalculateBucket('3m', reset_period, nominal), CalculateBucket('6m', reset_period, nominal), CalculateBucket('9m', reset_period, nominal), CalculateBucket('12m', reset_period, nominal), l.Currency().Name(), reset_period, fwd_curve, fwd_rt, se_rt, provision)                                      
                                                    data_file1.write(s)                                   
                                                    
                                                elif ReportType == 'Prov_per_ResetBucket':
                                                    if (r.StartDate() + ':' + r.EndDate()) not in rstb.keys():
                                                        rstb[r.StartDate() + ':' + r.EndDate()]=(r.StartDate(), r.EndDate(), nominal, fwd_rt, se_rt, provision)
                                                    else:
                                                        rstb[r.StartDate() + ':' + r.EndDate()]=(r.StartDate(), r.EndDate(), rstb[r.StartDate() + ':' + r.EndDate()][2]+nominal, fwd_rt, se_rt, rstb[r.StartDate() + ':' + r.EndDate()][5]+provision)                                                    

    
        #=========================================================Create reset date dictionary and write to file========================
        if  ReportType == 'Prov_per_Reset':
            for k in reset_dict.keys():        
                resdte = reset_dict[k][0]
                nominal1m = CalculateBucket('1m', reset_dict[k][6], reset_dict[k][4])
                nominal3m = CalculateBucket('3m', reset_dict[k][6], reset_dict[k][4])
                nominal6m = CalculateBucket('6m', reset_dict[k][6], reset_dict[k][4])
                nominal9m = CalculateBucket('9m', reset_dict[k][6], reset_dict[k][4])
                nominal12m = CalculateBucket('12m', reset_dict[k][6], reset_dict[k][4])
                provision = reset_dict[k][10]
                TotalProv += provision        
                if resdte in reset_day_dict.keys():
                    reset_day_dict[resdte]['1m'] += nominal1m
                    reset_day_dict[resdte]['3m'] += nominal3m
                    reset_day_dict[resdte]['6m'] += nominal6m
                    reset_day_dict[resdte]['9m'] += nominal9m
                    reset_day_dict[resdte]['12m'] += nominal12m   
                    reset_day_dict[resdte]['Provision'] += provision            
            temp_list = []
            for k in reset_day_dict.keys():
                temp_list.append(k)
            temp_list.sort()        
            for t in temp_list:
                s = GenStrFromList('\t', t, reset_day_dict[t]['1m'], reset_day_dict[t]['3m'], reset_day_dict[t]['6m'], reset_day_dict[t]['9m'],  reset_day_dict[t]['12m'], reset_day_dict[t]['Provision'] )
                data_file2.write(s)            
            data_file1.close()
            data_file2.close()
            
        elif ReportType == 'Prov_per_ResetBucket':
            dtr = dt
            fdict = {}
            while dtr <= dte:
                found = 0
                dtm = dtr.add_months(3)
                dtm = dtm.add_banking_day(ael.Instrument['ZAR'], 0)
                for k in rstb.keys():
                    if ael.date(rstb[k][0]) == dtr:
                        fdict[k] = rstb[k]
                        found = 1
                if found == 0:
                    fwd_rt = crv.IrCurveInformation().Rate(dtr, dtm, 'Quarterly', dc, 'Forward Rate', None, 0)        
                    se_rt = lin_interp(mkt_dte['ZAR'], mkt_rt['ZAR'], ael.date(dtr)) / 100
                    dtr_s = str(dtr)[6:10] + '-' + str(dtr)[3:5] + '-' + str(dtr)[0:2]
                    dtm_s = str(dtm)[6:10] + '-' + str(dtm)[3:5] + '-' + str(dtm)[0:2]
                    fdict[dtr_s + ':' + dtm_s] = (dtr_s, dtm_s, 0, fwd_rt, se_rt, 0)           
                dtr = dtr.add_days(1)                
            slst = fdict.keys()
            slst.sort()        
            for l in slst: 
                TotalProv += int(fdict[l][5])
                s = GenStrFromList('\t', fdict[l][0], fdict[l][1], fdict[l][2], fdict[l][3], fdict[l][4], fdict[l][5])
                data_file1.write(s)  
            data_file1.close()        
        
        print 'Finished'
        return TotalProv    
    

 #=======================================================For Reset Risk Reports============================================================
    elif ReportType == 'Reset_Risk':    
        for t in trds_final2:
            ins = t.Instrument()  
            for l in ins.Legs(): 
                if l.LegType() == 'Float':
                    if l.Currency().Name() == Currency:                    
                    
                        #M.KLIMKE fwd_curve = l.MappedForwardCurve().Parameter().Name()
                        if 'FYCAttribute' in str(l.MappedForwardLink().Link().YieldCurveComponent().Class()):
                            fwd_curve = l.MappedForwardLink().Link().YieldCurveComponent().Curve().Name()
                        else:
                            fwd_curve = l.MappedForwardLink().Link().YieldCurveComponent().Name()
                        if fwd_curve == FwdCurve:
                            for cf in l.CashFlows():
                                for r in cf.Resets():
                                    if r <> None and l.FloatRateReference() <> None:
                                        if r.ResetType() in ('Single', 'Compound', 'Weighted'):                        
                                            if ael.date(r.Day()) >= dt and ael.date(r.Day()) <= dte:                                           
                                                
                                                reset_period = ael.date(r.StartDate()).years_between(ael.date(r.EndDate()))
                                                sign = DetermineSign(l.PayLeg())
                                                nominal = cf.Calculation().Nominal(CalcSpace.calcSpace, t).Number()
                                                                                                                     
                                                reset_lst = [r.Day(), r.StartDate(), r.EndDate(), l.FloatRateReference().Name(), nominal, l.Currency().Name(), reset_period]                                            
                                                reset_dict[r.Oid(), t.Oid()]= reset_lst                     
                                                if reset_dict[r.Oid(), t.Oid()][0] in reset_day_dict.keys():
                                                    pass
                                                else:
                                                    reset_day_dict[reset_dict[r.Oid(), t.Oid()][0]] = {'1m' : 0 , '3m' : 0, '6m' : 0 ,'9m' : 0 , '12m' : 0}                                 
                                                s = GenStrFromList('\t', t.Oid(), ins.InsType(), l.RollingPeriodCount(), l.RollingPeriodUnit(), r.ResetType(), r.Day(), r.StartDate(), r.EndDate(), l.FloatRateReference().Name(),  CalculateBucket('1m', reset_period, nominal), CalculateBucket('3m', reset_period, nominal), CalculateBucket('6m', reset_period, nominal), CalculateBucket('9m', reset_period, nominal), CalculateBucket('12m', reset_period, nominal), l.Currency().Name(), reset_period )                                      
                                                data_file1.write(s) 
 
        for k in reset_dict.keys():        
            resdte = reset_dict[k][0]
            nominal1m = CalculateBucket('1m', reset_dict[k][6], reset_dict[k][4])
            nominal3m = CalculateBucket('3m', reset_dict[k][6], reset_dict[k][4])
            nominal6m = CalculateBucket('6m', reset_dict[k][6], reset_dict[k][4])
            nominal9m = CalculateBucket('9m', reset_dict[k][6], reset_dict[k][4])
            nominal12m = CalculateBucket('12m', reset_dict[k][6], reset_dict[k][4])    
    
            if resdte in reset_day_dict.keys():
                reset_day_dict[resdte]['1m'] += nominal1m
                reset_day_dict[resdte]['3m'] += nominal3m
                reset_day_dict[resdte]['6m'] += nominal6m
                reset_day_dict[resdte]['9m'] += nominal9m
                reset_day_dict[resdte]['12m'] += nominal12m    
        
        temp_list = []
        for k in reset_day_dict.keys():
            temp_list.append(k)
        temp_list.sort()   
    
        for t in temp_list:
            s = GenStrFromList('\t', t, reset_day_dict[t]['1m'], reset_day_dict[t]['3m'], reset_day_dict[t]['6m'], reset_day_dict[t]['9m'],  reset_day_dict[t]['12m']  )
            data_file2.write(s)
                
         
        data_file1.close()
        data_file2.close()
    
        print 'Finished'
        return 'Risk Report'

#============================================================Main End===========================================================================================
 
 
def CalculateBucket(bucket, resterm, nominal):
    if bucket == '1m':
        if resterm < 0.2:
            return nominal
        else:
            return 0
    if bucket == '3m':
        if resterm >= 0.2 and resterm < 0.45:
            return nominal
        else:
            return 0
    if bucket == '6m':
        if resterm >= 0.45 and resterm < 0.7:
            return nominal
        else:
            return 0
    if bucket == '9m':
        if resterm >= 0.7 and resterm < 1:
            return nominal
        else:
            return 0
    if bucket == '12m':
        if resterm > 1:
            return nominal
        else:
            return 0
        
#=====================================================================================
 
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
 
 
 
#=====================================================================================
 
def DetermineSign(payleg):
    if payleg == 1:
        return -1
    if payleg == 0:
        return 1
 
#=====================================================================================
                                        
def FindBasisTrades(trade):
    
    flag = 0
    ins = trade.Instrument()
    ins_legs = ins.Legs()
  
    
    if len(ins_legs) >= 2:        
        for l in ins_legs:

            
            if l.LegType() == 'Float':
                flag = flag + 1
            else:
                flag = flag - 1            
                

        return flag
           
    else:

        return flag
        
    
#=====================================================================================


def PickUpMPC(TSspec_Name): 
    date_list = []    
    tsspec = acm.FTimeSeriesSpec[TSspec_Name]    
    ts = tsspec.TimeSeries()
    for t in ts:
        date_list.append(t.Day())    
    return date_list


#=====================================================================================

def get_next_mpc(dt, date_list):
    
    date_list.sort()
    for d in date_list:        
        if ael.date(d) > ael.date(dt):                   
            return d    
    return -1


#=====================================================================================

def SE_Curve(d1, mpc, ins_ccy):


    list_data = []
   
    d1 = ael.date(d1)
    mpc = ael.date(mpc)
    mkt_lst = []
    mkt_dte_lst = []
    mkt_rt_lst = []
    
    done_mpc = 0
     
    
    if ins_ccy == 'ZAR':
        ccy = ael.Instrument[ins_ccy]
        mkt_lst.append('ZAR-JIBAR-3M')
        mkt_dte_lst.append(d1)
        ins = ael.Instrument['ZAR-JIBAR-3M']
        mkt_rt_lst.append(ins.used_price()) 
    
        for k in range(1, 10):    
            ins = ael.Instrument['ZAR/FRA/JI/' + str(k) + 'X' + str(k+3)]
            dte = d1.add_months(k).adjust_to_banking_day(ccy)
            rt = ins.used_price()
            
            if ael.date(dte) > mpc and done_mpc == 0:
                mkt_lst.append('pre-mpc')
                mkt_dte_lst.append(mpc)
                mkt_rt_lst.append( ael.Instrument['ZAR/FRA/JI/PRE_MPC'].used_price())
                
                mkt_lst.append('post-mpc')        
                mkt_dte_lst.append(mpc.add_days(1).adjust_to_banking_day(ccy))
                mkt_rt_lst.append( ael.Instrument['ZAR/FRA/JI/POST_MPC'].used_price())
                
                done_mpc = -1
            
            mkt_lst.append(ins.insid)        
            mkt_dte_lst.append(dte)
            mkt_rt_lst.append(rt)
    
    
    
    if ins_ccy == 'USD':
        ccy = ael.Instrument[ins_ccy]
        mkt_lst.append('USD-LIBOR-3M')
        mkt_dte_lst.append(d1)
        ins = ael.Instrument['USD-LIBOR-3M']
        mkt_rt_lst.append(ins.used_price())
    
        for k in range(1, 10):    
            ins = ael.Instrument['USD/FRA/LI/' + str(k) + 'X' + str(k+3) ]
            dte = d1.add_months(k).adjust_to_banking_day(ccy)
            rt = ins.used_price()
            
            if ael.date(dte) > mpc and done_mpc == 0:
                mkt_lst.append('pre-mpc')        
                mkt_dte_lst.append(mpc)
                mkt_rt_lst.append( mkt_rt_lst[len(mkt_rt_lst)-1] )
                
                mkt_lst.append('post-mpc')        
                mkt_dte_lst.append(mpc.add_days(1))
                mkt_rt_lst.append(rt)
                
                done_mpc = -1
            
            mkt_lst.append(ins.insid)        
            mkt_dte_lst.append(dte)
            mkt_rt_lst.append(rt)



    list_data = [mkt_lst, mkt_dte_lst, mkt_rt_lst]
    return list_data
    
#=====================================================================================

def lin_interp(x, y, val):

    if val <= x[0]:
        return y[0]   

    for k in range(1, len(x)):
        if x[k] > val: 
            n = x[k-1].days_between(x[k]) * 1.0
            n1 = x[k-1].days_between(val) * 1.0
            n2 = n - n1        
            interp = n1/n * y[k] + n2/n * y[k-1] 
            return interp
    return y[ len(y)-1 ]

#=====================================================================================

def get_fx_rate(fccy):

    hccy = 'ZAR'

    curr_base = ael.Instrument[hccy] 
    curr = ael.Instrument[fccy]    

    dt = ael.date_today()

    d = 1.0/curr_base.used_price(dt, curr.insid)

    return d


#=====================================================================================


#Main('Portfolio','LTFX','Provision','F:\\temp\\provision_workings\\','ZAR')

