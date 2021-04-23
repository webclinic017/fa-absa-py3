"""
Purpose                 :[Market Risk feed files],[Updated MaturityDATE and BusDayRuleCAL]
Department and Desk     :[IT],[MR]
Requester:              :[Natalie Austin],[Susan Kruger]
Developer               :[Douglas Finkel],[Willie van der Bank]
CR Number               :[264536,275268,289168,489655,572612,580529, 632898, 686048, 701575],[796426 14/10/2011]

Description
Change the SPOT price from Last price to Settle price
Added string "nan" for exception handling
Ex_Coupon_Period 'Preceding' added
Added support for extra rolling periods (Lukas Paluzga, C590239, 2012-11-08)

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2015-09-07                                         Chris Human        http://abcap-jira/browse/MINT-362
2016-01-20     CHNG0003404656   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-444
2016-02-22     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-488
2016-06-03                      Ashley Canter      Mpaki Elephant     http://abcap-jira/browse/MINT-533
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
"""

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

def Write(i,FileDir,Filename,PositionName,Generic_Expiry,Party_ID,Currency,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    ins = acm.FInstrument[i.insaddr]
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    calc = ins.Calculation()
    
    
    if (str(i.insaddr)+str(Currency)) not in InsL:
        InsL.append(str(i.insaddr)+str(Currency))

        outfile = open(filename, 'a')
        #Base record
        
        BASFLAG	=	'BAS'
        HeaderName	=	'Fixed Rate Bond'
        OBJECT	        =	'Fixed Rate BondSPEC'
        TYPE	        =	'Fixed Rate Bond'
        
        if Currency != '': 
            NAME            =       MR_MainFunctions.NameFix(i.insid+'_'+Currency)
        else:
            NAME            =       MR_MainFunctions.NameFix(i.insid)
        if Currency !='':
            IDENTIFIER      =       'insaddr_'+str(i.insaddr)+'_' + Currency
        else:
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
            
            CouponRatePERD      = MR_MainFunctions.RollingPeriodFix(LegNbr.rolling_period)
            SpotPricePERD       =  MR_MainFunctions.RollingPeriodFix(LegNbr.rolling_period)

            FixedCouponDateNB   = ''
            
            if i.generic:
                
                IssueDATE = MR_MainFunctions.Datefix(ael.date_today())
                
                if MR_MainFunctions.Datefix(i.exp_day) < MR_MainFunctions.Datefix(Generic_Expiry):
                    MaturityDATE	=	MR_MainFunctions.Datefix(Generic_Expiry) #MR_MainFunctions.Datefix(MR_MainFunctions.AddDatePeriod(ael.date_today(),i.exp_period))
                else:
                    MaturityDATE	=	MR_MainFunctions.Datefix(i.exp_day)    
            elif MR_MainFunctions.Datefix(i.exp_day) != MR_MainFunctions.Datefix(LegNbr.end_day):
                MaturityDATE    =          MR_MainFunctions.Datefix(LegNbr.end_day)
            else:
                MaturityDATE	=	MR_MainFunctions.Datefix(i.exp_day)
            
            #Dependant on fixing ZAR/R189
            if i.generic:
                FixedCouponDateNB = '0'
            if LegNbr.rolling_base_day == LegNbr.rolling_base_day.add_months(1).first_day_of_month().add_days(-1):
                FixedCouponDateNB   = '31'
            else:
                FixedCouponDateNB   = ael.date_from_string(LegNbr.rolling_base_day).to_string('%d')

        CouponRateCAL	        =	''
        
        StateProcFUNC	        =	'@cash flow generator'
        
        if i.generic:
            CouponGenENUM       =   'Forward'
        else:
            CouponGenENUM		=	'Backward'
        
        CouponPossessnENUM	=	'Follow CUM-EX'
        CUM_EX_CouponRULE	=	'Preceding' #MR_MainFunctions.BusRuleFRB(LegNbr.pay_day_method)
        CUM_EX_CouponBUSD	=	MR_MainFunctions.CurveDays(i.ex_coup_period)
        CUM_EX_CouponCONV	=	''
        CUM_EX_CouponCAL	=	''
        
        if i.generic:
            TermNB = '3'
            TermUNIT = 'Months'
        elif LegNbr.rolling_period in ('0d', '0m', '0y'):
            TermNB = ''
            TermUNIT = 'Maturity'
        elif LegNbr.rolling_period in ('90d', '91d', '92d'):
            TermNB = '3'
            TermUNIT = 'Months'
        elif LegNbr.rolling_period in ('180d', '181d', '182d', '183d', '184d'):
            TermNB = '6'
            TermUNIT = 'Months'
        elif LegNbr.rolling_period in ('360d', '361d', '362d', '363d', '364d', '365d', '366d'):
            TermNB = '1'
            TermUNIT = 'Years'
        else: 
            TermNB = getattr(LegNbr, 'rolling_period.count')
            TermUNIT = getattr(LegNbr, 'rolling_period.unit')
        
        TermCAL	=	''
        
        BusDayRuleRULE	=	MR_MainFunctions.BusRuleFRB(LegNbr.pay_day_method)
        BusDayRuleBUSD	=	''
        BusDayRuleCONV	=	''
        BusDayRuleCAL	=	'CalZAR'
        SpotPriceCAL	=	''
        
        SpotPriceFUNC	=	''
#        SpotPricePERD	=	''
        SpotPriceUNIT	=	'%'
        
#       If 1, the Mark-To-Market value is taken from the feed. If 0,a theoretical value is calculated.
        SpotPriceVAL	=	''
        SPOT = 0
        if ((i.mtm_from_feed == 1)and(i.quote_type =='Yield')):
            for price in ins.Prices():
                if price.Market().Name() == 'SPOT':
                    SpotPriceVAL = price.Settle()
                    SPOT = 1
                elif SPOT <> 1 and price.Market().Name() == 'internal':
                    SpotPriceVAL = price.Settle()
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
        TradeDayRuleCAL		=	'CalZAR'
        RepoCurveXREF		=       MR_MainFunctions.NameFix(ins.MappedRepoLink(ins.Currency()).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        
        # CR572612 Douglas Finkel Added USD bond bootstrap logic
        if i.curr.insid == 'ZAR':
            DiscountCurveXREF = 'bond bootstrap'
        elif i.curr.insid == 'USD':
            DiscountCurveXREF = 'USD bond bootstrap'
        else:
            DiscountCurveXREF = MR_MainFunctions.NameFix(ins.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        
        if Currency != '':
            DiscountCurveXREF = str(Currency+'-SWAP')
            RepoCurveXREF = str(Currency+'-SWAP')
			
		
        RM_MapProcFUNC	        =	''
        SpreadOverYldCAL	=	''
        
        SpreadOverYldFUNC	=	'@implied spread THEO'
        SpreadOverYldPERD	=	'semi-annual'
        SpreadOverYldUNIT	=	'%'
        SpreadOverYldVAL	=	''
        SpreadOverYldSTRG	=	''
        
        LegalEntityXREF         =       ''
        if i.issuer_ptynbr:
            LegalEntityXREF     =       'ptynbr_' + str(i.issuer_ptynbr.ptynbr)+str(CurrencyUNIT)
        
        SeniorityClassMB        =       ''
        if i.seniority_chlnbr:
            SeniorityClassMB    = MR_MainFunctions.Seniority(i.seniority_chlnbr.entry)
        
        TheoModelXREF	=	'SA Bond-THEO'
        MarketModelXREF	=	'SA Bond-MARKET'
        FairValueModelXREF	=	''
        SettlementProcFUNC	=	''
        
        if Party_ID != '':
            CrdtSprdCurveXREF = MR_MainFunctions.NameFix(Party_ID + '_' + Currency + '_SpreadCurve')
        else:
            CrdtSprdCurveXREF = ''
            
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, NotionalCAL, NotionalDAYC, NotionalFUNC, NotionalPERD, NotionalUNIT, NotionalVAL, NotionalSTRG, MaturityDATE, IssueDATE, FixedCouponDateNB, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, AccrualDCBasisDAYC, StateProcFUNC, CouponGenENUM, CouponPossessnENUM, CUM_EX_CouponRULE, CUM_EX_CouponBUSD, CUM_EX_CouponCONV, CUM_EX_CouponCAL, TermNB, TermUNIT, TermCAL, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, TradeDayRuleRULE, TradeDayRuleBUSD, TradeDayRuleCONV, TradeDayRuleCAL, RepoCurveXREF, DiscountCurveXREF, RM_MapProcFUNC, SpreadOverYldCAL, SpreadOverYldDAYC, SpreadOverYldFUNC, SpreadOverYldPERD, SpreadOverYldUNIT, SpreadOverYldVAL, SpreadOverYldSTRG, LegalEntityXREF, SeniorityClassMB, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC, CrdtSprdCurveXREF))
        
        #Roll over
        
        BASFLAG	        =       'rm_ro'
        HeaderName	=       'Fixed Rate Bond : Coupon List'
        ATTRIBUTE	=       'Coupon List'
        OBJECT	        =       'Fixed Rate BondSPEC'
        
        CouponListDATE	=	''
        CouponListENUM	=	''
        CouponListCAL	=	''
        CouponListDAYC  =       ''
        CouponListPERD  = ''
        Legs = i.legs()
        for LegNbr in Legs:
            for cf in LegNbr.cash_flows():
                CouponListDATE	=	MR_MainFunctions.Datefix(cf.pay_day)
                CouponListENUM	=	''
                CouponListCAL	=	''
                
                if cf.start_day <> None and cf.end_day <> None:
                    CouponListDAYC	=       MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
                
                CouponListPERD      = MR_MainFunctions.RollingPeriodFix(LegNbr.rolling_period)
        
        CouponListUNIT	=	'%'
        CouponListVAL	=       0
        
        for LegNbr in Legs:
            for cf in LegNbr.cash_flows():
                if cf.type == 'Fixed Rate':
                    CouponListVAL	=	cf.rate
        
        if CouponListVAL != 0:
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, CouponListDATE, CouponListENUM, CouponListCAL, CouponListDAYC, CouponListPERD, CouponListUNIT, CouponListVAL))
        
        outfile.close()
        
        #Position
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    if trades.value_day <= ael.date_today() or trades.premium == 0:
                        if trades.category != 'Collateral': #Collateral trades must be excluded from market risk calculations
                            PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################

