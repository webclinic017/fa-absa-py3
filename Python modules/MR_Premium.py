
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Ashley Kanter
Developer               :
CR Number               :

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-01-20     CHNG0003450270   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-413
2016-03-08     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-528
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''

import ael, string, acm, PositionFile, MR_MainFunctions

TrdL = []

#MoneyMarket Curve
def getMMYC(i):
    instrument = acm.FInstrument[i.insid]
    '''
    global calcSpace
    global collectLimit
    global collect
    '''
    calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    #component = instrument.Calculation().DiscountYieldCurveComponent(calcSpace)
    component = instrument.Calculation().MoneyMarketYieldCurveComponents(calcSpace)
    if component:
        if component.IsKindOf('FYieldCurve'):
            return component.Name()
        if component.IsKindOf('FArray') and component.Size() > 0:
            for c in component:
                if c.Currency().Name() == instrument.Currency().Name():
                    return c.Name()
        #if component.IsKindOf('FInstrumentSpread') or component.IsKindOf('FYCAttribute'):
        #    return component.Curve().Name()
    return ''

# OPENFILE ##########################################################################################################

def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    outfile             =  open(filename, 'w')
    outfileP            =  open(PositionFilename, 'w')
    
    outfile.close()
    outfileP.close()

    del TrdL[:]
    TrdL[:] = []
    
    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(t,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName

#    ins = acm.FInstrument[i.insaddr]
    Trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    Instrument = acm.FInstrument[t.insaddr.insid]
    
    if MR_MainFunctions.IsExcludedPortfolio(t) == False:
        if (t.trdnbr) not in TrdL:
            TrdL.append(t.trdnbr)

            #Base record
            outfile = open(filename, 'a')
            BASFLAG	        =	'BAS'
            HeaderName	        =	'Zero Coupon Bonds'
            OBJECT	        =	'Zero Coupon BondSPEC'
            TYPE	        =	'Zero Coupon Bond'

            NAME                =       str(t.trdnbr)+'_Premium'
            IDENTIFIER          =       str(t.trdnbr)+'_Premium'

            CurrencyCAL	        =	''
            CurrencyDAYC	=	''
            CurrencyPERD	=	''
            CurrencyUNIT	=	t.curr.insid
            NotionalCAL	        =	''
            NotionalDAYC	=	''
            NotionalFUNC	=	''
            NotionalPERD	=	''
            NotionalUNIT	=	t.curr.insid

            sheetType       = 'FTradeSheet'		
            calcSpace       = acm.Calculations().CreateCalculationSpace( context, sheetType )		
            columnName      = 'Trade Nominal'		
            NotionalVAL     = abs(t.premium) #calcSpace.CalculateValue(trade , columnName )
            
            NotionalSTRG    =	''

                            
            MaturityDATE        =	MR_MainFunctions.Datefix(t.value_day)
            IssueDATE           =   ''
                        
            StateProcFUNC	        =	'@cash flow generator'
            TermNB	                =	''
            TermUNIT	                =	''
            TermCAL	                =	''
            BusDayRuleRULE	        =	''
            BusDayRuleBUSD	        =	''
            BusDayRuleCONV	        =	''
            BusDayRuleCAL	        =	''
            TradeDayRuleRULE	        =	''
            TradeDayRuleBUSD	        =	''
            TradeDayRuleCONV	        =	''
            TradeDayRuleCAL	        =	''

            try:
                DiscountCurveXREF   =       Trade.Currency().MappedRepoLink(t.curr.insid).Value().Link().YieldCurveComponent().Curve().Name()
            except:
                DiscountCurveXREF   =       Trade.Currency().MappedRepoLink(t.curr.insid).Value().Link().YieldCurveComponent().Name()
            
     
    #        sheetType = 'FDealSheet'		
    #        calcSpace = acm.Calculations().CreateCalculationSpace( context, sheetType )		
    #        for leg in ins.Legs():		
    #            columnName = 'Discount Curve'		
    #            curve = calcSpace.CalculateValue( leg, columnName )		
    #            DiscountCurveXREF	=	MR_MainFunctions.NameFix(str(leg.MappedDiscountLink().Link()))

            RepoCurveXREF	=	''
            SpreadOverYldCAL	=	''
            SpreadOverYldDAYC	=	''
            SpreadOverYldFUNC	=	''
            SpreadOverYldPERD	=	''
            SpreadOverYldUNIT	=	''
            SpreadOverYldVAL	=	''
            SpreadOverYldSTRG	=	''
            RM_MapProcFUNC	=	''
            PremiumAtEndVAL	=	''
            TheoModelXREF	=	'PV Zero Coupon Bond'
            MarketModelXREF	=	''
            FairValueModelXREF	=	''
            SettlementProcFUNC	=	''
            
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, NotionalCAL, NotionalDAYC, NotionalFUNC, NotionalPERD, NotionalUNIT, NotionalVAL, NotionalSTRG, MaturityDATE, IssueDATE, StateProcFUNC, TermNB, TermUNIT, TermCAL, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, TradeDayRuleRULE, TradeDayRuleBUSD, TradeDayRuleCONV, TradeDayRuleCAL, DiscountCurveXREF, RepoCurveXREF, SpreadOverYldCAL, SpreadOverYldDAYC, SpreadOverYldFUNC, SpreadOverYldPERD, SpreadOverYldUNIT, SpreadOverYldVAL, SpreadOverYldSTRG, RM_MapProcFUNC, PremiumAtEndVAL, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC))
            
            outfile.close()
            
            if MR_MainFunctions.ValidTradeNo(t) == 0:
                PositionFile.CreatePositionPremium(t, PositionFilename)

    return ''

# WRITE - FILE ######################################################################################################




