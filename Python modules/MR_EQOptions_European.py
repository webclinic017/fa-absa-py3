'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536, 275268, 316586, 707888

Change history:
===============

2015-02-11  FA-Upgrade-2014 Peter Basista   Fix a change in FInstrument.
                                            MappedDiscountLink API

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
        HeaderName          =       'European Equity Option'
        OBJECT              =       'EuropeanSPEC'
        TYPE                =       'European'
        
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        
        CallOptionFLAG      =       Instrument.IsCallOption()
        
        if Instrument.Underlying().InsType() == 'Future/Forward':
            ContractSizeVAL     =       Instrument.ContractSize() / Instrument.Underlying().ContractSize()
	else:	
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
        SpotPriceUNIT       =       i.curr.insid #Trade.Currency().Name()
        SpotPriceVAL        =       '' #Trade.Price()       
        SpotPriceSTRG       =       ''

        UnderlyingXREF      =       'insaddr_'+str(i.und_insaddr.insaddr)

        MaturityDATE        =       MR_MainFunctions.Datefix(str(Instrument.ExpiryDateOnly()))

        VolatilityCAL       =       ''
        VolatilityDAYC      =       'actual/365'
        VolatilityFUNC      =       '@volatility'
        VolatilityPERD      =       'annual'
        VolatilityUNIT      =       '%'
        #VolSurfaceXREF      =       Instrument.MappedVolatilityStructure().ParameterName()
        VolSurfaceXREF      =       Instrument.MappedVolatilityLink().LinkName()
        if VolSurfaceXREF == 'DEFAULT':
            VolSurfaceXREF = None
        VolatilityVAL       =       ''
        
        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        calc = Instrument.Calculation()


        
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
            if Instrument.Underlying().InsType() =='Future/Forward':
                DiscountCurveXREF   =  'FLAT - 0%'
            else:
                DiscountCurveXREF   = Instrument.MappedRepoLink(Instrument.Currency()).Link().YieldCurveComponent().Curve().Name()
	else:
            try:
                DiscountCurveXREF   = Instrument.MappedDiscountLink(Instrument.Currency(), False, None).Link().YieldCurveComponent().Name()    
            except:
                DiscountCurveXREF   = Instrument.MappedDiscountLink(Instrument.Currency(), False, None).Link().YieldCurveComponent().Curve().Name()  
        
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


