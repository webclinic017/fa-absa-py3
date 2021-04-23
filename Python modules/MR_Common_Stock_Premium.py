
'''

#AEL module to produce Market Risk output files
#
#Input Variables:
#   FileDir 		- The drive where the output will be located
#   Filename 		- The name of the file that will be output
#   Object		    - The object that is sent from the equivalent ASQL to this AEL
#
#Requires Python installation on client PC.
#
#Created by
#Douglas Finkel - 2010/03/25
#Updated - Douglas Finkel - Add additional functionality

Purpose                 :Market Risk feed files, Added Exception handling for mtm_price
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel, Heinrich Cronje
CR Number               :264536,278978,569014, 683021

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-01-20     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-427
'''


import ael, string, acm, MR_PositionFile, MR_MainFunctions

InsL = []

# OPENFILE ##########################################################################################################
# Creates the file for the output
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

def Write(exch,FileDir,Filename,PositionName,Ccy,AcquireDay,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    i = acm.FInstrument[exch.insaddr]
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if ('Forward_' + str(Ccy) + '_' + str(AcquireDay)) not in InsL:
        InsL.append(('Forward_' + str(Ccy) + '_' + str(AcquireDay)))

        #Base record
        outfile = open(filename, 'a')
        BASFLAG	        =	'BAS'
        HeaderName	        =	'Zero Coupon Bonds'
        OBJECT	        =	'Zero Coupon BondSPEC'
        TYPE	        =	'Zero Coupon Bond'

        NAME                =       'Forward_' + str(Ccy) + '_' + str(AcquireDay)
        IDENTIFIER          =       'Forward_' + str(Ccy) + '_' + str(AcquireDay)

        CurrencyCAL	        =	''
        CurrencyDAYC	=	''
        CurrencyPERD	=	''
        CurrencyUNIT	=	MR_MainFunctions.NameFix(exch.insid)
        NotionalCAL	        =	''
        NotionalDAYC	=	''
        NotionalFUNC	=	''
        NotionalPERD	=	''
        NotionalUNIT	=	MR_MainFunctions.NameFix(exch.insid)

        sheetType       = 'FTradeSheet'		
        calcSpace       = acm.Calculations().CreateCalculationSpace( context, sheetType )		
        columnName      = 'Trade Nominal'		
        NotionalVAL     = 1
        
        NotionalSTRG    =	''

        		
        MaturityDATE        =	MR_MainFunctions.Datefix(AcquireDay)
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
            DiscountCurveXREF   =       i.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       i.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
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

    return ''

# WRITE - FILE ######################################################################################################
