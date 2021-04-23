from PS_UploadPrices import _setInstrumentPrice as set_price
import acm
from at_logging import  getLogger, bp_start

LOGGER = getLogger()



insLst = ['ZAR-USD/CCS/F-F/180906-230808/Internal',
'ZAR-USD/CCS/F-F/180906-230808',
'ZAR-AUD/CCS/JI-F/171016-210907/1.96',
'ZAR-AUD/CCS/JI-F/171016-200908/2.49',
'ZAR-AUD/CCS/JI-F/170307-200908/#1',
'ZAR-AUD/CCS/JI-F/170307-170907/#1',
'ZAR-AUD/CCS/JI-F/170307-170907',
'ZAR-AUD/CCS/JI-F/170306-230306/2.27/#1',
'ZAR-AUD/CCS/JI-F/170306-220307',
'ZAR-AUD/CCS/JI-F/170306-210308/1.51/#1',
'ZAR-AUD/CCS/JI-F/170306-200908/1.83',
'ZAR-AUD/CCS/JI-F/170306-200306/1.52',
'ZAR-AUD/CCS/JI-F/160606-200608',
'ZAR-AUD/CCS/JI-F/150930-200906#1',
'ZAR-AUD/CCS/JI-F/150930-200906',
'ZAR-AUD/CCS/F-F/180831-230906/Internal',
'ZAR-AUD/CCS/F-F/180831-230906',
'ZAR-AUD/CCS/F-F/170619-220620#1',
'ZAR-AUD/CCS/F-F/170619-220620',
'ZAR-AUD/CCS/F-F/160831-200908#1',
'ZAR-AUD/CCS/F-F/160831-200908',
'USD-AUD/CCS/LI-F/200306-230306/2.27',
'USD-AUD/CCS/LI-F/200306-210308/1.96',
'USD-AUD/CCS/LI-F/180905-230906/2.78',
'USD-AUD/CCS/LI-F/180905-230906/2.23',
'USD-AUD/CCS/LI-F/180306-210308/1.51',
'USD-AUD/CCS/LI-F/160617-200306/2.38',
'USD-AUD/CCS/LI-3M/180813-230814/#1',
'USD-AUD/CCS/LI-3M/180813-230814',
'AUD-USD/CCS/F-LI/170907-200908/2.49',
'AUD-USD/CCS/F-LI/170907-200908/2.10',
'AUD-USD/CCS/F-LI/170623-220307/2.75',
'AUD-USD/CCS/F-LI/160914-200306/2.20',
'AUD-USD/CCS/F-LI/151016-200908/2.87']

dict = {'ZAR-USD/CCS/F-F/180906-230808/Internal': 10.3,
'ZAR-USD/CCS/F-F/180906-230808': 10.3,
'ZAR-AUD/CCS/JI-F/171016-210907/1.96': 0.53,
'ZAR-AUD/CCS/JI-F/171016-200908/2.49': 0.51,
'ZAR-AUD/CCS/JI-F/170307-200908/#1': 0.43,
'ZAR-AUD/CCS/JI-F/170307-170907/#1': 0.51,
'ZAR-AUD/CCS/JI-F/170307-170907': 0.43,
'ZAR-AUD/CCS/JI-F/170306-230306/2.27/#1': 0.9,
'ZAR-AUD/CCS/JI-F/170306-220307': 0.9,
'ZAR-AUD/CCS/JI-F/170306-210308/1.51/#1': 0.34,
'ZAR-AUD/CCS/JI-F/170306-200908/1.83': 0.53,
'ZAR-AUD/CCS/JI-F/170306-200306/1.52': 0.34,
'ZAR-AUD/CCS/JI-F/160606-200608': 8.98,
'ZAR-AUD/CCS/JI-F/150930-200906#1': 10.44,
'ZAR-AUD/CCS/JI-F/150930-200906': 10.44,
'ZAR-AUD/CCS/F-F/180831-230906/Internal': 9.51,
'ZAR-AUD/CCS/F-F/180831-230906': 9.51,
'ZAR-AUD/CCS/F-F/170619-220620#1': 10.31,
'ZAR-AUD/CCS/F-F/170619-220620': 10.31,
'ZAR-AUD/CCS/F-F/160831-200908#1': 9.29,
'ZAR-AUD/CCS/F-F/160831-200908': 9.29,
'USD-AUD/CCS/LI-F/200306-230306/2.27': -1.62,
'USD-AUD/CCS/LI-F/200306-210308/1.96': 130.87,
'USD-AUD/CCS/LI-F/180905-230906/2.78': 136.27,
'USD-AUD/CCS/LI-F/180905-230906/2.23': 136.51,
'USD-AUD/CCS/LI-F/180306-210308/1.51': 129.86,
'USD-AUD/CCS/LI-F/160617-200306/2.38': 136.79,
'USD-AUD/CCS/LI-3M/180813-230814/#1': -100.29,
'USD-AUD/CCS/LI-3M/180813-230814': 139.77,
'AUD-USD/CCS/F-LI/170907-200908/2.49': -100.98,
'AUD-USD/CCS/F-LI/170907-200908/2.10': -100.21,
'AUD-USD/CCS/F-LI/170623-220307/2.75': -101.62,
'AUD-USD/CCS/F-LI/160914-200306/2.20': -100.51,
'AUD-USD/CCS/F-LI/151016-200908/2.87': -101.69,}

market = acm.FParty['internal']
date = '30/11/2018'




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
        #LOGGER.info('%s %s price on %s was updated to %s', ins.Name(), market, date, price)
        #logme('%s %s price on %s was updated to %s' % 
        #    (ins.Name(), market, date, price))
    except Exception, err:
        #LOGGER.exception('%s %s price on %s not committed.' , ins.Name(), market, date)
        #logme('%s %s price on %s not committed: %s' % (ins.Name(), market, date, err), 'ERROR')
        pass


for ins in insLst:
    INSTRUMENT = acm.FInstrument[ins]
    
    
    price  = INSTRUMENT.HistoricalPrices()
    rate = dict[ins]


    for p in price:
        curr = p.Currency().Name()
        Day = p.Day()
        clone = p.Clone()
        if curr == 'AUD':
            if Day == '11/30/2018':
                _setPriceFields(INSTRUMENT, clone, p, rate, date, market)
