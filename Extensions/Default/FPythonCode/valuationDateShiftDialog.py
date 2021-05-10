
import acm
import FUxUtils

timeBucketsKey = 'timeBuckets'

def ael_custom_dialog_show( shell, params ):
    result = acm.UX().Dialogs().SelectTimeBuckets(shell)
    if result:
        timeBuckets = result.TimeBuckets()
        if timeBuckets:
            parameters = {timeBucketsKey : timeBuckets}
            return parameters
        return None
    
def ael_custom_dialog_main( parameters, dictExtra ):
    if parameters:
        timeBuckets = parameters[timeBucketsKey]
        shiftVector = acm.CreateReplaceShiftVector('Valuation Date', None)
        
        for timeBucket in timeBuckets:
            if not timeBucket.IsRest():
                # datetimes are returned as strings in Python -> use typed array
                vector = acm.FTypedArray(acm.FDateTime)
                dateTime = acm.Time().FromDate(timeBucket.EndDate())
                vector.Add(dateTime)
                shiftVector.AddReplaceShiftItem(vector, timeBucket.Name())
        return shiftVector
