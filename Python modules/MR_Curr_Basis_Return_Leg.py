
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
2018-11-22     CHG1001083227    Market RisK        Andile Biyana      http://abcap-jira/browse/ABITFA-5619
2020-11-25     CHG0142194       Thando Mpalala     Andile Biyana      https://absa.atlassian.net/browse/CMRI-948
2021-02-11     CHG0151668       Thando Mpalala     Andile Biyana      https://absa.atlassian.net/browse/CMRI-948
'''

import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
CalZAR = ael.Calendar['ZAR Johannesburg']
defaultFixingDate = MR_MainFunctions.Datefix('1970-01-01')

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
    
    for l in ins.Legs():         
        if not l.IsLocked():
        
            if l.PayLeg == 'Yes':
                PayRecSign = -1
            else:
                PayRecSign = 1
        
            if (str(i.insaddr) + '_' + str(l.Oid())) not in InsL:
                InsL.append(str(i.insaddr) + '_' + str(l.Oid()))
                acmLeg = acm.FLeg[l.Oid()]                
                #Base record
                BASFLAG             =       'BAS'
                HeaderName          =       'Swap Post-determined Leg'
                OBJECT              =       'Swap Post-determined LegSPEC'
                TYPE                =       'Swap Post-determined Leg'
                calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                NAME            = (MR_MainFunctions.NameFix(i.insid) + '_Return')[0:50]
                IDENTIFIER      = 'insaddr_'+str(i.insaddr) + '_' + str(l.Oid()) + '_Return'
                
                IndxatnLagTermNB    =       ''
                IndxatnLagTermUNIT  =       ''

                    
                if abs(l.ResetDayOffset()) == 0:
                    IndxatnLagTermNB = ''
                    IndxatnLagTermUNIT = 'Maturity'
                else:
                    IndxatnLagTermNB = 0
                    IndxatnLagTermUNIT = 'Days'
                
                
                CurrencyCAL         =       ''
                CurrencyDAYC        =       ''
                CurrencyPERD        =       ''
                CurrencyUNIT        =       l.Currency().Name()

                NotionlAtStartFLAG  =       'TRUE'
                NotionalAtEndFLAG   =       'TRUE'

                EffectiveDATE       =	    MR_MainFunctions.Datefix(l.StartDate())

                SpreadCAL           =       ''
                SpreadDAYC          =       ''
                SpreadDAYC          =       MR_MainFunctions.DayCountFix(l.DayCountMethod())
                SpreadFUNC          =       ''
                SpreadPERD          =       'simple'
                SpreadUNIT          =       '%'
                SpreadVAL           =       '0'
                SpreadSTRG          =       ''
            
                CalendarAdjFLAG     =       'FALSE'

                CouponRateCAL       =       ''
                CouponRateDAYC      =       ''
                CouponRateDAYC      =       MR_MainFunctions.DayCountFix(l.DayCountMethod())
                CouponRatePERD      =       'simple'

                CouponRateVAL       =       '0'

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

                #if l.PayCalendar().Oid():
                #    Cal1    =       str(l.PayCalendar().Oid())[0:3]
                #else:
                #    Cal1    =       ''
                #
                #if l.Pay2Calendar().Oid():
                #    Cal2    =       str(l.Pay2Calendar.Oid())[0:3]
                #else:
                #    Cal2    =       ''

                #if l.Pay3Calendar().Oid:
                #    Cal3    =       str(l.Pay3Calendar.Oid())[0:3]                
                #else:
                #    Cal3    =       ''
                    
                #CAL = Cal1+Cal2+Cal3
                BusDayRuleCAL = 'CalZAR' #string.replace(CAL,'Target','Euribor')
                
                InitialIndxLvlVAL       =       ''
                InitialIndxLvlUNIT      =       ''
                InitialIndxLvlFUNC      =       ''
                InitialIndxLvlSTRG      =       ''
                LastResetRateVAL        =       ''
                PaymntProcXREF          =       ''
                Locked  =       ''
                Reset =      ''

                for leg in i.legs():
                    if leg.is_locked:
                        Locked      = str(leg.curr.insid)
                    else:
                        Reset    = str(leg.curr.insid)

                if not l.IsLocked():
                    PaymntProcXREF      =       Locked + Reset + '_PP'
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
                
                PaymntProcXREF      =       Locked + Reset + '_PP'
                UndrCrvIndXREF      =       Locked + Reset + '_NI'
                
                try:
                    DiscountCurveXREF   =       acmLeg.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
                except:
                    DiscountCurveXREF   =       acmLeg.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()

                CouponProratedFLAG  =       ''
                CouponPrepayENUM    =       ''

                TheoModelXREF           = 'Swap Post-determined Leg(Prime)'
                MarketModelXREF     =       ''
                FairValueModelXREF  =       ''
                SettlementProcFUNC  =       ''
                RunSCFPhaseFLAG      =       'FALSE'
				
                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, EffectiveDATE, SpreadCAL, SpreadDAYC, SpreadFUNC, SpreadPERD, SpreadUNIT, SpreadVAL, SpreadSTRG, NotionlAtStartFLAG, NotionalAtEndFLAG, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, CalendarAdjFLAG, StateProcFUNC, TermNB, TermUNIT, TermCAL, CouponGenENUM, FixedCouponDateNB, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, IndxatnLagTermNB, IndxatnLagTermUNIT, PaymntProcXREF, UndrCrvIndXREF, DiscountCurveXREF, CouponProratedFLAG, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC, RunSCFPhaseFLAG))

                BASFLAG             =       'rm_ro'
                HeaderName          =       'Swap Post-determined Leg : Variable Notional'
                ATTRIBUTE           =       'Variable Notional'
                OBJECT              =       'Swap Post-determined LegSPEC'

                VariabNotionalDATE  =       MR_MainFunctions.Datefix(i.exp_day)
                VariabNotionalENUM  =       ''
                VariabNotionalCAL   =       ''
                VariabNotionalDAYC  =       ''
                VariabNotionalPERD  =       ''
                VariabNotionalUNIT  =       l.Currency().Name()
                VariabNotionalVAL   =       -1*i.contr_size*l.NominalFactor()
                
                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, VariabNotionalDATE, VariabNotionalENUM, VariabNotionalCAL, VariabNotionalDAYC, VariabNotionalPERD, VariabNotionalUNIT, VariabNotionalVAL))
				
                BASFLAG             =       'rm_ro'
                HeaderName          =       'Swap Post-determined Leg : Structured CashFlow'
                ATTRIBUTE           =       'Structured CashFlow'
                OBJECT              =       'Swap Post-determined LegSPEC'
	
                Flows = l.CashFlows()
		
                def getKey(FCashFlow):
                    return FCashFlow.PayDate()
			
                sFlows = sorted(Flows, key=getKey)
	
                cfCount = 1
	
                for cf in sFlows:
                
                    if cf.CashFlowType() == 'Return':
                        
                        #sets the reset days for Return payments in the past so that the last return payment can be generated for the final notional payment
                        cfCount = cfCount + 1 
                        rcount = 1

                        for R in cf.Resets():
                            if R.ResetType() == 'Return':
                            
                                #R.ReadTime()[0:10] = rdayX
                                if R.ReadTime()[0:10] > '1970-01-01':
                                    #rday1 = R.Day()
                                    if not l.NominalAtEnd():
                                        rdayX = R.Day()
                                    else:
                                        rdayX = R.ReadTime()[0:10]
                                else:
                                    rdayX = R.Day()
                                    
                                if rcount == 1:
                                    rday1 = rdayX
                                    #rday2 = R.Day()
                                    rcount = rcount + 1
                                        
                                else:
                                    #if (rday1 > R.Day()):
                                    if (rday1 > rdayX):
                                        rday2 = rday1
                                       #rday1 = R.Day()
                                        rday1 = rdayX
                                    else:
                                        #rday2 = R.Day()
                                        rday2 = rdayX
                
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
                        LastResetRateVAL    =       ''
                                                
                        if cf.CashFlowType() == 'Fixed Amount':
                            
                            if cfCount >1:
                                
                                rday1=rday2
                                rday2= cf.PayDate()
                                    
                                StrCfCoupFctrNB     =       '0'
                                StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.DayCountMethod())
                                StrCfCoupRatePERD   =       'simple'
                                StrCfCoupRateVAL    =       '0'
                            
                                StrCfCrvIndexXREF  =        UndrCrvIndXREF
                           
                                StrCfCurRateVAL     =       ''
                                StrCfDiscENUM       =       'In Fine'
                                StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(rday2)
                            
                                StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(rday1) #MR_MainFunctions.Datefix(str(cf.StartDate()))
                                StrCfHidOddCpFLAG   =       'FALSE'
                                StrCfInstrFctrVAL   =       '1'
                            
                                StrCfPayFctrVAL     =       '1'

                                StrCfInstrSprdVAL   =       '0'
                                StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.PayDate()))
                                StrCfPayTYPE        =       'Float'
                                StrCfPayUNIT        =       l.Currency().Name()    

                                #PayRecSign backs out the cashflow direction built into ael.CashFlow(...
                                #Pay and Receive is built into Synthetic instrument
                                
                                if l.NominalScaling() in ('FX'): 
                                    if cf.Calculation().NominalFactor(calcSpace) == 0:
                                        StrCfPayVAL     = 0
                                    else:
                                        StrCfPayVAL =  -1*i.contr_size * cf.NominalFactor()*l.NominalFactor()
                                        #StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() / cf.Calculation().NominalFactor(calcSpace) - NominalFactor(calcSpace) includes inflation, and amortisation schedule, new calculation does not back out amortisation schedule
                                else:
                                    StrCfPayVAL     = -1*PayRecSign *ael.CashFlow[cf.Oid()].nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                                    
                                if l.NominalScaling() in ('FX'): 
                                    #if l.nominal_scaling == 'CPI Fixing In Arrears':
                                    StrCfProcXREF         = Locked + Reset + '_PP'
                                    #else:
                                    #     StrCfProcXREF         = str(l.IndexRef().Name())+'_Start_PP'
                                else:
                                    StrCfProcXREF =  ''

                                StrCfProratedFLAG   =       'TRUE'
                                StrCfRealEndDATE    =       rday2
                                StrCfRealStartDATE  =       rday1
                                StrCfRstDateDATE    =       rday2

                                if StrCfPayVAL != 0.0:
                                    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))

                        elif cf.CashFlowType() == 'Return':
                            
                            StrCfCoupFctrNB     =       '0'
                            StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.DayCountMethod())
                            StrCfCoupRatePERD   =       'simple'
                            StrCfCoupRateVAL    =       '0'
                            
                            StrCfCrvIndexXREF  =        UndrCrvIndXREF
                           
                            StrCfCurRateVAL     =       ''
                            StrCfDiscENUM       =       'In Fine'
                            StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(rday2)                                      
                            StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(rday1) #MR_MainFunctions.Datefix(str(cf.StartDate()))
                            StrCfHidOddCpFLAG   =       'FALSE'
                            StrCfInstrFctrVAL   =       '1'
                            
                            StrCfPayFctrVAL     =       '1'

                            StrCfInstrSprdVAL   =       '0'
                            StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.PayDate()))
                            StrCfPayTYPE        =       'Float'
                            StrCfPayUNIT        =       l.Currency().Name()    

                            #PayRecSign backs out the cashflow direction built into ael.CashFlow(...
                            #Pay and Receive is built into Synthetic instrument
                            
                            if l.NominalScaling() in ('FX'): 
                                if cf.Calculation().NominalFactor(calcSpace) == 0:
                                    StrCfPayVAL     = 0
                                else:
                                    StrCfPayVAL = -1*i.contr_size * cf.NominalFactor()*l.NominalFactor()
                                    #StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() / cf.Calculation().NominalFactor(calcSpace) - NominalFactor(calcSpace) includes inflation, and amortisation schedule, new calculation does not back out amortisation schedule
                            else:
                                StrCfPayVAL     = -1*PayRecSign * ael.CashFlow[cf.Oid()].nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                                
                            if l.NominalScaling() in ('FX'): 
                                #if l.nominal_scaling == 'CPI Fixing In Arrears':
                                if (MR_MainFunctions.Datefix(str(R.Day())) < MR_MainFunctions.Datefix(l.StartDate())) and (MR_MainFunctions.Datefix(l.StartDate())== MR_MainFunctions.Datefix(cf.StartDate())):                              
                                    today = MR_MainFunctions.Datefix(acm.Time().DateToday())
                                    tradeDate = MR_MainFunctions.Datefix(acm.FInstrument[i.insid].Trades()[0].TradeTime()[0:10])  
                                    legStartDate = MR_MainFunctions.Datefix(l.StartDate())
                                    resetFixingDate = MR_MainFunctions.Datefix(R.ReadTime()[0:10])
                                    if (resetFixingDate > defaultFixingDate) and (today > tradeDate and today < legStartDate):
                                        print  acm.FInstrument[i.insid].Name(), ", ", MR_MainFunctions.Datefix(R.Day()), ", ", resetFixingDate, ", ", defaultFixingDate, ",", l.StartDate(), ", ", today, ", ", tradeDate
                                        StrCfProcXREF =  ''
                                    else:
                                        StrCfProcXREF         = Locked + Reset + '_PP'
                                else:
                                    StrCfProcXREF         = Locked + Reset + '_PP'
                            else:
                                StrCfProcXREF =  ''

                            StrCfProratedFLAG   =       'TRUE'
                            StrCfRealEndDATE    =       rday2
                            StrCfRealStartDATE  =       rday1
                            StrCfRstDateDATE    =       rday2

                            if StrCfPayVAL != 0.0:
                        
                                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))

				
    outfile.close()

    return i.insid

# WRITE - FILE ######################################################################################################

#MR_Crs_Cur_Basis_Swap_Float

