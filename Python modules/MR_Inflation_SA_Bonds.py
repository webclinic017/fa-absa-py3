'''
Purpose                 :[Market Risk feed files],[Updated BusDayRuleRULE],[Updated DiscountCurveXREF,TradeDayRuleRULE,TradeDayRuleBUSD and TradeDayRuleCONV],
                        [Fixed position files check: trades.value_day <= ael.date_today]
Department and Desk     :[IT],[Market Risk],[MR],[MR]
Requester:              :[Natalie Austin],[Susan Kruger],[Susan Kruger],[Susan Kruger]
Developer               :[Douglas Finkel],[Willie van der Bank],[Willie van der Bank],[Willie van der Bank]
CR Number               :[264536, 275268, 644358, 701575],[796426 14/10/2011],[816235 04/11/11],[838719 25/11/2011]
2015-09-07              :Chris Human http://abcap-jira/browse/MINT-362

Description
Remove time zero cashflows from structured instruments
'Preceding' value assigned to CUM_EX_CouponRULE

FAU-2811        Melusi Maseko   2017-06-20      FA-Upgrade 2017 changes

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

def Write(i,FileDir,Filename,PositionName,Generic_Expiry,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    ins = acm.FInstrument[i.insaddr]
#   trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')
    
	#Base record
    
        BASFLAG	        =	'BAS'
        HeaderName	=	'Inflation Linked Bond'
        OBJECT	        =	'Fixed Rate BondSPEC'
        TYPE	        =	'Fixed Rate Bond'
        
        NAME            =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER      =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL	=	''
        CurrencyDAYC	=	''
        CurrencyPERD	=	''
        CurrencyUNIT	=	i.curr.insid
        NotionalCAL	=	''
        NotionalDAYC	=	''
        NotionalFUNC	=	''
        NotionalPERD	=	''
        NotionalUNIT	=	i.curr.insid
        
        sheetType           =   'FTradeSheet'		
        calcSpace           =   acm.Calculations().CreateCalculationSpace( context, sheetType )		
        columnName          =   'Trade Nominal'		
        NotionalVAL         =	i.contr_size
        
        LegalEntityXREF     =   ''
        if i.issuer_ptynbr:
            LegalEntityXREF     =       'ptynbr_' + str(i.issuer_ptynbr.ptynbr) + str(CurrencyUNIT)
        
        NotionalSTRG        =	''
        #MaturityDATE	    =	MR_MainFunctions.Datefix(i.exp_day)
            
        IssueDATE           =	MR_MainFunctions.Datefix(ael.date_today())
        FixedCouponDateNB   =   ''
        
        Legs = i.legs()		
        for LegNbr in Legs:		
            AccrualDCBasisDAYC  =       MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
            SpotPriceDAYC       =       MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
            CouponRateVAL	=       LegNbr.fixed_rate
            CouponRateDAYC      =       MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
            
            CouponRatePERD      =       MR_MainFunctions.RollingPeriodFixISABonds(LegNbr.rolling_period)
            SpotPricePERD       =       MR_MainFunctions.RollingPeriodFixISABonds(LegNbr.rolling_period)

            TermUNIT            =       MR_MainFunctions.CurveUnits(LegNbr.rolling_period)
            #BusDayRuleRULE      =       MR_MainFunctions.BusRuleFRB(LegNbr.pay_day_method)
            
            for cf in LegNbr.cash_flows():
                if MR_MainFunctions.Datefix(cf.start_day) <= IssueDATE and MR_MainFunctions.Datefix(cf.start_day) != '':
                    IssueDATE = MR_MainFunctions.Datefix(cf.start_day)

            FixedCouponDateNB       =       ''
            
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
                
        CouponRateCAL           =       ''
        
        TermNB                  =	MR_MainFunctions.Rolling_NameFix(LegNbr.rolling_period)

        StateProcFUNC           =       '@cash flow generator'
        CouponGenENUM           =       'Backward'
        CouponPossessnENUM	=       'Follow CUM-EX'
        PaymntProcXREF          =       ''

        sheetType = 'FDealSheet'
        calcSpace = acm.Calculations().CreateCalculationSpace( context, sheetType )
        for leg in ins.Legs():
        # Discount
            columnName = 'Discount Curve'
            curve = calcSpace.CalculateValue( leg, columnName )
            DiscountCurveXREF = MR_MainFunctions.NameFix(str(leg.MappedDiscountLink().Link()))
            # Repo
            columnName = 'Repo Curve'
            curve = calcSpace.CalculateValue( leg, columnName )
            MappedLeg = curve
            
            if MappedLeg  == 'None':
                PaymntProcXREF = 'None'
            elif leg.InflationScalingRef():
                if str(leg.InflationScalingRef().Name()) == 'SACPI-Bond':
                    PaymntProcXREF = str(leg.InflationScalingRef().Name()) + '_Start_PP'

            
            InitialIndxLvlVAL	=       leg.InflationBaseValue()
             
        InitialIndxLvlFUNC	=       ''
        InitialIndxLvlUNIT	=       ''
        
        InitialIndxLvlSTRG	=       ''
        
        TermCAL             =       ''
        BusDayRuleRULE      =       MR_MainFunctions.BusRuleFRB(LegNbr.pay_day_method)
        BusDayRuleBUSD      =       ''
        BusDayRuleCONV      =       ''
        BusDayRuleCAL       =       'CalZAR'
        SpotPriceCAL        =       ''
        SpotPriceFUNC       =       ''
        SpotPriceUNIT	        =       '%'

        SpotPriceVAL            =       '0'#t.price
        SpotPriceSTRG	        =       ''
        
        TradeDayRuleRULE	=       ''
        TradeDayRuleBUSD	=       ''
        TradeDayRuleCONV	=       ''
        TradeDayRuleCAL	        =       'CalZAR'
        RepoCurveXREF	        =       'ZAR_Bond_repo_GC'      
        DiscountCurveXREF	=       'ZAR-SWAP'
        
        dcurve                  =       MR_MainFunctions.NameFix(ins.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))    

        if dcurve == 'ZAR-Gov-Bonds-Disc':
            DiscountCurveXREF   =       'bond bootstrap'
        else:
            DiscountCurveXREF   =       dcurve
            
        RM_MapProcFUNC          =       ''    
        SpreadOverYldCAL	=       ''
        SpreadOverYldDAYC	=       'actual/365'
        SpreadOverYldFUNC	=       '@implied spread THEO'
        SpreadOverYldPERD	=       'semi-annual'
        SpreadOverYldUNIT	=       '%'
        SpreadOverYldVAL	=       ''
        SpreadOverYldSTRG	=       ''
        TheoModelXREF	        =       'SA Bond-THEO'
        MarketModelXREF         =	'SA Bond-MARKET'
        FairValueModelXREF	=       ''
        SettlementProcFUNC	=       ''

        CUM_EX_CouponRULE	=	'Preceding' #MR_MainFunctions.BusRuleFRB(LegNbr.pay_day_method)
        CUM_EX_CouponBUSD	=	MR_MainFunctions.CurveDays(i.ex_coup_period)
        CUM_EX_CouponCONV	=	''
        CUM_EX_CouponCAL	=	''        
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, NotionalCAL, NotionalDAYC, NotionalFUNC, NotionalPERD, NotionalUNIT, NotionalVAL, NotionalSTRG, MaturityDATE, IssueDATE, FixedCouponDateNB, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, AccrualDCBasisDAYC, StateProcFUNC, CouponGenENUM, CouponPossessnENUM, PaymntProcXREF, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, TermNB, TermUNIT, TermCAL, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, TradeDayRuleRULE, TradeDayRuleBUSD, TradeDayRuleCONV, TradeDayRuleCAL, RepoCurveXREF, DiscountCurveXREF, RM_MapProcFUNC, SpreadOverYldCAL, SpreadOverYldDAYC, SpreadOverYldFUNC, SpreadOverYldPERD, SpreadOverYldUNIT, SpreadOverYldVAL, SpreadOverYldSTRG, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC, CUM_EX_CouponRULE, CUM_EX_CouponBUSD, CUM_EX_CouponCONV, CUM_EX_CouponCAL, LegalEntityXREF))

        BASFLAG	=       'rm_ro'
        HeaderName	=       'Inflation Linked Bond : Coupon List'
        ATTRIBUTE	=       'Coupon List'
        OBJECT	=       'Fixed Rate BondSPEC'
        
        Legs = i.legs()
        for LegNbr in Legs:
            for cf in LegNbr.cash_flows():
                if cf.pay_day > ael.date_today() and MR_MainFunctions.Datefix(cf.pay_day) != '':
                    CouponListDATE	=	MR_MainFunctions.Datefix(cf.pay_day)
                    
                    CouponListENUM	=	''
                    CouponListCAL	=	''
                    CouponListDAYC	=	MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
                    CouponListPERD	=	MR_MainFunctions.RollingPeriodFixISABonds(LegNbr.rolling_period)
                    CouponListUNIT	=	'%'
                    CouponListVAL	=	cf.rate

                    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, CouponListDATE, CouponListENUM, CouponListCAL, CouponListDAYC, CouponListPERD, CouponListUNIT, CouponListVAL))
        outfile.close()
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    if trades.value_day <= ael.date_today() or trades.premium == 0:
                        if trades.category != 'Collateral': #Collateral trades must be excluded from market risk calculations
                            PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid
    
# WRITE - FILE ######################################################################################################

