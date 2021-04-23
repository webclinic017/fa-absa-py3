"""
Purpose                 :[Market Risk feed files],[Updated MaturityDATE and BusDayRuleCAL]
Department and Desk     :[IT],[MR]
Requester:              :[Natalie Austin],[Susan Kruger], ['Ashley Kanter']
Developer               :[Douglas Finkel],[Willie van der Bank], [Sandile S Saul]
CR Number               :[264536,275268,289168,489655,572612,580529, 632898, 686048, 701575],[796426 14/10/2011]

Description
Change the SPOT price from Last price to Settle price
Added string "nan" for exception handling
Ex_Coupon_Period 'Preceding' added
Added support for extra rolling periods (Lukas Paluzga, C590239, 2012-11-08)

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-03-08     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-489
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
"""

import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []

# OPENFILE ##########################################################################################################

def dateReversed(date):
    if date not in ('', None):
        try:
            return ael.date_from_string(str(date)).to_string('%Y/%m/%d')
        except:
            date = str(date).replace('/', '-')
            return ael.date_from_string(str(date)).to_string('%Y/%m/%d')
            
    return ''

def OpenFile(temp,FileDir,Filename,PositionName, *rest):

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

#def GetCurrency(tradeFilter):

#    filter = acm.FTradeSelection[tradeFilter]
#    prfName = filter.FilterCondition()[0][4]
#    if acm.FPhysicalPortfolio['%s' % prfName]:
#        return acm.FPhysicalPortfolio['%s' % prfName].Currency().Name()
#    else:
#        return ''


def Write(i,FileDir,Filename,PositionName,Generic_Expiry, *rest):

    currency = 'ZAR' #GetCurrency(TradeFilter)
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    ins = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()
    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    calc = ins.Calculation()
    
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')
        #Base record
        
        BASFLAG	        =	'BAS'
        HeaderName	=	'Fixed Amortizing Bond'
        OBJECT	        =	'Fixed Amortizing BondSPEC'
        TYPE	        =	'Fixed Amortizing Bond'
        NAME            =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER      =       'insaddr_'+str(i.insaddr)
        CurrencyCAL	=	''
        CurrencyDAYC	=	''
        CurrencyPERD	=	''
        CurrencyUNIT	=	i.curr.insid
        NotionalCAL     =	''
        NotionalDAYC	=	''
        NotionalFUNC	=	''
        NotionalPERD	=	''
        NotionalUNIT	=	''
        
        sheetType       =       'FTradeSheet'		
        calcSpace       =       acm.Calculations().CreateCalculationSpace( context, sheetType )		
        columnName      =       'Trade Nominal'		
        NotionalVAL	=       i.contr_size 
        
        NotionalSTRG	=	''
        
        CouponRateDAYC          =       ''
        CouponRateVAL	        =       ''
        SpotPriceDAYC           =       ''
        SpreadOverYldDAYC       =       ''
        
        IssueDATE	= MR_MainFunctions.Datefix(ael.date_today())
        CouponRatePERD  = ''
        SpotPricePERD   = ''
        FixedCouponDateNB	=	''
        isEdited = False
        isEditedTemp = False
        Legs = i.legs()
        for LegNbr in Legs:		
            
            CouponRateVAL	        =       LegNbr.fixed_rate
            
            if LegNbr.daycount_method == '':
                AccrualDCBasisDAYC	=	MR_MainFunctions.DayCountFix('Act/365')        
                CouponRateDAYC          =	MR_MainFunctions.DayCountFix('Act/365')        
                SpotPriceDAYC           =	MR_MainFunctions.DayCountFix('Act/365')        
                SpreadOverYldDAYC       =	MR_MainFunctions.DayCountFix('Act/365')
            else:
                CouponRateDAYC          =       MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
                AccrualDCBasisDAYC	=	MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
                SpotPriceDAYC           =       MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
                SpreadOverYldDAYC	=	MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
                
            for cf in LegNbr.cash_flows():
                if MR_MainFunctions.Datefix(cf.start_day) <= IssueDATE and MR_MainFunctions.Datefix(cf.start_day) != '':
                    IssueDATE = MR_MainFunctions.Datefix(cf.start_day)
                if acm.FCashFlow[cf.cfwnbr].IsManuallyEdited():
                    isEditedTemp = True
                if isEditedTemp == True:
                    isEdited = isEditedTemp
       
            #All treated as cashflow edited due to complications determining current notional
            isEdited=True
            CouponRatePERD      = MR_MainFunctions.RollingPeriodFix(LegNbr.rolling_period)
            SpotPricePERD       =  MR_MainFunctions.RollingPeriodFix(LegNbr.rolling_period)

            FixedCouponDateNB   = ''
            
            if i.generic:
                if MR_MainFunctions.Datefix(i.exp_day) < MR_MainFunctions.Datefix(Generic_Expiry):
                    MaturityDATE	=	MR_MainFunctions.Datefix(Generic_Expiry) #MR_MainFunctions.Datefix(MR_MainFunctions.AddDatePeriod(ael.date_today(),i.exp_period))
                else:
                    MaturityDATE	=	MR_MainFunctions.Datefix(i.exp_day)    
            elif MR_MainFunctions.Datefix(i.exp_day) != MR_MainFunctions.Datefix(LegNbr.end_day):
                MaturityDATE    =          MR_MainFunctions.Datefix(LegNbr.end_day)
            else:
                MaturityDATE	=	MR_MainFunctions.Datefix(i.exp_day)
            
            #Dependant on fixing ZAR/R189
            if LegNbr.rolling_base_day == LegNbr.rolling_base_day.add_months(1).first_day_of_month().add_days(-1):
                FixedCouponDateNB   = '31'
            else:
                FixedCouponDateNB   = ael.date_from_string(LegNbr.rolling_base_day).to_string('%d')
                
            

        CouponRateCAL	        =	''
        
        StateProcFUNC	        =	'@cash flow generator'
        CouponGenENUM	        =	'Backward'
        CouponPossessnENUM	=	'Follow CUM-EX'
        CUM_EX_CouponRULE	=	'Preceding' #MR_MainFunctions.BusRuleFRB(LegNbr.pay_day_method)
        CUM_EX_CouponBUSD	=	MR_MainFunctions.CurveDays(i.ex_coup_period)
        CUM_EX_CouponCONV	=	''
        CUM_EX_CouponCAL	=	''
        
        TermNB = getattr(LegNbr, 'rolling_period.count')
        TermUNIT = getattr(LegNbr, 'rolling_period.unit')
        
        TermCAL	=	''
        CouponProrated = ''
        
        if not (LegNbr.rolling_period.endswith('y') or LegNbr.rolling_period.endswith('m')):
            CouponProrated  = 'TRUE'
        else:
            CouponProrated = 'FALSE'
            
        BusDayRuleRULE	=	MR_MainFunctions.BusRuleFRB(LegNbr.pay_day_method)
        BusDayRuleBUSD	=	''
        BusDayRuleCONV	=	''
        BusDayRuleCAL	=	'Cal%s' % currency
        SpotPriceCAL	=	''
        
        SpotPriceFUNC	=	''
#        SpotPricePERD	=	''
        SpotPriceUNIT	=	'%'
        
#       If 1, the Mark-To-Market value is taken from the feed. If 0,a theoretical value is calculated.
        SpotPriceVAL	=	''
        SPOT = 0
        if i.mtm_from_feed == 1:
            for price in ins.Prices():
                if price.Market():
                    if price.Market().Name() == 'SPOT':
                        SpotPriceVAL = price.Settle()
                        SPOT = 1
                    elif SPOT <> 1 and price.Market().Name() == 'internal':
                        SpotPriceVAL = price.Settle()
                else:
                    SpotPriceVAL	=	''
        else:
            try:
                SpotPriceVAL	=	calc.TheoreticalYieldToMaturity(cs)*100
            except:
                SpotPriceVAL	=	''
        
        if str(SpotPriceVAL) in ('1.#QNAN', 'NaN', 'nan'):
            SpotPriceVAL = ''
        
        SpotPriceSTRG	        =	''
        TradeDayRuleRULE	=	''
        TradeDayRuleBUSD	=	''
        TradeDayRuleCONV	=	''
        TradeDayRuleCAL		=	'Cal%s' % currency
        RepoCurveXREF		=       MR_MainFunctions.NameFix(ins.MappedRepoLink(ins.Currency()).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        
        # CR572612 Douglas Finkel Added USD bond bootstrap logic
        DiscountCurveXREF = '%s-GOVI-ME' % i.curr.insid
        if i.curr.insid == 'USD':
            DiscountCurveXREF = 'USD bond bootstrap'
        else:
            DiscountCurveXREF = MR_MainFunctions.NameFix(ins.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        
        RM_MapProcFUNC	        =	''
        SpreadOverYldCAL	=	''
        
        SpreadOverYldFUNC	=	'@implied spread THEO'
        SpreadOverYldPERD	=	'semi-annual'
        SpreadOverYldUNIT	=	'%'
        SpreadOverYldVAL	=	''
        SpreadOverYldSTRG	=	''
        
        LegalEntityXREF         =       ''
        if i.issuer_ptynbr:
            LegalEntityXREF     =       'ptynbr_' + str(i.issuer_ptynbr.ptynbr) + str(i.curr.insid)
        
        SeniorityClassMB        =       ''
        if i.seniority_chlnbr:
            SeniorityClassMB    = MR_MainFunctions.Seniority(i.seniority_chlnbr.entry)
        
        TheoModelXREF	=	'SA Bond-THEO'
        MarketModelXREF	=	'SA Bond-MARKET'
        FairValueModelXREF	=	''
        SettlementProcFUNC	=	''
        
        amortizedHeader = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, NotionalCAL, NotionalDAYC, NotionalFUNC, NotionalPERD, NotionalUNIT, NotionalVAL, NotionalSTRG, dateReversed(MaturityDATE), dateReversed(IssueDATE), FixedCouponDateNB, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, AccrualDCBasisDAYC, StateProcFUNC, CouponGenENUM, CouponPossessnENUM, CUM_EX_CouponRULE, CUM_EX_CouponBUSD, CUM_EX_CouponCONV, CUM_EX_CouponCAL, TermNB, TermUNIT, TermCAL, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, TradeDayRuleRULE, TradeDayRuleBUSD, TradeDayRuleCONV, TradeDayRuleCAL, RepoCurveXREF, DiscountCurveXREF, RM_MapProcFUNC, SpreadOverYldCAL, SpreadOverYldDAYC, SpreadOverYldFUNC, SpreadOverYldPERD, SpreadOverYldUNIT, SpreadOverYldVAL, SpreadOverYldSTRG, LegalEntityXREF, SeniorityClassMB, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC, CouponProrated, 'TRUE')
        #outfile.write(fxdAmountHeader)
        NAME            =       MR_MainFunctions.NameFix(i.insid) + '-cfedit'
        structuredHeader = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, NotionalCAL, NotionalDAYC, NotionalFUNC, NotionalPERD, NotionalUNIT, NotionalVAL, NotionalSTRG, dateReversed(MaturityDATE), dateReversed(IssueDATE), FixedCouponDateNB, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, AccrualDCBasisDAYC, StateProcFUNC, CouponGenENUM, CouponPossessnENUM, CUM_EX_CouponRULE, CUM_EX_CouponBUSD, CUM_EX_CouponCONV, CUM_EX_CouponCAL, TermNB, TermUNIT, TermCAL, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, TradeDayRuleRULE, TradeDayRuleBUSD, TradeDayRuleCONV, TradeDayRuleCAL, RepoCurveXREF, DiscountCurveXREF, RM_MapProcFUNC, SpreadOverYldCAL, SpreadOverYldDAYC, SpreadOverYldFUNC, SpreadOverYldPERD, SpreadOverYldUNIT, SpreadOverYldVAL, SpreadOverYldSTRG, LegalEntityXREF, SeniorityClassMB, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC, CouponProrated, 'FALSE') 
        
        #Roll over
        
        BASFLAG	        =       'rm_ro'
        HeaderName	=       'Fixed Amortizing Bond : Coupon List'
        ATTRIBUTE	=       'Coupon List'
        OBJECT	        =       'Fixed Amortizing BondSPEC'
        
        CouponListDATE	=	''
        CouponListENUM	=	''
        CouponListCAL	=	''
        CouponListDAYC  =       ''
        CouponListPERD  =       ''
        CouponListUNIT	=	'%'
        CouponListVAL	=       0
        Legs = i.legs()
        #Get last coupon list details
        for LegNbr in Legs:
            for cf in LegNbr.cash_flows():
                CouponListDATE	=	MR_MainFunctions.Datefix(cf.pay_day)
                if cf.start_day <> None and cf.end_day <> None:
                    CouponListDAYC	=       MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
                CouponListPERD      = MR_MainFunctions.RollingPeriodFix(LegNbr.rolling_period)
                
        amortizedCoupList =  ('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, dateReversed(CouponListDATE), CouponListENUM, CouponListCAL, CouponListDAYC, CouponListPERD, CouponListUNIT))
        #outfile.write
        amortizedCFlows = {}
        structuredCFlows = {}
        randomKey = 0
        for LegNbr in Legs:
            for cf in LegNbr.cash_flows():
                CouponListCAL	=	''
                CouponListENUM	=	''
                StrCfPayTYPE    =       ''
                StrCfHidOddCpFLAG =     ''
                CouponListVAL  = ''
                CouponListDAYC = ''
                CouponListPERD = ''
                CouponListDATE  = ''
                
                acmCashFlow = acm.FCashFlow[cf.cfwnbr]
                if isEdited == False and acmCashFlow.CashFlowType() != 'Fixed Rate':
                    HeaderName = 'Fixed Amortizing Bond : Amortization cashflow' 
                    ATTRIBUTE = 'Amortization cashflow'
                    if cf.type == 'Fixed Amount':
                        amount = cf.fixed_amount * 1000000
                    #else:
                     #   amount = acmCashFlow.FixedRate() * 1000000
                    CouponListDATE	=	MR_MainFunctions.Datefix(cf.pay_day)
                    curr =  LegNbr.curr.insid 
                    amortizedCFlows[randomKey] = '%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, dateReversed(CouponListDATE), curr, str(amount))
                    randomKey+=1
                else:
                    if isEdited == True:
                        HeaderName = 'Fixed Amortizing Bond : Structured CashFlow'
                        ATTRIBUTE = 'Structured CashFlow' 
                        CouponListENUM = ''
                        if LegNbr.rolling_period in ('0d', '0m', '0y'):
                            CouponListENUM = ''
                        elif LegNbr.rolling_period.endswith('y'):
                            CouponListENUM = 1/int(LegNbr.rolling_period[:LegNbr.rolling_period.find('y')])
                        elif LegNbr.rolling_period.endswith('m'):
                            CouponListENUM = 12/int(LegNbr.rolling_period[:LegNbr.rolling_period.find('m')])
                        else:
                            CouponListENUM = 365/int(LegNbr.rolling_period[:LegNbr.rolling_period.find('d')])
                            
                        payDay = MR_MainFunctions.Datefix(cf.pay_day)
                        endDate = cf.end_day
                        startDate = cf.start_day
                        currency = LegNbr.curr.insid
                        StrCfHidOddCpFLAG = 'FALSE'
                        if cf.type == 'Fixed Amount':
                            nominal = cf.fixed_amount * 1000000
                            StrCfPayTYPE = 'Notional'
                        elif cf.type == 'Float Rate':
                            nominal = cf.nominal_factor * 1000000
                            StrCfPayTYPE = 'Float'
                        elif cf.type not in ('Caplet', 'Digital Caplet', 'Digital Floorlet', 'Floorlet'):
                            nominal = cf.nominal_factor * 1000000
                            StrCfPayTYPE = 'Fixed'
                                
                        CouponListDAYC	=       MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
                        CouponListPERD      = MR_MainFunctions.RollingPeriodFix(LegNbr.rolling_period)
                        if acmCashFlow.CashFlowType() == 'Fixed Rate':
                            CouponListVAL = cf.rate
                        if startDate == '' and endDate == '':
                            structuredCFlows[randomKey] = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, dateReversed(CouponListDATE), CouponListENUM, CouponListCAL, CouponListDAYC, CouponListPERD, CouponListVAL, '', '', '', '', '', StrCfHidOddCpFLAG, '', '', '', dateReversed(payDay), '', '', '', StrCfPayTYPE, currency, nominal, '', 'FALSE')                  
                        else:
                            structuredCFlows[randomKey] = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, dateReversed(CouponListDATE), CouponListENUM, CouponListCAL, CouponListDAYC, CouponListPERD, CouponListVAL, '', '', '', '', '', StrCfHidOddCpFLAG, '', '', '', dateReversed(payDay), '', '', '', StrCfPayTYPE, currency, nominal, '', 'FALSE', dateReversed(endDate), dateReversed(startDate))                  
                                          
                        randomKey+=1
                
        #Write fixed Amounts
        if len(amortizedCFlows) > 0:
            outfile.write(amortizedHeader)
            outfile.write(amortizedCoupList)
            for k in amortizedCFlows.keys():
                #print fixedAmounts[k]
                outfile.write(amortizedCFlows[k])
        #Write other cashflows
        #print '============'
        if len(structuredCFlows) > 0:
            outfile.write(structuredHeader)
            for k in structuredCFlows.keys():
                #print fixedRates[k]
                outfile.write(structuredCFlows[k])
 
  
        outfile.close()
        
        #Position
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    if trades.value_day <= ael.date_today() or trades.premium == 0:
                        PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################
