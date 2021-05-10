import ael

def update_add_info(temp,cfwnbr,value,*rest):
    cf = ael.CashFlow[(int)(cfwnbr)]
    flag = 0
    for a in cf.additional_infos():
        if a.addinf_specnbr.field_name == 'Settle_Type':
            flag = a.valnbr
    if flag:
        a = ael.AdditionalInfo[flag].clone()
        a.value = value
        a.commit()
    else:
        ais = ael.AdditionalInfoSpec['Settle_Type']
        tc = cf.clone()
        an = ael.AdditionalInfo.new(tc)
        an.value = value
        an.addinf_specnbr = ais
        an.commit()
    
    return 'Done'
