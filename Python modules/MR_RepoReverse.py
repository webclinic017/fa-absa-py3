'''
 -- HISTORY --
Date           CR                 Requestor          Developer                Change
--------------------------------------------------------------------------------------------------
2010-09-01     264536, 644358     Natalie Austin     Douglas Finkel           Original
               622355, 622355, 
               644358
2015/09/08     796426             Susan Kruger       Willie van der Bank      Remove time zero cashflows from structured instruments
2019-11-26                        Gary Beukes        Richard Coppin           https://jira-agl.absa.co.za/browse/FAU-493 
                                                                              MR Extracts - MR_RepoReverse missing trades
2020-09-11     CHG0128302	  Garth Saunders     Heinrich Cronje          https://absa.atlassian.net/browse/CMRI-776
'''

import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []



# OPENFILE ##########################################################################################################

def OpenFile(temp,FileDir,Filename,PositionName,*rest):
    
    filename = FileDir + Filename
    PositionFilename = FileDir + PositionName
    
    outfile = open(filename, 'w')
    outfileP = open(PositionFilename, 'w')
    
    outfile.close()
    outfileP.close()
    
    del InsL[:]
    InsL[:] = []
    
    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename = FileDir + Filename
    PositionFilename = FileDir + PositionName
    
    Instrument = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        
        outfile = open(filename, 'a')
        
        #Base record
        
        BASFLAG = 'BAS'
        HeaderName = 'IRS Structured Instrument'
        OBJECT = 'Structured InstrumentSPEC'
        TYPE = 'Structured Instrument'
        NAME = MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER = 'insaddr_'+str(i.insaddr)
        
        CurrencyCAL = ''
        CurrencyDAYC = ''
        CurrencyPERD = ''
        CurrencyUNIT = i.curr.insid
        
        # get the curve using calc space because the instrument map does not bring through the correct curve
        cs = acm.FCalculationSpace('FOrderBookSheet')
        calc = cs.CreateCalculation(Instrument, 'Discount Curve')

        DiscountCurveXREF = ''
        if calc.Value():
            try:
                if isinstance(calc.Value(), str):
                    DiscountCurveXREF = calc.Value().split(",")[0]
                elif calc.Value().IsKindOf(acm.FArray):
                    # The last element in the array aligns to what is used in the calculation 
                    DiscountCurveXREF = calc.Value()[-1].split(",")[0]
                else:
                    # The return type is unexpected
                    DiscountCurveXREF = calc.Value()
            except:
                DiscountCurveXREF = None
                
        InitialIndxLvlFUNC = ''
        InitialIndxLvlUNIT = ''
        InitialIndxLvlVAL = '0'
        InitialIndxLvlSTRG = ''
        TheoModelXREF = 'General Structured Instrument'
        MarketModelXREF = ''
        FairValueModelXREF = ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, DiscountCurveXREF, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
        
        BASFLAG = 'rm_ro'
        HeaderName = 'IRS Structured Instrument : Structured CashFlow'
        ATTRIBUTE = 'Structured CashFlow'
        OBJECT = 'Structured InstrumentSPEC'
        
        for l in i.legs():
            
            StrCfCapMatDATE = ''
            StrCfCoupFctrNB = ''
            StrCfCoupRateCAL = ''
            StrCfCoupRateDAYC = ''
            StrCfCoupRatePERD = ''
            StrCfCoupRateVAL = ''
            StrCfCrvIndexXREF = ''
            StrCfCurRateVAL = ''
            StrCfDiscENUM = ''
            StrCfFwdEndDATE = ''
            StrCfFwdStartDATE = ''
            StrCfHidOddCpFLAG = ''
            StrCfInstrFctrVAL = ''
            StrCfInstrSprdVAL = ''
            StrCfPayCAL = ''
            StrCfPayDATE = ''
            StrCfPayUNIT = ''
            StrCfPayDAYC = ''
            StrCfPayFctrVAL = ''
            StrCfPayPERD = ''
            StrCfPayTYPE = ''
            StrCfPayVAL = ''
            StrCfProcXREF = ''
            StrCfProratedFLAG = ''
            StrCfRealEndDATE = ''
            StrCfRealStartDATE = ''
            StrCfRstDateDATE = ''
            StrCfTheoEndDATE = ''
            StrCfTheoStartDATE = ''
            
            for cf in l.cash_flows():
            
                StrCfCapMatDATE = ''
                StrCfCoupFctrNB = ''
                StrCfCoupRateCAL = ''
                StrCfCoupRateDAYC = ''
                StrCfCoupRatePERD = ''
                StrCfCoupRateVAL = ''
                StrCfCrvIndexXREF = ''
                StrCfCurRateVAL = ''
                StrCfDiscENUM = ''
                StrCfFwdEndDATE = ''
                StrCfFwdStartDATE = ''
                StrCfHidOddCpFLAG = ''
                StrCfInstrFctrVAL = ''
                StrCfInstrSprdVAL = ''
                StrCfPayCAL = ''
                StrCfPayDATE = ''
                StrCfPayUNIT = ''
                StrCfPayDAYC = ''
                StrCfPayFctrVAL = ''
                StrCfPayPERD = ''
                StrCfPayTYPE = ''
                StrCfPayVAL = ''
                StrCfProcXREF = ''
                StrCfProratedFLAG = ''
                StrCfRealEndDATE = ''
                StrCfRealStartDATE = ''
                StrCfRstDateDATE = ''
                StrCfTheoEndDATE = ''
                StrCfTheoStartDATE = ''
                
                #Rollover record
                
                if MR_MainFunctions.Datefix(cf.pay_day) > MR_MainFunctions.Datefix(ael.date_today()) and MR_MainFunctions.Datefix(cf.pay_day) != '':
                    if cf.type == 'Fixed Amount':
                        StrCfPayDATE = MR_MainFunctions.Datefix(str(cf.pay_day))
                        StrCfPayTYPE = 'Notional'
                        StrCfPayUNIT = l.curr.insid     
                        StrCfPayVAL = cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                    
                    elif cf.type == 'Float Rate':
                        try:
                            for reset in cf.resets():
                                
                                StrCfCoupFctrNB = '0'
                                StrCfCoupRateDAYC = MR_MainFunctions.DayCountFix(l.daycount_method)
                                StrCfCoupRatePERD = 'simple'
                                StrCfCoupRateVAL = str(l.spread)
                                
                                StrCfCrvIndexXREF = ''  
                                float_rate = getattr(l, 'float_rate')
                                
                                if float_rate:
                                    output = float_rate.insid
                                    StrCfCrvIndexXREF = 'SCI_' + output + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
                                else:
                                    StrCfCrvIndexXREF = ''
                                
                                StrCfCurRateVAL = str(reset.value / 100)
                                StrCfDiscENUM = 'In Fine'
                                StrCfFwdEndDATE = MR_MainFunctions.Datefix(str(cf.end_day))
                                
                                StrCfFwdStartDATE = MR_MainFunctions.Datefix(str(cf.start_day))
                                StrCfHidOddCpFLAG = 'FALSE'
                                StrCfInstrFctrVAL = '1'
                                StrCfInstrSprdVAL = '0'
                                StrCfPayDATE = MR_MainFunctions.Datefix(str(cf.pay_day))
                                StrCfPayTYPE = 'Float'
                                StrCfPayUNIT = l.curr.insid           
                                StrCfPayVAL = cf.nominal_amount()
                                StrCfProratedFLAG = 'TRUE'
                                StrCfRealEndDATE = MR_MainFunctions.Datefix(str(cf.end_day))
                                StrCfRealStartDATE = MR_MainFunctions.Datefix(str(cf.start_day))
                                StrCfRstDateDATE = MR_MainFunctions.Datefix(str(cf.start_day))
                                
                        except:
                            StrCfCoupFctrNB = '0'
                            StrCfCoupRateDAYC = MR_MainFunctions.DayCountFix(l.daycount_method)
                            StrCfCoupRatePERD = 'simple'
                            StrCfCoupRateVAL = str(l.spread)

                            StrCfCrvIndexXREF = ''  
                            float_rate = getattr(l, 'float_rate')
                            
                            if float_rate:
                                output = float_rate.insid
                                StrCfCrvIndexXREF = 'SCI_' + output + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
                            else:
                                StrCfCrvIndexXREF = ''

                            StrCfCurRateVAL = '' #str(reset.FixingValue())
                            StrCfDiscENUM = 'In Fine'
                            StrCfFwdEndDATE = MR_MainFunctions.Datefix(str(cf.end_day))

                            StrCfFwdStartDATE = MR_MainFunctions.Datefix(str(cf.start_day))
                            StrCfHidOddCpFLAG = 'FALSE'
                            StrCfInstrFctrVAL = '1'
                            StrCfInstrSprdVAL = '0'
                            StrCfPayDATE = MR_MainFunctions.Datefix(str(cf.pay_day))
                            StrCfPayTYPE = 'Float'
                            StrCfPayUNIT = l.curr.insid            
                            StrCfPayVAL = cf.nominal_amount()
                            StrCfProratedFLAG = 'TRUE'
                            StrCfRealEndDATE = MR_MainFunctions.Datefix(str(cf.end_day))
                            StrCfRealStartDATE = MR_MainFunctions.Datefix(str(cf.start_day))
                            StrCfRstDateDATE = MR_MainFunctions.Datefix(str(cf.start_day)) #reset.Day()

                    elif cf.type == 'Fixed Rate' or cf.type == 'Fixed Rate Adjustable':

                        StrCfCoupFctrNB = '0'
                        StrCfCoupRateCAL = ''
                        StrCfCoupRateDAYC = MR_MainFunctions.DayCountFix(l.daycount_method)
                        StrCfCoupRatePERD = 'simple'
                        StrCfCoupRateVAL = str(cf.rate)
                        StrCfHidOddCpFLAG = 'FALSE'
                        StrCfPayDATE = MR_MainFunctions.Datefix(str(cf.pay_day))
                        StrCfPayTYPE = 'Fixed'
                        StrCfPayUNIT = l.curr.insid            
                        StrCfPayVAL = cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                        StrCfProratedFLAG = 'TRUE'
                        StrCfRealEndDATE = MR_MainFunctions.Datefix(str(cf.end_day))
                        StrCfRealStartDATE = MR_MainFunctions.Datefix(str(cf.start_day))

                    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))
        
        #Premium
        StrCfCapMatDATE = ''
        StrCfCoupFctrNB = ''
        StrCfCoupRateCAL = ''
        StrCfCoupRateDAYC = ''
        StrCfCoupRatePERD = ''
        StrCfCoupRateVAL = ''
        StrCfCrvIndexXREF = ''
        StrCfCurRateVAL = ''
        StrCfDiscENUM = ''
        StrCfFwdEndDATE = ''
        StrCfFwdStartDATE = ''
        StrCfHidOddCpFLAG = ''
        StrCfInstrFctrVAL = ''
        StrCfInstrSprdVAL = ''
        StrCfPayCAL = ''
        StrCfPayDATE = ''
        StrCfPayUNIT = ''
        StrCfPayDAYC = ''
        StrCfPayFctrVAL = ''
        StrCfPayPERD = ''
        StrCfPayTYPE = ''
        StrCfPayVAL = ''
        StrCfProcXREF = ''
        StrCfProratedFLAG = ''
        StrCfRealEndDATE = ''
        StrCfRealStartDATE = ''
        StrCfRstDateDATE = ''
        StrCfTheoEndDATE = ''
        StrCfTheoStartDATE = ''        
        
        '''
        for leg in i.legs():
            for cf in leg.cash_flows():
                 if cf.type != 'Fixed Amount':
                    if cf.start_day > ael.date_today():
                        
                        StrCfPayDATE = MR_MainFunctions.Datefix(str(cf.start_day))
                        StrCfPayTYPE = 'Notional'
                        StrCfPayUNIT = i.curr.insid
                        StrCfPayVAL = -1*i.contr_size
        '''
        
        for leg in i.legs():
            if l.start_day > ael.date_today():
                
                StrCfPayDATE = MR_MainFunctions.Datefix(str(l.start_day))
                StrCfPayTYPE = 'Notional'
                StrCfPayUNIT = i.curr.insid
                StrCfPayVAL = -1*i.contr_size
                
                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))
        
        outfile.close()
        
        #Position
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)
    
    return i.insid

# WRITE - FILE ######################################################################################################



