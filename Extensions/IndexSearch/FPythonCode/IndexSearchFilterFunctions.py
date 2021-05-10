import acm

def FilterInstrument(instrument):
    try :
        filter = not instrument.IsExpired()
    except:
        filter = True

    return filter
