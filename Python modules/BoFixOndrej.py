import acm

trades = ['91561240',
         '91859676',
         '93271398',
         '93401712',]
         
for trdnbr in trades:
    t = acm.FTrade[trdnbr]
    t.MirrorTrade(None)
    t.Status('BO Confirmed')
    t.Commit()
