import acm

instrument = acm.FInstrument["ZAR/NFGOVI"]
trade1 = acm.FTrade[87174054]
trade2 = acm.FTrade[87174055]

acm.BeginTransaction()
try:
    trade1.Status("Void")
    trade1.Commit()
    trade2.Status("Void")
    trade2.Commit()
    for dividend in instrument.Dividends():
        dividend.Delete()
    acm.CommitTransaction()
except Exception as ex:
    acm.AbortTransaction()
    print("Error:", ex)
print("Finished")
