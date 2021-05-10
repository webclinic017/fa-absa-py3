import acm
import deltaDynamicInstruments


def get_time_buckets(dateVector):
    timeBuckets = []
    for i in range(0, len(dateVector)):
        dateTriple = [0, 0, 0]
        #start day
        if i == 0:
            dateTriple[0] = '1970-01-01' #small date
        else:
            dateTriple[0] = timeBuckets[i-1][1]
        #end day
        dateTriple[1] = dateVector[i]
        #next end day for shift
        if i == len(dateVector) - 1:
            dateTriple[2] = '9999-12-31' #big date
        else:
            dateTriple[2] = dateVector[i+1]
        timeBuckets.append(dateTriple)
    return timeBuckets
    
    
def ael_custom_label(parameters, dictExtra):
    return deltaDynamicInstruments.ael_custom_label(parameters, dictExtra)

def ael_custom_dialog_show(shell, params):
    return deltaDynamicInstruments.ael_custom_dialog_show(shell, params)

def ael_custom_dialog_main(parameters, dictExtra):
    #old version used different parameterization
    #need to be supported for upgrading customers
    hedgeIns = parameters.At('Hedge Instruments')
    if not hedgeIns:
        asqlQuery = parameters.At('asqlQuery')
        hedgeIns = deltaDynamicInstruments.createInstruments(asqlQuery)
    resultVector = [] 
    dateVector = []
    
    for ins in hedgeIns:
        dateVector.append(ins.LastIRSensDay())
            
    timeBuckets = get_time_buckets(dateVector)
    
    for i in range(0, len(hedgeIns)):
        params = acm.FNamedParameters()
        params.Name(hedgeIns[i].Name())
        params.UniqueTag(hedgeIns[i].Oid())
        params.AddParameter('instrument', hedgeIns[i])
        params.AddParameter('start date', timeBuckets[i][0])
        params.AddParameter('end date', timeBuckets[i][1])
        params.AddParameter('next date', timeBuckets[i][2])
        resultVector.append(params)
   
    return resultVector
