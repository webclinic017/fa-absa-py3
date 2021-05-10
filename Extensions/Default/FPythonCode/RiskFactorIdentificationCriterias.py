
import acm

#------------------------------------------------------------------------------
# Published
#------------------------------------------------------------------------------
def ParameterCriteriaFromRiskFactorCollection( riskFactorCollection ):
    riskFactorType = acm.RiskFactor().RiskFactorType( riskFactorCollection.RiskFactorType() )
    targetDimensionData = riskFactorType.TargetDimensionData()

    targetConfig = None
    for dimensionId in targetDimensionData:
        targetDomain = targetDimensionData[dimensionId][acm.FSymbol('Domain')]
        
        criteria = AdditionalConstraint( riskFactorType, dimensionId )
        
        if not criteria:
            criteria = targetDomain
        
        targetConfig = riskFactorType.TargetConfiguration( dimensionId, criteria, targetConfig )
        
    return targetConfig

#------------------------------------------------------------------------------
# Published
#------------------------------------------------------------------------------
def AdditionalConstraintCriteria( riskFactorCollection ):
    additionalConstraintByMethod = acm.FDictionary()
    
    for dimension in riskFactorCollection.RiskFactorDimensions():
        dimensionDefinition = RiskFactorDimensionDefinition( dimension )
        
        if dimensionDefinition:
            method = dimensionDefinition[acm.FSymbol('Method')]

            additionalConstraintFilter = AdditionalConstraintFromDimensionDefinition( dimensionDefinition )
            
            if additionalConstraintFilter:
                additionalConstraintByMethod[method] = additionalConstraintFilter
    
    if additionalConstraintByMethod.Size() > 0:
        return acm.FAttributeCriteria( additionalConstraintByMethod )
    return None

#------------------------------------------------------------------------------
def AdditionalConstraint( riskFactorType, dimensionId ):
    definition = riskFactorType.RiskFactorDimensionDefinition( dimensionId )
    
    if not definition:
        definition = acm.ExtensionTools().GetDefaultContext().GetExtension( acm.FRiskFactorParameterType, acm.FObject, dimensionId ).Value()
        
    return AdditionalConstraintFromDimensionDefinition( definition )
    
#------------------------------------------------------------------------------
def AdditionalConstraintFromDimensionDefinition( dimensionDefinition ):
    additionalConstraint = dimensionDefinition[acm.FSymbol('AdditionalConstraint')]
    additionalConstraintFunc = acm.GetFunction( additionalConstraint, 1 )
    
    if additionalConstraintFunc:
        return additionalConstraintFunc.CreateCall( [None] )
    else:
        return None

#------------------------------------------------------------------------------
def RiskFactorDimensionDefinition( dimension ):
    riskFactorType = acm.RiskFactor().RiskFactorType( dimension.RiskFactorCollection().RiskFactorType() )
    
    return riskFactorType.RiskFactorDimensionDefinition( dimension.DimensionId() )
