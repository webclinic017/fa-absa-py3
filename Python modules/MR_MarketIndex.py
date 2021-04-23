'''
Change History:
Date          CR/JIRA Number     Developer         Description
2010/03/23    264536             Douglas Finkel    Original Implementation
              289168             Douglas Finkel    Code fixes
2018/07/25    ABITFA-5506        Lucky Lesese      Added Price link to link multiple versions of the same insuance.
'''
import os, ael, string, acm, PositionFile, MR_MainFunctions

InsL = []


# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename = os.path.join(FileDir, Filename)
    
    outfile = open(filename, 'w')
    
    outfile.close()
    
    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename = os.path.join(FileDir, Filename)
    
    Instrument = acm.FInstrument[i.insaddr]

    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')

        #Base record
       
        BASFLAG = 'BAS'
        HeaderName = 'Market Index'
        OBJECT = 'Market IndexSPEC'
        TYPE = 'Market IndexSPEC'
        
        NAME = MR_MainFunctions.NameFix(i.insid)+'_MarketIndex'
        IDENTIFIER = 'insaddr_'+str(i.insaddr)+'_MarketIndex'
        
        CurrencyCAL = ''
        CurrencyDAYC = ''
        CurrencyPERD = ''
        CurrencyUNIT = Instrument.Currency().Name()
        
        CostOfCarryCAL = ''
        CostOfCarryDAYC = ''
        CostOfCarryPERD = ''        
        divYield = Instrument.AdditionalInfo().DividendYield()
        if divYield:
            CostOfCarryVAL = divYield
        else:
            CostOfCarryVAL = ''
        
        SpotPriceCAL = ''
        SpotPriceDAYC = ''
        SpotPriceFUNC = ''
        SpotPricePERD = ''
        SpotPriceSTRG = ''
        SpotPriceUNIT = Instrument.Currency().Name()
        SpotPriceVAL = 0.00
        
        
        if Instrument.InsType() == 'PriceIndex':
            SpotPriceVAL = i.cpi_reference(ael.date_today())
        else:
            if Instrument.Prices():
                for price in Instrument.Prices():
                    if price.Settle():
                        if price.Market().Name() == 'SPOT':
                            SpotPriceVAL = price.Settle()
                        elif price.Market().Name() == 'internal':
                            SpotPriceVAL = price.Settle()
            else:
                if Instrument.HistoricalPrices():
                    CompareDays = '1900-01-01'
                    for price in Instrument.HistoricalPrices():
                        if price.Settle():
                            if CompareDays <= price.Day():
                                CompareDays = price.Day()
                                if price.Market().Name() == 'SPOT':
                                    SpotPriceVAL = price.Settle()
                                elif price.Market().Name() == 'internal':
                                    SpotPriceVAL = price.Settle()

        
        if str(float(SpotPriceVAL)).lower() == 'nan':
            SpotPriceVAL = 0.00
        
        print i.insid, Instrument.InsType(), SpotPriceVAL        
        
        RIC_Code = MR_MainFunctions.NameFix(i.insid)
            
        GrowthRateXREF = str(RIC_Code) + '_GrowthCurve'

        try:
            DiscountCurveXREF = Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF = Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()      
        
        TheoModelXREF = 'CurveGrowth'
        MarketModelXREF = 'CurveGrowth'
        FairValueModelXREF = ''
        SettlementProcFUNC = '' #'@cashflow settlement'
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG,   
            HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CostOfCarryCAL,   
            CostOfCarryDAYC, CostOfCarryPERD, CostOfCarryVAL, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD,   
            SpotPriceSTRG, SpotPriceUNIT, SpotPriceVAL, GrowthRateXREF, DiscountCurveXREF, TheoModelXREF, MarketModelXREF,   
            FairValueModelXREF, SettlementProcFUNC))

        #Rollover record
        for dividend in Instrument.Dividends():
            BASFLAG = 'rm_ro'
            HeaderName = 'Market Index : Cash Flow'
            ATTRIBUTE = 'Cash Flow'
            object = 'Market IndexSPEC'
            
            CashFlowDATE = dividend.ExDivDay()
            CashFlowVAL = dividend.Amount()
            CashFlowUNIT = dividend.Currency().Name()
                
            outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, CashFlowDATE, CashFlowVAL,   
                CashFlowUNIT))
        
        outfile.close()
    return i.insid

# WRITE - FILE ######################################################################################################



