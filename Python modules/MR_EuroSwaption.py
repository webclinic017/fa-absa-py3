'''
Purpose                 :[Market Risk feed files],[Updated VolatilityFUNC]
Department and Desk     :[IT],[MR]
Requester:              :[Natalie Austin],[Susan Kruger]
Developer               :[Douglas Finkel / Henk Nel],[Willie van der Bank]
CR Number               :[264536,278978],[2012-08-10, 380391]

Change history:
===============

2015-02-11  FA-Upgrade-2014 Peter Basista   Fix a change in FInstrument.
                                            MappedDiscountLink API

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

class SheetCalcSpace(object):
    CALC_SPACE = acm.FCalculationSpace('FPortfolioSheet')
    @classmethod
    
    def get_column_calc(cls, obj, column_id):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation(obj, column_id)
        return calc

# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    outfile = open(filename, 'a')
    
    Instrument = acm.FInstrument[i.insaddr]

    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        
        
        #Base record
        outfile = open(filename, 'a')
        BASFLAG             =       'BAS'
        HeaderName          =       'Swaption'
        OBJECT              =       'SwaptionSPEC'
        TYPE                =       'Swaption'
        
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        
        CallOption          =       Instrument.IsCallOption()
        
        UndrFixdLegXREF =       ''
        UnderlyingXREF  =       ''
        
        for leg in i.und_insaddr.legs():
        
            if leg.type == 'Fixed':
                UndrFixdLegXREF =       'insaddr_' + str(i.und_insaddr.insaddr) + '_' + str(leg.legnbr)
            elif leg.type == 'Float':
                UnderlyingXREF  =       'insaddr_' + str(i.und_insaddr.insaddr) + '_' + str(leg.legnbr)
            elif leg.type == 'None':
                if UndrFixdLegXREF == '':
                    UndrFixdLegXREF = ''
                elif UnderlyingXREF == '':
                    UnderlyingXREF  = ''
                    
                    
        EffectiveDATE           =        ''
        '''            
        EffectiveDATE           =        ael.date_today()
        for l in i.legs():
                if l.start_day <= EffectiveDATE:
                        EffectiveDATE = l.start_day
        EffectiveDATE           =	    MR_MainFunctions.Datefix(EffectiveDATE)
        '''
        MaturityDATE        =       MR_MainFunctions.Datefix(str(Instrument.ExpiryDateOnly()))
        
        SpotPriceCAL        =       ''
        SpotPriceDAYC       =       ''
        SpotPriceFUNC       =       ''
        SpotPricePERD       =       ''
        SpotPriceUNIT       =       i.curr.insid 
        SpotPriceVAL        =       '' #calc.PresentValue(CalcSpace.cs).Number()
        SpotPriceSTRG       =       ''
        
        StrikePriceCAL      =       ''
        StrikePriceDAYC     =       'actual/365'
        StrikePriceFUNC     =       ''
        StrikePricePERD     =       'simple'
        StrikePriceUNIT     =       '%'
        StrikePriceVAL      =       Instrument.StrikePrice()
        StrikePriceSTRG     =       ''
        
        VolatilityCAL       =       ''
        VolatilityDAYC      =       'actual/actual'
        VolatilityFUNC      =       '@volatility'
        VolatilityPERD      =       'annual'
        VolatilityUNIT      =       '%'
        
        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        calc = Instrument.Calculation()
        
        VolatilityVAL       =       calc.Volatility(cs)*100
        VolatilitySTRG      =       ''
        
        #VolSurfaceXREF      =       Instrument.MappedVolatilityStructure().ParameterName()
        VolSurfaceXREF      =       Instrument.MappedVolatilityLink().LinkName()
        if VolSurfaceXREF == 'DEFAULT':
            VolSurfaceXREF = 'None'
        
        HighSkewSurfXREF    =       ''
        LowSkewSurfXREF     =       ''
        
        CouponGenENUM       =       ''
        FixedCouponDateNB   =       ''
        UndrCrvIndXREF      =       MR_MainFunctions.NameFix(Instrument.Underlying().MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        
        DiscountCurveXREF   =       MR_MainFunctions.NameFix(Instrument.MappedDiscountLink(Instrument.Currency(), False, None).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        
        TheoModelXREF       =       'Swaption'
        MarketModelXREF     =       ''
        FairValueModelXREF  =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'
                      %(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CallOption, UnderlyingXREF,
                        UndrFixdLegXREF, EffectiveDATE, MaturityDATE, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL,
                        SpotPriceSTRG, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG,
                        VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF,
                        HighSkewSurfXREF, LowSkewSurfXREF, CouponGenENUM, FixedCouponDateNB, UndrCrvIndXREF, DiscountCurveXREF, TheoModelXREF,
                        MarketModelXREF, FairValueModelXREF))

                # Roll Over Variable Notional
        
        BASFLAG             =       'rm_ro'
        HeaderName          =       'Swaption : Variable Notional'
        ATTRIBUTE           =       'Variable Notional'
        OBJECT              =       'SwaptionSPEC'
        
        VariabNotionalDATE  =       MR_MainFunctions.Datefix(i.exp_day)
        VariabNotionalENUM  =       ''
        VariabNotionalCAL   =       ''
        VariabNotionalDAYC  =       ''
        VariabNotionalPERD  =       ''      
        VariabNotionalUNIT  =       i.curr.insid
        VariabNotionalVAL   =       i.contr_size
                
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, VariabNotionalDATE, VariabNotionalENUM, VariabNotionalCAL, VariabNotionalDAYC, VariabNotionalPERD, VariabNotionalUNIT, VariabNotionalVAL))
        
        outfile.close()
        
        #Position
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################

