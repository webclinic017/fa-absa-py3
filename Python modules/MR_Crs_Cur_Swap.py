'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536, 644358

Description             :Remove time zero cashflows from structured instruments
'''

import ael, string, acm, PositionFile, MR_MainFunctions

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



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    
    Instrument = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()

    Legs = i.legs()
    for l in Legs:
        if (str(i.insaddr) + '_' + str(l.legnbr)) not in InsL:
            InsL.append(str(i.insaddr) + '_' + str(l.legnbr))

            outfile = open(filename, 'a')

            #Base record
            BASFLAG             =       'BAS'
            HeaderName          =       'IRS Structured Instrument'
            OBJECT              =       'Structured InstrumentSPEC'
            TYPE                =       'Structured Instrument'
            if l.payleg == 1:
                NAME            =       MR_MainFunctions.NameFix(i.insid)+'_Pay'
            else:
                NAME            =       MR_MainFunctions.NameFix(i.insid)+'_Rec'
                
            IDENTIFIER          =      'insaddr_'+str(i.insaddr)+'_'+str(l.legnbr)
            
            CurrencyCAL         =       ''
            CurrencyDAYC        =       ''
            CurrencyPERD        =       ''
            
            CurrencyUNIT        =       l.curr.insid
            
            leg = acm.FLeg[l.legnbr]
            
            try:
                DiscountCurveXREF   =       leg.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
            except:
                DiscountCurveXREF   =       leg.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
            
            InitialIndxLvlFUNC  =       ''
            InitialIndxLvlUNIT  =       ''
            InitialIndxLvlVAL   =       '0'
            InitialIndxLvlSTRG  =       ''
            
            TheoModelXREF       =       'General Structured Instrument'
            MarketModelXREF     =       ''
            FairValueModelXREF  =       ''
            
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, DiscountCurveXREF, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
            
            #Rollover record
            BASFLAG	        =	'rm_ro'
            HeaderName	        =	'IRS Structured Instrument : Structured CashFlow'
            ATTRIBUTE	        =	'Structured CashFlow'
            OBJECT	        =	'Structured InstrumentSPEC'
            
            if l.payleg == 1:
                PayRecSign = -1.0
            else:
                PayRecSign = 1.0
            
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
                
                # calc = cf.Calculation()
                
                if MR_MainFunctions.Datefix(cf.pay_day) > MR_MainFunctions.Datefix(ael.date_today()) and MR_MainFunctions.Datefix(cf.pay_day) != '':
                    if cf.type == 'Fixed Amount':
                        
                        StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                        StrCfPayTYPE        =       'Notional'
                        StrCfPayUNIT        =       l.curr.insid     
                        
                        StrCfPayVAL         =       cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                        StrCfCrvIndexXREF   = 	    ''  
                        
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
                                    # Add compounding convention
                                    cfspread   = getattr(l, 'spread')
                                    rtype = getattr(l, 'reset_type')
                                    lrp = getattr(l, 'reset_period')
                                    comp = str(MR_MainFunctions.CompoundConvention(cfspread, rtype, lrp))	
                                    
                                    StrCfCrvIndexXREF 	=	'SCI_' + output + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method) + comp
                                else:
                                    StrCfCrvIndexXREF  = ''                                
                                
                                StrCfCurRateVAL     =       str(reset.value / 100)
                                StrCfDiscENUM       =       'In Fine'
                                StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(cf.end_day))
                                 
                                StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(cf.start_day))
                                StrCfHidOddCpFLAG   =       'FALSE'
                                StrCfInstrFctrVAL   =       '1'
                                StrCfInstrSprdVAL   =       '0'
                                StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                                StrCfPayTYPE        =       'Float'
                                StrCfPayUNIT        =       l.curr.insid         
                                
                                StrCfPayVAL         =       cf.nominal_amount()    # calc.Nominal(CalcSpace(cs), Trade).Number()
                                StrCfProratedFLAG   =       'TRUE'
                                StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                                StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))
                                StrCfRstDateDATE    =       MR_MainFunctions.Datefix(str(cf.start_day))

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
                                    # Add compounding convention
                                    cfspread   = getattr(l, 'spread')
                                    rtype = getattr(l, 'reset_type')
                                    lrp = getattr(l, 'reset_period')
                                    comp = str(MR_MainFunctions.CompoundConvention(cfspread, rtype, lrp))	
                                    
                                    StrCfCrvIndexXREF 	=	'SCI_' + output + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method) + comp
                                else:
                                    StrCfCrvIndexXREF  = ''                                

                                StrCfCurRateVAL     =       str(reset.value / 100)
                                StrCfDiscENUM       =       'In Fine'
                                StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(cf.end_day))
                                 
                                StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(cf.start_day))
                                StrCfHidOddCpFLAG   =       'FALSE'
                                StrCfInstrFctrVAL   =       '1'
                                StrCfInstrSprdVAL   =       '0'
                                StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                                StrCfPayTYPE        =       'Float'
                                StrCfPayUNIT        =       l.curr.insid  
                                               
                                StrCfPayVAL         =       cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor    # calc.Nominal(CalcSpace(cs), Trade).Number()
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
                        StrCfPayVAL         =       cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                        StrCfProratedFLAG   =       'TRUE'
                        StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                        StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))
                        
                    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))
                
            outfile.close()        
        
    
    return i.insid

# WRITE - FILE ######################################################################################################

