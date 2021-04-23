'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536,472409, 644358, 701575, 707888

Description             
Remove time zero cashflows from structured instruments

MINT-454 : Amended notional claculation rules. 
FAU-952    2017 UPGRADE - Ammended InitialIndxLvlVAL to use inf_base_value instead of initial_index_value

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''

import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []

def get_StrCfCrvIndexXREF(l, cf):
    StrCfCrvIndexXREF  = ''
    float_rate = str(l.FloatRateReference().Name())
    cfspread = cf.Spread()
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
    cfspread = cf.Spread()
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
    PositionFilename    = FileDir + PositionName
    
    outfile             =  open(filename, 'w')
    outfileP            =  open(PositionFilename, 'w')
    
    outfile.close()
    outfileP.close()
    
    del InsL[:]
    InsL[:] = []
    
    return filename

# OPENFILE ##########################################################################################################



# DATEFIX ##########################################################################################################
def Datefix(d, *rest):
    if d == None:
        return ''
    else:
        return ael.date_from_string(d).to_string('%Y/%m/%d')
# DATEFIX ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    
    ins = acm.FInstrument[i.insaddr]
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        
        outfile = open(filename, 'a')
        
        #Base record
        BASFLAG                 =       'BAS'
        HeaderName              =       'Inflation Structured Instrument'
        OBJECT                  =       'Structured InstrumentSPEC'
        TYPE                    =       'Structured Instrument'
        NAME                    =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER              =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL             =       ''
        CurrencyDAYC            =       ''
        CurrencyPERD            =       ''
        
        try:
            CurrencyUNIT        =       ins.Currency().Name()
        except:
            CurrencyUNIT        =       ''
        
        InitialIndxLvlUNIT      =       ''
        InitialIndxLvlVAL       =       ''
        InitialIndxLvlFUNC      =       ''
        EffectiveDATE           =       ''
        PaymentProcXREF         =       ''
        
        for l in i.legs():
            if l.inf_scal_ref:
                if l.start_day > ael.date_today():
                    InitialIndxLvlVAL       = ''
                    InitialIndxLvlFUNC      = '@issue date level'
                    EffectiveDATE           = Datefix(l.start_day)
                    PaymentProcXREF         = ''
                    
                    #if l.nominal_scaling == 'CPI Fixing In Arrears':
                    PaymentProcXREF         = str(l.inf_scal_ref.insid)+'_End_PP'
                    #elif l.nominal_scaling == 'CPI':
                    #     PaymentProcXREF         = str(l.index_ref.insid)+'_Start_PP'
                else:
                    InitialIndxLvlVAL       = l.inf_base_value
                    InitialIndxLvlFUNC      = ''
                    EffectiveDATE           = ''
                    PaymentProcXREF         = ''
        
        InitialIndxLvlSTRG      =       ''
        
        try:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        TheoModelXREF           =       'General Structured Instrument'
        MarketModelXREF         =       ''
        FairValueModelXREF      =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, DiscountCurveXREF, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, EffectiveDATE, PaymentProcXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
        
        # Roll Over Variable Notional

        BASFLAG	                =	'rm_ro'
        HeaderName              =       'Inflation Structured Instrument : Structured CashFlow'
        ATTRIBUTE	        =	'Structured CashFlow'
        OBJECT	                =	'Structured InstrumentSPEC'
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        ins  = acm.FInstrument[i.insaddr]
        
        for l in ins.Legs():
        
            if l.PayLeg == 'Yes':
                PayRecSign = -1
            else:
                PayRecSign = 1
        
            for cf in l.CashFlows():
                if Datefix(cf.PayDate()) > Datefix(acm.Time().DateToday()) and Datefix(cf.PayDate()) != '':
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
                        if cf.Resets(): #Test for Fixed Amount Cashflows where a reset date of the cashflow does not equal pay date of the cash flow
                            for R in cf.Resets():
                                if cf.PayDate() <> R.Day():
                                
                                    StrCfCoupFctrNB     =       '1'
                                    StrCfCoupRateCAL    =       ''
                                    StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.DayCountMethod())
                                    StrCfCoupRatePERD   =       'simple'
                                    StrCfCoupRateVAL    =       '100'
                                    StrCfHidOddCpFLAG   =       'FALSE'
                                    
                                    StrCfPayDATE        =       Datefix(str(cf.PayDate()))
                                    StrCfPayTYPE        =       'Fixed'
                                    StrCfPayUNIT        =       l.Currency().Name()         
                                    
                                    if l.InflationScalingRef():
                                        if cf.Calculation().NominalFactor(calcSpace) == 0:
                                            StrCfPayVAL     = 0
                                        else:
                                            StrCfPayVAL = PayRecSign * i.contr_size * cf.FixedAmount()
                                            #StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() / cf.Calculation().NominalFactor(calcSpace) - NominalFactor(calcSpace) includes inflation, and amortisation schedule, new calculation does not back out amortisation schedule
                                    else:
                                        StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor

                                    StrCfProcXREF   = '' 
                                    if l.InflationScalingRef():
                                        StrCfProcXREF       = str(l.InflationScalingRef().Name()) + '_Start_PP'
                                        StrCfRealEndDATE    =       Datefix(str('3000-12-31'))
                                        StrCfRealStartDATE  =       Datefix(str(R.Day()))
                                    else:
                                        StrCfProcXREF =  ''
                                        StrCfRealEndDATE    =       Datefix(str(cf.EndDate()))
                                        StrCfRealStartDATE  =       Datefix(str(cf.StartDate()))

                                    StrCfProratedFLAG   =       'FALSE'
                                    
                                else:
                                    StrCfPayDATE        =       Datefix(str(cf.PayDate()))
                                    StrCfPayTYPE        =       'Notional'
                                    StrCfPayUNIT        =       l.Currency().Name()
                                    
                                    if l.InflationScalingRef():
                                        if cf.Calculation().NominalFactor(calcSpace) == 0:
                                            StrCfPayVAL     = 0
                                        else:
                                            StrCfPayVAL = PayRecSign * i.contr_size * cf.FixedAmount()
                                            #StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() / cf.Calculation().NominalFactor(calcSpace) - NominalFactor(calcSpace) includes inflation, and amortisation schedule, new calculation does not back out amortisation schedule
                                    else:
                                        StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor

                                    StrCfProcXREF   = '' 
                                    if l.InflationScalingRef(): 
                                        #if l.NominalScaling() == 'CPI Fixing In Arrears':
                                        StrCfProcXREF         = str(l.InflationScalingRef().Name())+'_End_PP'
                                        #elif l.NominalScaling() == 'CPI':
                                        #    StrCfProcXREF         = str(l.IndexRef().Name())+'_Start_PP'
                                    else:
                                        StrCfProcXREF =  ''
                                        
                        else:
                            StrCfPayDATE        =       Datefix(str(cf.PayDate()))
                            StrCfPayTYPE        =       'Notional'
                            StrCfPayUNIT        =       l.Currency().Name()
                            
                            if l.InflationScalingRef():
                                if cf.Calculation().NominalFactor(calcSpace) == 0:
                                    StrCfPayVAL     = 0
                                else:
                                    StrCfPayVAL = PayRecSign * i.contr_size * cf.FixedAmount()
                                    #StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() / cf.Calculation().NominalFactor(calcSpace) - NominalFactor(calcSpace) includes inflation, and amortisation schedule, new calculation does not back out amortisation schedule
                            else:
                                StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor

                            StrCfProcXREF   = '' 
                            if l.InflationScalingRef(): 
                                #if l.NominalScaling() == 'CPI Fixing In Arrears':
                                StrCfProcXREF         = str(l.InflationScalingRef().Name())+'_End_PP'
                                #else:
                                #    StrCfProcXREF         = str(l.IndexRef().Name())+'_Start_PP'
                            else:
                                StrCfProcXREF =  ''

                    elif cf.CashFlowType() == 'Float Rate':
                        try:
                            for r in cf.Resets():
                               
                                StrCfCoupFctrNB     =       '0'
                                StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.DayCountMethod())
                                StrCfCoupRatePERD   =       get_StrCfCoupRatePERD(l, cf)
                                StrCfCoupRateVAL    =       str(cf.spread)
                                
                                StrCfCrvIndexXREF  = ''  
                                StrCfCrvIndexXREF  = get_StrCfCrvIndexXREF(l, cf)
                                
                                StrCfCurRateVAL     =       str(r.FixingValue() / 100)
                                StrCfDiscENUM       =       'In Fine'
                                StrCfFwdEndDATE     =       Datefix(str(cf.EndDate()))
                                 
                                StrCfFwdStartDATE   =       Datefix(str(cf.StartDate())) #MR_MainFunctions.Datefix(str(cf.StartDate()))
                                StrCfHidOddCpFLAG   =       'FALSE'
                                StrCfInstrFctrVAL   =       '1'
                                
                                if cf.FloatRateFactor() == '0':
                                    StrCfPayFctrVAL   =       ''
                                else:
                                    StrCfPayFctrVAL   = cf.FloatRateFactor()

                                StrCfInstrSprdVAL   =       '0'
                                
                                StrCfPayDATE        =       Datefix(str(cf.PayDate()))
                                StrCfPayTYPE        =       'Float'
                                StrCfPayUNIT        =       l.Currency().Name()       
                                
                                if l.InflationScalingRef(): 
                                    if cf.Calculation().NominalFactor(calcSpace) == 0:
                                        StrCfPayVAL     = 0
                                    else:
                                        StrCfPayVAL = PayRecSign * i.contr_size * cf.NominalFactor()
                                        #StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() / cf.Calculation().NominalFactor(calcSpace) - NominalFactor(calcSpace) includes inflation, and amortisation schedule, new calculation does not back out amortisation schedule
                                else:
                                    StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                                
                                StrCfProratedFLAG   =       'TRUE'
                                StrCfRealEndDATE    =       Datefix(str(cf.EndDate()))
                                StrCfRealStartDATE  =       Datefix(str(cf.StartDate()))
                                StrCfRstDateDATE    =       Datefix(str(cf.StartDate()))
                                
                                StrCfProcXREF   = ''
                                if l.InflationScalingRef(): 
                                    #if l.nominal_scaling == 'CPI Fixing In Arrears':
                                    StrCfProcXREF         = str(l.InflationScalingRef().Name())+'_End_PP'
                                    #else:
                                    #     StrCfProcXREF         = str(l.IndexRef().Name())+'_Start_PP'
                                else:
                                    StrCfProcXREF =  ''
                        except:
                            for r in cf.Resets():
                                
                                StrCfCoupFctrNB     =       '0'
                                StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.DayCountMethod())
                                StrCfCoupRatePERD   =       get_StrCfCoupRatePERD(l, cf)
                                StrCfCoupRateVAL    =       str(cf.Spread())
                                
                                StrCfCrvIndexXREF  = ''  
                                StrCfCrvIndexXREF  = get_StrCfCrvIndexXREF(l, cf)                            
                                
                                StrCfCurRateVAL     =       str(r.FixingValue() / 100)
                                StrCfDiscENUM       =       'In Fine'
                                StrCfFwdEndDATE     =       Datefix(str(cf.EndDate()))
                                
                                StrCfFwdStartDATE   =       Datefix(str(cf.StartDate())) #MR_MainFunctions.Datefix(str(cf.StartDate()))
                                StrCfHidOddCpFLAG   =       'FALSE'
                                StrCfInstrFctrVAL   =       '1'
                                
                                if cf.FloatRateFactor() == '0':
                                    StrCfPayFctrVAL   =       ''
                                else:
                                    StrCfPayFctrVAL   = cf.FloatRateFactor()

                                StrCfInstrSprdVAL   =       '0'
                                StrCfPayDATE        =       Datefix(str(cf.PayDate()))
                                StrCfPayTYPE        =       'Float'
                                StrCfPayUNIT        =       l.Currency().Name()    
                                
                                if l.InflationScalingRef(): 
                                    if cf.Calculation().NominalFactor(calcSpace) == 0:
                                        StrCfPayVAL     = 0
                                    else:
                                        StrCfPayVAL = PayRecSign * i.contr_size * cf.NominalFactor()
                                        #StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() / cf.Calculation().NominalFactor(calcSpace) - NominalFactor(calcSpace) includes inflation, and amortisation schedule, new calculation does not back out amortisation schedule
                                else:
                                    StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                                
                                StrCfProratedFLAG   =       'TRUE'
                                StrCfRealEndDATE    =       Datefix(str(cf.EndDate()))
                                StrCfRealStartDATE  =       Datefix(str(cf.StartDate()))
                                StrCfRstDateDATE    =       Datefix(str(cf.StartDate()))
                    else:
                        StrCfCoupFctrNB     =       '0'
                        StrCfCoupRateCAL    =       ''
                        StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.DayCountMethod())
                        StrCfCoupRatePERD   =       'simple'
                        StrCfCoupRateVAL    =       str(cf.FixedRate())
                        StrCfHidOddCpFLAG   =       'FALSE'
                        StrCfPayDATE        =       Datefix(str(cf.PayDate()))
                        StrCfPayTYPE        =       'Fixed'
                        StrCfPayUNIT        =       l.Currency().Name()
                        
                        if l.InflationScalingRef(): 
                            if cf.Calculation().NominalFactor(calcSpace) == 0:
                                StrCfPayVAL     = 0
                            else:
                                StrCfPayVAL = PayRecSign * i.contr_size * cf.NominalFactor()
                                #StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount() / cf.Calculation().NominalFactor(calcSpace) - NominalFactor(calcSpace) includes inflation, and amortisation schedule, new calculation does not back out amortisation schedule
                        else:
                            StrCfPayVAL     = ael.CashFlow[cf.Oid()].nominal_amount()  
                        
                        StrCfProcXREF   = '' 
                        if l.InflationScalingRef(): 
                            #if l.NominalScaling() == 'CPI Fixing In Arrears':
                            StrCfProcXREF         = str(l.InflationScalingRef().Name())+'_End_PP'
                            #elif l.NominalScaling() == 'CPI':
                            #    StrCfProcXREF         = str(l.IndexRef().Name())+'_Start_PP'
                        else:
                            StrCfProcXREF =  ''
                        
                        StrCfProratedFLAG   =       'TRUE'
                        StrCfRealEndDATE    =       Datefix(str(cf.EndDate()))
                        StrCfRealStartDATE  =       Datefix(str(cf.StartDate()))

                    if StrCfPayVAL != 0.0:
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))
        outfile.close()
        calcSpace.Delete()
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)
    
    return i.insid
