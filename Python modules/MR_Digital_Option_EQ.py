
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
    
    Instrument = acm.FInstrument[i.insaddr]
#    Trade = acm.FTrade[t.trdnbr]
    
    e = i.exotic()
    
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')
    
        #Base record
        
        BASFLAG             =       'BAS'
        HeaderName          =       'Digital Equity Option'
        OBJECT              =       'Double BarrierSPEC'
        TYPE                =       'Double Barrier'

        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        StlmntDayRuleBUSD   =       ''
        StlmntDayRuleCAL    =       ''
        StlmntDayRuleCONV   =       ''
        StlmntDayRuleRULE   =       ''
        RebateCAL           =       ''
        RebateDAYC          =       ''
        RebatePERD          =       ''
        RebateUNIT          =       Instrument.Currency().Name()
        
        try:
            RebateVAL           =       Instrument.Rebate().Name()
        except:
            RebateVAL           =       Instrument.Rebate()
            
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        CallOptionFLAG      =       Instrument.IsCallOption()
        ContractSizeVAL     =       ''
        StrikePriceCAL      =       ''
        StrikePriceDAYC     =       ''
        StrikePriceFUNC     =       ''
        StrikePricePERD     =       ''
        StrikePriceUNIT     =       Instrument.StrikeCurrency().Name()
        StrikePriceVAL      =       Instrument.StrikePrice()
        StrikePriceSTRG     =       ''
        SpotPriceCAL        =       ''
        SpotPriceDAYC       =       ''
        SpotPriceFUNC       =       ''
        SpotPricePERD       =       ''
        SpotPriceUNIT       =       ''
        SpotPriceVAL        =       ''
        SpotPriceSTRG       =       ''
        
        UnderlyingXREF      =       'insaddr_'+str(i.und_insaddr.insaddr)
            
        MaturityDATE        =       MR_MainFunctions.Datefix(str(Instrument.ExpiryDateOnly()))
        
        VolatilityCAL       =       ''
        VolatilityDAYC      =       'actual/365'
        VolatilityFUNC      =       '@volatility THEO'
        VolatilityPERD      =       'annual'
        VolatilityUNIT      =       '%'
        VolatilityVAL       =       ''
        VolatilitySTRG      =       ''
        #VolSurfaceXREF      =       Instrument.MappedVolatilityStructure().ParameterName()
        VolSurfaceXREF      =       Instrument.MappedVolatilityLink().LinkName()        
        
        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        calc = Instrument.Calculation()

        
        #if (Instrument.MappedVolatilityStructure().ParameterName()) == 'DEFAULT':
        if (Instrument.MappedVolatilityLink().LinkName()) == 'DEFAULT':
            VolatilityFUNC      =               ''
            VolatilityVAL       =               calc.Volatility(cs)
            VolSurfaceXREF      =               ''
  


        RM_MapProcFUNC      =       ''
        
        
        try:
            DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        
        SettlementTYPE      =       ''
        SettlementProcFUNC  =       ''
        TheoModelXREF       =       'Double Barrier'
        MarketModelXREF     =       ''
        FairValueModelXREF  =       ''

       
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'
                      %(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, StlmntDayRuleBUSD, StlmntDayRuleCAL, StlmntDayRuleCONV, StlmntDayRuleRULE, RebateCAL, RebateDAYC, RebatePERD, RebateUNIT, RebateVAL, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOptionFLAG, ContractSizeVAL, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, UnderlyingXREF, MaturityDATE, VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, RM_MapProcFUNC, DiscountCurveXREF, SettlementTYPE, SettlementProcFUNC, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
        outfile.close()

        #Position
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################
