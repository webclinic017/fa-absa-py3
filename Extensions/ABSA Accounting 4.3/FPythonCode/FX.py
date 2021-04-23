
import ael
    
def func(ins):
    instrument = ael.Instrument[ins]
    price = instrument.used_price(ael.date_today(), 'ECB/EUR-ZAR')
    return  price
