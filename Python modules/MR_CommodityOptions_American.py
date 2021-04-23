
'''
Purpose                 :[Market Risk feed files],[Amended VolSurfaceXREF]
Department and Desk     :[IT],[MR]
Requester:              :[Natalie Austin],[Susan Kruger]
Developer               :[Douglas Finkel],[Willie van der Bank]
CR Number               :[264536,394236,489655],[792659 07/10/2011]

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
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        outfile = open(filename, 'a')

        #Base record
        
        BASFLAG             =       'BAS'
        HeaderName          =       'American Commodity Option'
        OBJECT              =       'AmericanSPEC'
        TYPE                =       'American'    

        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        
        CallOptionFLAG      =       Instrument.IsCallOption()
        
        if Instrument.Underlying().InsType() == 'ETF':
            ContractSizeVAL     =       Instrument.ContractSize() / Instrument.Underlying().Underlying().ContractSize()
        else:
            ContractSizeVAL     =       Instrument.ContractSize() / Instrument.Underlying().ContractSize()
            
        StrikePriceCAL      =       ''
        StrikePriceDAYC     =       ''
        StrikePriceFUNC     =       ''
        StrikePricePERD     =       ''
        StrikePriceUNIT     =       Instrument.StrikeCurrency().Name()
        StrikePriceVAL      =       Instrument.StrikePrice() / Instrument.ContractSize()
        StrikePriceSTRG     =       ''
        
        SpotPriceCAL        =       ''
        SpotPriceDAYC       =       ''
        SpotPriceFUNC       =       ''
        SpotPricePERD       =       ''
        SpotPriceUNIT       =       i.curr.insid #Trade.Currency().Name()
        SpotPriceVAL        =       '' #Trade.Price()       
        SpotPriceSTRG       =       ''
        
        
        if i.und_insaddr.instype == 'ETF':
            UndInst = ael.Instrument[i.und_insaddr.insaddr]
            UndUndInst = ael.Instrument[UndInst.und_insaddr.insaddr]
            UnderlyingXREF      =       'insaddr_'+str(UndUndInst.insaddr)
        else:
            UnderlyingXREF      =       'insaddr_'+str(i.und_insaddr.insaddr)
        
        MaturityDATE        =       MR_MainFunctions.Datefix(str(Instrument.ExpiryDateOnly()))
        
        VolatilityCAL       =       ''
        VolatilityDAYC      =       'actual/365'
        VolatilityFUNC      =       '@volatility'
        VolatilityPERD      =       'annual'
        VolatilityUNIT      =       '%'
        VolatilityVAL       =       ''
        VolatilitySTRG      =       ''
        
        VolSurfaceXREF      =       Instrument.MappedVolatilityLink().LinkName()
        #VolSurfaceXREF      =       Instrument.MappedVolatilityStructure().ParameterName()
        #VolSurfaceXREF      =       ins.MappedVolatilityLink().LinkName()

        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        calc = Instrument.Calculation()

       	if VolSurfaceXREF == 'DEFAULT':
            VolatilityFUNC      =               ''
            VolatilityVAL       =               calc.Volatility(cs)
            VolSurfaceXREF      =               ''
        
        if string.find(str(VolatilityVAL), 'FException'):
            VolatilityVAL = '0.0'
        
        VolatltySpreadCAL   =       ''
        VolatltySpreadDAYC  =       ''
        VolatltySpreadFUNC  =       ''
        VolatltySpreadPERD  =       ''
        VolatltySpreadUNIT  =       ''
        VolatltySpreadVAL   =       ''
        VolatltySpreadSTRG  =       ''
        
        VolatltyTypeENUM    =       'price volatility'
        
        DaysPerTimeStepNB   =       ''
        
        RM_MapProcFUNC      =       ''
        
        DiscountCurveXREF   =       acm.FInstrument[i.curr.insaddr].MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        TheoModelXREF       =       'American Future Option'
        
        MarketModelXREF     =       ''
        
        FairValueModelXREF  =       ''
        
        SettlementTYPE      =       ''
        
        SettlementProcFUNC  =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'
                      %(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOptionFLAG, ContractSizeVAL,
                        StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, SpotPriceCAL,
                        SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, UnderlyingXREF, MaturityDATE, VolatilityCAL,
                        VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, VolatltySpreadCAL,
                        VolatltySpreadDAYC, VolatltySpreadFUNC, VolatltySpreadPERD, VolatltySpreadUNIT, VolatltySpreadVAL, VolatltySpreadSTRG, VolatltyTypeENUM,
                        DaysPerTimeStepNB, RM_MapProcFUNC, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))

        outfile.close()

        #Position
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################
