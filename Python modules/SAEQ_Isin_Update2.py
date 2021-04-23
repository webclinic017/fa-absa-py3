import ael, string
try:
    Dual=open('C:\ISIN.csv')
except:
    print'Problem opening file'
line=Dual.readline()
CallDic={}
while line:
        line=Dual.readline()
        l=string.split(line, ',')
        if l[0]=='':break
        l[1]='ZAR/'+l[1]
        #print l[0],l[1]
        CallDic[l[1]] = l[0]
print CallDic

#print dir(CallDic)
for s in ael.Instrument.select('Instype = "Stock"'):
    
    if CallDic.has_key(s.insid):
        isin = CallDic[s.insid]
        c = s.insid + '/CFD'
        cfd = ael.Instrument[c]
        try:
            c_clone=cfd.clone()   
        except:
            print'Problem cloning instrument:', c
        #print cfd.isin
        c_clone.isin=''
        c_clone.commit()
        s_clone=s.clone()
        s_clone.isin=isin
        try:
            s_clone.commit()
        except:
            print'Problem committing instrument:', s.insid        
Dual.close()
