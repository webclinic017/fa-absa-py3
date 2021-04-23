'''
Purpose                 :[Market Risk feed files],[Added section for edited cashflows and added RunSCFPhaseFLAG]
Department and Desk     :[IT],[Market Risk]
Requester:              :[Natalie Austin],[Susan Kruger]
Developer               :[Douglas Finkel],[Willie van der Bank]
CR Number               :[264536, 289168],[802084 (21/10/2011)]

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
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
        
        BASFLAG	        = 'BAS'
        HeaderName  	= 'Cap/Floor'
        OBJECT	        = 'Cap/FloorSPEC'
        TYPE	        = 'Cap/Floor'
        
        NAME            = MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER      = 'insaddr_'+str(i.insaddr)
        
        CurrencyCAL	= ''
        CurrencyDAYC	= ''
        CurrencyPERD	= ''
        CurrencyUNIT	= i.curr.insid
        
        CapFLAG = ''
        
        if i.instype == 'Floor':
            CapFLAG = 'False'
        
        if i.instype == 'Cap':
            CapFLAG = 'True'

        datelist = []
        for l in i.legs():
            if MR_MainFunctions.Datefix(l.start_day) not in datelist:
                datelist.append(MR_MainFunctions.Datefix(l.start_day))
        datelist.sort()
        EffectiveDATE = datelist[0]
        
        MaturityDATE            = MR_MainFunctions.Datefix(i.exp_day) 
        
        CouponPrepayENUM	= 'In Fine'
        CapDigitalPayVAL	= ''
        StateProcFUNC	        = '@cash flow generator'
        TermNB                  = ''
        TermUNIT                = ''
        
        for l in i.legs():
            if l.rolling_period not in ('0d', '0m', '0y'):
                TermNB = getattr(l, 'rolling_period.count')
                TermUNIT = getattr(l, 'rolling_period.unit')
            else:
                TermNB = ''
                TermUNIT = 'Maturity'
        
        TermCAL	                =       ''
        ResetRuleRULE	        =       ''
        ResetRuleBUSD	        =       ''
        ResetRuleCONV	        =       ''
        ResetRuleCAL	        =       ''
        CouponGenENUM	        =       'Backward'
        FixedCouponDateNB	=       ''
        BusDayRuleRULE	        =       ''
        BusDayRuleBUSD	        =       ''
        BusDayRuleCONV	        =       ''
        BusDayRuleCAL	        =       ''    

        try:
            cashflow = acm.FCashFlow.Select01("leg = '%s' and startDate <= '%s' and endDate >= '%s'" % (leg.Oid(), acm.Time().TimeNow(), acm.Time().TimeNow()), '')
            calc = cashflow.Calculation()
            LastResetRateVAL    =   (calc.ForwardRate(cs) * 100) - cashflow.Spread()
        except:
            LastResetRateVAL    =       ''

        for c in i.cash_flows():
            for r in c.resets():
                LastResetRateVAL	=   (r.value / 100)
           
        NextResetRateVAL	=       ''
        
        #for cf in l.cash_flows():		
        UndrCrvIndXREF          =       ''   
        Legs = i.legs()
        for l in Legs:
            #if l.payleg == 1:
            UndrCrvIndXREF 	=	'SCI_' + str(getattr(l, 'float_rate').insid) + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
        
        try:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        CouponProratedFLAG	=       ''
        TheoModelXREF	        =       'CapFloor'
        MarketModelXREF	        =       ''
        FairValueModelXREF	=       ''
        SettlementProcFUNC	=       ''
     
        CashflowEditted = 0
        Legs = i.legs()
        for l in Legs:
            for cf in l.cash_flows():
                if cf.type in ('Caplet', 'Digital Caplet', 'Digital Floorlet', 'Floorlet'):
                    if CashflowEditted == 0:
                        if cf.creat_time <> cf.updat_time:
                            CashflowEditted = 1

        RunSCFPhaseFLAG = 'true'
        if CashflowEditted:
            RunSCFPhaseFLAG = 'false'
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CapFLAG, EffectiveDATE, MaturityDATE, CouponPrepayENUM, CapDigitalPayVAL, StateProcFUNC, TermNB, TermUNIT, TermCAL, ResetRuleRULE, ResetRuleBUSD, ResetRuleCONV, ResetRuleCAL, CouponGenENUM, FixedCouponDateNB, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, LastResetRateVAL, NextResetRateVAL, UndrCrvIndXREF, DiscountCurveXREF, CouponProratedFLAG, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC, RunSCFPhaseFLAG))

        if CashflowEditted:
            Legs = i.legs()
            for l in Legs:
                for cf in l.cash_flows():
                    if cf.type in ('Caplet', 'Floorlet', 'Digital Caplet', 'Digital Floorlet', 'Float'):
                        BASFLAG	                = 'rm_ro'
                        HeaderName	        = 'Cap/Floor : Structured CashFlow'
                        ATTRIBUTE	        = 'Structured CashFlow'
                        OBJECT	                = 'Cap/FloorSPEC'
                        StrCfProratedFLAG	= 'TRUE'
                        StrCfCoupRateCAL	= ''
                        StrCfTheoStartDATE	= ''            
                        StrCfPayCAL	        = ''
                        StrCfPayDAYC	        = ''
                        StrCfPayPERD	        = ''            
                        StrCfCoupFctrNB	        = '0'
                        StrCfCoupRatePERD	= 'simple'
                        StrCfCapMatDATE	        = MR_MainFunctions.Datefix(i.exp_day)            
                        StrCfDiscENUM	        = 'In Fine'            
                        StrCfHidOddCpFLAG	= 'FALSE'
                        StrCfInstrFctrVAL	= '1'
                        StrCfInstrSprdVAL	= '0'
                        StrCfProcXREF	        = ''
                        StrCfTheoEndDATE	= ''                        
                        
                        StrCfPayDATE	        = MR_MainFunctions.Datefix(str(cf.pay_day))
                        StrCfCoupRateDAYC	= MR_MainFunctions.DayCountFix(l.daycount_method)
                        StrCfPayUNIT	        = l.curr.insid
                        StrCfPayVAL	        = cf.nominal_amount()
                        
                        StrCfCrvIndexXREF   = ''  
                        float_rate = getattr(l, 'float_rate')
                        if float_rate:
                            output = float_rate.insid
                            StrCfCrvIndexXREF 	=	'SCI_' + output + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
                        else:
                            StrCfCrvIndexXREF   = ''
                        
                        StrCfCoupRateVAL	= str(l.strike)
                        if cf.resets():
                            for reset in cf.resets():
                                StrCfCurRateVAL	= str(reset.value / 100)
                        else:
                            StrCfCurRateVAL	= '0'
                            
                        StrCfRealEndDATE	= MR_MainFunctions.Datefix(cf.end_day)
                        StrCfFwdEndDATE	        = MR_MainFunctions.Datefix(cf.end_day)
                        StrCfFwdStartDATE	= MR_MainFunctions.Datefix(cf.start_day)
                        StrCfRstDateDATE	= MR_MainFunctions.Datefix(cf.start_day)
                        StrCfRealStartDATE	= MR_MainFunctions.Datefix(cf.start_day)
                        
                        if cf.type == 'Caplet':
                            StrCfPayTYPE = 'Cap'
                        elif cf.type == 'Floorlet' :
                            StrCfPayTYPE = 'Floor'
                        elif cf.type == 'Digital Caplet':
                            StrCfPayTYPE = 'Digital Cap'
                        elif cf.type == 'Digital Floorlet':
                            StrCfPayTYPE = 'Digital Floor'
                        elif cf.type == 'Float Rate':
                            StrCfPayTYPE = 'Float'
                        
                        StrCfPayFctrVAL	 = cf.float_rate_factor
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfProratedFLAG, StrCfCoupRateCAL, StrCfPayDATE, StrCfTheoStartDATE, StrCfCoupRateDAYC, StrCfCoupFctrNB, StrCfPayCAL, StrCfPayDAYC, StrCfPayPERD, StrCfPayUNIT, StrCfPayVAL, StrCfCoupRatePERD, StrCfCrvIndexXREF, StrCfCoupRateVAL, StrCfCurRateVAL, StrCfCapMatDATE, StrCfDiscENUM, StrCfRealEndDATE, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfProcXREF, StrCfRstDateDATE, StrCfRealStartDATE, StrCfPayTYPE, StrCfPayFctrVAL, StrCfTheoEndDATE))
                    
                    elif cf.type in ('Fixed Rate'):
                    
                        BASFLAG	                = 'rm_ro'
                        HeaderName	        = 'Cap/Floor : Structured CashFlow'
                        ATTRIBUTE	        = 'Structured CashFlow'
                        OBJECT	                = 'Cap/FloorSPEC'
                        StrCfProratedFLAG	= 'TRUE'
                        StrCfCoupRateCAL	= ''
                        StrCfPayDATE	        = MR_MainFunctions.Datefix(str(cf.pay_day))
                        StrCfTheoStartDATE	= ''
                        StrCfCoupRateDAYC	= MR_MainFunctions.DayCountFix(l.daycount_method)
                        StrCfCoupFctrNB	        = '0'
                        StrCfPayCAL	        = ''
                        StrCfPayDAYC	        = ''
                        StrCfPayPERD	        = ''
                        StrCfPayUNIT	        = l.curr.insid
                        StrCfPayVAL	        = cf.nominal_amount()
                        StrCfCoupRatePERD	= 'simple'
                        StrCfCrvIndexXREF	= ''
                        StrCfCoupRateVAL	= str(l.strike)
                        StrCfCurRateVAL	        = ''
                        StrCfCapMatDATE	        = ''
                        StrCfDiscENUM	        = ''
                        StrCfRealEndDATE	= MR_MainFunctions.Datefix(str(cf.end_day))
                        StrCfFwdEndDATE	        = ''
                        StrCfFwdStartDATE	= ''
                        StrCfHidOddCpFLAG	= 'FALSE'
                        StrCfInstrFctrVAL	= ''
                        StrCfInstrSprdVAL	= ''
                        StrCfProcXREF	        = ''
                        StrCfRstDateDATE	= ''
                        StrCfRealStartDATE	= MR_MainFunctions.Datefix(str(cf.start_day))
                        StrCfPayTYPE            = 'Fixed'
                        StrCfPayFctrVAL	        = ''
                        StrCfTheoEndDATE	= ''
                        
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfProratedFLAG, StrCfCoupRateCAL, StrCfPayDATE, StrCfTheoStartDATE, StrCfCoupRateDAYC, StrCfCoupFctrNB, StrCfPayCAL, StrCfPayDAYC, StrCfPayPERD, StrCfPayUNIT, StrCfPayVAL, StrCfCoupRatePERD, StrCfCrvIndexXREF, StrCfCoupRateVAL, StrCfCurRateVAL, StrCfCapMatDATE, StrCfDiscENUM, StrCfRealEndDATE, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfProcXREF, StrCfRstDateDATE, StrCfRealStartDATE, StrCfPayTYPE, StrCfPayFctrVAL, StrCfTheoEndDATE))

                    elif cf.type in ('Fixed Amount'):
                        BASFLAG	                = 'rm_ro'
                        HeaderName	        = 'Cap/Floor : Structured CashFlow'
                        ATTRIBUTE	        = 'Structured CashFlow'
                        OBJECT	                = 'Cap/FloorSPEC'
                        StrCfProratedFLAG	= ''
                        StrCfCoupRateCAL	= ''
                        StrCfPayDATE	        = MR_MainFunctions.Datefix(str(cf.pay_day))
                        StrCfTheoStartDATE	= ''
                        StrCfCoupRateDAYC	= ''
                        StrCfCoupFctrNB	        = ''
                        StrCfPayCAL	        = ''
                        StrCfPayDAYC	        = ''
                        StrCfPayPERD	        = ''
                        StrCfPayUNIT	        = l.curr.insid
                        StrCfPayVAL	        = cf.nominal_amount()
                        StrCfCoupRatePERD	= ''
                        StrCfCrvIndexXREF	= ''
                        StrCfCoupRateVAL	= str(l.strike)
                        StrCfCurRateVAL	        = ''
                        StrCfCapMatDATE	        = ''
                        StrCfDiscENUM	        = ''
                        StrCfRealEndDATE	= ''
                        StrCfFwdEndDATE	        = ''
                        StrCfFwdStartDATE	= ''
                        StrCfHidOddCpFLAG	= ''
                        StrCfInstrFctrVAL	= ''
                        StrCfInstrSprdVAL	= ''
                        StrCfProcXREF	        = ''
                        StrCfRstDateDATE	= ''
                        StrCfRealStartDATE	= ''
                        StrCfPayTYPE            = 'Notional'
                        StrCfPayFctrVAL	        = ''
                        StrCfTheoEndDATE	= ''
                        
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfProratedFLAG, StrCfCoupRateCAL, StrCfPayDATE, StrCfTheoStartDATE, StrCfCoupRateDAYC, StrCfCoupFctrNB, StrCfPayCAL, StrCfPayDAYC, StrCfPayPERD, StrCfPayUNIT, StrCfPayVAL, StrCfCoupRatePERD, StrCfCrvIndexXREF, StrCfCoupRateVAL, StrCfCurRateVAL, StrCfCapMatDATE, StrCfDiscENUM, StrCfRealEndDATE, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfProcXREF, StrCfRstDateDATE, StrCfRealStartDATE, StrCfPayTYPE, StrCfPayFctrVAL, StrCfTheoEndDATE))

        else:
            
            #Roll Over Cap Strike Rates
            
            BASFLAG	        =	'rm_ro'
            HeaderName	        =	'Cap/Floor : Cap Strike Rates'
            ATTRIBUTE	        =	'Cap Strike Rates'
            OBJECT	        =	'Cap/FloorSPEC'
            
            Legs = i.legs()
            for l in Legs:
                for cf in l.cash_flows():
                    if cf.type in ('Caplet', 'Digital Caplet', 'Digital Floorlet', 'Floorlet'):
            
                        CapStrikeRatesDATE  = MR_MainFunctions.Datefix(cf.start_day)
                        CapStrikeRatesENUM  = ''
                        CapStrikeRatesCAL   = ''
                        CapStrikeRatesDAYC  = MR_MainFunctions.DayCountFix(l.daycount_method)
                        CapStrikeRatesPERD  = 'simple'
                        CapStrikeRatesUNIT  = '%'
                        CapStrikeRatesVAL   = l.strike

                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, CapStrikeRatesDATE, CapStrikeRatesENUM, CapStrikeRatesCAL, CapStrikeRatesDAYC, CapStrikeRatesPERD, CapStrikeRatesUNIT, CapStrikeRatesVAL))

            #Roll Over Cap Notional Principal
            
            BASFLAG	        =	'rm_ro'
            HeaderName	        =	'Cap/Floor : Cap Notional Principal'
            ATTRIBUTE	        =	'Cap Notional Principal'
            OBJECT	        =	'Cap/FloorSPEC'
            
            Legs = i.legs()
            for l in Legs:
                for cf in l.cash_flows():
                    if cf.type in ('Caplet', 'Digital Caplet', 'Digital Floorlet', 'Floorlet'):
                        CapNotnalPrincDATE  = MR_MainFunctions.Datefix(cf.pay_day)
                        CapNotnalPrincENUM  = ''
                        CapNotnalPrincCAL   = ''
                        CapNotnalPrincDAYC  = MR_MainFunctions.DayCountFix(l.daycount_method)
                        CapNotnalPrincPERD  = ''
                        CapNotnalPrincUNIT  = i.curr.insid
                        CapNotnalPrincVAL   = cf.nominal_amount() #i.contr_size#t.quantity*i.contr_size
                        
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, CapNotnalPrincDATE, CapNotnalPrincENUM, CapNotnalPrincCAL, CapNotnalPrincDAYC, CapNotnalPrincPERD, CapNotnalPrincUNIT, CapNotnalPrincVAL))

        outfile.close()
        
        #Position
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################
