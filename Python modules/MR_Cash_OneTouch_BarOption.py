
'''
Purpose                 :Market Risk feed files,[Ammended to give the correct model name]
Department and Desk     :IT
Requester:              :Natalie Austin,Susan Kruger
Developer               :Douglas Finkel,Tshepo Mabena
CR Number               :264536, 714504,[824244 - 919,952,1037,1054] 

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

        BASFLAG	        =	'BAS'
        HeaderName	        =	'Single Barrier'
        OBJECT	        =	'Single BarrierSPEC'
        TYPE	        =	'Single Barrier'
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        BarDirectionENUM        =       'Up'                
        if (ins.Exotics().First().BarrierOptionType() == 'Up & In')|(ins.Exotics().First().BarrierOptionType() == 'Up & Out'):
            BarDirectionENUM        =       'Up'
        elif (ins.Exotics().First().BarrierOptionType() == ''):
            BarDirectionENUM        =       'None'
        else:
            BarDirectionENUM        =       'Down'


        BarStartDateDATE        =       ins.StartDate()
        BarrierEndDATE          =       ins.ExpiryDateOnly()
        KnockoutFLAG        =       'False'
        
        if (ins.Exotics().First().BarrierOptionType() == 'Down & In')|(ins.Exotics().First().BarrierOptionType() == 'Up & In'):
                KnockoutFLAG        =       'False'
        elif (ins.Exotics().First().BarrierOptionType() == ''):
            KnockoutFLAG        =       'None'
        else:
            KnockoutFLAG        =       'True'

        
        ObservationFrqNB	=	''
        ObsRuleENUM	        =	''

        #ACM returns True - (Pay At Expiry) write to file False
        #ACM returns False - (Pay At Hit) write to file true
        if ins.Exotic().BarrierRebateOnExpiry() == 'True':
            PayAtBreachFLAG	=	'False'
        else:
            PayAtBreachFLAG	=	'True'
            
        StlmntDayRuleBUSD	=	''
        StlmntDayRuleCAL	=	''
        StlmntDayRuleCONV	=	''
        StlmntDayRuleRULE	=	''
        RebateCAL	        =	''
        RebateDAYC	        =	''
        RebatePERD	        =	''
        RebateUNIT	        =	ins.StrikeCurrency().Name()
        RebateVAL	        =	'1'
        CurrencyCAL	        =	''
        CurrencyDAYC	        =	''
        CurrencyPERD	        =	''
        CurrencyUNIT	        =	ins.StrikeCurrency().Name()
        CallOptionFLAG	        =	ins.IsCall()
        ContractSizeVAL	        =	ins.ContractSize()
        StrikePriceCAL	        =	''
        StrikePriceDAYC 	=	''
        StrikePriceFUNC	        =	''
        StrikePricePERD	        =	''
        StrikePriceUNIT	        =	ins.StrikeCurrency().Name()
        
        if ins.Underlying().InsType() in ('Curr'):
            if ins.StrikeQuotation():
                if ins.StrikeQuotation().Name() == 'Per Unit Inverse':
                    StrikePriceVAL = 1/ins.StrikePrice()
                else:
                    StrikePriceVAL = ins.StrikePrice()
            else:
                StrikePriceVAL = ins.StrikePrice()
        else:
            StrikePriceVAL	    =       ins.StrikePrice()
        
        StrikePriceSTRG	        =	''
        BarrierCAL	        =	''
        BarrierDAYC	        =	''
        BarrierHitFLAG	        =	''
        BarrierPERD	        =	''
        BarrierUNIT	        =	ins.StrikeCurrency().Name()
        BarrierVAL	        =	ins.Barrier()
        SpotPriceCAL	        =	''
        SpotPriceDAYC	        =	''
        SpotPriceFUNC	        =	''
        SpotPricePERD	        =	''
        SpotPriceUNIT	        =	''
        SpotPriceVAL	        =	''
        SpotPriceSTRG	        =	''
        OutputCurrencyCAL	=	''
        OutputCurrencyDAYC	=	''
        OutputCurrencyPERD	=	''
        OutputCurrencyUNIT	=	''
        UnderlyingXREF	        =	'insaddr_'+str(i.und_insaddr.insaddr)
        MaturityDATE	        =	MR_MainFunctions.Datefix(i.exp_day)
        VolatilityCAL	        =	''
        VolatilityDAYC	        =       'actual/365'
        VolatilityFUNC	        =       '@volatility THEO'
        VolatilityPERD	        =       'continuous'
        VolatilityUNIT	        =       '%'
        VolatilityVAL	        =	''
        VolatilitySTRG	        =	''
        
        #VolSurfaceXREF      =       Instrument.MappedVolatilityStructure().ParameterName()
        VolSurfaceXREF      =       ins.MappedVolatilityLink().LinkName()
        
        VolatltySpreadCAL	=	''
        VolatltySpreadDAYC	=	''
        VolatltySpreadFUNC	=	''
        VolatltySpreadPERD	=	''
        VolatltySpreadUNIT	=	''
        VolatltySpreadVAL	=	''
        VolatltySpreadSTRG	=	''
        RM_MapProcFUNC	        =	''
        DiscountCurveXREF	=	MR_MainFunctions.NameFix(ins.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        SettlementTYPE	        =	''
        SettlementProcFUNC	=	''
        TheoModelXREF	        =	'Binary Cash Barrier'
        MarketModelXREF	        =	''
        FairValueModelXREF	=	''

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, BarDirectionENUM, BarStartDateDATE, BarrierEndDATE, KnockoutFLAG, ObservationFrqNB, ObsRuleENUM, PayAtBreachFLAG, StlmntDayRuleBUSD, StlmntDayRuleCAL, StlmntDayRuleCONV, StlmntDayRuleRULE, RebateCAL, RebateDAYC, RebatePERD, RebateUNIT, RebateVAL, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOptionFLAG, ContractSizeVAL, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, BarrierCAL, BarrierDAYC, BarrierHitFLAG, BarrierPERD, BarrierUNIT, BarrierVAL, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, OutputCurrencyCAL, OutputCurrencyDAYC, OutputCurrencyPERD, OutputCurrencyUNIT, UnderlyingXREF, MaturityDATE, VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, VolatltySpreadCAL, VolatltySpreadDAYC, VolatltySpreadFUNC, VolatltySpreadPERD, VolatltySpreadUNIT, VolatltySpreadVAL, VolatltySpreadSTRG, RM_MapProcFUNC, DiscountCurveXREF, SettlementTYPE, SettlementProcFUNC, TheoModelXREF, MarketModelXREF, FairValueModelXREF))

        #Roll over
        
        BASFLAG	=	'rm_ro'
        HeaderName	=	'Single Barrier : Observation Dates'
        ATTRIBUTE	=	'Observation Dates'
        OBJECT	=	'Single BarrierSPEC'
        ObsDatesDATE	=	''


        outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ObsDatesDATE))

        outfile.close()
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################
