import acm
import FUxCore


def ael_custom_label( parameters, dictExtra ):
    query =  parameters.At('query')
    if query:
       return '(' + query.StringKey() + ')'
    return None

def ael_custom_dialog_show(shell, params):
    
    initParams = params.At('initialData')
    selectedQuery = initParams.At('query')
    
    query =  acm.UX().Dialogs().SelectStoredASQLQuery(shell, acm.FInstrument, selectedQuery )
    parameters = acm.FDictionary()
    
    if query : 
        parameters.AtPut('query', query)
        return parameters
    else :
        return None
    
def ael_custom_dialog_main( parameters, dictExtra ):
    
    query = parameters.At('query')
    
    return CreateBuckets(parameters, query)
    
class DateFactory( object ):
    def __init__(self, instrument):
        self.m_instrument = instrument
        
    def Create( self, dateAdjuster, startDate, spotDates, dateStartsBucket, monthPeriodMapping ):
        return self.m_instrument.LastIRSensDay( startDate )
        
def CreateBuckets( parameters, query ):
    
    buckets = acm.FArray()
    
    instruments = query.Query().Select()
    
    for ins in instruments : 
        if ins.IsKindOf('FInstrument') : 
            bucketDef = None
            if ins.Generic() :
                bucketDef = acm.FCustomTimeBucketDefinition()
                bucketDef.SetFunction( DateFactory( ins ).Create )

                if ins.IsCashFlowInstrument() : 
                    legs = ins.Legs()
                    endPeriod = legs[0].EndPeriod()
                    startPeriod = legs[0].StartPeriod()
                    name = acm.Time().AddDatePeriods(legs[0].StartPeriod(), endPeriod)
                    if ins.IsKindOf(acm.FFra) :
                        name = endPeriod                    
                    if ins.IsKindOf(acm.FDeposit) : 
                        count = acm.Time.DatePeriodCount(endPeriod)
                        unit = acm.Time.DatePeriodUnit(endPeriod)
                        if count > 0 and count < 7 and unit == 'Days': 
                            name = acm.Time().AddDatePeriods(legs[0].StartPeriod(), endPeriod)
                            spotBankingDaysOffset = ins.SpotBankingDaysOffset()
                            if spotBankingDaysOffset > 0:
                                name = acm.Time().AddDatePeriods(name, str(spotBankingDaysOffset) + ' D')
                    elif ins.IsKindOf(acm.FFxSwap) : 
                        count = acm.Time.DatePeriodCount(endPeriod)
                        unit = acm.Time.DatePeriodUnit(endPeriod)
                        if count < 7 and unit == 'Days': 
                            spotBankingDaysOffset = ins.SpotBankingDaysOffset()
                            if spotBankingDaysOffset > 0:
                                name = acm.Time().AddDatePeriods(name, str(spotBankingDaysOffset) + ' D')
                else:
                    name = ins.ExpiryPeriod()

                bucketDef.Name(acm.Time().DatePeriodToString(name))
                bucketDef.SetSpec( ins.Name() )
            else:
                bucketDef = acm.FFixedDateTimeBucketDefinition()
                bucketDef.DiscardIfExpired( True )
                bucketDef.FixedDate( ins.LastIRSensDay( acm.Time().DateToday() ) )
                
            buckets.Add(bucketDef)
    
    return buckets;
