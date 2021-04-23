
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536, 275268, 714504

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
        HeaderName          =       'FX European Option'
        OBJECT              =       'EuropeanSPEC'
        TYPE                =       'European'
        
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)

        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.StrikeCurrency().Name() #Instrument.Currency().Name()
        
        CallOptionFLAG      =       Instrument.IsCallOption()    
        
        ContractSizeVAL     =       Instrument.ContractSize()

        StrikePriceCAL      =       ''
        StrikePriceDAYC     =       ''
        StrikePriceFUNC     =       ''
        StrikePricePERD     =       ''
        StrikePriceUNIT     =       Instrument.StrikeCurrency().Name()

        if Instrument.StrikeQuotation():
            if Instrument.StrikeQuotation().Name() == 'Per Unit Inverse':
                StrikePriceVAL = 1/Instrument.StrikePrice()
            else:
                StrikePriceVAL = Instrument.StrikePrice()
        else:
            StrikePriceVAL = Instrument.StrikePrice()
        
        StrikePriceSTRG     =       ''
        
        SpotPriceCAL        =       ''
        SpotPriceDAYC       =       ''
        SpotPriceFUNC       =       ''
        SpotPricePERD       =       ''
        SpotPriceUNIT       =       i.curr.insid #Trade.Currency().Name()
        SpotPriceVAL        =       '' #Trade.Price()       
        SpotPriceSTRG       =       ''
        
        OutputCurrencyCAL   =       ''
        OutputCurrencyDAYC  =       ''
        OutputCurrencyPERD  =       ''
        OutputCurrencyUNIT  =       ''

        UnderlyingXREF      =       'insaddr_'+str(i.und_insaddr.insaddr)
        
        MaturityDATE        =       MR_MainFunctions.Datefix(str(Instrument.ExpiryDateOnly()))

        VolatilityCAL       =       ''
        VolatilityDAYC      =       'actual/365'
        VolatilityFUNC      =       '@volatility THEO'
        VolatilityPERD      =       'annual'
        VolatilityUNIT      =       '%'
        VolatilityVAL       =       ''
        VolatilitySTRG      =       ''
        
        #VolSurfaceXREF      =       Instrument.MappedVolatilityStructure().ParameterName() # + MR_MainFunctions.AppendOptionType(Instrument)
        VolSurfaceXREF      =       Instrument.MappedVolatilityLink().LinkName()        
        if VolSurfaceXREF == 'DEFAULT':
            VolSurfaceXREF = 'None'

        VolatilityTypeENUM  =       'price volatility'
        
        RM_MapProcFUNC      =       ''

        try:
            DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        TheoModelXREF       =       'European FX option no calib'
        
        MarketModelXREF     =       ''
        
        FairValueModelXREF  =       ''
        
        SettlementTYPE      =       ''
        
        SettlementProcFUNC  =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'
                      %(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOptionFLAG, ContractSizeVAL, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, OutputCurrencyCAL, OutputCurrencyDAYC, OutputCurrencyPERD, OutputCurrencyUNIT, UnderlyingXREF, MaturityDATE, VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, VolatilityTypeENUM, RM_MapProcFUNC, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))
        
        outfile.close()
        
        #Position
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################
