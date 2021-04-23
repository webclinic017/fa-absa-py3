
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
CR Number               :289168
''' 
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :316586

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
        HeaderName          =       'European Bond Option'
        OBJECT              =       'EuropeanSPEC'
        TYPE                =       'European'    

        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        
        CallOptionFLAG      =       Instrument.IsCallOption()
        
        ContractSizeVAL     =       Instrument.ContractSize() / Instrument.Underlying().ContractSize()

        StriPric_YieCAL     =       ''
        StriPric_YieDAYC    =       'actual/365'
        StriPric_YieFUNC    =       ''
        StriPric_YiePERD    =       'semi-annual'
        StriPric_YieUNIT    =       '%'
        StriPric_YieVAL     =       Instrument.StrikePrice()
        StriPric_YieSTRG    =       ''
        StrikePriceFUNC     =       '@strike price given yield SA'
        
        SensTypeENUM        =       'spot sensitivity'
        
        UnderlyingXREF      =       'insaddr_'+str(i.und_insaddr.insaddr)
        
        MaturityDATE        =       MR_MainFunctions.Datefix(str(Instrument.ExpiryDateOnly()))

        VolatilityTypeENUM  =       'price volatility'

        VolatilityCAL       =       ''
        VolatilityDAYC      =       'actual/365'
        VolatilityFUNC      =       '@volatility'
        VolatilityPERD      =       'continuous'
        VolatilityUNIT      =       '%'
        VolatilityVAL       =       ''
        VolatilitySTRG      =       ''
        
        VolSurfaceXREF      =       str(Instrument.MappedVolatilityLink().LinkName()) + '_' + str(i.und_insaddr.insid)
        #VolSurfaceXREF      =       Instrument.MappedVolatilityStructure().ParameterName() + '_' + i.und_insaddr.insid
        
        DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        TheoModelXREF       =       'SA Bond Option European'
        
        MarketModelXREF     =       'SA Bond Option European'
        
        FairValueModelXREF  =       ''
        
        SettlementTYPE      =       'Cash Settlement'
        
        SettlementProcFUNC  =       '@SA bond option cash THEO'
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOptionFLAG, ContractSizeVAL, StriPric_YieCAL, StriPric_YieDAYC, StriPric_YieFUNC, StriPric_YiePERD, StriPric_YieUNIT, StriPric_YieVAL, StriPric_YieSTRG, StrikePriceFUNC, SensTypeENUM, UnderlyingXREF, MaturityDATE, VolatilityTypeENUM, VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))

        outfile.close()

        #Position
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################
