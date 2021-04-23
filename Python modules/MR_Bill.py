
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536
2015/11/25: Brendan Bosman - MINT 440

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

    Instrument = acm.FInstrument[i.insaddr]
#    Trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()

    if (i.insaddr) not in InsL:

        InsL.append(i.insaddr)
        outfile = open(filename, 'a')

        #Base record

        BASFLAG             =       'BAS'
        HeaderName          =       'Zero Coupon Bonds'
        OBJECT              =       'Zero Coupon BondSPEC'
        TYPE                =       'Zero Coupon Bonds'

        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()

        NotionalCAL         =       ''
        NotionalDAYC        =       ''
        NotionalFUNC        =       ''
        NotionalPERD        =       ''
        NotionalUNIT        =       Instrument.Currency().Name()

        sheetType                   = 'FTradeSheet'
        calcSpace                   = acm.Calculations().CreateCalculationSpace( context, sheetType )
        columnName                  = 'Trade Nominal'
        NotionalVAL                 = i.contr_size

        NotionalSTRG        =       ''

        MaturityDATE        =       MR_MainFunctions.Datefix(str(Instrument.ExpiryDateOnly()))

        IssueDATE           =       MR_MainFunctions.Datefix(Instrument.StartDate())


        StateProcFUNC       =       '@cash flow generator'
        TermNB              =       ''
        TermUNIT            =       ''
        TermCAL             =       ''

        BusDayRuleRULE      =       ''
        BusDayRuleBUSD      =       ''
        BusDayRuleCONV      =       ''
        BusDayRuleCAL       =       ''
        TradeDayRuleRULE    =       ''
        TradeDayRuleBUSD    =       ''
        TradeDayRuleCONV    =       ''
        TradeDayRuleCAL     =       ''

        DiscountCurveXREF       =       MR_MainFunctions.NameFix(Instrument.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))

        RepoCurveXREF       =       ''
        SpreadOverYldCAL    =       ''
        SpreadOverYldDAYC   =       ''
        SpreadOverYldFUNC   =       ''
        SpreadOverYldPERD   =       ''
        SpreadOverYldUNIT   =       ''
        SpreadOverYldVAL    =       ''
        SpreadOverYldSTRG   =       ''
        RM_MapProcFUNC      =       ''
        PremiumAtEndVAL     =       ''
        TheoModelXREF       =       'PV Zero Coupon Bond'
        MarketModelXREF     =       ''
        FairValueModelXREF  =       ''
        SettlementProcFUNC  =       ''

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, NotionalCAL, NotionalDAYC, NotionalFUNC, NotionalPERD, NotionalUNIT, NotionalVAL, NotionalSTRG, MaturityDATE, IssueDATE, StateProcFUNC, TermNB, TermUNIT, TermCAL, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, TradeDayRuleRULE, TradeDayRuleBUSD, TradeDayRuleCONV, TradeDayRuleCAL, DiscountCurveXREF, RepoCurveXREF, SpreadOverYldCAL, SpreadOverYldDAYC, SpreadOverYldFUNC, SpreadOverYldPERD, SpreadOverYldUNIT, SpreadOverYldVAL, SpreadOverYldSTRG, RM_MapProcFUNC, PremiumAtEndVAL, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC))
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


