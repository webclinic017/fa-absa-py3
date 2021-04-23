import acm
import FUxCore


def ael_custom_label(parameters, dictExtra):
    vs =  parameters.At('inflation curve')
    if vs:
       return '(' + vs.StringKey() + ')'
    return None

def ael_custom_dialog_show(shell, params):
    
    initParams = params.At('initialData')
    selectedYieldCurve = initParams.At('inflation curve')
    
    yieldCurves = acm.FFilteredSet()
    yieldCurves.AddSource(acm.FYieldCurve.Select('type = Inflation'))
    yieldCurves = yieldCurves.AsIndexedCollection().SortByProperty('Name')
    
    yieldCurve =  acm.UX().Dialogs().SelectObject(shell, 'Select Inflation Curve', 'Inflation Curve', yieldCurves, selectedYieldCurve)
    parameters = acm.FDictionary()
    
    if yieldCurve: 
        parameters.AtPut('inflation curve', yieldCurve)
        return parameters
    else :
        return None
    
def ael_custom_dialog_main(parameters, dictExtra):
    
    yc = parameters.At('inflation curve')
    
    return CreateBuckets(yc)
    
class DateFactory(object):
    def __init__( self, yc, ycPoint ):
        self.m_yc = yc
        self.m_ycPoint = ycPoint
        
    def Create( self, dateAdjuster, startDate, spotDates, dateStartsBucket, monthPeriodMapping ):
        date = None
        curveStartDate = self.m_yc.CurveCPIDate( startDate )

        if self.m_ycPoint.Instrument():
            date = self.m_ycPoint.Instrument().LastCPISensDay( startDate )
        elif self.m_ycPoint.Date():
            date = self.m_ycPoint.ActualDate()
        else:
            date = self.m_ycPoint.ActualDate( startDate )
            period = self.m_ycPoint.DatePeriod()
        if date > curveStartDate:
            return date
        return None
            
def CreateBuckets(yc):
    buckets = acm.FArray()
    
    for point in yc.Points() :
        spec = ''
        if(point.Instrument()):
            spec = point.Name()
        elif(point.Date()):
            spec = str(point.ActualDate())
        else:
            spec = acm.Time().DatePeriodToString( point.DatePeriod() )

        factory = DateFactory( yc, point )
            
        bucketDef = acm.FCustomTimeBucketDefinition()
        bucketDef.SetFunction( factory.Create )
        bucketDef.SetSpec( spec )
        bucketDef.Name( spec )
        buckets.Add(bucketDef)
    if buckets.Size():
        return buckets;
    else:
        return None
