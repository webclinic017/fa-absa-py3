import acm

t = acm.FTrade[84916299]
ins = acm.FInstrument['ZAR/171018-181017/SARB']
t.Instrument(ins)
try:
    t.Commit()
    print('Update successful...')
except Exception, e:
    print(e)
