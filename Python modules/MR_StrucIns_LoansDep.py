'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536,522873

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-03-08     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-507
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''

import ael, string, acm, PositionFile, MR_MainFunctions

global outputList
outputList = []
InsL = []
NomL = []
DateL = []
nom_start = 0
nom_end = 0
dep_amount = 500
dep_day = ael.date('1900-01-01')
count = 0


# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    outfileP            =  open(PositionFilename, 'w')
    
    outfileP.close()

    del InsL[:]
    InsL[:] = []

    del NomL[:]
    NomL[:] = []
    
    del DateL[:]
    DateL[:] = []

    return filename

# OPENFILE ##########################################################################################################



# TRADE #############################################################################################################

def TradeWrite(i,trades,FileDir,Filename,PositionName,l,*rest):
    global outputList
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    Instrument = acm.FInstrument[i.insaddr]
    
    outfile = open(filename, 'a')
    
    if l.type in ('Call Fixed', 'Call Fixed Adjustable', 'Call Float'):
            #initialise variables for cycling through call loan/deposit balances
            nom_start = 0
            nom_end = 0
            dep_amount = 0
            dep_day = ael.date('1900-01-01')
            count = 0
    
            NomL[:] = []
            DateL[:] = []
        
            NomL.append(0)
            DateL.append(dep_day)
    
    BASFLAG             =       'BAS'
    HeaderName          =       'Loans Deposits'
    OBJECT              =       'Structured InstrumentSPEC'
    TYPE                =       'Structured Instrument'
    
    NAME                =       MR_MainFunctions.NameFix(i.insid+'_'+str(trades.trdnbr))
    IDENTIFIER          =       'insaddr_'+str(i.insaddr)+'_'+str(trades.trdnbr)
    
    CurrencyCAL         =       ''
    CurrencyDAYC        =       ''
    CurrencyPERD        =       ''
    CurrencyUNIT        =       Instrument.Currency().Name()
    
    try:
        DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
    except:
        DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
    
    InitialIndxLvlFUNC  =       ''
    InitialIndxLvlUNIT  =       ''
    InitialIndxLvlVAL   =       '0'
    InitialIndxLvlSTRG  =       ''
    
    TheoModelXREF       =       'General Structured Instrument'
    MarketModelXREF     =       ''
    FairValueModelXREF  =       ''
    
    outputList.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, DiscountCurveXREF, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
    
    if l.type in ('Call Fixed', 'Call Fixed Adjustable', 'Call Float'):
        Flows = l.cash_flows()
		
        def getKey(FCashFlow):
            return FCashFlow.pay_day
			
        sFlows = sorted(Flows, key=getKey)
    else:
        sFlows = l.cash_flows()
    
    #Rollover record
    BASFLAG	        =	'rm_ro'
    HeaderName	        =	'Loans Deposits : Structured CashFlow'
    ATTRIBUTE	        =	'Structured CashFlow'
    OBJECT	        =	'Structured InstrumentSPEC'
    
    for cf in sFlows:
        
        fix_float_ind = 0
        
        if l.type in ('Call Fixed', 'Call Fixed Adjustable', 'Call Float'):
		
            count += 1
            fix_float_ind = 0
			
                #outfile.write('%s,%s\n'%(cf.cfwnbr,count))

            if cf.type in ('Fixed Amount', 'Interest Reinvestment', 'Redemption Amount'):

                if cf.nominal_amount() == 0 and cf.fixed_amount != 0:
                    dep_amount = dep_amount-cf.fixed_amount
                else:
                    dep_amount = dep_amount-cf.nominal_amount()

                if dep_day != cf.pay_day:
                    NomL.append(dep_amount)
                    DateL.append(cf.pay_day)
                    nom_end += 1
                else:
                    NomL[nom_end]=dep_amount
                        
                dep_day=cf.pay_day
				
        if MR_MainFunctions.Datefix(cf.pay_day) > MR_MainFunctions.Datefix(ael.date_today()) and MR_MainFunctions.Datefix(cf.pay_day) != '':
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

            if cf.type == 'Fixed Amount':
                StrCfPayVAL         =       cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                StrCfPayTYPE        =       'Notional'
                StrCfPayUNIT        =       l.curr.insid     
                StrCfPayVAL         =       cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                StrCfCrvIndexXREF   = 	    ''
            elif cf.type == 'Redemption Amount':
                StrCfPayVAL         =       cf.projected_cf() #nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                StrCfPayTYPE        =       'Notional'
                StrCfPayUNIT        =       l.curr.insid     
                StrCfPayVAL         =       cf.known_cashflow() # PayRecSign*i.contr_size*cf.nominal_factor                    

            elif cf.type in  ('Call Float Rate', 'Float Rate'):
                if l.type in ('Call Fixed', 'Call Fixed Adjustable', 'Call Float'):
                    fix_float_ind = 2    
                                    
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
								
                            for float_leg in float_rate.legs():
                                fl = float_leg
								
                                StrCfCrvIndexXREF 	=	'SCI_' + output + '_' + str(getattr(reset, 'type')) + '_' + str(getattr(fl, 'end_period.count')) + str(getattr(fl, 'end_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
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
								
                            for float_leg in float_rate.legs():
                                fl = float_leg
                                StrCfCrvIndexXREF 	=	'SCI_' + output + '_' + str(getattr(reset, 'type')) + '_' + str(getattr(fl, 'end_period.count')) + str(getattr(fl, 'end_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
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
                if l.type in ('Call Fixed', 'Call Fixed Adjustable', 'Call Float'):
                    fix_float_ind = 1    
                
                StrCfCoupFctrNB     =       '0'
                StrCfCoupRateCAL    =       ''
                StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.daycount_method)
                StrCfCoupRatePERD   =       'simple'
                    
                if cf.type == 'Call Fixed Rate Adjustable':
                    for reset in cf.resets():
                        StrCfCoupRateVAL    =       str(reset.value)
                else:
                    StrCfCoupRateVAL    =       str(cf.rate)
                    
                StrCfHidOddCpFLAG   =       'FALSE'
                StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                StrCfPayTYPE        =       'Fixed'
                StrCfPayUNIT        =       l.curr.insid            
                StrCfPayVAL         =       cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                StrCfProratedFLAG   =       'TRUE'
                
            if fix_float_ind > 0:
			
                s_day = cf.start_day
                nom_start_day = DateL[min(nom_start, nom_end)]
                nom_val = NomL[min(nom_start, nom_end)]
				
                test_1 = (nom_start_day<cf.end_day)
                test_2 = (nom_start < nom_end)
					
                while (nom_start_day < cf.end_day) and (nom_start <= nom_end):
                    nom_val = NomL[nom_start]
				
                    if nom_start_day > cf.start_day:

                        StrCfRealEndDATE    =       MR_MainFunctions.Datefix(nom_start_day)
                        StrCfRealStartDATE  =       MR_MainFunctions.Datefix(s_day)
                        StrCfPayVAL         =       NomL[nom_start-2]                            
					
                        nom_val = NomL[nom_start]
					
                        if fix_float_ind == 2:
                            StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(nom_start_day))
                            StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(s_day))
                            StrCfRstDateDATE    =       MR_MainFunctions.Datefix(str(s_day))
							
                        s_day = nom_start_day
                            
                        if ((StrCfRealEndDATE!=StrCfRealStartDATE)and(StrCfPayVAL!=0)):
                            outputList.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))

                    nom_start_day = DateL[nom_start] 
                    nom_start += 1    
			
                StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(s_day))
                StrCfPayVAL         =       NomL[nom_start-1]
			
                if fix_float_ind == 2:
                    StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(cf.end_day))
                    StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(s_day))
                    StrCfRstDateDATE    =       MR_MainFunctions.Datefix(str(s_day))
			
                if ((StrCfRealEndDATE!=StrCfRealStartDATE)and(StrCfPayVAL!=0)):
                    outputList.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))
            else:
                outputList.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))

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

    print_zero_quantity_warning = False

    if MR_MainFunctions.Datefix(trades.value_day) > MR_MainFunctions.Datefix(ael.date_today()):
        StrCfPayDATE        =       MR_MainFunctions.Datefix(str(trades.value_day))
        StrCfPayTYPE        =       'Notional'
        StrCfPayUNIT        =       trades.curr.insid
        if trades.quantity == 0:
            print_zero_quantity_warning = True
            StrCfPayVAL         =       trades.premium
        else:
            StrCfPayVAL         =       trades.premium/trades.quantity
        StrCfCrvIndexXREF   = 	''
        outputList.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))

    for payments in trades.payments():
        if MR_MainFunctions.Datefix(payments.payday) > MR_MainFunctions.Datefix(ael.date_today()):

            StrCfPayDATE        =       MR_MainFunctions.Datefix(str(payments.payday))
            StrCfPayTYPE        =       'Notional'
            StrCfPayUNIT        =       payments.curr.insid
            if trades.quantity == 0:
                print_zero_quantity_warning = True
                StrCfPayVAL         =       payments.amount
            else:
                StrCfPayVAL         =       payments.amount/trades.quantity
            StrCfCrvIndexXREF   = 	 ''
            outputList.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))

    if print_zero_quantity_warning:
        print "Warning: Zero quantity on trade {0}.".format(trades.trdnbr)

    return trades.trdnbr

# TRADE #############################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,l,*rest):
    global outputList
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    Instrument = acm.FInstrument[i.insaddr]
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        if l.type in ('Call Fixed', 'Call Fixed Adjustable', 'Call Float'):
            #initialise variables for cycling through call loan/deposit balances
            nom_start = 0
            nom_end = 0
            dep_amount = 0
            dep_day = ael.date('1900-01-01')
            count = 0
    
            NomL[:] = []
            DateL[:] = []
        
            NomL.append(0)
            DateL.append(dep_day)
        
        BASFLAG             =       'BAS'
        HeaderName          =       'Loans Deposits'
        OBJECT              =       'Structured InstrumentSPEC'
        TYPE                =       'Structured Instrument'
        
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        
        try:
            DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        InitialIndxLvlFUNC  =       ''
        InitialIndxLvlUNIT  =       ''
        InitialIndxLvlVAL   =       '0'
        InitialIndxLvlSTRG  =       ''
        
        TheoModelXREF       =       'General Structured Instrument'
        MarketModelXREF     =       ''
        FairValueModelXREF  =       ''
        
        outputList.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, DiscountCurveXREF, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
        
        if l.type in ('Call Fixed', 'Call Fixed Adjustable', 'Call Float'):
            Flows = l.cash_flows()
		
            def getKey(FCashFlow):
                return FCashFlow.pay_day
			
            sFlows = sorted(Flows, key=getKey)
        else:
            sFlows = l.cash_flows()
	
        for cf in sFlows:
            #Rollover record
            BASFLAG	        =	'rm_ro'
            HeaderName	        =	'Loans Deposits : Structured CashFlow'
            ATTRIBUTE	        =	'Structured CashFlow'
            OBJECT	        =	'Structured InstrumentSPEC'

            fix_float_ind = 0
		
            if l.type in ('Call Fixed', 'Call Fixed Adjustable', 'Call Float'):
		
                count += 1
                fix_float_ind = 0
			
                if cf.type in ('Fixed Amount', 'Interest Reinvestment', 'Redemption Amount'):

                    if cf.nominal_amount() == 0 and cf.fixed_amount != 0:
                        dep_amount = dep_amount-cf.fixed_amount
                    else:
                        dep_amount = dep_amount-cf.nominal_amount()

                    if dep_day != cf.pay_day:
                        NomL.append(dep_amount)
                        DateL.append(cf.pay_day)
                        nom_end += 1
                    else:
                        NomL[nom_end]=dep_amount
                        
                    dep_day=cf.pay_day
				
            if MR_MainFunctions.Datefix(cf.pay_day) > MR_MainFunctions.Datefix(ael.date_today()) and MR_MainFunctions.Datefix(cf.pay_day) != '':
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
                
                if cf.type == 'Fixed Amount' or cf.type == 'Interest Reinvestment':
                    StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                    StrCfPayTYPE        =       'Notional'
                    StrCfPayUNIT        =       l.curr.insid     
                    StrCfPayVAL         =       cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                    StrCfCrvIndexXREF   = 	    ''
                elif cf.type == 'Redemption Amount':
                    StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                    StrCfPayTYPE        =       'Notional'
                    StrCfPayUNIT        =       l.curr.insid     
                    StrCfPayVAL         =       cf.known_cashflow() # PayRecSign*i.contr_size*cf.nominal_factor

                elif cf.type in ('Call Float Rate', 'Float Rate'):
			
                    if l.type in ('Call Fixed', 'Call Fixed Adjustable', 'Call Float'):
                        fix_float_ind = 2    
			
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
                                for float_leg in float_rate.legs():
                                    fl = float_leg
                                    StrCfCrvIndexXREF 	=	'SCI_' + output + '_' + str(getattr(reset, 'type')) + '_' + str(getattr(fl, 'end_period.count')) + str(getattr(fl, 'end_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
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
                            try:
                                StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                            except:
                                StrCfRealEndDATE    =  ''
                            try:
                                StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))
                            except:
                                StrCfRealStartDATE    =  ''
						
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
						
                                for float_leg in float_rate.legs():
                                    fl = float_leg
                                    StrCfCrvIndexXREF 	=	'SCI_' + output + '_' + str(getattr(reset, 'type')) + '_' + str(getattr(fl, 'end_period.count')) + str(getattr(fl, 'end_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
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
                        try:
                            StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                        except:
                            StrCfRealEndDATE    =  ''
                        try:
                            StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))
                        except:
                            StrCfRealStartDATE    =  ''
						
                        StrCfRstDateDATE    =       MR_MainFunctions.Datefix(str(cf.start_day))
                else:
				
                    if l.type in ('Call Fixed', 'Call Fixed Adjustable', 'Call Float'):
                        fix_float_ind = 1    
			
                    StrCfCoupFctrNB     =       '0'
                    StrCfCoupRateCAL    =       ''
                    StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.daycount_method)
                    StrCfCoupRatePERD   =       'simple'
                    
                    if cf.type == 'Call Fixed Rate Adjustable':
                        for reset in cf.resets():
                            StrCfCoupRateVAL    =       str(reset.value)
                    else:
                        StrCfCoupRateVAL    =       str(cf.rate)
                    
                    StrCfHidOddCpFLAG   =       'FALSE'
                    StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                    StrCfPayTYPE        =       'Fixed'
                    StrCfPayUNIT        =       l.curr.insid            
                    StrCfPayVAL         =       cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                    StrCfProratedFLAG   =       'TRUE'
                    try:
                        StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                    except:
                        StrCfRealEndDATE    =  ''
                    try:
                        StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))
                    except:
                        StrCfRealStartDATE    =  ''

                if fix_float_ind > 0:
			
                    s_day = cf.start_day
                    nom_start_day = DateL[min(nom_start, nom_end)]
                    nom_val = NomL[min(nom_start, nom_end)]
				
                    test_1 = (nom_start_day<cf.end_day)
                    test_2 = (nom_start < nom_end)
					
                    while (nom_start_day < cf.end_day) and (nom_start <= nom_end):
			
                        nom_val = NomL[nom_start-1]
				
                        if nom_start_day > cf.start_day:

                            StrCfRealEndDATE    =       MR_MainFunctions.Datefix(nom_start_day)
                            StrCfRealStartDATE  =       MR_MainFunctions.Datefix(s_day)
                            StrCfPayVAL         =       NomL[nom_start-2]                            
					
                            nom_val = NomL[nom_start]
					
                            if fix_float_ind == 2:
                                StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(nom_start_day))
                                StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(s_day))
                                StrCfRstDateDATE    =       MR_MainFunctions.Datefix(str(s_day))
							
                            s_day = nom_start_day
                            
                            if ((StrCfRealEndDATE!=StrCfRealStartDATE)and(StrCfPayVAL!=0)):
                                outputList.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))

                        nom_start_day = DateL[nom_start] 
                        nom_start += 1    
			
                    StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                    StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(s_day))
                    StrCfPayVAL         =       NomL[nom_start-1]
			
                    if fix_float_ind == 2:
                        StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(cf.end_day))
                        StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(s_day))
                        StrCfRstDateDATE    =       MR_MainFunctions.Datefix(str(s_day))
			
                    if ((StrCfRealEndDATE!=StrCfRealStartDATE)and(StrCfPayVAL!=0)):
                        outputList.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))
                else:
                    outputList.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))
        
        TradesValid = 0
        PaymentsValid = 0
        if len(i.trades()) > 0:
            for trades in i.trades():
                if MR_MainFunctions.ValidTradeNo(trades) == 0:
                    if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                        if MR_MainFunctions.Datefix(trades.value_day) > MR_MainFunctions.Datefix(ael.date_today()):
                            TradesValid = 1
                        for payments in trades.payments():
                            if MR_MainFunctions.Datefix(payments.payday) > MR_MainFunctions.Datefix(ael.date_today()):
                                PaymentsValid = 1
                        if PaymentsValid or TradesValid:
                            TradeWrite(i, trades, FileDir, Filename, PositionName, l)
                        if  PaymentsValid or TradesValid:
                            PositionFile.CreatePositionForwardStartingDeposits(trades, PositionFilename)
                        else:
                            PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################

def WriteOutput(temp,FileDir,Filename,*rest):
    global outputList
    filename = FileDir + Filename
    
    outfile =  open(filename, 'w')

    for item in outputList:
        outfile.write(item)
    
    outfile.close()
    return 'Successful'

