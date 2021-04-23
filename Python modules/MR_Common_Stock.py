
'''

#AEL module to produce Market Risk output files
#
#Input Variables:
#   FileDir 		- The drive where the output will be located
#   Filename 		- The name of the file that will be output
#   Object		    - The object that is sent from the equivalent ASQL to this AEL
#
#Requires Python installation on client PC.
#
#Created by
#Douglas Finkel - 2010/03/25
#Updated - Douglas Finkel - Add additional functionality

Purpose                 :Market Risk feed files, Added Exception handling for mtm_price
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel, Heinrich Cronje
CR Number               :264536,278978,569014, 683021
'''


import ael, string, acm, MR_PositionFile, MR_MainFunctions

InsL = []

# OPENFILE ##########################################################################################################
# Creates the file for the output
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

        #Base record
        outfile = open(filename, 'a')

        BASFLAG             =       'BAS'
        HeaderName          =       'Common Stock'
        OBJECT              =       'Common StockSPEC'
        TYPE                =       'Common Stock'

        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
      
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       i.curr.insid
        CostOfCarryCAL      =       '' 
        CostOfCarryDAYC     =       MR_MainFunctions.DayCountFix('Act/365')
        CostOfCarryPERD     =       'annual'
        
        dividendYield       =       ins.AdditionalInfo().DividendYield()
        if dividendYield == None:
            CostOfCarryVAL      =       ''
        else:
            CostOfCarryVAL      =       dividendYield
        
        
        DscrtDvdCutoffDATE  =       MR_MainFunctions.Datefix('01/01/1900')

        for div in i.dividends():
            if MR_MainFunctions.Datefix(div.pay_day) >= DscrtDvdCutoffDATE:
                DscrtDvdCutoffDATE = MR_MainFunctions.Datefix(div.pay_day)
        
        dividendStreams = acm.FDividendStream.Select('instrument = %s' %(i.insid))
        for dividendStream in dividendStreams:
            for dividend in dividendStream.Dividends():
                if (dividend.Description() != 'Simulated') and (MR_MainFunctions.Datefix(dividend.PayDay())  >= DscrtDvdCutoffDATE):
                    DscrtDvdCutoffDATE = MR_MainFunctions.Datefix(dividend.PayDay())   
                
        cl = acm.FCombInstrMap.Select('instrument=' + ins.Instrument().Name())

        GrowthRateXREF = 'EquityDefault_GrowthCurve'
        
        for item in cl.Elements():
            
            if item.Combination().Name() == 'ZAR/ALSI':
                GrowthRateXREF1  = item.Combination().Name()
                break
            else:
                GrowthRateXREF1  = 'Non-ZAR/ALSI'

        for SecItem in cl.Elements():
            if SecItem.Combination().Name() in ('ZAR/RESI', 'ZAR/FINI', 'ZAR/INDI'):
                GrowthRateXREF2 = SecItem.Combination().Name()
                GrowthRateXREF = GrowthRateXREF1 + '_' + GrowthRateXREF2 + '_GrowthCurve'
                break
            else:
                GrowthRateXREF = GrowthRateXREF1+ '_GrowthCurve'

        SpotPriceCAL        =       ''
        SpotPriceDAYC       =       ''
        SpotPriceFUNC       =       ''
        SpotPricePERD       =       ''
        SpotPriceSTRG       =       ''
        SpotPriceUNIT       =       i.curr.insid
        
        try:
            if i.quote_type == 'Per 100 Units':
                SpotPriceVAL        =       i.mtm_price(ael.date_today())/100
            else:
                SpotPriceVAL        =       i.mtm_price(ael.date_today())
        except:
            SpotPriceVAL        =       0
                
        VolatilityCAL       =       ''
        VolatilityDAYC      =       ''
        VolatilityFUNC      =       ''
        VolatilityPERD      =       ''
        VolatilitySTRG      =       ''
        VolatilityUNIT      =       ''
        VolatilityVAL       =       ''
        
        sheetType           =       'FDealSheet'		
        calcSpace           =       acm.Calculations().CreateCalculationSpace( context, sheetType )	
          
                    
        
        try:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        

        TheoModelXREF       =       'Equity'
        MarketModelXREF     =       'Equity'
        FairValueModelXREF  =       ''
        SettlementProcFUNC  =       '' #'@cashflow settlement'
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CostOfCarryCAL, CostOfCarryDAYC, CostOfCarryPERD, CostOfCarryVAL, DscrtDvdCutoffDATE, GrowthRateXREF, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceSTRG, SpotPriceUNIT, SpotPriceVAL, VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilitySTRG, VolatilityUNIT, VolatilityVAL, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC))
        
            
        #Roll Over Cash Flow
        
        BASFLAG             =       'rm_ro'
        HeaderName          =       'Common Stock : Cash Flow'
        ATTRIBUTE           =       'Cash Flow'
        OBJECT              =       'Common StockSPEC'

        #Get the dividend off the instrument if they exist
        for div in i.dividends():
            if (div.pay_day) >= ael.date_today():
                CashFlowDATE        =   MR_MainFunctions.Datefix(div.pay_day)    
                CashFlowVAL         =   div.dividend
                CashFlowUNIT        =   div.curr.insid

                outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, CashFlowDATE, CashFlowVAL, CashFlowUNIT))
                
       #CR569014 - Get the dividend estimation off the instrument if they exist
        if ins.MappedDividendStream().Parameter():
            for dividend in ins.MappedDividendStream().Parameter().Dividends():
                if dividend.Description() <> 'Simulated' and dividend.PayDay() >= ael.date_today():
                    CashFlowDATE        =   MR_MainFunctions.Datefix(dividend.PayDay())    
                    CashFlowVAL         =   dividend.Amount()
                    CashFlowUNIT        =   dividend.Currency().Name()

                    outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, CashFlowDATE, CashFlowVAL, CashFlowUNIT))

        IndexFound = 0
        
        cl= acm.FCombInstrMap.Select('instrument=' + i.insid)
        for item in cl.Elements():
            if item.Combination().Name() in ['ZAR/ALSI', 'ZAR/FINI', 'ZAR/INDI', 'ZAR/RESI', 'ZAR/FINDI', 'ZAR/SWIX']:
                IndexFound = 1
                #Roll Over Market Index
                
                BASFLAG             =       'rm_ro'
                HeaderName          =       'Common Stock : Market Index'
                ATTRIBUTE           =       'Market Index'
                OBJECT              =       'Common StockSPEC'
                
                MarketIndexXREF     =       ''
                
                try:
                    MarketIndexXREF  = 'insaddr_' + str(item.Combination().Instrument().Oid()) + '_MarketIndex'
                except:     
                    MarketIndexXREF  = str(item.Combination()) + '_MarketIndex'
                        
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, MarketIndexXREF))
                
                #Roll Over Equity Beta

                BASFLAG             =       'rm_ro'
                HeaderName          =       'Common Stock : Equity Beta'
                ATTRIBUTE           =       'Equity Beta'
                OBJECT              =       'Common StockSPEC'
                EquityBetaVAL       =       '1'

                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, EquityBetaVAL))
        
        if IndexFound == 0:
        
            #Roll Over Market Index
            
            BASFLAG             =       'rm_ro'
            HeaderName          =       'Common Stock : Market Index'
            ATTRIBUTE           =       'Market Index'
            OBJECT              =       'Common StockSPEC'
            
            MarketIndexXREF     =       'EquityDefault_MarketIndex'
            
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, MarketIndexXREF))
            
            #Roll Over Equity Beta

            BASFLAG             =       'rm_ro'
            HeaderName          =       'Common Stock : Equity Beta'
            ATTRIBUTE           =       'Equity Beta'
            OBJECT              =       'Common StockSPEC'
            EquityBetaVAL       =       '1'

            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, EquityBetaVAL))
        
        outfile.close()
        
#       Includes the valid trades/position on the instruments
#        for trades in i.trades():
#            if MR_MainFunctions.ValidTradeNo(trades) == 0:
#                MR_PositionFile.CreatePosition(trades,PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################
