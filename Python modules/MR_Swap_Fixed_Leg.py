'''
Purpose                 :[Market Risk feed files],[Removed check as described by change 573640],[Amended EffectiveDATE,CouponRatePERD and CouponProratedFLAG for TRS]
                        [ValNotional changed to positive for certain instruments]
Department and Desk     :[IT],[Market Risk],[MR], [Market Risk]
Requester:              :[Natalie Austin],[Susan Kruger],[Susan Kruger], [Susan Kruger]
Developer               :[Douglas Finkel],[Willie van der Bank],[Willie van der Bank], [Bhavnisha Sarawan]
CR Number               :[264536,394236,573640],[749647],[838719 25/11/2011], [C147729]
FAU 912         Melusi Maseko           FA UPGRADE 2017 dev changes
'''


import ael, string, acm, PositionFile, MR_MainFunctions, datetime

InsL = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    outfile             =  open(filename, 'w')
    outfile.close()

    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################

def CashFlowStart(i):
    for l in i.legs():
        if len(l.cash_flows()) > 0:
            FirstCF = l.cash_flows()[0].start_day
    for l in i.legs():
        if len(l.cash_flows()) > 0:
            for cf in l.cash_flows():
                if cf.start_day < FirstCF:
                    FirstCF = cf.start_day
                    
    return FirstCF

# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    outfile = open(filename, 'a')
    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    
    ins = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()
    
    TotalReturnLeg_PayRec = 5
    TotalReturnSwap_Bond_IndexLinkedBond = 'false'
    TotalReturnLeg_Bond_IndexLinkedBond = 'false'
    if i.instype == 'TotalReturnSwap':
        for l in i.legs():
            if l.index_ref:
                if l.index_ref.instype in ('Bond', 'IndexLinkedBond'):
                    TotalReturnSwap_Bond_IndexLinkedBond = 'true'
                    if l.type == 'Total Return':
                        TotalReturnLeg_PayRec = l.payleg
                        TotalReturnLeg_Bond_IndexLinkedBond = 'true'
        
    for l in i.legs():
        Dividend = 0
        CashFlow = 0

        if l.type in ('Fixed', 'Call Fixed'):
            for cf in l.cash_flows():
                if cf.type == 'Dividend':
                    Dividend = 1

            if Dividend != 1:
                if (l.cash_flows()):
                    if (str(i.insaddr) + '_' + str(l.legnbr)) not in InsL:
                        InsL.append(str(i.insaddr) + '_' + str(l.legnbr))
                        
                        #Base record    
                        BASFLAG             =       'BAS'
                        HeaderName          =       'Swap Fixed Leg'
                        OBJECT              =       'Swap Fixed LegSPEC'
                        TYPE                =       'Swap Fixed Leg'

                        NAME                =       MR_MainFunctions.NameFix(i.insid)+'_Fixed'
                        IDENTIFIER          =       'insaddr_'+str(i.insaddr)+'_'+str(l.legnbr)
                
                        CurrencyCAL         =       ''
                        CurrencyDAYC        =       ''
                        CurrencyPERD        =       ''
                        CurrencyUNIT        =       l.curr.insid

                        NotionlAtStartFLAG  =       ''
                        NotionalAtEndFLAG   =       ''

                        # 573640 - Douglas Finkel - Updated to check that leg start day matches todays date and sets it to yesterdays date

                        #CurrDayDate = datetime.date.today()
                        #CurrDay = MR_MainFunctions.Datefix(str(CurrDayDate))
                        #
                        #if CurrDay == MR_MainFunctions.Datefix(l.start_day):
                        #    PrevDayDate = CurrDayDate + datetime.timedelta(days=(-1))
                        #    PrevDay = MR_MainFunctions.Datefix(str(PrevDayDate))
                        #    EffectiveDATE       = PrevDay
                        #else:
                        EffectiveDATE       = MR_MainFunctions.Datefix(l.start_day)

                        CouponRateCAL       =       ''
                        
                        CouponRateDAYC      =       ''
                        CouponRateDAYC      =       MR_MainFunctions.DayCountFix(l.daycount_method)
                        CouponRatePERD      =       'simple'
                        CouponRateVAL       =       l.fixed_rate
                        
                        StateProcFUNC       =       '@cash flow generator'
                        
                        if l.rolling_period not in ('0d', '0m', '0y'):
                            TermNB = getattr(l, 'rolling_period.count')
                            TermUNIT = getattr(l, 'rolling_period.unit')
                        else:
                            TermNB = ''
                            TermUNIT = 'Maturity'
                        
                        TermCAL             =       ''

                        CouponGenENUM       =       'Backward'
                        FixedCouponDateNB   =       '' 

                        BusDayRuleRULE      =       ''
                        BusDayRuleBUSD      =       ''
                        BusDayRuleCONV      =       ''
                        BusDayRuleCAL       =       ''
                        
                        PaymntProcXREF          =       ''
                        InitialIndxLvlFUNC      =       ''
                        InitialIndxLvlUNIT      =       ''
                        InitialIndxLvlVAL       =       ''
                        InitialIndxLvlSTRG      =       ''
                        CouponProratedFLAG      =       ''
                        
                        if l.nominal_scaling and i.instype == 'TotalReturnSwap':
                            if l.type in ('Fixed', 'Call Fixed'):
                                EffectiveDATE       = MR_MainFunctions.Datefix(CashFlowStart(i))
                            if l.index_ref:
                                if l.index_ref.instype in ('EquityIndex', 'Stock'):
                                    InitialIndxLvlFUNC      = '@issue date level'
                                    PaymntProcXREF          = MR_MainFunctions.NameFix(str(l.index_ref.insid)) + '_PP'
                            else:
                                for Leg in i.legs():
                                    if l.legnbr != Leg.legnbr:
                                        if l.index_ref:
                                            PaymntProcXREF  = MR_MainFunctions.NameFix(str(l.index_ref.insid)) + '_PP'
                                            break
                        else:
                            InitialIndxLvlFUNC  =       ''
                            PaymntProcXREF      =       ''

                        if TotalReturnSwap_Bond_IndexLinkedBond == 'true':
                            CouponRatePERD      = MR_MainFunctions.RollingPeriodFix(l.rolling_period)
                            
                        if TotalReturnLeg_Bond_IndexLinkedBond == 'true':
                            if l.type == 'Fixed' and l.payleg == TotalReturnLeg_PayRec:
                                CouponProratedFLAG  = 'False'

                        try:
                            DiscountCurveXREF   =   ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
                        except:
                            DiscountCurveXREF   =   ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
                        
                        if l.initial_index_value == 0:
                            InitialIndxLvlVAL  = l.inf_base_value
                        else:
                            InitialIndxLvlVAL  = l.initial_index_value
                        
                        TheoModelXREF       =       'Swap Fixed Leg(Cashflows)'
                        MarketModelXREF     =       ''
                        FairValueModelXREF  =       ''
                        SettlementProcFUNC  =       ''
                        
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, NotionlAtStartFLAG, NotionalAtEndFLAG, EffectiveDATE, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, StateProcFUNC, TermNB, TermUNIT, TermCAL, CouponGenENUM, FixedCouponDateNB, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, PaymntProcXREF, DiscountCurveXREF, CouponProratedFLAG, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC))

                        # Roll Over Equity Swap Fixed Leg Coupon List

                        BASFLAG             =       'rm_ro'
                        HeaderName          =       'Swap Fixed Leg : Variable Notional'
                        ATTRIBUTE           =       'Variable Notional'
                        OBJECT              =       'Swap Fixed LegSPEC'
                        
                        for cf in l.cash_flows():
                            if cf.pay_day > ael.date_today():
                                VariabNotionalDATE  =       MR_MainFunctions.Datefix(cf.pay_day) 
                                VariabNotionalENUM  =       ''
                                VariabNotionalCAL   =       ''
                                VariabNotionalDAYC  =       ''
                                VariabNotionalPERD  =       ''
                                VariabNotionalUNIT  =       l.curr.insid

                                if i.instype == 'TotalReturnSwap':
                                    if VariabNotionalDATE <= EffectiveDATE:
                                        VariabNotionalDATE = ael.date(EffectiveDATE).add_days(1)
                                        
                                
                                    CashFlow = acm.FCashFlow[cf.cfwnbr]
                                    
                                    NominalFactor = CashFlow.Calculation().NominalFactor(calcSpace)
                                    if NominalFactor == 0:
                                        NominalFactor = 1
                                    
                                    if l.initial_index_value == 0:
                                        for leg in i.legs():
                                            if (l.legnbr != leg.legnbr):
                                                initialIndex  = leg.initial_index_value
                                    else:
                                        initialIndex = l.initial_index_value
                                    
                                    if l.index_ref:
                                        if l.index_ref.instype in ('Bond', 'IndexLinkedBond', 'PriceIndex'):
                                            VariabNotionalVAL = abs(cf.nominal_amount())
                                        elif l.index_ref and l.index_ref.quote_type == 'Per 100 Units':
                                            VariabNotionalVAL = ((cf.nominal_amount() / NominalFactor)*initialIndex) / 100
                                        else:
                                            VariabNotionalVAL = ((cf.nominal_amount() / NominalFactor)*initialIndex)
                                    else:
                                        VariabNotionalVAL = cf.nominal_amount()
                                else:
                                    VariabNotionalVAL = i.contr_size*cf.nominal_factor
                                
                                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, VariabNotionalDATE, VariabNotionalENUM, VariabNotionalCAL, VariabNotionalDAYC, VariabNotionalPERD, VariabNotionalUNIT, VariabNotionalVAL))
    outfile.close()

    return i.insid

# WRITE - FILE ######################################################################################################

#MR_IRS_FixedLeg
#MR_Equity_Swap_Fixed_Leg
