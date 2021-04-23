'''

 -- HISTORY --
Date           CR               Requestor          Developer                    Change
-----------------------------------------------------------------------------------------------------------------
2010-09-001    264536           Natalie Austin     Douglas Finkel / Henk Nel    
2018-11-16     CHG1001135377    Reinhold Du Randt  Richard Coppin               http://http://abcap-jira/browse/ABITFA-5615
2019-06-12     MRINFRA-388    Reinhold Du Randt  Lucky Lesese 
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
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
    
    Ins = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()
	
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')

        #Base record
        BASFLAG = 'BAS'
        HeaderName = 'Forward Rate Agreement'
        OBJECT = 'Forward Rate AgreementSPEC'
        TYPE = 'Forward Rate Agreement'

        NAME = MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER = 'insaddr_' + str(i.insaddr)

        CurrencyCAL = ''
        CurrencyDAYC = ''
        CurrencyPERD = ''
        CurrencyUNIT = i.curr.insid
        NotionalCAL = ''
        NotionalDAYC = ''
        NotionalFUNC = ''
        NotionalPERD = ''
        NotionalUNIT = i.curr.insid

        sheetType = 'FTradeSheet'
        calcSpace = acm.Calculations().CreateCalculationSpace( context, sheetType )
        columnName = 'Trade Nominal'

        NotionalVAL = i.contr_size

        NotionalSTRG = ''

        UndrMaturityDATE = ''
        MaturityDATE = ''
        DaycountBasisDAYC = ''
        StrikePriceDAYC = ''
        StrikePriceVAL = ''
        StrikePricePERD = ''
        
        DaycountBasisCAL = ''
        StrikePriceCAL = ''
        StrikePriceFUNC = ''
        
        StrikePriceUNIT = '%'
        StrikePriceSTRG = ''
        UndrCrvIndXREF = ''
        StateProcFUNC = '@cash flow generator'
        CouponProratedFLAG = 'TRUE'
        CouponPrepayENUM = 'Discount'
        RunSCFPhaseFLAG = 'TRUE'
        BusDayRuleRULE = ''
        BusDayRuleBUSD = ''
        BusDayRuleCONV = ''
        BusDayRuleCAL = ''		

        sheetType = 'FDealSheet'
        calcSpace = acm.Calculations().CreateCalculationSpace( context, sheetType )        
        
        for Leg in Ins.Legs():
            UndrMaturityDATE = MR_MainFunctions.Datefix(Leg.EndDate())
            MaturityDATE = MR_MainFunctions.Datefix(Leg.StartDate())
            StrikePriceVAL = Leg.FixedRate()
            LocalCAL = str(Leg.PayCalendar().Name())[0:3]
            BusDayRuleRULE = MR_MainFunctions.BusRule(Leg.PayDayMethod())
            BusDayRuleCONV = MR_MainFunctions.BusConv(Leg.PayDayMethod())
            ounit = string.replace(str(Leg.PayOffsetUnit()), 'Days', 'd')
            ounit = string.replace(ounit, 'Weeks', 'w')
            ounit = string.replace(ounit, 'Months', 'm')
            ounit = string.replace(ounit, 'Years', 'y')
            BusDayRuleBUSD = MR_MainFunctions.CurveDays(str(Leg.PayOffsetCount()) + ounit)
            BusDayRuleCAL = 'Cal'+ str(LocalCAL)
            if Leg.LegType() == 'Float':
                StrikePricePERD = 'simple' 
                UndrCrvIndXREF = ('CI_' + str(Leg.FloatRateReference().Name()) + '_' + str(Leg.PayOffsetCount()) + str(Leg.PayOffsetUnit()))[0:50]
            for cf in Leg.CashFlows():
                DaycountBasisDAYC = MR_MainFunctions.DayCountFix(Leg.DayCountMethod())
                StrikePriceDAYC = MR_MainFunctions.DayCountFix(Leg.DayCountMethod())

            columnName = 'Forward Curve'
            curve = calcSpace.CalculateValue(Leg, columnName)
            UndrDiscCrvXREF = MR_MainFunctions.NameFix(str(Leg.MappedForwardLink().Link()))
            
            columnName = 'Discount Curve'
            curve = calcSpace.CalculateValue(Leg, columnName)
            DiscountCurveXREF = MR_MainFunctions.NameFix(str(Leg.MappedDiscountLink().Link()))

        TermLengthCAL = ''
        TermLengthDAYC = ''
        TermLengthFUNC = '@maturity relative days'
        TermLengthPERD = ''
        TermLengthUNIT = ''
        TermLengthVAL = ''
        TermLengthSTRG = ''
        TheoModelXREF = 'FRA2'
        MarketModelXREF = ''
        FairValueModelXREF = ''
        SettlementProcFUNC = '' #'@cashflow settlement'

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'   
            '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT,   
            NotionalCAL, NotionalDAYC, NotionalFUNC, NotionalPERD, NotionalUNIT, NotionalVAL, NotionalSTRG, MaturityDATE, UndrMaturityDATE, DaycountBasisCAL,   
            DaycountBasisDAYC, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG,   
            UndrCrvIndXREF, StateProcFUNC, CouponProratedFLAG, CouponPrepayENUM, RunSCFPhaseFLAG, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV,   
            BusDayRuleCAL, UndrDiscCrvXREF, DiscountCurveXREF, TermLengthCAL, TermLengthDAYC, TermLengthFUNC, TermLengthPERD, TermLengthUNIT, TermLengthVAL,   
            TermLengthSTRG, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC))
				
        outfile.close()
        
        #Position

        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################


