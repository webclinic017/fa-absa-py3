import ael

CallDic={} 
for ins in ael.Instrument.select('Instype="CFD"'):
    #Creating SEDOL codes for the Underlyings of the CFD's by copying the SEDOL codes 
    #from the instrument(CFD) to the underlying in the additional Info table
    CallDic[ins.und_insaddr.insid]=ins.add_info('SEDOL')
    ins_clone=ins.und_insaddr.clone()
    addinf = ael.AdditionalInfo.new(ins_clone)
    addinf.addinf_specnbr = ael.AdditionalInfoSpec['SEDOL']
    addinf.value = CallDic[ins.und_insaddr.insid]
    addinf.commit()

    #Removing the SEDOL numbers of the CFD instruments
    c_clone=ins.clone() 
    for a in ins.additional_infos():
        #print a.pp()
        if a.addinf_specnbr.field_name == 'SEDOL':
            val = a.value
            ai = a.clone()
            print(ai.pp())
            ai.value = ''
            ai.commit()
    c_clone.commit()
    




