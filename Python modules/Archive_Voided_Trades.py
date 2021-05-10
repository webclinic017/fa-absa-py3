import ael

trades = ael.TradeFilter['Archive'].trades()
for t in trades:
 tc = t.clone()
 tc.archive_status = 1
 tc.commit()
