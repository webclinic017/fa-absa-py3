
import acm
from MeasureSpecificationGenerator import MeasureSpecificationComponents

def DefinesColumn():
    return True

def DefinesParameters():
    return False

def DefinesScenarios():
    return False

def DefinesDimensions():
    return True

def CreateMsc( columnId, displayId, config ):
    msc = MeasureSpecificationComponents()
    msc.m_columnId = columnId
    msc.m_columnName = displayId
    if config:
        msc.m_parameters = [config]
    return msc
    
def Generate( parameters ):
    specs = []
    name = parameters["columnName"]
    setup = parameters["rfSetup"]
    shiftType = parameters["shiftType"]
    shiftSize = parameters["shiftSize"]
    shiftUnit = parameters["shiftUnit"]
    scaleFactor = parameters["scaleFactor"]
    riskFactorType = parameters["riskFactorType"]
    dimensions = parameters["dimensions"]
    

    params = acm.FDictionary()
    params[acm.FSymbol('rfsetup')] = setup.Name()
    params[acm.FSymbol('shiftType')] = shiftType
    params[acm.FSymbol('shiftSize')] = shiftSize
    params[acm.FSymbol('riskFactorType')] = riskFactorType
    params[acm.FSymbol('dimensions')] = dimensions
    params[acm.FSymbol('shiftUnit')] = shiftUnit
    params[acm.FSymbol('scaleFactor')] = scaleFactor
    vConfig = acm.Risk().CreateDynamicVectorConfiguration(
        acm.ExtensionTools().GetDefaultContext().Name(),
        'Risk Factor Dimensions',
        params
    )
    
    rfColls = []
    for c in setup.RiskFactorCollections():
        if c.RiskFactorType() == riskFactorType:
            rfColls.append( c )
    calcConfig = acm.Sheet().Column().ConfigurationFromVectorConfiguration( vConfig, None )
    calcConfig = acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(
            { acm.FSymbol('RiskFactorCollections') : rfColls }, calcConfig )

    specs.append( CreateMsc( 'Risk Factor Delta', name, calcConfig ) )
    return specs
    
