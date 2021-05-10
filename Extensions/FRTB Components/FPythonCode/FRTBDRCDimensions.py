
import acm
import string


def ConfigurationFromSeniority( path ):
    config = None
    if len(path) > 0:
        config = acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(
            { acm.FSymbol('FRTBDRCSeniority') : [acm.FSymbol(item) for item in string.split(str(path[0]), '/')] }, None )
            
    return config

def ConfigurationFromIssuer( path ):
    config = None
    if len(path) > 0:
        config = acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(
            {acm.FSymbol('FRTBDRCIssuer') : path[0]}, None )
    return config

ael_variables = [
    ['hierarchy', 'Hierarchy', 'string', acm.FHierarchy.Select(''), None, 1, 0, '', None]
]

def ael_main_ex(parameters, unused):
    dims = []
    hierarchy = acm.FHierarchy[parameters['hierarchy']]
    context = acm.ExtensionTools().GetDefaultContext()

    hierarchyTree = acm.FHierarchyTree()
    hierarchyTree.Hierarchy( hierarchy )
    root = hierarchyTree.RootNode()
    lgdNode = hierarchyTree.FindChildByName01( "Loss Given Default", root, 3 )

    shiftData = acm.FPathDependentVectorShiftData()
    for child in hierarchyTree.Children( lgdNode ):
        seniority = child.DisplayName()
        lgd = 1.0 - hierarchyTree.DataValueFromColumnName( child, "Loss Given Default" ).DataValueVA()
        shiftData.AddShiftVector( [acm.FSymbol(seniority)], [[[acm.FSymbol(item) for item in string.split(seniority, '/')], lgd]], [seniority] )
        
    dimDef = context.GetExtension(acm.FColumnDimensionDefinition, acm.FObject, 'FRTB SA DRC Seniorities And Recovery Rates').Value()
    dim = acm.Risk().CreateVectorDimension( "Seniority", dimDef, shiftData, None, None, ["Seniority"] )
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

    return dims

def ael_dimension_ids( parameters, unused ):
    dimIds = [acm.FSymbol( "Seniority" ), acm.FSymbol( "Issuer" ), acm.FSymbol( "IssuerType" ), acm.FSymbol( "CreditQuality" )]
    return dimIds
