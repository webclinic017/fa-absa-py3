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
    
class DateFactory( object ):
    def __init__(self, volatilityStructure, point, skew ):
        self.m_point = point
        self.m_skew = skew
        self.m_vs = volatilityStructure
        
    def Create( self, dateAdjuster, startDate, spotDates, dateStartsBucket, monthPeriodMapping ):
        if self.m_point:
            if self.m_point.IsGenericExpiry():
                period = self.m_point.ActualExpiryPeriod()
                return DateFromGenericPeriod(self.m_vs, startDate, period)
            else:
                return self.m_point.ActualExpiryDay()
        if self.m_skew:
            if self.m_skew.IsGenericExpiry():
                period = self.m_skew.ExpiryPeriod()
                return DateFromGenericPeriod(self.m_vs, startDate, period)
            else:
                return self.m_skew.ActualExpiryDay()
        return None
            
def CreateBuckets( parameters, vs ):
                
    buckets = acm.FArray()
    
    for p in vs.Points() :
        bucketDef = acm.FCustomTimeBucketDefinition()
        bucketDef.SetFunction( DateFactory( vs, p, None ).Create )
        
        spec = None
        if p.IsGenericExpiry():
            period = p.ActualExpiryPeriod()
            spec = acm.Time().DatePeriodToString(period)
        else:
            spec = p.ActualExpiryDay()
        
        bucketDef.SetSpec( spec )
        bucketDef.Name( spec )
        buckets.Add( bucketDef )
    
    for s in vs.Skews() :
        bucketDef = acm.FCustomTimeBucketDefinition()
        bucketDef.SetFunction( DateFactory( vs, None, s ).Create )
        
        spec = None
        if s.IsGenericExpiry():
            period = s.ExpiryPeriod()
            spec = acm.Time().DatePeriodToString(period)
        else:
            spec = s.ActualExpiryDay()
            
        bucketDef.SetSpec( spec )
        bucketDef.Name( spec )
        buckets.Add( bucketDef )
    
    if buckets.Size() :
        return buckets;
    else :
        return None

def DateFromGenericPeriod( vs, startDate, period ):
    date = startDate
    if vs.InstrumentPair():
        date = vs.InstrumentPair().ExpiryDate( date, period )
    else:
        date = acm.Time().PeriodSymbolToRebasedDate( period, startDate )
        
    return date
