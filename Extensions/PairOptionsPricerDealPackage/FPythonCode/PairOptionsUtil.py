from __future__ import print_function
import acm
import math
import re
import itertools
import types
from ChoicesExprInstrument import getFixingSources, getValuationGroups
from DealPackageUtil import IsIterable
from DealPackageDevKit import ParseFloat
from FXOptionPricerExtensionPoint import DefaultFXInstrumentOverride, DefaultPMInstrumentOverride    
from InstrumentPairFromStrUtil import InstrumentPairFromStr

# -------------------------------------------------------------------------------
# Label functions
# -------------------------------------------------------------------------------   
 
def IsFxOption(insOrTrade):
    instrument = insOrTrade.Instrument()
    return instrument.UnderlyingType() == 'Curr'

def CurrencyLabel(isDomPerFor, isCall, put='Put', call='Call'):
    label = ''
    if isDomPerFor:
        label = put if isCall else call
    else:
        label = call if isCall else put
    return label

def QuotationLabelImpl(quotation, fxoCurrency, underlying, strikeCurrency, expressAsPriceOnly):
    label = quotation
    if expressAsPriceOnly:
        # Regardless of quotation, use the 'curr per curr' notation.
        label = strikeCurrency + 'per' + underlying
    else:
        if quotation == "Points of UndCurr":
            label = fxoCurrency + "per" + underlying
        elif quotation == "Pct of Nominal":
            label = "%" + fxoCurrency
        elif quotation == "Points of BaseCurr":
            label = fxoCurrency + "per" + strikeCurrency
    return label

def QuotationLabel(trade, expressAsPriceOnly = False):
    quotation = trade.Instrument().Quotation().Name()
    if not IsFxOption(trade) or (trade.Instrument().IsKindOf('FCombination') and not trade.Instrument().Instruments()):
        return quotation
    else:
        instrument = trade.Instrument()
        if instrument.IsKindOf('FCombination'):
            instrument = instrument.Instruments().First()
        fxoCurrency = instrument.Currency().Name()
        underlying = instrument.Underlying().Name()
        strikeCurrency = instrument.StrikeCurrency().Name()
        return QuotationLabelImpl(quotation, fxoCurrency, underlying, strikeCurrency, expressAsPriceOnly)

def Inverse(quoteQuotationLabel):
    place = quoteQuotationLabel.find('per')
    return quoteQuotationLabel[place+3:] + 'per' + quoteQuotationLabel[:place]

def InterestRateLabel(trade):
    curr = ''
    try:
        curr = trade.Instrument().Underlying().Name()
    except Exception: pass
    return curr + ' %'

# -------------------------------------------------------------------------------
# Calculation parameter functions
# -------------------------------------------------------------------------------  
def UsePerUnitQuotationImpl(attrName):
    configDict = acm.FDictionary()
    configDict.AtPut(acm.FSymbol('UsePerUnitQuotation'), True)
    config = acm.Sheet.Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(configDict) 
    return config    

def PriceGreekExcludeVolatilityMovement(attrName):
    configDict = acm.FDictionary()
    configDict.AtPut(acm.FSymbol('PriceGreekIncludeVolatilityMovement'), False)
    config = acm.Sheet.Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(configDict) 
    return config      

def DomesticColumnConfig(attrName):
    configDict = acm.FDictionary()
    configDict.AtPut(acm.FSymbol('NormalizeFxRisk'), False)        
    config = acm.Sheet.Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(configDict) 
    return config      
    
def DeltaNoSurfaceDelta():
    configDict = acm.FDictionary()
    configDict.AtPut(acm.FSymbol('PriceGreekIncludeVolatilityMovement'), False)
    config = acm.Sheet.Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(configDict) 
    return config        

# -------------------------------------------------------------------------------
# Currency pair help functions
# -------------------------------------------------------------------------------  
def InstrumentPairPointValue(instrPairName):
    pointValue = 0.0001
    try: 
        pointValue = acm.FInstrumentPair[instrPairName].PointValue()
    except Exception:
        pass
    return pointValue
    
def CurrencyStrFromDV(dv):
    currencyStr = ''
    try:
        value = dv.Value()
        if value.IsKindOf(acm.FLot):
            value = value[0]
        currencyStr = ' ' + value.Unit().AsString()
    except Exception as e:
        # Can't trust DV to always be OK
        pass
    return currencyStr    
    
def CurrencyNameFromCurrency(currency):
    currencyStr = ''
    try:
        currencyStr = currency.Name()
    except Exception: pass
    return currencyStr

# -------------------------------------------------------------------------------
# Composite attribute help functions
# -------------------------------------------------------------------------------  
def Flipped(attrName):
    return attrName.startswith('flipped')

def GetOppositeAttributeName(attrName):
    side = 'flippedQuoteTradeCalcVal_'
    if Flipped(attrName):
        side = 'quoteTradeCalcVal_'
    return side + attrName.split('_')[1]

# -------------------------------------------------------------------------------
# Solving parameter functions
# ------------------------------------------------------------------------------- 
def GetMaxMinBounderiesStrikeSolving(midValue):
    return {'minValue': midValue/3, 'maxValue': midValue*3, 'precision' : 0.0001}

def GetInitialBarrierLevel(fwdPrice, barrierTypeForeign):
    fraction = 0.05                                             # TODO: Get from conf/param file in the future
    factor = 1 + fraction if barrierTypeForeign.startswith('Up') else 1 - fraction
    return fwdPrice * factor
    
def GetInitialDoubleBarrierLevel(fwdPrice):
    fraction = 0.05
    factor = 1 + fraction
    return fwdPrice * factor

# -------------------------------------------------------------------------------
# Trade and instrument creation functions
# -------------------------------------------------------------------------------
def SetAttributesOnTradeAndInstrument(fxoTradeDeco, instrumentPair, expiryDate):
    fxoInsDec = fxoTradeDeco.Instrument()
    
    fxoInsDec.ForeignInstrument(instrumentPair.Instrument1())
    fxoInsDec.DomesticCurrency(instrumentPair.Instrument2())
    fxoInsDec.StrikePrice(1)
    fxoInsDec.FxoExpiryDate(expiryDate)
    fxoTradeDeco.FxoPremiumCurr(instrumentPair.Instrument2())
    fxoTradeDeco.Currency(instrumentPair.Instrument2())
    if fxoInsDec.OptionTypeIsCall():
        fxoInsDec.SuggestOptionType(False)  

def GetValidDefaultInstrumentPair(foreignInstrument, domesticCurrency, fallBackPair, isFxOption):
    pairName = 'ACC'
    
    if hasattr(foreignInstrument, 'Name'):
        foreignInstrument = foreignInstrument.Name()
    if hasattr(domesticCurrency, 'Name'):
        domesticCurrency = domesticCurrency.Name()
    
    if foreignInstrument and domesticCurrency:        
        pairName = foreignInstrument+'/'+domesticCurrency
        
    instrPair = InstrumentPairFromStr(pairName, fallBackPair, isFxOption)
    return acm.FInstrumentPair[instrPair]

def SetFXTradeAndInstrumentAttributes(fxoTradeDeco):

    instrumentPair = None
    foreignInstrument = None
    domesticCurrency = None
    expiryDate = '3m'
    
    try:
        instrument = fxoTradeDeco.Instrument()
        foreignInstrument, domesticCurrency, expiryDate = DefaultFXInstrumentOverride(instrument.ForeignInstrument(), instrument.DomesticCurrency(), instrument.ExpiryDate())
    except Exception as e:
        print ('Failure running DefaultFXInstrumentOverride hook', e)
    finally:
        instrumentPair = GetValidDefaultInstrumentPair(foreignInstrument, domesticCurrency, 'EUR/USD', True)

    SetAttributesOnTradeAndInstrument(fxoTradeDeco, instrumentPair, expiryDate)
 

def SetPMTradeAndInstrumentAttributes(pmoTradeDeco):
    instrumentPair = None
    foreignInstrument = None
    domesticCurrency = None
    expiryDate = '3m' 
 
    try:
        instrument = pmoTradeDeco.Instrument()
        foreignInstrument, domesticCurrency, expiryDate = DefaultPMInstrumentOverride(instrument.ForeignInstrument(), instrument.DomesticCurrency(), instrument.ExpiryDate())
    except Exception as e:
        print ('Failure running DefaultPMInstrumentOverride hook', e)
    finally:
        fallBackPair = acm.FPreciousMetalPair.Instances().First().Name()
        instrumentPair = GetValidDefaultInstrumentPair(foreignInstrument, domesticCurrency, fallBackPair, False)
        
    SetAttributesOnTradeAndInstrument(pmoTradeDeco, instrumentPair, expiryDate)
    
def SetCombinationParamsFromFXOTrade(combinationTrade, fxoTrade):
    combination = combinationTrade.Instrument()
    setParams = False
    curr = fxoTrade.Currency()
    und = fxoTrade.CurrencyPair().GetComplementingCurrency(fxoTrade.Currency())
    quotation = fxoTrade.Instrument().Quotation()
    if combination.Currency() != curr:
        setParams = True
        combination.Currency = curr
    if combinationTrade.Currency() != curr:
        setParams = True
        combinationTrade.Currency = curr
    if combination.Underlying() != und:
        setParams = True
        combination.Underlying = und
    if combination.Quotation() != quotation:
        setParams = True
        combination.Quotation = quotation
    return setParams
       
# -------------------------------------------------------------------------------
# Misc FXO help functions
# -------------------------------------------------------------------------------  
def IsDoubleBarrier(barrierType):
    return barrierType.startswith('Double')

def IsFxOptionFlipped(option):
    foreignInstrument = option.Underlying().Name()
    domesticCurrency = option.StrikeCurrency().Name()
    return bool(acm.FInstrumentPair['%s/%s' % (domesticCurrency, foreignInstrument)])

def IsParametricStructureFilter(obj):
    return obj.IsParametricStructure()
def IsParametricStructure():
    return IsParametricStructureFilter

def RoundPremium(premiumCurrency, value, defaultDecimals = 2):
    decimals = defaultDecimals
    roundingSpec = premiumCurrency.RoundingSpecification()
    if roundingSpec:
        rounding = acm.FRounding.Select01("roundingSpec = %d and attribute = 'Premium'" % roundingSpec.StorageId(), "")
        if rounding:
            decimals = rounding.Decimals()
    return round(value, decimals)
    
def IsValidBidAskVolatilitySurfaces(ins):
    volatilities = acm.GetCalculatedValueFromString(ins, acm.GetDefaultContext(), 'snoop(scenarioaxis(theoreticalPrice, <["alternativeContext"], , , ["Bid", "Ask"]>), "volatilityInformation", object)', acm.CreateEBTag()).Value()
    vola, bidAskVola = volatilities
    if not bidAskVola.IsKindOf('FArray'):
        #No bid/ask volatilty surfaces mapped, OK!
        return True
    vola, volaBid, volaAsk = map(lambda vol:vol.VolatilityStructure(), [vola] + list(bidAskVola))
    if type(vola) != type(volaBid) or type(vola) != type(volaAsk):
        acm.Log('Bid/Ask volatility surfaces are of different type than mid surface. This is not a supported usecase, the mid volatilty will be used')
        return False
    return True

def UpdateDealPackageTradeLink(dealPackage, trade, linkName):
    tradeLink = dealPackage.TradeLinkAt(linkName)
    if tradeLink.Trade() != trade:
        tradeLink.Trade().DealPackageTradeLinks().Clear()
        tradeLink.Trade(trade)
        tradeLink.Trade().DealPackageTradeLinks().Add(tradeLink)
        instrumentLink = dealPackage.InstrumentLinkAt(linkName)
        instrumentLink.Instrument().DealPackageInstrumentLinks().Clear()
        instrumentLink.Instrument(trade.Instrument())
        instrumentLink.Instrument().DealPackageInstrumentLinks().Add(instrumentLink)
        return tradeLink


def GetColumnProperties(col, context = acm.GetDefaultContext()):
    if isinstance(col, str):
        col = context.GetExtension('FColumnDefinition', 'FTradingSheet', col)
    columnDictionary = dict(keyValue for keyValue in  zip(col.Value().Keys(), col.Value().Values()))
    if acm.FSymbol('InheritsFrom') in columnDictionary:
        col = context.GetExtension(col.TypeClass(), col.ExtendedClass(), columnDictionary[acm.FSymbol('InheritsFrom')])
        if col:
            parentDict = GetColumnProperties(col, context)
            parentDict.update(columnDictionary)
            return parentDict
    return columnDictionary

def GetColumnsForDealPackage(dealPackageType, context = acm.GetDefaultContext()):
    columns = acm.FArray()
    for col in context.GetAllExtensions('FColumnDefinition', None, False, False, group = 'fx option pricer columns', values = False):
        groupItems = col.Definition().Memberships().At('fx option pricer columns')
        if groupItems.Size() == 0 or groupItems.Includes(acm.FSymbol(dealPackageType.lower())):
            columns.Add(col)
    return columns


lot = acm.GetFunction('lot', 1)

# -------------------------------------------------------------------------------
# Misc calculation functions
# -------------------------------------------------------------------------------  
def GetFloatFromCalculation(calculation, buySell = None):
    value = None
    try:
        value = GetSingleValue(calculation.Value(), buySell).Number()
    except Exception as e:
        pass
    return value

def IsOfTypeFLot(value):
    return hasattr(value, 'IsKindOf') and value.IsKindOf(acm.FLot)
    
def CalculateForwardPoints(forwardPrice, spotPrice, instrPairName):
    return (forwardPrice - spotPrice) / InstrumentPairPointValue(instrPairName)

def CalculateInverseValue(value):
    return 1 / value if value else 1

def IsBidAskValue(value):
    return IsIterable(value) and not isinstance(value, str)

def GetSingleValue(value, buySell = None):
    if value and IsBidAskValue(value):
        value = value[-1] if buySell == "Sell" else value[0] if buySell == "Buy" else (reduce(lambda x,y:x+y, value) / len(value))
    return value

def AlmostEqual(value1, value2, decimals=8):
    if value1 == value2: #Should implement check that can handle both floats and denominated values
        return True
    try:
        return abs(value1 - value2) < float('10e-{}'.format(decimals))
    except TypeError:
        return False
        
def SameValuesInList(values):
    return isinstance(values, list) and len(values) > 1 and AlmostEqual(values[0], values[1])
    
def ValuesAreEqual(value1, value2):
    if IsBidAskValue(value1):
        if IsBidAskValue(value2):
            if len(value1) == len(value2):
                for v1, v2 in zip(value1, value2):
                    if not AlmostEqual(v1, v2):
                        break
                else:
                    return True
        return False
    return AlmostEqual(value1, value2)

def TransformDecimalPoints(value):
    if isinstance(value, list):
        first = value[0]
        groups = re.split('[,\.]' , repr(first))
        decimals = 0 if len(groups) == 1 else len(re.findall('\d', groups[-1]))
        values = [ParseFloat(first)]
        for v in value[1:]:
            if isinstance(v, float):
                v = repr(v)
            try:
                val = int(v) * 10 ** -decimals
                power = 10 ** (len(re.findall('\d', v)) - decimals)
                val = values[0] // power * power + val + (power if round(val, decimals) <= round(values[0] % power, decimals) else 0)
                val = round(val, decimals)
            except ValueError:
                val = ParseFloat(v)
            values.append(val)
        value = values
    return value

def TransformMagnitude(value, currentValue):
    if not currentValue:
        return value
    lb = currentValue / acm.Math.Sqrt(10.0)
    ub = currentValue * acm.Math.Sqrt(10.0)
    returnValue = []
    for v in value if IsBidAskValue(value) else [value]:
        v = ParseFloat(v)
        if v:
            for i in range(100):
                if v > ub:
                    v *= 0.1
                elif v < lb:
                    v *= 10
                else:
                    break
        returnValue.append(v)
    return returnValue if IsBidAskValue(value) else returnValue[0]


# -------------------------------------------------------------------------------
# Choices functions
# -------------------------------------------------------------------------------  
def GetFixingSourceChoices():
    populator = acm.FChoiceListPopulator()
    fixingSources = getFixingSources(True)
    fixingSources.append('')
    populator.SetChoiceListSource(fixingSources)
    return populator   
    
def GetValGroupChoices():
    populator = acm.FChoiceListPopulator()
    valGroups = getValuationGroups()
    populator.SetChoiceListSource(valGroups)
    return populator   
    
# -------------------------------------------------------------------------------
# Strike attribute mapping functions
# -------------------------------------------------------------------------------  
def GuiAttributeToSolverAttributeName(guiAttr):
    solverAttr = guiAttr
    if guiAttr == 'strikeDomesticPerForeign':
        solverAttr = 'solverStrikeDomPerFor'
    elif guiAttr == 'strikeForeignPerDomestic':
        solverAttr = 'solverStrikeForPerDom'
    elif guiAttr == 'strike2DomesticPerForeign':
        solverAttr = 'solverStrike2DomPerFor'
    elif guiAttr == 'strike2ForeignPerDomestic':
        solverAttr = 'solverStrike2ForPerDom'
    return solverAttr

def SolverAttributeToGuiAttributeName(solverAttr):
    guiAttr = solverAttr
    if solverAttr == 'solverStrikeDomPerFor':
        guiAttr = 'strikeDomesticPerForeign'
    elif solverAttr == 'solverStrikeForPerDom':
        guiAttr = 'strikeForeignPerDomestic'
    elif solverAttr == 'solverStrike2DomPerFor':
        guiAttr = 'strike2DomesticPerForeign'
    elif solverAttr == 'solverStrike2ForPerDom':
        guiAttr = 'strike2ForeignPerDomestic'
    return guiAttr

def SolverAttributeChangeOnStripFlip(solverAttr):
    flipMapping = {'strikeDomesticPerForeign':'strikeForeignPerDomestic', 
                   'strikeForeignPerDomestic':'strikeDomesticPerForeign',
                   'strike2DomesticPerForeign':'strike2ForeignPerDomestic',
                 'strike2ForeignPerDomestic':'strike2DomesticPerForeign'}
    return flipMapping.get(solverAttr, solverAttr)


# -------------------------------------------------------------------------------
# Valuation Model info
# -------------------------------------------------------------------------------  
def ValuationAddOnModelIsUsed(instrument):
            isNone = instrument.ValuationAddOnModel() == 'None'
            return not isNone
# -------------------------------------------------------------------------------
# Custom fuction
# -------------------------------------------------------------------------------  
def FlipBidAskPrices(prices, isBidAsk = True):
    if IsBidAskValue(prices):
        if len(prices) == 1:
            prices = prices[0]
        else:
            if isBidAsk:
                prices = list(prices)[::-1]
            prices = lot(prices)
    return prices

def InvBidAsk(prices, isBidAsk = True):
    inv = acm.GetFunction('inv', 1)
    return inv(FlipBidAskPrices(prices, isBidAsk))

# -------------------------------------------------------------------------------
# Choice List values from string
# -------------------------------------------------------------------------------  
def ChoiceListValueFromString(choices, value):
    if type(value) == types.StringType:
        try:
            index = [c.upper() for c in choices].index(value.upper())
            return choices[index]
        except ValueError:
            return None
    return value

def FixingSourceFromString(value):
    valuesAsStrings = [v.Name() if type(v) != types.StringType else v for v in getFixingSources(True)]
    return ChoiceListValueFromString(valuesAsStrings, value)

def ValGroupFromString(value):
    valuesAsStrings = [c.Name() if type(c) != types.StringType else c for c in getValuationGroups()]
    return ChoiceListValueFromString(valuesAsStrings, value)
