
import acm
import FRTBCustomOverrides

def ConfigurationFromSeniority( path ):
    config = None
    if len(path) > 0:
        config = acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(
            { acm.FSymbol('FRTBDRCSeniority') : [path[0]] }, None )
            
    return config

def ConfigurationFromIssuer( path ):
    config = None
    if len(path) > 0:
        config = acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(
            { acm.FSymbol('FRTBDRCIssuer') : path[0] }, None )
    return config

def LossGivenDefault( path ):
    base = FRTBCustomOverrides.Custom_LossGivenDefault( path[1], path[2], path[3], str(path[0]) )
    if base is None:
        base = 1.0
    return [base - 0.01, base]

def RecoveryRates( path ):
    return [ 1 - lgd for lgd in LossGivenDefault(path) ]

ael_variables = []

def ael_main_ex(parameters, unused):
    dims = []
    context = acm.ExtensionTools().GetDefaultContext()

    shiftData = acm.FVectorShiftData()
    dimDef = context.GetExtension(acm.FColumnDimensionDefinition, acm.FObject, 'FRTB IMA DRC Seniorities').Value()
    dim = acm.Risk().CreateVectorDimension( "Seniority", dimDef, shiftData, None, None, None )
    dims.append( dim )
    
    shiftData = acm.FVectorShiftData()
    dimDef = context.GetExtension(acm.FColumnDimensionDefinition, acm.FObject, 'FRTB DRC Issuers').Value()
    dim = acm.Risk().CreateVectorDimension( "Issuer", dimDef, shiftData, None, ConfigurationFromSeniority, ["Seniority", "Issuer"] )
    dims.append( dim )

    shiftData = acm.FVectorShiftData()
    dimDef = context.GetExtension(acm.FColumnDimensionDefinition, acm.FObject, 'FRTB DRC Issuer Types').Value()
    dim = acm.Risk().CreateVectorDimension( "IssuerType", dimDef, shiftData, None, ConfigurationFromIssuer, ["Issuer", "IssuerType"] )
    dims.append( dim )

    shiftData = acm.FVectorShiftData()
    dimDef = context.GetExtension(acm.FColumnDimensionDefinition, acm.FObject, 'FRTB DRC Credit Quality').Value()
    dim = acm.Risk().CreateVectorDimension( "CreditQuality", dimDef, shiftData, None, ConfigurationFromIssuer, ["Issuer", "CreditQuality"] )
    dims.append( dim )

    shiftData = acm.FDynamicVectorShiftData()
    shiftData.SetFunctions( RecoveryRates, LossGivenDefault )
    dimDef = context.GetExtension(acm.FColumnDimensionDefinition, acm.FObject, 'FRTB DRC Loss Given Default').Value()
    dim = acm.Risk().CreateVectorDimension( "LossGivenDefault", dimDef, shiftData, None, ConfigurationFromIssuer, ["Seniority", "Issuer", "IssuerType", "CreditQuality"] )
    dims.append( dim )

    return dims

def ael_dimension_ids( parameters, unused ):
    dimIds = [acm.FSymbol( "Seniority" ), acm.FSymbol( "Issuer" ), acm.FSymbol( "IssuerType" ), acm.FSymbol( "CreditQuality" ), acm.FSymbol( "LossGivenDefault" )]
    return dimIds
