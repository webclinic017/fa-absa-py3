import acm, ael

def change_instrument(p):
    new_ins = p.Instrument().Name().replace("ZAR/GEN-ZC/REAL/", "ZAR/GEN/ZC/CPI/SWAP/")
    clone = p.Clone()
    clone.Instrument(new_ins)
    clone.Commit()


acm.BeginTransaction()
for b in acm.FYieldCurve['ZAR-CPI'].Benchmarks():  
    instrument = b.Instrument()

    for p in  list(instrument.HistoricalPrices()):
        p.Delete()
    for p in  list(instrument.Prices()):
        p.Delete()
acm.CommitTransaction()

for b in acm.FYieldCurve['ZAR-REAL'].Benchmarks():  
    acm.BeginTransaction()
    instrument = b.Instrument()
    for p in  list(instrument.HistoricalPrices()):
        if p.Day() > "2013-12-30":
            change_instrument(p)
    acm.CommitTransaction()
