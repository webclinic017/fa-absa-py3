import ael
oldAcq = ael.Party['EQ Derivatives Desk']
newAcq = ael.Party['Eq Derivative Desk']
trades = ael.Trade.select('acquirer_ptynbr = %d' %oldAcq.ptynbr)
print(trades)
for t in trades:
    tclone = t.clone()
    tclone.acquirer_ptynbr = newAcq
    tclone.commit()
