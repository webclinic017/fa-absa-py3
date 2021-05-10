
import acm

#------------------------------------------------------------------------------
def RiskFactorCurrencyPairs(termCurrency, baseCurrencies):
    riskFactors = []
    
    for curr in baseCurrencies:
        if curr != termCurrency:
            riskFactors.append( {'TermCurrency' : termCurrency, 'BaseCurrency' : curr} )
        
    return riskFactors

#------------------------------------------------------------------------------
def MethodChainFromDimension( dimension ):
    attrs = []
    
    riskFactorType = acm.RiskFactor().RiskFactorType( dimension.RiskFactorCollection().RiskFactorType() )
    
    if not acm.RiskFactor().DimensionIsTargetDimension( dimension ):
        dimDef = riskFactorType.RiskFactorDimensionDefinition( dimension.DimensionId() )
        if dimDef["Method"]:
            attrs.append( str( dimDef["Method"] ) )
    
    attrs.append( dimension.MethodChain() )
    attrs.append( "StringKey" )
    
    return MethodChainFromAttributes( attrs )

#------------------------------------------------------------------------------
def MethodChainFromAttributes( attrs ):
    methodChain = ".".join( attr for attr in attrs if attr )
    return acm.FMethodChain(methodChain)
    
