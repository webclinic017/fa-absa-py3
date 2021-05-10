import at_time
from math import log
import warnings

def calc_carry_cost(dateN, dateF, priceN, priceF):
    """ carry cost calculation,

    Keyword arguments:
    dateN -- the date now
    dateF -- the future date
    priceN -- price now
    priceF -- future price
    """

    dN=at_time.to_datetime(dateN)
    dF=at_time.to_datetime(dateF)
    t=(dF-dN).days
    if t < 0:
        warnings.warn("Date Warning... future date used is before date now.")
    t=t/365.0
    yeild=0
    if t>0 and priceN>0 and priceF>0:
        yeild=log(priceF/priceN)/t
        
    return yeild
