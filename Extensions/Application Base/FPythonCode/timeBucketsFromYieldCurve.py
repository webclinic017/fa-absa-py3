import acm
import FUxCore


def ael_custom_label(parameters, dictExtra):
    vs =  parameters.At('yield curve')
    if vs:
       return '(' + vs.StringKey() + ')'
    return None

def ael_custom_dialog_show(shell, params):
    
    initParams = params.At('initialData')
    selectedYieldCurve = initParams.At('yield curve')
    
    yieldCurves = acm.FFilteredSet()
    yieldCurves.AddSource(acm.FYieldCurve.Select('type = Spread'))
    yieldCurves.AddSource(acm.FYieldCurve.Select('type = Attribute Spread'))
    yieldCurves = yieldCurves.AsIndexedCollection().SortByProperty('Name')
    
    yieldCurve =  acm.UX().Dialogs().SelectObject(shell, 'Select Yield Curve', 'Yield Curve', yieldCurves, selectedYieldCurve)
    parameters = acm.FDictionary()
    
    if yieldCurve: 
        parameters.AtPut('yield curve', yieldCurve)
        return parameters
    else :
        return None
    
def ael_custom_dialog_main(parameters, dictExtra):
    
    yc = parameters.At('yield curve')
    
    return CreateBuckets(yc)
    
class DateFactory( object ):
    
    def __init__( self, ycPoint ):
        self.m_ycPoint = ycPoint
        
    def Create( self, dateAdjuster, startDate, spotDates, dateStartsBucket, monthPeriodMapping ):
        if self.m_ycPoint:
            return self.m_ycPoint.ActualDate( startDate )
        return None
        
def CreateBuckets(yc):
    buckets = acm.FArray()
    for point in yc.Points():
        bucketDef = acm.FCustomTimeBucketDefinition()

        factory = DateFactory( point )
        bucketDef.SetFunction( factory.Create )

        if point.Instrument():
            bucketDef.Name( point.Name() )
        elif point.Date():
            bucketDef.Name( point.Date() )
        elif point.DatePeriod():
            bucketDef.Name( point.DatePeriod() )
        bucketDef.SetSpec( bucketDef.Name() )
        buckets.Add(bucketDef)
    if buckets.Size():
        return buckets;
    else:
        return None
