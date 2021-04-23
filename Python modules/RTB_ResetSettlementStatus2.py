import acm

settlements = [2585699]

for s in settlements:      
    try:
        acm.BeginTransaction()
        sett = acm.FSettlement[s]
        
        sett.Status('Released')
        sett.Commit()
        print('Settlement %s set to Released' %s)
           
        acm.CommitTransaction()
    except Exception:
        sett.Undo()
