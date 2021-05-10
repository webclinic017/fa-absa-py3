
import acm
from MeasureSpecificationGenerator import MeasureSpecificationComponents

measureMap  = { "Delta" : ["Delta"],
                "Vega" : ["Vega"],
                "Curvature" : ["Curvature Up", "Curvature Down"] }

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
    for riskClass in parameters["riskClasses"]:
        for measure in parameters["measures"]:
            for measureType in measureMap[ measure ]:
                id = name + " - " + riskClass 
                id += " " + measureType
                params = acm.FDictionary()
                params[acm.FSymbol('riskClass')] = riskClass
                params[acm.FSymbol('measureType')] = measureType
                params[acm.FSymbol('rfsetup')] = parameters["rfSetup"].Name()
                params[acm.FSymbol('hierarchy')] = parameters["hierarchy"].Name()

                vConfig = acm.Risk().CreateDynamicVectorConfiguration(
                    acm.ExtensionTools().GetDefaultContext().Name(),
                    'FRTB Dynamic Dimensions',
                    params
                )
                calcConfig = acm.Sheet().Column().ConfigurationFromVectorConfiguration( vConfig, None )
                specs.append( CreateMsc( 'FRTB Measure', id, calcConfig ) )
    
    if "DRC" in parameters["additionals"]:
        params = acm.FDictionary()
        params[acm.FSymbol('hierarchy')] = parameters["hierarchy"].Name()
        vConfig = acm.Risk().CreateDynamicVectorConfiguration(
            acm.ExtensionTools().GetDefaultContext().Name(),
            'FRTB DRC Dimensions',
            params
        )
        calcConfig = acm.Sheet().Column().ConfigurationFromVectorConfiguration( vConfig, None )
        specs.append( CreateMsc( "FRTB DRC Gross Jump To Default",  name + " - Gross JTD", calcConfig ) )

    if "RRAO" in parameters["additionals"]:
        dimData = {}
        dimData["externalId"] = "Residual Risk Type"
        dimData["dimDefName"] = "FRTB Residual Risk Types"
        params = acm.FDictionary()
        params["dimensions"] = acm.FArray()
        params["dimensions"].Add( dimData )

        vConfig = acm.Risk().CreateDynamicVectorConfiguration(
            acm.ExtensionTools().GetDefaultContext().Name(),
            'VectorConfiguration',
            params
        )
        calcConfig = acm.Sheet().Column().ConfigurationFromVectorConfiguration( vConfig, None )
        specs.append( CreateMsc( "FRTB Residual Risk Notional Per Type", name + " - RRAO Notional", calcConfig ) )
        
    return specs
