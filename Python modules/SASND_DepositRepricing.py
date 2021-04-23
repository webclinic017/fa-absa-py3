'''
Purpose:                [Optimize code and ensure that only unique instruments
                        are being added to the yield curve.],[The code has been modified
                        to upload instrumets spreads from the tradeFilter:AbCap_VALUING FOR OWN CREDIT into the ZAR-Swap curve.]
Department and Desk:    [PCG SND],[PCG SM SND]
Requester:              [Dumisani Mkhonza], [Lott Chidawaya]
Developer:              [Heinrich Cronje],[Tshepo Mabena]
CR Number:              [229553],[732873]
'''

import ael

def Create_FRN_InstrSprd(yieldCurve, tradeFilter, undCurve):  

    yc    = ael.YieldCurve[yieldCurve].clone()
    isprd = yc.instrument_spreads().members()
    
    for x in isprd:
        x.delete()    
    ael.poll()
    
    inst = {}
    
    for filter, flag in tradeFilter.iteritems():
        
        tf = ael.TradeFilter[filter]    
                
        for t in tf.trades():
            if not inst.has_key(t.insaddr.insid):
                inst[t.insaddr.insid] = (t, flag)
               
    for i in inst:
               
        ins = ael.Instrument[i]
        x = ael.InstrumentSpread.new(yc)
        x.instrument = ins.insaddr
        x.underlying_yield_curve_seqnbr = ael.YieldCurve[undCurve]
        if ins.instype == 'FRN':
            x.spread_type = 'Disc Marg'
        else:
            x.spread_type = 'YTM'

        if inst[i][1]:
            x.spread = ins.legs()[0].spread / 100.0        
                               
        elif inst[i][0].add_info('SND Contract Spread') == '':
            x.spread = 0 
                     
        else:
            x.spread = float(inst[i][0].add_info('SND Contract Spread')) / 100.0
               
    try:
        yc.commit()
        print 'Yield curve committed'
    except:
        print 'Could not save the yield curve'

ZAR_Curve = {'SND_All_Internal Deposit FV':0,'AbCap_VALUING FOR OWN CREDIT':1}
USD_Curve = {'SND_FV_FILTER_DEPOSITS_USD' :0}
   
Create_FRN_InstrSprd('USD-SWAP-SND_CS', USD_Curve, 'USD-SWAP')
Create_FRN_InstrSprd('ZAR-SWAP-SND_CS', ZAR_Curve, 'ZAR-SWAP')

