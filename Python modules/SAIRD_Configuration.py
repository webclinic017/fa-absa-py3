import ael

#trds = ael.Trade.select('creat_time=ael.date_today()')

Swap = ael.Instrument.read('insid="SwapDefault"')
legs = ael.Leg.select('insaddr=%d'%Swap.insaddr)
print Swap.instype
detail = []
detail.append(('Valgroup', Swap.product_chlnbr))
for l in legs:
    if l.type == 'Float':
    	Receive = l.payleg
	print 'Receive ', Receive
    elif l.type == 'Fixed':
    	Pay = l.payleg
	print Pay

