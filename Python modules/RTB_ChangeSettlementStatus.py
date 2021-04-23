import acm

settlements = [2653405]
for s in settlements:      
    try:
        acm.BeginTransaction()
        sett = acm.FSettlement[s]
        
        sett.Status('Settled')
        sett.Commit()
        print('Settlement %s set to Settled' %s)
        acm.CommitTransaction()
        
        
    except Exception:
        sett.Undo()
