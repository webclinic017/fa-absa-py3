import acm

t = acm.FTrade[100420170]
t1 = acm.FTrade[100291146]

d = t.Difference(t1)
for each in d.Keys():
    print(each, '->',  d[str(each)])
#print d['acquireDay']

#print d.Values()

#print t.Instrument().Legs()
