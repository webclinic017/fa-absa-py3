import ael, acm
from at_time import to_timestamp, to_datetime
from datetime import datetime

mapping = [
{'source_portfolio': '43091 EQ_SA_StockVol', 'target_portfolio': 'IARBF'},
{'source_portfolio': 'Delta One 4 45096', 'target_portfolio': '45153 SSF1'},
{'source_portfolio': '41103_SSF_DMA', 'target_portfolio': 'Brad_OTC'},
{'source_portfolio': '45104 Barcap Flow', 'target_portfolio': 'Brad_OTC'},
{'source_portfolio': '45120 MSCI Breakable', 'target_portfolio': '45112 USD Breakable SS'},
{'source_portfolio': '45138_IDX_2', 'target_portfolio': '45005'},
{'source_portfolio': '45179 SSF3', 'target_portfolio': '45153 SSF1'},
{'source_portfolio': '45187 STX', 'target_portfolio': '45005'},
{'source_portfolio': '45203 EFP', 'target_portfolio': '45005'},
{'source_portfolio': '45211 Market Making', 'target_portfolio': '45005'},
{'source_portfolio': '45229 Pairs Trading', 'target_portfolio': '45146 ZAR Breakable SS'},
{'source_portfolio': '46102 Structured Hedges', 'target_portfolio': '45146 ZAR Breakable SS'},
{'source_portfolio': 'BRADS', 'target_portfolio': 'Brad_OTC'},
{'source_portfolio': 'Breakable Other', 'target_portfolio': '45112 USD Breakable SS'},
{'source_portfolio': 'D1 Structures', 'target_portfolio': 'Brad_OTC'},
{'source_portfolio': 'Delta One 1 45062', 'target_portfolio': '45005'},
{'source_portfolio': 'Delta One 2 47605', 'target_portfolio': '45005'},
{'source_portfolio': 'EQ_SA_PairsOption', 'target_portfolio': 'PROPT'},
{'source_portfolio': 'Zimbabwe Equities', 'target_portfolio': 'Nigeria Equities'}
]

for entry in mapping:

    source_portfolio = acm.FPhysicalPortfolio[entry['source_portfolio']]
    target_portfolio = acm.FPhysicalPortfolio[entry['target_portfolio']]
    
    query = r'''
        select t.trdnbr
        from trade t join instrument i on i.insaddr = t.insaddr
        where t.prfnbr = %s
    ''' % source_portfolio.Oid()
    
    res = ael.dbsql(query)[0]
    
    for trdnbr, in res:
        ael.log('Moved trade %s from %s to %s' % (trdnbr, source_portfolio.Name(), target_portfolio.Name()))
    
    query = r'''
        update trade
        set prfnbr = %s,
        updat_usrnbr = %s,
        updat_time = %s
        from trade t join instrument i on i.insaddr = t.insaddr
        where t.prfnbr = %s
    ''' % (target_portfolio.Oid(), acm.FUser['FMAINTENANCE'].Oid(), '21/11/2015', source_portfolio.Oid())
    
    
    ael.dbsql(query)
