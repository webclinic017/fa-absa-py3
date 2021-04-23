
import acm

fxType = acm.RiskFactor.RiskFactorType('FX')
fxShiftConfiguration = fxType.ShiftConfiguration('DifferenceType', 'Relative')
fxValueConfiguration = fxType.ValueConfiguration('ValueUnit', 'Percent')

irType = acm.RiskFactor.RiskFactorType('Benchmark Price')
irShiftConfiguration = irType.ShiftConfiguration('DifferenceType', 'Absolute')
irValueConfiguration = irType.ValueConfiguration('ValueUnit', 'Basis Point')

crType = acm.RiskFactor.RiskFactorType('Par CDS Rate')
crShiftConfiguration = crType.ShiftConfiguration('DifferenceType', 'Absolute')
crValueConfiguration = crType.ValueConfiguration('ValueUnit', 'Basis Point')
crValueConfiguration = crType.ValueConfiguration('CalcType', 'Par CDS Rate', crValueConfiguration)
crValueConfiguration = crType.ValueConfiguration('DaycountMethod', 'Act/360', crValueConfiguration)
crValueConfiguration = crType.ValueConfiguration('RateType', 'Quarterly', crValueConfiguration)

volType = acm.RiskFactor.RiskFactorType('Volatility')
volShiftConfiguration = volType.ShiftConfiguration('DifferenceType', 'Absolute')
volShiftConfiguration = volType.ShiftConfiguration('ShiftType', 'Triangle', volShiftConfiguration)
volValueConfiguration = volType.ValueConfiguration('ValueUnit', 'Percent')

timeType = acm.RiskFactor.RiskFactorType('Time')
timeShiftConfiguration = timeType.ShiftConfiguration('DifferenceType', 'Absolute')

eqType = acm.RiskFactor.RiskFactorType('Equity')
eqShiftConfiguration = eqType.ShiftConfiguration('DifferenceType', 'Relative')
eqValueConfiguration = volType.ValueConfiguration('ValueUnit', 'Percent')

keyOrderForExternalId = ['CreditEntity', 'Seniority', 'Restructuring', 'Currency', 'Time', 'Strike', 'BaseCurrency', 'TermCurrency']
propertyForExternalId = ['Name', 'Name', 'AsString', 'Name', 'Name', 'Name', 'First.Name', 'Name']

configurationsByType = {
    fxType : [fxShiftConfiguration, fxValueConfiguration],
    irType : [irShiftConfiguration, irValueConfiguration],
    crType : [crShiftConfiguration, crValueConfiguration],
    volType : [volShiftConfiguration, volValueConfiguration],
    eqType : [eqShiftConfiguration, eqValueConfiguration]
    }
    

def RiskFactorExternalId( riskFactorDescription, target ):
    externalId = ""
    if not target.IsKindOf(acm.FClass):
        externalId = target.StringKey()
    for key, property in zip(keyOrderForExternalId, propertyForExternalId):
        coord = riskFactorDescription.Coordinate( key )
        if coord:
            mchain = acm.FMethodChain( property )
            idPart = mchain.Call( [coord] )
            if idPart != 'None':
                if externalId:
                    externalId += ' - '
                externalId += idPart
    return externalId

def RiskFactorDeltaParameters( description, shiftConfig, referenceDate, noOfSteps, scaleFactor ):
    params = description.ShiftParameters( shiftConfig, referenceDate )
    shift = description.ValueScaleFactor() * noOfSteps * scaleFactor
    diffType = shiftConfig.ParamDict()[acm.FSymbol('DifferenceType')]
    params[0] = 1.0 + (diffType == 'Relative' and shift or 0.0)
    params[1] = (diffType != 'Relative' and shift or 0.0)
    return params

def CreateRiskFactorDeltaParameters( riskFactors, referenceDate, noOfSteps, scaleFactor ):
    parameters = []
    for riskFactor in riskFactors:
        parameters.append( RiskFactorDeltaParameters( riskFactor.RiskFactorDescription(),
            riskFactor.ShiftConfiguration(), referenceDate, noOfSteps, scaleFactor ) )
    return parameters

targetCache = {}

def AlwaysMatchedTarget( riskFactorType ):
    if riskFactorType == irType:
        target = irType.TargetConfiguration('Yield Curve', acm.FObject, None)
        target = irType.TargetConfiguration('BenchmarkInstrument', acm.FObject, target)
        return target
    return acm.FObject
    
def RiskFactorTargetCriteria( target ):
    if target.IsKindOf( acm.FInstrument ):
        return target
    if target.IsKindOf( acm.FBenchmark ):
        return target.Instrument()
    if target.IsKindOf( acm.FCollection ):
        return [RiskFactorTargetCriteria(el) for el in target]
    if target.IsKindOf( acm.FCommonObject ):
        global targetCache
        if not targetCache.has_key( target ):
            targetCache[ target ] = acm.Filter().SimpleAndQuery(acm.FCommonObject, ["LiveEntity"], [], [target])
        return targetCache[ target ]
    return target

def TransformTarget(targetObject, coordinateConfigurationTime, riskFactorType):
    target = targetObject
    coordinateConfiguration = coordinateConfigurationTime
    if targetObject.IsKindOf('FYCAttribute'):
        target = targetObject.Curve()
        coordinateConfiguration = riskFactorType.CoordinateConfiguration('Currency', targetObject.Currency(), coordinateConfiguration)
        coordinateConfiguration = riskFactorType.CoordinateConfiguration('CreditEntity', targetObject.CreditEntity(), coordinateConfiguration)
        coordinateConfiguration = riskFactorType.CoordinateConfiguration('Seniority', targetObject.SeniorityChlItem(), coordinateConfiguration)
        coordinateConfiguration = riskFactorType.CoordinateConfiguration('Restructuring', targetObject.RestructuringType(), coordinateConfiguration)
    return target, coordinateConfiguration

def BucketRiskFactor( targetObject, coordinates, riskFactorType, extId = None, creationScope = None, shiftType = None ):
    shiftConfiguration = configurationsByType[riskFactorType][0]
    valueConfiguration = configurationsByType[riskFactorType][1]
    if shiftType:
        valueConfiguration = riskFactorType.ValueConfiguration('BenchmarkShiftType', shiftType, valueConfiguration)

    valueCoordinateConfiguration = None
    for key in coordinates.keys():
        valueCoordinateConfiguration = riskFactorType.CoordinateConfiguration( key, coordinates[key], valueCoordinateConfiguration )

    target, coordinateConfiguration = TransformTarget(targetObject, valueCoordinateConfiguration, riskFactorType)
    riskFactorDescription = riskFactorType.CreateRiskFactorDescription(coordinateConfiguration, valueConfiguration)
    
    externalId = extId and extId or RiskFactorExternalId( riskFactorDescription, target )
    riskFactor = riskFactorDescription.CreateRiskFactor(target, shiftConfiguration, externalId, creationScope)
    return riskFactor


def FXRiskFactorFromCurrencyPair(cp, creationScope = None):
    return BucketRiskFactor( acm.FObject, {'BaseCurrency':acm.FStaticArray( [cp.Currency1()] ), 'TermCurrency':cp.Currency2()}, fxType, cp.Name(), creationScope )


def InterestRateRiskFactor():
    target = irType.TargetConfiguration('Yield Curve', acm.FObject, None)
    target = irType.TargetConfiguration('BenchmarkInstrument', acm.FObject, target)
    return BucketRiskFactor( target, {'BenchmarkInstrument': acm.FObject}, irType )
