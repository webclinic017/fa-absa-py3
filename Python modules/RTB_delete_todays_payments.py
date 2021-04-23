import acm, ael

fname='F:/Input_File.txt'
f=open(fname, 'r')
x='\t'
dict_n={}
for line in f.readlines():
    line=line.replace('\n', '')
    data_vect=line.split('\t')
    trade=acm.FTrade[data_vect[0]]
    amount_v=data_vect[1]    
    try:
        d=ael.date(data_vect[2])
        for p in trade.Payments():
            if d==ael.date(p.PayDay()):
                print trade.Name(), x, p.Amount(), x, amount_v, x, 'To be amended'
                p.Amount(amount_v)
                trade.Commit()
                print 'Successful'
    except:
        dict_n[trade.Name()]=[data_vect[0], data_vect[1], data_vect[2], 'Do not convert']

print 'ERRORS'
for elem in dict_n:
    print dict_n[elem]
