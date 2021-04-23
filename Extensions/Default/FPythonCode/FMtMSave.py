from __future__ import print_function
"""
    This module is used to save MarkToMarket prices from the Trading Manager.
    Triggered from the columns Mark-To-Market Price and Mark-To-Market Price Yesterday
"""
import acm, ael

def changeMtMPrice(row, col, calcval, val, operation):
    if str(operation) == 'remove':
        return
    ins = row.Instrument()
    today = ael.date_today()
    if col.StringKey() == 'Mark-to-Market Price':
        date = today
    elif col.StringKey() == 'Mark-to-Market Price Yesterday':
        date = today.add_banking_day(ael.Instrument[ins.Name()], -1)
    else:
        return
    mappedPar = acm.GetFunction('mappedGlobalAccountingParameters', 0)()
    accPar = mappedPar.Parameter()
    mtmMarket = accPar.MtmMarket()
    c="insaddr=%d and day='%s' and curr=%d and ptynbr=%d" % \
        (ins.Oid(), date, ins.Currency().Oid(), mtmMarket.Oid())
    aelprice = ael.Price.read(c)
    if aelprice:
        price = aelprice.clone()
        old_price = aelprice.settle
    else:
        price = ael.Price.new()
        old_price = 'None'
    price.settle = val.Number()
    price.insaddr = ins.Oid()
    price.curr = ins.Currency().Oid()
    price.ptynbr = mtmMarket.Oid()
    price.day = date
    price.commit()
    print ('Saved MtM price %d (%s) for %s with date %s (market, "%s")' % \
        (val.Number(), str(old_price), ins.Name(), date, mtmMarket.Name()))
