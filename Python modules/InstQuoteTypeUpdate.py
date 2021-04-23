'''
Description
This code changes the user QuoteType.

Date            Who                     What
13/10/2009      Willie van der Bank     Created
'''

import ael, acm

def filters():
    filters = []
    for f in ael.TradeFilter:
        filters.append(f.fltid)
    filters.sort()
    return filters
    
def quote():
    filter = []
    for t in ael.Instrument.select():
        if t.quote_type not in filter:
            filter.append(t.quote_type)
    filter.sort()
    return filter
    
ael_variables = [('tf', 'Trade Filter', 'string', filters(), '', 1),
                 ('qt', 'Qoute Type', 'string', quote(), '', 1)]  
                 
def ael_main(dict):
    quotetype = dict['qt']
    tf = ael.TradeFilter[dict['tf']]
    for t in tf.trades():
        trdnbr = t.trdnbr
        trd = ael.Trade[trdnbr]
        ins = ael.Instrument[trd.insaddr.insaddr]
        insc = ins.clone()
        insc.quote_type = quotetype
        insc.commit()
        ael.poll()
        print 'Inst ' + ins.insid + ' quote_type updated to ' + quotetype

