import ael, acm
def setcfaddinfo(temp,cfnbr,aivalue,*rest):
    try:
        cf = ael.CashFlow[(int)(cfnbr)].clone()
        val = 0
        for ac in cf.additional_infos():
            if ac.addinf_specnbr.field_name == 'Call Midas_nbr':
                val = ac 
                break
        sp = ael.AdditionalInfoSpec['Call Midas_nbr']
        spec = sp.specnbr
        add = ael.AdditionalInfo.select('addinf_specnbr =' + str(spec))
        new_number = aivalue
        flag = 0
        for x in add:
            if int(x.value) == int(new_number):
                flag = 1
                s = 'ERROR: This Midas number', x.value, ' is already in use'
                func=acm.GetFunction('msgBox', 3)
                func("ERROR", s, 0)

        if flag == 0:
            if val:
                valc = val.clone()
                valc.value = aivalue
                valc.commit()
            else:
                add = ael.AdditionalInfo.new(cf)
                spec = ael.AdditionalInfoSpec['Call Midas_nbr']
                add.addinf_specnbr = spec
                add.value = aivalue
                add.commit()
            return 'Updated'
        else:
            return 'Not Updated'
    except:
        return 'Not Updated'
