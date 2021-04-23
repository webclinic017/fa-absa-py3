'''
Purpose                 :[Market Risk feed files],[]
Department and Desk     :[IT],[MR]
Requester:              :[Natalie Austin],[Susan Kruger]
Developer               :[Douglas Finkel / Henk Nel],[Willie van der Bank]
CR Number               :[264536],[883286]

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''

import ael, string, acm, PositionFile, MR_MainFunctions, SAGEN_IT_TM_Column_Calculation

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
        HeaderName          =       'Inflation Cap Option'
        OBJECT              =       'EuropeanSPEC'
        TYPE                =       'European'
        
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        
        CallOptionFLAG      =       Instrument.IsCallOption()
        
        ContractSizeVAL     =       Instrument.ContractSize()
        
        StrikePriceCAL      =       ''
        StrikePriceDAYC     =       ''
        StrikePriceFUNC     =       ''
        StrikePricePERD     =       ''
        StrikePriceUNIT     =       Instrument.StrikeCurrency().Name()
        
        StrikePriceVAL      =       ''
        if i.und_insaddr.quote_type == 'Per 100 Units':
            StrikePriceVAL      =       Instrument.StrikePrice() / 100
        else:
            StrikePriceVAL      =       Instrument.StrikePrice()
        
        StrikePriceSTRG     =       ''
        
        SpotPriceCAL        =       ''
        SpotPriceDAYC       =       ''
        SpotPriceFUNC       =       ''
        SpotPricePERD       =       ''
        SpotPriceUNIT       =       i.curr.insid
        SpotPriceVAL        =       ''
        SpotPriceSTRG       =       ''

        UnderlyingXREF      =       'insaddr_'+str(i.und_insaddr.insaddr)

        MaturityDATE        =       MR_MainFunctions.Datefix(str(Instrument.ExpiryDateOnly()))

        VolatilityCAL       =       ''
        VolatilityDAYC      =       'actual/365'
        VolatilityFUNC      =       '@volatility'
        VolatilityPERD      =       'annual'
        VolatilityUNIT      =       '%'
        VolSurfaceXREF      =       Instrument.MappedVolatilityLink().LinkName()
        VolatilityVAL       =       ''
        
        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        calc = Instrument.Calculation()

       	if VolSurfaceXREF == 'DEFAULT':
            VolatilityFUNC      =               ''
            VolatilityVAL       =               calc.Volatility(cs)
            VolSurfaceXREF      =               ''


        
        if string.find(str(VolatilityVAL), 'FException'):
            VolatilityVAL = '0.0'

        VolatilitySTRG      =       ''
        VolatltyTypeENUM    =       'price volatility'

        VolatltySpreadCAL   =       ''
        VolatltySpreadDAYC  =       ''
        VolatltySpreadFUNC  =       ''
        VolatltySpreadPERD  =       ''
        VolatltySpreadUNIT  =       ''
        VolatltySpreadVAL   =       ''
        VolatltySpreadSTRG  =       ''
        
        RM_MapProcFUNC      =       ''
        
        if Instrument.PayType() == 'Future':
            DiscountCurveXREF = Instrument.MappedRepoLink(Instrument.Currency()).Link().YieldCurveComponent().Curve().Name()
        else:
            DiscountCurveXREF = SAGEN_IT_TM_Column_Calculation.get_TM_Column_Calculation(None, 'Standard', 'FPortfolioSheet', Instrument.Oid(), 'Instrument', 'Repo Curve Name As String', Instrument.Currency().Name(), 0, None, None)
        
        TheoModelXREF       =       'European Equity Option'
        MarketModelXREF     =       ''
        
        FairValueModelXREF  =       ''
        SettlementTYPE      =       ''
        SettlementProcFUNC  =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'
                      %(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOptionFLAG, ContractSizeVAL,
                        StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, SpotPriceCAL, SpotPriceDAYC,
                        SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, UnderlyingXREF, MaturityDATE, VolatilityCAL, VolatilityDAYC,
                        VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, VolatltyTypeENUM, VolatltySpreadCAL,
                        VolatltySpreadDAYC, VolatltySpreadFUNC, VolatltySpreadPERD, VolatltySpreadUNIT, VolatltySpreadVAL, VolatltySpreadSTRG, RM_MapProcFUNC,
                        DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))

        outfile.close()
        
        #Position

        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################


