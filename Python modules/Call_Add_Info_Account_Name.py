import ael, string

file = 'C:\As_End_day\Call_Account\InsidUpload.csv'

try:
    f = open(file)
except:
    print'Problem opening file'
    
line = f.readline()

while line:
    line = f.readline()
    line = line.rstrip()
    l = string.split(line, ',')
    if (l[0] == '\n' or l[0] == ''): break
    try:
        ins = ael.Instrument[l[0]]
    except:
        print 'error:' + l[0]
    
    if ins:
        for tr in ins.trades():
            flag = 0
            for a in tr.additional_infos():
                if a.addinf_specnbr.field_name == 'Account_Name':
                    flag = a.valnbr
            if flag:
                a = ael.AdditionalInfo[flag].clone()
                a.value = l[1]
                a.commit()
            else:
                ais = ael.AdditionalInfoSpec['Account_Name']
                tc = tr.clone()
                an = ael.AdditionalInfo.new(tc)
                an.value = l[1]
                an.addinf_specnbr = ais
                an.commit()
f.close()


