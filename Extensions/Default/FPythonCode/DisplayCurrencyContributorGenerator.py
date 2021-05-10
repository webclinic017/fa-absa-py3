
import acm
from MeasureSpecificationGenerator import MeasureSpecificationComponents


def DefinesColumn():
    return False

def DefinesParameters():
    return True

def DefinesScenarios():
    return False

def DefinesDimensions():
    return False       
       
def CreateMsc( displayId, config ):
    msc = MeasureSpecificationComponents()
    if config:
        msc.m_parameters = [[config, displayId]]
    return msc
    
def Generate( parameters ):
    specs = []
    for curr in parameters["selectedCurrencies"]:
        parameters = acm.FDictionary()
        parameters[acm.FSymbol( "PositionReportCurrency" )] = curr
        config = acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues( parameters, None)
        specs.append( CreateMsc( curr.Name(), config ) )
        
    return specs
