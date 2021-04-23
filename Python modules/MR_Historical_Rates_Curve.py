'''
Purpose                 :[Market Risk feed files],[Only include prices older than 4 months for PriceIndex],[Updated HistRateSurfNODE for Bond and IndexLinkedBond]
Department and Desk     :[IT],[MR],[MR]
Requester:              :[Natalie Austin],[Susan Kruger],[Susan Kruger]
Developer               :[Douglas Finkel],[Willie van der Bank],[Willie van der Bank],[Kevin Kistan]
CR Number               :[264536, 316586, 622355, 622355],[824244 11/11/2011],[[831357 18/11/2011]], [2418286 06/11/2014]
'''


import ael, string, acm, MR_MainFunctions
from sl_functions import YTM_To_Price
InsL = []
CurrSwapsL = []


# Front Upgrade 2013.3 -- rerouting this function, later maybe remove the _old one
def YieldToPrice(bond, date, bondYield, toDirty=True, isSettlementDate=True):
    return YTM_To_Price(bond, date, bondYield, toDirty, isSettlementDate)

def YieldToPrice_old(bond, date, bondYield, toDirty=True, isSettlementDate=True):
    ''' Convert a bonds yield to price. For a given trade/settlement date, return the 
        clean or dirty price for the given bondYield for settlement
    '''
    denominatedvalue = acm.GetFunction('denominatedvalue', 4)
    price = denominatedvalue(bondYield, acm.FCurrency['ZAR'], None, date)
    leg = bond.Legs().At(0)
    staticLegInfo = leg.StaticLegInformation(bond, date, None)
    legInf = staticLegInfo.LegInformation(date)
    
    if isSettlementDate:
        result = bond.QuoteToRoundedCleanUnitValue(price, date, date, toDirty, [legInf], bond.Quotation(), 1.0, 0.0)
    else:
        result = bond.QuoteToRoundedCleanUnitValue(price, date, toDirty, [legInf], bond.Quotation(), 1.0, 0.0)
    return result.Number() * 100

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,*rest):

    filename            = FileDir + Filename
    outfile             =  open(filename, 'w')
    outfile.close()

    del InsL[:]
    InsL[:] = []  
    
    del CurrSwapsL[:]
    CurrSwapsL[:] = []  

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,*rest):

    FourMonthsAgo = ael.date(acm.Time.DateAddDelta(ael.date_today(), 0, -4, 0))
    
    filename            = FileDir + Filename
    ins = acm.FInstrument[i.insid]
    quotation_factor = 1 / ins.Quotation().QuotationFactor()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        outfile = open(filename, 'a')
        
        #Base record
        BAS                     =       'BAS'
        HistoricalRatesSPEC    =        'Historical RatesSPEC'
        OBJECT                  =       'Historical RatesSPEC'
        TYPE                    =       'Historical Rates'
        IDENTIFIER              =       str(i.insid)+'_HistoricalCurve'
        NAME                    =       str(i.insid)+'_HistoricalCurve'
        
        ActiveFLAG              =       'TRUE'
        
        CurveFUNC               =       ''
        if i.instype in ('RateIndex'):
            CurveUnitCAL            =       ''
            CurveUnitDAYC           =       MR_MainFunctions.DayCountFix(i.daycount_method)

            for l in i.legs():
                if (l):
                    CurveUnitDAYC       =       MR_MainFunctions.DayCountFix(l.daycount_method)
                else:
                    CurveUnitDAYC       =       MR_MainFunctions.DayCountFix('Act/365')
            
            CurveUnitPERD           =       'simple'
            CurveUnitUNIT           =       '%'
        else:
            CurveUnitCAL            =       ''
            CurveUnitDAYC           =       ''
            CurveUnitPERD           =       ''
            CurveUnitUNIT           =       i.curr.insid
        
        DatumDATE               =       MR_MainFunctions.Datefix(acm.Time().DateNow())
        OriginOffsetNB          =       '0'
        RelativeCurveFLAG       =       'TRUE'
        StateProcFUNC           =       ''
        TimeEvolutionFUNC       =       '@Constant'
        FunctionIdFLAG          =       'TRUE'
        HistRateSfExt0FLAG      =       'FALSE'

        HistRateSurf0SIN        =       '@Constant'

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, HistoricalRatesSPEC, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CurveFUNC, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, HistRateSfExt0FLAG, HistRateSurf0SIN))
        
        if i.instype == 'PriceIndex':
            aelToday = FourMonthsAgo
        else:
            aelToday = ael.date_today()
        HistoricalDates = []
        for p in i.historical_prices():
            if (i.instype == 'PriceIndex' and p.day <= FourMonthsAgo) or i.instype != 'PriceIndex':
                if p.ptynbr.ptyid in ('SPOT'):
                    # Roll Over Generic Zero Surface
                    if (str(aelToday.days_between(p.day))+str(p.curr.insid)) not in HistoricalDates:
                        HistoricalDates.append(str(aelToday.days_between(p.day))+str(p.curr.insid))
                        
                        rm_ro                    =       'rm_ro'
                        HistoricalRatesSPEC      =       'Historical RatesSPEC : Historical Rate Surface'
                        ATTRIBUTE                =       'Historical Rate Surface'
                        OBJECT                   =       'Historical RatesSPEC'
                        
                        HistRateSurf0AXS        =       aelToday.days_between(p.day) 
                        
                        if i.instype in ('RateIndex', 'Stock', 'EquityIndex'):
                            HistRateSurfNODE        =       p.settle / quotation_factor
                        elif i.instype in ('Bond', 'IndexLinkedBond'):
                            HistRateSurfNODE        =       YieldToPrice(ins, p.day, p.settle, True, False) * 10000
                        else:
                            HistRateSurfNODE        =       p.settle
                        '''
                        if i.instype in ('RateIndex', 'Stock','Bond','IndexLinkedBond'):
                            HistRateSurfNODE        =       p.settle / 100
                        else:
                            HistRateSurfNODE        =       p.settle
                        '''
                        
                        if HistRateSurfNODE != 0.0:
                            outfile.write('%s,%s,%s,%s,%s,%s\n'%(rm_ro, HistoricalRatesSPEC, ATTRIBUTE, OBJECT, HistRateSurf0AXS, HistRateSurfNODE))
                elif p.ptynbr.ptyid in ('internal'):
                    # Roll Over Generic Zero Surface
                    if (str(aelToday.days_between(p.day))+str(p.curr.insid)) not in HistoricalDates:
                        HistoricalDates.append(str(aelToday.days_between(p.day))+str(p.curr.insid))
                        
                        rm_ro                    =       'rm_ro'
                        HistoricalRatesSPEC      =       'Historical RatesSPEC : Historical Rate Surface'
                        ATTRIBUTE                =       'Historical Rate Surface'
                        OBJECT                   =       'Historical RatesSPEC'
                        
                        HistRateSurf0AXS        =       aelToday.days_between(p.day) 
                        
                        if i.instype in ('RateIndex', 'Stock', 'EquityIndex'):
                           HistRateSurfNODE        =       p.settle / quotation_factor
                        elif i.instype in ('Bond', 'IndexLinkedBond'):
                            HistRateSurfNODE        =       YieldToPrice(ins, p.day, p.settle, True, False) * 10000
                        else:
                            HistRateSurfNODE        =       p.settle
                        '''
                        if i.instype in ('RateIndex', 'Stock','Bond','IndexLinkedBond'):
                            HistRateSurfNODE        =       p.settle / 100
                        else:
                            HistRateSurfNODE        =       p.settle
                        '''
                            
                        if HistRateSurfNODE != 0.0:
                            outfile.write('%s,%s,%s,%s,%s,%s\n'%(rm_ro, HistoricalRatesSPEC, ATTRIBUTE, OBJECT, HistRateSurf0AXS, HistRateSurfNODE))
            
        # Roll Over  Function Parameters
        
        BASFLAG             =       'rm_ro'
        HeaderName          =       'Historical RatesSPEC : Function Parameters'
        ATTRIBUTE           =       'Function Parameters'
        OBJECT              =       'Historical RatesSPEC'
        FunctionParamsVAL   =       ''
        if FunctionParamsVAL != '':
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, FunctionParamsVAL))
        
        # Roll Over  Procedure Parameter
        
        BASFLAG             =       'rm_ro'
        HeaderName          =       'Historical RatesSPEC : Procedure Parameter'
        ATTRIBUTE           =       'Procedure Parameter'
        OBJECT              =       'Historical RatesSPEC'
        ProcedureParamXREF  =       ''
        
        if ProcedureParamXREF != '':
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ProcedureParamXREF))
            
        outfile.close()

    return str(i.insaddr)

# WRITE - FILE ######################################################################################################

BASECURR = ['USD', 'GBP', 'EUR', 'ZAR']

def FXRate(LOCKCURR, RESETCURR):
    LockCurr = ael.Instrument[LOCKCURR]
    ResetCurr = ael.Instrument[RESETCURR]
    retVal = []

    for BASE in BASECURR:
        BaseCurr = ael.Instrument[BASE]
        LockPrices = dict([(ael.date_today().days_between(price.day), price.settle) for price in BaseCurr.historical_prices() if price.curr.insid == LOCKCURR and price.ptynbr.ptyid in ('SPOT', 'internal')])
        LockPrices.keys().sort()
        if len(LockPrices.keys()) > 10 and LockPrices.keys()[len(LockPrices.keys())-1] > -5 and BASE != LOCKCURR:
            LockBASE = BASE
            InvertLock = False
            break
        else:          
            LockPrices = dict([(ael.date_today().days_between(price.day), price.settle) for price in LockCurr.historical_prices() if price.curr.insid == BASE and price.ptynbr.ptyid in ('SPOT', 'internal')])
            LockPrices.keys().sort()
            if len(LockPrices.keys()) > 10 and LockPrices.keys()[len(LockPrices.keys())-1] > -5 and BASE != LOCKCURR:
                LockBASE = BASE
                InvertLock = True
                break

    for BASE in BASECURR:
        BaseCurr = ael.Instrument[BASE]
        ResetPrices = dict([(ael.date_today().days_between(price.day), price.settle) for price in BaseCurr.historical_prices() if price.curr.insid == RESETCURR and price.ptynbr.ptyid in ('SPOT', 'internal')])
        ResetPrices.keys().sort()
        if len(ResetPrices.keys()) > 10 and ResetPrices.keys()[len(ResetPrices.keys())-1] > -5 and BASE != RESETCURR:
            ResetBASE = BASE
            InvertReset = False
            break
        else:          
            ResetPrices = dict([(ael.date_today().days_between(price.day), price.settle) for price in ResetCurr.historical_prices() if price.curr.insid == BASE and price.ptynbr.ptyid in ('SPOT', 'internal')])
            ResetPrices.keys().sort()
            if len(ResetPrices.keys()) > 10 and ResetPrices.keys()[len(ResetPrices.keys())-1] > -5 and BASE != RESETCURR:
                ResetBASE = BASE
                InvertReset = True
                break

    if LockBASE != ResetBASE and LockBASE != RESETCURR and ResetBASE != LOCKCURR:
        # this case is currently not dealt with
        BaseCurr = ael.Instrument[LockBASE]
        CrossPrices = dict([(ael.date_today().days_between(price.day), price.settle) for price in BaseCurr.historical_prices() if price.curr.insid == ResetBASE and price.ptynbr.ptyid in ('SPOT', 'internal')])
        print '    ', 'Different Base', LockBASE, ResetBASE
    else:
        for key in LockPrices.keys():
            if key in ResetPrices:
                if ResetBASE == LOCKCURR:
                    LockPriceValue = 1
                else:
                    if InvertLock:
                         LockPriceValue = LockPrices[key]
                    else:
                        if LockPrices[key] < 0.0000001:
                            continue
                        LockPriceValue = 1/LockPrices[key]
                if LockBASE == RESETCURR and ResetBASE != LOCKCURR:
                    ResetPriceValue = 1
                else:    
                    if InvertReset:
                        if ResetPrices[key] < 0.0000001:
                            continue
                        ResetPriceValue = 1/ResetPrices[key]
                    else:
                        ResetPriceValue = ResetPrices[key]
                retVal.append([key, LockPriceValue * ResetPriceValue])

    return retVal
 
# WRITE2 - FILE ######################################################################################################

def Write2(temp,CurrSwaps,FileDir,Filename,*rest):

    if (CurrSwaps) not in CurrSwapsL:
        CurrSwapsL.append(CurrSwaps)

        LockCurr, ResetCurr = CurrSwaps.split('/')
        
        filename    = FileDir + Filename
        outfile = open(filename, 'a')
        
        #Base record
        
        BAS                     =       'BAS'
        HistoricalRatesSPEC     =       'Historical RatesSPEC'
        OBJECT                  =       'Historical RatesSPEC'
        TYPE                    =       'Historical Rates'
        
        IDENTIFIER              =       LockCurr +  ResetCurr + '_HistoricalCurve'
        NAME                    =       LockCurr +  ResetCurr + '_HistoricalCurve'
        
        ActiveFLAG              =       'TRUE'
        
        CurveFUNC               =       ''
        CurveUnitCAL            =       ''
        CurveUnitDAYC           =       ''
        CurveUnitPERD           =       ''
        CurveUnitUNIT           =       ResetCurr
        
        DatumDATE               =       MR_MainFunctions.Datefix(acm.Time().DateNow())
        OriginOffsetNB          =       '0'
        RelativeCurveFLAG       =       'TRUE'
        StateProcFUNC           =       ''
        TimeEvolutionFUNC       =       '@Constant'
        FunctionIdFLAG          =       'TRUE'
        HistRateSfExt0FLAG      =       'FALSE'
        
        HistRateSurf0SIN        =       '@Constant'
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, HistoricalRatesSPEC, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CurveFUNC, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, HistRateSfExt0FLAG, HistRateSurf0SIN))
        
        for retVal in FXRate(LockCurr, ResetCurr):
          
            # Roll Over Generic Zero Surface
            rm_ro                    =       'rm_ro'
            HistoricalRatesSPEC      =       'Historical RatesSPEC : Historical Rate Surface'
            ATTRIBUTE                =       'Historical Rate Surface'
            OBJECT                   =       'Historical RatesSPEC'
            HistRateSurf0AXS         =       retVal[0]
            HistRateSurfNODE         =       retVal[1]
            
            if HistRateSurfNODE != 0.0:
                outfile.write('%s,%s,%s,%s,%s,%s\n'%(rm_ro, HistoricalRatesSPEC, ATTRIBUTE, OBJECT, HistRateSurf0AXS, HistRateSurfNODE))
            
        # Roll Over  Function Parameters

        BASFLAG             =       'rm_ro'
        HeaderName          =       'Historical RatesSPEC : Function Parameters'
        ATTRIBUTE           =       'Function Parameters'
        OBJECT              =       'Historical RatesSPEC'
        FunctionParamsVAL   =       ''
        
        if FunctionParamsVAL != '':
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, FunctionParamsVAL))
        
        # Roll Over  Procedure Parameter
        
        BASFLAG             =       'rm_ro'
        HeaderName          =       'Historical RatesSPEC : Procedure Parameter'
        ATTRIBUTE           =       'Procedure Parameter'
        OBJECT              =       'Historical RatesSPEC'
        ProcedureParamXREF  =       ''
        
        if ProcedureParamXREF != '':
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ProcedureParamXREF))                                
            
        outfile.close()

    return str(CurrSwaps)

# WRITE2 - FILE ######################################################################################################
