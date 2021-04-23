import acm, FLogger
from at import TP_FX_SPOT, TP_FX_FORWARD
from at_time import acm_datetime
logger = FLogger.FLogger.GetLogger('ROUTING')
logger.Reinitialize(level=1)  # Level 2 is debug , level 1 is for production
SOURCE_PORTFOLIO = acm.Routing().SourcePortfolio()
FOP_PORTFOLIO = acm.Routing().FailedOperationPortfolio()
PARAMS = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', 'ABSASweepingParameters').Value()
portfolios = PARAMS.At('portfolios').Split(',')
mapping = None
CACHED = False
rates = {}

def get_nearleg_nominal(original_trade, trade_artifacts):

    if not original_trade.Instrument().Currency().Name() == 'ZAR':
        return [art_trade.Nominal() for art_trade in trade_artifacts if art_trade.IsFxSwapNearLeg() and \
                           art_trade.Instrument().Currency().Name() == original_trade.Instrument().Currency().Name() and \
                           art_trade.Status() == 'Internal']
    else:
       return [art_trade.Premium() for art_trade in trade_artifacts if art_trade.IsFxSwapNearLeg() and \
                           art_trade.Instrument().Currency().Name() == original_trade.Instrument().Currency().Name() and \
                           art_trade.Status() == 'Internal']
                


def calculate_implied_notional(original_trade, routing_trade, aip_instance, trade_artifacts):

    if not routing_trade.IsFxSwapFarLeg():
        if not routing_trade.IsFxSpot() and aip_instance.B2BCrossMktPr() is not None:
            market_price = aip_instance.B2BCrossMktPr()
        elif aip_instance.B2BCrossSptMktPr() is not None:
            market_price = aip_instance.B2BCrossSptMktPr()
    elif routing_trade.IsFxSwapFarLeg():
        if aip_instance.B2BCrossSwpFarMktPr() is not None:
            market_price = aip_instance.B2BCrossSwpFarMktPr()
        elif aip_instance.B2BCrossMktPr() is not None:
            market_price = aip_instance.B2BCrossMktPr()
            
    if original_trade.IsFxSwap() and routing_trade.IsFxSwapNearLeg():
        nearleg_nominal = get_nearleg_nominal(original_trade, trade_artifacts)
        if not original_trade.Instrument().Currency().Name() == 'ZAR' and nearleg_nominal[0] <> None:
            return nearleg_nominal[0] * market_price*-1
        else:
            return nearleg_nominal[0]/market_price
    elif not original_trade.Instrument().Currency().Name() == 'ZAR':
        return original_trade.Nominal()* market_price*-1
    else:
        return original_trade.Premium()/market_price


        

def is_in_USD_public_holiday(trade):
    holidays = []
    calendar = acm.FCurrency['USD'].Calendar()
    for days in calendar.Dates():
        holidays.append(days.Date())
    
    if trade.IsFxSwap():
        near_leg = trade.FxSwapNearLeg()
        far_leg = trade.FxSwapFarLeg()
        leg = near_leg or far_leg
        return (leg.ValueDay() in holidays) or (trade.ValueDay() in holidays)
    
    val_day_in_hol = trade.ValueDay() in holidays
    return trade.ValueDay() in holidays


def PreCache():

    global CACHED
    global rates
    global mapping

    if CACHED == False:

        user = acm.FUser.Select('')
        mapping = acm.Mapping().GetMap("routingInstructionMapping")
        a = acm.FRoutingInstruction.Select('')
        b = acm.FRoutingInstructionMapping.Select('')
        c = acm.FRoutingOperationParameters.Select('')
        d = acm.FRoutingTradeParameters.Select('')
        [RMap.Query() for RMap in b]

        SML_variance = {'AED':0.75,'AOA':0.75,'AUD':0.10,'BWP':1.50,'CAD':0.05,
                        'CHF':0.05,'CNH':0.75,'CNY':0.75,'CZK':0.01,'DKK':0.05,
                        'EGP':0.75,'EUR':0.07,'GBP':0.05,'GHS':0.05,'HKD':0.05,
                        'HUF':0.25,'ILS':0.75,'INR':1.12,'JPY':0.10,'KES':0.00,
                        'KMF':0.25,'KWD':0.69,'LSL':0.00,'MUR':1.00,'MWK':0.39,
                        'MXN':0.05,'MYR':0.75,'MZN':1.00,'NAD':0.00,'NGN':0.75,
                        'NOK':0.05,'NZD':0.12,'PKR':0.50,'PLN':0.75,'QAR':0.50,
                        'RUB':0.00,'SAR':0.05,'SEK':0.05,'SGD':0.19,'SZL':0.00,
                        'THB':0.75,'TRY':0.05,'TZS':0.50,'UGX':0.50,'USD':0.12,
                        'XAF':0.50,'XAU':0.02,'XOF':0.50,'ZAR':0.05,'ZMW':0.06}

        currency_pairs = acm.FCurrencyPair.Select('')

        for cp in currency_pairs:
            valueDay = acm_datetime('2m') # forward date needed to load base curve for each currency
            trade = acm.FTrade()
            trade.RegisterInStorage()
            trade.TradeTime( acm.Time.TimeNow() )
            trade.AcquireDay(  valueDay )
            trade.ValueDay ( trade.AcquireDay() )
            trade.Instrument( cp.Currency1() )
            trade.Currency( cp.Currency2() )
            rates[cp] = {}
            rates[cp]['trade'] = trade
            rates[cp]['calc_space'] = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), acm.FTradeSheet)
            rates[cp]['calculation'] = rates[cp]['calc_space'].CreateCalculation(trade, 'First Prize FX Rate')
            rates[cp]['calc_space'].SimulateValue(trade, 'Portfolio Currency', cp.Currency1())
            rates[cp]['calc_space'].Refresh()
            rates[cp]['calculation'].Value().Number()
            if cp.IncludesCurrency(acm.FCurrency['USD']):
                complement_curr = cp.GetComplementingCurrency(acm.FCurrency['USD']).Name()
                if complement_curr in SML_variance.keys():
                    rates[cp]['variance'] = SML_variance[complement_curr]
                else:
                    rates[cp]['variance'] = 0.00

        CACHED = True


def CreateTrade( position_dict, trade, commit):

    ZAR = acm.FCurrency['ZAR']
    Currecny1 = position_dict.Keys()[0]
    Currecny2 = position_dict.Keys()[1]

    if abs(position_dict[Currecny1]) > 0.009:
        ProfitCurrency = acm.FCurrency[Currecny1]
        ProfitValue = position_dict[Currecny1]

    if abs(position_dict[Currecny2]) > 0.009:
        ProfitCurrency = acm.FCurrency[Currecny2]
        ProfitValue = position_dict[Currecny2]

    CurrencyPair = ZAR.CurrencyPair(ProfitCurrency)
    Price = get_fx_rate(CurrencyPair, trade.ValueDay())
    SpotDate = CurrencyPair.SpotDate(acm.Time.DateNow())
    SpotPrice = get_fx_rate(CurrencyPair, SpotDate)

    NewTrade = acm.FTrade()
    NewTrade.RegisterInStorage()
    NewTrade.Instrument(CurrencyPair.Currency1())
    NewTrade.Currency(CurrencyPair.Currency2())
    NewTrade.Portfolio('ROUT_INTERBANK')
    NewTrade.Price(Price)
    NewTrade.ReferencePrice(SpotPrice)

    NewTrade.Counterparty(trade.Acquirer())
    if trade.IsFxSpot() == True:
        NewTrade.Acquirer(CurrencyPair.SpotPortfolio().PortfolioOwner())
        NewTrade.TradeProcess( TP_FX_SPOT )
    else:
        NewTrade.Acquirer(CurrencyPair.ForwardPortfolio().PortfolioOwner())
        NewTrade.TradeProcess( TP_FX_FORWARD )

    if ProfitCurrency == CurrencyPair.Currency1():
        NewTrade.Quantity( ProfitValue )
        NewTrade.Premium( -1 * (ProfitValue * Price))
    else:
        NewTrade.Premium( -1 * ProfitValue )
        NewTrade.Quantity( (ProfitValue / Price) )

    NewTrade.ValueDay(trade.ValueDay())
    NewTrade.AcquireDay(trade.AcquireDay())
    NewTrade.Status( 'Internal' )
    NewTrade.TradeTime(trade.TradeTime())
    NewTrade.YourRef(trade.YourRef())

    if commit == True:
        Mirror = CreateMirrorTrade(NewTrade, 'ROUT_INTERBANK', trade.YourRef())  #will the YouRef automaticvally be set
        return [NewTrade, Mirror]
    else:
        NewTrade.MirrorPortfolio( trade.Portfolio())
        return [NewTrade]


def MirrorPortfolioName(trade):
    if trade.MirrorPortfolio() != None:
        return trade.MirrorPortfolio().Name()
'''================================================================================================
why did we do this for mirror trade ?
================================================================================================'''
def CalcProfitValue(dict, trade):

    isMirrorTrade = MirrorPortfolioName(trade) in portfolios #why chek this
    if trade.Portfolio().Name() in portfolios or isMirrorTrade:

        Quantity = trade.Quantity()
        Premium = trade.Premium()
        if isMirrorTrade == False:
            Quantity = -1*Quantity
            Premium = -1*Premium

        if dict.HasKey(trade.Instrument().Name()):
            dict[trade.Instrument().Name()] = dict[trade.Instrument().Name()] + Quantity
        else:
            dict[trade.Instrument().Name()] = Quantity

        if dict.HasKey(trade.Currency().Name()):
            dict[trade.Currency().Name()] = dict[trade.Currency().Name()] + Premium
        else:
            dict[trade.Currency().Name()] = Premium


def FXForeignCurrSellOff( original_trade , constellation , commit = False ):

    if not original_trade.CurrencyPair().IncludesCurrency('ZAR'):
        PosInCurrency = acm.FDictionary()
        for artifact in constellation:
            if artifact.Class() == acm.FTrade:
                CalcProfitValue(PosInCurrency, artifact)

            if artifact.Class() == acm.FFxRiskAllocationResult:
                for trade in artifact.ArtifactsToBeCommitted():
                    CalcProfitValue(PosInCurrency, trade) # ah shit why doing this  ????

        SellTrade = CreateTrade( PosInCurrency, original_trade, commit)
        Cons = FRouting.route( SellTrade[0], {}, commit, False, False )
        return SellTrade, Cons


class TradeAIProxy():

    __trade  = None
    def __init__(self, trade, params = None , ts = False ):
        self.__trade = trade
        self.__params = params or {}
        self.__aip = trade.AdditionalInfo()
        self.__ts = ts

    # Rates
    def B2BSptMktPr(self): return self.__params['B2BSptMktPr'] if 'B2BSptMktPr' in self.__params.keys() else self.__aip.B2BSptMktPr()
    def B2BMktPr(self): return self.__params['B2BMktPr'] if 'B2BMktPr' in self.__params.keys() else self.__aip.B2BMktPr()
    def B2BSwpFarMktPr(self): return self.__params['B2BSwpFarMktPr'] if 'B2BSwpFarMktPr' in self.__params.keys() else self.__aip.B2BSwpFarMktPr()
    def B2BSplitSptMktPr(self): return self.__params['B2BSplitSptMktPr'] if 'B2BSplitSptMktPr' in self.__params.keys() else self.__aip.B2BSplitSptMktPr()
    def B2BSplitMktPr(self): return self.__params['B2BSplitMktPr'] if 'B2BSplitMktPr' in self.__params.keys() else self.__aip.B2BSplitMktPr()
    def B2BSplitSwpFarMktPr(self): return self.__params['B2BSplitSwpFarMktPr'] if 'B2BSplitSwpFarMktPr' in self.__params.keys() else self.__aip.B2BSplitSwpFarMktPr()
    def B2BCrossSptMktPr(self): return self.__params['B2BCrossSptMktPr'] if 'B2BCrossSptMktPr' in self.__params.keys() else self.__aip.B2BCrossSptMktPr()
    def B2BCrossMktPr(self): return self.__params['B2BCrossMktPr'] if 'B2BCrossMktPr' in self.__params.keys() else self.__aip.B2BCrossMktPr()
    def B2BCrossSwpFarMktPr(self): return self.__params['B2BCrossSwpFarMktPr'] if 'B2BCrossSwpFarMktPr' in self.__params.keys() else self.__aip.B2BCrossSwpFarMktPr()
    def B2BAllInPr(self): return self.__params['B2BAllInPr'] if 'B2BAllInPr' in self.__params.keys() else self.__aip.B2BAllInPr()
    def B2BSplitAllInPr(self): return self.__params['B2BSplitAllInPr'] if 'B2BSplitAllInPr' in self.__params.keys() else self.__aip.B2BSplitAllInPr()

    # Portfolios
    def B2BPortfolioSpt(self): return self.__params['B2BPortfolioSpt'] if 'B2BPortfolioSpt' in self.__params.keys() else self.__aip.B2BPortfolioSpt()
    def B2BPortfolioFwd(self): return self.__params['B2BPortfolioFwd'] if 'B2BPortfolioFwd' in self.__params.keys() else self.__aip.B2BPortfolioFwd()

    def Trade(self): return self.__trade
    def AddInfoProxy(self): return self.__aip
    def TradeServicesCall(self):return self.__ts

TradeAIproxyInstance = None


def isCross(trade):
    if 'USD' not in (trade.CurrencyPair().Currency1().Name(), trade.CurrencyPair().Currency2().Name()):
        return True
    return False


def banking_holiday_check(trade):
    
    if isCross(trade) and is_in_USD_public_holiday(trade):
        trade.CurrencyPair().SpotSplitPair(None)
        trade.CurrencyPair().ForwardSplitPair(None)
        trade.AdditionalInfo().B2BPortfolioSpt(None)
        trade.AdditionalInfo().B2BPortfolioFwd(None)
        trade.AdditionalInfo().B2BMktPr(0.0)
        trade.AdditionalInfo().B2BSptMktPr(0.0)
        trade.AdditionalInfo().B2BSplitMktPr(0.0)
        trade.AdditionalInfo().B2BSplitSptMktPr(0.0)
        trade.RegisterInStorage()
        
    return trade


def ensure_configuration_valid():
    if not SOURCE_PORTFOLIO:
        raise RuntimeError('Invalid configuration: No source portfolio set')
    if not FOP_PORTFOLIO:
        raise RuntimeError('Invalid configuration: No failed operation portfolio set')
    if is_member_of_or_same_as(FOP_PORTFOLIO, SOURCE_PORTFOLIO):
        raise RuntimeError('Invalid configuration: Failed operation portfolio %s is member of or same as source portfolio %s', \
            FOP_PORTFOLIO.Name(), SOURCE_PORTFOLIO.Name())


def execute_instruction(trade, instruction,routingparams,commit = True,ts = False,fs = False):
    global TradeAIproxyInstance
    TradeAIproxyInstance = TradeAIProxy(trade, routingparams, ts)
    
    trade = banking_holiday_check(trade)

    tempTrade = None
    if trade.IsFxSwap() and trade.FxSwapNearLeg().CorrectionTrade() != None:
        tempTrade = trade.FxSwapNearLeg().CorrectionTrade()
        trade.FxSwapNearLeg().CorrectionTrade(None)
    result = instruction.Execute(trade)         #returns FRoutingOperationResult
    if tempTrade != None:trade.FxSwapNearLeg().CorrectionTrade(tempTrade)
    
    
    artifacts = result.CreatedArtifacts()       #Array with FFxRiskAllocationResult()
    
    if tempTrade != None:
        for art in artifacts:                       #we need to check what type atrtifacts is
            if art.Class() == acm.FFxRiskAllocationResult:
                for trade in art.ArtifactsToBeCommitted():
                    if trade.IsFxSwap() and trade.FxSwapNearLeg():
                        trade.FxSwapNearLeg().CorrectionTrade(tempTrade)
    if isCross(trade) and '|FFO|' in trade.OptionalKey():
        for art in artifacts:
            if art.Class() == acm.FFxRiskAllocationResult:
                for art_trade in art.ArtifactsToBeCommitted():
                    if (art_trade.Currency().Name() == trade.Currency().Name() and not trade.Instrument().Currency().Name() == 'ZAR') or (art_trade.Currency().Name() == trade.Instrument().Currency().Name() and trade.Instrument().Currency().Name() == 'ZAR'):
                        if art_trade.Status() == "Internal":
                            recalculated_notional = calculate_implied_notional(trade, art_trade, TradeAIproxyInstance, art.ArtifactsToBeCommitted())
                            logger.info('recalculated_notional is: {}'.format(recalculated_notional))
                            if recalculated_notional <> None:
                                price = abs(recalculated_notional/art_trade.Nominal())
                                art_trade.Price(price)
                                if art_trade.Nominal() < 0:
                                    art_trade_premium = abs(recalculated_notional)*1
                                else:
                                    art_trade_premium = abs(recalculated_notional)*-1
                                art_trade.Premium(art_trade_premium)
                                art_trade.RegisterInStorage()
                                logger.info('{} price changed successfully to: {}'.format(art_trade.CurrencyPair().Name(), price))
                        

    ZarCon = None
    if fs == True:
        FsTrades, ZarCon = FXForeignCurrSellOff(trade, artifacts)
    
    #Upgrade 2017 - FFxRiskAllocationResult object does not return optional key for parent trade anymore
    if not trade.IsFxSwap() and artifacts[0].IsKindOf(acm.FFxRiskAllocationResult):
        if len(artifacts[0].ArtifactsToBeCommitted()) > 0:
            parent_artifact_trd = artifacts[0].ArtifactsToBeCommitted()[0]
            parent_artifact_trd.OptionalKey(trade.OptionalKey())
        
    if commit == True:
        try:
            acm.BeginTransaction()
            trade.Commit()
            #logger.debug('Committing routed trade %d', trade.Oid())
            for artifact in artifacts:
                artifact.Commit()
                #logger.debug('Committing artifact %s', artifact.ClassName())
            if fs == True:
                for fst in FsTrades:
                    fst.Commit
                if ZarCon != None:
                    for t in ZarCon:
                        t.Commit()
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            #logger.debug('Could not commit transaction')
            raise
    
    #if fs == False:
    #    return artifacts , ZarCon #ah cant return this because trying to commit it again do we need to yes?
    #else:
    return artifacts


def find_routing_instruction(trade):
    global mapping
    if mapping == None: mapping = acm.Mapping().GetMap("routingInstructionMapping")
    return mapping.MatchSingle(trade)


def is_member_of_or_same_as(child, parent):
    if not child: return False
    if child == parent: return True
    links = acm.FPortfolioLink.Select('memberPortfolio="' + child.Name() + '"')
    return any(is_member_of_or_same_as(link.OwnerPortfolio(), parent) for link in links)


def route(trade, routingparams = None, commit = True, ts = False, fs = False):
    if not CACHED:
        logger.debug('Calling PreCache')
        PreCache()
    
    #logger.debug('Logging for 4-Front Swap Trade - Near Leg', trade.FxSwapNearLeg())
    #logger.debug('Logging for 4-Front Swap Trade - Far Leg', trade)

    if not should_be_routed(trade):
        logger.debug('Trade %d is not a candidate for routing (OptionalKey: %s)', trade.Oid(), trade.OptionalKey())
        return
    logger.debug('Message is trade %d YourRef is %s (OptionalKey: %s)', trade.Oid(), trade.YourRef(), trade.OptionalKey())

    routing_instruction = find_routing_instruction(trade)

    if not routing_instruction:
        logger.debug('No routing instruction matched for trade %d (OptionalKey: %s)', trade.Oid(), trade.OptionalKey())
        return
    logger.debug('Executing routing instruction "%s" on trade %d (OptionalKey: %s)', routing_instruction.Name(), trade.Oid(), trade.OptionalKey())

    try:
        artifacts = execute_instruction(trade, routing_instruction, routingparams, commit, ts, fs)
    except Exception as ex:
        logger.error("Risk routing failed (OptionalKey: %s)", trade.OptionalKey(), exc_info=1)
        raise
    finally:
        if trade.CurrencyPair().IsModified():
            trade.CurrencyPair().Undo()

    logger.info('Routing of trade %d completed, using instruction "%s"', trade.Oid(), routing_instruction.Name())

    return artifacts


def should_be_routed(trade):
    if trade.IsFxSwapNearLeg():
        logger.debug('Will not route FX swap near leg trades')
        return False
    elif not is_member_of_or_same_as(trade.Portfolio(), SOURCE_PORTFOLIO):
        logger.debug('Trade %d is not in source portfolio', trade.Oid()) #where does debug tooooo? Not the ATS log so stupid........
        return False
    return True


ensure_configuration_valid()
