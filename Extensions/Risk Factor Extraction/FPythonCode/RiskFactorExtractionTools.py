
import acm

def CreateRiskFactorDescription( instance, riskFactorCreatorCache, valuationDate ):
    externalId = acm.FSymbol(acm.RiskFactor.RiskFactorExternalId(instance))
    riskFactor = acm.RiskFactor.RiskFactorFromRiskFactorInstance(instance, externalId, riskFactorCreatorCache, valuationDate)
    return riskFactor.RiskFactorDescription()

_s_historicalItemFunctions = {
    acm.FYieldCurve : acm.GetFunction( "shiftYieldCurveDate", 2 ),
    acm.FVolatilityStructure : acm.GetFunction( "shiftVolatilityStructureDate", 2 )
}
def GetHistorical( parameter, date ):
    for baseClass in list(_s_historicalItemFunctions.keys()):
        if parameter.IsKindOf(baseClass):
            return _s_historicalItemFunctions[ baseClass ]( parameter, date )
    return parameter
        
def __BenchmarkInstrument( riskFactorInstance ):
    benchmarkInstrument = None
    for dimension in riskFactorInstance.RiskFactorCollection().RiskFactorDimensions():
        if dimension.DimensionId() == "BenchmarkInstrument":
            benchmarkInstrument = acm.FInstrument[ riskFactorInstance.CoordinateValue( dimension ) ]
        else:
            #TODO::JANKAR01 fix for YC + Time Combo (historical curve?)
            pass
    return benchmarkInstrument
    
def RiskFactorTargetParameter( riskFactorInstance, historicalMode, valuationDate, valuationSystemDate ):
    riskFactorType = riskFactorInstance.RiskFactorCollection().RiskFactorType()
    
    parameter = None
    if riskFactorType == "FX":
        baseCurrency = None
        termCurrency = None
        for dimension in riskFactorInstance.RiskFactorCollection().RiskFactorDimensions():
            if dimension.DimensionId() == "BaseCurrency":
                baseCurrency = acm.FCurrency[ riskFactorInstance.CoordinateValue( dimension ) ]
            elif dimension.DimensionId() == "TermCurrency":
                termCurrency = acm.FCurrency[ riskFactorInstance.CoordinateValue( dimension ) ]
        parameter = acm.FX.CreateFxRate( baseCurrency, termCurrency )
    elif riskFactorType == "Benchmark Price":
        parameter = __BenchmarkInstrument( riskFactorInstance )
    else:
        isHistorical = historicalMode or (valuationDate < valuationSystemDate)
        
        for targetDimensionId in acm.RiskFactor.RiskFactorType( riskFactorType ).TargetDimensionData():
            query = acm.RiskFactor().TargetParameterQuery( riskFactorInstance, targetDimensionId )
            if query:
                parameter = query.Select()
                break
        if isHistorical:
            parameter = [GetHistorical( param, valuationDate ) for param in parameter]
    return parameter
