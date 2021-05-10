
import acm
import SPANCSVParser as parser
import SPANParameterGenerator as generator

def spanParametersProvider(path = None):
    '''Function to provide FSpanParameters object to be used in the validation provider and for the Trading Manager Colunmns.'''
    
    if path is None or len(path) == 0:
        path = acm.GetDefaultValueFromName(acm.GetDefaultContext(), "FObject", "SPAN Directory")
    dataProvider = parser.SpanFileParser(str(path)).parse
    spanParameters = generator.SpanParametersGenerator(dataProvider).getSpanParameters()
    
    return spanParameters


