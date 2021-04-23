
import ael

def instrument_dirty_from_yield(insid):
    """
    Used in columns:
    Interest Rate Yield Delta Hedge Equivalent ABSA
    Interest Rate Yield Delta ABSA
    Repliactes functionality in asql query DW_Bond_Delta_New
    """
    
    i = ael.Instrument[insid]
    date = ael.date_today()
    price = i.mtm_price(date)
    value1 = i.dirty_from_yield(date, None, None, price - 0.5)
    value2 = i.dirty_from_yield(date, None, None, price + 0.5)
    return - (value1 - value2) / (0.5 + 0.5)/10000
    
