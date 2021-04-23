"""-----------------------------------------------------------------------------
MODULE	  XTPMessageAdaptations

Version: 1.1

DESCRIPTION

This module contain scripts to adapt trade messages booked from XTP where necessary.
It is hooked in the amba.ini file on the Front Arena Server.
Changes to this AEL will only take effect if the AMBA Server Services are restarted.

History:
Date	    	    Who     	    	    	    	    What
2013-09-18          Anwar Banoo                     Created
ENDDESCRIPTION

-----------------------------------------------------------------------------"""

import ael, string, acm, sys, os


def map_XTP_portfolio(m):
    o1 = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    val = o1.mbf_get_value().strip()
    if val in ('INSERT_TRADE', 'UPDATE_TRADE'):
        trd = m.mbf_find_object('TRADE', 'MBFE_BEGINNING')
        prf = trd.mbf_find_object('COUNTERPARTY_PORTFOLIO.ASSINF', 'MBFE_BEGINNING')
        if prf:
            prfVal = prf.mbf_get_value().strip()
            actualPrf = acm.FPhysicalPortfolio.Select01('assignInfo=%s' % prfVal, 'Book with assinfo "%s" not found' % prfVal)
            if actualPrf:
                trd.mbf_remove_object()
                trd.mbf_add_string('COUNTERPARTY_PORTFOLIO.PRFID', actualPrf.Name())
    return m

print "XTPMessageAdaptations Hook loaded...."
TESTMESSAGES = True
for item in ael.ServerData.select():
    if item.customer_name == 'Production':
        TESTMESSAGES = False
print 'Run using test message =', TESTMESSAGES
