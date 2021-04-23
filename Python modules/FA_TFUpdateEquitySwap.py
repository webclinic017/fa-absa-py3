# FA_TFUpdateEquitySwap
# Updates all trade filters that refer to 'EquitySwap' to instead
# refer to 'TotalReturnSwap'
# Todo: Remove or change the filter EQ_IR_Risk_Eddie. It refers to
# portfolio UNKNOWN
#
# 2009-07-15    bs      initial version

import ael
import sys

skip = ['EQ_IR_Risk_Eddie']

def changefilter(filter):
    f = filter.clone()
    q2 = []
    for r in f.get_query():
        if r[4]=='EquitySwap':
            q2.append((r[0], r[1], r[2], r[3], 'TotalReturnSwap', r[5]))
        else:
            q2.append(r)
    f.set_query(q2)
    f.commit()

def hasEquitySwap(filter):
    for r in filter.get_query():
        if r[4]=='EquitySwap':
            return True

def replace_trade_filters():
    fs = [f.fltnbr for f in ael.TradeFilter.select() if hasEquitySwap(f)]
    for fltnbr in fs:
        f = ael.TradeFilter[fltnbr]
        if f.fltid not in skip:
            print >> sys.stderr, f.fltid
            changefilter(f)
    return len(fs) - len(skip)

n = replace_trade_filters()
print >> sys.stderr, "Replaced %d trade filters" % n
