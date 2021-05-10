import ael

def CP_Portf(temp,trade,*rest):
    t = ael.Trade[trade]
    if t.mirror_trdnbr:
        if t.mirror_trdnbr.trdnbr == trade:
            mirrorT = ael.Trade.select('mirror_trdnbr=%i' %trade)
            for tr in mirrorT:
                if tr.trdnbr != trade:
                    return tr.prfnbr.prfid
        else:
            return t.mirror_trdnbr.prfnbr.prfid

