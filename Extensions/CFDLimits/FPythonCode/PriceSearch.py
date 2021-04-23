"""-----------------------------------------------------------------------
MODULE
    PriceSearch

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Returns the price of an instrument for a specific market and date.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Marco Cerutti
    CR Number           : 455227

ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm

def returnPrice(ins, market, date):
    try:
        date=acm.Time().DateAdjustPeriod(date, '-1d')
        return acm.FPrice.Select01("instrument = %s and market = '%s' and day = %s" % (ins.Oid(), market, date ), 'NaN').Settle()
    except:
        return 0
