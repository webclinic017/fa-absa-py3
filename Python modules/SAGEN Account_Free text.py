import ael
list = ['FX EMMERGING MKTS', 'FX EURO FUNDING', 'FX FORWARD', 'FX SPOT']
for p in list:
    partycl = ael.Party[p]
    for ac in partycl.accounts():
    	print ac
    	accl = ac.clone()
	accl.name = 'DEFAULT-' + accl.curr.insid
	accl.accounting = 'TT-FX-Default'
	accl.commit()
