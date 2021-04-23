import acm
ins = ['ZAR/GEN/ZC/CPI/SWAP/1M',
'ZAR/GEN/ZC/CPI/SWAP/2M',
'ZAR/GEN/ZC/CPI/SWAP/3M',
'ZAR/GEN/ZC/CPI/SWAP/4M',
'ZAR/GEN/ZC/CPI/SWAP/5M',
'ZAR/GEN/ZC/CPI/SWAP/6M',
'ZAR/GEN/ZC/CPI/SWAP/7M',
'ZAR/GEN/ZC/CPI/SWAP/8M',
'ZAR/GEN/ZC/CPI/SWAP/9M',
'ZAR/GEN/ZC/CPI/SWAP/10M',
'ZAR/GEN/ZC/CPI/SWAP/11M',
'ZAR/GEN/ZC/CPI/SWAP/1Y',
'ZAR/GEN/ZC/CPI/SWAP/13M',
'ZAR/GEN/ZC/CPI/SWAP/14M',
'ZAR/GEN/ZC/CPI/SWAP/15M',
'ZAR/GEN/ZC/CPI/SWAP/16M',
'ZAR/GEN/ZC/CPI/SWAP/17M',
'ZAR/GEN/ZC/CPI/SWAP/18M',
'ZAR/GEN/ZC/CPI/SWAP/2Y',
'ZAR/GEN/ZC/CPI/SWAP/3Y',
'ZAR/GEN/ZC/CPI/SWAP/4Y',
'ZAR/GEN/ZC/CPI/SWAP/5Y',
'ZAR/GEN/ZC/CPI/SWAP/6Y',
'ZAR/GEN/ZC/CPI/SWAP/7Y',
'ZAR/GEN/ZC/CPI/SWAP/8Y',
'ZAR/GEN/ZC/CPI/SWAP/9Y',
'ZAR/GEN/ZC/CPI/SWAP/10Y',
'ZAR/GEN/ZC/CPI/SWAP/12Y',
'ZAR/GEN/ZC/CPI/SWAP/15Y',
'ZAR/GEN/ZC/CPI/SWAP/20Y',
'ZAR/GEN/ZC/CPI/SWAP/25Y',
'ZAR/GEN/ZC/CPI/SWAP/30Y']

markets = ['SPOT', 'SPOT_MID', 'SPOT_SOB', 'internal']

for i in ins:
    for m in markets:
        try:
            instr = acm.FInstrument[i]
            price = acm.FPrice.Select01('instrument="%s" market="%s" day="%s" currency="%s"' % (i, m, acm.Time().DateToday(), 'ZAR'), '')
            clone = price.Clone()
            price.Delete()
            clone.Commit()
        except Exception as e:
            pass
        
