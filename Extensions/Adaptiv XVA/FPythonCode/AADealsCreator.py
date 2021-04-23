""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AADealsCreator.py"
import AACustomDealsCreator as cdc
import acm
import AACfInstrumentDeal
import AAFxForwardDeal
import AAFxSwapDeal
import AAParameterDictionary
import AACfInstrumentDealCCSwap
import AAStockOptionDeal
import AACfInstrumentDealSwaption
import AACfInstrumentDealCapFloor
import AAFRADeal
import AAFxOptionDeal
import AAUtilFunctions as Util
import AAComposer
import AACfInstrumentDealCMSSwap
import AACfInstrumentDealCallPutableSwap
import AAParamsAndSettingsHelper
import AACommodityFutureDeal
import AACommodityOptionDeal
import AAILBondFutureDeal
import AAEquitySwapDeal
import AACreditDefaultSwapDeal
import AAEquityDeal
import AABondOptionDeal
import AABondFutureDeal

logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

def createCashFlowInstrumentDealString(portfolioTradeQuantities, positionProjectedPayments, staticLegInformations, valuationDate, cfInformation):
    (deals, parameterDict) = createAnyCashFlowInstrumentDealString(portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation)
    AddFixedPaymentDeals(deals, parameterDict, positionProjectedPayments)
    return AAParameterDictionary.createReturnDictionary(deals, parameterDict)

def createCashFlowInstrumentCMSSwapDealString(swap, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation):
    AACmsSwap = AACfInstrumentDealCMSSwap.AACMSSwapDeal(swap, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation)
    return AACmsSwap.get()   

def createCallPutableSwapDealString(swap, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation):
    aaCallPutableSwap = AACfInstrumentDealCallPutableSwap.AACfInstrumentDealCallPutableSwap(swap, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation)
    return aaCallPutableSwap.get()   

def createTRSDealString(swap, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation):
    AAEquitySwap = AAEquitySwapDeal.AAEquitySwapDeal(swap, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation)
    return AAEquitySwap.get()

def createCDSDealString(cds, trades, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation):
    aaCreditDefaultSwap = AACreditDefaultSwapDeal.AACreditDefaultSwapDeal(cds, trades, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation, logger)
    return aaCreditDefaultSwap.get()

def createEquityDealString(equity, positionProjectedPayments, positionTradeQuantities):
    aaEquity = AAEquityDeal.AAEquityDeal(equity, positionProjectedPayments, positionTradeQuantities)
    return aaEquity.createStock()

def createCashFlowInstrumentCurrencySwapDealString(currencySwap, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation):
    AAcurrencySwap = AACfInstrumentDealCCSwap.AAMtMCrossCurrencySwapDeal(currencySwap, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation)
    return AAcurrencySwap.get()

def createStepStrikeCapFloorDealString(deals, is_cap, strike, parameterDict, trdQuantity, staticLeginfo, valuationDate, contractSize):
    for cflInfo in staticLeginfo.CashFlowInformations():
        if is_cap and cflInfo.Type() != 'Caplet':
            continue
        if not is_cap and cflInfo.Type() != 'Floorlet':
            continue

        cflStrike = cflInfo.StrikePrice() * 100
        if cflStrike == strike:
            continue

        cflDeal = None
        cashFlowEngine = AACfInstrumentDeal.CashFlowListEngine()
        if is_cap:
            cflDeal = AACfInstrumentDeal.CapInterestDeal(trdQuantity, 
                staticLeginfo, valuationDate, cflInfo, parameterDict,
                cashFlowEngine, contractSize = contractSize,
                stepStrike = cflStrike)
        else:
            cflDeal = AACfInstrumentDeal.FloorInterestDeal(trdQuantity, 
                staticLeginfo, valuationDate, cflInfo, parameterDict, 
                cashFlowEngine, contractSize = contractSize, 
                stepStrike = cflStrike)
        cflDeal.AddInterestCashFlow(cflInfo)
        dealDictionary = cflDeal.CreateInterestDealDictionary()
        deals.Add(dealDictionary.compose())

def AddFixedDeal(deals, parameterDict, discountRate, payment):
    deal = AAComposer.PairList()
    deal["Object"] = "FixedCashflowDeal"
    currStr = payment.Unit().AsString()
    deal["Currency"] = currStr
    mappingLink = acm.FCurrency[currStr].MappedDiscountLink()
    discountCurveName = parameterDict.AddDiscountCurveAndGetName(mappingLink)
    deal["Discount_Rate"] = discountCurveName
    deal["Payment_Date"]=Util.createDateStringFromDateTime(payment.DateTime())
    deal["Amount"] = payment.Number()
    if discountRate:
        deal["Discount_Rate"] = discountRate
    deals.Add(deal.compose())

def IsPremiumInFuture(payment):
    return (payment.Type().Text() in ('Premium', 'FutureSettlement')) and \
    payment.DateTime()[:len('yyyy-mm-dd')] > acm.Time().DateToday()

def AddFixedPaymentDeals(deals, parameterDict, positionProjectedPayments,
                         discountRate=None):
    for payment in positionProjectedPayments:
        if payment.Type() and \
            (payment.Type().Text()=='Cash' or IsPremiumInFuture(payment)):
            #Premium in past has no influence on present value of deal
            AddFixedDeal(deals, parameterDict, discountRate, payment)

def AddFixedPaymentForDividendDeals(deals, parameterDict, positionProjectedPayments,
                                    discountRate=None):
    for payment in positionProjectedPayments:
        if payment.Type() and payment.Type().Text()=='Dividend':
            AddFixedDeal(deals, parameterDict, discountRate, payment)

def createLegCashFlowInstrumentDealString(deals, parameterDict , portfolioTradeQuantities, staticLegInformation, valuationDate, cfInformation, **args):

    legType = staticLegInformation.LegType()
    nominalScaleType = staticLegInformation.NominalScaleType()

    if  legType in ["Fixed", "Fixed Accretive"] and \
            nominalScaleType not in [ "None", "FX", "Initial Price", "Price"]:
        raise AssertionError("NominalScaleType %s on Leg type %s is not supported. " %(nominalScaleType, legType))
    elif legType != "Zero Coupon Fixed" and nominalScaleType not in [ "None", "FX", "Initial Price", "Price"]:
        raise AssertionError("NominalScaleType %s on Leg type %s is not supported. " %(nominalScaleType, legType))

    cashFlowEngine = None
    capfloorDefaultcflEngine = None
    if "staticLegInformationCashFlowEngineDict" in args:
        staticLegInformationCashFlowEngineDict = args["staticLegInformationCashFlowEngineDict"]
        if staticLegInformation in staticLegInformationCashFlowEngineDict:
            cashFlowEngine = staticLegInformationCashFlowEngineDict[staticLegInformation]
    if not cashFlowEngine:
        if nominalScaleType in ["Initial Price", "Price"]:
            raise AssertionError("NominalScaleType %s on Leg type %s is not supported."
            "You need to explicitly specify a cashflowEngine to support above nomial "
            "scale type." %(nominalScaleType, legType))
        else: 
            cashFlowEngine = AACfInstrumentDeal.CashFlowListEngine()
            capfloorDefaultcflEngine = AACfInstrumentDealCapFloor.CashFlowListEngineCapFloor()

    contract_size = None
    if "contractSize" in args:
        contract_size = args["contractSize"]

    fixed_rate = None 
    if "fixedRate" in args:
        fixed_rate = args["fixedRate"]

    buy_sell = None
    if "buySell" in args:
        buy_sell = args["buySell"]
    for tradeQuantity in portfolioTradeQuantities:
        if not cfInformation or staticLegInformation.CashFlowInformations().IndexOf(cfInformation) != -1:
            if staticLegInformation.LegType() == "Fixed":
                if staticLegInformation.NominalScaleType() == "None" and staticLegInformation.InflationScalingType() != "None":
                    indexLinkedLeg = AACfInstrumentDeal.IndexLinkedInterestDeal(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contract_size)
                    indexLinkedLeg.AppendToDealsArray(deals)
                else:
                    fixedLeg = AACfInstrumentDeal.FixedInterestDeal(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contract_size, fixed_rate)
                    fixedLeg.AppendToDealsArray(deals)

            elif staticLegInformation.LegType() == "Fixed Accretive":
                if staticLegInformation.NominalScaleType() == "None" and staticLegInformation.InflationScalingType() != "None":
                    indexLinkedLeg = AACfInstrumentDeal.FixedAccretiveIndexLinkedInterestDeal(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contract_size)
                    indexLinkedLeg.AppendToDealsArray(deals)
                else:
                    fixedLeg = AACfInstrumentDeal.FixedAccretiveInterestDeal(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contract_size, fixed_rate)
                    fixedLeg.AppendToDealsArray(deals)

            elif staticLegInformation.LegType() == "Float":
                floatLeg = AACfInstrumentDeal.FloatInterestDeal(tradeQuantity, staticLegInformation, valuationDate,
                               cfInformation, parameterDict, cashFlowEngine, contract_size, buy_sell)
                floatLeg.AppendToDealsArray(deals)

            elif staticLegInformation.LegType() == "Cap":
                capfloorCflEngine = capfloorDefaultcflEngine if capfloorDefaultcflEngine else cashFlowEngine
                capLeg = AACfInstrumentDeal.CapInterestDeal(tradeQuantity, staticLegInformation, valuationDate,
                               cfInformation, parameterDict, capfloorCflEngine, contract_size, buy_sell)
                capLeg.AppendToDealsArray(deals)
                cap_strike = capLeg.strike
                createStepStrikeCapFloorDealString(deals, True, cap_strike, parameterDict, tradeQuantity, staticLegInformation,
                    valuationDate, contract_size)

            elif staticLegInformation.LegType() == "Floor":
                capfloorCflEngine = capfloorDefaultcflEngine if capfloorDefaultcflEngine else cashFlowEngine
                floorLeg = AACfInstrumentDeal.FloorInterestDeal(tradeQuantity, staticLegInformation, valuationDate, 
                               cfInformation, parameterDict, capfloorCflEngine, contract_size, buy_sell)
                floorLeg.AppendToDealsArray(deals)
                floor_strike = floorLeg.strike
                createStepStrikeCapFloorDealString(deals, False, floor_strike, parameterDict, tradeQuantity, staticLegInformation,
                    valuationDate, contract_size)
            elif staticLegInformation.LegType() == "Capped Float":
                capfloorCflEngine = capfloorDefaultcflEngine if capfloorDefaultcflEngine else cashFlowEngine
                capLeg = AACfInstrumentDeal.CapInterestDeal(tradeQuantity, staticLegInformation, valuationDate, 
                             cfInformation, parameterDict, capfloorCflEngine, contract_size, buy_sell)
                capLeg.AppendToDealsArray(deals)
                floatLeg = AACfInstrumentDeal.FloatInterestDeal(tradeQuantity, staticLegInformation, valuationDate, 
                             cfInformation, parameterDict, cashFlowEngine, contract_size, buy_sell)
                floatLeg.AppendToDealsArray(deals)
                cap_strike = capLeg.strike
                createStepStrikeCapFloorDealString(deals, True, cap_strike, parameterDict, tradeQuantity, staticLegInformation, 
                    valuationDate, contract_size)

            elif staticLegInformation.LegType() == "Floored Float":
                capfloorCflEngine = capfloorDefaultcflEngine if capfloorDefaultcflEngine else cashFlowEngine
                floorLeg = AACfInstrumentDeal.FloorInterestDeal(tradeQuantity, staticLegInformation, valuationDate,
                               cfInformation, parameterDict, capfloorCflEngine, contract_size, buy_sell)
                floorLeg.AppendToDealsArray(deals)
                floatLeg = AACfInstrumentDeal.FloatInterestDeal(tradeQuantity, staticLegInformation, valuationDate, 
                               cfInformation, parameterDict, cashFlowEngine, contract_size, buy_sell)
                floatLeg.AppendToDealsArray(deals)
                floor_strike = floorLeg.strike
                createStepStrikeCapFloorDealString(deals, False, floor_strike, parameterDict, tradeQuantity, staticLegInformation,
                    valuationDate, contract_size)

            elif staticLegInformation.LegType() == "Collared Float":
                capfloorCflEngine = capfloorDefaultcflEngine if capfloorDefaultcflEngine else cashFlowEngine
                capLeg = AACfInstrumentDeal.CapInterestDeal(tradeQuantity, staticLegInformation, valuationDate, 
                        cfInformation, parameterDict, capfloorCflEngine, contract_size, buy_sell)
                capLeg.AppendToDealsArray(deals)
                floorLeg = AACfInstrumentDeal.FloorInterestDeal(tradeQuantity, staticLegInformation, valuationDate, 
                    cfInformation, parameterDict, capfloorCflEngine, contract_size, buy_sell)
                floorLeg.AppendToDealsArray(deals)
                floatLeg = AACfInstrumentDeal.FloatInterestDeal(tradeQuantity, staticLegInformation, valuationDate,
                    cfInformation, parameterDict, cashFlowEngine, contract_size, buy_sell)
                floatLeg.AppendToDealsArray(deals)
                cap_strike = capLeg.strike
                floor_strike = floorLeg.strike
                createStepStrikeCapFloorDealString(deals, True, cap_strike, parameterDict, tradeQuantity, staticLegInformation,
                    valuationDate, contract_size)
                createStepStrikeCapFloorDealString(deals, False, floor_strike, parameterDict, tradeQuantity, staticLegInformation,
                    valuationDate, contract_size)

            elif staticLegInformation.LegType() == "Zero Coupon Fixed":
                compoundLeg = AACfInstrumentDeal.CompoundingFixedInterestDeal(tradeQuantity, staticLegInformation, valuationDate, 
                    cfInformation, parameterDict, cashFlowEngine, contract_size, buy_sell)
                compoundLeg.AppendToDealsArray(deals)
            else:
                legType = staticLegInformation.LegType()
                raise AssertionError("Leg type %s is not supported. " %(legType))        

def createAnyCashFlowInstrumentDealString(portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation, **args):
    parameterDict = AAParameterDictionary.ParameterDictionary()
    deals = acm.FArray()
    for staticLegInformation in staticLegInformations:
        createLegCashFlowInstrumentDealString(deals, parameterDict, portfolioTradeQuantities, 
            staticLegInformation, valuationDate, cfInformation, **args)
    return (deals, parameterDict)

def createFxForwardDateBasisDealString(trades, fxBaseCurrencyDiscountCurveMappingLink):
    deals = acm.FArray()
    parameterDict = AAParameterDictionary.ParameterDictionary()
    for trade in trades:
        deal = AAFxForwardDeal.createFxForwardDateBasisDealDictionary(trade, fxBaseCurrencyDiscountCurveMappingLink, parameterDict)
        dealStr = deal.compose()
        deals.Add(dealStr)
    return AAParameterDictionary.createReturnDictionary(deals, parameterDict)

def createFxForwardDealString(trades):
    deals = acm.FArray()
    parameterDict = AAParameterDictionary.ParameterDictionary()
    for trade in trades:
        if trade.IsFxSwap():
            if trade.IsFxSwapFarLeg():
                #map as FXSwapDeal
                deal = AAFxSwapDeal.createFxSwapDealDictionary(trade, parameterDict)
                if deal:
                    dealStr = deal.compose()
                    deals.Add(dealStr)
            else:
                deal = AAFxSwapDeal.createZeroDealDictionary(trade, parameterDict)
                if deal:
                    dealStr = deal.compose()
                    deals.Add(dealStr)
        else:
            deal = AAFxForwardDeal.createFxForwardDealDictionary(trade, parameterDict)
            dealStr = deal.compose()
            deals.Add(dealStr)
    return AAParameterDictionary.createReturnDictionary(deals, parameterDict)

def createSwaptionDealString(swaption, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation):
    underlying = swaption.Underlying()
    if underlying.IsKindOf("FSwap"):
        if swaption.ExerciseType() == "European":
            AAswaption = AACfInstrumentDealSwaption.AASwaptionDeal(swaption, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation)
            return AAswaption.get()   
        if swaption.ExerciseType() == "Bermudan":
            AAswaption = AACfInstrumentDealSwaption.AABermudanSwaptionDeal(swaption, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation)
            return AAswaption.get()
    elif underlying.IsKindOf("FCurrencySwap"):
        if swaption.ExerciseType() == "European":
            AAswaption = AACfInstrumentDealSwaption.AAXccySwaptionDeal(swaption, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation)
            return AAswaption.get()   
        if swaption.ExerciseType() == "Bermudan":
            AAswaption = AACfInstrumentDealSwaption.AAXccyBermudanSwaptionDeal(swaption, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation)
            return AAswaption.get()

def createStockOptionDealString(stockOption, positionProjectedPayments, positionTradeQuantities, valuationDate, cfInformation):
    aaStockOption = AAStockOptionDeal.AAStockOption(stockOption, positionProjectedPayments, positionTradeQuantities)
    return aaStockOption.createStockOption() 

def createBondOptionDealString(bondoption, positionProjectedPayments, positionTradeQuantities, valuationDate, cfInformation):
    aaBondOption = AABondOptionDeal.AABondOptionDeal(bondoption, positionProjectedPayments, positionTradeQuantities, valuationDate, cfInformation)
    return aaBondOption.get()

def createBondFutureDealString(bondfuture, positionProjectedPayments, trades, valuationDate):
    aaBondFuture = AABondFutureDeal.AABondFutureDeal(bondfuture, positionProjectedPayments, trades, valuationDate)
    return aaBondFuture.get()

def createFRADealString(fra, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation, mtm):
    AAFRA = AAFRADeal.AAFRADeal(fra, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation, mtm)
    return AAFRA.get()

def createCapFloorDealString(capfloor, portfolioTradeQuantities, positionProjectedPayments, staticLegInformations, valuationDate, cfInformation, mtm):
    AACapFloor = AACfInstrumentDealCapFloor.AACapFloorDeal(capfloor, portfolioTradeQuantities, positionProjectedPayments, staticLegInformations, valuationDate, cfInformation, mtm)
    return AACapFloor.get()

def createFXOptionDealString (option, portfolioTradeQuantities, valuationDate,  mtm):
    return AAFxOptionDeal.createFXOptionDealString(option, portfolioTradeQuantities, valuationDate, mtm)

def createCommodityDealString(commodity, trades, value_date, mtm):
    return AACommodityFutureDeal.createCommodityDealString(commodity, trades, value_date, mtm)
    
def createCommodityOptionDealString(option, trades, value_date, mtm):
    return AACommodityOptionDeal.createCommodityOptionDealString(option, trades, value_date, mtm)

def createCommodityFutureDealString(future, trades, value_date, mtm):
    return AACommodityFutureDeal.createCommodityFutureDealString(future, trades, value_date, mtm)

def createIndexLinkedBondFutureDealString(future, trades, staticLegInformations, value_date, mtm):
    return AAILBondFutureDeal.createILBondFutureDealString(future, trades, staticLegInformations, value_date, mtm)

def _categoriseInstrument(instrument):

    if instrument.IsKindOf("FDeposit"):
        return "CashFlowInstrument"
        
    if instrument.IsKindOf("FCommodity"):
        return "Commodity"

    if instrument.IsKindOf("FCurrency"):
        return "FX"

    #
    # Futures
    #
    if instrument.IsKindOf("FFuture"):
        underlying = instrument.Underlying()
        if underlying.IsKindOf("FCommodity"):
            return "CommodityFuture"
        if underlying.IsKindOf("FIndexLinkedBond"):
            return "IndexLinkedBondFuture"
        if underlying.IsKindOf("FBond"):
            return "BondFuture"

    #
    # Options
    #
    if instrument.IsKindOf("FOption"):
        underlying = instrument.Underlying()
        if underlying.IsKindOf("FCommodity"):
            return "CommodityOption"

    return ""

def getCvaDealModelCall(instrument):
    customDealModelCall = cdc.CustomDealModelCall(instrument)
    if customDealModelCall:
        return customDealModelCall
    instrument_group = _categoriseInstrument(instrument)
    if instrument_group:
        return "create" + instrument_group + "DealStringModelCall"

    if instrument.IsKindOf("FStock"):
        return "createEquityDealStringModelCall"
    if instrument.IsKindOf("FFra"):
        return 'createFRAStringModelCall'
    if instrument.IsKindOf("FCap") or instrument.IsKindOf("FFloor"):
        return 'createCapFloorStringModelCall'
    if instrument.IsKindOf('FCurrencySwap'):
        return 'createCashFlowInstrumentCurrencySwapDealStringModelCall'        
    if instrument.IsKindOf('FTotalReturnSwap'):
        return 'createTRSDealStringModelCall'
    if instrument.IsKindOf('FCreditDefaultSwap'):
        return 'createCDSDealStringModelCall'
    if instrument.IsKindOf('FSwap') or instrument.IsKindOf('FIndexLinkedSwap'):
        if  instrument.ExerciseEvents():
            return 'createCallPutableSwapDealStringModelCall'

        for l in instrument.Legs():
            if l.FloatRateReference() and l.FloatRateReference().IsKindOf("FSwap"):
                return 'createCashFlowInstrumentCMSSwapDealStringModelCall'
    if instrument.IsKindOf('FCashFlowInstrument'):
        return 'createCashFlowInstrumentDealStringModelCall'
    if instrument.IsKindOf('FFxRate'):
        return 'createFxForwardDealStringModelCall'
    if instrument.IsKindOf('FOption'):
        if instrument.Underlying().IsKindOf('FCurrency'):
            return 'createFXOptionDealStringModelCall'
        elif instrument.Underlying().IsKindOf('FSwap') or \
            instrument.Underlying().IsKindOf('FCurrencySwap'):
            return 'createSwaptionDealStringModelCall'
        elif instrument.Underlying().IsKindOf('FStock'):
            return 'createStockOptionDealStringModelCall'
        elif instrument.Underlying().IsKindOf('FBond'):
            return 'createBondOptionDealStringModelCall'
    logger.ELOG("Can't calculate CVA for instrument %s of type %s" %(instrument.Name(), instrument.Class().Name()))
    return ''
