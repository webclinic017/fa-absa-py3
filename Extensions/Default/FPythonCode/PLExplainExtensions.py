from __future__ import print_function
import acm
import RiskFactorExtensions
from RiskFactorExtensions import BucketRiskFactor
from RiskFactorExtensions import crType
from RiskFactorExtensions import eqType
from RiskFactorExtensions import fxType
from RiskFactorExtensions import irType
from RiskFactorExtensions import timeType
from RiskFactorExtensions import volType
import StrikeBucketsGeneration
from StrikeBucketsGeneration import GenerateStrikeBuckets
import timeBucketsFromVolatilityStructure
from timeBucketsFromVolatilityStructure import CreateBuckets

def GenerateTimeBucketsFromVolatilityStructure( vs, params ):
    definitions = CreateBuckets( None, vs )
    return acm.Time().CreateTimeBucketsFromDefinitions( acm.Time().DateToday(),
        definitions, None, 0, False, False, False, False, False )
    
    
def NormalizedMarketPrice( price, instrument ):
    insType = instrument.InsType()
    if insType == 'FxSwap':
        return price / 10000.0
    qType = instrument.Quotation().QuotationType()
    qFactor = instrument.Quotation().QuotationFactor()
    if qType in ['Yield', 'Simple Rate']:
        return price / 100.0
    elif qType in ['Coupon', 'Spread']:
        return price * qFactor
    elif qType in ['100-rate']:
        return -acm.GetFunction('deltasub', 2)(price, 100.0) / 100.0
    else:
        return price

def ShiftFactorFromQuotation(quotation):
    return cmp(quotation.QuotationFactor(), 0)

targetSortingKeyByType = {
    irType: [], 
    fxType: []
    }
    
dimensionAndMethodsForSortingByType = {
    irType: [["BenchmarkInstrument", ["Currency", "LastIRSensDay", "StringKey"]]]
    }
    
def RiskFactorComparator(leftRiskFactor, rightRiskFactor):
    rfType = leftRiskFactor.RiskFactorDescription().RiskFactorType()
    methods = ["StringKey"]
    if targetSortingKeyByType.has_key( rfType ):
        methods = targetSortingKeyByType[rfType]
    for method in methods:        
        leftRiskFactorTargetString = leftRiskFactor.Target().PerformWith( method, [], 2 )
        rightRiskFactorTargetString = rightRiskFactor.Target().PerformWith( method, [], 2 )
        if leftRiskFactorTargetString < rightRiskFactorTargetString:
            return -1
        elif leftRiskFactorTargetString > rightRiskFactorTargetString:
            return 1
    
    if dimensionAndMethodsForSortingByType.has_key( rfType ):
        for keyAndMethods in dimensionAndMethodsForSortingByType[ rfType ]:
            key = keyAndMethods[0]
            methods = keyAndMethods[1]
            for method in methods:
                leftCoord = leftRiskFactor.RiskFactorDescription().Coordinate(key).PerformWith( method, [], 2 )
                rightCoord = rightRiskFactor.RiskFactorDescription().Coordinate(key).PerformWith( method, [], 2 )
                if leftCoord < rightCoord:
                    return -1
                elif leftCoord > rightCoord:
                    return 1
    else:
        for key in RiskFactorExtensions.keyOrderForExternalId:
            leftCoord = leftRiskFactor.RiskFactorDescription().Coordinate(key)
            rightCoord = rightRiskFactor.RiskFactorDescription().Coordinate(key)
            if leftCoord < rightCoord:
                return -1
            elif leftCoord > rightCoord:
                return 1
    return 0

#Generic Risk Factor Generator
def BucketRiskFactors(creationScope, targetObjects, coordinateData, riskFactorType, additionalGenerator=None, additionalParams=None, shiftTypes = None):
    riskFactors = acm.FArray()
    for i in range(len(targetObjects)):
        if additionalGenerator:
            for key in additionalGenerator.keys():
                coordinateData[ key ] = additionalGenerator[ key ]( targetObjects[i], additionalParams[ key ] )
        coordinates = None
        for key in coordinateData.keys():
            if not coordinates:
                coordinates = [{key: coord} for coord in coordinateData[ key ] ]
            else:
                newCoordinates = []
                for coord in coordinates:
                    for idx, newCoord in enumerate(coordinateData[ key ]):
                        if idx == 0:
                            coord[ key ] = newCoord
                        else:
                            nc = coord.copy()
                            nc[ key ] = newCoord
                            newCoordinates.append(nc)
                coordinates.extend( newCoordinates )
        if coordinates:
            for coord in coordinates:
                if targetObjects[i] and coord:
                    riskFactors.Add( BucketRiskFactor(targetObjects[i], coord, riskFactorType, None, creationScope, shiftTypes[i] if shiftTypes else None) )
        else:
            riskFactors.Add( BucketRiskFactor(targetObjects[i], {}, riskFactorType, None, creationScope, shiftTypes[i] if shiftTypes else None) )
    return riskFactors


# RISK FACTOR CREATOR

def CreationScope( type, timeBuckets=None, maxCount=-1 ):
    cscope = str(type.MappingType())
    if timeBuckets:
        cscope += "|" + str(acm.TimeBuckets().StoredNameOrSimpleDefinition( timeBuckets ))
    if maxCount > -1:
        cscope += "|" + str(maxCount)
    return cscope

def InterestRateRiskFactors(targetObjects):
    creationScope = CreationScope( irType )
    rfs = []
    instruments = []
    shiftTypes = []
    for bm in targetObjects:
        if bm.Instrument() not in instruments:
            instruments.append( bm.Instrument() )
            shiftTypes.append( bm.ShiftType() )

    for instrument, shiftType in zip(instruments, shiftTypes):
        target = irType.TargetConfiguration('Yield Curve', acm.FObject, None)
        target = irType.TargetConfiguration('BenchmarkInstrument', instrument, target)
        rfs.append( BucketRiskFactor( target, {'BenchmarkInstrument': instrument}, irType, instrument.Name(), creationScope, shiftType ) )
    return rfs

def CreditRiskFactors(targetObjects, timeBuckets, targetCoordinates=None):
    creationScope = CreationScope( crType, timeBuckets )
    coordinates = {'Time':timeBuckets}
    if targetCoordinates:
        for key in targetCoordinates.Keys():
            coordinates[ key ] = [targetCoordinates[ key ]]
    return BucketRiskFactors(creationScope, targetObjects, coordinates, crType)

def VolatilityRiskFactors(targetObjects, timeBuckets, timeBucketsFromStructure, maxCount):
    eqStructures = [to for to in targetObjects if to.IsEqParametricStructure()]
    otherStructures = [to for to in targetObjects if not to.IsEqParametricStructure()]
    
    creationScope = CreationScope( volType, timeBuckets, maxCount )
    if timeBuckets:
        riskFactors = BucketRiskFactors(creationScope, otherStructures, {'Time':timeBuckets}, 
            volType, {'Strike':GenerateStrikeBuckets}, {'Strike':{'maxCount':maxCount}} )
    else:
        riskFactors = BucketRiskFactors(creationScope, otherStructures, {}, 
            volType, {'Strike':GenerateStrikeBuckets, 'Time':GenerateTimeBucketsFromVolatilityStructure}, {'Strike':{'maxCount':maxCount}, 'Time':{}} )

    creationScope = CreationScope( volType, None, -1 )
    riskFactors.AddAll( BucketRiskFactors(creationScope, eqStructures, {}, 
        volType, {'Strike':GenerateStrikeBuckets, 'Time':GenerateTimeBucketsFromVolatilityStructure}, {'Strike':{'maxCount':-1}, 'Time':{}}) )
        
    return riskFactors
    
def TimeRiskFactor():
    riskFactorDescription = timeType.CreateRiskFactorDescription(None, None)
    riskFactor = riskFactorDescription.CreateRiskFactor(None, RiskFactorExtensions.timeShiftConfiguration, 'Time', None)
    return riskFactor

def GetCurrencyPair( curr, fxBaseCurr ):
    cp = acm.FCurrencyPair.Select( "currency1 = '" + curr.Name() + "' and currency2 = '" + fxBaseCurr.Name() +"'")
    if not cp:
        cp = acm.FCurrencyPair.Select( "currency2 = '" + curr.Name() + "' and currency1 = '" + fxBaseCurr.Name() +"'")
    return cp and cp.First() or None

    
def FXRiskFactor( curr1, curr2 ):
    cp = GetCurrencyPair( curr1, curr2 )
    if cp:
        return RiskFactorExtensions.FXRiskFactorFromCurrencyPair( cp )
    print ("No Currency Pair found for currencies " + curr1.Name()  +" and " + curr2.Name())
    return None
    
def FXRiskFactors(targetObjects, fxBaseCurrency):
    rfs = []
    for curr in targetObjects:
        if not curr == fxBaseCurrency:
            riskFactor = FXRiskFactor( curr, fxBaseCurrency )
            if riskFactor:
                rfs.append( riskFactor )
    return rfs


def IRRiskFactorsPerCurve( irCurves ):
    rfs = []
    creationScope = CreationScope( irType )
    for curve in irCurves:
        target = irType.TargetConfiguration('Yield Curve', acm.FObject, None)
        target = irType.TargetConfiguration('BenchmarkInstrument', [bm.Instrument() for bm in curve.Benchmarks().AsArray()], target)
        rfs.append( BucketRiskFactor( target, {'BenchmarkInstrument': [bm.Instrument() for bm in curve.Benchmarks().AsArray()]}, irType, curve.Name(), creationScope ) )
    return rfs

def RiskFactorPairs( rfs1, rfs2 ):
    pairs = acm.FArray()
    for rf1 in rfs1:
        for rf2 in rfs2:
            pairs.Add( acm.FStaticArray( [rf1, rf2] ) )
    return pairs

def CreditIRXFactors( creditCurves, irCurves ):
    return RiskFactorPairs( CreditRiskFactors( creditCurves, [] ), IRRiskFactorsPerCurve( irCurves ) )

def InterestRateFXXFactors( irCurves, currencies, fxBaseCurrency ):
    return RiskFactorPairs( IRRiskFactorsPerCurve( irCurves ), FXRiskFactors( currencies, fxBaseCurrency ) )

def CreditFXXFactors( creditCurves, currencies, fxBaseCurrency ):
    return RiskFactorPairs( CreditRiskFactors( creditCurves, [] ), FXRiskFactors( currencies, fxBaseCurrency ) )

def EquityRateRiskFactors( instruments ):
    rfs = []
    creationScope = CreationScope( eqType )
    for ins in instruments:
        rfs.append( BucketRiskFactor( ins, {}, eqType, ins.Name(), creationScope ) )
    return rfs
    
    
#Fill with default volatility values (until they are added to the Profit/Loss Explain)
def RiskFactorFillVolatilityCoordinates(riskFactor):
    externalId = riskFactor.ExternalId()
    shiftConfiguration = riskFactor.ShiftConfiguration()
    riskFactorDescription = riskFactor.RiskFactorDescription()
    target = riskFactor.Target()
    riskFactorType = riskFactorDescription.RiskFactorType()
    coordinateConfiguration = riskFactorType.CoordinateConfiguration('Time', riskFactorDescription.Coordinate('Time'), None)
    coordinateConfiguration = riskFactorType.CoordinateConfiguration('Strike', riskFactorDescription.Coordinate('Strike'), coordinateConfiguration)
    coordinateConfiguration = riskFactorType.CoordinateConfiguration('UnderlyingMaturity', None, coordinateConfiguration)
    coordinateConfiguration = riskFactorType.CoordinateConfiguration('CallPutType', 'None', coordinateConfiguration)
    newRiskFactorDescription = riskFactorType.CreateRiskFactorDescription(coordinateConfiguration, riskFactorDescription.ValueConfiguration())
    newRiskFactor = newRiskFactorDescription.CreateRiskFactor(target, shiftConfiguration, externalId)
    return newRiskFactor

#Fill with default benchmark price values (until they are added to the Profit/Loss Explain)
def RiskFactorFillBenchmarkPriceCoordinates(riskFactor):
    externalId = riskFactor.ExternalId()
    shiftConfiguration = riskFactor.ShiftConfiguration()
    riskFactorDescription = riskFactor.RiskFactorDescription()
    target = riskFactor.Target()
    riskFactorType = riskFactorDescription.RiskFactorType()
    coordinateConfiguration = riskFactorType.CoordinateConfiguration('Time', None, None)
    coordinateConfiguration = riskFactorType.CoordinateConfiguration('Benchmark Curve', None, coordinateConfiguration)
    coordinateConfiguration = riskFactorType.CoordinateConfiguration('BenchmarkInstrument', riskFactorDescription.Coordinate('BenchmarkInstrument'), coordinateConfiguration)
    newRiskFactorDescription = riskFactorType.CreateRiskFactorDescription(coordinateConfiguration, riskFactorDescription.ValueConfiguration())
    newRiskFactor = newRiskFactorDescription.CreateRiskFactor(target, shiftConfiguration, externalId)
    return newRiskFactor    

def ProfitAndLossExplainTargetForFlatChange(riskFactor):
    if riskFactor.RiskFactorDescription().RiskFactorType() == irType:
        return acm.FYieldCurve[ str(riskFactor.ExternalId()) ]
    return None
