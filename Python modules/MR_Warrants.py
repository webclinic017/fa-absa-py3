
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536

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



# WRITE - EQ WARRANTS ###############################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName

    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        
        outfile = open(filename, 'a')
        
        ins = acm.FInstrument[i.insaddr]
#        trade = acm.FTrade[t.trdnbr]
        context = acm.GetDefaultContext()
        
        #Base record
        BASFLAG                 =       'BAS'
        HeaderName              =       'Warrant'
        OBJECT                  =       'EuropeanSPEC'
        TYPE                    =       'European'
        NAME                    =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER              =       'insaddr_'+str(i.insaddr)
        CurrencyCAL             =       ''
        CurrencyDAYC            =       ''
        CurrencyPERD            =       ''
        CurrencyUNIT            =       i.curr.insid
        CallOptionFLAG          =       MR_MainFunctions.TrueFalse(i.call_option)
        ContractSizeVAL         =       i.contr_size
        StrikePriceCAL          =       ''
        StrikePriceDAYC         =       ''
        StrikePriceFUNC         =       ''
        StrikePricePERD         =       ''
        StrikePriceUNIT         =       i.strike_curr.insid
        StrikePriceVAL          =       i.strike_price
        StrikePriceSTRG         =       ''
        SpotPriceCAL            =       ''
        SpotPriceDAYC           =       ''
        SpotPriceFUNC           =       ''
        SpotPricePERD           =       ''
        SpotPriceUNIT           =       i.curr.insid
        SpotPriceVAL            =       ''#t.price
        SpotPriceSTRG           =       ''
        UnderlyingXREF          =       'insaddr_'+str(i.und_insaddr.insaddr)
        MaturityDATE            =       MR_MainFunctions.Datefix(i.exp_day)
        VolatilityCAL           =       ''
        VolatilityDAYC          =       'actual/365'
        VolatilityFUNC          =       '@volatility'
        VolatilityPERD          =       'annual'
        VolatilityUNIT          =       '%'
        
        #VolSurfaceXREF      =       ins.MappedVolatilityStructure().ParameterName()
        VolSurfaceXREF      =       ins.MappedVolatilityLink().LinkName()
        VolatilityVAL       =       ''
        
        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        calc = ins.Calculation()

       	if VolSurfaceXREF == 'DEFAULT':
            VolatilityFUNC      =       ''
            VolatilityVAL       =       calc.Volatility(cs)
            VolSurfaceXREF      =       ''
        
        VolatilitySTRG          =       ''
        #VolSurfaceXREF          =       ins.MappedVolatilityStructure().Parameter().Name()
        #VolatilityTypeENUM      =       'price vol'
        VolatltySpreadCAL       =       ''
        VolatltySpreadDAYC      =       ''
        VolatltySpreadFUNC      =       ''
        VolatltySpreadPERD      =       ''
        VolatltySpreadUNIT      =       ''
        VolatltySpreadVAL       =       ''
        VolatltySpreadSTRG      =       ''
        DaysPerTimeStepNB       =       ''
        DiscountCurveXREF       =       MR_MainFunctions.NameFix(ins.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        #RepoCurveXREF           =       MR_MainFunctions.NameFix(ins.MappedRepoLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        TheoModelXREF           =       'European Equity Option'
        MarketModelXREF         =       ''
        FairValueModelXREF      =       ''
        SettlementTYPE          =       ''
        SettlementProcFUNC      =       ''

        #outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG,HeaderName,OBJECT,TYPE,NAME,IDENTIFIER,CurrencyCAL,CurrencyDAYC,CurrencyPERD,CurrencyUNIT,CallOptionFLAG,ContractSizeVAL,StrikePriceCAL,StrikePriceDAYC,StrikePriceFUNC,StrikePricePERD,StrikePriceUNIT,StrikePriceVAL,StrikePriceSTRG,SpotPriceCAL,SpotPriceDAYC,SpotPriceFUNC,SpotPricePERD,SpotPriceUNIT,SpotPriceVAL,SpotPriceSTRG,UnderlyingXREF,MaturityDATE,VolatilityCAL,VolatilityDAYC,VolatilityFUNC,VolatilityPERD,VolatilityUNIT,VolatilityVAL,VolatilitySTRG,VolSurfaceXREF,VolatilityTypeENUM,VolatltySpreadCAL,VolatltySpreadDAYC,VolatltySpreadFUNC,VolatltySpreadPERD,VolatltySpreadUNIT,VolatltySpreadVAL,VolatltySpreadSTRG,DaysPerTimeStepNB,DiscountCurveXREF,RepoCurveXREF,TheoModelXREF,MarketModelXREF,FairValueModelXREF,SettlementTYPE,SettlementProcFUNC))
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOptionFLAG, ContractSizeVAL, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, UnderlyingXREF, MaturityDATE, VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, VolatltySpreadCAL, VolatltySpreadDAYC, VolatltySpreadFUNC, VolatltySpreadPERD, VolatltySpreadUNIT, VolatltySpreadVAL, VolatltySpreadSTRG, DaysPerTimeStepNB, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))
        outfile.close()
        #Position

        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid
    
# WRITE - NCD #######################################################################################################



