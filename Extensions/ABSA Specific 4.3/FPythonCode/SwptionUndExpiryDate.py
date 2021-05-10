#This is meant to get the expiry date of the underlying of a Swaption.
def getUndelyingExpiryDate(object):
    if object.Trade():
        expiryDate = None
        ins = object.Trade().Instrument()
        if ins.InsType() == 'Option' and ins.Underlying().InsType() == 'Swap':
            expiryDate = ins.Underlying().ExpiryDate()
        
        return expiryDate
