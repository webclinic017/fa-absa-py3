import acm
import FUxCore


def ael_custom_label( parameters, dictExtra ):
    vs =  parameters.At('volatility structure')
    if vs:
       return '(' + vs.StringKey() + ')'
    return None

def ael_custom_dialog_show(shell, params):
    
    initParams = params.At('initialData')
    selectedStructure = initParams.At('volatility structure')
    structures = acm.FVolatilityStructure.Select('').SortByProperty('Name')
    
    structure =  acm.UX().Dialogs().SelectObject(shell, 'Select Volatility Structure', 'Volatility Structures', structures, selectedStructure)
    parameters = acm.FDictionary()
    
    if structure: 
        parameters.AtPut('volatility structure', structure)
        return parameters
    else :
        return None
    
def ael_custom_dialog_main( parameters, dictExtra ):
    
    vs = parameters.At('volatility structure')
    
    return CreateBuckets(parameters, vs)
    
def CreateBuckets( parameters, vs ):
                
    buckets = acm.FArray()
    
    for p in vs.Points() :
        bucketDef = None
        if p.IsGenericUnderlyingMaturity():
            period = p.ActualUnderlyingMaturityPeriod()
            bucketDef = acm.FDatePeriodTimeBucketDefinition()
            bucketDef.DatePeriod( period )
        else:
            date = p.ActualUnderlyingMaturityDay()
            bucketDef = acm.FFixedDateTimeBucketDefinition()
            bucketDef.FixedDate( date )
        buckets.Add( bucketDef )
    
    for s in vs.Skews() :
        bucketDef = None
        if s.IsGenericUnderlyingMaturity():
            period = s.ActualUnderlyingMaturityPeriod()
            bucketDef = acm.FDatePeriodTimeBucketDefinition()
            bucketDef.DatePeriod( period )
        else:
            date = s.ActualUnderlyingMaturityDay()
            bucketDef = acm.FFixedDateTimeBucketDefinition()
            bucketDef.FixedDate( date )
        buckets.Add( bucketDef )
    
    if buckets.Size() :
        return buckets;
    else :
        return None
