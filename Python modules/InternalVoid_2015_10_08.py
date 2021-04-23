import acm
 
trdGroup = [54096591, 54096590, 54096589, 54096588, 54096587, 54096586]
 
acm.BeginTransaction()
try:
    for t in trdGroup:
        trd = acm.FTrade[t]
        trd.Status('Void')
        trd.Commit()   
    acm.CommitTransaction()
except Exception as ex:
    acm.AbortTransaction()
    raise ex
