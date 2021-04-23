import ael, string
subtype = 'C:\subtypeup.csv'
try:   
    sub = open(subtype)
except:
    print 'Problem opening file'

line = sub.readline()
line = sub.readline()
dic={}
count=0
fail_list=[]
while line:
    Type = string.split(line, ',')
    dic[Type[0]] = Type[4]
    type = Type[4]
    nbr = (int)(Type[0])
    trd = ael.Trade[nbr]
    t_trade = trd.clone()
    fund = trd.additional_infos()
    flag = 'no'
    for fun in fund:
        print t_trade.trdnbr, fun.addinf_specnbr.field_name, fun.pp()
        if fun.addinf_specnbr.field_name == 'Funding Instype':
            if fun.value == ''  :
                flag = 'old'
                break
            else:
                flag = 'yes'
        else:
            flag = 'no'
            break
    
    if flag == 'no':
        print flag
        addinf = ael.AdditionalInfo.new(t_trade)
        addinf.addinf_specnbr = ael.AdditionalInfoSpec['Funding Instype']
        addinf.value = Type[4]
        print addinf.pp()
        addinf.commit()
    elif flag == 'old':
        for fun in fund:
            if fun.addinf_specnbr.field_name == 'Funding Instype':
                fund_clone = fun.clone()
                print type, Type[0]
                fund_clone.value = type
                fund_clone.commit()
    else:
        fail_list.append(t_trade.trdnbr)
        
    try:
        t_trade.commit()
        print 'Trade %i comitted succesfully' %(t_trade.trdnbr)
        count = count + 1
    except:
        print 'Error committing trade ', t_trade.trdnbr	
        fail_list.append(t_trade.trdnbr)

    if len(dic) == 3188:
        break
    else:
        line = sub.readline()   
sub.close()
print count
print fail_list    
    
    
