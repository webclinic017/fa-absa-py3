
import acm

def getAdsInstance( instrumentArguments ):
    instrumentKey = instrumentArguments[0]
    ins = None
    try:
        ins = acm.FInstrument.Select01('externalId2=%s' %instrumentArguments[0], 'err')
        instrumentKey = ins.Oid() 
    except:
        print ('No match found for instrument descriptor %s.' % instrumentKey)

    return instrumentKey
