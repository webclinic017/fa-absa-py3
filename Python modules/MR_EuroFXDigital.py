'''
Purpose                 :Market Risk feed files
Department and Desk     :IT, Market Risk
Requester:              :Natalie Austin, Susan Kruger
Developer               :Douglas Finkel, Susan Kruger
CR Number               :264536, 275268, 714504, CHNG0000834576

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
#    calc = Trade.Calculation()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')

        #Base record
        
        BASFLAG             =       'BAS'
        HeaderName          =       'Digital FX Option'
        OBJECT              =       'Single BarrierSPEC'
        TYPE                =       'Single Barrier'
        
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)

        StlmntDayRuleBUSD   =       ''
        StlmntDayRuleCAL    =       ''
        StlmntDayRuleCONV   =       ''
        StlmntDayRuleRULE   =       ''
        
        RebateCAL           =       ''
        RebateDAYC          =       ''
        RebatePERD          =       ''
        RebateUNIT          =       ''
        RebateVAL           =       1   
        
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.StrikeCurrency().Name()
        
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
        SpotPriceUNIT       =       ''
        SpotPriceVAL        =       ''
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
        VolatilityPERD      =       'continuous'
        VolatilityUNIT      =       ''
        VolatilityVAL       =       ''
        VolatilitySTRG      =       ''

        #VolSurfaceXREF      =       Instrument.MappedVolatilityStructure().ParameterName()
        VolSurfaceXREF      =       Instrument.MappedVolatilityLink().LinkName()
        
        RM_MapProcFUNC      =       ''
        
        try:
            DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()    
        except:
            DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()        
        SettlementTYPE      =       ''
        SettlementProcFUNC  =       ''      

        TheoModelXREF       =       'Digital Cash Option'
        
        MarketModelXREF     =       ''
        
        FairValueModelXREF  =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'
                      %(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, StlmntDayRuleBUSD, StlmntDayRuleCAL, StlmntDayRuleCONV, StlmntDayRuleRULE, RebateCAL,
                        RebateDAYC, RebatePERD, RebateUNIT, RebateVAL, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOptionFLAG, ContractSizeVAL,
                        StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, SpotPriceCAL,
                        SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, OutputCurrencyCAL, OutputCurrencyDAYC,
                        OutputCurrencyPERD, OutputCurrencyUNIT, UnderlyingXREF, MaturityDATE, VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD,
                        VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, RM_MapProcFUNC, DiscountCurveXREF, SettlementTYPE, SettlementProcFUNC,
                        TheoModelXREF, MarketModelXREF, FairValueModelXREF))

        outfile.close()

        #Position
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################

