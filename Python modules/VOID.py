import acm

acm.BeginTransaction()
try:
    t1 = acm.FTrade[87915041]
    t1.Status('Void')
    t1.Commit()
    
    
    t2 = acm.FTrade[87915042]
    t2.Status('Void')
    t2.Commit()
    
    acm.CommitTransaction()
except Exception as exc:
    acm.AbortTransaction()
    print(exc)
