import ael
def resetnumb(l,payday,*rest):
    A = []
    day = payday.to_string()
    for r in l.cash_flows():
    	A.append(r.pay_day.to_string())
    A.sort()
    count = 1
    C = {}
    for i in A:
    	C['%s' %i] = count
    	count = count + 1	
    return C[day]
