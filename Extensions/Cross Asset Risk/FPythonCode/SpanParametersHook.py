import acm

def spanParametersProvider(optionalSpanData = None):
    '''Function to provide FSpanParameters object to be used in the validation provider and for the Trading Manager Colunmns.'''
    storedSpanParameters = acm.FStoredSpanParameters['DefaultStoredSpanParameters']
    
    if storedSpanParameters:
        return storedSpanParameters.SpanParameters()
    else:
        acm.Log("spanParametersProvider: Failed to find stored span parameters")
        return acm.FSpanParameters()
