'''-----------------------------------------------------------------------
MODULE
  EQ_Barrier_Theor

DESCRIPTION
  This module is called by the EQ_Barrier_Price ASQL to calculate the Theor value from trading manager.

History:
Date            Who                     What
2009-07-28	Herman Hoon             Created

ENDDESCRIPTION
-----------------------------------------------------------------------'''

import acm

def theor(temp,trd,curr,*rest):
    t = acm.FTrade[trd.trdnbr]
    ins = t.Instrument()
    tag = acm.CreateEBTag()
    return acm.GetCalculatedValueFromString(ins, 'Standard', 'object:*"theor"[showCurr = "%s",useDatabasePrice = portPriceSource]' %(curr), tag).Value()
