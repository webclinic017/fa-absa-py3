import at_time
from math import log
import warnings

def compoadjcarry(dateN, dateF, fxSpot, fxFwd, domCarryCost):
    """ compo adjusted carry cost calculation.

    Keyword arguments:
    dateN -- the date now
    dateF -- the future date
    fxSpot -- the spot fx rate
    fxFwd -- the forward fx rate
    domCarryCost -- the domestic carry cost
    """

    dN=at_time.to_datetime(dateN)
    dF=at_time.to_datetime(dateF)
    t=(dF-dN).days
    if t < 0:
        warnings.warn("Date Warning... future date used is before date now.")
    t=t/365.0
    yeild=0
    if t>0 and fxFwd >0 and fxSpot >0:
        yeild=log(fxFwd/fxSpot)/t

    return domCarryCost+yeild
