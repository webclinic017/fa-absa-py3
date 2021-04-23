
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536

-- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-01-20     CHNG0003565354   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-424
2018-08-22     CHG1000738329    Market RisK        Andile Biyana      http://abcap-jira/browse/ABITFA-5491
2018-11-22     CHG1001083227    Market RisK        Andile Biyana      http://abcap-jira/browse/ABITFA-5619
'''

import ael, string, acm, PositionFile, MR_MainFunctions
from FBDPCommon import acm_to_ael

InsL = []
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def get_StrCfCrvIndexXREF(l, cf):
    StrCfCrvIndexXREF  = ''
    float_rate = str(l.FloatRateReference().Name())
    cfspread = str(cf.Spread())
    rtype = str(l.ResetType())
    lrp = str(l.ResetPeriod())
    periodcount = str(l.ResetPeriodCount())
    periodunit  = str(l.ResetPeriodUnit())
    dayoffset   = str(l.ResetDayOffset())
    daymethod   = str(l.ResetDayMethod())

    if l.FloatRateReference():
        float_rate = str(l.FloatRateReference().Name())
        if cfspread != 0 and rtype == 'Compound':
            StrCfCrvIndexXREF = 'SCI_' + float_rate + '_' + rtype + '_' + periodcount + periodunit + '_' + dayoffset + daymethod+MR_MainFunctions.CompoundConvention(cfspread, rtype, lrp)
        else:
            StrCfCrvIndexXREF = 'SCI_' + float_rate + '_' + rtype + '_' + periodcount + periodunit + '_' + dayoffset + daymethod+MR_MainFunctions.CompoundConvention(cfspread, rtype, lrp)
    return StrCfCrvIndexXREF

def get_StrCfCoupRatePERD(l, cf):
    result  = ''
    float_rate = str(l.FloatRateReference().Name())
    cfspread = str(cf.Spread())
    rtype = str(l.ResetType())
    lrp = str(l.ResetPeriod())

    if float_rate:
        float_rate = str(l.FloatRateReference().Name())
        if cfspread != 0 and rtype == 'Compound':
            result = MR_MainFunctions.DatePeriodUnit(lrp)
        else:
            result = 'simple'

    return result

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    outfile             =  open(filename, 'w')
    outfile.close()

    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################

# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename

    outfile = open(filename, 'a')

    ins = acm.FInstrument[i.insaddr]
    LocalCAL = acm.FCalendar['ZAR Johannesburg'].Name()[0:3]

    for l in ins.Legs(): 
        if l.LegType() in ('Fixed', 'Call Fixed'):

            if l.PayLeg():
                PayRecSign = -1
            else:
                PayRecSign = 1

            if (str(i.insaddr) + '_' + str(l.Oid())) not in InsL:
                InsL.append(str(i.insaddr) + '_' + str(l.Oid()))
                acmLeg = acm.FLeg[l.Oid()]
                #Base record
                BASFLAG             =       'BAS'
                HeaderName          =       'Basis Swap Fixed Leg'
                OBJECT              =       'Swap Fixed LegSPEC'
                TYPE                =       'Swap Fixed Leg'
                IndxatnLagTermNB    =       ''
                IndxatnLagTermUNIT  =       ''
                calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()

                if l.IsLocked():
                    NAME = (MR_MainFunctions.NameFix(i.insid)+'_Locked')[0:50]
                else:
                    NAME = (MR_MainFunctions.NameFix(i.insid)+'_Reset')[0:50]
                    
                    if abs(l.ResetDayOffset()) == 0:
                        IndxatnLagTermNB = ''
                        IndxatnLagTermUNIT = 'Maturity'
                    else:
                        IndxatnLagTermNB = 0
                        IndxatnLagTermUNIT = 'Days'

                IDENTIFIER          =       'insaddr_'+str(i.insaddr) + '_' + str(l.Oid())
                CurrencyCAL         =       ''
                CurrencyDAYC        =       ''
                CurrencyPERD        =       ''
                CurrencyUNIT        =       l.Currency().Name()
                NotionlAtStartFLAG  =       'TRUE'
                NotionalAtEndFLAG   =       'TRUE'
                EffectiveDATE       =	    MR_MainFunctions.Datefix(l.StartDate())
                CouponRateCAL       =       ''
                CouponRateDAYC      =       ''
                CouponRateDAYC      =       MR_MainFunctions.DayCountFix(l.DayCountMethod())
                CouponRatePERD      =       'simple'
                CouponRateVAL       =       l.FixedRate()
                StateProcFUNC       =       '@cash flow generator'

                if l.RollingPeriod() not in ('0d', '0m', '0y'):
                    TermNB = l.RollingPeriodCount()
                    TermUNIT = l.RollingPeriodUnit()
                else:
                    TermNB = ''
                    TermUNIT = 'Maturity'

                BusDayRuleRULE      =   MR_MainFunctions.BusRule(l.PayDayMethod())
                BusDayRuleCONV      =   MR_MainFunctions.BusConv(l.PayDayMethod())
                TermCAL                 =       ''
                CouponGenENUM           =       ''
                FixedCouponDateNB       =       ''
                ounit = string.replace(str(l.PayOffsetUnit()), 'Days', 'd')
                ounit = string.replace(ounit, 'Weeks', 'w')
                ounit = string.replace(ounit, 'Months', 'm')
                ounit = string.replace(ounit, 'Years', 'y')
                BusDayRuleBUSD          =       MR_MainFunctions.CurveDays(str(l.PayOffsetCount()) + ounit)
                BusDayRuleCAL = 'Cal'+LocalCAL
                InitialIndxLvlVAL       =       ''
                InitialIndxLvlUNIT      =       ''
                InitialIndxLvlFUNC      =       ''
                InitialIndxLvlSTRG      =       ''
                PaymntProcXREF          =       ''
                InitialStrCfProcXREF    =       ''
                Locked  =       ''
                Reset =      ''
                NDS = 'No'

                for leg in i.legs():
                    if leg.is_locked:
                        Locked      = str(leg.curr.insid)
                    else:
                        Reset    = str(leg.curr.insid)

                isScaling = 1

                if (not leg.nominal_at_end) and (not leg.nominal_at_start):
                    isScaling = 0

                if i.non_deliverable:

                    NDS = 'Yes'

                    if (l.OriginalCurr().Name() != i.curr.insid):
                        for fl in i.legs():
                            if fl.nominal_factor <> 1:
                                if fl.legnbr == l.Oid():
                                    InitialIndxLvlVAL = 1/fl.nominal_factor
                                else:
                                    InitialIndxLvlVAL = fl.nominal_factor
                        
                            if (fl.original_curr.insid == i.curr.insid):
                                ScalingFactor = fl.nominal_factor

                        InitialStrCfProcXREF = l.OriginalCurr().Name() + i.curr.insid + '_PP_End'

                        if abs(l.ResetDayOffset()) == 0:
                            IndxatnLagTermNB = ''
                            IndxatnLagTermUNIT = 'Maturity'
                        else:
                            IndxatnLagTermNB = 0
                            IndxatnLagTermUNIT = 'Days'
                    else:
                        NDS = 'No'
                        InitialIndxLvlVAL = '0'
                else:
                    NDS = 'No'
                    InitialIndxLvlVAL = '0'

                    if not l.IsLocked():
                        InitialStrCfProcXREF      =       Locked + Reset + '_PP'
                        if l.InitialIndexValue() == 0:
                            InitialIndxLvlVAL  = 0
                            for leg in i.legs():
                                if (l.Oid() != leg.legnbr):
                                    if leg.initial_index_value != 0:
                                        InitialIndxLvlVAL  = 1/leg.initial_index_value
                                    else:
                                        InitialIndxLvlVAL  = 0
                        else:
                            InitialIndxLvlVAL  = l.InitialIndexValue()

                try:
                    DiscountCurveXREF   =       acmLeg.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
                except:
                    DiscountCurveXREF   =       acmLeg.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()

                CouponProratedFLAG  =       ''
                TheoModelXREF       =       'Swap Fixed Leg(Cashflows)'
                MarketModelXREF     =       ''
                FairValueModelXREF  =       ''
                SettlementProcFUNC  =       ''
                RunSCFPhaseFLAG      =       'FALSE'

                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, NotionlAtStartFLAG, NotionalAtEndFLAG, EffectiveDATE, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, StateProcFUNC, TermNB, TermUNIT, TermCAL, CouponGenENUM, FixedCouponDateNB, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, IndxatnLagTermNB, IndxatnLagTermUNIT, InitialStrCfProcXREF, DiscountCurveXREF, CouponProratedFLAG, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC, RunSCFPhaseFLAG))

                BASFLAG             =       'rm_ro'
                HeaderName          =       'Basis Swap Fixed Leg : Variable Notional'
                ATTRIBUTE           =       'Variable Notional'
                OBJECT              =       'Swap Fixed LegSPEC'
                VariabNotionalDATE  =       MR_MainFunctions.Datefix(i.exp_day)
                VariabNotionalENUM  =       ''
                VariabNotionalCAL   =       ''
                VariabNotionalDAYC  =       ''
                VariabNotionalPERD  =       ''
                VariabNotionalUNIT  =       l.Currency().Name()
                VariabNotionalVAL   =       i.contr_size*l.NominalFactor()
                
                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, VariabNotionalDATE, VariabNotionalENUM, VariabNotionalCAL, VariabNotionalDAYC, VariabNotionalPERD, VariabNotionalUNIT, VariabNotionalVAL))

                BASFLAG             =       'rm_ro'
                HeaderName          =       'Basis Swap Fixed Leg : Structured CashFlow'
                ATTRIBUTE           =       'Structured CashFlow'
                OBJECT              =       'Swap Fixed LegSPEC'

                FACount = 0

                Flows = l.CashFlows()

                def getKey(FCashFlow):
                    return FCashFlow.PayDate()

                sFlows = sorted(Flows, key=getKey)

                for cf in sFlows:

                    if cf.CashFlowType() == 'Fixed Amount':
                        FACount = FACount + 1
                            
                    if MR_MainFunctions.Datefix(cf.PayDate()) > (MR_MainFunctions.Datefix(acm.Time().DateToday())) and MR_MainFunctions.Datefix(cf.PayDate()) != '':
                        StrCfCapMatDATE     =       ''
                        StrCfCoupFctrNB     =       ''
                        StrCfCoupRateCAL    =       ''
                        StrCfCoupRateDAYC   =       ''
                        StrCfCoupRatePERD   =       ''
                        StrCfCoupRateVAL    =       ''
                        StrCfCrvIndexXREF   =       ''
                        StrCfCurRateVAL     =       ''
                        StrCfDiscENUM       =       ''
                        StrCfFwdEndDATE     =       ''
                        StrCfFwdStartDATE   =       ''
                        StrCfHidOddCpFLAG   =       ''
                        StrCfInstrFctrVAL   =       ''
                        StrCfInstrSprdVAL   =       ''
                        StrCfPayCAL         =       ''
                        StrCfPayDATE        =       ''
                        StrCfPayDAYC        =       ''
                        StrCfPayFctrVAL     =       ''
                        StrCfPayPERD        =       ''
                        StrCfPayTYPE        =       ''
                        StrCfPayUNIT        =       ''
                        StrCfPayVAL         =       ''
                        StrCfProcXREF       =       ''
                        StrCfProratedFLAG   =       ''
                        StrCfRealEndDATE    =       ''
                        StrCfRealStartDATE  =       ''
                        StrCfRstDateDATE    =       ''
                        StrCfTheoEndDATE    =       ''
                        StrCfTheoStartDATE  =       ''

                        if cf.CashFlowType() == 'Fixed Amount':
                            if cf.Resets(): 
                                for R in cf.Resets():
                                    if cf.PayDate() <> R.Day():
                                        StrCfCoupFctrNB     =       '1'
                                        StrCfCoupRateCAL    =       ''
                                        StrCfCoupRateDAYC   =       ''
                                        StrCfCoupRatePERD   =       ''
                                        StrCfCoupRateVAL    =       ''
                                        StrCfHidOddCpFLAG   =       ''
                                        StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.PayDate()))
                                        StrCfPayTYPE        =       'Notional'
                                        StrCfPayUNIT        =       l.Currency().Name()
                                        StrCfProcXREF   = '' 

                                        FXScaling = 0
                                        if i.non_deliverable:
                                            for r in cf.Resets():
                                                if r.ResetType() == 'Settlement FX':
                                                    FXScaling = 1
                                                    
                                            if FXScaling:
                                                StrCfProcXREF = InitialStrCfProcXREF
                                                StrCfPayVAL = PayRecSign * i.contr_size * cf.FixedAmount() * ScalingFactor
                                            else:
                                                StrCfPayVAL         =      PayRecSign * acm_to_ael(cf).nominal_amount()
                                        else:                                               
                                            if ((not l.IsLocked()) and isScaling):
                                                if ((MR_MainFunctions.Datefix(str(R.Day())) <= MR_MainFunctions.Datefix(acm.Time().DateToday())) and (FACount==1)):
                                                    StrCfPayVAL     = PayRecSign * acm_to_ael(cf).nominal_amount()
                                                else:
                                                    StrCfProcXREF       = Locked + Reset + '_PP'
                                                    if cf.Calculation().NominalFactor(calcSpace) == 0:
                                                        StrCfPayVAL     = 0
                                                    else:
                                                        StrCfPayVAL = i.contr_size * cf.FixedAmount() * l.NominalFactor()
                                                       
                                            else:
                                                StrCfPayVAL     = PayRecSign * acm_to_ael(cf).nominal_amount()
                                                StrCfProcXREF =  ''
 
                                        StrCfProratedFLAG   =       'FALSE'
                                    else:
                                        StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.PayDate()))
                                        StrCfPayTYPE        =       'Notional'
                                        StrCfPayUNIT        =       l.Currency().Name()
                                        
                                        FXScaling = 0
                                        if i.non_deliverable:
                                            for r in cf.Resets():
                                                if r.ReseType() == 'Settlement FX':
                                                    FXScaling = 1
                                                
                                            if FXScaling:
                                                StrCfProcXREF = InitialStrCfProcXREF
                                                StrCfPayVAL = PayRecSign * i.contr_size * cf.FixedAmount() * ScalingFactor
                                            else:
                                                StrCfPayVAL         =       PayRecSign * acm_to_ael(cf).nominal_amount()
                                        else:
                                            if ((not l.IsLocked()) and isScaling):
                                                StrCfProcXREF         = Locked + Reset + '_PP'
                                                if cf.Calculation().NominalFactor(calcSpace) == 0:
                                                    StrCfPayVAL     = 0
                                                else:
                                                    StrCfPayVAL = i.contr_size * cf.FixedAmount() * l.NominalFactor()
                                            else:
                                                StrCfPayVAL     = PayRecSign * acm_to_ael(cf).nominal_amount() 
                                                StrCfProcXREF =  ''
                            else:
                                StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.PayDate()))
                                StrCfPayTYPE        =       'Notional'
                                StrCfPayUNIT        =       l.Currency().Name()
                                StrCfProcXREF =  ''
                                FXScaling = 0

                                if i.non_deliverable:
                                    for r in cf.Resets():
                                        if r.ResetType() == 'Settlement FX':
                                            FXScaling = 1
                                            
                                    if FXScaling == 1:
                                        StrCfProcXREF = InitialStrCfProcXREF
                                        StrCfPayVAL = PayRecSign * i.contr_size * cf.FixedAmount() * ScalingFactor
                                    else:
                                        StrCfPayVAL         =       PayRecSign * acm_to_ael(cf).nominal_amount()
                                else:
                                    if ((not l.IsLocked()) and isScaling):
                                        StrCfProcXREF         = Locked + Reset + '_PP'
                                        if cf.Calculation().NominalFactor(calcSpace) == 0:
                                            StrCfPayVAL     = 0
                                        else:
                                            StrCfPayVAL = i.contr_size * cf.FixedAmount() * l.NominalFactor()
                                    else:
                                        StrCfPayVAL     = PayRecSign * acm_to_ael(cf).nominal_amount()
                                        StrCfProcXREF =  ''

                            if StrCfPayVAL != 0.0:
                                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))

                        elif cf.CashFlowType() in('Fixed Rate', 'Call Fixed Rate'):
                            StrCfCoupFctrNB     =       '0'
                            StrCfCoupRateCAL    =       ''
                            StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.DayCountMethod())
                            StrCfCoupRatePERD   =       'simple'
                            StrCfCoupRateVAL    =       str(cf.FixedRate())
                            StrCfHidOddCpFLAG   =       'FALSE'
                            StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.PayDate()))
                            StrCfPayTYPE        =       'Fixed'
                            StrCfPayUNIT        =       l.Currency().Name()
                            StrCfProcXREF   = '' 
                            FXScaling = 0

                            if i.non_deliverable:
                                for r in cf.Resets():
                                    if r.ResetType() == 'Settlement FX':
                                        FXScaling = 1
                                        
                                if FXScaling:
                                    StrCfProcXREF = InitialStrCfProcXREF
                                    StrCfPayVAL = PayRecSign * i.contr_size * cf.NominalFactor() * ScalingFactor
                                else:
                                    StrCfPayVAL         =       PayRecSign * acm_to_ael(cf).nominal_amount() 
                            else:
                                if ((not l.IsLocked()) and isScaling): 
                                    StrCfProcXREF       = Locked + Reset + '_PP'
                                    if cf.Calculation().NominalFactor(calcSpace) == 0:
                                        StrCfPayVAL     = 0
                                    else:
                                        StrCfPayVAL =  i.contr_size * l.NominalFactor()
                                else:
                                    StrCfPayVAL     = PayRecSign * acm_to_ael(cf).nominal_amount()
                                    StrCfProcXREF =  ''

                            StrCfProratedFLAG   =       'TRUE'
                            StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.EndDate()))
                            StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.StartDate()))

                            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))

    outfile.close()

    return i.insid

# WRITE - FILE ######################################################################################################

#MR_Crs_Cur_Basis_Swap_Float
