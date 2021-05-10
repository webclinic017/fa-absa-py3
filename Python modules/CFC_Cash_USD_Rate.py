'''----------------------------------------------------------------------------------------
    CFC_Cash_USD_Rate

    This query calculate extracts all trade cash movements across all instrument types.
    The cash is extracted in its original currency.
    The result is used for the Cash Recon.

    Department and Desk : Product Control
    Requester           : Suveshan Iyaloo
    Developer           : Manyano Dlulane

    History:
    When: 	        CR Number:      Who:		        What:       
    2019-06-19      FTF-201         Manyano Dlulane	    Created
--------------------------------------------------------------------------------------------'''

import acm
from at_logging import getLogger

LOGGER = getLogger()

def usd_rate(curr_to, market, date, *rest):
    """Return USD/curr_to FX rate."""
    usd = acm.FInstrument['USD']
    usd_zar = usd.UsedPrice(date, 'ZAR', market)

    currency = acm.FInstrument[curr_to.insid]
    curr_usd = usd.UsedPrice(date, currency, market)

    try:
        fx_rate = usd_zar / curr_usd
    except Exception:
        LOGGER.info("Unable to get USD/%s rate. Rate calculation returned: %s" % (currency.Name(), curr_usd))

    
    if fx_rate:
        return fx_rate

    raise ValueError("Unable to find rate for USD/'%s' ('%s' @{'%s'})" % (currency.Name(), market, date))
