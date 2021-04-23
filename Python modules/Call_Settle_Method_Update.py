import ael, SAGEN_Set_Additional_Info_new

def update_Call_Settle_Method(temp,cfwnbr,*rest):
    try:
        cf = ael.CashFlow[cfwnbr]
        set = ael.Settlement.select('cfwnbr=%f' %cfwnbr)
        if set.members() != []:
            for s in set:
                if s.ref_seqnbr == None:
                    found = 0
                    addinf = ael.AdditionalInfo.select('addinf_specnbr=661') #Call_Settle_Method
                    for ai in addinf:
                        if ai.recaddr == s.seqnbr:
                            found = 1
                            return 'Already Exist'
                            break
                    if not found:
                        SAGEN_Set_Additional_Info_new.setAddInfoEntity(s, 'Call_Settle_Method', cf.add_info('Settle_Type'))
                        return 'Updated'
        else:
            return 'Not Updated'
    except:
        return 'Not Updated'
