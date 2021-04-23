
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



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName

    ins = acm.FInstrument[i.insaddr]
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')
        
        #Base record
        
        BASFLAG                 =       'BAS'
        HeaderName              =       'Eur FX Future Option' 
        OBJECT                  =       'EuropeanSPEC'
        TYPE                    =       'European'

        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL             =       ''
        CurrencyDAYC            =       ''
        CurrencyPERD            =       ''
        CurrencyUNIT            =       i.curr.insid
        
        CallOptionFLAG          =       'TRUE'
        ContractSizeVAL         =       ''
        
        StrikePriceCAL          =       ''
        StrikePriceDAYC         =       ''
        StrikePriceFUNC         =       ''
        StrikePricePERD         =       ''
        StrikePriceUNIT         =       i.curr.insid
        StrikePriceVAL          =       '' #trade.Price()
        StrikePriceSTRG         =       ''
        
        SpotPriceCAL            =       ''
        SpotPriceDAYC           =       ''
        SpotPriceFUNC           =       ''
        SpotPricePERD           =       ''
        SpotPriceUNIT           =       i.curr.insid
        SpotPriceVAL            =       ''
        SpotPriceSTRG           =       ''
        
        OutputCurrencyCAL       =       ''
        OutputCurrencyDAYC      =       ''
        OutputCurrencyPERD      =       ''
        OutputCurrencyUNIT      =       ''
        
      
      
        UnderlyingXREF      =       'insaddr_'+str(i.und_insaddr.insaddr)
            
        
        MaturityDATE            =       MR_MainFunctions.Datefix(i.exp_day)
        
        VolatilityCAL           =       ''
        VolatilityDAYC          =       'actual/365'
        VolatilityFUNC          =       '@volatility THEO'
        VolatilityPERD          =       'annual'
        VolatilityUNIT          =       '%'
        VolatilityVAL           =       ''
        VolatilitySTRG          =       ''
        #VolSurfaceXREF          =       ins.MappedVolatilityStructure().ParameterName()
        VolSurfaceXREF          =       ins.MappedVolatilityLink().LinkName()
   
        RM_MapProcFUNC          =       ''
        
        try:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
             
        
        TheoModelXREF           =       'European Future Option'
        MarketModelXREF         =       ''
        FairValueModelXREF      =       ''
        SettlementTYPE          =       ''
        SettlementProcFUNC      =       ''

        
     
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOptionFLAG, ContractSizeVAL, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, OutputCurrencyCAL, OutputCurrencyDAYC, OutputCurrencyPERD, OutputCurrencyUNIT, UnderlyingXREF, MaturityDATE, VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, RM_MapProcFUNC, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))
        
        
        outfile.close()

        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################


