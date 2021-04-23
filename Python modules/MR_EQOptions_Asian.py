'''
Purpose                 :[Market Risk feed files],[Updated DiscountCurveXREF],[Updated code to cater for Asian Performance Options]
Department and Desk     :[IT],[MR],[MR]
Requester:              :[Natalie Austin],[Susan Kruger],[Susan Kruger]
Developer               :[Douglas Finkel / Henk Nel],[Willie van der Bank],[Willie van der Bank]
CR Number               :[264536],[831357 18/11/2011],[838719 25/11/2011]

-- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-01-20     CHNG0003487839   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-433
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''
import ael, string, acm, PositionFile, MR_MainFunctions, SAGEN_IT_TM_Column_Calculation

InsL = []

#Repo curve
def getRepoYC(instrument):
    if instrument:
        repoCurve = SAGEN_IT_TM_Column_Calculation.get_TM_Column_Calculation(None, 'Standard', 'FPortfolioSheet', instrument.Oid(), 'Instrument', 'Repo Curve Name As String', None, 0, None, None)
    else:
        repoCurve = ''
        
    return repoCurve

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
        HeaderName          =       'Asian'
        OBJECT              =       'AsianSPEC'
        TYPE                =       'Asian'   
 
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)

        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        
        CallOptionFLAG      =       Instrument.IsCallOption()
        
        ContractSizeVAL     =       Instrument.ContractSize()
        CorrelationVAL      =       ''
        CorrelationSrfXREF  =       ''
        
        FXVolatilityCAL     =       ''
        FXVolatilityDAYC    =       ''
        FXVolatilityFUNC    =       ''
        FXVolatilityPERD    =       ''
        FXVolatilityUNIT    =       ''
        FXVolatilityVAL     =       ''
        FXVolatilitySTRG    =       ''
        FXVolatilitySfXREF  =       ''
        
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
        
        UnderlyingXREF      =       'insaddr_'+str(i.und_insaddr.insaddr)
        
        ProcessTypeENUM     =       'Geometric Brownian'
        
        MeanRvrsnConstCAL   =       ''
        MeanRvrsnConstDAYC  =       ''
        MeanRvrsnConstFUNC  =       ''
        MeanRvrsnConstPERD  =       ''
        MeanRvrsnConstUNIT  =       ''
        MeanRvrsnConstVAL   =       ''
        MeanRvrsnConstSTRG  =       ''
        
        AveragingTypeENUM   =       'Discrete'
        
        MaturityDATE        =       MR_MainFunctions.Datefix(str(Instrument.ExpiryDateOnly()))
        
        FixingRuleENUM      =       'Fixing Dates'
        
        BusDayRuleRULE      =       ''
        BusDayRuleBUSD      =       ''
        BusDayRuleCONV      =       ''
        BusDayRuleCAL       =       ''
        
        NumofFixiDateNB     =       ''
        
        AvgSoFarCAL         =       ''
        AvgSoFarDAYC        =       ''
        AvgSoFarFUNC        =       '@GD2 historical'
        AvgSoFarPERD        =       ''
        AvgSoFarUNIT        =       ''
        AvgSoFarVAL         =       ''
        AvgSoFarSTRG        =       ''
        
        #Additional fields for Asian Performance Options
        # ##############################
        
        #exotic events are listed in reverse order
        try:
            AvgStartDateDATE    =   MR_MainFunctions.Datefix(Instrument.ExoticEvents().First().Date())
        except:
            AvgStartDateDATE    =   ael.date_today()
        
        for ExoticEvent in Instrument.ExoticEvents():
            if AvgStartDateDATE > MR_MainFunctions.Datefix(ExoticEvent.Date()):
                AvgStartDateDATE = MR_MainFunctions.Datefix(ExoticEvent.Date())
        
        AveEndDateDATE = ''
        AveSoFarCAL = ''
        AveSoFarDAYC = ''
        AveSoFarFUNC = ''
        AveSoFarPERD = ''
        AveSoFarUNIT = ''
        AveSoFarVAL = ''
        AveSoFarSTRG = ''
        AveStartDateDATE = ''

        # ##############################
        
        HistoricalCrvXREF   =       str(i.und_insaddr.insid) + '_HistoricalCurve'
        
        FixedTodayFLAG      =       ''
        
        #DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        DiscountCurveXREF   =       getRepoYC(Instrument)
        
        if DiscountCurveXREF == 0:
            DiscountCurveXREF   =  Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
		
        VolatilityCAL       =       ''
        VolatilityDAYC      =       'actual/365'
        VolatilityFUNC      =       '@volatility THEO'
        VolatilityPERD      =       'annual'
        VolatilityUNIT      =       '%'
        VolatilityVAL       =       ''
        VolatilitySTRG      =       ''
        
        #VolSurfaceXREF      =       Instrument.MappedVolatilityStructure().ParameterName()
        VolSurfaceXREF      =       Instrument.MappedVolatilityLink().LinkName()
        
        SettlementTYPE      =       ''
        
        SettlementProcFUNC  =       ''
        
        if i.add_info('Average_In') == 'Yes':
            TheoModelXREF       =       'Performance Asian'
        else:
            TheoModelXREF       =       'Asian Option'
        
        MarketModelXREF     =       ''
        
        FairValueModelXREF  =       ''
        
        #Field values for Asian Performance Options
        if i.exotic():
            Exo = i.exotic()
            if  Exo.average_strike_type == 'Average':
            
                StrikeDate = []
                PriceDate = []

                for e in Instrument.ExoticEvents():
                    if e.Type() == 'Average price':
                        PriceDate.append(e.Date())
                    elif e.Type() == 'Average strike':
                        StrikeDate.append(e.Date())

                PriceDate.sort()
                StrikeDate.sort()
            
                AvgSoFarCAL = ''
                AvgSoFarDAYC = ''
                AvgSoFarFUNC = '@GD2 historical'
                AvgSoFarPERD = ''
                AvgSoFarUNIT = ''
                AvgSoFarVAL = ''
                AvgSoFarSTRG = ''
                
                AvgStartDateDATE = PriceDate[0]
                if len(StrikeDate) > 0:
                    AveEndDateDATE = StrikeDate[len(StrikeDate) - 1]
                else:
                    AveEndDateDATE = ''
                AveSoFarCAL = ''
                AveSoFarDAYC = ''
                AveSoFarFUNC = '@GD2 Average-In historical'
                AveSoFarPERD = ''
                AveSoFarUNIT = ''
                AveSoFarVAL = ''
                AveSoFarSTRG = ''
                if len(StrikeDate) > 0:
                    AveStartDateDATE = StrikeDate[0]
                else:
                    AveStartDateDATE = ''
                AveragingTypeENUM = ''
                if i.add_info('Average_In') == 'Yes':
                    TheoModelXREF       =       'Performance Asian'
                else:
                    TheoModelXREF       =       'Asian Option'
                VolatilityFUNC = ''
                StrikePriceCAL = ''
                StrikePriceDAYC = '' 
                StrikePriceFUNC = ''
                StrikePricePERD = ''
                StrikePriceUNIT = ''
                '''
                if i.und_insaddr.quote_type == 'Per 100 Units':
                    StrikePriceVAL      =       Instrument.StrikePrice() / 100
                else:
                    StrikePriceVAL      =       Instrument.StrikePrice()
                '''
                StrikePriceVAL      =       i.add_info('AsianInWeight')
    
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOptionFLAG, ContractSizeVAL, CorrelationVAL, CorrelationSrfXREF, FXVolatilityCAL, FXVolatilityDAYC, FXVolatilityFUNC, FXVolatilityPERD, FXVolatilityUNIT, FXVolatilityVAL, FXVolatilitySTRG, FXVolatilitySfXREF, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, UnderlyingXREF, ProcessTypeENUM, MeanRvrsnConstCAL, MeanRvrsnConstDAYC, MeanRvrsnConstFUNC, MeanRvrsnConstPERD, MeanRvrsnConstUNIT, MeanRvrsnConstVAL, MeanRvrsnConstSTRG, AveragingTypeENUM, MaturityDATE, FixingRuleENUM, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, NumofFixiDateNB, AvgSoFarCAL, AvgSoFarDAYC, AvgSoFarFUNC, AvgSoFarPERD, AvgSoFarUNIT, AvgSoFarVAL, AvgSoFarSTRG, AvgStartDateDATE, AveEndDateDATE, AveSoFarCAL, AveSoFarDAYC, AveSoFarFUNC, AveSoFarPERD, AveSoFarUNIT, AveSoFarVAL, AveSoFarSTRG, AveStartDateDATE, HistoricalCrvXREF, FixedTodayFLAG, DiscountCurveXREF, VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, SettlementTYPE, SettlementProcFUNC, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
        #outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG,HeaderName,OBJECT,TYPE,NAME,IDENTIFIER,CurrencyCAL,CurrencyDAYC,CurrencyPERD,CurrencyUNIT,CallOptionFLAG,ContractSizeVAL,CorrelationVAL,CorrelationSrfXREF,FXVolatilityCAL,FXVolatilityDAYC,FXVolatilityFUNC,FXVolatilityPERD,FXVolatilityUNIT,FXVolatilityVAL,FXVolatilitySTRG,FXVolatilitySfXREF,StrikePriceCAL,StrikePriceDAYC,StrikePriceFUNC,StrikePricePERD,StrikePriceUNIT,StrikePriceVAL,StrikePriceSTRG,UnderlyingXREF,ProcessTypeENUM,MeanRvrsnConstCAL,MeanRvrsnConstDAYC,MeanRvrsnConstFUNC,MeanRvrsnConstPERD,MeanRvrsnConstUNIT,MeanRvrsnConstVAL,MeanRvrsnConstSTRG,AveragingTypeENUM,MaturityDATE,AvgStartDateDATE,FixingRuleENUM,BusDayRuleRULE,BusDayRuleBUSD,BusDayRuleCONV,BusDayRuleCAL,NumofFixiDateNB,AvgSoFarCAL,AvgSoFarDAYC,AvgSoFarFUNC,AvgSoFarPERD,AvgSoFarUNIT,AvgSoFarVAL,AvgSoFarSTRG,HistoricalCrvXREF,FixedTodayFLAG,DiscountCurveXREF,VolatilityCAL,VolatilityDAYC,VolatilityFUNC,VolatilityPERD,VolatilityUNIT,VolatilityVAL,VolatilitySTRG,VolSurfaceXREF,SettlementTYPE,SettlementProcFUNC,TheoModelXREF,MarketModelXREF,FairValueModelXREF))

        #Field values for Asian Performance Options
        if i.exotic():
            Exo = i.exotic()
            if  Exo.average_strike_type == 'Average':
                BASFLAG = 'rm_ro'
                HeaderName = 'Asian : Average-In Averaging Weights'
                ATTRIBUTE = 'Average-In Averaging Weights'
                OBJECT = 'AsianSPEC'
                AveAveWeightsVAL = '1'

                outfile.write('%s,%s,%s,%s,%s\n' %(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, AveAveWeightsVAL))
                
                for evt in Instrument.ExoticEvents():
                    if evt.Type() == 'Average strike':
                    
                        BASFLAG     = 'rm_ro'
                        HeaderName  = 'Asian : Average-In Fixing Dates'
                        ATTRIBUTE   = 'Average-In Fixing Dates'
                        OBJECT      = 'AsianSPEC'
                        AveFixDatesDATE     = MR_MainFunctions.Datefix(evt.Date())
                
                        outfile.write('%s,%s,%s,%s,%s\n' %(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, AveFixDatesDATE))

        for evt in Instrument.ExoticEvents():
            BASFLAG     =       'rm_ro'
            HeaderName	=       'Asian : Averaging Weights'
            ATTRIBUTE	=       'Averaging Weights'
            OBJECT	=       'AsianSPEC'
                        
            AverWeightsFLAG = 'FALSE'
            AverWeightsVAL  = '1'

            outfile.write('%s,%s,%s,%s,%s,%s\n' %(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, AverWeightsFLAG, AverWeightsVAL))
                      
            if evt.Type() == 'Average price':
            
                BASFLAG     =       'rm_ro'
                HeaderName  =       'Asian : Fixing Dates'
                ATTRIBUTE   =       'Fixing Dates'
                OBJECT	    =       'AsianSPEC'
                FixingDatesDATE = MR_MainFunctions.Datefix(evt.Date())

                outfile.write('%s,%s,%s,%s,%s\n' %(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, FixingDatesDATE))
                      
        outfile.close()
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################


#OpenFile('1','f:\\','FileName.csv','PositionName.csv')
#Write(ael.Instrument['ZAR/EQ/SWIX/25MAR13/C/5454.32/OTC/ASIA'],'f:\\','FileName.csv','PositionName.csv')
