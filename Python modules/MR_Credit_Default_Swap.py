'''
Purpose                 :[Market Risk feed files], [Amended PercentLossVAL]
Department and Desk     :[IT], [Makret Risk]
Requester:              :[Natalie Austin], [Susan Kruger]
Developer               :[Douglas Finkel], [Willie van der Bank]
CR Number               :[264536, 707888], [790080 07/10/2011]
'''

import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []

# OPENFILE ##########################################################################################################

def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    outfile             =  open(filename, 'w')
    outfileP            =  open(PositionFilename, 'w')
    
    outfile.close()
    outfileP.close()

    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    ins = acm.FInstrument[i.insaddr]
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        
        outfile = open(filename, 'a')
        
        #Base record
        
        BASFLAG             =       'BAS'
        HeaderName          =       'Default Swap'
        OBJECT              =       'Default SwapSPEC'
        TYPE                =       'Default Swap'
        
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
     
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       i.curr.insid
        
        MaturityDATE        =       MR_MainFunctions.Datefix(i.exp_day)
        ReferenceAssetXREF  =       'insaddr_'+str(ins.CreditReference().Oid())
        
        datelist = []
        r = getattr(i, 'recovery_rate')
        PercentLossVAL      =       1 - r()
        
        for l in i.legs():
            if l.digital == 1:

                #This is the generic instrument created specifically for MR, for the use of digital CDS - insid MarketRiskGenericBond
                ReferenceAssetXREF  =       'insaddr_'+str(1361321)
                #PercentLossVAL  =       1
                PercentLossVAL  =       str(l.digital_payoff / 100)
            
            if MR_MainFunctions.Datefix(l.start_day) not in datelist:
                datelist.append(MR_MainFunctions.Datefix(l.start_day))
        datelist.sort()
        EffectiveDATE = datelist[0]
        
        LegalEntityXREF     =       ''
        if i.issuer_ptynbr:
            LegalEntityXREF     =       'ptynbr_' + str(i.issuer_ptynbr.ptynbr)
        
        CouponRateCAL       =       ''
        CouponRateDAYC      =       ''
        CouponRatePERD      =       'simple'
        CouponRateVAL       =       '0'
        UndrCrvIndXREF      =       ''
                
        #Take from Fixed Leg only
        Legs = i.legs()
        for l in Legs:
            if l.type in ('Fixed', 'Call Fixed'):
                CouponRateVAL       =       l.fixed_rate
                CouponRateDAYC      =       MR_MainFunctions.DayCountFix(l.daycount_method)      
            elif l.type == ('Float'):
                for r in l.resets():
                    if r.start_day <= ael.date_today() and r.end_day >= ael.date_today():
                        CouponRateVAL       =       l.spread + r.value
			CouponRateDAYC      =       MR_MainFunctions.DayCountFix(l.daycount_method)
                float_rate = getattr(l, 'float_rate')
                if float_rate:
                    output = float_rate.insid
                    UndrCrvIndXREF 	=	'SCI_' + output + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
                else:
                    UndrCrvIndXREF = 'None'
        
        DfltProtectionENUM = 'Receive Default Protection'
        
        for l in i.legs():
            if l.payleg: 
                if l.type == 'Credit Default':
                    DfltProtectionENUM  = 'Provide Default Protection'
                else: 
                    DfltProtectionENUM  = 'Receive Default Protection'
                
        PremiumTypeENUM     =       'Rolling Premium'
        '''
        for l in i.legs():
            if l.type <> 'Credit Default':
                if getattr(l,'rolling_period.count') == 0:
                    PremiumTypeENUM = 'Rolling Premium'
                else:
                    PremiumTypeENUM = 'Initial Premium'
        '''
        PremiumSchedXREF    =       ''
        InitialPremiumVAL   =       '' #trade.Premium()
        
        StateProcFUNC       =       '@default swap'
        
        CouponGenENUM   =       'Backward'
        TermNB          =       ''
        TermUNIT        =       ''
        for l in i.legs():
            if l.type in ('Fixed', 'Call Fixed', 'Float'):
                if getattr(l, 'rolling_period') == '0d':
                    TermNB   = ''
                    TermUNIT = 'Maturity'
                else:
                    TermNB   = getattr(l, 'rolling_period.count')
                    TermUNIT = getattr(l, 'rolling_period.unit')
        
        TermCAL             =       ''
        BusDayRuleRULE      =       ''
        BusDayRuleBUSD      =       ''
        BusDayRuleCONV      =       ''
        BusDayRuleCAL       =       ''
        CouponProratedFLAG  =       ''
        
        try:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        CrdtSprdCurveXREF       =       ''
        
        cl = acm.FContextLink.Select('groupChlItem = ' + str(ins.ValuationGrpChlItem().Oid()) + ' and type = Core Valuation Function' )
        
        #HazardCurveXREF     =       cl[0].Name()
        
        try:
            HazardCurveXREF =       ins.Legs().First().CreditRef().Issuer().Name() + '_' + i.curr.insid + '_HazardCurve'
        except:
            HazardCurveXREF =       ''

        
        TheoModelXREF       =       'CDS Model'
        MarketModelXREF     =       ''
        FairValueModelXREF  =       ''
        SettlementProcFUNC  =       ''
	
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, MaturityDATE, EffectiveDATE, ReferenceAssetXREF, LegalEntityXREF, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, UndrCrvIndXREF, DfltProtectionENUM, PremiumTypeENUM, PremiumSchedXREF, InitialPremiumVAL, StateProcFUNC, PercentLossVAL, CouponGenENUM, TermNB, TermUNIT, TermCAL, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, CouponProratedFLAG, DiscountCurveXREF, CrdtSprdCurveXREF, HazardCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC))
        
        # Roll Over Default Swap Variable Notional
        BASFLAG             =       'rm_ro'
        HeaderName          =       'Default Swap : Variable Notional'
        ATTRIBUTE           =       'Variable Notional'
        OBJECT              =       'Default SwapSPEC'
        
        Legs = i.legs()
        for LegNbr in Legs:
            if LegNbr.type <> 'Credit Default':
                if LegNbr.digital == 1:
                    for cf in LegNbr.cash_flows():
                        VariabNotionalDATE  =       MR_MainFunctions.Datefix(cf.pay_day)
                        VariabNotionalENUM  =       ''
                        VariabNotionalCAL   =       ''
                        VariabNotionalDAYC  =       ''
                        VariabNotionalPERD  =       ''      
                        VariabNotionalUNIT  =       i.curr.insid
                        VariabNotionalVAL   =       (i.contr_size*cf.nominal_factor*LegNbr.digital_payoff)/100
                        
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, VariabNotionalDATE, VariabNotionalENUM, VariabNotionalCAL, VariabNotionalDAYC, VariabNotionalPERD, VariabNotionalUNIT, VariabNotionalVAL))
                else:
                    for cf in LegNbr.cash_flows():
                        VariabNotionalDATE  =       MR_MainFunctions.Datefix(cf.pay_day)
                        VariabNotionalENUM  =       ''
                        VariabNotionalCAL   =       ''
                        VariabNotionalDAYC  =       ''
                        VariabNotionalPERD  =       ''      
                        VariabNotionalUNIT  =       i.curr.insid
                        VariabNotionalVAL   =       i.contr_size*cf.nominal_factor

                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, VariabNotionalDATE, VariabNotionalENUM, VariabNotionalCAL, VariabNotionalDAYC, VariabNotionalPERD, VariabNotionalUNIT, VariabNotionalVAL))
        
        outfile.close()
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################
