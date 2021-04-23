import acm

settlements = [2585699]
for s in settlements:      
    try:
        acm.BeginTransaction()
        sett = acm.FSettlement[s]
        
        sett.Status('Not Acknowledged')
        sett.Commit()
        
        sett.Status('Exception')
        sett.Commit()
      
        sett.Status('Authorised')
        sett.Commit()
        print('Settlement %s set to Authorised' %s)
        acm.CommitTransaction()
        
        
    except Exception:
        sett.Undo()
