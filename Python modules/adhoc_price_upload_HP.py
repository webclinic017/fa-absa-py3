import acm
import FBDPString
from at_logging import  getLogger, bp_start

LOGGER = getLogger()

logme = FBDPString.logme

TODAY = acm.Time.DateToday()

instrument_list = {
    ("ZAR/DAUS/C/13.72/190509/MTM", 636.4168),
    ("ZAR/DAUS/C/13.95/190507/MTM", 406.6216),
    ("ZAR/DAUS/C/14.03/190507/MTM", 333.1478),
    ("ZAR/DAUS/C/14.20/190509/MTM", 214.9972),
    ("ZAR/DAUS/C/14.25/190520/MTM", 251.9399),
    ("ZAR/DAUS/C/15.25/190520/MTM", 19.9337),
    ("ZAR/DAUS/P/14.00/190613/MTM", 108.5912),
    ("ZAR/DAUS/P/14.00/190620/MTM", 122.8237),
    ("ZAR/DAUS/P/14.20/190524/MTM", 127.2763),
    ("ZAR/DAUS/YIELDX/AnyExp/07MAY19/MTM", 14.3467),
    ("ZAR/DAUS/YIELDX/AnyExp/09MAY19/MTM", 14.3514),
    ("ZAR/DAUS/YIELDX/AnyExp/10JUN19/MTM", 14.402),
    ("ZAR/ZAEU/YIELDX/JUN19/MTM", 16.224),
    ("ZAR/ZAGB/YIELDX/JUN19/MTM", 18.8468),
    ("ZAR/ZATR/YIELDX/JUN19/MTM", 2.3452),
    ("ZAR/ZAUS/C/14.50/190916/MTM", 563.9886),
    ("ZAR/ZAUS/C/15.89/190614/MTM", 29.5209),
    ("ZAR/ZAUS/C/16.09/190614/MTM", 20.098),
    ("ZAR/ZAUS/P/13.00/190614/MTM", 6.4415),
    ("ZAR/ZAUS/P/14.20/190614/MTM", 184.7303),
    ("ZAR/ZAUS/YIELDX/JUN19/MTM", 14.4141),
    ("ZAR/ZAUS/YIELDX/MAR20/MTM", 14.9064)
}



def _setPriceFields(ins, p, orig, price, date, market):
    p.Day(date)
    p.Settle(price)
    if market in ('SPOT', 'SPOT_SOB'):
        p.Bid(price)
        p.Ask(price)
        p.Last(price)
    try:
        orig.Apply(p)
        orig.Touch()
        orig.Commit()
        LOGGER.info('%s %s price on %s was updated to %s', ins.Name(), market, date, price)
        logme('%s %s price on %s was updated to %s' % 
            (ins.Name(), market, date, price))
    except Exception, err:
        LOGGER.exception('%s %s price on %s not committed.', ins.Name(), market, date)
        logme('%s %s price on %s not committed: %s' % 
            (ins.Name(), market, date, err), 'ERROR')
            

def _setInstrumentPrice(ins, price, date, market):
    found = False
    if market in ['SPOT', 'SPOT_SOB']:
        for p in ins.Prices():
            update_spot = (market == 'SPOT' and p.Market().Name() == market and
                           date == TODAY and p.Day() <= date)
            update_spot_sob = (market == 'SPOT_SOB' and 
                               p.Market().Name() == market and p.Day() <= date)
            if update_spot or update_spot_sob:
                found = True
                clone = p.Clone()
                _setPriceFields(ins, clone, p, price, date, market)

    for p in ins.HistoricalPrices():
        if p.Market().Name() == market and p.Day() == date:
            found = True
            clone = p.Clone()
            _setPriceFields(ins, clone, p, price, date, market)

    if not found:
        p = acm.FPrice()
        clone = p.Clone()
        clone.Day(date)
        clone.Instrument(ins)
        clone.Market(acm.FParty[market])
        clone.Currency(ins.Currency())
        _setPriceFields(ins, clone, p, price, date, market)
        
    
    
date = "2019-04-30"
for name, price in instrument_list:
    try:
        ins = acm.FInstrument[name]
        _setInstrumentPrice(ins, price, date, 'SPOT')
        _setInstrumentPrice(ins, price, date, 'internal')
    except Exception, err:
        print err
            
print "Completed Successfully"

