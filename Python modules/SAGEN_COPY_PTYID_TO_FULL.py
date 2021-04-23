import ael
ptys = ael.Party.select()
for pty in ptys:
    if pty.fullname == '' and pty.type != 'None':
    	p = pty.clone()
    	print pty.ptyid, ' FULL: ', pty.fullname, ' TYPE: ', pty.type
    	p.fullname = pty.ptyid
	p.commit()
