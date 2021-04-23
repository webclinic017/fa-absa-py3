'''
RollBack - early ZAR stocks and equity indexes APH adjustments for early close in December 2017
coded by Anil Parbhoo

'''

import acm

pls = acm.FPriceLinkDefinition.Select('')

print   'pl.Oid()', ',', 'pl.Instrument().InsType()', ',', 'pl.Instrument().Name()', ',', 'pl.Currency().Name()', ',', 'pl.StartTime()', ',', 'pl.StopTime()', ',', 'pl.SemanticSeqNbr().Name()', ',', 'Details of change'


for pl in pls:
    if pl.Market().Oid()==10 and pl.Instrument().Currency().Oid()==2 and (pl.Oid() not in [4865, 3481]):
        if pl.Instrument().InsType() in ['Stock', 'EquityIndex'] and pl.SemanticSeqNbr().Name()=='STK':
            #print   pl.Oid(), ',', pl.Instrument().InsType(),',', pl.Instrument().Name(),',',  pl.Currency().Name(),',', pl.StartTime(),',', pl.StopTime(),',', pl.SemanticSeqNbr().Name(),',', 'stop at 1025'
            
            try:
                pl.StopTime(1025)
                pl.Commit()
                print  pl.Oid(), ',', pl.Instrument().InsType(), ',', pl.Instrument().Name(), ',',  pl.Currency().Name(), ',', pl.StartTime(), ',', pl.StopTime(), ',', pl.SemanticSeqNbr().Name()
            except:
                print '%s could NOT amend aph stop time for %s' % (pl.Oid(), pl.Instrument().Name())
            
        elif pl.Instrument().InsType() in ['Stock', 'EquityIndex'] and pl.SemanticSeqNbr().Name()in ['STKCLS', 'CLS']:
            #print   pl.Oid(), ',', pl.Instrument().InsType(),',', pl.Instrument().Name(),',',  pl.Currency().Name(),',', pl.StartTime(),',', pl.StopTime(),',', pl.SemanticSeqNbr().Name(),',', 'start 1025 stop at 1095'
            
            try:
                pl.StartTime(1025)
                pl.StopTime(1095)
                pl.Commit()
                print  pl.Oid(), ',', pl.Instrument().InsType(), ',', pl.Instrument().Name(), ',',  pl.Currency().Name(), ',', pl.StartTime(), ',', pl.StopTime(), ',', pl.SemanticSeqNbr().Name()
            except:
                print '%s could NOT amend aph1 start and stop time for %s' % (pl.Oid(), pl.Instrument().Name())
            
                
        elif pl.Instrument().InsType() == 'EquityIndex' and (pl.SemanticSeqNbr().Name() not in ['STKCLS', 'CLS']):
            #print   pl.Oid(), ',', pl.Instrument().InsType(),',', pl.Instrument().Name(),',',  pl.Currency().Name(),',', pl.StartTime(),',', pl.StopTime(),',', pl.SemanticSeqNbr().Name(),',', 'stop at 1410'
            
            try:
            
                pl.StopTime(1410)
                pl.Commit()
                print pl.Oid(), ',', pl.Instrument().InsType(), ',', pl.Instrument().Name(), ',',  pl.Currency().Name(), ',', pl.StartTime(), ',', pl.StopTime(), ',', pl.SemanticSeqNbr().Name()
            
            except:
                print '%s could NOT amend aph stop time for %s' % (pl.Oid(), pl.Instrument().Name())
            
            
