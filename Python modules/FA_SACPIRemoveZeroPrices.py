# FA_SACPIRemoveZeroPrices
# Clears bit field for zero prices for SACPI index so that these prices
# are not considered in Prime
#
# 2009-07-15    bs      initial version

import ael
import sys

BIT_BID = 1
BIT_ASK = 1<<1
BIT_NBI = 1<<2
BIT_NAS = 1<<3
BIT_LAS = 1<<4
BIT_HIG = 1<<5
BIT_LOW = 1<<6
BIT_OPE = 1<<7

def clearPrice(ins):
    n_changed = 0
    for p in ins.prices():
        bits = 0
        if p.bid == 0.0:
            bits += (BIT_BID + BIT_NBI)
        if p.ask == 0.0:
            bits += (BIT_ASK + BIT_NAS)
        if p.last == 0.0:
            bits += BIT_LAS
        if p.high == 0.0:
            bits += BIT_HIG
        if p.low == 0.0:
            bits += BIT_LOW
        if p.open == 0.0:
            bits += BIT_OPE
        if bits>0:
            new_bits = p.bits & (~bits)
            if new_bits != p.bits:
                c = p.clone()
                c.bits = new_bits
                c.commit()
                n_changed += 1
    return n_changed
            
i = ael.Instrument['SACPI']
n_changed = clearPrice(i)
print('Changed %d prices' % n_changed, file=sys.stderr)
