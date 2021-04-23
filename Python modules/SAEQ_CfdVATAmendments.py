import ael


success=[]
failed=[]
trd = ael.TradeFilter['CFD']

for t in trd.trades():
    t_clone = t.clone()
    ais = t.additional_infos()
    for ai in ais:
        if ai.addinf_specnbr.field_name == ('VAT'):
            ai_clone = ai.clone()
            #print dir(ai_clone)
            ai_clone.value = 'FULL'
            #addinf.addinf_specnbr = ael.AdditionalInfoSpec['VAT']
            #addinf.value = 'FULL'

        try:
            ai_clone.commit()
            t_clone.commit()
            success.append(t.trdnbr)
        except:
            failed.append(t.trdnbr)
            
print 'success', success
print 'failed', failed

