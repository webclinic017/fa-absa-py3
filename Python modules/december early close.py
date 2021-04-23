'''

early ZAR stocks and equity indexes APH adjustments for early close in December 2017
coded by Anil Parbhoo
reinstatement is defined in 'roll back december early close.py'
'''

import acm

pls = acm.FPriceLinkDefinition.Select('')

print   'pl.Oid()', ',', 'pl.Instrument().InsType()', ',', 'pl.Instrument().Name()', ',', 'pl.Currency().Name()', ',', 'pl.StartTime()', ',', 'pl.StopTime()', ',', 'pl.SemanticSeqNbr().Name()', ',', 'Details of change'


for pl in pls:
    if pl.Market().Oid()==10 and pl.Instrument().Currency().Oid()==2 and (pl.Oid() not in [4865, 3481]):
        if pl.Instrument().InsType() in ['Stock', 'EquityIndex'] and pl.SemanticSeqNbr().Name()=='STK':
            #print   pl.Oid(), ',', pl.Instrument().InsType(),',', pl.Instrument().Name(),',',  pl.Currency().Name(),',', pl.StartTime(),',', pl.StopTime(),',', pl.SemanticSeqNbr().Name(),',', 'stop at 720'
            
            try:
                pl.StopTime(720)
                pl.Commit()
                print  pl.Oid(), ',', pl.Instrument().InsType(), ',', pl.Instrument().Name(), ',',  pl.Currency().Name(), ',', pl.StartTime(), ',', pl.StopTime(), ',', pl.SemanticSeqNbr().Name()
            except:
                print '%s could NOT amend aph stop time for %s' % (pl.Oid(), pl.Instrument().Name())
            
        elif pl.Instrument().InsType() in ['Stock', 'EquityIndex'] and pl.SemanticSeqNbr().Name()in ['STKCLS', 'CLS']:
            #print   pl.Oid(), ',', pl.Instrument().InsType(),',', pl.Instrument().Name(),',',  pl.Currency().Name(),',', pl.StartTime(),',', pl.StopTime(),',', pl.SemanticSeqNbr().Name(),',', 'start 720 stop at 810'
            
            try:
                pl.StartTime(720)
                pl.StopTime(810)
                pl.Commit()
                print  pl.Oid(), ',', pl.Instrument().InsType(), ',', pl.Instrument().Name(), ',',  pl.Currency().Name(), ',', pl.StartTime(), ',', pl.StopTime(), ',', pl.SemanticSeqNbr().Name()
            except:
                print '%s could NOT amend aph1 start and stop time for %s' % (pl.Oid(), pl.Instrument().Name())
            
                
        elif pl.Instrument().InsType() == 'EquityIndex' and (pl.SemanticSeqNbr().Name() not in ['STKCLS', 'CLS']):
            #print   pl.Oid(), ',', pl.Instrument().InsType(),',', pl.Instrument().Name(),',',  pl.Currency().Name(),',', pl.StartTime(),',', pl.StopTime(),',', pl.SemanticSeqNbr().Name(),',', 'stop at 810'
            
            try:
            
                pl.StopTime(810)
                pl.Commit()
                print pl.Oid(), ',', pl.Instrument().InsType(), ',', pl.Instrument().Name(), ',',  pl.Currency().Name(), ',', pl.StartTime(), ',', pl.StopTime(), ',', pl.SemanticSeqNbr().Name()
            
            except:
                print '%s could NOT amend aph stop time for %s' % (pl.Oid(), pl.Instrument().Name())
            
            
