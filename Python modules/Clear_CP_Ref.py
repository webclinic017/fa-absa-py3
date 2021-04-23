import ael

trades = ael.Trade.select()
count = 0
for t in trades:
    if t.your_ref == '0':
    	count = count + 1
	if t.status not in ('Void', 'Simulated'):
	    t_clone = t.clone()
	    t_clone.your_ref = ''
    	    print('Trade', t_clone.trdnbr, '  Updated t.your_ref = ', t_clone.your_ref)
	    t_clone.commit()


print()
print(count, 'trades updated')
