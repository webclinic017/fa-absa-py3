import ael 
import sys

vsl = ael.Volatility.select()

for vs in vsl:
    try:
        if ael.Instrument[vs.vol_name[0:3]].instype == 'Curr' and ael.Instrument[vs.vol_name[3:6]].instype == 'Curr':

            print >> sys.stderr, vs.vol_name, vs.vol_name[0:3], vs.vol_name[3:6]
            i1 = ael.Instrument[vs.vol_name[0:3]]
            i2 = ael.Instrument[vs.vol_name[3:6]]
            print >> sys.stderr, i1.instype, i2.instype 
            vsc = vs.clone()
            
            if ael.CurrencyPair[i1.insid+'/'+i2.insid]:
                vsc.curr_pair_seqnbr = ael.CurrencyPair[i1.insid+'/'+i2.insid]
                print >> sys.stderr, 'Curr pair 1/2 is', vsc.curr_pair_seqnbr.name

            elif ael.CurrencyPair[i2.insid+'/'+i1.insid]:
                vsc.curr_pair_seqnbr = ael.CurrencyPair[i2.insid+'/'+i1.insid]
                print >> sys.stderr, 'Curr pair 2/1 is', vsc.curr_pair_seqnbr.name
                
            else:
                print >> sys.stderr, 'No Curr pair'
            vsc.commit()

    except:
        if 1 == 2:
            print >> sys.stderr, vs.vol_name, 'Failed'
