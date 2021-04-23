"""---------------------------------------------------------------------------------------------------------------
Project                 : NOD RISK Project
Purpose                 : Show Risk exposed by non-ZAR Trades
Requester               : Vincent Ncuphuka
Developer               : Ryan Burton
Jira-Task               : http://abcap-jira/browse/ABITFA-1493
CR Number               :  
------------------------------------------------------------------------------------------------------------------"""		
		
import ael, acm, csv, time
import SAGEN_Resets, FXRATE, OverrideFields
		
tradeFilters = [	
    'LA_NOP_Bill',
    'LA_NOP_Bonds',
    'LA_NOP_BSB_Repos',
    'LA_NOP_CAPFLOOR',
    'LA_NOP_CD',
    'LA_NOP_CFD',
    'LA_NOP_CredDefSwap',
    'LA_NOP_Curr',
    'LA_NOP_Commodity',
    'LA_NOP_Deposit',
    'LA_NOP_ETF',
    'LA_NOP_Fut_Fwds',
    'LA_NOP_FXCurrSwap',
    'LA_NOP_FRA',
    'LA_NOP_FreeDefCFs',
    'LA_NOP_FRN',
    'LA_NOP_Options',    
    'LA_NOP_STOCKS',
    'LA_NOP_SWAPS',    
    'LA_NOP_Warrants',
    'LA_NOP_Zero_Coupon_Bonds',
    'LA_NOP_RYAN', #used for my own testing    
    'LA_RYAN' #used for my own testing
]		
		
USDRateDict = acm.FDictionary()
TradeSheet = acm.FCalculationSpace('FTradeSheet')
PortfolioSheet = acm.FCalculationSpace('FPortfolioSheet')
OrderBookSheet = acm.FCalculationSpace('FOrderBookSheet')

cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
		
def present_val(t, leg, *rest):
    pv = 0		
    		
    insType = t.Instrument().InsType()    
    try:		
        if insType in ('BuySellback', 'Warrant', 'CFD', 'Stock', 'Future/Forward', 'VarianceSwap', 'Bill', 'Deposit', 'FRN', 'CD', 'Combination', 'FreeDefCF', 'Commodity', 'Cap', 'Floor', 'EquityIndex'):
            pv = ael.Trade[t.Oid()].present_value()
        elif insType in ('Swap', 'IndexLinkedSwap', 'CurrSwap', 'CreditDefaultSwap', 'EquitySwap', 'Repo/Reverse', 'Bond', 'IndexLinkedBond', 'Zero', 'FRA', 'CLN'):
            if leg or leg !='':
                calc = leg.Calculation()
                pv = calc.PresentValue(cs, t).Number()                
        elif insType in ('TotalReturnSwap'):
            if leg or leg !='':
                for cf in leg.CashFlows():
                    cals = cf.Calculation()                    
                    pv   = cals.PresentValue(cs, t).Number() + pv        
        else:
            pv = ael.Trade[t.Oid()].present_value()        
            
    except Exception, e:
        print 'Present_Val - Error', str(e), ' on trade ', t.Oid()
    return pv		
    
def getTradeUSDRate(t, l, date):
    try:
        if l:
            USDRate = USDRateDict[l.Currency()] = FXRATE.FXRate(ael.Instrument[l.Currency().Name()], date, 'USD')
        else:
            USDRate = USDRateDict[t.Currency()] = FXRATE.FXRate(ael.Instrument[t.Currency().Name()], date, 'USD')
    except:
        if l:
            USDRate = USDRateDict[l.Currency()] = 1
        else:
            USDRate = USDRateDict[t.Currency()] = 1
    return USDRate
		
def write_file(name, data, access):
    f = file(name, access)
    c = csv.writer(f, dialect = 'excel-tab')
    c.writerows(data)
    f.close()    

def getNotional(trade):
    try:
        column    = 'Portfolio Underlying Price'    
        ins       = acm.FInstrument[trade.Instrument().Oid()]    
        notional  = OrderBookSheet.CreateCalculation(ins, column)    
        
        if notional:        
            if notional.Value().Number().__str__() == 'nan':
                return 0
            else:
                return notional.Value().Number() * trade.Nominal()            
        else:
            return 0
    except Exception, e:                        
        return 0
   
def get_PresentValues(trade, leg):
    eval        = 0
    evalUSD     = 0    
    column      = 'Portfolio Present Value Per Currency'    
    USD         = acm.FCurrency['USD']
    vector      = acm.FArray()
    param       = acm.FNamedParameters()
    
    if leg:        
        param.AddParameter('currency', leg.Currency())
    else:
        param.AddParameter('currency', trade.Currency())
    vector.Add(param)
    
    try:
        col_config  = acm.Sheet.Column().ConfigurationFromVector(vector)    
        eval        = TradeSheet.CreateCalculation(trade, column, col_config)    
        
        vector      = acm.FArray()
        param       = acm.FNamedParameters()
        param.AddParameter('currency', USD)    
        vector.Add(param)
        column_config = acm.Sheet.Column().ConfigurationFromVector(vector)    
        evalUSD       = TradeSheet.CreateCalculation(trade, column, column_config)    
         
        if eval or evalUSD:
            if eval.Value()[0].Number().__str__() == 'nan' or evalUSD.Value()[0].Number().__str__() == 'nan':
                return 0, 0
            else:                
                #print 'in get_PresentValues', eval.Value()[0].Number(), evalUSD.Value()[0].Number()
                #This is a FA bug!!!!
                usdPV = evalUSD.Value()[0].Number()
                if eval.Value()[0].Number() > 0:
                    usdPV = abs(usdPV)
                else:
                    usdPV = usdPV * -1 if usdPV > 0 else usdPV
                return eval.Value()[0].Number(), usdPV
        else:
            return 0, 0
    except Exception, e:            
        return 0, 0
       
def get_DeltaValues(trade):
    deltaCalculation = 0
    try:
        deltaCalculation = trade.Instrument().Calculation().PriceDelta(cs)
        return deltaCalculation.Value().Number()
    except Exception, e:        
        return 0

def get_DeltaOneValues(trade, leg):
    eval        = 0    
    column      = 'Portfolio FX Tpl Delta Cash'    
    vector      = acm.FArray()
    param       = acm.FNamedParameters()
    
    if leg:
        param.AddParameter('currency', leg.Currency())
    else:
        param.AddParameter('currency', trade.Currency())        
    vector.Add(param)
    
    try:    
        col_config  = acm.Sheet.Column().ConfigurationFromVector(vector)    
        eval        = TradeSheet.CreateCalculation(trade, column, col_config)
     
        if eval:
                return eval.Value().Number(), eval.Value().Number() * getTradeUSDRate(trade, leg, acm.Time().DateToday())
        else:        
            return 0, 0            
    except Exception, e:            
            return 0, 0
    		
ael_variables = [['tradeFilter', 'TradeFilter', 'string', tradeFilters, '', 0, 1],
                 ['filePath_day', 'File and Path Daily', 'string', None, 'F:/FRONT WORK/NOP/NOD_Risk.tab'],
                 ['RepDay', 'Date', 'string', None, 'Today', 1],
                 ['takeOn', 'Takeon Delta', 'int', [0, 1], 1]]		
		
def ael_main(ael_dict):		
    filename_day   = ael_dict['filePath_day']    		
    takeOn = ael_dict['takeOn']		
        		
    tradeDetail = []
    PVCurrency = []
    		
    inputDate = ael_dict['RepDay']
    if inputDate == 'Today':
        d = acm.DateToday()
    else:
        try:
            d = ael.date_from_string(inputDate, '%Y-%m-%d')
        except:
            d = acm.DateToday()
    		
    #file headings
    tradeDetail.append(['TradeID', 'BuySell', 'TradeDate', 'CptyNbr', 'Book', 'InsAddr', 'SDSID', 'Counterpary', 'insid', 'InsType', 'Expiry', 'Currency', 'Amount', 'PV', 'PV (USD)', 'Delta'])
    count = 0    
    ael.log('Running extract for ' + d)
    TradeFilters = ael_dict['tradeFilter']
    
    for tfName in TradeFilters:
        filter = acm.FTradeSelection[tfName]        
        if filter:
            tf = filter.Trades()
            nonZarFound = False
            
            ctpyId = ''
            sourceCtpyId = 0
            sourceCtpyName = ''
            
            notional = 0                
            
            for t in tf:
                externPort = ''
                PVCurrency = 0, 0
                ctpyId = ''
                sourceCtpyId = ''
                sourceCtpyName = ''
                sourceTraderType = ''
                DeltaOne = 0                
                nonZarFound = False
                
                if t:
                    if t.Instrument().Legs():
                        portfolio = t.Portfolio().Name()                        
                        if portfolio in ( 'MIDAS_FLO', 'MIDAS_FWD', 'MIDAS_IRP', 'MIDAS_JDY', 'MIDAS_FLD'):
                            sourceCtpyId = t.add_info('Source Ctpy Id')
                            sourceCtpyName = t.add_info('Source Ctpy Name')
                            sourceTraderType = t.add_info('Source Trade Type')
                            
                            if t.Counterparty().Type() == 'Intern Dept' and t.Counterparty().Name() != 'MIDAS DUAL KEY':
                                continue
                            
                            if sourceTraderType == 'SH' or sourceCtpyId in ('915215', '32845', '47498', '530766', '545541', '546044', '743062', '808865', '545699', '746396', '830349', '917419', '972414', '215' ):
                               continue
                                    
                            if acm.FParty[sourceCtpyName]:
                                if acm.FParty[sourceCtpyName].Type() == 'Intern Dept':
                                    continue
                        
                        if sourceCtpyId == '':
                            ctpyId = t.Counterparty().Oid()
                        else:
                            ctpyId = sourceCtpyId
                        
                        if t.Instrument().InsType() == 'Curr':
                            nom = t.Premium()

                            PVCurrency = get_PresentValues(t, None)                            
                            
                            SpotUSD = t.Currency().Instrument().UsedPrice(d, 'USD', 'SPOT')                            
                            if t.Currency().Name() != 'USD':                                    
                                PVCurrency = PVCurrency[0], PVCurrency[0] * SpotUSD
                            
                            Purchase = True if PVCurrency[0] > 0 else False
                            
                            tradeDetail.append([t.Oid(), 'Purchase' if PVCurrency[0] > 0 else 'Sale', t.TradeTime(), ctpyId, t.Portfolio().Oid(), t.Instrument().Oid(), t.Portfolio().add_info('BarCap_SMS_CP_SDSID'), \
                            t.Counterparty().Name() if sourceCtpyName == '' else sourceCtpyName, t.Instrument().Name(), t.Instrument().InsType(), t.maturity_date(), t.Currency().Name(), abs(nom) if Purchase else nom if nom < 0 else -1 * nom, PVCurrency[0], PVCurrency[1], 0.0])
                            print 'Legged Trade Level', t.Oid(), 'Purchase' if PVCurrency[0] > 0 else 'Sale', t.TradeTime(), ctpyId, t.Portfolio().Oid(), t.Instrument().Oid(), t.Portfolio().add_info('BarCap_SMS_CP_SDSID'), \
                            t.Counterparty().Name() if sourceCtpyName == '' else sourceCtpyName, t.Instrument().Name(), t.Instrument().InsType(), t.maturity_date(), t.Currency().Name(), abs(nom) if Purchase else nom if nom < 0 else -1 * nom, PVCurrency[0], PVCurrency[1], 0.0
                        
                            for l in t.Instrument().Legs():
                                SpotUSD = t.Instrument().UsedPrice(d, 'USD', 'SPOT')                                
                                PVCurrency = get_PresentValues(t, l)                                            
                                if t.Currency().Name() != 'USD':
                                    PVCurrency = PVCurrency[0], PVCurrency[0] * SpotUSD
                                else:
                                    PVCurrency = PVCurrency[0], PVCurrency[0] * getTradeUSDRate(t, l, acm.Time().DateToday())
                                
                                Purchase = True if PVCurrency[0] > 0 else False
                                nom = t.Nominal()
                                nf  = l.NominalFactor()
                                
                                tradeDetail.append([t.Oid(), 'Purchase' if Purchase else 'Sale', t.TradeTime(), ctpyId, t.Portfolio().Oid(), t.Instrument().Oid(), t.Portfolio().add_info('BarCap_SMS_CP_SDSID'), \
                                t.Counterparty().Name() if sourceCtpyName == '' else sourceCtpyName, t.Instrument().Name(), t.Instrument().InsType(), t.maturity_date(), l.Currency().Name(), abs(nom) * nf if Purchase else nom * nf if nom < 0 else -1 * nom * nf, PVCurrency[0], PVCurrency[1], 0.0])
                                print 'Leg Level', t.Oid(), 'Purchase' if Purchase else 'Sale', t.TradeTime(), ctpyId, t.Portfolio().Oid(), t.Instrument().Oid(), t.Portfolio().add_info('BarCap_SMS_CP_SDSID'), \
                                t.Counterparty().Name() if sourceCtpyName == '' else sourceCtpyName, t.Instrument().Name(), t.Instrument().InsType(), t.maturity_date(), l.Currency().Name(), abs(nom) * nf if Purchase else nom * nf if nom < 0 else -1 * nom * nf, PVCurrency[0], PVCurrency[1], 0.0                                
                        else:
                            for l in t.Instrument().Legs():
                                if nonZarFound:
                                    nonZarFound = False
                                    continue
                                
                                if l.Currency().Name() != 'ZAR':
                                    nonZarFound = True
                                
                                if nonZarFound == True:
                                    for l in t.Instrument().Legs():
                                        PVCurrency = 0, 0                                        
                                        PVCurrency = present_val(t, l), present_val(t, l) * getTradeUSDRate(t, l, acm.Time().DateToday())
                                        
                                        if t.Instrument().InsType() == 'TotalReturnSwap':
                                            PVCurrency = get_DeltaOneValues(t, l)
                                        
                                        if t.Instrument().InsType() == 'TotalReturnSwap' and DeltaOne == PVCurrency[0]:
                                            continue
                                        
                                        Purchase = True if PVCurrency[0] > 0 else False
                                        nom = t.Nominal()
                                        nf  = l.NominalFactor()
                                        
                                        tradeDetail.append([t.Oid(), 'Purchase' if Purchase else 'Sale', t.TradeTime(), ctpyId, t.Portfolio().Oid(), t.Instrument().Oid(), t.Portfolio().add_info('BarCap_SMS_CP_SDSID'), \
                                        t.Counterparty().Name() if sourceCtpyName == '' else sourceCtpyName, t.Instrument().Name(), t.Instrument().InsType(), t.maturity_date(), l.Currency().Name(), abs(nom) * nf if Purchase else nom * nf if nom < 0 else -1 * nom * nf, PVCurrency[0], PVCurrency[1], 0.0])
                                        print 'Leg Level', t.Oid(), 'Purchase' if Purchase else 'Sale', t.TradeTime(), ctpyId, t.Portfolio().Oid(), t.Instrument().Oid(), t.Portfolio().add_info('BarCap_SMS_CP_SDSID'), \
                                        t.Counterparty().Name() if sourceCtpyName == '' else sourceCtpyName, t.Instrument().Name(), t.Instrument().InsType(), t.maturity_date(), l.Currency().Name(), abs(nom) * nf if Purchase else nom * nf if nom < 0 else -1 * nom * nf, PVCurrency[0], PVCurrency[1], 0.0
                                        DeltaOne = PVCurrency[0]                                        
                    else:
                    
                        nonZar = False
                        if t.Instrument():
                            
                            if t.Instrument().Underlying():
                                if t.Currency().Name() != 'ZAR' or t.Instrument().Underlying().Currency().Name() != 'ZAR':
                                    nonZar = True
                            elif t.Currency().Name() != 'ZAR':                            
                                nonZar = True
                            
                            portfolio = t.Portfolio().Name()
                            if portfolio in ( 'MIDAS_FLO', 'MIDAS_FWD', 'MIDAS_IRP', 'MIDAS_JDY', 'MIDAS_FLD'):
                                sourceCtpyId = t.add_info('Source Ctpy Id')
                                sourceCtpyName = t.add_info('Source Ctpy Name')
                                sourceTraderType = t.add_info('Source Trade Type')
                            
                                if sourceTraderType == 'SH' or sourceCtpyId in ('915215', '32845', '47498', '530766', '545541', '546044', '743062', '808865', '545699', '746396', '830349', '917419', '972414', '215' ):
                                    continue
                            
                                if acm.FParty[sourceCtpyName]:
                                    if acm.FParty[sourceCtpyName].Type() == 'Intern Dept':
                                        continue
                                
                            if nonZar:
                                    
                                PVCurrency = get_PresentValues(t, None)
                                
                                if PVCurrency[1] == 0:
                                    PVCurrency = PVCurrency[0],  PVCurrency[0] * getTradeUSDRate(t, None, acm.Time().DateToday())
                                            
                                delta =  get_DeltaValues(t)
                                nom   = getNotional(t)
                                Purchase = True if PVCurrency[0] > 0 else False
                                
                                if t.Instrument().InsType() == 'Option' and t.Instrument().Underlying().InsType() == 'Curr':
                                    displayCurr = t.Instrument().Underlying().Currency().Name()                                    
                                    PVCurrency = PVCurrency[0] * FXRATE.FXRate(ael.Instrument[t.Currency().Name()], d, displayCurr), PVCurrency[1]
                                    nom = nom * FXRATE.FXRate(ael.Instrument[t.Currency().Name()], d, displayCurr)
                                else:
                                    displayCurr = t.Currency().Name()
                                    
                                tradeDetail.append([t.Oid(), 'Purchase' if PVCurrency[0] > 0 else 'Sale', t.TradeTime(), t.Counterparty().Oid(), t.Portfolio().Oid(), t.Instrument().Oid(), t.Portfolio().add_info('BarCap_SMS_CP_SDSID'), \
                                t.Counterparty().Name(), t.Instrument().Name(), t.Instrument().InsType(), t.maturity_date(), displayCurr, abs(nom) if Purchase else nom if nom < 0 else -1 * nom, PVCurrency[0], PVCurrency[1], abs(delta)])
                                print 'Non-Leg Level', t.Oid(), 'Purchase' if PVCurrency[0] > 0 else 'Sale', t.TradeTime(), t.Counterparty().Oid(), t.Portfolio().Oid(), t.Instrument().Oid(), t.Portfolio().add_info('BarCap_SMS_CP_SDSID'), \
                                t.Counterparty().Name(), t.Instrument().Name(), t.Instrument().InsType(), t.maturity_date(), displayCurr, abs(nom) if Purchase else nom if nom < 0 else -1 * nom, PVCurrency[0], PVCurrency[1], abs(delta)
        write_file(filename_day, tradeDetail, 'wb')		
    ael.log('Wrote secondary output to:::' + filename_day)
    ael.log('completed successfully')
    print 'Complete'
