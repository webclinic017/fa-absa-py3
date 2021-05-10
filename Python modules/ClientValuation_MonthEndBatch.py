'''-----------------------------------------------------------------------
MODULE
  ClientValuation_MonthEndBatch

DESCRIPTION
  This module runs though all the client valuation filters and creates the PDF files for the FX options and IRD valuations.

History:
Date            Who                     What
2009-07-26	Herman Hoon             Created

ENDDESCRIPTION
-----------------------------------------------------------------------'''

import ael, Client_Valuations, Fx_Option_Client_Valuations

date = ael.date_today().to_string('%Y-%m-%d')

for tf in ael.TradeFilter.select():
    if tf.fltid[0:13] == "Valuation_IRD":
        dict = {'tf': tf.fltid, 'date': date, 'trdnbr': '0'}
        Client_Valuations.ael_main(dict)
    if tf.fltid[0:13] == "Valuation_OPT":
        dict = {'tf': tf.fltid, 'date': date, 'trdnbr': '0'}
        Fx_Option_Client_Valuations.ael_main(dict)
