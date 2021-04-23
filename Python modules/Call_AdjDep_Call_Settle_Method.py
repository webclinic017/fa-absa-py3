import ael, SAGEN_Set_Additional_Info

def Call_Settle_Method(cfwnbr, settl_type):
    settl = ael.Settlement.select('cfwnbr=%i' %(cfwnbr))
    for s in settl:
        SAGEN_Set_Additional_Info.main(settl, (str)(s.seqnbr), 'Call_Settle_Method', settl_type)


