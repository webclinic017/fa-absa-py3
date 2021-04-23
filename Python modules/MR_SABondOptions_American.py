
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536
'''

'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :278978
'''

'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :289168

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
        HeaderName          =       'American Bond Option'
        OBJECT              =       'AmericanSPEC'
        TYPE                =       'American'    
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        
        CallOptionFLAG      =       Instrument.IsCall()    
        
        ContractSizeVAL     =       Instrument.ContractSize() / Instrument.Underlying().ContractSize()

        StrikePriceCAL      =       ''
        StrikePriceDAYC     =       ''
        StrikePriceFUNC     =       '@strike price given yield SA'
        StrikePricePERD     =       ''
        StrikePriceUNIT     =       Instrument.Currency().Name()
        StrikePriceVAL      =       ''
        StrikePriceSTRG     =       ''
        
        StriPric_YieCAL     =       ''
        StriPric_YieDAYC    =       'actual/365'
        StriPric_YieFUNC    =       ''
        StriPric_YiePERD    =       'semi-annual'
        StriPric_YieUNIT    =       '%'
        StriPric_YieVAL     =       Instrument.StrikePrice()
        StriPric_YieSTRG    =       ''
        
        SensTypeENUM        =       'spot sensitivity'

        UnderlyingXREF      =       'insaddr_'+str(i.und_insaddr.insaddr)
        
        MaturityDATE        =       MR_MainFunctions.Datefix(str(Instrument.ExpiryDateOnly()))

        VolatltyTypeENUM    =       'price volatility'

        VolatilityCAL       =       ''
        VolatilityDAYC      =       'actual/365'
        VolatilityFUNC      =       '@volatility THEO'
        VolatilityPERD      =       'continuous'
        VolatilityUNIT      =       '%'
        VolatilityVAL       =       ''
        VolatilitySTRG      =       ''
        VolSurfaceXREF      =       Instrument.MappedVolatilityLink().LinkName() + '_' + i.und_insaddr.insid
        #VolSurfaceXREF      =       Instrument.MappedVolatilityStructure().ParameterName() + '_' + i.und_insaddr.insid
        
        DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        TheoModelXREF       =       'SA Bond Option American'
        
        MarketModelXREF     =       'SA Bond Option American'
        
        FairValueModelXREF  =       ''
        
        SettlementTYPE      =       ''
        
        SettlementProcFUNC  =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'
                      %(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOptionFLAG, ContractSizeVAL, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, StriPric_YieCAL, StriPric_YieDAYC, StriPric_YieFUNC, StriPric_YiePERD, StriPric_YieUNIT, StriPric_YieVAL, StriPric_YieSTRG, SensTypeENUM, UnderlyingXREF, MaturityDATE, VolatltyTypeENUM, VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))
                      
        outfile.close()

        #Position
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################
