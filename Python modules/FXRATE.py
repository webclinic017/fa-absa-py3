import acm, math

_rates_cache = {}

class StandardCalcSpace( object ):
    CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def FXRate(i, date, toCurr, *rest):    
    curr1 = acm.FCurrency[i.insid]
    curr2 = acm.FCurrency[ toCurr ]
    baseCurr = acm.FCurrency[ 'USD' ]
    if curr1.Name() != baseCurr.Name():
        try:
            fxRateCurr1 = curr1.Calculation().FXRate( StandardCalcSpace.CALC_SPACE,baseCurr,date ).Number()
        except:
            fxRateCurr1 = 0.0
    else:
        fxRateCurr1 = 1
    if curr2.Name() != baseCurr.Name():
        try:
            fxRateCurr2 = baseCurr.Calculation().FXRate( StandardCalcSpace.CALC_SPACE,curr2,date ).Number()
        except:
            fxRateCurr2 = 0.0
    else:
        fxRateCurr2 = 1
    return fxRateCurr2 * fxRateCurr1

def latest_available_rate(curr_from, curr_to, days_back = 10):
    """Return latest available curr_from/curr_to spot rate."""
    try:
        return live_rate(curr_from, curr_to)
    except ValueError, e:
        pass
    
    date = acm.Time.DateToday()
    for x in range(days_back):
        try:
            return rate(curr_from, curr_to, date=date)
        except ValueError, e:
            pass
        date = acm.Time.DateAddDelta(date, 0, 0, -1)
    
    raise ValueError('Unable to find latest SPOT rate for {0}/{1}'.format(curr_from, curr_to))

def forward_rate(curr_from, curr_to, date):
    """Return forward FX rate."""
    cs = StandardCalcSpace.CALC_SPACE
    c1 = acm.FCurrency[curr_from]
    c2 = acm.FCurrency[curr_to]
    rate = c1.Calculation().FXRate(cs, c2, date).Value().Number()
    if math.isnan(rate) or math.isinf(rate): raise ValueError('Rate is NaN or inf')
    rate = round_rate(curr_from, curr_to, rate)
    
    return rate

def live_rate(curr_from, curr_to):
    """Return live curr_from/curr_to FX spot rate."""
    return _liveusdrate(curr_to) / _liveusdrate(curr_from)

def rate(curr_from, curr_to, market='SPOT', date=None):
    """Return curr_from/curr_to FX rate."""
    date = date or acm.Time.DateToday()
    rate_from = _rates_cache.setdefault((market, date, curr_from), _usdrate(curr_from, market, date))
    rate_to = _rates_cache.setdefault((market, date, curr_to), _usdrate(curr_to, market, date))
    
    return rate_to / rate_from

def round_rate(curr_from, curr_to, rate):
    """Rounds FX rate based on currency pair conventions."""
    pval = 0
        
    cp = acm.FCurrencyPair[curr_from + '/' + curr_to]
    if cp: pval = cp.PointValue()
    else:
        cp = acm.FCurrencyPair[curr_to + '/' + curr_from]
        if cp: pval = cp.PointValueInverse()
    if pval:
        rate = round(rate / pval, 2) * pval
    return rate

def _liveusdrate(curr_to):
    """Return live USD/curr_to FX rate."""
    if curr_to == 'USD': return 1.0
    
    query = "instrument='{0}' AND currency='{1}' and market='SPOT_RT'"
    prices = acm.FPrice.Select(query.format('USD', curr_to))
    if prices:
        return prices[0].Settle()
    prices = acm.FPrice.Select(query.format(curr_to, 'USD'))
    if prices:
        return 1 / prices[0].Settle()
    
    raise ValueError('Unable to find live SPOT rate for USD/{0}'.format(curr_to))        

def _usdrate(curr_to, market, date):
    """Return USD/curr_to FX rate."""
    if curr_to == 'USD': return 1.0
    
    query = "instrument='{0}' AND currency='{1}' and market='{2}' AND day='{3}'"
    prices = acm.FPrice.Select(query.format('USD', curr_to, market, date))
    if prices:
        return prices[0].Settle()
    prices = acm.FPrice.Select(query.format(curr_to, 'USD', market, date))
    if prices:
        return 1 / prices[0].Settle()
    
    raise ValueError('Unable to find rate for USD/{0} ({1} @{2})'.format(curr_to, market, date))
