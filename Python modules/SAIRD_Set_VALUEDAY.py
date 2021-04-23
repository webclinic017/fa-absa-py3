import ael
trds = ael.TradeFilter['SAIRD_MB_IRP'].trades()
print(trds)
for t in trds:
    tc = t.clone()
    tc.time = ael.date_today().add_days(-1).to_time()
    tc.commit()
print('..Done..')
