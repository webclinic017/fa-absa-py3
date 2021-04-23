import acm, ael


def getMentisPrice(ins, date):
    Bondmrkt = 'SPOT_BESA'
    Othermrkt = 'SPOT'
    Internal = 'internal'
    if ins.InsType() in ('Bond', 'IndexLinkedBond'):
        price = ins.UsedPrice(date, 'ZAR', Bondmrkt)
    else:
        price = ins.UsedPrice(date, 'ZAR', Othermrkt)
    
    return price

def getMentisRate(object, date):
    if object.Instrument().InsType() in ('Bond', 'IndexLinkedBond'):
        price = getMentisPrice(object.Instrument(), date)
        instrument = ael.Instrument[object.Instrument().Name()]
        dirty = instrument.dirty_from_yield(instrument.spot_date(), None, None, price).value()
    elif object.Instrument().InsType() in ('Fx Rate'):
        dirty = getMentisPrice(object.Instrument().Underlying(), date)
    else:
        dirty = getMentisPrice(object.Instrument(), date) 
    return dirty

