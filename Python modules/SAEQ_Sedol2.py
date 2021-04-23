import ael, string
try:
    SED=open('C:\SEDOL.csv')
except:
    print'Problem opening file'
line=SED.readline()
CallDic={}
while line:
        line=SED.readline()
        l=string.split(line, ',')
        if l[0]=='':break
        l[1]='ZAR/'+l[1]
        #print l[0],l[1]
        CallDic[l[1]] = l[0]
print CallDic

for s in ael.Instrument.select('Instype="Stock"'):
    #Creating SEDOL codes for the Stocks by copying the SEDOL codes 
    #from the file to the Stocks in the additional Info table
    if CallDic.has_key(s.insid):
        sedol = CallDic[s.insid]
        s_clone=s.clone()
        
        for a in s.additional_infos():
            if a.addinf_specnbr.field_name == 'SEDOL':
                sedol_clone = a.clone()
                sedol_clone.value = sedol
                sedol_clone.commit()
        
        s_clone.commit()

SED.close()
