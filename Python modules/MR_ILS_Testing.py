'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536,472409
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
            if l.nominal_scaling in ('CPI Fixing In Arrears', 'CPI'):
                if l.start_day > ael.date_today():
                    InitialIndxLvlVAL       = ''
                    InitialIndxLvlFUNC      = '@issue date level'
                    EffectiveDATE           = l.start_day
                    PaymentProcXREF         = str(l.index_ref.insid)+'_PP'
                else:
                    InitialIndxLvlVAL       = l.initial_index_value
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

        for l in i.legs():
            for cf in l.cash_flows():

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
            
                if MR_MainFunctions.Datefix(cf.pay_day) >= MR_MainFunctions.Datefix(ael.date_today()) and MR_MainFunctions.Datefix(cf.pay_day) != '':
                    if cf.type == 'Fixed Amount':
                    
                        StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                        StrCfPayTYPE        =       'Notional'
                        StrCfPayUNIT        =       l.curr.insid     
                        
                        if l.nominal_scaling in ('CPI Fixing In Arrears', 'CPI'): 
                            CashFlow = acm.FCashFlow[cf.cfwnbr]
                            calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                            if CashFlow.Calculation().NominalFactor(calcSpace).Number() == 0:
                                StrCfPayVAL     = 0
                            else:
                                StrCfPayVAL     = cf.nominal_amount() / CashFlow.Calculation().NominalFactor(calcSpace).Number()
                        else:
                            StrCfPayVAL     = cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                        
                        StrCfProcXREF   = '' 
                        if l.nominal_scaling in ('CPI Fixing In Arrears', 'CPI'): 
                            StrCfProcXREF =  str(l.index_ref.insid)+'_PP'
                            

                    elif cf.type == 'Float Rate':
                    
                        try:
                        
                            for reset in cf.resets():
                               
                                StrCfCoupFctrNB     =       '0'
                                StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.daycount_method)
                                StrCfCoupRatePERD   =       'simple'
                                StrCfCoupRateVAL    =       str(l.spread)

                                StrCfCrvIndexXREF  = ''  
                                float_rate = getattr(l, 'float_rate')
                                
                                if float_rate:
                                    output = float_rate.insid
                                    StrCfCrvIndexXREF 	=	'SCI_' + output + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
                                else:
                                    StrCfCrvIndexXREF  = ''                                
                                
                                StrCfCurRateVAL     =       str(reset.value / 100)
                                StrCfDiscENUM       =       'In Fine'
                                StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(cf.end_day))
                                 
                                StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(cf.start_day)) #MR_MainFunctions.Datefix(str(cf.start_day))
                                StrCfHidOddCpFLAG   =       'FALSE'
                                StrCfInstrFctrVAL   =       '1'
                                StrCfInstrSprdVAL   =       '0'
                                StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                                StrCfPayTYPE        =       'Float'
                                StrCfPayUNIT        =       l.curr.insid         
                                
                                if l.nominal_scaling in ('CPI Fixing In Arrears', 'CPI'): 
                                    CashFlow = acm.FCashFlow[cf.cfwnbr]
                                    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                                    if CashFlow.Calculation().NominalFactor(calcSpace).Number() == 0:
                                        StrCfPayVAL     = 0
                                    else:
                                        StrCfPayVAL     = cf.nominal_amount() / CashFlow.Calculation().NominalFactor(calcSpace).Number()
                                else:
                                    StrCfPayVAL     = cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                                    
                                StrCfProratedFLAG   =       'TRUE'
                                StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                                StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))

                                StrCfRstDateDATE    =       MR_MainFunctions.Datefix(str(cf.start_day))
                                
                                StrCfProcXREF   = ''
                                if l.nominal_scaling in ('CPI Fixing In Arrears', 'CPI'): 
                                    StrCfProcXREF =  str(l.index_ref.insid)+'_PP'
                                    
                        except:
                            for reset in cf.resets():
                            
                                StrCfCoupFctrNB     =       '0'
                                StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.daycount_method)
                                StrCfCoupRatePERD   =       'simple'
                                StrCfCoupRateVAL    =       str(l.spread)

                                StrCfCrvIndexXREF  = ''  
                                float_rate = getattr(l, 'float_rate')
                                if float_rate:
                                    output = float_rate.insid
                                    StrCfCrvIndexXREF 	=	'SCI_' + output + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
                                else:
                                    StrCfCrvIndexXREF  = ''                                

                                StrCfCurRateVAL     =       str(reset.value / 100)
                                StrCfDiscENUM       =       'In Fine'
                                StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(cf.end_day))
                                 
                                StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(cf.start_day)) #MR_MainFunctions.Datefix(str(cf.start_day))
                                StrCfHidOddCpFLAG   =       'FALSE'
                                StrCfInstrFctrVAL   =       '1'
                                StrCfInstrSprdVAL   =       '0'
                                StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                                StrCfPayTYPE        =       'Float'
                                StrCfPayUNIT        =       l.curr.insid  
                                               
                                if l.nominal_scaling in ('CPI Fixing In Arrears', 'CPI'): 
                                    CashFlow = acm.FCashFlow[cf.cfwnbr]
                                    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                                    if CashFlow.Calculation().NominalFactor(calcSpace).Number() == 0:
                                        StrCfPayVAL     = 0
                                    else:
                                        StrCfPayVAL     = cf.nominal_amount() / CashFlow.Calculation().NominalFactor(calcSpace).Number()
                                else:
                                    StrCfPayVAL     = cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                                    
                                StrCfProratedFLAG   =       'TRUE'
                                StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                                StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))
                                StrCfRstDateDATE    =       MR_MainFunctions.Datefix(str(cf.start_day))
                    else:
                        
                        StrCfCoupFctrNB     =       '0'
                        StrCfCoupRateCAL    =       ''
                        StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.daycount_method)
                        StrCfCoupRatePERD   =       'simple'
                        StrCfCoupRateVAL    =       str(cf.rate)
                        StrCfHidOddCpFLAG   =       'FALSE'
                        StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                        StrCfPayTYPE        =       'Fixed'
                        StrCfPayUNIT        =       l.curr.insid            
                        
                        if l.nominal_scaling in ('CPI Fixing In Arrears', 'CPI'): 
                            CashFlow = acm.FCashFlow[cf.cfwnbr]
                            calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                            if CashFlow.Calculation().NominalFactor(calcSpace).Number() == 0:
                                StrCfPayVAL     = 0
                            else:
                                StrCfPayVAL     = cf.nominal_amount() / CashFlow.Calculation().NominalFactor(calcSpace).Number()
                        else:
                            StrCfPayVAL     = cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                            
                        StrCfProcXREF   = '' 
                        if l.nominal_scaling in ('CPI Fixing In Arrears', 'CPI'): 
                            StrCfProcXREF =  str(l.index_ref.insid)+'_PP'

                        StrCfProratedFLAG   =       'TRUE'
                        StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                        StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))
                    
                    if StrCfPayVAL != 0.0:
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))
        outfile.close()

        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                PositionFile.CreatePosition(trades, PositionFilename)
    
    return i.insid

# WRITE - FILE ######################################################################################################


