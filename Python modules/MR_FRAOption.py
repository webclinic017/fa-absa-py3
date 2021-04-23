
'''
Purpose                 :Market Risk feed files],[Updated TermNB and TermUNIT]
Department and Desk     :[IT],[MR]
Requester:              :[Natalie Austin],[Susan Kruger]
Developer               :[Douglas Finkel / Henk Nel],[Willie van der Bank]
CR Number               :[264536,289168],[816235 04/11/11]

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
        
        BASFLAG	        = 'BAS'
        HeaderName  	= 'Cap/Floor'
        OBJECT	        = 'Cap/FloorSPEC'
        TYPE	        = 'Cap/Floor'
        
        NAME            = MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER      = 'insaddr_'+str(i.insaddr)
        
        CurrencyCAL	= ''
        CurrencyDAYC	= ''
        CurrencyPERD	= ''
        CurrencyUNIT	= i.curr.insid
        
        CapFLAG = ''
        if i.call_option:
            CapFLAG = 'True'
        elif not i.call_option:
            CapFLAG = 'False'
        
        for l in i.und_insaddr.legs():
            EffectiveDATE            = MR_MainFunctions.Datefix(l.start_day)
            MaturityDATE            = MR_MainFunctions.Datefix(l.end_day)

        CouponPrepayENUM	= 'In Fine'
        CapDigitalPayVAL	= ''
        StateProcFUNC	        = '@cash flow generator'
        TermNB                  = ''
        TermUNIT                = ''
        
        '''
        for l in i.und_insaddr.legs():
            if l.rolling_period not in ('0d','0m','0y'):
                TermNB = getattr(l,'rolling_period.count')
                TermUNIT = getattr(l,'rolling_period.unit')
            else:
                TermNB = ''
                TermUNIT = 'Maturity'
        '''
        
        TermNB = ''
        TermUNIT = 'Maturity'
        
        TermCAL	        =       ''
        ResetRuleRULE	=       ''
        ResetRuleBUSD	=       ''
        ResetRuleCONV	=       ''
        ResetRuleCAL	=       ''
        CouponGenENUM	=       'Backward'
        FixedCouponDateNB	=       ''
        BusDayRuleRULE	=       ''
        BusDayRuleBUSD	=       ''
        BusDayRuleCONV	=       ''
        BusDayRuleCAL	=       ''    

        try:
            cashflow = acm.FCashFlow.Select01("leg = '%s' and startDate <= '%s' and endDate >= '%s'" % (leg.Oid(), acm.Time().TimeNow(), acm.Time().TimeNow()), '')
            calc = cashflow.Calculation()
            LastResetRateVAL    =   (calc.ForwardRate(cs) * 100) - cashflow.Spread()
        except:
            LastResetRateVAL    =       ''
        
        
        for c in i.und_insaddr.cash_flows():
            for r in c.resets():
                LastResetRateVAL	=   (r.value / 100)
           
        NextResetRateVAL	=       ''
        
        UndrCrvIndXREF      =       ''   

        for l in i.und_insaddr.legs():
            UndrCrvIndXREF 	=	'SCI_' + str(getattr(l, 'float_rate').insid) + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)

        try:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        CouponProratedFLAG	=       ''
        TheoModelXREF	=       'CapFloor'
        MarketModelXREF	=       ''
        FairValueModelXREF	=       ''
        SettlementProcFUNC	=       ''

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CapFLAG, EffectiveDATE, MaturityDATE, CouponPrepayENUM, CapDigitalPayVAL, StateProcFUNC, TermNB, TermUNIT, TermCAL, ResetRuleRULE, ResetRuleBUSD, ResetRuleCONV, ResetRuleCAL, CouponGenENUM, FixedCouponDateNB, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, LastResetRateVAL, NextResetRateVAL, UndrCrvIndXREF, DiscountCurveXREF, CouponProratedFLAG, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC))
        
        #Roll Over Cap Strike Rates
        
        BASFLAG	        =	'rm_ro'
        HeaderName	=	'Cap/Floor : Cap Strike Rates'
        ATTRIBUTE	=	'Cap Strike Rates'
        OBJECT	        =	'Cap/FloorSPEC'

        CapStrikeRatesDATE  = EffectiveDATE
        CapStrikeRatesENUM  = ''
        CapStrikeRatesCAL   = ''
        for l in i.und_insaddr.legs():
            CapStrikeRatesDAYC  = MR_MainFunctions.DayCountFix(l.daycount_method)
            
        CapStrikeRatesPERD  = 'simple'
        CapStrikeRatesUNIT  = '%'
        CapStrikeRatesVAL   = i.strike_price
                    
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, CapStrikeRatesDATE, CapStrikeRatesENUM, CapStrikeRatesCAL, CapStrikeRatesDAYC, CapStrikeRatesPERD, CapStrikeRatesUNIT, CapStrikeRatesVAL))
        
        #Roll Over Cap Notional Principal
        
        BASFLAG	        =	'rm_ro'
        HeaderName	=	'Cap/Floor : Cap Notional Principal'
        ATTRIBUTE	=	'Cap Notional Principal'
        OBJECT	        =	'Cap/FloorSPEC'
        
        CapNotnalPrincDATE  = EffectiveDATE
        CapNotnalPrincENUM  = ''
        CapNotnalPrincCAL   = ''
        CapNotnalPrincDAYC  = CapStrikeRatesDAYC
        CapNotnalPrincPERD  = ''
        CapNotnalPrincUNIT  = i.curr.insid
        CapNotnalPrincVAL   = i.contr_size
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, CapNotnalPrincDATE, CapNotnalPrincENUM, CapNotnalPrincCAL, CapNotnalPrincDAYC, CapNotnalPrincPERD, CapNotnalPrincUNIT, CapNotnalPrincVAL))

        outfile.close()
        
        #Position
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid