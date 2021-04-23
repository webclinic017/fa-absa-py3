import ael

def change(ssi,settle_cf_type,*rest):
    ssi_clone = ssi.clone()
    ssi_clone.settle_cf_type = settle_cf_type
    try:
        ssi_clone.commit()
        return 'settle_cf_type ' + (str)(ssi.seqnbr) + ' Fine'
    except:
        return 'settle_cf_type ' + (str)(ssi.seqnbr) + ' Error'

def insid(ssi,*rest):
    ssi_clone = ssi.clone()
    ssi_clone.settleid = ssi.settleid[0:len(ssi.settleid)-1] + 'a'
    try:
        ssi_clone.commit()
        return 'settleid ' + (str)(ssi.seqnbr) + ' Fine'
    except:
        print 'settleid ' + (str)(ssi.seqnbr) + ' Error'
        return 'settleid ' + (str)(ssi.seqnbr) + ' Error'
        
ssiTRS = ael.SettleInstruction.select('instype = "TotalReturnSwap"')

#ssiTRS = []
#ssiTRS.append(ael.SettleInstruction[29140])

for ssi in ssiTRS:
    if ssi.settle_cf_type == 'Fixed Amount':
        print change(ssi, 'Total Return')
    elif ssi.settle_cf_type == 'Dividend':
        print change(ssi, 'Cashflow Dividend')

ael.poll()

for ssi in ssiTRS:
    ael.poll()
    print insid(ssi)
