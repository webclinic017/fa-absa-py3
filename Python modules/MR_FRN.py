'''
Purpose                 :[Market Risk feed files],[Added section for generic instruments and updated StrCfPayFctrVAL and StrCfPayVAL]
Department and Desk     :[IT],[Market Risk]
Requester:              :[Natalie Austin],[Susan Kruger]
Developer               :[Douglas Finkel],[Willie van der Bank]
CR Number               :[264536,445783, 644358],[790080,796426 07/10/2011,14/10/2011]
2015-09-07              :Chris Human http://abcap-jira/browse/MINT-362

Description             :Remove time zero cashflows from structured instruments

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''

import ael, string, acm, PositionFile, MR_MainFunctions, UserDict

class GenericCF(UserDict.UserDict):
    '''
    Wacky dictionary
    '''
    def __init__(self):
        UserDict.UserDict.__init__(self)

    def __setitem__(self, key, val):
        UserDict.UserDict.__setitem__(self, key, val)
        setattr(self, key, val)
        
def GetForwardPrice(instrument, date):
    ''' Return the forward price for an instrument on the given date.
    '''
    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    forwardPrice = instrument.Calculation().ForwardPrice(calcSpace, date).Number()
    return forwardPrice

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
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        
        outfile = open(filename, 'a')
        
        #Base record
        BASFLAG	                =       'BAS'
        HeaderName	        =       'Floating Rate Note'
        OBJECT	                =       'Structured InstrumentSPEC'
        TYPE	                =       'Structured Instrument'
        
        NAME                    =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER              =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL	        =       ''
        CurrencyDAYC	        =       ''
        CurrencyPERD	        =       ''
        CurrencyUNIT	        =       i.curr.insid
        
        try:
            if ins.MappedDiscountLink().Link().YieldCurveComponent().Issuer() and ins.MappedDiscountLink().Link().YieldCurveComponent().RecordType() == 'YCAttribute':
                DiscountCurveXREF   =       ins.MappedDiscountLink().Link().UnderlyingComponent().AsString().rsplit(',')[0].lstrip("'").rstrip("'")
                CrdtSprdCurveXREF   =       MR_MainFunctions.NameFix(ins.MappedDiscountLink().Link().YieldCurveComponent().Issuer().Name()) + '_' + i.curr.insid + '_SpreadCurve'
            else:
                DiscountCurveXREF   =       MR_MainFunctions.NameFix(ins.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
                CrdtSprdCurveXREF   =       ''
        except:
            DiscountCurveXREF   =       MR_MainFunctions.NameFix(ins.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
            CrdtSprdCurveXREF   =       ''
        
        try:
            yc = ins.MappedDiscountLink().Link().YieldCurveComponent().Curve()
            if yc.Type() == 'Instrument Spread' and yc.RiskType() == 'Interest Rate':
                DiscountCurveXREF = ins.Name() + '_Curve'
        except:
            a = 1
        
        InitialIndxLvlFUNC	=       ''
        InitialIndxLvlUNIT	=       ''
        InitialIndxLvlVAL	=       '0'
        InitialIndxLvlSTRG	=       ''
        TheoModelXREF	        =       'General Structured Instrument'
        MarketModelXREF	        =       ''
        FairValueModelXREF	=       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, DiscountCurveXREF, CrdtSprdCurveXREF, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, TheoModelXREF, MarketModelXREF, FairValueModelXREF))

        #Rollover record
        BASFLAG	        =	'rm_ro'
        HeaderName	        =	'Floating Rate Note : Structured CashFlow'
        ATTRIBUTE	        =	'Structured CashFlow'
        OBJECT	                =	'Structured InstrumentSPEC'
        Legs = i.legs()
        for l in Legs:
        
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
            
            CFS = []
            if ins.Generic():   #Build cash flows for generic FRNs
                cf = GenericCF()

                cal = ins.Legs()[0].PayCalendar().Name()

                Start = ael.date_today().add_banking_day(ael.Calendar[cal], ins.SpotBankingDaysOffset())
                if ins.ExpiryPeriod_unit() == 'Years':
                    End =  acm.Time.DateAddDelta(ael.date(Start), ins.ExpiryPeriod_count(), 0, 0)
                elif (ins.ExpiryPeriod_unit() == 'Days' and ins.ExpiryPeriod_count() == 365):
                    End =  acm.Time.DateAddDelta(ael.date(Start), 1, 0, 0)
                elif ins.ExpiryPeriod_unit() == 'Days':
                    End =  acm.Time.DateAddDelta(ael.date(Start), 0, 0, ins.ExpiryPeriod_count())
                BusEnd = ael.date(End).adjust_to_banking_day(ael.Calendar[cal], ins.Legs()[0].PayDayMethod())

                if ins.Legs()[0].RollingPeriodUnit() == 'Days':
                    startday = ael.date(acm.Time.DateAddDelta(ael.date(End), 0, 0, -1)).adjust_to_banking_day(ael.Calendar[cal], ins.Legs()[0].PayDayMethod())
                if ins.Legs()[0].RollingPeriodUnit() == 'Months':
                    startday = ael.date(acm.Time.DateAddDelta(ael.date(End), 0, -3, 0)).adjust_to_banking_day(ael.Calendar[cal], ins.Legs()[0].PayDayMethod())

                payday = BusEnd
                cf = GenericCF()
                cf['pay_day'] = payday
                cf['end_day'] = payday
                cf['start_day'] = startday
                cf['type'] = 'Generic'
                CFS.append(cf)
                cf = GenericCF()
                cf['type'] = 'Fixed Amount'
                cf['pay_day'] = payday
                cf['end_day'] = ''
                cf['start_day'] = ''
                CFS.append(cf)

                if ins.Legs()[0].RollingPeriodUnit() == 'Months':
                    ind = 1
                    while ind <= 3:
                        payday = ael.date(acm.Time.DateAddDelta(ael.date(End), 0, -(ind*3), 0)).adjust_to_banking_day(ael.Calendar[cal], ins.Legs()[0].PayDayMethod())
                        startday = ael.date(acm.Time.DateAddDelta(ael.date(End), 0, -(ind*3+3), 0)).adjust_to_banking_day(ael.Calendar[cal], ins.Legs()[0].PayDayMethod())
                        cf = GenericCF()
                        cf['pay_day'] = payday
                        cf['end_day'] = payday
                        cf['start_day'] = startday
                        cf['type'] = 'Generic'
                        CFS.append(cf)
                        ind = ind + 1
            else:
                CFS = l.cash_flows()
                
            #for cf in l.cash_flows():
            for cf in CFS:
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
                        
                        StrCfPayDATE        =       MR_MainFunctions.Datefix(cf.pay_day)
                        StrCfPayTYPE        =       'Notional'
                        StrCfPayUNIT        =       l.curr.insid     
                        
                        if not ins.Generic():
                            StrCfPayVAL         =       cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                        else:
                            StrCfPayVAL         = i.contr_size
                        StrCfCrvIndexXREF   = 	    ''
                        #StrCfCapMatDATE = MR_MainFunctions.Datefix(str(i.exp_day))
                        #StrCfFwdStartDATE = MR_MainFunctions.Datefix(str(cf.start_day))

                    elif cf.type == 'Float Rate':
                    
                        try:
                        
                            for reset in cf.resets():
                                
                                StrCfCapMatDATE     =    MR_MainFunctions.Datefix(str(i.exp_day))
                                StrCfFwdStartDATE   =    MR_MainFunctions.Datefix(str(cf.start_day))
                                StrCfCoupFctrNB     =    '0'
                                StrCfCoupRateDAYC   =    MR_MainFunctions.DayCountFix(l.daycount_method)
                                StrCfCoupRatePERD   =    'simple'
                                StrCfCoupRateVAL    =    str(l.spread)
                                
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
                                #StrCfCrvIndexXREF   =       'StrCfCrvIndexXREF'
                                
                                StrCfCurRateVAL     =       str(reset.value / 100)
                                StrCfDiscENUM       =       'In Fine'
                                StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(cf.end_day))
                                
                                #StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(reset.day))
                                StrCfHidOddCpFLAG   =       'FALSE'
                                StrCfInstrFctrVAL   =       '1'
                                StrCfInstrSprdVAL   =       '0'
                                StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                                StrCfPayTYPE        =       'Float'
                                StrCfPayUNIT        =       l.curr.insid         
                                StrCfPayFctrVAL     =       cf.float_rate_factor
                                StrCfPayVAL         =       cf.nominal_amount()    # calc.Nominal(CalcSpace(cs), Trade).Number()
                                StrCfProratedFLAG   =       'TRUE'
                                StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                                StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))

                                StrCfRstDateDATE    =       MR_MainFunctions.Datefix(str(cf.start_day))
                        
                        except:
                            for reset in cf.resets():
                            
                                StrCfCapMatDATE         = MR_MainFunctions.Datefix(str(i.exp_day))
                                StrCfFwdStartDATE       = MR_MainFunctions.Datefix(str(cf.start_day))
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
#                                StrCfCrvIndexXREF   =       'StrCfCrvIndexXREF'

                                StrCfCurRateVAL     =       str(reset.value / 100)
                                StrCfDiscENUM       =       'In Fine'
                                StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(cf.end_day))
                                 
                                #StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(reset.day))
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
                    elif cf.type == 'Generic':
                    
                        StrCfCapMatDATE         = MR_MainFunctions.Datefix(str(BusEnd))
                        StrCfFwdStartDATE       = MR_MainFunctions.Datefix(str(cf.start_day))
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
#                                StrCfCrvIndexXREF   =       'StrCfCrvIndexXREF'

                        #StrCfCurRateVAL     =       str(reset.value / 100)
                        StrCfCurRateVAL     =       str(GetForwardPrice(ins.Legs()[0].FloatRateReference(), cf.start_day) / 100)
                        StrCfDiscENUM       =       'In Fine'
                        StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(cf.end_day))
                         
                        #StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(reset.day))
                        StrCfHidOddCpFLAG   =       'FALSE'
                        StrCfInstrFctrVAL   =       '1'
                        StrCfInstrSprdVAL   =       '0'
                        StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                        StrCfPayTYPE        =       'Float'
                        StrCfPayUNIT        =       l.curr.insid  
                                       
                        StrCfPayVAL         =       i.contr_size # PayRecSign*i.contr_size*cf.nominal_factor    # calc.Nominal(CalcSpace(cs), Trade).Number()
                        StrCfProratedFLAG   =       'TRUE'
                        StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                        StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))

                        StrCfRstDateDATE    =       MR_MainFunctions.Datefix(str(cf.start_day))
                    else:
                        
                        StrCfCapMatDATE     =       MR_MainFunctions.Datefix(str(i.exp_day))
                        StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(cf.start_day))
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
        #Position

        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    if trades.category != 'Collateral': #Collateral trades must be excluded from market risk calculations
                        PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################
