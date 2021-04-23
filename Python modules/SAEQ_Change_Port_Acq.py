import ael
old_pty = ael.Party['EQ Derivatives Desk']
new_pty = ael.Party['Eq Derivative Desk']
print old_pty, new_pty
port = ael.Portfolio.select('owner_ptynbr = %d' %old_pty.ptynbr)
print port
for p in port:
    pclone = p.clone()
    pclone.owner_ptynbr = new_pty.ptynbr
    pclone.commit()
