#   encoding: utf-8
from __future__ import print_function
import acm, ael
import datetime

# --- Creation of objects ---
def createPortfolio(name, curr):
    port = acm.FPhysicalPortfolio(name)
    port.Name(name)
    port.AssignInfo(name)
    port.Currency(curr)
    return port
            
def createPortfolios(dictionary):
    if dictionary.has_key('Portfolio'):
        name = dictionary['Portfolio']['Id']
        curr = dictionary['Portfolio']['Currency']
        port = createPortfolio(name, curr)
        port.Commit()
    if dictionary.has_key('Portfolios'):
        portList = dictionary['Portfolios']
        for portDict in portList:
            name = portDict['Id']
            curr = portDict['Currency']
            port = createPortfolio(name, curr)
            port.Commit()

def createCounterparty(name):
    counterparty = acm.FCounterParty(name)
    counterparty.Name(name)
    return counterparty

def createCounterparties(dictionary):
    if dictionary.has_key('Counterparties'):
        countList = dictionary['Counterparties']
        for countDict in countList:
            count = createCounterparty(countDict['Id']);
            count.Commit()

def createMarket(dictionary):
    name = dictionary['Id']
    type = dictionary['Type']
    market = None
    if type.upper() == 'MTMMARKET':
        market = acm.FMTMMarket(name)
    if type.upper() == 'MARKETPLACE':
        market = acm.FMarketPlace(name)
    if market != None:
        market.Name(name)
    return market
  
def createMarkets(dictionary):
    if dictionary.has_key('Markets'):
        marketList = dictionary['Markets']
        for marketDict in marketList:
            market = createMarket(marketDict);
            if market != None:
                market.Commit()
            else:
                print ('Could not create market', dictionary['Id'])
              
def createStockOld(name, curr, spotDays):
    ins = acm.FStock(name)
    ins.Name(name)
    ins.Currency(curr)
    ins.SpotBankingDaysOffset(spotDays)
    return ins

def setInstrumentDetails(ins, dictionary):
    ins.Name(dictionary['Id'])
    ins.Currency(dictionary['Currency'])
    if dictionary.has_key('Underlying'):
        und = acm.FInstrument[dictionary['Underlying']]
        ins.Underlying(und)
        ins.UnderlyingType(und.InsType())
    if dictionary.has_key('ExpiryDate'):
        ins.ExpiryDate(dictionary['ExpiryDate'])
    if dictionary.has_key('ExpiryTime'):
        ins.ExpiryTime(dictionary['ExpiryTime'])
    if dictionary.has_key('ContractSize'):
        ins.ContractSize(dictionary['ContractSize'])
    if dictionary.has_key('ExerciseType'):
        ins.ExerciseType(dictionary['ExerciseType'])#'American')
    if dictionary.has_key('Quotation'):
        ins.Quotation(dictionary['Quotation'])#'Per Unit')
    if dictionary.has_key('QuoteType'):
        ins.QuoteType(dictionary['QuoteType'])#'Per Unit')
    if dictionary.has_key('PayType'):
        ins.PayType(dictionary['PayType'])#'Spot')
    if dictionary.has_key('SettlementType'):
        ins.SettlementType(dictionary['SettlementType'])#'Physical Delivery')
    if dictionary.has_key('StrikePrice'):
        ins.StrikePrice(dictionary['StrikePrice'])
    if dictionary.has_key('StrikeType'):
        ins.StrikeType(dictionary['StrikeType'])#'Absolute')
    if dictionary.has_key('OTC'):
        ins.Otc(dictionary['OTC'])
        
def setInstrumentProperties(ins, dictionary):
    # --- ID ---
    if dictionary.has_key('Isin'):
        ins.Isin(dictionary['Isin'])
    if dictionary.has_key('ExternalId1'):
        ins.ExternalId1(dictionary['ExternalId1'])
    if dictionary.has_key('ExternalId2'):
        ins.ExternalId2(dictionary['ExternalId2'])
    # --- Offsets ---
    if dictionary.has_key('SpotBankingDaysOffset'):
        ins.SpotBankingDaysOffset(dictionary['SpotBankingDaysOffset'])
    if dictionary.has_key('PayOffsetMethod'):
        ins.PayOffsetMethod(dictionary['PayOffsetMethod'])
    if dictionary.has_key('IssueDay'):
        ins.IssueDay(dictionary['IssueDay'])
    if dictionary.has_key('MinimumPiece'):
        ins.MinimumPiece(dictionary['MinimumPiece'])
    if dictionary.has_key('MinimumIncremental'):
        ins.MinimumIncremental(dictionary['MinimumIncremental'])
    # --- Ex Coupons ---
    # --- Misc ---
    if dictionary.has_key('FreeText'):
        ins.FreeText(dictionary['FreeText'])
    if dictionary.has_key('OriginalCurrency'):
        ins.OriginalCurrency(dictionary['OriginalCurrency'])
    if dictionary.has_key('MtmFromFeed'):
        ins.MtmFromFeed(dictionary['MtmFromFeed'])
   
def setAelInstrumentProperties(ins, dictionary):
    # --- ID ---
    if dictionary.has_key('Isin'):
        ins.isin = dictionary['Isin']
    if dictionary.has_key('ExternalId1'):
        ins.extern_id1 = dictionary['ExternalId1']
    if dictionary.has_key('ExternalId2'):
        ins.extern_id2 = dictionary['ExternalId2']
    # --- Offsets ---
    if dictionary.has_key('SpotBankingDaysOffset'):
        ins.spot_banking_days_offset = int(dictionary['SpotBankingDaysOffset'])
    if dictionary.has_key('PayOffsetMethod'):
        ins.pay_offset_method = dictionary['PayOffsetMethod']
    if dictionary.has_key('IssueDay'):
        ins.issue_day = ael.date(dictionary['IssueDay'])
    if dictionary.has_key('MinimumPiece'):
        ins.minimum_piece = dictionary['MinimumPiece']
    if dictionary.has_key('MinimumIncremental'):
        ins.minimum_incremental = dictionary['MinimumIncremental']
    # --- Ex Coupons ---
    # --- Misc ---
    if dictionary.has_key('FreeText'):
        ins.free_text = dictionary['FreeText']
    if dictionary.has_key('OriginalCurrency'):
        ins.original_currency = ael.Instrument[dictionary['OriginalCurrency']]
    if dictionary.has_key('MtmFromFeed'):
        ins.mtm_from_feed = int(dictionary['MtmFromFeed'])
     
def createStock(dictionary):
    ins = acm.FStock(dictionary['Id'])
    ins.Name(dictionary['Id'])
    ins.Currency(dictionary['Currency'])
    setInstrumentProperties(ins, dictionary)
    return ins
                
def createCurrency(name):
    curr = ael.Instrument.new('Curr')
    curr.insid = name
    curr.commit()
    ael.poll()
    return curr
    
def createBaseCurrency(name):
    curr = createCurrency(name)
    curr2 = curr.clone()
    curr2.curr = curr
    curr2.commit()
    ael.poll()
    
def createCurrencies(insList):
    currencyFound = False
    # Create Base Currencies
    for insDict in insList:
        insType = insDict['Type']
        if insType.upper().startswith('CURR'):
            currencyFound = True
            name = insDict['Id']
            if name == insDict['Currency']:
                createBaseCurrency(name)
                ins = acm.FInstrument[name]
                setInstrumentProperties(ins, insDict)
                ins.Commit()
    # Create non base currencies
    for insDict in insList:
        insType = insDict['Type']
        if insType.upper().startswith('CURR'):
            name = insDict['Id']
            if name != insDict['Currency']:
                createCurrency(name)
                ins = acm.FInstrument[name]
                ins.Currency = insDict['Currency']
                setInstrumentProperties(ins, insDict)
                ins.Commit()
    return currencyFound
  
def createBond(dictionary):
    required = ['Id', 'Currency',]
    assertRequired('Bond', required, dictionary)
    bond = ael.Instrument.new('Bond')
    bond.insid = dictionary['Id']
    bond.curr = ael.Instrument[dictionary['Currency']]
    if dictionary.has_key('Quotation'):
        bond.quote_type = dictionary['Quotation']
    if dictionary.has_key('ExCouponPeriod'):
        bond.ex_coup_period = dictionary['ExCouponPeriod']
    if dictionary.has_key('ExCouponMethod'):
        bond.ex_coup_method = dictionary['ExCouponMethod']
    setAelInstrumentProperties(bond, dictionary)
    # Cashflow settings on leg
    leg = bond.legs()[0]
    if dictionary.has_key('StartDay'):
        leg.start_day = getDay(dictionary['StartDay'])
    if dictionary.has_key('EndDay'):
        leg.end_day = getDay(dictionary['EndDay'])
    else:
        if dictionary.has_key('StartDay') and dictionary.has_key('EndPeriod'):
            startDay = getDay(dictionary['StartDay'])
            endPeriod = dictionary['EndPeriod']
            leg.end_day = getDay(str(startDay) + endPeriod)
    if dictionary.has_key('EndPeriod'):
        leg.end_period = dictionary['EndPeriod']
    if dictionary.has_key('FixedRate'):
        leg.fixed_rate = float(dictionary['FixedRate'])
    if dictionary.has_key('RollingPeriod'):
        leg.rolling_period = dictionary['RollingPeriod']
    if dictionary.has_key('PayOffset'):
        leg.pay_day_offset = dictionary['PayOffset']
    if dictionary.has_key('PayMethod'):
        leg.pay_day_method = dictionary['PayMethod']
    return bond
    
def createFutureForward(dictionary):
    required = ['Id', 'Currency', 'Underlying', 'ExpiryDate', 'ContractSize']
    assertRequired(dictionary['Type'], required, dictionary)
    ins = acm.FFuture(dictionary['Id'])
    payType = dictionary['Type']
    if dictionary.has_key('PayType') and dictionary['PayType'] != '':
        payType = dictionary['PayType']
    ins.PayType(payType)
    setInstrumentDetails(ins, dictionary)
    setInstrumentProperties(ins, dictionary)
    return ins

def createOption(dictionary):
    required = ['Id', 'Currency', 'Underlying', 'ExpiryDate', 'ExpiryTime', 'ContractSize', 'ExerciseType']
    assertRequired('Option', required, dictionary)
    option = acm.FOption(dictionary['Id'])
    setInstrumentDetails(option, dictionary)
    setInstrumentProperties(option, dictionary)
    return option

def assertRequired(type, requiredKeys, dictionary):
    for key in requiredKeys:
        if not dictionary.has_key(key):
            raise Exception('%s must have key %s' %(type, key))

def createCommitPrices(dictionary):
    if dictionary.has_key('Prices'):
        pricesList = dictionary['Prices']
        useUpdateOrder = False
        for priceDict in pricesList:
            if priceDict.has_key('UpdateOrder') and priceDict['UpdateOrder'] != '':
                useUpdateOrder = True
        if useUpdateOrder:
            import time
            pricesList.sort(cmp=UpdateOrderCompare)
            for priceDict in pricesList:
                price = createPrice(priceDict)
                price.Commit()
                time.sleep(1)
        else:
            acm.BeginTransaction()
            try:
                for priceDict in pricesList:
                    price = createPrice(priceDict)
                    price.Commit()
                acm.CommitTransaction()
            except:
                acm.AbortTransaction()
                raise
                
def UpdateOrderCompare(x, y):
        if x['UpdateOrder'] > y['UpdateOrder']:
            return 1
        else:
            return -1
              
def createPrice(dictionary):
    ins = acm.FInstrument[dictionary['Instrument']]
    #market = acm.FMarketPlace[dictionary['Market']]
    price = acm.FPrice()
    price.Instrument(ins)
    price.Market(dictionary['Market'])
    price.Currency(dictionary['Currency'])
    print ('')
    print ('Day', dictionary['Day'])
    print (changeDateStr(dictionary['Day']))
    price.Day(changeDateStr(dictionary['Day']))
    if dictionary.has_key('TradeTime') and dictionary['TradeTime'] != '':
        price.TradeTime(changeDateTimeStr(dictionary['TradeTime']))
    priceSetBits = 0
    if dictionary.has_key('Ask') and dictionary['Ask'] != '':
        price.Ask(dictionary['Ask'])
        priceSetBits += 2
    if dictionary.has_key('Bid') and dictionary['Bid'] != '':
        price.Bid(dictionary['Bid'])
        priceSetBits += 1
    if dictionary.has_key('Open') and dictionary['Open'] != '':
        price.Open(dictionary['Open'])
        priceSetBits += 128
    if dictionary.has_key('Last') and dictionary['Last'] != '':
        price.Last(dictionary['Last'])
        priceSetBits += 16
    if dictionary.has_key('Settle') and dictionary['Settle'] != '':
        price.Settle(dictionary['Settle'])
        priceSetBits += 256
    price.Bits(priceSetBits)
    return price
  
def createCommitTrades(dictionary):
    if dictionary.has_key('Trades'):
        tradeList = dictionary['Trades']
        if tradeList != None:
            port = acm.FPhysicalPortfolio[dictionary['Portfolio']['Id']]
            acm.BeginTransaction()
            try:
                #-- Create and populate trade
                for tradeDict in tradeList:
                    trade = createTrade(port, tradeDict)
                    trade.Commit()
                acm.CommitTransaction()
            except:
                acm.AbortTransaction()
                raise
                    
def createTrade(port, dictionary):
    ins = acm.FInstrument[dictionary['Instrument']]
    count = acm.FCounterParty[dictionary['Counterparty']]
    acq = acm.FCounterParty[dictionary['Acquirer']]
    trade = acm.FTrade()
    trade.Portfolio(port)
    trade.Instrument(ins)
    trade.Counterparty(count)
    trade.Acquirer(acq)
    trade.Price(dictionary['Price'])
    trade.Quantity(dictionary['Quantity'])
    trade.Premium(dictionary['Premium'])
    trade.ValueDay(dictionary['ValueDay'])
    trade.AcquireDay(dictionary['AcquireDay'])
    trade.TradeTime(dictionary['TradeTime'])
    trade.Currency(dictionary['Currency'])
    if dictionary.has_key('Status'):
        trade.Status(dictionary['Status'])
    return trade
  
def createPriceFinding(dictionary):
    pf = acm.FPriceFinding(dictionary['Id'])
    pf.Name(dictionary['Id'])
    pf.Market(dictionary['Market'])
    pf.PriceType(dictionary['PriceType'])
    pf.MarketRule(dictionary['MarketRule'])
    pf.CurrencyRule(dictionary['CurrencyRule'])
    return pf
   
def createContextLink(dictionary):
    link = acm.FContextLink(dictionary['Id'])
    link.Name(dictionary['Id'])
    link.Context(dictionary['Context'])
    link.Type(dictionary['ParameterType'])
    link.MappingType(dictionary['MappingType'])
    link.Instrument(dictionary['Instrument'])
    return link
    
def createTestAccountingParameters(name):
    acc_param = acm.FAccountingParameters(name)
    acc_param.Name(name)
    # ---
    acc_param.PlVersion(2)
    acc_param.MtmMarket('internal')
    acc_param.AccountMethod('Mark-to-Market')
    acc_param.MatchMethod('Open Average')
    # ---
    acc_param.RealizeDaily(1)
    # --- Fee Allocation
    acc_param.SwapPremiumAllocate('As Fee')
    acc_param.AssignmentFeeAllocate('As Fee on Trade Day')
    acc_param.BrokerFeeAllocate('As Fee on Trade Day')
    acc_param.InternalFeeAllocate('As Fee on Trade Day')
    acc_param.ExtensionFeeAllocate('As Fee on Trade Day')
    acc_param.TerminationFeeAllocate('As Fee on Trade Day')
    acc_param.CashAllocate('As Fee on Trade Day')
    acc_param.ExerciseCashAllocate('As Fee on Trade Day')
    # --- Premium/Discount Distributions
    acc_param.IraPremiumAllocate('Depr Prem At Maturity')
    acc_param.BondPremiumAllocate('Depr Prem At Maturity')
    acc_param.ZeroPremiumAllocate('Depr Prem At Maturity')
    acc_param.BillPremiumAllocate('Depr Prem At Maturity')
    acc_param.FrnPremiumAllocate('Depr Prem At Maturity')
    acc_param.InstrumentDaycountAllocate(1)
    # --- Interest Income/Expense
    acc_param.FraPremiumAllocate('As Interest Coupon')
    acc_param.InterestDueAllocate('As Interest Coupon')
    acc_param.Commit()
    return acc_param

def createAccountingParameters(dict):
    acc_param = acm.FAccountingParameters(dict['Id'])
    acc_param.Name(dict['Id'])
    # ---
    acc_param.PlVersion(2)
    key = 'MtMMarket'
    if dict.has_key(key) and dict[key] != '':
        acc_param.MtmMarket(dict[key])
    key = 'Method'
    if dict.has_key(key) and dict[key] != '':
        acc_param.AccountMethod(dict[key])
    key = 'Position'
    if dict.has_key(key) and dict[key] != '':
        acc_param.MatchMethod(dict[key])
    # ---
    key = 'RealizeDaily'
    if dict.has_key(key) and dict[key] != '':
        acc_param.RealizeDaily(dict[key])
    # --- Fee Allocation
    key = 'SwapsPremium'
    if dict.has_key(key) and dict[key] != '':
        acc_param.SwapPremiumAllocate(dict[key])
    key = 'AssignementFee'
    if dict.has_key(key) and dict[key] != '':
        acc_param.AssignmentFeeAllocate(dict[key])
    key = 'BrokerFee'
    if dict.has_key(key) and dict[key] != '':
        acc_param.BrokerFeeAllocate(dict[key])
    key = 'InternalFee'
    if dict.has_key(key) and dict[key] != '':
        acc_param.InternalFeeAllocate(dict[key])
    acc_param.ExtensionFeeAllocate('As Fee on Trade Day')
    acc_param.TerminationFeeAllocate('As Fee on Trade Day')
    acc_param.CashAllocate('As Fee on Trade Day')
    acc_param.ExerciseCashAllocate('As Fee on Trade Day')
    # --- Premium/Discount Distributions
    acc_param.IraPremiumAllocate('Depr Prem At Maturity')
    acc_param.BondPremiumAllocate('Depr Prem At Maturity')
    acc_param.ZeroPremiumAllocate('Depr Prem At Maturity')
    acc_param.BillPremiumAllocate('Depr Prem At Maturity')
    acc_param.FrnPremiumAllocate('Depr Prem At Maturity')
    acc_param.InstrumentDaycountAllocate(1)
    # --- Interest Income/Expense
    acc_param.FraPremiumAllocate('As Interest Coupon')
    acc_param.InterestDueAllocate('As Interest Coupon')
    acc_param.Commit()
    return acc_param

def linkAccountingParameterToContext(accParam, portfolio):
    context = acm.FContext['Global']
    if context == None:
        raise Exception('Context Global does not exist. Exiting...')
        
    link = acm.FContextLink(accParam.Name())
    link.Type('Accounting Parameter')
    link.Name(accParam.Name())
    link.MappingType('Portfolio')
    link.Portfolio(portfolio)
    link.Context(context)
    link.Commit()
    return link

def createTestValuationParameters(name):
    val_param = acm.FValuationParameters(name)
    # --- General
    val_param.Name(name)
    # --- Profit & Loss
    # - FX Conversion
    val_param.RealizeOverCurrencies(1)
    val_param.AccountingCurrency('EUR')
    val_param.ProfitAndLossPeriodFX('Report Date')
    val_param.AggregateCurrencyChoice('Portfolio Curr')
    val_param.PositionCurrencyChoice('Instrument Curr')
    val_param.PremiumFXTranslation('Payments')
    # - Historical Financing
    val_param.DisableFunding(1)
    # - Other
    val_param.PlUntilSpot(1)
    val_param.CloseDerivativesAfterExpiry(1)
    val_param.ForwardStartPL(1)
    # --- Default Price Finding
    val_param.PricefindingType('SprAvg')
    val_param.PricefindingMarketRule('Median')
    val_param.PricefindingCurrencyRule('Shortest')
    # --- Greeks & Buckets
    val_param.IrShiftType('Rectangle')
    # --- Model Settings
    # - Miscellaneous Options Pricing
    val_param.TrinomialSteps(200)
    val_param.BdtTrinomStepsPerPeriod(1)
    val_param.BdtTrinomStepsPeriodType('Per rolling period')
    # - Binomial Parameters
    val_param.BinomialSteps(200)
    val_param.BinomialForward(1)
    val_param.BinomialModel('Normal equal probability')
    val_param.BinomialBSSmooth(1)
    val_param.BinomialRichardson(1)
    # - Finite Difference Parameters
    val_param.FiniteStateSteps(100)
    val_param.FiniteTimeSteps(100)
    val_param.PdeType(1)
    # - LIBOR Market Model
    val_param.LmmSimulations(5000)
    val_param.BoundarySimulations(2000)
    val_param.BgmFactors(2)
    val_param.LmmRandom('Sobol')
    val_param.LmmJumpType('Short Step')
    val_param.LmmPriceFunction('Andersen I')
    # - Basket CDS Model
    val_param.CdsBasketSimulations(10000)
    val_param.CdsBasketRandom('Sobol')
    # --- IR & Hedge Parameters
    val_param.ConfidenceInterval(95.0)
    val_param.ShortVolatility(10.0)
    val_param.ShortCorrelation(0.6)
    val_param.LongVolatility(7.0)
    val_param.LongCorrelation(0.95)
    # --- Misc
    # - Security Settings
    val_param.Val01CTD(1)
    # - Trade Endtry Defaults
    val_param.LockOutPeriodJGB_count(3)
    val_param.LockOutPeriodJGB_unit('Days')
    # - Other
    val_param.GridMinimumDays(7.3)
    val_param.YtmMod('ISMA')
    val_param.Commit()
    return val_param
    
def createValuationParameters(name, dict):
    val_param = acm.FValuationParameters[name]
    if val_param == None:
        val_param = createTestValuationParameters(name)
    # --- Profit & Loss
    # - FX Conversion
    key = 'RealizeOverCurrencies'
    if dict.has_key(key) and dict[key] != '':
        val_param.RealizeOverCurrencies(dict[key])
    key = 'AccountingCurrency'
    if dict.has_key(key) and dict[key] != '':
        val_param.AccountingCurrency(dict[key])
    key = 'HistoricalPaymentFX'
    if dict.has_key(key) and dict[key] != '':
        val_param.HistoricalFXChoice(dict[key])
    key = 'HistoricalPaymentFXDay'
    if dict.has_key(key) and dict[key] != '':
        val_param.HistoricalFXDay(dict[key])
    key = 'HistoricalPaymentFXCurrency'
    if dict.has_key(key) and dict[key] != '':
        val_param.HistoricalFXCurrency(dict[key])
    key = 'PLPeriodFX'
    if dict.has_key(key) and dict[key] != '':
        val_param.ProfitAndLossPeriodFX(dict[key])
    key = 'AggregateDisplayCurrency'
    if dict.has_key(key) and dict[key] != '':
        val_param.AggregateCurrencyChoice(dict[key])
    key = 'PositionReportCurrency'
    if dict.has_key(key) and dict[key] != '':
        val_param.PositionCurrencyChoice(dict[key])
    key = 'FXPremiumTranslation'
    if dict.has_key(key) and dict[key] != '':
        val_param.PremiumFXTranslation(dict[key])
    # - Historical Financing
    key = 'DisableFunding'
    if dict.has_key(key) and dict[key] != '':
        val_param.DisableFunding(dict[key])
    # - Other
    key = 'PLUntilSpot'
    if dict.has_key(key) and dict[key] != '':
        val_param.PlUntilSpot(dict[key])
    key = 'PLUntilStartDayOfForwardStartingInstrument'
    if dict.has_key(key) and dict[key] != '':
        val_param.PlUntilForwardStartingIns(dict[key])
    key = 'CloseDerivativeAfterExpiry'
    if dict.has_key(key) and dict[key] != '':
        val_param.CloseDerivativesAfterExpiry(dict[key])
    key = 'ForwardStartPL'
    if dict.has_key(key) and dict[key] != '':
        val_param.ForwardStartPL(dict[key])
    key = 'DiscountMTM_VALUE_BO'
    if dict.has_key(key) and dict[key] != '':
        val_param.DiscountMtmValueBO(dict[key])
    key = 'PLDiscounting'
    if dict.has_key(key) and dict[key] != '':
        val_param.PlDiscount(dict[key])
    key = 'PLDecompositionCutOffTime'
    if dict.has_key(key) and dict[key] != '':
        val_param.PlCutOffTime(dict[key])
    # --- Default Price Finding
    key = 'PriceType'
    if dict.has_key(key) and dict[key] != '':
        val_param.PricefindingType(dict[key])
    else:
        val_param.PricefindingType('SprAvg')
    key = 'MarketRule'
    if dict.has_key(key) and dict[key] != '':
        val_param.PricefindingMarketRule(dict[key])
    else:
        val_param.PricefindingMarketRule('Median')
    key = 'CurrencyRule'
    if dict.has_key(key) and dict[key] != '':
        val_param.PricefindingCurrencyRule(dict[key])
    else:
        val_param.PricefindingCurrencyRule('Shortest')
    val_param.Commit()
    return val_param

def overrideValuationParameters(valParam):
    whereClause = "user='%s' and overrideLevel='User'" %acm.User().Name()
    parMappings = acm.FParameterMapping.Select(whereClause)
    if len(parMappings) > 0:
        parMapp = parMappings[0]
    else:
        parMapp = acm.FParameterMapping('')
        parMapp.User(acm.User())
        parMapp.OverrideLevel('User')
        parMapp.Commit()

    # First unmap parameter if existing
    whereClause = "parameterType='Valuation Par' and parameterMapping=%s" %parMapp.Oid()
    parMappInstances = acm.FParMappingInstance.Select(whereClause)
    if len(parMappInstances) > 0:
        parMappInstances[0].Delete()
 
    parMappInstance = acm.FParMappingInstance('')
    parMappInstance.ValuationParameters(valParam)
    parMappInstance.ParameterType('Valuation Par')
    parMappInstance.ParameterMapping(parMapp)
    parMappInstance.Commit()
 
def createExtensionValues(dictionary):
    if dictionary.has_key('ExtensionValues'):
        extList = dictionary['ExtensionValues']
        if type(extList) == type({}):
            extList = [extList]
        for extDict in extList:
            extName = extDict['Name']
            extValue = extDict['Value']
            if extDict.has_key('Class'):
                extClass = extDict['Class']
            else:
                extClass = 'FObject'
            createExtensionValue(extName, extValue, extClass)
    
def createExtensionValue(extName, extValue, extClass='FObject'):
    context = acm.GetDefaultContext()
    editModule = context.EditModule()
    moduleName = editModule.Name()
    text = '[%s]%s:%s\n"%s"\n¤' %(moduleName, extClass, extName, extValue)
    context.EditImport('FExtensionValue', text)
    
# --- Misc create functions ---
def getDay(dayStr):
    if dayStr.upper() == 'TODAY':
        dayStr = acm.Time.DateToday()
        day = getDateFromString(dayStr)
    elif dayStr.upper().startswith('TODAY'):
        todayStr = acm.Time.DateToday()
        day = addDeltaToDate(dayStr, todayStr, dayStr[len('TODAY'):len(dayStr)])
    elif len(dayStr) > 10:
        date = dayStr[0:10]
        deltaStr = dayStr[10:len(dayStr)]
        day = addDeltaToDate(dayStr, date, deltaStr)
    else:
        day = getDateFromString(dayStr)
    if day.weekday() == 5:
        # Add two days for saturdays
        day += datetime.timedelta(days=2)
    if day.weekday() == 6:
        # Add one day for sundays
        day += datetime.timedelta(days=1)
    return ael.date(str(day))

def changeDateStr(day):
    if day.upper() == 'TODAY':
        day = acm.Time.DateToday()
    elif day.upper().startswith('TODAY'):
        todayStr = acm.Time.DateToday()
        day = str(addDeltaToDate(day, todayStr, day[len('TODAY'):len(day)]))
    return day

def changeDateTimeStr(dayTime):
    if dayTime.upper() == 'NOW':
        now = datetime.datetime.now()
        dayTime = now.strftime('%Y-%m-%d %H:%M:%S')
    elif dayTime.upper().startswith('NOW'):
        dayTime = addDeltaToTime(dayTime, dayTime[len('NOW'):len(dayTime)])
    return dayTime
   
def addDeltaToTime(orig, deltaStr):
    deltaStr = deltaStr.replace(' ', '')
    last = deltaStr[len(deltaStr)-1]
    delta = int(deltaStr[0:len(deltaStr)-1])
    date = datetime.datetime.now()
    if last.upper() == 'D':
        diff = datetime.timedelta(days=delta)
    elif last.upper() == 'H':
        diff = datetime.timedelta(hours=delta)
    elif last.upper() == 'M':
        diff = datetime.timedelta(minutes=delta)
    elif last.upper() == 'S':
        diff = datetime.timedelta(seconds=delta)
    elif last.upper() == 'W':
        diff = datetime.timedelta(weeks=delta)
    else:
        msg = "Wrong delta character '%s' in '%s'" %(last, orig)
        raise Exception(msg)
    day = date + diff
    return day.strftime('%Y-%m-%d %H:%M:%S')
        
def addDeltaToDate(orig, dayStr, deltaStr): 
    deltaStr = deltaStr.replace(' ', '')
    last = deltaStr[len(deltaStr)-1]
    delta = int(deltaStr[0:len(deltaStr)-1])
    date = getDateFromString(dayStr)
    if last.upper() == 'Y':
        year = int(date.year) + delta
        day = date.replace(year=year)
    elif last.upper() == 'W':
        diff = datetime.timedelta(weeks=delta)
        day = date + diff
    elif last.upper() == 'D':
        diff = datetime.timedelta(days=delta)
        day = date + diff
    else:
        msg = "Wrong delta character '%s% in '%s'" %(last, orig)
        raise Exception(msg)
    return day

def getDateFromString(str):
    year = int(str[0:4])
    month = int(str[5:7])
    day = int(str[8:10])
    return datetime.date(year, month, day)
    
# --- Deletion of objects ---
def deleteExtensionValues(dictionary, verbose=False):
    if dictionary.has_key('ExtensionValues'):
        extList = dictionary['ExtensionValues']
        if type(extList) == type({}):
            extList = [extList]
        for extDict in extList:
            extName = extDict['Name']
            if extDict.has_key('Class'):
                extClass = extDict['Class']
            else:
                extClass = 'FObject'
            deleteExtensionValue(extName, extClass, verbose)
            
def deleteExtensionValue(extName, extClass='FObject', verbose=False):
    editModule = acm.GetDefaultContext().EditModule()
    moduleName = editModule.Name()
    ext = editModule.RemoveExtension('FExtensionValue', extClass, extName)
    if ext != None and verbose:
        print ('Removed FExtensionValue %s in %s module' %(ext.Name(), moduleName))
        
def deleteAccountingParameters(dictionary, verbose=False):
    if dictionary.has_key('AccountingParameters'):
        accList = dictionary['AccountingParameters']
        for accDict in accList:
            name = accDict['Id']
            deleteAccountingParameterByName(name, verbose)
        
def deleteAccountingParameter(dictionary):
    if dictionary.has_key('AccountingParameters'):
        name = dictionary['AccountingParameters']['Id']
        deleteAccountingParameterByName(name)

def deleteAccountingParameterByName(name, verbose=False):
        accParam = acm.FAccountingParameters[name]
        whereClause = "type='Accounting Parameter' and mappingType='Portfolio'"
        contextLinks = acm.FContextLink.Select(whereClause)
        for link in contextLinks:
            if link.Name() == name:
                if verbose:
                    print ('Deleting ContextLink', link.Name(), link.Oid())
                link.Delete()
        if accParam != None:
            if verbose:
                print ('Deleting AccountingParameter', accParam.Name(), accParam.Oid())
            accParam.Delete()

def deleteValuationParameter(dictionary):
    if dictionary.has_key('ValuationParameters'):
        valName = dictionary['ValuationParameters']['Id']
        valParam = acm.FValuationParameters[valName]
        if valParam != None:
            whereClause = "parameterType='Valuation Par' and valuationParameters='%s'" %valName
            parMappInstances = acm.FParMappingInstance.Select(whereClause)
            for parMappInstance in parMappInstances:
                if parMappInstance.UpdateUser() == acm.User():
                    parMappInstance.Delete()       
            valParam.Delete()
            
def deleteValuationParameterMappings(name):
    valParam = acm.FValuationParameters[name]
    if valParam != None:
        whereClause = "parameterType='Valuation Par' and valuationParameters='%s'" %name
        parMappInstances = acm.FParMappingInstance.Select(whereClause)
        for parMappInstance in parMappInstances:
            if parMappInstance.UpdateUser() == acm.User():
                parMappInstance.Delete()       

def deletePortfolio(dictionary):
    if dictionary.has_key('Portfolio'):
        port = acm.FPhysicalPortfolio[dictionary['Portfolio']['Id']]
        if port != None:
            port.Delete()
                
def deleteTrades(dictionary):
    if dictionary.has_key('Portfolio'):
        port = acm.FPhysicalPortfolio[dictionary['Portfolio']['Id']]
        if port != None:
            tradesColl = port.Trades()
            for trade in tradesColl:
                trade.Delete()

def deleteCommitAllTrades(portId):
        port = acm.FPhysicalPortfolio[portId]
        #Delete trades and perhaps aggregated trades
        if port != None:
            tradesColl = port.Trades()
            if tradesColl.Size() > 0:
                ael.begin_transaction
                try:
                    sqlStr = 'select trdnbr from trade where aggregate_trdnbr in ('
                    for trade in tradesColl:
                        sqlStr += ',' + str(trade.Oid())
                    sqlStr = sqlStr.replace('(,', '(')
                    sqlStr += ') and archive_status=1'
                    print (sqlStr)
                    tradeIds = ael.dbsql(sqlStr)
                    for id in tradeIds[0]:
                        trade = ael.Trade[id[0]]
                        if trade != None:
                            print ('Deleting trade', trade.trdnbr)
                            trade.delete()
                    ael.commit_transaction
                except:
                    ael.abort_transaction
                    raise
                acm.BeginTransaction()
                try:
                    for trade in tradesColl:
                        print ('Deleting trade', trade.Oid())
                        trade.Delete()
                    acm.CommitTransaction()
                except:
                    acm.AbortTransaction()
                    raise

def deleteCounterparties(dictionary, verbose=False):
    if dictionary.has_key('Counterparties'):
        countList = dictionary['Counterparties']
        for countDict in countList:
            count = acm.FCounterParty[countDict['Id']];
            if count != None:
                if verbose:
                    print ('Deleting Counterparty', count.Name(), count.Oid())
                count.Delete()
            
def deleteMarkets(dictionary, verbose=False):
    if dictionary.has_key('Markets'):
        marketList = dictionary['Markets']
        for marketDict in marketList:
            market = None
            name = marketDict['Id']
            type = marketDict['Type']
            if type.upper() == 'MTMMARKET':
                market = acm.FMTMMarket[name]
            if type.upper() == 'MARKETPLACE':
                market = acm.FMarketPlace[name]
            if market != None:
                if verbose:
                    print ('Deleting Market', market.Name(), market.Oid())
                market.Delete()

def deleteContextLinks(dictionary):
    if dictionary.has_key('ContextLinks'):
        linkList = dictionary['ContextLinks']
        for linkDict in linkList:
            select = "name='%s'" % linkDict['Id']
            link = acm.FContextLink.Select01(select, '')
            if link != None:
                link.Delete()
                
def deletePriceFindings(dictionary):
    if dictionary.has_key('PriceFindings'):
        findList = dictionary['PriceFindings']
        for findDict in findList:
            priceFinding = acm.FPriceFinding[findDict['Id']]
            if priceFinding != None:
                priceFinding.Delete()

def deleteInstrumentPrices(insList):
    for insDict in insList:
        ins = acm.FInstrument[insDict['Id']]
        if ins != None:
            whereClause = "instrument=%d" % (ins.Oid())
            pricesColl = acm.FPrice.Select(whereClause)
            for price in pricesColl:
                price.Delete()

def deletePrice(price, insName, verbose):
    if verbose:
        print ('Deleting Price %d for %s in %s at %s' \
        %(price.Oid(), insName, price.Currency().Name(), price.Day()))
    price.Delete()

def deleteInstrument(name, verbose=False):
    ins = acm.FInstrument[name]
    if ins != None:
        whereClause = "instrument=%d" % (ins.Oid())
        pricesColl = acm.FPrice.Select(whereClause)
        for price in pricesColl:
            deletePrice(price, ins.Name(), verbose)
        for price in ins.Prices():
            deletePrice(price, ins.Name(), verbose)
        if verbose:
            print ('Deleting', ins.InsType(), ins.Name(), ins.Oid())
        ins.Delete()
                      
def deleteInstruments(insList, type, verbose=False):
    for insDict in insList:
        if insDict['Type'].upper() == type.upper():
            deleteInstrument(insDict['Id'], verbose)

def deleteCurrencies(insList, verbose=False):
    # Delete non base currencies
    for insDict in insList:
        if insDict['Type'].upper().startswith('CURR'):
            name = insDict['Id']
            if name != insDict['Currency']:
                deleteInstrument(name, verbose)
    # Delete base currencies
    for insDict in insList:
        if insDict['Type'].upper().startswith('CURR'):
            name = insDict['Id']
            if name == insDict['Currency']:
                deleteInstrument(name, verbose)
                
# --- Check existance ---                    
def checkNoExistance(dictionary, checkList):
    strPortfolio = 'Portfolio'
    strInstruments = 'Instruments'
    strCounterparties = 'Counterparties'
    strMarkets = 'Markets'
    strAccountingParameters = 'AccountingParameters'
    strValuationParameters = 'ValuationParameters'
    strExtensionValue = 'ExtensionValues'
    for name in checkList:
        if name == strPortfolio and dictionary.has_key(strPortfolio):
            portName = dictionary[strPortfolio]['Id']
            port = acm.FPhysicalPortfolio[portName]
            if port != None:
                return createExistanceMessage(port, portName, strPortfolio)
        if name == strInstruments and dictionary.has_key(strInstruments):
            insList = dictionary[strInstruments]
            for insDict in insList:
                insName = insDict['Id']
                ins = acm.FInstrument[insName]
                if ins != None:
                    return createExistanceMessage(ins, insName, 'Instrument')
        if name == strCounterparties and dictionary.has_key(strCounterparties):
            countList = dictionary[strCounterparties]
            for countDict in countList:
                countName = countDict['Id']
                count = acm.FCounterParty[countName]
                if count != None:
                    return createExistanceMessage(count, countName, 'Counterparty')
        if name == strMarkets and dictionary.has_key(strMarkets):
            marketList = dictionary[strMarkets]
            for marketDict in marketList:
                marketName = marketDict['Id']
                party = acm.FParty[marketName]
                if party != None:
                    return createExistanceMessage(party, marketName, 'Market')
        if name == strAccountingParameters and dictionary.has_key(strAccountingParameters):
            accParamName = dictionary[strAccountingParameters]['Id']
            accParam = acm.FAccountingParameters[accParamName]
            if accParam != None:
                return createExistanceMessage(accParam, accParamName, 'Accounting Parameter')
        if name == strValuationParameters and dictionary.has_key(strValuationParameters):
            valParamName = dictionary[strValuationParameters]['Id']
            valParam = acm.FValuationParameters[valParamName]
            if valParam != None:
                return createExistanceMessage(valParam, valParamName, 'Valuation Parameter')
        if name == strExtensionValue and dictionary.has_key(strExtensionValue):
            #def getExt(extName, extClass='FObject'):
            extName = dictionary[strExtensionValue]['Name']
            if dictionary[strExtensionValue].has_key('Class'):
                extClass = dictionary[strExtensionValue]['Class']
            else:
                extClass = 'FObject'
            editModule = acm.GetDefaultContext().EditModule()
            ext = editModule.GetExtension('FExtensionValue', extClass, extName)
            if ext != None:
                return  'FExtensionValue %s with value %s already created in module %s' \
                        %(extName, ext.Value(), editModule.Name())

    
    return None
        
    
def createExistanceMessage(fObject, name, type):
    message = '%s %s already created by user: %s' %(name, type, fObject.CreateUser().Name())
    message += ' at time: %s' %convertSecToString(fObject.CreateTime())
    return message
        
def convertSecToString(seconds, format='%Y-%m-%d %H:%M:%S'):
    import time
    return time.strftime(format, time.strptime(time.ctime(seconds)))





