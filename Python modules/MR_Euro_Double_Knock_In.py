
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536, 714504

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
        
        BASFLAG             =       'BAS'
        HeaderName          =       'Double Barrier'
        OBJECT              =       'Double BarrierSPEC'
        TYPE                =       'Double Barrier'

        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        BarStartDateDATE    =       ins.StartDate()
        BarrierEndDATE      =       ins.ExpiryDateOnly()

        KnockoutFLAG        =       ''
        if (ins.Exotics().First().BarrierOptionType() == 'Double In'):
                KnockoutFLAG        =       'False'
        elif (ins.Exotics().First().BarrierOptionType() == 'Double Out'):
            KnockoutFLAG        =       'True'
        else:
            KnockoutFLAG        =       ''

        ObservationFrqNB    =       ''
        ObsRuleENUM         =       ''

        #ACM returns True - (Pay At Expiry) write to file False
        #ACM returns False - (Pay At Hit) write to file true
        if ins.Exotic().BarrierRebateOnExpiry() == 'True':
            PayAtBreachFLAG	=	'False'
        else:
            PayAtBreachFLAG	=	'True'

        StlmntDayRuleBUSD   =       ''
        StlmntDayRuleCAL    =       ''
        StlmntDayRuleCONV   =       ''
        StlmntDayRuleRULE   =       ''

        RebateCAL           =       ''
        RebateDAYC          =       ''
        RebatePERD          =       ''
        RebateUNIT          =       ins.StrikeCurrency().Name()
        RebateVAL           =       ins.Rebate()

        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       ins.StrikeCurrency().Name()

        CallOptionFLAG      =       ins.IsCall()
        ContractSizeVAL     =       ins.ContractSize()

        StrikePriceCAL      =       ''
        StrikePriceDAYC     =       ''
        StrikePriceFUNC     =       ''
        StrikePricePERD     =       ''
        StrikePriceUNIT     =       ''
        
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
        
        StrikePriceSTRG     =       ''

        BarrierHitFLAG      =       ''
        BarrierCAL          =       ''
        BarrierDAYC         =       ''
        BarrierPERD         =       ''
        BarrierUNIT         =       ins.StrikeCurrency().Name()
        BarrierVAL = ''
        if ins.Barrier() >= ins.Exotic().DoubleBarrier():
            BarrierVAL = ins.Barrier()
        else:
            BarrierVAL = ins.Exotic().DoubleBarrier()



        DownBarrierCAL      =       ''
        DownBarrierDAYC     =       ''
        DownBarrierPERD     =       ''
        DownBarrierUNIT     =       ins.StrikeCurrency().Name()
        DownBarrierVAL = ''
        if ins.Barrier() >= ins.Exotic().DoubleBarrier():
            DownBarrierVAL = ins.Exotic().DoubleBarrier()
        else:
            DownBarrierVAL = ins.Barrier()



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
        
        Legs = i.legs()
        for l in Legs:
            if l.payleg == 1:
                UnderlyingXREF 	=	'SCI_' + str(getattr(l, 'float_rate')) + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
                    
        MaturityDATE        =       MR_MainFunctions.Datefix(i.exp_day)
 
        VolatilityCAL       =       ''
        VolatilityDAYC      =       'actual/365'
        VolatilityFUNC      =       '@volatility THEO'
        VolatilityPERD      =       'continuous'
        VolatilityUNIT      =       '%'
        VolatilityVAL       =       0.0
        VolatilitySTRG      =       ''

        #VolSurfaceXREF      =       Instrument.MappedVolatilityStructure().ParameterName()
        VolSurfaceXREF      =       ins.MappedVolatilityLink().LinkName()
        
        VolatltySpreadCAL   =       ''
        VolatltySpreadDAYC  =       ''
        VolatltySpreadFUNC  =       ''
        VolatltySpreadPERD  =       ''
        VolatltySpreadUNIT  =       ''
        VolatltySpreadVAL   =       ''
        VolatltySpreadSTRG  =       ''

        RM_MapProcFUNC      =       ''
       
	try:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        SettlementTYPE      =       ''
        SettlementProcFUNC  =       ''
        TheoModelXREF       =       'European Barrier GD2'
        MarketModelXREF     =       ''
        FairValueModelXREF  =       ''

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, BarStartDateDATE, BarrierEndDATE, KnockoutFLAG, ObservationFrqNB, ObsRuleENUM, PayAtBreachFLAG, StlmntDayRuleBUSD, StlmntDayRuleCAL, StlmntDayRuleCONV, StlmntDayRuleRULE, RebateCAL, RebateDAYC, RebatePERD, RebateUNIT, RebateVAL, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOptionFLAG, ContractSizeVAL, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, BarrierHitFLAG, BarrierCAL, BarrierDAYC, BarrierPERD, BarrierUNIT, BarrierVAL, DownBarrierCAL, DownBarrierDAYC, DownBarrierPERD, DownBarrierUNIT, DownBarrierVAL, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, OutputCurrencyCAL, OutputCurrencyDAYC, OutputCurrencyPERD, OutputCurrencyUNIT, UnderlyingXREF, MaturityDATE, VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, VolatltySpreadCAL, VolatltySpreadDAYC, VolatltySpreadFUNC, VolatltySpreadPERD, VolatltySpreadUNIT, VolatltySpreadVAL, VolatltySpreadSTRG, RM_MapProcFUNC, DiscountCurveXREF, SettlementTYPE, SettlementProcFUNC, TheoModelXREF, MarketModelXREF, FairValueModelXREF))

        # Roll Over Fixing Dates
        
        BASFLAG             =       'rm_ro'
        HeaderName          =       'AsianSPEC : Fixing Dates'
        ATTRIBUTE           =       'Fixing Dates'
        OBJECT              =       'AsianSPEC'
        
        Legs = i.legs()
        for l in Legs:
            for cf in l.cash_flows():
                ObsDatesDATE        =       Datefix(cf.start_day)
                
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ObsDatesDATE))
        
        outfile.close()

        #Position
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)
  
    return i.insid

# WRITE - FILE ######################################################################################################
